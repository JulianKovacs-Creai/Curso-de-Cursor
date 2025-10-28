# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-redis-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-subnet-group"
  }
}

# Security Group for Redis
resource "aws_security_group" "redis" {
  name        = "${var.project_name}-${var.environment}-redis-sg"
  description = "Security group for Redis cluster"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
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
    Name = "${var.project_name}-${var.environment}-redis-sg"
  }
}

# ElastiCache Parameter Group
resource "aws_elasticache_parameter_group" "main" {
  family = "redis7.x"
  name   = "${var.project_name}-${var.environment}-redis-params"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }

  parameter {
    name  = "timeout"
    value = "300"
  }

  parameter {
    name  = "tcp-keepalive"
    value = "60"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-params"
  }
}

# ElastiCache Replication Group (Redis Cluster)
resource "aws_elasticache_replication_group" "main" {
  replication_group_id       = "${var.project_name}-${var.environment}-redis"
  description                = "Redis cluster for ${var.project_name} ${var.environment}"

  # Engine configuration
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = var.node_type
  port                 = 6379
  parameter_group_name = aws_elasticache_parameter_group.main.name

  # Cluster configuration
  num_cache_clusters = var.num_cache_nodes
  port               = 6379

  # Network configuration
  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  # Backup configuration
  snapshot_retention_limit = var.environment == "prod" ? 5 : 1
  snapshot_window         = "03:00-05:00"
  maintenance_window      = "sun:05:00-sun:07:00"

  # Security configuration
  at_rest_encryption_enabled = true
  transit_encryption_enabled = var.environment == "prod" ? true : false
  auth_token                 = var.environment == "prod" ? random_password.redis_auth[0].result : null

  # Logging configuration
  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis.name
    destination_type = "cloudwatch-logs"
    log_format       = "text"
  }

  # Multi-AZ for production
  multi_az_enabled = var.environment == "prod" ? true : false

  # Automatic failover for production
  automatic_failover_enabled = var.environment == "prod" ? true : false

  tags = {
    Name = "${var.project_name}-${var.environment}-redis"
  }
}

# Random password for Redis auth (for production)
resource "random_password" "redis_auth" {
  count   = var.environment == "prod" ? 1 : 0
  length  = 32
  special = true
}

# CloudWatch Log Group for Redis
resource "aws_cloudwatch_log_group" "redis" {
  name              = "/aws/elasticache/redis/${var.project_name}-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-logs"
  }
}

# ElastiCache Event Subscription (for production)
resource "aws_elasticache_event_subscription" "main" {
  count     = var.environment == "prod" ? 1 : 0
  name      = "${var.project_name}-${var.environment}-redis-events"
  sns_topic = aws_sns_topic.redis_events[0].arn

  source_type = "replication-group"
  source_ids  = [aws_elasticache_replication_group.main.id]

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
    Name = "${var.project_name}-${var.environment}-redis-events"
  }
}

# SNS Topic for Redis Events (for production)
resource "aws_sns_topic" "redis_events" {
  count = var.environment == "prod" ? 1 : 0
  name  = "${var.project_name}-${var.environment}-redis-events"

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-events"
  }
}
