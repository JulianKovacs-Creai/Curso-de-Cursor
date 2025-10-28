# Staging Environment Configuration
environment = "staging"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr = "10.1.0.0/16"
az_count = 2

# Database Configuration
db_name     = "ecommerce_staging"
db_username = "postgres"
db_password = "staging_password_456" # Change this in production
db_instance_class = "db.t3.small"
db_allocated_storage = 50

# Redis Configuration
redis_node_type = "cache.t3.small"
redis_num_cache_nodes = 1

# ECS Configuration
backend_image = "ghcr.io/username/ecommerce/backend:staging"
frontend_image = "ghcr.io/username/ecommerce/frontend:staging"

backend_cpu = 512
backend_memory = 1024
backend_desired_count = 2

frontend_cpu = 512
frontend_memory = 1024
frontend_desired_count = 2

# Auto Scaling Configuration
min_capacity = 2
max_capacity = 5
target_cpu_utilization = 70
target_memory_utilization = 80

# Monitoring Configuration
enable_monitoring = true
log_retention_days = 14
alert_email = "staging-team@company.com"

# Security Configuration
allowed_cidr_blocks = ["0.0.0.0/0"]
enable_waf = true

# Cost Optimization
enable_spot_instances = true
enable_graviton = true
