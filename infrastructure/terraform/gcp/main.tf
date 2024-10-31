# Human Tasks:
# 1. Ensure GCP project has required APIs enabled:
#    - Compute Engine API
#    - Kubernetes Engine API
#    - Cloud SQL Admin API
#    - Redis Enterprise API
#    - Cloud Memorystore Redis API
# 2. Configure GCP credentials and authentication
# 3. Review and adjust resource configurations based on environment needs
# 4. Ensure proper IAM roles are assigned to the service account
# 5. Verify network CIDR ranges don't conflict with existing networks

# Requirement: Cloud Infrastructure (11.1.1 Environment Architecture)
# VPC Network Module
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "~> 6.0"

  project_id   = var.project_id
  network_name = "${var.environment}-network"
  routing_mode = "REGIONAL"

  subnets = [
    {
      subnet_name   = "${var.environment}-gke-subnet"
      subnet_ip     = "10.10.0.0/20"
      subnet_region = var.region
    },
    {
      subnet_name   = "${var.environment}-db-subnet"
      subnet_ip     = "10.20.0.0/20"
      subnet_region = var.region
    }
  ]

  secondary_ranges = {
    "${var.environment}-gke-subnet" = [
      {
        range_name    = "pods"
        ip_cidr_range = "10.100.0.0/16"
      },
      {
        range_name    = "services"
        ip_cidr_range = "10.200.0.0/16"
      }
    ]
  }
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# GKE Cluster Module
module "gke" {
  source = "./modules/gke"

  project_id    = var.project_id
  region        = var.region
  cluster_name  = "${var.environment}-cluster"
  network       = module.vpc.network_name
  subnetwork    = module.vpc.subnets_names[0]
  
  # Environment-specific configurations
  machine_type  = lookup(var.gke_config[var.environment], "machine_type")
  node_count    = lookup(var.gke_config[var.environment], "node_count")
  disk_size_gb  = lookup(var.gke_config[var.environment], "disk_size_gb")

  # Pod and service secondary ranges
  ip_range_pods     = "pods"
  ip_range_services = "services"

  depends_on = [module.vpc]
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# Cloud SQL PostgreSQL Instance Module
module "cloudsql" {
  source = "./modules/cloudsql"

  project_id     = var.project_id
  region         = var.region
  instance_name  = "${var.environment}-db"
  database_name  = "codegenapp"
  network_id     = module.vpc.network_id

  # Environment-specific configurations
  tier              = lookup(var.database_config[var.environment], "tier")
  availability_type = lookup(var.database_config[var.environment], "availability_type")
  backup_enabled    = lookup(var.database_config[var.environment], "backup_enabled")

  # Database configuration
  database_version = "POSTGRES_14"
  disk_size       = 20
  disk_type       = "PD_SSD"

  # Private IP configuration
  private_network = module.vpc.network_self_link
  
  depends_on = [module.vpc]
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# Cloud Memorystore Redis Instance Module
module "redis" {
  source = "./modules/redis"

  project_id   = var.project_id
  region       = var.region
  environment  = var.environment
  network_id   = module.vpc.network_id

  # Environment-specific configurations
  tier            = lookup(var.redis_config[var.environment], "tier")
  memory_size_gb  = lookup(var.redis_config[var.environment], "memory_size_gb")
  redis_version   = lookup(var.redis_config[var.environment], "version")

  # Redis configuration
  display_name     = "${var.environment}-redis"
  reserved_ip_range = "10.30.0.0/29"
  
  depends_on = [module.vpc]
}

# Requirement: Environment Specifications (11.1.2 Environment Specifications)
# Output values for use by other resources or modules
output "gke_cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = module.gke.cluster_endpoint
  sensitive   = true
}

output "database_connection_name" {
  description = "Cloud SQL connection name"
  value       = module.cloudsql.connection_name
}

output "redis_host" {
  description = "Redis instance hostname"
  value       = module.redis.redis_host
  sensitive   = true
}

# Additional outputs for network information
output "network_name" {
  description = "The name of the VPC network"
  value       = module.vpc.network_name
}

output "subnet_names" {
  description = "The names of the subnets"
  value       = module.vpc.subnets_names
}

output "network_self_link" {
  description = "The self-link of the VPC network"
  value       = module.vpc.network_self_link
}