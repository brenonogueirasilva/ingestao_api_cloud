terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.69.1"
    }
  }
}

provider "google" {
  credentials = file("./apt-theme-402300-32506a51a70d.json")
  project     = var.project_id
  region      = var.region
}