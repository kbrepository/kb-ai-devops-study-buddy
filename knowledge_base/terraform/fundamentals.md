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


## Terraform Cloud and Enterprise

Terraform Cloud provides remote execution, state storage, team collaboration features, and a policy-as-code engine called Sentinel. Key features include:
- Remote plan and apply with audit logs
- Workspace-based environment management
- VCS-driven workflow (plans triggered on pull requests)
- Private module registry
- Sentinel policies for compliance enforcement

---

## Common Patterns

### Blue-Green Deployments
Create new resources (blue) before destroying old ones (green) using `create_before_destroy` and traffic shifting at the load balancer level.

### Immutable Infrastructure
Replace rather than update infrastructure. Use `create_before_destroy` and avoid in-place updates to compute resources. This reduces configuration drift and improves rollback reliability.

### Terragrunt
Terragrunt is a thin wrapper around Terraform that adds features like DRY configurations, automatic backend configuration, and dependency management across modules. It is widely used in large multi-account AWS environments.

---
