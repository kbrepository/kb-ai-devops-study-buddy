
## Terraform State

### What is State
Terraform state is a JSON file (typically `terraform.tfstate`) that maps real-world resources to your configuration. Terraform uses state to determine what changes need to be made. Without state, Terraform cannot track what infrastructure it manages.

### State Locking
State locking prevents multiple users or automation processes from running Terraform simultaneously, which could corrupt state. When using remote backends like S3 with DynamoDB, Terraform automatically acquires and releases locks.

DynamoDB table for state locking requires a partition key named `LockID` of type String.

### Remote Backends
Storing state remotely enables team collaboration and improves security. The S3 backend is the most common choice for AWS users.

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

Other supported backends include: Terraform Cloud, Azure Blob Storage, GCS, Consul, and HTTP.

### State Drift
State drift occurs when infrastructure is modified outside of Terraform (e.g., manually via the AWS Console). Terraform detects drift when you run `terraform plan` by comparing the state file with the actual infrastructure. Use `terraform refresh` to update the state file to match real infrastructure without making changes.

### State Commands
- `terraform state list` — lists all resources in state
- `terraform state show <resource>` — shows attributes of a specific resource
- `terraform state mv` — moves a resource from one state address to another (useful for refactoring)
- `terraform state rm` — removes a resource from state without destroying it
- `terraform import` — imports existing infrastructure into Terraform state

---