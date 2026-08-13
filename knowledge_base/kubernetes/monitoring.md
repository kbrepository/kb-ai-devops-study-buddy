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
