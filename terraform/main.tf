terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "ecommerce-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# VPC Module
module "vpc" {
  source = "./modules/vpc"

  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
  azs          = slice(data.aws_availability_zones.available.names, 0, var.az_count)
}

# RDS Module
module "rds" {
  source = "./modules/rds"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  db_name      = var.db_name
  db_username  = var.db_username
  db_password  = var.db_password
  db_instance_class = var.db_instance_class
  db_allocated_storage = var.db_allocated_storage
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  public_subnet_ids = module.vpc.public_subnet_ids
  
  # Backend configuration
  backend_image = var.backend_image
  backend_cpu = var.backend_cpu
  backend_memory = var.backend_memory
  backend_desired_count = var.backend_desired_count
  
  # Frontend configuration
  frontend_image = var.frontend_image
  frontend_cpu = var.frontend_cpu
  frontend_memory = var.frontend_memory
  frontend_desired_count = var.frontend_desired_count
  
  # Database configuration
  db_endpoint = module.rds.db_endpoint
  db_name = var.db_name
  db_username = var.db_username
  db_password = var.db_password
  
  # Redis configuration
  redis_endpoint = module.redis.redis_endpoint
  
  # ALB configuration
  alb_arn = module.alb.alb_arn
  alb_target_group_arn = module.alb.target_group_arn
}

# ALB Module
module "alb" {
  source = "./modules/alb"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.public_subnet_ids
  certificate_arn = var.certificate_arn
}

# Redis Module
module "redis" {
  source = "./modules/redis"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  node_type    = var.redis_node_type
  num_cache_nodes = var.redis_num_cache_nodes
}

# Monitoring Module
module "monitoring" {
  source = "./modules/monitoring"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  alb_arn      = module.alb.alb_arn
  ecs_cluster_name = module.ecs.cluster_name
  rds_instance_id = module.rds.db_instance_id
  redis_cluster_id = module.redis.cluster_id
}

# Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = module.alb.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the ALB"
  value       = module.alb.alb_zone_id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = module.redis.redis_endpoint
  sensitive   = true
}