terraform {
    required_version = ">= 1.2.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
}

# Configure AWS provider
provider "aws" {
    region = var.aws_region
}



# Create S3 bucket
resource "aws_s3_bucket" "jobdata-bucket" {
  bucket = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

resource "aws_s3_bucket_ownership_controls" "example" {
  bucket = aws_s3_bucket.jobdata-bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_jobdata-bucket_acl" {
  bucket = aws_s3_bucket.jobdata-bucket.id
  acl    = "private"
}