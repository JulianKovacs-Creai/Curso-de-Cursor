variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for ECS tasks"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

# Backend Configuration
variable "backend_image" {
  description = "Backend Docker image"
  type        = string
}

variable "backend_cpu" {
  description = "Backend CPU units"
  type        = number
}

variable "backend_memory" {
  description = "Backend memory in MB"
  type        = number
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks"
  type        = number
}

# Frontend Configuration
variable "frontend_image" {
  description = "Frontend Docker image"
  type        = string
}

variable "frontend_cpu" {
  description = "Frontend CPU units"
  type        = number
}

variable "frontend_memory" {
  description = "Frontend memory in MB"
  type        = number
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks"
  type        = number
}

# Database Configuration
variable "db_endpoint" {
  description = "RDS instance endpoint"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Redis Configuration
variable "redis_endpoint" {
  description = "Redis cluster endpoint"
  type        = string
}

# ALB Configuration
variable "alb_arn" {
  description = "ARN of the Application Load Balancer"
  type        = string
}

variable "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  type        = string
}

variable "backend_target_group_arn" {
  description = "ARN of the backend target group"
  type        = string
}

variable "frontend_target_group_arn" {
  description = "ARN of the frontend target group"
  type        = string
}

# Auto Scaling Configuration
variable "min_capacity" {
  description = "Minimum capacity for auto scaling"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum capacity for auto scaling"
  type        = number
  default     = 10
}

variable "target_cpu_utilization" {
  description = "Target CPU utilization for auto scaling"
  type        = number
  default     = 70
}

variable "target_memory_utilization" {
  description = "Target memory utilization for auto scaling"
  type        = number
  default     = 80
}

# Monitoring Configuration
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}
