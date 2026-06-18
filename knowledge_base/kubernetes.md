# Kubernetes Knowledge Base

## What is Kubernetes

Kubernetes (K8s) is an open-source container orchestration platform originally developed by Google and donated to the CNCF (Cloud Native Computing Foundation). It automates the deployment, scaling, and management of containerized applications. Kubernetes abstracts away the underlying infrastructure, allowing applications to run consistently across on-premises, cloud, and hybrid environments.

Key design philosophy: declarative configuration. You describe the desired state of your system, and Kubernetes continuously works to maintain that state.

---

## Architecture

### Control Plane Components

The control plane manages the cluster and makes global decisions about scheduling, scaling, and responding to cluster events.

**kube-apiserver:** The front end of the Kubernetes control plane. All communication — internal and external — passes through the API server. It validates and processes REST requests, updating the cluster state in etcd. Horizontally scalable.

**etcd:** Highly available, distributed key-value store. The single source of truth for all cluster state. All cluster data (pods, services, configs) is stored here. Backups of etcd are critical for disaster recovery.

**kube-scheduler:** Watches for newly created pods with no assigned node and selects the best node based on resource requirements, affinity/anti-affinity rules, taints, tolerations, and policies.

**kube-controller-manager:** Runs controller processes that watch the cluster state and make changes to drive it toward the desired state. Examples:
- Node Controller — monitors node health
- Deployment Controller — manages ReplicaSets
- Endpoint Controller — manages Service-to-Pod endpoint mapping
- Job Controller — manages batch Jobs

**cloud-controller-manager:** Integrates with cloud provider APIs. Manages cloud-specific controllers for nodes, routes, and load balancers. Separates cloud-provider logic from core Kubernetes code.

### Node Components

Nodes (formerly called minions) are the worker machines that run containerized workloads.

**kubelet:** Agent running on every node. Ensures containers described in PodSpecs are running and healthy. Communicates with the API server. Does not manage containers not created by Kubernetes.

**kube-proxy:** Network proxy running on each node. Maintains network rules (iptables or IPVS) to route traffic to Services. Handles connection forwarding.

**Container Runtime:** The software responsible for running containers. Kubernetes supports any runtime implementing the Container Runtime Interface (CRI). Common runtimes: containerd (default in modern clusters), CRI-O, Docker Engine (via dockershim, deprecated in K8s 1.24).

---

## Core Workload Objects

### Pod

A Pod is the smallest deployable unit in Kubernetes. It encapsulates one or more containers that share the same network namespace (same IP, same ports) and storage volumes. Containers in a pod communicate via `localhost`.

Pods are ephemeral — when a pod dies, it is not resurrected. Higher-level controllers manage pod lifecycle.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
  - name: app
    image: nginx:1.25
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

**Init Containers:** Run before app containers. Complete sequentially. Used for setup tasks like waiting for a database to be ready or copying config files.

**Sidecar Containers:** Run alongside the main app container in the same pod. Common patterns: log shippers (Fluentd), service mesh proxies (Envoy/Istio), secret fetchers (Vault Agent).

### Deployment

A Deployment manages a ReplicaSet, which manages multiple identical pod replicas. Deployments support rolling updates and rollbacks.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:v2
```

**Rolling Update Strategy:** Gradually replaces old pods with new ones. `maxSurge` controls how many extra pods can exist during update. `maxUnavailable` controls how many pods can be unavailable.

**Rollback:** `kubectl rollout undo deployment/my-app` reverts to the previous revision. `kubectl rollout history deployment/my-app` shows revision history.

### StatefulSet

StatefulSets manage stateful applications (databases, queues). Unlike Deployments, each pod gets a stable network identity (e.g., `pod-0`, `pod-1`) and dedicated persistent storage that follows the pod even after rescheduling.

Pods are created and deleted in order. Suitable for: MySQL, PostgreSQL, Cassandra, Kafka, Zookeeper, Redis Sentinel.

### DaemonSet

Ensures a copy of a pod runs on every (or selected) node. Used for: log collectors (Fluentd, Filebeat), monitoring agents (Datadog, Prometheus Node Exporter), network plugins, storage plugins.

### Job and CronJob

**Job:** Runs a pod to completion. Useful for batch processing, database migrations, report generation. Retries on failure. Can run pods in parallel.

**CronJob:** Schedules Jobs on a cron schedule. Used for periodic tasks like backups, cleanup, report generation.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: db-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: db-backup:latest
          restartPolicy: OnFailure
```

