# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.project_name}-${var.environment}-db-subnet-group"
  }
}

# Security Group for RDS
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-rds-sg"
  }
}

# RDS Parameter Group
resource "aws_db_parameter_group" "main" {
  family = "postgres15"
  name   = "${var.project_name}-${var.environment}-db-params"

  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  parameter {
    name  = "log_checkpoints"
    value = "1"
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
    name  = "log_lock_waits"
    value = "1"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-db-params"
  }
}

# RDS Option Group
resource "aws_db_option_group" "main" {
  name                     = "${var.project_name}-${var.environment}-db-options"
  option_group_description = "Option group for ${var.project_name} ${var.environment}"
  engine_name              = "postgres"
  major_engine_version     = "15"

  tags = {
    Name = "${var.project_name}-${var.environment}-db-options"
  }
}

# RDS Database Instance
resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-${var.environment}-db"

  # Engine configuration
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.instance_class

  # Storage configuration
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 5
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id           = aws_kms_key.rds.arn

  # Database configuration
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  # Network configuration
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  # Backup configuration
  backup_retention_period = var.environment == "prod" ? 7 : 1
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  # Monitoring configuration
  monitoring_interval = var.environment == "prod" ? 60 : 0
  monitoring_role_arn = var.environment == "prod" ? aws_iam_role.rds_enhanced_monitoring[0].arn : null

  # Performance Insights
  performance_insights_enabled = var.environment == "prod" ? true : false
  performance_insights_retention_period = var.environment == "prod" ? 7 : null

  # Parameter and option groups
  parameter_group_name = aws_db_parameter_group.main.name
  option_group_name    = aws_db_option_group.main.name

  # Deletion protection
  skip_final_snapshot = var.environment != "prod"
  deletion_protection = var.environment == "prod" ? true : false

  # Multi-AZ for production
  multi_az = var.environment == "prod" ? true : false

  # Public accessibility
  publicly_accessible = false

  tags = {
    Name = "${var.project_name}-${var.environment}-db"
  }
}

# KMS Key for RDS encryption
resource "aws_kms_key" "rds" {
  description             = "KMS key for RDS encryption"
  deletion_window_in_days = 7

  tags = {
    Name = "${var.project_name}-${var.environment}-rds-kms"
  }
}

resource "aws_kms_alias" "rds" {
  name          = "alias/${var.project_name}-${var.environment}-rds"
  target_key_id = aws_kms_key.rds.key_id
}

# Enhanced Monitoring IAM Role (for production)
resource "aws_iam_role" "rds_enhanced_monitoring" {
  count = var.environment == "prod" ? 1 : 0
  name  = "${var.project_name}-${var.environment}-rds-enhanced-monitoring"

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

  tags = {
    Name = "${var.project_name}-${var.environment}-rds-enhanced-monitoring"
  }
}

resource "aws_iam_role_policy_attachment" "rds_enhanced_monitoring" {
  count      = var.environment == "prod" ? 1 : 0
  role       = aws_iam_role.rds_enhanced_monitoring[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# CloudWatch Log Groups for RDS
resource "aws_cloudwatch_log_group" "postgresql" {
  name              = "/aws/rds/instance/${var.project_name}-${var.environment}-db/postgresql"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-${var.environment}-postgresql-logs"
  }
}

# RDS Event Subscription (for production)
resource "aws_db_event_subscription" "main" {
  count     = var.environment == "prod" ? 1 : 0
  name      = "${var.project_name}-${var.environment}-db-events"
  sns_topic = aws_sns_topic.rds_events[0].arn

  source_type = "db-instance"
  source_ids  = [aws_db_instance.main.id]

  event_categories = [
    "availability",
    "deletion",
    "failover",
    "failure",
    "low storage",
    "maintenance",
    "notification",
    "recovery",
    "restoration"
  ]

  tags = {
    Name = "${var.project_name}-${var.environment}-db-events"
  }
}

# SNS Topic for RDS Events (for production)
resource "aws_sns_topic" "rds_events" {
  count = var.environment == "prod" ? 1 : 0
  name  = "${var.project_name}-${var.environment}-rds-events"

  tags = {
    Name = "${var.project_name}-${var.environment}-rds-events"
  }
}
