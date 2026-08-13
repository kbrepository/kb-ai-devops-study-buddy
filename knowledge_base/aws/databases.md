
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