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

Deployment Success
The infrastructure was successfully provisioned using Terraform in less than 1 minute.
<img width="1920" height="295" alt="image" src="https://github.com/user-attachments/assets/895fe3eb-9f87-419d-a978-fd1d6b02de07" />
- Evidence of Automation: By executing terraform apply, I deployed 8 critical cloud resources simultaneously, ensuring zero configuration drift and maintaining a strict security posture (Honeypot-ready).


"Troubleshooting: Solving the Connectivity Gap":
- "During the initial deployment, I encountered a Connection timed out error. I diagnosed that while the NSG rules were defined, the explicit association between the NSG and the NIC was missing. I resolved this by implementing the azurerm_network_interface_security_group_association resource in Terraform, ensuring the security policy was correctly applied to the instance."
- "Detected a sync issue where the cloud provider's state didn't match the local HCL definition. Resolved by using -replace flags to re-provision the security layer without impacting compute resources."

Final Connectivity Fix

During deployment, a synchronization issue between the Terraform state and the Azure API prevented the NSG rules from being applied correctly.
- Root Cause: Resource drift or partial deployment.
- Solution: Forced a resource recreation using the command terraform apply -replace="azurerm_network_security_group.honeypot_nsg".
- Outcome: Full SSH connectivity established and security rules successfully verified in the Azure Portal.

Real-Time Threat Intelligence Capture".
- "Successfully implemented a Python middleware that monitors SSH auth logs and enriches brute-force attempts with geolocation metadata. First live captures originated from ASN 45090 (Tencent Cloud Computing), demonstrating the immediate exposure of cloud assets to global scanning bots."
<img width="910" height="980" alt="image" src="https://github.com/user-attachments/assets/7288a67c-3222-4073-af65-7617100074b7" />


"An audit of the installed binaries was performed using dpkg -L, confirming the presence of the core components: mdsd (Ingestion), telegraf (Metrics), and fluent-bit (Log Processing). Despite the absence of the ama_status.py diagnostic script, the agent's functionality was validated at the systemctl service level, allowing the ingestion of custom telemetry into Sentinel."

"Corruption was identified in the prerm script of the azuremonitoragent package. Resolution required manually editing the dpkg package management system's execution flow to force a purge of binaries and allow a clean reinstallation of the monitoring agent."

ataques de las comandos : tail -f /var/log/honeypot/attacks.log
<img width="1914" height="992" alt="image" src="https://github.com/user-attachments/assets/cecc7d13-6e7b-418a-82c4-13a6e15f8eda" />

Honeypot Live Attack Map
<img width="1507" height="652" alt="image" src="https://github.com/user-attachments/assets/9dcdda94-33d2-4d8a-b0a6-471b5f4f311b" />


