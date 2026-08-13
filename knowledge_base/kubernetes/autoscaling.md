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
