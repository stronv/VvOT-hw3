terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.135.0"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  service_account_key_file = pathexpand("~/.yc-keys/key.json")
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = var.zone
}

variable "zone" {
  type        = string
  default     = "ru-central1-d"
}

variable "cloud_id" {
  type        = string
}

variable "folder_id" {
  type        = string
}
