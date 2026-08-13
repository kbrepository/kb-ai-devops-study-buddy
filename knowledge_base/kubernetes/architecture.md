
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