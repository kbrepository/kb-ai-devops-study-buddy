
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