# Human Tasks:
# 1. Ensure GCP project has Cloud Memorystore API enabled
# 2. Configure appropriate IAM roles for Terraform service account
# 3. Verify network connectivity settings in target VPC
# 4. Review maintenance window settings align with organization's maintenance policies

# Requirement: Cache Layer Configuration (11.1.1 Environment Architecture/Cache Tier)
# Defines environment variable with validation for allowed values
variable "environment" {
  description = "Environment name (production, staging, development)"
  type        = string
  
  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Environment must be one of: production, staging, development"
  }
}

# Requirement: Environment-Specific Cache Resources (11.1.2 Environment Specifications)
# Configures memory size based on environment with strict validation
variable "redis_memory_size_gb" {
  description = "Memory size in GB for Redis instance"
  type        = number
  
  validation {
    condition     = (var.environment == "production" && var.redis_memory_size_gb == 4) || (var.environment == "staging" && var.redis_memory_size_gb == 2) || (var.environment == "development" && var.redis_memory_size_gb == 1)
    error_message = "Memory size must be 4GB for production, 2GB for staging, and 1GB for development"
  }
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Defines Redis tier with environment-specific validation
variable "redis_tier" {
  description = "Service tier of the Redis instance"
  type        = string
  
  validation {
    condition     = (var.environment == "production" && var.redis_tier == "STANDARD_HA") || ((var.environment == "staging" || var.environment == "development") && var.redis_tier == "BASIC")
    error_message = "Redis tier must be BASIC for staging/development and STANDARD_HA for production"
  }
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Defines deployment region for Redis instance
variable "region" {
  description = "GCP region for Redis instance deployment"
  type        = string
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Specifies network for Redis instance deployment
variable "network_id" {
  description = "VPC network ID where Redis instance will be deployed"
  type        = string
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Defines Redis version with default to latest stable version
variable "redis_version" {
  description = "Redis version to be used"
  type        = string
  default     = "REDIS_6_X"
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Configures maintenance window day with validation
variable "maintenance_day" {
  description = "Day of week for maintenance window (0-6 for Sunday-Saturday)"
  type        = number
  
  validation {
    condition     = var.maintenance_day >= 0 && var.maintenance_day <= 6
    error_message = "Maintenance day must be between 0 and 6"
  }
}

# Requirement: Cloud Memorystore Settings (11.2.1 Google Cloud Platform Services)
# Configures maintenance window hour with validation
variable "maintenance_hour" {
  description = "Hour of day for maintenance window (0-23)"
  type        = number
  
  validation {
    condition     = var.maintenance_hour >= 0 && var.maintenance_hour <= 23
    error_message = "Maintenance hour must be between 0 and 23"
  }
}