# Human Tasks:
# 1. Ensure Cloud SQL Admin API is enabled in the GCP project
# 2. Configure appropriate IAM roles for the service account:
#    - roles/cloudsql.admin
#    - roles/cloudsql.client
# 3. Review and adjust database flags based on security requirements
# 4. Verify backup retention policies comply with data retention requirements

# Provider version: hashicorp/google ~> 4.0
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
# Create a private VPC network for database instances
resource "google_compute_network" "private_network" {
  name                    = "private-network-${var.instance_name}"
  project                 = var.project_id
  auto_create_subnetworks = false
}

# Create a private subnet for the database instances
resource "google_compute_subnetwork" "private_subnet" {
  name          = "private-subnet-${var.instance_name}"
  project       = var.project_id
  region        = var.region
  network       = google_compute_network.private_network.id
  ip_cidr_range = "10.0.0.0/24"
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
# Create a Cloud SQL instance with high availability and security configurations
resource "google_sql_database_instance" "primary" {
  name                = var.instance_name
  database_version    = "POSTGRES_14"
  region             = var.region
  project            = var.project_id
  deletion_protection = true # Prevent accidental deletion

  settings {
    tier              = var.instance_tier[var.environment]
    availability_type = var.availability_type[var.environment]
    disk_autoresize   = true
    disk_size         = 20 # Initial disk size in GB
    disk_type         = "PD_SSD"

    # Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
    backup_configuration {
      enabled                        = var.backup_enabled
      point_in_time_recovery_enabled = var.backup_enabled
      retained_backups              = var.backup_retention_days
      retention_unit                = "COUNT"
    }

    # Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.private_network.id
      require_ssl                                   = var.require_ssl
      enable_private_path_for_google_cloud_services = true
    }

    # Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
    database_flags = var.database_flags

    # Maintenance window configuration
    maintenance_window {
      day          = 7  # Sunday
      hour         = 2  # 2 AM
      update_track = "stable"
    }

    # Insights configuration for monitoring
    insights_config {
      query_insights_enabled  = true
      query_string_length    = 1024
      record_application_tags = true
      record_client_address  = true
    }
  }

  depends_on = [google_compute_network.private_network]
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
# Create the main database
resource "google_sql_database" "main" {
  name     = var.database_name
  instance = google_sql_database_instance.primary.name
  project  = var.project_id
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
# Generate a secure random password for the database user
resource "random_password" "db_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
# Create the application database user
resource "google_sql_user" "app" {
  name     = var.database_user
  instance = google_sql_database_instance.primary.name
  password = random_password.db_password.result
  project  = var.project_id
}

# Requirement: High Availability (11.1 Deployment Environment/11.1.2 Environment Specifications)
# Create Cloud SQL replica for high availability in production
resource "google_sql_database_instance" "replica" {
  count                = var.availability_type[var.environment] == "REGIONAL" ? 1 : 0
  name                 = "${var.instance_name}-replica"
  database_version     = "POSTGRES_14"
  region              = var.region
  project             = var.project_id
  deletion_protection = true

  replica_configuration {
    failover_target = false
  }

  settings {
    tier              = var.instance_tier[var.environment]
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    
    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.private_network.id
      require_ssl                                   = var.require_ssl
      enable_private_path_for_google_cloud_services = true
    }

    database_flags = var.database_flags
  }

  master_instance_name = google_sql_database_instance.primary.name

  depends_on = [google_sql_database_instance.primary]
}

# Outputs for use by other modules
output "instance_name" {
  description = "The name of the database instance"
  value       = google_sql_database_instance.primary.name
}

output "database_name" {
  description = "The name of the database"
  value       = google_sql_database.main.name
}

output "database_user" {
  description = "The database user"
  value       = google_sql_user.app.name
}

output "database_password" {
  description = "The database password"
  value       = random_password.db_password.result
  sensitive   = true
}

output "private_ip_address" {
  description = "The private IP address of the database instance"
  value       = google_sql_database_instance.primary.private_ip_address
}

output "connection_name" {
  description = "The connection name of the database instance"
  value       = google_sql_database_instance.primary.connection_name
}

output "replica_instance_name" {
  description = "The name of the replica instance (if created)"
  value       = var.availability_type[var.environment] == "REGIONAL" ? google_sql_database_instance.replica[0].name : null
}