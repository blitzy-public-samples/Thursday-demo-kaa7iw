# Human tasks:
# 1. Ensure that the GKE cluster has been successfully created before accessing these outputs
# 2. Store the cluster_ca_certificate output securely as it contains sensitive information
# 3. Use these outputs for configuring kubectl and other tools that need to interact with the cluster

# Requirement addressed: Kubernetes Cluster Management (11.4.1)
# Exposes the unique identifier of the GKE cluster for resource referencing
output "cluster_id" {
  description = "The unique identifier of the GKE cluster"
  value       = google_container_cluster.primary.id
}

# Requirement addressed: Kubernetes Cluster Management (11.4.1)
# Exposes the cluster endpoint for kubectl and API server access
output "cluster_endpoint" {
  description = "The IP address of the cluster's Kubernetes master endpoint"
  value       = google_container_cluster.primary.endpoint
}

# Requirement addressed: Security Architecture (10.2.1)
# Exposes the cluster CA certificate for secure communication with the API server
output "cluster_ca_certificate" {
  description = "The public certificate authority (CA) certificate used by the cluster's certificate authority"
  value       = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  sensitive   = true
}

# Requirement addressed: Kubernetes Cluster Management (11.4.1)
# Exposes the cluster name for resource identification and management
output "cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

# Requirement addressed: Kubernetes Cluster Management (11.4.1)
# Exposes the cluster location for regional/zonal operations
output "cluster_location" {
  description = "The location (region or zone) of the GKE cluster"
  value       = google_container_cluster.primary.location
}