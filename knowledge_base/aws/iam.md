## Identity and Access Management (IAM)

### EC2 Access to S3

EC2 instances should access S3 using IAM roles instead of long-lived access keys. Attach an instance profile to the EC2 instance with the minimum required S3 permissions. This follows the principle of least privilege.

For private connectivity, use an S3 Gateway VPC Endpoint so traffic between EC2 and S3 does not need to go through the public internet.

Bucket policies can be used to restrict access to specific IAM roles, VPC endpoints, accounts, or conditions.
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
