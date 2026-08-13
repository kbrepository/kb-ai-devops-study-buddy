
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