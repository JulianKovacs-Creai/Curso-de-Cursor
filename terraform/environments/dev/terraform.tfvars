# Development Environment Configuration
environment = "dev"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
az_count = 2

# Database Configuration
db_name     = "ecommerce_dev"
db_username = "postgres"
db_password = "dev_password_123" # Change this in production
db_instance_class = "db.t3.micro"
db_allocated_storage = 20

# Redis Configuration
redis_node_type = "cache.t3.micro"
redis_num_cache_nodes = 1

# ECS Configuration
backend_image = "ghcr.io/username/ecommerce/backend:dev"
frontend_image = "ghcr.io/username/ecommerce/frontend:dev"

backend_cpu = 256
backend_memory = 512
backend_desired_count = 1

frontend_cpu = 256
frontend_memory = 512
frontend_desired_count = 1

# Auto Scaling Configuration
min_capacity = 1
max_capacity = 3
target_cpu_utilization = 70
target_memory_utilization = 80

# Monitoring Configuration
enable_monitoring = true
log_retention_days = 7
alert_email = "dev-team@company.com"

# Security Configuration
allowed_cidr_blocks = ["0.0.0.0/0"]
enable_waf = false

# Cost Optimization
enable_spot_instances = false
enable_graviton = false
