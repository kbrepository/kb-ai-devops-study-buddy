

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