# AWS Knowledge Base

## What is AWS

Amazon Web Services (AWS) is the world's most comprehensive and broadly adopted cloud platform, offering over 200 fully featured services from data centers globally. AWS provides on-demand access to compute power, storage, databases, networking, analytics, machine learning, security, and more — all with a pay-as-you-go pricing model. AWS follows a shared responsibility model: AWS manages security of the cloud, customers manage security in the cloud.

---

## Identity and Access Management (IAM)

### Core IAM Concepts
IAM controls who (authentication) and what (authorization) can access AWS resources. It is global — not region-specific.

**Users** represent individual people or applications. They have long-term credentials (access keys and passwords). Best practice: avoid using the root account for daily work. Create individual IAM users.

**Groups** are collections of IAM users. Attach policies to groups rather than individual users for easier permission management.

**Roles** are IAM identities with policies that can be assumed by users, AWS services, or federated identities. Roles have temporary credentials (via STS). EC2 instances, Lambda functions, and ECS tasks use roles to interact with other AWS services.

**Policies** are JSON documents defining permissions. Types:
- **AWS Managed Policies** — maintained by AWS
- **Customer Managed Policies** — created and managed by you
- **Inline Policies** — embedded directly in a user, group, or role

### Policy Evaluation Logic
IAM uses an explicit deny model. Evaluation order:
1. Explicit Deny — always wins
2. Service Control Policy (SCP) limits
3. Explicit Allow
4. Implicit Deny (default)

### IAM Best Practices
- Enable MFA for all users, especially root
- Use IAM roles for EC2, Lambda, ECS instead of embedding access keys
- Apply least privilege — grant only permissions needed
- Rotate access keys regularly
- Use IAM Access Analyzer to identify overly permissive policies
- Use permission boundaries to limit maximum permissions

---

## Compute

### EC2 (Elastic Compute Cloud)

EC2 provides resizable virtual servers. Key concepts:

**Instance Types** are categorized by use case:
- General Purpose: `t3`, `m6i` — balanced compute, memory, networking
- Compute Optimized: `c6i` — high CPU workloads (batch, HPC)
- Memory Optimized: `r6i`, `x2idn` — in-memory databases, analytics
- Storage Optimized: `i4i`, `d3` — high sequential I/O
- Accelerated Computing: `p4`, `g5` — GPU workloads, ML

**Purchasing Options:**
- **On-Demand** — pay per second/hour, no commitment
- **Reserved Instances (RI)** — 1 or 3 year commitment, up to 72% discount
- **Savings Plans** — flexible alternative to RIs, applies to EC2, Fargate, Lambda
- **Spot Instances** — use spare AWS capacity, up to 90% discount, can be interrupted with 2-minute warning
- **Dedicated Hosts** — physical servers dedicated to your use, for compliance/licensing

**AMI (Amazon Machine Image):** Template for the instance OS and pre-installed software. Can be AWS-provided, marketplace, or custom.

**User Data:** Scripts passed at launch time to bootstrap instances (install packages, configure services). Runs once on first boot.

**Instance Metadata Service (IMDS):** EC2 instances can query `http://169.254.169.254/latest/meta-data/` to retrieve metadata like instance ID, region, IAM role credentials. IMDSv2 (token-based) is recommended over IMDSv1 for security.

**Placement Groups:**
- Cluster — low latency, high throughput within single AZ
- Spread — maximum availability, instances on different hardware
- Partition — groups of instances on separate hardware partitions, for distributed systems like HDFS, Cassandra

### Auto Scaling

Auto Scaling automatically adjusts the number of EC2 instances based on demand.

**Auto Scaling Group (ASG):** Defines min, max, and desired capacity. Works with launch templates. Integrates with Application Load Balancer for automatic health checks and instance replacement.

**Scaling Policies:**
- **Target Tracking** — maintain a metric at a target value (e.g., keep CPU at 50%)
- **Step Scaling** — scale by different amounts based on alarm breach size
- **Scheduled Scaling** — scale at specific times
- **Predictive Scaling** — uses ML to forecast and scale proactively

**Health Checks:** ASG can use EC2 health checks (instance status) or ELB health checks (application-level). Unhealthy instances are terminated and replaced.

### Lambda

Lambda is a serverless compute service. You upload code, Lambda runs it in response to triggers, and you pay only for execution time (milliseconds).

**Key Concepts:**
- Supports runtimes: Python, Node.js, Java, Go, Ruby, .NET, and custom runtimes
- Max execution time: 15 minutes
- Memory: 128 MB to 10 GB (CPU scales proportionally)
- Ephemeral storage: `/tmp` up to 10 GB
- Concurrency: default 1000 concurrent executions per account per region

**Triggers:** S3 events, API Gateway, SQS, SNS, DynamoDB Streams, EventBridge, Cognito, ALB.

**Invocation Models:**
- Synchronous — caller waits for result (API Gateway, ALB)
- Asynchronous — event queued, Lambda retries on failure (S3, SNS)
- Stream-based — Lambda polls the stream (Kinesis, DynamoDB Streams)

