# KAN-464: Terraform variables
variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources in."
  type        = string
  default     = "us-central1"
}

variable "app_name" {
  description = "The name of the application."
  type        = string
  default     = "conversational-agent"
}

variable "db_password" {
  description = "The password for the Cloud SQL database."
  type        = string
  sensitive   = true
}
