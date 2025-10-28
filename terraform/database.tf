# Database Configuration for E-commerce
# RDS PostgreSQL with high availability and security

# =============================================================================
# RDS Subnet Group
# =============================================================================

resource "aws_db_subnet_group" "main" {
  name       = "${local.name_prefix}-db-subnet-group"
  subnet_ids = aws_subnet.database[*].id
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-db-subnet-group"
  })
}

# =============================================================================
# RDS Parameter Group
# =============================================================================

resource "aws_db_parameter_group" "main" {
  family = "postgres15"
  name   = "${local.name_prefix}-db-params"
  
  parameter {
    name  = "log_statement"
    value = "all"
  }
  
  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }
  
  parameter {
    name  = "log_connections"
    value = "1"
  }
  
  parameter {
    name  = "log_disconnections"
    value = "1"
  }
  
  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-db-params"
  })
}

# =============================================================================
# RDS Instance
# =============================================================================

resource "aws_db_instance" "main" {
  identifier = "${local.name_prefix}-db"
  
  # Engine
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  # Storage
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true
  
  # Database
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  # Network
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  
  # Backup
  backup_retention_period = var.db_backup_retention_period
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # Monitoring
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring.arn
  
  # Performance Insights
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  
  # Parameter Group
  parameter_group_name = aws_db_parameter_group.main.name
  
  # Deletion Protection
  deletion_protection = var.environment == "production" ? true : false
  skip_final_snapshot = var.environment == "production" ? false : true
  final_snapshot_identifier = var.environment == "production" ? "${local.name_prefix}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null
  
  # Multi-AZ for production
  multi_az = var.environment == "production" ? true : false
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-db"
  })
}

# =============================================================================
# RDS Monitoring Role
# =============================================================================

resource "aws_iam_role" "rds_monitoring" {
  name = "${local.name_prefix}-rds-monitoring-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-monitoring-role"
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# =============================================================================
# ElastiCache Redis
# =============================================================================

resource "aws_elasticache_subnet_group" "main" {
  name       = "${local.name_prefix}-cache-subnet-group"
  subnet_ids = aws_subnet.database[*].id
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-cache-subnet-group"
  })
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "${local.name_prefix}-redis"
  description                = "Redis cluster for e-commerce"
  
  # Node Configuration
  node_type                  = var.redis_node_type
  port                       = 6379
  parameter_group_name       = aws_elasticache_parameter_group.redis.name
  
  # Cluster Configuration
  num_cache_clusters         = var.redis_num_cache_clusters
  automatic_failover_enabled  = var.redis_automatic_failover_enabled
  multi_az_enabled          = var.redis_multi_az_enabled
  
  # Network Configuration
  subnet_group_name         = aws_elasticache_subnet_group.main.name
  security_group_ids        = [aws_security_group.redis.id]
  
  # Backup Configuration
  snapshot_retention_limit  = var.redis_snapshot_retention_limit
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"
  
  # Encryption
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  # Auth
  auth_token = var.redis_auth_token
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis"
  })
}

resource "aws_elasticache_parameter_group" "redis" {
  family = "redis7.x"
  name   = "${local.name_prefix}-redis-params"
  
  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }
  
  parameter {
    name  = "timeout"
    value = "300"
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis-params"
  })
}

# =============================================================================
# Secrets Manager
# =============================================================================

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${local.name_prefix}-db-password"
  description             = "Database password for e-commerce"
  recovery_window_in_days = 7
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-db-password"
  })
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

# =============================================================================
# CloudWatch Alarms
# =============================================================================

resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${local.name_prefix}-rds-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors RDS CPU utilization"
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-cpu-alarm"
  })
}

resource "aws_cloudwatch_metric_alarm" "rds_connections" {
  alarm_name          = "${local.name_prefix}-rds-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors RDS database connections"
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rds-connections-alarm"
  })
}

resource "aws_cloudwatch_metric_alarm" "redis_cpu" {
  alarm_name          = "${local.name_prefix}-redis-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ElastiCache"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors Redis CPU utilization"
  
  dimensions = {
    CacheClusterId = aws_elasticache_replication_group.redis.id
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-redis-cpu-alarm"
  })
}

# =============================================================================
# Database Backup
# =============================================================================

resource "aws_db_instance_automated_backups_replication" "main" {
  count = var.environment == "production" ? 1 : 0
  
  source_db_instance_arn = aws_db_instance.main.arn
  kms_key_id            = aws_kms_key.rds.arn
  retention_period      = 7
  pre_signed_url        = null
}
