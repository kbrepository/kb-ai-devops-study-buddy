
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