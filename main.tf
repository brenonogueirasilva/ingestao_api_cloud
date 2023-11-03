#File Zip for the Cloud Function
data "archive_file" "my_function_zip" {
    type = "zip"
    source_dir = "${path.module}/src"
    output_path = "${path.module}/src.zip"
}

#Cloud Storage Create a Bucket
resource "google_storage_bucket" "function_source_bucket" {
  name = "brasil_api_function_bucket"
  location = var.region
}

#Cloud Storage create a bucket_object
resource "google_storage_bucket_object" "function_source_bucket_object" {
  name   = "brasil-api-bucket-object"
  bucket = google_storage_bucket.function_source_bucket.name
  source = data.archive_file.my_function_zip.output_path
}

#Google Cloud Function  
resource "google_cloudfunctions2_function" "my_function" {
    name = "brasil-api-terraform"
    description = "brasil api function to deploy"
    location = var.region

    build_config {
    runtime     = "python310"
    entry_point = "main" 
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_source_bucket.name
        object = google_storage_bucket_object.function_source_bucket_object.name
      }
    }
    }
    service_config {
    max_instance_count  = 1
    min_instance_count = 0
    available_memory    = "512M"
    timeout_seconds     = 60
    all_traffic_on_latest_revision = true
    }
    
    }

