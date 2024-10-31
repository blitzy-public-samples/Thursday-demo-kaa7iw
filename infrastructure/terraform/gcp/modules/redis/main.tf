# Provider version constraint
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# Requirement: Cache Layer Implementation (11.1.1 Environment Architecture/Cache Tier)
# Local variables for resource naming and tagging
locals {
  resource_prefix = "${var.environment}-redis"
}

# Requirement: Cloud Memorystore Configuration (11.2.1 Google Cloud Platform Services)
# Implements managed Redis cache with high availability settings
resource "google_redis_instance" "cache" {
  # Basic instance configuration
  name           = "${local.resource_prefix}-cache"
  memory_size_gb = var.redis_memory_size_gb
  tier           = var.redis_tier
  
  # Network configuration
  location_id       = var.region
  authorized_network = var.network_id
  
  # Redis version configuration
  redis_version    = var.redis_version
  
  # Requirement: Environment-Specific Cache Resources (11.1.2 Environment Specifications)
  # Maintenance window configuration
  maintenance_policy {
    weekly_maintenance_window {
      day = var.maintenance_day
      start_time {
        hours = var.maintenance_hour
        minutes = 0
        seconds = 0
        nanos = 0
      }
    }
  }
  
  # Environment labeling
  labels = {
    environment = var.environment
  }

  # Requirement: Cache Layer Implementation (11.1.1 Environment Architecture/Cache Tier)
  # Configure Redis instance based on environment tier
  lifecycle {
    precondition {
      condition = (
        (var.environment == "production" && var.redis_tier == "STANDARD_HA" && var.redis_memory_size_gb == 4) ||
        (var.environment == "staging" && var.redis_tier == "BASIC" && var.redis_memory_size_gb == 2) ||
        (var.environment == "development" && var.redis_tier == "BASIC" && var.redis_memory_size_gb == 1)
      )
      error_message = "Redis configuration does not match environment requirements"
    }
  }

  # Prevent replacement of the instance
  lifecycle {
    prevent_destroy = var.environment == "production"
  }

  # Enable automatic failover for production environment
  dynamic "read_replicas_mode" {
    for_each = var.environment == "production" ? [1] : []
    content {
      replica_count = 1
    }
  }

  # Configure Redis persistence
  persistence_config {
    persistence_mode = var.environment == "production" ? "RDB" : "DISABLED"
    rdb_snapshot_period = var.environment == "production" ? "ONE_HOUR" : null
  }

  # Configure Redis authentication
  auth_enabled = true

  # Configure connection settings
  connect_mode = "PRIVATE_SERVICE_ACCESS"
  
  # Configure Redis transit encryption
  transit_encryption_mode = "SERVER_AUTHENTICATION"
}