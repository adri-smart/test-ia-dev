# KAN-464, KAN-465: Basic Terraform Infrastructure for GCP
# This is a placeholder for a production-ready setup.
# It outlines resources for Cloud Run, Cloud SQL, and Secret Manager.

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# --- Networking ---
resource "google_project_service" "vpcaccess" {
  service = "vpcaccess.googleapis.com"
}

resource "google_vpc_access_connector" "main" {
  name          = "${var.app_name}-vpc-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28"
  depends_on    = [google_project_service.vpcaccess]
}

# --- Database (Cloud SQL) ---
resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"
}

resource "google_sql_database_instance" "main" {
  name             = "${var.app_name}-db-instance"
  database_version = "POSTGRES_13"
  region           = var.region
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = "projects/${var.project_id}/global/networks/default"
    }
  }
  deletion_protection = false # Set to true in production
  depends_on          = [google_project_service.sqladmin]
}

resource "google_sql_database" "main_db" {
  instance = google_sql_database_instance.main.name
  name     = "customer_db"
}

resource "google_sql_user" "main_user" {
  instance = google_sql_database_instance.main.name
  name     = "user"
  password = var.db_password
}

# --- Secret Management ---
resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
}

resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = "GEMINI_API_KEY"
  replication {
    automatic = true
  }
  depends_on = [google_project_service.secretmanager]
}

# --- Application (Cloud Run) ---
resource "google_project_service" "run" {
  service = "run.googleapis.com"
}

resource "google_cloud_run_v2_service" "main" {
  name     = var.app_name
  location = var.region
  template {
    containers {
      image = "gcr.io/${var.project_id}/${var.app_name}:latest" # Assumes image is pushed to GCR
      ports {
        container_port = 8080 # Gunicorn port
      }
      env {
        name  = "DB_HOST"
        value = google_sql_database_instance.main.private_ip_address
      }
      # Other env vars (DB_USER, DB_NAME, etc.) would be set here
      # Secrets would be mounted from Secret Manager
    }
    vpc_access {
      connector = google_vpc_access_connector.main.id
      egress    = "all-traffic"
    }
  }
  depends_on = [google_project_service.run]
}
