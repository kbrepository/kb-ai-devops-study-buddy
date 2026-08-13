
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
