# Automated-Security-Lab-IaC-Edition
This project represents a significant evolution from manual cloud deployment to Infrastructure as Code (IaC). I have automated the provisioning of a fully functional Cybersecurity Monitoring Lab (Honeypot) in Microsoft Azure using Terraform.
The goal is to provide a repeatable, consistent, and secure environment to observe real-world threat actor behavior, capturing live attacks and geolocating them through a cloud-native SIEM.

<img width="1898" height="958" alt="image" src="https://github.com/user-attachments/assets/c1342aeb-c2f6-47c9-a277-b2fb046b6b0a" />

The Terraform Workflow
To manage the lifecycle of this lab, I follow a professional DevOps workflow in my CachyOS environment:

1. Write: Define infrastructure components in HCL (HashiCorp Configuration Language).
2. Init: Initialize the working directory and download the AzureRM provider.
3. Plan: Generate an execution plan to preview changes before they happen, ensuring security compliance.
4. Apply: Execute the plan to build the Resource Group, VNet, Subnet, and Security Rules in Azure.

Infrastructure Components (Defined as Code)

By using Terraform, the following resources are provisioned automatically:
- Resource Group: A dedicated logical container for the entire lab.
- Virtual Network (VNet) & Subnet: Isolated networking environment for the Honeypot.
- Network Security Group (NSG): Configured with intentional "vulnerabilities" (Open Port 22) to attract brute-force traffic.
- Public IP: Assigned to the Ubuntu VM to make it discoverable by global botnets.

Security & Monitoring Pipeline

Once the infrastructure is up, the monitoring stack takes over:
- Data Ingestion: Log Analytics Workspace centralizes Syslog data streamed via the Azure Monitor Agent (AMA).
- Threat Detection: Microsoft Sentinel (SIEM) analyzes the logs to identify high-severity incidents.
- Visualization: Custom KQL queries map the attacker's physical location based on their source IP.

Manual Deployment vs. Infrastructure as Code (IaC)
This project highlights the efficiency gains of transitioning from manual cloud management to automated provisioning.

<img width="599" height="125" alt="image" src="https://github.com/user-attachments/assets/0b6e5f68-674b-4c22-b33b-e4d7a937cbeb" />

- Key Takeaway: By using Terraform, I eliminated "Configuration Drift" and ensured that my SOC environment is identical every time it's deployed, allowing me to focus on threat analysis rather than infrastructure troubleshooting.


Cost Optimization & Resource Selection
- Instance Selection: Chose the Standard_B1s instance type. Since a Honeypot primarily processes text-based Syslog telemetry, 1 GiB of RAM is sufficient, reducing cloud spend by over 70% compared to D-series instances.
- Storage Strategy: Implemented Standard_LRS (HDD) for the OS disk. This minimizes costs while providing adequate IOPS for log generation during brute-force attacks.
