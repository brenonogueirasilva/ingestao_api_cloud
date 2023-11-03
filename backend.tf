terraform {
#   backend "gcs" {
#     bucket = "gcp-cloud-function-terraform-bucket-" # GCS bucket name to store terraform tfstate
#     prefix = "function"               # Prefix name should be unique for each Terraform project having same remote state bucket.
#   }
    backend "local" {}
}