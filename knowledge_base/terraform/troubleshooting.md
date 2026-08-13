
## Troubleshooting

- `Error: Resource already exists` — Resource exists in AWS but not in state. Use `terraform import`.
- `Error acquiring state lock` — A previous run left a stale lock. Manually delete the lock item from DynamoDB or use `terraform force-unlock <LOCK_ID>`.
- Provider version conflicts — Pin provider versions in `required_providers` and run `terraform init -upgrade`.
- Dependency cycles — Terraform will error if resources depend on each other circularly. Restructure references or use `depends_on` carefully.