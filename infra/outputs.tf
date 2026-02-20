# KAN-464: Terraform outputs

output "cloud_run_service_url" {
  description = "The URL of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.main.uri
}

output "database_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance."
  value       = google_sql_database_instance.main.connection_name
}
