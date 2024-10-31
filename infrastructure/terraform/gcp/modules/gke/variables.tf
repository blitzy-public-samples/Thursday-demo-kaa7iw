# Human Tasks:
# 1. Ensure the following IAM roles are assigned to the GKE service account:
#    - roles/container.admin
#    - roles/compute.networkAdmin
#    - roles/monitoring.admin
# 2. Review and adjust node pool configurations based on workload requirements
# 3. Configure VPC firewall rules to allow GKE master-node communication
# 4. Set up monitoring and logging IAM permissions for GKE workload identity

# Provider version: hashicorp/google ~> 4.0

# Requirement: Kubernetes Cluster Management (11.4.1 Kubernetes Architecture)
variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,38}[a-z0-9]$", var.cluster_name))
    error_message = "Cluster name must be between 6 and 40 characters, start with a letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

# Requirement: Environment Specifications (11.1.2 Environment Specifications)
variable "location" {
  description = "The location (region or zone) where the GKE cluster will be created"
  type        = string
  default     = "us-central1"

  validation {
    condition     = can(regex("^[a-z]+-[a-z]+[0-9](?:-[a-z])?$", var.location))
    error_message = "Location must be a valid GCP region (e.g., us-central1) or zone (e.g., us-central1-a)."
  }
}

# Requirement: Security Architecture (10.2 Data Security/10.2.1 Data Classification)
variable "network_config" {
  description = "Network configuration for the GKE cluster"
  type = object({
    network                 = string
    subnetwork             = string
    master_ipv4_cidr_block = string
  })

  default = {
    network                 = "default"
    subnetwork             = "default"
    master_ipv4_cidr_block = "172.16.0.0/28"
  }

  validation {
    condition     = can(cidrhost(var.network_config.master_ipv4_cidr_block, 0))
    error_message = "Master CIDR block must be a valid IPv4 CIDR range."
  }
}

# Requirement: Kubernetes Cluster Management (11.4.1 Kubernetes Architecture)
variable "node_pools" {
  description = "Configuration for GKE node pools"
  type = map(object({
    initial_node_count = number
    min_nodes         = number
    max_nodes         = number
    machine_type      = string
    disk_size_gb      = number
    labels            = map(string)
    taints = list(object({
      key    = string
      value  = string
      effect = string
    }))
  }))

  validation {
    condition = alltrue([
      for k, v in var.node_pools : (
        v.min_nodes >= 1 &&
        v.max_nodes >= v.min_nodes &&
        v.disk_size_gb >= 30 &&
        can(regex("^[a-z][a-z0-9-]+$", v.machine_type))
      )
    ])
    error_message = "Invalid node pool configuration. Check min_nodes (>= 1), max_nodes (>= min_nodes), disk_size_gb (>= 30), and machine_type format."
  }
}

# Requirement: Security Architecture (10.2 Data Security/10.2.1 Data Classification)
variable "private_cluster_config" {
  description = "Private cluster configuration settings"
  type = object({
    enable_private_nodes    = bool
    enable_private_endpoint = bool
  })

  default = {
    enable_private_nodes    = true
    enable_private_endpoint = false
  }
}

# Requirement: Kubernetes Cluster Management (11.4.1 Kubernetes Architecture)
variable "maintenance_config" {
  description = "Cluster maintenance configuration"
  type = object({
    daily_maintenance_window = string
    maintenance_exclusions = list(object({
      name       = string
      start_time = string
      end_time   = string
    }))
  })

  default = {
    daily_maintenance_window = "03:00"
    maintenance_exclusions   = []
  }

  validation {
    condition     = can(regex("^(?:[01]\\d|2[0-3]):[0-5]\\d$", var.maintenance_config.daily_maintenance_window))
    error_message = "Daily maintenance window must be in 24-hour format (HH:MM)."
  }
}

# Requirement: Kubernetes Cluster Management (11.4.1 Kubernetes Architecture)
variable "release_channel" {
  description = "Release channel for GKE version updates"
  type        = string
  default     = "REGULAR"

  validation {
    condition     = contains(["RAPID", "REGULAR", "STABLE"], var.release_channel)
    error_message = "Release channel must be one of: RAPID, REGULAR, STABLE."
  }
}

# Requirement: Kubernetes Cluster Management (11.4.1 Kubernetes Architecture)
variable "monitoring_config" {
  description = "Monitoring configuration for the cluster"
  type = object({
    enable_components  = list(string)
    managed_prometheus = bool
  })

  default = {
    enable_components  = ["SYSTEM_COMPONENTS", "WORKLOADS"]
    managed_prometheus = true
  }

  validation {
    condition = alltrue([
      for component in var.monitoring_config.enable_components :
      contains(["SYSTEM_COMPONENTS", "WORKLOADS"], component)
    ])
    error_message = "Monitoring components must be either SYSTEM_COMPONENTS or WORKLOADS."
  }
}