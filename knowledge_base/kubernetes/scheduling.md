
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