

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