# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
# Expose essential CloudSQL PostgreSQL instance information
output "instance_name" {
  description = "The name of the Cloud SQL instance"
  value       = google_sql_database_instance.primary.name
  sensitive   = false
}

output "instance_connection_name" {
  description = "The connection name of the instance to be used in connection strings"
  value       = google_sql_database_instance.primary.connection_name
  sensitive   = false
}

output "database_name" {
  description = "The name of the database"
  value       = google_sql_database.main.name
  sensitive   = false
}

output "database_version" {
  description = "The PostgreSQL version of the database"
  value       = google_sql_database_instance.primary.database_version
  sensitive   = false
}

output "public_ip_address" {
  description = "The public IPv4 address of the primary instance"
  value       = google_sql_database_instance.primary.public_ip_address
  sensitive   = false
}

output "private_ip_address" {
  description = "The private IPv4 address of the primary instance"
  value       = google_sql_database_instance.primary.private_ip_address
  sensitive   = false
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
# Expose database credentials securely
output "database_user" {
  description = "The database user for application connections"
  value       = google_sql_user.app.name
  sensitive   = true
}

output "database_password" {
  description = "The database password for application connections"
  value       = random_password.db_password.result
  sensitive   = true
}

output "replica_configuration" {
  description = "The configuration of the replica instances"
  value       = google_sql_database_instance.primary.replica_configuration
  sensitive   = false
}

output "ssl_required" {
  description = "Whether SSL connections to the database are required"
  value       = google_sql_database_instance.primary.settings[0].ip_configuration[0].require_ssl
  sensitive   = false
}