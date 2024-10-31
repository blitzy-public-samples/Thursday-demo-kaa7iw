# Provider version requirements:
# google ~> 4.0
# google-beta ~> 4.0

# Local variables for cluster configuration
locals {
  default_node_count = 3
  min_nodes         = 3
  max_nodes         = 10
  machine_type      = "n1-standard-2"
  master_ipv4_cidr  = "172.16.0.0/28"
  network_config = {
    network    = "default"
    subnetwork = "default"
  }
}

# Fetch current project details
# Requirement addressed: Environment Specifications (11.1.2)
data "google_project" "current" {}

# Fetch current client configuration
# Requirement addressed: Environment Specifications (11.1.2)
data "google_client_config" "current" {}

# Primary GKE cluster resource
# Requirement addressed: Kubernetes Cluster Management (11.4.1)
resource "google_container_cluster" "primary" {
  name     = "primary-gke-cluster"
  location = data.google_client_config.current.region
  
  # Network configuration
  network    = local.network_config.network
  subnetwork = local.network_config.subnetwork
  
  # Enable VPC-native cluster
  networking_mode = "VPC_NATIVE"
  
  # Initial node configuration
  initial_node_count       = local.default_node_count
  remove_default_node_pool = true
  
  # Private cluster configuration
  # Requirement addressed: Security Architecture (10.2.1)
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = local.master_ipv4_cidr
  }
  
  # Workload Identity configuration for enhanced security
  # Requirement addressed: Security Architecture (10.2.1)
  workload_identity_config {
    workload_pool = "${data.google_project.current.project_id}.svc.id.goog"
  }
  
  # Release channel configuration for automatic upgrades
  # Requirement addressed: Kubernetes Cluster Management (11.4.1)
  release_channel {
    channel = "REGULAR"
  }
  
  # Maintenance window configuration
  maintenance_policy {
    recurring_window {
      start_time = "2023-01-01T00:00:00Z"
      end_time   = "2023-01-01T04:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }
  
  # IP allocation policy for VPC-native cluster
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = ""
    services_ipv4_cidr_block = ""
  }
  
  # Master authorized networks configuration
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "0.0.0.0/0"
      display_name = "all"
    }
  }
  
  # Cluster addons configuration
  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
    network_policy_config {
      disabled = false
    }
  }
  
  # Enable network policy for enhanced security
  network_policy {
    enabled = true
    provider = "CALICO"
  }
}

# Node pool configuration
# Requirement addressed: Environment Specifications (11.1.2)
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = data.google_client_config.current.region
  cluster    = google_container_cluster.primary.id
  
  initial_node_count = local.default_node_count
  
  # Autoscaling configuration
  autoscaling {
    min_node_count = local.min_nodes
    max_node_count = local.max_nodes
  }
  
  # Node configuration
  node_config {
    machine_type = local.machine_type
    
    # OAuth scopes
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    
    # Workload Identity configuration
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
    
    # Labels for node identification
    labels = {
      environment = "production"
      node_pool   = "primary"
    }
    
    # Taints to prevent scheduling of non-tolerant pods
    taint {
      key    = "node-pool"
      value  = "primary"
      effect = "NO_SCHEDULE"
    }
    
    # Shielded instance configuration for enhanced security
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }
  
  # Management configuration for node updates
  management {
    auto_repair  = true
    auto_upgrade = true
  }
  
  # Upgrade configuration
  upgrade_settings {
    max_surge       = 1
    max_unavailable = 0
  }
}