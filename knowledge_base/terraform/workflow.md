

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