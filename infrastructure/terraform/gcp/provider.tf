# Human Tasks:
# 1. Ensure GCP project has required APIs enabled:
#    - Compute Engine API
#    - Kubernetes Engine API
#    - Cloud SQL Admin API
#    - Redis Enterprise API
# 2. Configure GCP credentials using one of:
#    - GOOGLE_APPLICATION_CREDENTIALS environment variable
#    - gcloud auth application-default login
#    - Service account key file
# 3. Verify project ID and region settings match your GCP setup

# Requirement: Cloud Infrastructure Provider (11.1.1 Environment Architecture)
# Configure Terraform settings and required providers
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    # Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    
    # Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
}

# Requirement: Cloud Infrastructure Provider (11.1.1 Environment Architecture)
# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
  
  # Recommended provider settings for production use
  user_project_override = true
  request_timeout      = "60s"
  request_reason      = "terraform-managed-infrastructure"
}

# Requirement: GCP Services Integration (11.2.1 Google Cloud Platform Services)
# Configure the Google Cloud Beta provider for preview features
provider "google-beta" {
  project = var.project_id
  region  = var.region
  
  # Recommended provider settings for production use
  user_project_override = true
  request_timeout      = "60s"
  request_reason      = "terraform-managed-infrastructure"
}