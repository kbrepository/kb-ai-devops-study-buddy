## Workspaces

Terraform workspaces allow you to manage multiple distinct state files from a single configuration. Each workspace has its own state file. Workspaces are useful for managing environments (dev/staging/prod) within a single configuration but are not a substitute for full environment separation.

```bash
terraform workspace new staging
terraform workspace select prod
terraform workspace list
```

In configuration, reference the current workspace with `terraform.workspace`.

---