

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