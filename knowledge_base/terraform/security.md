## Security Best Practices

- Never store sensitive values in plain text in `.tf` files or state files
- Mark sensitive variables with `sensitive = true` to suppress output
- Use `aws_secretsmanager_secret` or `vault_generic_secret` to retrieve secrets at runtime
- Enable state file encryption at rest (S3 server-side encryption)
- Restrict access to the state bucket and DynamoDB lock table using IAM policies
- Use separate AWS accounts or Terraform workspaces per environment
- Rotate provider credentials regularly; prefer IAM roles over long-lived access keys

---