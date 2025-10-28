# Backend configuration for Terraform state
terraform {
  backend "s3" {
    bucket = "ecommerce-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
    
    # Enable state locking
    dynamodb_table = "ecommerce-terraform-locks"
    encrypt        = true
    
    # Enable versioning
    versioning = true
  }
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name           = "ecommerce-terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform State Locking"
  }
}