**Cold Starts:** Initial invocation takes longer as Lambda provisions a new execution environment. Mitigated by provisioned concurrency, keeping functions warm, or using lighter runtimes.

### ECS and Fargate

ECS (Elastic Container Service) is a container orchestration service. Fargate is a serverless compute engine for containers — you define CPU and memory, AWS manages the underlying infrastructure.

Key concepts: Task Definition (blueprint for a container), Task (running instance of a task definition), Service (maintains a desired number of running tasks), Cluster (logical grouping of tasks or EC2 instances).

---

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

---

## Networking

### VPC (Virtual Private Cloud)

VPC is a logically isolated section of the AWS cloud. You define your own IP address range (CIDR block), subnets, route tables, gateways, and security settings.

**Subnets:** Subdivisions of a VPC in a specific AZ. Public subnets have a route to an Internet Gateway. Private subnets do not.

**Internet Gateway (IGW):** Allows communication between VPC instances and the internet. One per VPC. Stateful — allows return traffic automatically.

**NAT Gateway:** Allows instances in private subnets to initiate outbound connections to the internet without exposing them to inbound traffic. Deployed in a public subnet. Managed by AWS — no maintenance required. NAT Instances are the self-managed alternative.

**Route Tables:** Control where network traffic is directed. Each subnet is associated with one route table. Default routes for VPC traffic are local. Add `0.0.0.0/0 → igw-xxx` for internet access.

**Security Groups:** Virtual firewalls for EC2 instances and other resources. Stateful — return traffic is automatically allowed. Rules are inbound/outbound. Only allow rules (no explicit deny). Reference other security groups by ID.

**Network ACLs (NACLs):** Stateless firewalls at the subnet level. Support both allow and deny rules. Rules evaluated in order by number. Both inbound and outbound rules required for bidirectional traffic.

**VPC Peering:** Connects two VPCs using private IP addresses. Not transitive — if A peers with B and B peers with C, A cannot reach C through B.

**VPC Endpoints:**
- Interface Endpoint — uses PrivateLink, an ENI with a private IP, for services like SSM, Secrets Manager
- Gateway Endpoint — for S3 and DynamoDB only; modifies route table

**AWS Transit Gateway:** Hub-and-spoke model connecting multiple VPCs and on-premises networks. Transitive routing — solve the peering scalability problem.

**Direct Connect:** Dedicated network connection from on-premises to AWS, bypassing the internet. More consistent latency and throughput. Typically used for high-bandwidth, low-latency, or compliance-driven workloads.

**VPN:** Site-to-Site VPN creates an encrypted IPsec tunnel over the internet between on-premises and a VPC Virtual Private Gateway. Faster to set up than Direct Connect but relies on internet.

### Load Balancing

**Application Load Balancer (ALB):** Layer 7 (HTTP/HTTPS). Routes based on host, path, headers, or query strings. Supports WebSockets, HTTP/2. Best for microservices and container-based applications. Integrates with ECS, Lambda, Cognito.

**Network Load Balancer (NLB):** Layer 4 (TCP/UDP). Handles millions of requests per second with ultra-low latency. Supports static IPs and Elastic IPs. Used for gaming, IoT, financial applications.

**Gateway Load Balancer (GWLB):** For deploying, scaling, and managing third-party network virtual appliances (firewalls, intrusion detection). Layer 3.

---

## Databases

### RDS (Relational Database Service)

Managed relational database service supporting MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Aurora. AWS handles patching, backups, and hardware.

**Multi-AZ:** Synchronous standby replica in another AZ. Automatic failover. Used for high availability, not for read scaling.

**Read Replicas:** Asynchronous replication for read scaling. Can be in the same region, cross-region. Can be promoted to standalone instance for disaster recovery.

**Aurora:** AWS-proprietary database compatible with MySQL and PostgreSQL. Up to 5x faster than MySQL RDS. Storage auto-scales up to 128 TB. 6 copies of data across 3 AZs. Aurora Serverless v2 for variable workloads.

**Backup:** Automated backups retained up to 35 days. Manual snapshots retained until deleted. Point-in-time recovery (PITR) available.

### DynamoDB

DynamoDB is a fully managed NoSQL database offering single-digit millisecond latency. No servers to manage. Scales to any workload.

**Data Model:** Tables contain items (rows). Items have attributes (columns). Each item is uniquely identified by a primary key — either a partition key alone, or a composite key (partition key + sort key).

**Capacity Modes:**
- Provisioned — specify read/write capacity units (RCUs/WCUs); use auto-scaling
- On-Demand — pay per request, ideal for unpredictable workloads

**Global Secondary Index (GSI):** Allows querying on non-primary-key attributes. Has its own partition key and optional sort key. Supports eventual consistency.

**DynamoDB Streams:** Capture item-level changes (INSERT, MODIFY, REMOVE) in order. Used to trigger Lambda functions for event-driven architectures.

