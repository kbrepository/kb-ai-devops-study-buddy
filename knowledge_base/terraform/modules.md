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