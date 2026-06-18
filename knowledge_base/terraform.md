# Terraform Knowledge Base

## What is Terraform

Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It allows you to define, provision, and manage infrastructure across multiple cloud providers and on-premises environments using a declarative configuration language called HCL (HashiCorp Configuration Language). Terraform follows the principle of desired state configuration — you describe what infrastructure you want, and Terraform figures out how to create or modify existing resources to reach that state.

---

## Core Concepts

### Providers
Providers are plugins that allow Terraform to interact with APIs of cloud platforms and services. Each provider defines a set of resource types and data sources. Common providers include AWS, Azure, GCP, Kubernetes, and GitHub.

```hcl
provider "aws" {
  region = "us-east-1"
}
```

Providers must be declared and initialized before use. Terraform downloads provider plugins during `terraform init`. Provider versioning is critical for reproducibility — always pin provider versions in the `required_providers` block.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Resources
Resources are the fundamental building blocks in Terraform. Each resource block describes one or more infrastructure objects, such as an EC2 instance, an S3 bucket, or a VPC.

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}
```

Resource syntax: `resource "<PROVIDER>_<TYPE>" "<LOCAL_NAME>"`. The local name is used to reference the resource within the same module.

### Data Sources
Data sources allow Terraform to fetch information about existing infrastructure that was not created by the current Terraform configuration. They are read-only.

```hcl
data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

Data sources are commonly used to look up AMI IDs, availability zones, existing VPCs, or IAM policies.

### Variables
Input variables make Terraform configurations flexible and reusable. Variables can have types, default values, descriptions, and validation rules.

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro", "t3.small"], var.instance_type)
    error_message = "Instance type must be t2.micro, t3.micro, or t3.small."
  }
}
```

Variable values can be passed via CLI flags (`-var`), `.tfvars` files, environment variables (`TF_VAR_name`), or interactive prompts.

### Outputs
Output values expose specific data from a Terraform configuration, making it available for use by other configurations, CI/CD pipelines, or humans.

```hcl
output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web.public_ip
}
```

### Locals
Local values are computed expressions assigned to a name, useful for avoiding repetition and simplifying complex expressions.

```hcl
locals {
  common_tags = {
    Project     = "MyApp"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

---

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

## Terraform Workflow

### Init
`terraform init` initializes a working directory. It downloads provider plugins, sets up the backend, and installs modules. Must be run before any other command, and re-run when providers or modules change.

### Plan
`terraform plan` creates an execution plan showing what actions Terraform will take to reach the desired state. It compares configuration, state, and real infrastructure. Always review the plan before applying. Use `-out=planfile` to save the plan for later use.

### Apply
`terraform apply` executes the changes described in a plan. It asks for confirmation by default. Use `-auto-approve` to skip confirmation in automation pipelines. Pass a saved plan file to apply exactly what was reviewed.

### Destroy
`terraform destroy` removes all resources managed by the configuration. It generates a destroy plan and asks for confirmation. In production, prefer targeted destruction over full destroy.

### Validate and Format
- `terraform validate` — checks that configuration is syntactically valid and internally consistent
- `terraform fmt` — rewrites configuration files to the canonical HCL format
- `terraform graph` — produces a visual dependency graph in DOT format

---

## Modules

### What are Modules
Modules are reusable, self-contained packages of Terraform configuration. Every Terraform configuration is technically a module (the root module). Child modules are called from the root module.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}
```

### Module Sources
Modules can be sourced from:
- Local paths (`./modules/networking`)
- Terraform Registry (`hashicorp/consul/aws`)
- GitHub or other VCS repositories
- S3 buckets or GCS buckets

### Module Best Practices
- Keep modules focused on a single concern (networking, compute, security)
- Always version-pin registry modules
- Use input variable validation to enforce contracts
- Expose only the outputs that callers need
- Document all variables and outputs with descriptions

---

## Dependencies and Meta-Arguments

### Implicit Dependencies
Terraform automatically infers dependencies when one resource references another using expressions. It builds a dependency graph and creates resources in the correct order.

### Explicit Dependencies
Use `depends_on` to declare dependencies that Terraform cannot detect automatically (e.g., a Lambda function that needs an S3 bucket policy to exist before it can run).

```hcl
resource "aws_instance" "app" {
  depends_on = [aws_iam_role_policy.app_policy]
}
```

### Count and For Each
`count` creates multiple instances of a resource using an integer.

```hcl
resource "aws_instance" "server" {
  count         = 3
  ami           = var.ami_id
  instance_type = "t3.micro"
}
```

`for_each` creates multiple instances from a map or set, giving each instance a meaningful key.

```hcl
resource "aws_iam_user" "team" {
  for_each = toset(["alice", "bob", "carol"])
  name     = each.key
}
```

Prefer `for_each` over `count` when managing collections of similar resources, because adding or removing items in the middle of a list doesn't cause index-based replacement with `for_each`.

### Lifecycle
The `lifecycle` block controls resource behavior during creation, updates, and destruction.

```hcl
resource "aws_instance" "web" {
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [tags]
    prevent_destroy       = true
  }
}
```

- `create_before_destroy` — creates a replacement resource before destroying the old one (useful for zero-downtime updates)
- `ignore_changes` — tells Terraform to ignore changes to specific attributes
- `prevent_destroy` — prevents accidental destruction of critical resources

---

## Workspaces

Terraform workspaces allow you to manage multiple distinct state files from a single configuration. Each workspace has its own state file. Workspaces are useful for managing environments (dev/staging/prod) within a single configuration but are not a substitute for full environment separation.

```bash
terraform workspace new staging
terraform workspace select prod
terraform workspace list
```

In configuration, reference the current workspace with `terraform.workspace`.

---

## Terraform Cloud and Enterprise

Terraform Cloud provides remote execution, state storage, team collaboration features, and a policy-as-code engine called Sentinel. Key features include:
- Remote plan and apply with audit logs
- Workspace-based environment management
- VCS-driven workflow (plans triggered on pull requests)
- Private module registry
- Sentinel policies for compliance enforcement

---

## Security Best Practices

- Never store sensitive values in plain text in `.tf` files or state files
- Mark sensitive variables with `sensitive = true` to suppress output
- Use `aws_secretsmanager_secret` or `vault_generic_secret` to retrieve secrets at runtime
- Enable state file encryption at rest (S3 server-side encryption)
- Restrict access to the state bucket and DynamoDB lock table using IAM policies
- Use separate AWS accounts or Terraform workspaces per environment
- Rotate provider credentials regularly; prefer IAM roles over long-lived access keys

---

## Common Patterns

### Blue-Green Deployments
Create new resources (blue) before destroying old ones (green) using `create_before_destroy` and traffic shifting at the load balancer level.

### Immutable Infrastructure
Replace rather than update infrastructure. Use `create_before_destroy` and avoid in-place updates to compute resources. This reduces configuration drift and improves rollback reliability.

### Terragrunt
Terragrunt is a thin wrapper around Terraform that adds features like DRY configurations, automatic backend configuration, and dependency management across modules. It is widely used in large multi-account AWS environments.

---

## Troubleshooting

- `Error: Resource already exists` — Resource exists in AWS but not in state. Use `terraform import`.
- `Error acquiring state lock` — A previous run left a stale lock. Manually delete the lock item from DynamoDB or use `terraform force-unlock <LOCK_ID>`.
- Provider version conflicts — Pin provider versions in `required_providers` and run `terraform init -upgrade`.
- Dependency cycles — Terraform will error if resources depend on each other circularly. Restructure references or use `depends_on` carefully.