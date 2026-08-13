## Storage

### S3 (Simple Storage Service)

S3 is object storage offering unlimited scalability. Objects are stored in buckets. Each object has a key (path-like name), value (data), metadata, and optional version ID.

**Storage Classes:**
- S3 Standard — frequently accessed data, low latency
- S3 Intelligent-Tiering — automatically moves objects between tiers based on access patterns
- S3 Standard-IA (Infrequent Access) — lower cost, retrieval fee
- S3 One Zone-IA — single AZ, cheaper, less resilient
- S3 Glacier Instant Retrieval — archive with millisecond retrieval
- S3 Glacier Flexible Retrieval — minutes to hours retrieval
- S3 Glacier Deep Archive — lowest cost, 12-hour retrieval

**Key Features:**
- Versioning — retains all versions of an object; protects against accidental deletion
- Lifecycle Policies — automatically transition objects between storage classes or delete them
- Replication — Cross-Region Replication (CRR) and Same-Region Replication (SRR)
- Event Notifications — trigger Lambda, SQS, or SNS on object events
- Presigned URLs — temporary access URLs for objects without requiring AWS credentials

**Security:**
- Block Public Access settings — should be enabled by default
- Bucket Policies — resource-based policies for cross-account access
- ACLs — legacy, prefer bucket policies
- SSE-S3 — server-side encryption with S3-managed keys
- SSE-KMS — encryption with AWS KMS keys (audit trail, key rotation)
- SSE-C — encryption with customer-provided keys

### EBS (Elastic Block Store)

EBS provides persistent block storage volumes for EC2 instances. Volumes are tied to an AZ. Must be manually snapshotted for backup. Only one EC2 instance can attach an EBS volume at a time (except io1/io2 Multi-Attach).

**Volume Types:**
- gp3 — general purpose SSD, 3000 IOPS baseline, recommended default
- gp2 — general purpose SSD, IOPS tied to size
- io2 Block Express — high performance, up to 256,000 IOPS
- st1 — throughput-optimized HDD, for big data, data warehouses
- sc1 — cold HDD, lowest cost, infrequent access

**Snapshots:** Point-in-time backups stored in S3. Incremental — only changed blocks are saved after the first snapshot. Can be copied across regions for disaster recovery.

### EFS (Elastic File System)

EFS is a managed NFS file system that can be mounted by multiple EC2 instances simultaneously across AZs. Auto-scales storage. Supports Standard and Infrequent Access storage classes. More expensive than EBS per GB but eliminates capacity planning.