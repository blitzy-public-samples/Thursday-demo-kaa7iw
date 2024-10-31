# Human Tasks:
# 1. Ensure Cloud SQL Admin API is enabled in the GCP project
# 2. Configure appropriate IAM roles for the service account:
#    - roles/cloudsql.admin
#    - roles/cloudsql.client
# 3. Review and adjust default database flags based on security requirements
# 4. Verify backup retention policies comply with data retention requirements

# Provider version: hashicorp/google ~> 4.0

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
# Import root variables for project configuration
variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "The GCP region where resources will be deployed"
  type        = string
}

variable "environment" {
  description = "Deployment environment (production, staging, development)"
  type        = string
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
variable "instance_name" {
  description = "The name of the Cloud SQL instance"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*[a-z0-9]$", var.instance_name))
    error_message = "Instance name must start with a letter, can only contain lowercase letters, numbers, and hyphens."
  }
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
variable "database_name" {
  description = "The name of the PostgreSQL database to create"
  type        = string
  default     = "codegenapp"

  validation {
    condition     = can(regex("^[a-z][a-z0-9_]*$", var.database_name))
    error_message = "Database name must be a valid PostgreSQL database name and must not be a reserved keyword."
  }
}

# Requirement: Database Infrastructure (7.1 High-Level Architecture/Data Layer)
variable "database_user" {
  description = "The name of the database user to create"
  type        = string
  default     = "appuser"

  validation {
    condition     = can(regex("^[a-z][a-z0-9_]*$", var.database_user))
    error_message = "Database user must be a valid PostgreSQL username and must not be a reserved keyword."
  }
}

# Requirement: Environment Specifications (11.1.2 Environment Specifications)
variable "instance_tier" {
  description = "The machine type for each environment"
  type        = map(string)
  default = {
    production  = "db-custom-4-16384"
    staging     = "db-custom-2-8192"
    development = "db-custom-1-4096"
  }

  validation {
    condition     = alltrue([for tier in values(var.instance_tier) : can(regex("^db-custom-[0-9]+-[0-9]+$", tier))])
    error_message = "Instance tier must be a valid Cloud SQL machine type (e.g., db-custom-4-16384)."
  }
}

# Requirement: Environment Specifications (11.1.2 Environment Specifications)
variable "availability_type" {
  description = "The availability type for each environment (REGIONAL or ZONAL)"
  type        = map(string)
  default = {
    production  = "REGIONAL"
    staging     = "ZONAL"
    development = "ZONAL"
  }

  validation {
    condition     = alltrue([for type in values(var.availability_type) : contains(["REGIONAL", "ZONAL"], type)])
    error_message = "Availability type must be either REGIONAL or ZONAL."
  }
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
variable "backup_enabled" {
  description = "Whether to enable automated backups"
  type        = bool
  default     = true
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7

  validation {
    condition     = var.backup_retention_days >= 1 && var.backup_retention_days <= 365
    error_message = "Backup retention days must be between 1 and 365."
  }
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
variable "require_ssl" {
  description = "Whether to require SSL/TLS for database connections"
  type        = bool
  default     = true
}

# Requirement: Database Security (10.2 Data Security/10.2.3 Database Security)
variable "database_flags" {
  description = "Database flags for instance configuration"
  type        = list(object({
    name  = string
    value = string
  }))
  default = [
    {
      name  = "log_checkpoints"
      value = "on"
    },
    {
      name  = "log_connections"
      value = "on"
    },
    {
      name  = "log_disconnections"
      value = "on"
    },
    {
      name  = "log_lock_waits"
      value = "on"
    }
  ]

  validation {
    condition     = alltrue([for flag in var.database_flags : can(regex("^[a-z][a-z0-9_]*$", flag.name))])
    error_message = "Database flag names must be valid PostgreSQL parameter names."
  }
}