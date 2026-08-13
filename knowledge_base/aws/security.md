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