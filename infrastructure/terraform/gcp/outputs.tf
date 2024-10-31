# Human Tasks:
# 1. Ensure that sensitive outputs are properly marked to prevent accidental exposure
# 2. Verify that the outputs are being consumed correctly by the application configuration
# 3. Review access policies for these outputs in your CI/CD pipeline
# 4. Configure appropriate output value encryption in your state backend

# Requirement addressed: Cloud Infrastructure (11.1 Deployment Environment/11.1.1 Environment Architecture)
# GKE cluster endpoint for Kubernetes API access
output "gke_cluster_endpoint" {
  description = "The endpoint for accessing the GKE cluster"
  value       = module.gke.cluster_endpoint
}

# Requirement addressed: Environment Configuration (11.1.2 Environment Specifications)
# GKE cluster name for resource identification
output "gke_cluster_name" {
  description = "The name of the GKE cluster"
  value       = module.gke.cluster_name
}

# Requirement addressed: Security Architecture (10.2 Data Security/10.2.1 Data Classification)
# GKE cluster CA certificate for secure cluster authentication
output "gke_cluster_ca_certificate" {
  description = "The cluster CA certificate for GKE authentication"
  value       = module.gke.cluster_ca_certificate
  sensitive   = true
}

# Requirement addressed: Environment Configuration (11.1.2 Environment Specifications)
# Cloud SQL instance name for database identification
output "database_instance_name" {
  description = "The name of the Cloud SQL instance"
  value       = module.cloudsql.instance_name
}

# Requirement addressed: Cloud Infrastructure (11.1 Deployment Environment/11.1.1 Environment Architecture)
# Cloud SQL connection name for database access
output "database_connection_name" {
  description = "The connection name for the Cloud SQL instance"
  value       = module.cloudsql.connection_name
}

# Requirement addressed: Cloud Infrastructure (11.1 Deployment Environment/11.1.1 Environment Architecture)
# Cloud SQL private IP for secure database access
output "database_private_ip" {
  description = "The private IP address of the Cloud SQL instance"
  value       = module.cloudsql.private_ip_address
}

# Requirement addressed: Security Architecture (10.2 Data Security/10.2.1 Data Classification)
# Cloud SQL password for database authentication
output "database_password" {
  description = "The generated password for the database"
  value       = module.cloudsql.db_password
  sensitive   = true
}

# Requirement addressed: Environment Configuration (11.1.2 Environment Specifications)
# Redis host for cache access
output "redis_host" {
  description = "The hostname of the Redis instance"
  value       = module.redis.redis_host
}

# Requirement addressed: Environment Configuration (11.1.2 Environment Specifications)
# Redis port for cache connection
output "redis_port" {
  description = "The port number of the Redis instance"
  value       = module.redis.redis_port
}

# Requirement addressed: Security Architecture (10.2 Data Security/10.2.1 Data Classification)
# Redis authentication string for secure cache access
output "redis_auth_string" {
  description = "The authentication string for Redis connection"
  value       = module.redis.redis_auth_string
  sensitive   = true
}