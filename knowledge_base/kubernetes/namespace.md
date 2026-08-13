
## Namespaces and RBAC

### Namespaces

Namespaces provide logical isolation within a cluster. Resource names must be unique within a namespace. Resources like Nodes and PersistentVolumes are cluster-scoped (not namespace-scoped).

Common namespace pattern: `default`, `kube-system` (system components), `kube-public`, and custom namespaces per team or environment.

### RBAC (Role-Based Access Control)

RBAC controls who can do what within a Kubernetes cluster.

**Role:** Defines permissions within a specific namespace.
**ClusterRole:** Defines permissions cluster-wide.
**RoleBinding:** Grants a Role to a user or ServiceAccount in a namespace.
**ClusterRoleBinding:** Grants a ClusterRole to a user or ServiceAccount cluster-wide.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

**ServiceAccounts:** Identities for processes running in pods. Pods use ServiceAccounts to authenticate to the Kubernetes API. On AWS EKS, IRSA (IAM Roles for Service Accounts) links Kubernetes ServiceAccounts to AWS IAM Roles.

---
