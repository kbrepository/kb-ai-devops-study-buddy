# Kubernetes Knowledge Base

## What is Kubernetes

Kubernetes (K8s) is an open-source container orchestration platform originally developed by Google and donated to the CNCF (Cloud Native Computing Foundation). It automates the deployment, scaling, and management of containerized applications. Kubernetes abstracts away the underlying infrastructure, allowing applications to run consistently across on-premises, cloud, and hybrid environments.

Key design philosophy: declarative configuration. You describe the desired state of your system, and Kubernetes continuously works to maintain that state.


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