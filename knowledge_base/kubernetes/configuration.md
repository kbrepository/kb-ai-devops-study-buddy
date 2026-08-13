## Configuration and Secrets

### ConfigMap

ConfigMaps store non-sensitive configuration data as key-value pairs. Can be consumed as environment variables, command-line arguments, or mounted as files.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgres://db:5432/mydb"
  LOG_LEVEL: "info"
```

### Secret

Secrets store sensitive data (passwords, tokens, TLS certificates). Encoded in base64 (not encrypted by default). Enable etcd encryption at rest for production security. Use external secret managers (AWS Secrets Manager + External Secrets Operator, HashiCorp Vault) for true secrets management.

Types of secrets: `Opaque` (generic), `kubernetes.io/tls` (TLS certs), `kubernetes.io/dockerconfigjson` (registry credentials), `kubernetes.io/service-account-token`.

---