---

## Services and Networking

### Service

A Service provides a stable IP address and DNS name for a set of pods, abstracting away pod churn. Services use label selectors to identify the pods they route to.

**ClusterIP (default):** Internal-only virtual IP. Accessible only within the cluster. Used for communication between microservices.

**NodePort:** Exposes the service on a static port on every node's IP. Accessible externally via `<NodeIP>:<NodePort>`. Port range: 30000–32767.

**LoadBalancer:** Provisions a cloud load balancer (e.g., AWS ELB/NLB, GCP LB). External IP assigned. Most common way to expose production services. Each LoadBalancer service creates a separate cloud load balancer (can be costly at scale).

**ExternalName:** Maps a service to an external DNS name. No proxy involved. Useful for accessing external services as if they were in-cluster.

**Headless Services:** Set `clusterIP: None`. DNS returns pod IPs directly instead of a virtual IP. Used with StatefulSets for peer discovery.

### Ingress

Ingress manages external HTTP/HTTPS routing to multiple services within the cluster. Provides:
- Host-based routing (`api.example.com` → api-service)
- Path-based routing (`/api` → api-service, `/` → frontend-service)
- TLS termination

Requires an **Ingress Controller** to be deployed (nginx-ingress, AWS ALB Ingress Controller, Traefik, Istio Gateway). The controller watches Ingress resources and configures the underlying load balancer or proxy.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### Network Policies

Network Policies control traffic between pods and namespaces at Layer 3/4. By default, all pods can communicate with all other pods. Network Policies use label selectors to define ingress and egress rules. Requires a CNI plugin that supports Network Policy (Calico, Cilium, Weave Net).

---

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

## Storage

### Volumes

A Volume is a directory accessible to containers in a pod. Volumes outlive containers in the pod but not the pod itself.

Common volume types:
- `emptyDir` — temporary storage on the node, deleted when pod dies
- `hostPath` — mounts a file or directory from the host node
- `configMap` / `secret` — mount config or secret data as files
- `persistentVolumeClaim` — mounts persistent storage

### Persistent Volumes (PV) and Persistent Volume Claims (PVC)

**PersistentVolume (PV):** A piece of storage provisioned by an administrator or dynamically via a StorageClass. Independent of any pod.

**PersistentVolumeClaim (PVC):** A request for storage by a user or pod. Binds to a PV that satisfies the requested capacity and access mode.

**StorageClass:** Defines the provisioner and parameters for dynamic volume provisioning. When a PVC specifies a StorageClass, Kubernetes dynamically creates a PV.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  storageClassName: gp2
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

**Access Modes:**
- `ReadWriteOnce (RWO)` — single node read/write (EBS, gp2)
- `ReadOnlyMany (ROX)` — many nodes read-only
- `ReadWriteMany (RWX)` — many nodes read/write (EFS, NFS)

---

## Scheduling

### Resource Requests and Limits

`requests` — minimum resources guaranteed to the container; used by the scheduler to place pods.
`limits` — maximum resources the container can use.

CPU is compressible (throttled when over limit). Memory is not compressible — exceeding memory limit causes OOMKilled.

### Node Affinity and Anti-Affinity

**Node Affinity:** Constrains which nodes a pod can be scheduled on based on node labels.
- `requiredDuringSchedulingIgnoredDuringExecution` — hard constraint
- `preferredDuringSchedulingIgnoredDuringExecution` — soft constraint

**Pod Affinity:** Schedule pods near (or away from) other pods based on labels.
**Pod Anti-Affinity:** Spread pods across nodes or zones to improve availability.

### Taints and Tolerations

**Taints** are applied to nodes to repel pods. Format: `key=value:effect`. Effects: `NoSchedule`, `PreferNoSchedule`, `NoExecute`.

**Tolerations** are applied to pods to allow scheduling on tainted nodes.

Use case: Dedicate nodes for specific workloads (GPU nodes, high-memory nodes), or mark nodes as unschedulable during maintenance.

### Priority and Preemption

