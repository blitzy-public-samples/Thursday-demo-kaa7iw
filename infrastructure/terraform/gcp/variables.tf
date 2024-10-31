# Human Tasks:
# 1. Ensure GCP project has required APIs enabled:
#    - Compute Engine API
#    - Kubernetes Engine API
#    - Cloud SQL Admin API
#    - Redis Enterprise API
# 2. Configure GCP credentials and authentication
# 3. Review and adjust default values based on specific environment needs
# 4. Ensure proper IAM roles are assigned to the service account

# Provider version: hashicorp/google ~> 4.0

# Requirement: Cloud Infrastructure (11.1.1 Environment Architecture)
# Core project configuration variables
variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Project ID must be between 6 and 30 characters, start with a letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

# Requirement: Cloud Infrastructure (11.1.1 Environment Architecture)
variable "region" {
  description = "The GCP region where resources will be deployed"
  type        = string
  default     = "us-central1"

  validation {
    condition     = can(regex("^[a-z]+-[a-z]+[0-9]$", var.region))
    error_message = "Region must be a valid GCP region identifier (e.g., us-central1, europe-west1)."
  }
}

# Requirement: Environment Specifications (11.1.2 Environment Specifications)
variable "environment" {
  description = "Deployment environment (production, staging, development)"
  type        = string

  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Environment must be one of: production, staging, development."
  }
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# GKE cluster configuration per environment
variable "gke_config" {
  description = "GKE cluster configuration per environment"
  type = map(object({
    machine_type  = string
    node_count    = number
    disk_size_gb  = number
  }))

  default = {
    production = {
      machine_type  = "n1-standard-4"
      node_count    = 3
      disk_size_gb  = 100
    }
    staging = {
      machine_type  = "n1-standard-2"
      node_count    = 2
      disk_size_gb  = 50
    }
    development = {
      machine_type  = "n1-standard-1"
      node_count    = 1
      disk_size_gb  = 30
    }
  }

  validation {
    condition = alltrue([
      for k, v in var.gke_config :
      can(regex("^[a-z][a-z0-9-]+$", v.machine_type)) &&
      v.node_count > 0 && v.node_count <= 10 &&
      v.disk_size_gb >= 10 && v.disk_size_gb <= 65536
    ])
    error_message = "Invalid GKE configuration. Check machine type format, node count (1-10), and disk size (10-65536 GB)."
  }
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# Cloud SQL database configuration per environment
variable "database_config" {
  description = "Database configuration per environment"
  type = map(object({
    tier              = string
    availability_type = string
    backup_enabled    = bool
  }))

  default = {
    production = {
      tier              = "db-custom-4-16384"
      availability_type = "REGIONAL"
      backup_enabled    = true
    }
    staging = {
      tier              = "db-custom-2-8192"
      availability_type = "ZONAL"
      backup_enabled    = true
    }
    development = {
      tier              = "db-custom-1-4096"
      availability_type = "ZONAL"
      backup_enabled    = false
    }
  }

  validation {
    condition = alltrue([
      for k, v in var.database_config :
      can(regex("^db-custom-[0-9]+-[0-9]+$", v.tier)) &&
      contains(["REGIONAL", "ZONAL"], v.availability_type)
    ])
    error_message = "Invalid database configuration. Check tier format (db-custom-*) and availability type (REGIONAL or ZONAL)."
  }
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# Redis cache configuration per environment
variable "redis_config" {
  description = "Redis configuration per environment"
  type = map(object({
    tier            = string
    memory_size_gb  = number
    version         = string
  }))

  default = {
    production = {
      tier            = "STANDARD_HA"
      memory_size_gb  = 4
      version         = "REDIS_6_X"
    }
    staging = {
      tier            = "BASIC"
      memory_size_gb  = 2
      version         = "REDIS_6_X"
    }
    development = {
      tier            = "BASIC"
      memory_size_gb  = 1
      version         = "REDIS_6_X"
    }
  }

  validation {
    condition = alltrue([
      for k, v in var.redis_config :
      contains(["BASIC", "STANDARD_HA"], v.tier) &&
      v.memory_size_gb >= 1 && v.memory_size_gb <= 300 &&
      contains(["REDIS_6_X"], v.version)
    ])
    error_message = "Invalid Redis configuration. Check tier (BASIC or STANDARD_HA), memory size (1-300 GB), and version (REDIS_6_X)."
  }
}