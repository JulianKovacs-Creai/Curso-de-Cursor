output "cluster_id" {
  description = "ID of the Redis cluster"
  value       = aws_elasticache_replication_group.main.id
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
  sensitive   = true
}

output "redis_port" {
  description = "Redis cluster port"
  value       = aws_elasticache_replication_group.main.port
}

output "redis_arn" {
  description = "ARN of the Redis cluster"
  value       = aws_elasticache_replication_group.main.arn
}

output "redis_security_group_id" {
  description = "ID of the Redis security group"
  value       = aws_security_group.redis.id
}

output "redis_subnet_group_name" {
  description = "Name of the Redis subnet group"
  value       = aws_elasticache_subnet_group.main.name
}

output "redis_auth_token" {
  description = "Redis auth token (if enabled)"
  value       = var.environment == "prod" ? random_password.redis_auth[0].result : null
  sensitive   = true
}