PriorityClasses assign priority values to pods. Higher-priority pods can preempt (evict) lower-priority pods if cluster resources are constrained. Useful for ensuring critical workloads always get scheduled.

---

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

HPA automatically scales the number of pod replicas based on observed metrics (CPU, memory, or custom metrics). Requires Metrics Server.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

### Vertical Pod Autoscaler (VPA)

VPA automatically adjusts CPU and memory requests and limits based on actual usage. Can update pods in-place (Kubernetes 1.27+) or recommend values. Avoid using VPA and HPA on the same resource simultaneously.

### Cluster Autoscaler

Cluster Autoscaler automatically adjusts the number of nodes in the cluster. Scales up when pods are unschedulable due to resource constraints. Scales down when nodes are underutilized and pods can be rescheduled elsewhere.

On AWS, Cluster Autoscaler integrates with EC2 Auto Scaling Groups. KARPENTER is a modern alternative that is more efficient and flexible.

---

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

## Observability

### Metrics

Kubernetes exposes metrics via the Metrics Server (resource metrics) and via custom metrics adapters (Prometheus Adapter). Prometheus + Grafana is the de facto monitoring stack.

kube-state-metrics exposes metrics about Kubernetes object state (deployment replicas, pod phases, job completions).

### Logging

Kubernetes does not provide a built-in centralized logging solution. Common patterns:
- Node-level logging: DaemonSet agents (Fluentd, Fluent Bit, Filebeat) collect container logs from each node and ship to a central store (OpenSearch, Loki, Splunk, CloudWatch Logs)
- Sidecar pattern: Log-shipping sidecar containers for applications with non-standard log formats

### Probes

Probes allow Kubernetes to detect container health and readiness.

**Liveness Probe:** Kubernetes restarts the container if the probe fails. Used to detect deadlocks or crashed applications.

**Readiness Probe:** Kubernetes removes the pod from Service endpoints if the probe fails. Used to signal when the app is not ready to receive traffic (during startup or under load).

**Startup Probe:** Disables liveness and readiness probes until it succeeds. Used for slow-starting applications to avoid premature restarts.

Probe types: HTTP GET, TCP Socket, Exec (command).

---

## Kubernetes on AWS: EKS

Amazon EKS (Elastic Kubernetes Service) is AWS's managed Kubernetes service. AWS manages the control plane (API server, etcd, controller manager). You manage worker nodes.

**EKS Managed Node Groups:** AWS manages the lifecycle (provisioning, patching, scaling) of EC2 instances in the node group. Supports on-demand and Spot.

**Fargate on EKS:** Run pods on serverless infrastructure. No node management. Pod-level isolation. Pay per vCPU and memory per second.

**EKS Add-ons:** Managed versions of common cluster components: CoreDNS, kube-proxy, Amazon VPC CNI, EBS CSI driver.

**AWS VPC CNI:** Assigns VPC IP addresses directly to pods, enabling pods to communicate natively within the VPC. Each pod gets a real VPC IP.

**IRSA (IAM Roles for Service Accounts):** Associates a Kubernetes ServiceAccount with an AWS IAM Role using OIDC. Pods using the ServiceAccount automatically get temporary AWS credentials via STS. The recommended approach for AWS API access from pods (replaces node-level instance profiles).

---

## Helm

Helm is the package manager for Kubernetes. Helm Charts package Kubernetes manifests with templating. Charts can be installed, upgraded, and rolled back.

```bash
helm install my-release bitnami/nginx
helm upgrade my-release bitnami/nginx --set replicaCount=3
helm rollback my-release 1
helm uninstall my-release
```

**Chart Structure:**
- `Chart.yaml` — chart metadata
- `values.yaml` — default configuration values
- `templates/` — Kubernetes manifests with Go templating

**Helm Repositories:** Public repos (Bitnami, Artifact Hub) and private repos. OCI-compatible registries (ECR, GHCR) can store Helm charts.

---

## GitOps and Continuous Delivery

**ArgoCD** and **Flux** are popular GitOps controllers. They continuously sync Kubernetes cluster state with a Git repository. Any change merged to Git is automatically applied to the cluster. Provides auditability, easy rollback (revert the Git commit), and drift detection.

GitOps principles: Git is the single source of truth. All changes via pull requests. Automated reconciliation loop.

---

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