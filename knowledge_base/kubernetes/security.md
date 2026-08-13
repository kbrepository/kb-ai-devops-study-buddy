## Security Best Practices

- Enable RBAC and apply least privilege
- Use Pod Security Standards (Baseline or Restricted) to enforce security context constraints
- Never run containers as root; set `runAsNonRoot: true`
- Use read-only root filesystems where possible: `readOnlyRootFilesystem: true`
- Drop all Linux capabilities and add only what's needed: `capabilities: drop: ["ALL"]`
- Scan container images for vulnerabilities (Trivy, Snyk, ECR image scanning)
- Use Network Policies to restrict pod-to-pod traffic
- Encrypt secrets at rest in etcd
- Use External Secrets Operator or Vault Agent for production secrets management
- Enable audit logging on the API server
- Keep Kubernetes version up to date; supported versions receive security patches