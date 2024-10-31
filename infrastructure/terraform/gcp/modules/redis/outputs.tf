# Human Tasks:
# 1. Ensure that the Redis instance has been successfully provisioned before accessing outputs
# 2. Verify that the network connectivity is properly configured to access Redis instance
# 3. Store the auth_string securely in your application's secret management system

# Requirement: Cache Layer Implementation (11.1.1 Environment Architecture/Cache Tier)
# Exposes the Redis instance hostname for application connectivity
output "redis_host" {
  description = "The IP address or hostname of the Redis instance"
  value       = google_redis_instance.cache.host
}

# Requirement: Cache Layer Implementation (11.1.1 Environment Architecture/Cache Tier)
# Exposes the Redis instance port for application connectivity
output "redis_port" {
  description = "The port number of the Redis instance"
  value       = google_redis_instance.cache.port
}

# Requirement: Cloud Memorystore Integration (11.2.1 Google Cloud Platform Services)
# Exposes the unique identifier of the Redis instance for reference
output "redis_instance_id" {
  description = "The unique identifier of the Redis instance"
  value       = google_redis_instance.cache.id
}

# Requirement: Cloud Memorystore Integration (11.2.1 Google Cloud Platform Services)
# Exposes the authentication string required for Redis access
output "redis_auth_string" {
  description = "The authentication string for Redis instance access"
  value       = google_redis_instance.cache.auth_string
  sensitive   = true
}

# Requirement: Cache Layer Implementation (11.1.1 Environment Architecture/Cache Tier)
# Provides a formatted connection string for easy application configuration
output "connection_string" {
  description = "The full Redis connection string in the format redis://host:port"
  value       = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}"
}