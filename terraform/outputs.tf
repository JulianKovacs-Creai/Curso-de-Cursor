# Outputs for E-commerce Terraform Configuration
# Important values and endpoints for the deployed infrastructure

# =============================================================================
# VPC and Networking Outputs
# =============================================================================

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "database_subnet_ids" {
  description = "IDs of the database subnets"
  value       = aws_subnet.database[*].id
}

output "availability_zones" {
  description = "Availability zones used"
  value       = local.azs
}

# =============================================================================
# Load Balancer Outputs
# =============================================================================

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = aws_lb.main.zone_id
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = aws_lb.main.arn
}

# =============================================================================
# ECS Outputs
# =============================================================================

output "ecs_cluster_id" {
  description = "ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "ecs_cluster_arn" {
  description = "ARN of the ECS cluster"
  value       = aws_ecs_cluster.main.arn
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "backend_service_name" {
  description = "Name of the backend ECS service"
  value       = aws_ecs_service.backend.name
}

output "frontend_service_name" {
  description = "Name of the frontend ECS service"
  value       = aws_ecs_service.frontend.name
}

output "backend_task_definition_arn" {
  description = "ARN of the backend task definition"
  value       = aws_ecs_task_definition.backend.arn
}

output "frontend_task_definition_arn" {
  description = "ARN of the frontend task definition"
  value       = aws_ecs_task_definition.frontend.arn
}

# =============================================================================
# Database Outputs
# =============================================================================

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "rds_identifier" {
  description = "RDS instance identifier"
  value       = aws_db_instance.main.identifier
}

output "rds_arn" {
  description = "ARN of the RDS instance"
  value       = aws_db_instance.main.arn
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  sensitive   = true
}

output "redis_port" {
  description = "Redis cluster port"
  value       = aws_elasticache_replication_group.redis.port
}

output "redis_arn" {
  description = "ARN of the Redis cluster"
  value       = aws_elasticache_replication_group.redis.arn
}

# =============================================================================
# Security Group Outputs
# =============================================================================

output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = aws_security_group.alb.id
}

output "ecs_security_group_id" {
  description = "ID of the ECS security group"
  value       = aws_security_group.ecs.id
}

output "rds_security_group_id" {
  description = "ID of the RDS security group"
  value       = aws_security_group.rds.id
}

output "redis_security_group_id" {
  description = "ID of the Redis security group"
  value       = aws_security_group.redis.id
}

# =============================================================================
# ECR Outputs
# =============================================================================

output "backend_ecr_repository_url" {
  description = "URL of the backend ECR repository"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository_url" {
  description = "URL of the frontend ECR repository"
  value       = aws_ecr_repository.frontend.repository_url
}

output "backend_ecr_arn" {
  description = "ARN of the backend ECR repository"
  value       = aws_ecr_repository.backend.arn
}

output "frontend_ecr_arn" {
  description = "ARN of the frontend ECR repository"
  value       = aws_ecr_repository.frontend.arn
}

# =============================================================================
# Route53 Outputs
# =============================================================================

output "domain_name" {
  description = "Domain name of the application"
  value       = var.domain_name
}

output "zone_id" {
  description = "Route53 hosted zone ID"
  value       = aws_route53_zone.main.zone_id
}

output "certificate_arn" {
  description = "ARN of the SSL certificate"
  value       = aws_acm_certificate.main.arn
}

# =============================================================================
# CloudWatch Outputs
# =============================================================================

output "backend_log_group_name" {
  description = "Name of the backend CloudWatch log group"
  value       = aws_cloudwatch_log_group.backend.name
}

output "frontend_log_group_name" {
  description = "Name of the frontend CloudWatch log group"
  value       = aws_cloudwatch_log_group.frontend.name
}

# =============================================================================
# Auto Scaling Outputs
# =============================================================================

output "backend_autoscaling_target_arn" {
  description = "ARN of the backend autoscaling target"
  value       = aws_appautoscaling_target.backend.arn
}

output "frontend_autoscaling_target_arn" {
  description = "ARN of the frontend autoscaling target"
  value       = aws_appautoscaling_target.frontend.arn
}

# =============================================================================
# Application URLs
# =============================================================================

output "application_url" {
  description = "URL of the application"
  value       = "https://${var.domain_name}"
}

output "api_url" {
  description = "URL of the API"
  value       = "https://${var.domain_name}/api"
}

output "health_check_url" {
  description = "URL of the health check endpoint"
  value       = "https://${var.domain_name}/health"
}

# =============================================================================
# Connection Information
# =============================================================================

output "database_connection_string" {
  description = "Database connection string (without password)"
  value       = "postgresql://${var.db_username}@${aws_db_instance.main.endpoint}:${aws_db_instance.main.port}/${var.db_name}"
  sensitive   = true
}

output "redis_connection_string" {
  description = "Redis connection string (without password)"
  value       = "redis://${aws_elasticache_replication_group.redis.primary_endpoint_address}:${aws_elasticache_replication_group.redis.port}/0"
  sensitive   = true
}

# =============================================================================
# Deployment Information
# =============================================================================

output "deployment_region" {
  description = "AWS region where resources are deployed"
  value       = var.aws_region
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

# =============================================================================
# Cost Information
# =============================================================================

output "estimated_monthly_cost" {
  description = "Estimated monthly cost (USD)"
  value       = "~$200-500 (depending on usage)"
}

# =============================================================================
# Monitoring Information
# =============================================================================

output "cloudwatch_dashboard_url" {
  description = "URL to CloudWatch dashboard"
  value       = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${local.name_prefix}-dashboard"
}

output "ecs_console_url" {
  description = "URL to ECS console"
  value       = "https://${var.aws_region}.console.aws.amazon.com/ecs/v2/clusters/${aws_ecs_cluster.main.name}/services"
}

# =============================================================================
# Security Information
# =============================================================================

output "secrets_manager_secrets" {
  description = "List of secrets in AWS Secrets Manager"
  value       = [
    aws_secretsmanager_secret.db_password.name
  ]
}

# =============================================================================
# Backup Information
# =============================================================================

output "backup_retention_period" {
  description = "Backup retention period in days"
  value       = var.db_backup_retention_period
}

output "backup_window" {
  description = "Backup window"
  value       = "03:00-04:00 UTC"
}

# =============================================================================
# Maintenance Information
# =============================================================================

output "maintenance_window" {
  description = "Maintenance window"
  value       = "Sunday 04:00-05:00 UTC"
}

output "monitoring_enabled" {
  description = "Whether detailed monitoring is enabled"
  value       = var.enable_detailed_monitoring
}