**DAX (DynamoDB Accelerator):** In-memory cache for DynamoDB. Microsecond read latency. No application code changes required.

### ElastiCache

Managed in-memory caching service supporting Redis and Memcached. Used to reduce database load, session storage, leaderboards, pub/sub messaging.

**Redis** supports data persistence, replication, cluster mode, Lua scripting, sorted sets, and pub/sub. Preferred for complex use cases.

**Memcached** is simpler, supports multi-threading, ideal for simple caching without persistence.

---

## Messaging and Integration

### SQS (Simple Queue Service)

Fully managed message queuing service that decouples application components. Messages are persisted until consumed or expired (up to 14 days). Consumers poll for messages.

**Standard Queue:** At-least-once delivery, best-effort ordering, nearly unlimited throughput.

**FIFO Queue:** Exactly-once processing, strict ordering, up to 3,000 messages per second with batching.

**Dead Letter Queue (DLQ):** Holds messages that failed processing after a specified number of attempts (MaxReceiveCount). Useful for debugging and reprocessing.

**Visibility Timeout:** Period during which a received message is hidden from other consumers. Gives the consumer time to process and delete the message. Default 30 seconds, max 12 hours.

### SNS (Simple Notification Service)

Fully managed pub/sub messaging. Publishers send messages to topics. Topics fan out messages to multiple subscribers simultaneously. Supports SQS, Lambda, HTTP endpoints, email, SMS.

Fan-out pattern: Publish once to SNS → delivers to multiple SQS queues or Lambda functions. Decouples event producers from consumers.

### EventBridge

Serverless event bus that connects AWS services, SaaS applications, and custom applications. Uses event patterns to route events to targets. Supports scheduled rules (cron-based). The backbone for event-driven architecture on AWS.

### Kinesis

**Kinesis Data Streams:** Real-time data streaming for logs, metrics, clickstreams. Data retained up to 7 days (extended). Consumers can replay data. Shard capacity: 1 MB/s write, 2 MB/s read per shard.

**Kinesis Data Firehose:** Fully managed delivery stream to S3, Redshift, OpenSearch, Splunk. Near real-time (buffer based on time or size). No consumers to manage.

---

## Monitoring and Observability

### CloudWatch

CloudWatch is AWS's native monitoring service.

**Metrics:** Time-series data points from AWS services and custom applications. Default EC2 metrics include CPU, disk I/O, network. Detailed monitoring (1-minute intervals) costs extra.

**Logs:** CloudWatch Logs stores, monitors, and analyzes log files. Log Groups contain Log Streams. Log Insights for querying. Metric Filters extract metrics from log patterns.

**Alarms:** Trigger actions (SNS notifications, Auto Scaling, EC2 actions) when metrics cross thresholds. States: OK, ALARM, INSUFFICIENT_DATA.

**Dashboards:** Customizable visualizations of metrics.

### CloudTrail

Records all API calls made to AWS services. Who did what, when, from where. Stores logs in S3. Essential for security auditing, compliance, and incident investigation. Enabled by default for 90 days; create a Trail for longer retention.

### AWS Config

Continuously records configuration changes to AWS resources and evaluates them against desired configurations (Config Rules). Tracks resource relationships. Enables compliance auditing and change management.

---

## Security Services

### AWS KMS (Key Management Service)

Managed service for creating and controlling encryption keys. Integrates with most AWS services. Keys never leave KMS unencrypted. Supports automatic annual key rotation. Customer Managed Keys (CMK) give you full control.

### AWS Secrets Manager

Stores and rotates secrets (database credentials, API keys). Supports automatic rotation using Lambda. Charges per secret per month. Access via SDK or IAM policy.

### AWS WAF (Web Application Firewall)

Protects web applications from common exploits (SQL injection, XSS). Works with ALB, CloudFront, API Gateway. Uses Web ACLs with rules and rule groups. AWS Managed Rules for common threats.

### AWS Shield

DDoS protection. Shield Standard is automatic and free. Shield Advanced provides enhanced detection, protection for EC2, ELB, CloudFront, Route 53, and 24/7 access to the AWS DDoS Response Team (DRT).

### GuardDuty

Intelligent threat detection service. Analyzes CloudTrail logs, VPC Flow Logs, DNS logs using ML. Detects anomalies like unauthorized access, cryptocurrency mining, data exfiltration. No agents required.

---

## Cost Optimization

- Use AWS Cost Explorer and Budgets to track and forecast spending
- Rightsize EC2 instances using Compute Optimizer recommendations
- Purchase Reserved Instances or Savings Plans for predictable workloads
- Use Spot Instances for fault-tolerant batch and stateless workloads
- Enable S3 Intelligent-Tiering for data with unpredictable access patterns
- Delete unattached EBS volumes and unused Elastic IPs
- Use CloudWatch to identify underutilized resources
- Set up billing alerts to catch unexpected cost increases