# Production Environment Configuration
environment = "prod"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr = "10.2.0.0/16"
az_count = 3

# Database Configuration
db_name     = "ecommerce_prod"
db_username = "postgres"
db_password = "prod_password_789" # Change this in production
db_instance_class = "db.t3.medium"
db_allocated_storage = 100

# Redis Configuration
redis_node_type = "cache.t3.medium"
redis_num_cache_nodes = 2

# ECS Configuration
backend_image = "ghcr.io/username/ecommerce/backend:latest"
frontend_image = "ghcr.io/username/ecommerce/frontend:latest"

backend_cpu = 1024
backend_memory = 2048
backend_desired_count = 3

frontend_cpu = 1024
frontend_memory = 2048
frontend_desired_count = 3

# Auto Scaling Configuration
min_capacity = 3
max_capacity = 20
target_cpu_utilization = 70
target_memory_utilization = 80

# Monitoring Configuration
enable_monitoring = true
log_retention_days = 30
alert_email = "ops-team@company.com"

# Security Configuration
allowed_cidr_blocks = ["0.0.0.0/0"]
enable_waf = true

# Cost Optimization
enable_spot_instances = true
enable_graviton = true
