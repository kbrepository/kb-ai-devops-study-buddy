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
