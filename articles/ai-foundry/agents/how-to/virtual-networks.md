---
title: 'How to use a virtual network with the Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to use your own virtual network with the Foundry Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/11/2026
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.custom: azure-ai-agents, references_regions
monikerRange: 'foundry-classic || foundry'
---

# Create a new network-secured environment with user-managed identity

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Foundry Agent Service offers **Standard Setup with private networking** environment setup, allowing you to bring your own (BYO) private virtual network. This setup creates an isolated network environment that lets you securely access data and perform actions while maintaining full control over your network infrastructure. This guide provides a step-by-step walkthrough of the setup process and outlines all necessary requirements.

> [!TIP]
> See the [FAQ article](../faq.yml#virtual-networking) for common questions when working with Virtual Networks.

> [!NOTE]
> End-to-end network isolation is not supported in the new Foundry portal experience. Please use the classic Foundry portal experience or the SDK or CLI to securely access your Foundry projects when network isolation is enabled. 

## Security features

By default, the Standard Setup with Private Network Isolation ensures:
- **No public egress**: foundational infrastructure ensures the right authentication and security for your agents and tools, without you having to do trusted service bypass.

- **Container injection**: allows the platform network to host APIs and inject a subnet into your network, enabling local communication of your Azure resources within the same virtual network.

- **Private resource access**: If your resources are marked as private and nondiscoverable from the internet, the platform network can still access them, provided the necessary credentials and authorization are in place.

For customers without an existing virtual network, the Standard Setup with Private Networking template simplifies deployment by automatically provisioning the necessary network infrastructures. 

## Architecture diagram

:::image type="content" source="../media/private-network-isolation.png" alt-text="A diagram showing virtual network architecture.":::
### Known limitations

- **Subnet IP address limitation**: both subnets must have IP ranges within valid RFC1918 private IPv4 ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`. Public IP address ranges aren't supported. For more details, see the [Private Network Secured Agent deployment template on GitHub](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup).
- **Agent subnet exclusivity**: The agent subnet cannot be shared by multiple Microsoft Foundry resources. Each Foundry resource must use a dedicated agent subnet.
- **Agent subnet size**: The recommended size of the delegated Agent subnet is /24 (256 addresses) due to the delegation of the subnet to `Microsoft.App/environment`. For more on the subnet sizing, see [Configuring virtual networks for Azure Container Apps](/azure/container-apps/custom-virtual-networks?tabs=workload-profiles-env#subnet).
- **Agent subnet egress firewall allowlisting**: If you are integrating an Azure Firewall with your private network secured standard agent, please allowlist the Fully Qualified Domain Names (FQDNs) listed under __Managed Identity__ in the [Integrate with Azure Firewall](/azure/container-apps/use-azure-firewall#application-rules) article or add the Service Tag __AzureActiveDirectory__.
    - Verify no TLS inspection happens in the Firewall that could be adding a self-signed certificate. During failures, inspect if there is any traffic landing on the Firewall and what traffic is being blocked by the Firewall.
    - Additionally, expect traffic to a `10.x.x.x` private IP (for non-class A scenarios) or `100.x.x.x` private IP (for class A scenario) as necessary traffic to Agent Infra services. Allow this traffic if you are integrating with a Firewall.
- **All Foundry workspace resources must be deployed in the same region as the virtual network (VNet)**. This includes Cosmos DB, Storage Account, AI Search, Foundry Account, Project, Managed Identity, Azure OpenAI, or another Foundry resource used for model deployments. 
- **Region availability**:
  - For supported regions for model deployments, see: [Azure OpenAI model region support](../concepts/model-region-support.md#available-models).
- **Azure Blob Storage**: using Azure Blob Storage files with the File Search tool isn't supported.
- **Private MCP Server**: using private MCP servers deployed in the same virtual network is not supported, only publicly accessible MCP servers are supported.
- **Grounding with Bing Search**: Only the following regions are supported:
  - West Europe
  - Canada East
  - Switzerland North
  - Spain Central
  - UAE North
  - Korea Central
  - Poland Central
  - Southeast Asia
  - West US
  - West US 2
  - West US 3
  - East US
  - East US 2
  - Central US
  - South India
  - Japan East
  - UK South
  - France Central
  - Norway East
  - Australia East
  - Canada Central
  - Sweden Central
  - South Africa North
  - Italy North
  - Brazil South

## Prerequisites
* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope
* The person deploying the template must also have permissions to assign roles to required resources (Cosmos DB, Search, Storage).
    * The built-in role needed is **Role Based Access Administrator**.
    * Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    * The key permission needed is: `Microsoft.Authorization/roleAssignments/write`
* [Python 3.8 or later](https://www.python.org/)
* Once the agent environment is configured, ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI User** [RBAC role](../../concepts\rbac-foundry.md) for the project.
    * The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**  
* Register providers. The following providers must be registered:
    * `Microsoft.KeyVault`
    * `Microsoft.CognitiveServices`
    * `Microsoft.Storage`
    * `Microsoft.MachineLearningServices`
    * `Microsoft.Search`
    * `Microsoft.Network`
    * `Microsoft.App`
    * `Microsoft.ContainerService`
    * To use Bing Search tool: `Microsoft.Bing`

    ```console
       az provider register --namespace 'Microsoft.KeyVault'
       az provider register --namespace 'Microsoft.CognitiveServices'
       az provider register --namespace 'Microsoft.Storage'
       az provider register --namespace 'Microsoft.MachineLearningServices'
       az provider register --namespace 'Microsoft.Search'
       az provider register --namespace 'Microsoft.Network'
       az provider register --namespace 'Microsoft.App'
       az provider register --namespace 'Microsoft.ContainerService'
       # only to use Grounding with Bing Search tool
       az provider register --namespace 'Microsoft.Bing'
    ```

## Configure a new network-secured environment 

> [!NOTE]
> - Programmatic deployment is required to set up a network-secured environment for Agent Service. Deployment through the Azure portal is currently not supported.
> - If you want to delete your Foundry resource and Standard Agent with secured network set-up, delete your Foundry resource and virtual network last. Before deleting the virtual network, ensure to delete and [purge](../../../ai-services/recover-purge-resources.md#purge-a-deleted-resource) your Foundry resource.
> - In the Standard Setup, agents use customer-owned, single-tenant resources. You have full control and visibility over these resources, but you incur costs based on your usage.

You can deploy and customize the Standard Setup with Private Networking using either Bicep or Terraform. The provided samples allow you to bring your own virtual network and customize the deployment to meet your specific requirements:

* Foundry account and Foundry project are created.
* A gpt-4o model is deployed.
* Azure resources for storing customer data: Azure Storage, Azure Cosmos DB, and Azure AI Search are automatically created if existing resources are not provided. 
* These resources are connected to your project to store files, threads, and vector data.
* Microsoft-managed encryption keys for Storage Account and Cognitive Account (Foundry) are used by default.
 
Select one of the available deployment methods:

- **Bicep templates**: follow instructions in [this sample from GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup).

- **Terraform configuration**: follow instructions in [this sample from GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform/15b-private-network-standard-agent-setup-byovnet).

## Deep Dive Standard Setup with Private Networking Template
When you use the Standard Setup with Private Networking Agent Template, the following will automatically be provisioned, unless you bring your own: 

**Network Infrastructure**
* A Virtual Network (192.168.0.0/16) is created 
* Agent Subnet (192.168.0.0/24): Hosts Agent client 
* Private endpoint Subnet (192.168.1.0/24): Hosts private endpoints

**Private DNS Zones** 
The following DNS zones are configured: 
* privatelink.blob.core.windows.net 
* privatelink.cognitiveservices.azure.com 
* privatelink.documents.azure.com 
* privatelink.file.core.windows.net 
* privatelink.openai.azure.com 
* privatelink.search.windows.net 
* privatelink.services.ai.azure.com  

### Virtual network (Vnet) capabilities
Virtual networks enable you to specify which endpoints can make API calls to your resources. The Azure service automatically rejects API calls from devices outside your defined network. You can establish allowed networks using either formula-based definitions or by creating an exhaustive list of permitted endpoints. This security layer can be combined with other security measures for enhanced protection.

> [!NOTE]
> If you bring your existing virtual network and subnet with the *Microsoft.App/environments* delegation, the minimized size of your subnet should be /27 (32 addresses). We recommend a subnet size of /24 (256 addresses), which is the default subnet size set in the network secured template. 

### Network rules

All accounts and their corresponding projects are protected by default with **Public network access Disabled flag**, requiring explicit configuration to allow access through private endpoints.

These rules apply to **all protocols**, including REST and WebSocket. Even internal testing tools like Azure portal's test consoles require explicit permission to access your account and its child resources—ensuring complete security across all agent projects.


### Private endpoints

For Agents, private endpoints ensure secure, internal-only connectivity for the following Azure resources:

- Foundry
- Azure AI Search
- Azure Storage
- Azure Cosmos DB


### DNS zone configurations summary

| Private Link Resource Type | Sub Resource | Private DNS Zone Name | Public DNS Zone Forwarders |
|----------------------------|--------------|------------------------|-----------------------------|
| **Foundry**       | account      | `privatelink.cognitiveservices.azure.com`<br>`privatelink.openai.azure.com`<br>`privatelink.services.ai.azure.com` | `cognitiveservices.azure.com`<br>`openai.azure.com`<br>`services.ai.azure.com` |
| **Azure AI Search**        | searchService| `privatelink.search.windows.net` | `search.windows.net` |
| **Azure Cosmos DB**        | Sql          | `privatelink.documents.azure.com` | `documents.azure.com` |
| **Azure Storage**          | blob         | `privatelink.blob.core.windows.net` | `blob.core.windows.net` |

To create a conditional forwarder in the DNS Server to the Azure DNS Virtual Server, use the list of zones mentioned in the above table. The Azure DNS Virtual Server IP address is 168.63.129.16.

### Access your secured agents

Once your template deployment is complete, you can access your Foundry project behind a virtual network using one of the following methods:
* **Azure VPN Gateway**: Connects on-premises networks to the virtual network over a private connection. Connection is made over the public internet. There are two types of VPN gateways that you might use: 
    * **Point-to-site**: Each client computer uses a VPN client to connect to the virtual network. 
    * **Site-to-site**: A VPN device connects the virtual network to your on-premises network. 
* **ExpressRoute**: Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider.
* **Azure Bastion**: In this scenario, you create an Azure Virtual Machine (sometimes called a jump box) inside the virtual network. You then connect to the VM using Azure Bastion. Bastion allows you to connect to the VM using either an RDP or SSH session from your local web browser. You then use the jump box as your development environment. Since it is inside the virtual network, it can directly access the workspace.


## Summary

**Private Networking for Standard Agent Setup** delivers enterprise-grade isolation and control:
- ✅ All inbound and outbound traffic remains isolation from public internet 
- ✅ Dedicated private endpoints secure all your customer data  
- ✅ Automatic private DNS resolution for seamless internal access 
- ✅ Strict deny-by-default network rules for maximum security 

This setup enables AI agents to operate entirely within a dedicated, isolated virtual network. By leveraging private network isolation (BYO VNet), organizations can enforce custom security policies, ensuring that AI agents operate within their trusted infrastructure.    

Our goal is to accelerate the development and deployment of AI agents without compromising critical security requirements. With our bicep and ARM templates, you can quickly set up your agent environment while still maintaining full control over their networking and data.   

## Troubleshooting guide 

Refer to this guide to resolve errors regarding the standard secured agent template deployment errors or errors post template deployment in the Foundry portal.  

### Template deployment errors 

`"CreateCapabilityHostRequestDto is invalid: Agents CapabilityHost supports a single, non empty value for vectorStoreConnections property."` 

`"Agents CapabilityHost supports a single, non empty value for storageConnections property."`

`"Agents CapabilityHost supports a single, non empty value for threadStorageConnections property."`

**Solution**: Providing all connections to all Bring-your-Own (BYO) resources, requires connections to all BYO resources. You cannot create a secured standard agent in Foundry without all three resources provided. 

`"Provided subnet must be of the proper address space. Please provide a subnet which has address space in the range of 172 or 192."` 

**Solution**: You are not using a proper IP range for your delegated agent subnet. Please verify you are using a valid Private IP address spaces.  

`"Subscripton is not registered with the required resource providers, please register with the resource providers Microsoft.App and Microsoft.ContainerService."` 

**Solution**: You are missing the correct resource registration. Ensure the required resources are registered in your tenant. 

```azurecli
az provider register --namespace 'Microsoft.KeyVault' 
az provider register --namespace 'Microsoft.CognitiveServices' 
az provider register --namespace 'Microsoft.Storage' 
az provider register --namespace 'Microsoft.MachineLearningServices' 
az provider register --namespace 'Microsoft.Search' 
az provider register --namespace 'Microsoft.Network' 
az provider register --namespace 'Microsoft.App' 
az provider register --namespace 'Microsoft.ContainerService' 
```
 

`"Failed to create Aml RP virtual workspace due to System.Exception: Failed async operation."` or `"The resource operation completed with terminal provisioning state 'Failed'. Capability host operation failed."` 

**Solution**: This is a catch all error we provide. Create a support ticket request to investigate your set-up. Check the capability host for the error. 

 

`"Subnet requires any of the following delegation(s) [Microsoft.App/environments] to reference service association link /subscriptions/11111-aaaaa-2222-bbbb-333333333/resourceGroups/agentRANGEChange/providers/Microsoft.Network/virtualNetworks/my-agent-vnet/subnets/agent-subnet/serviceAssociationLinks/legionservicelink."` 

**Solution**: This error appears when you try to delete your secured standard template set-up in Azure and did not correctly delete all resources. One solution is to navigate to your Foundry resource page in the Azure portal and select **Manage deleted resources**. From there, purge the resource that the agent was associated with for this virtual network. The other option is to run the `deleteCaphost.sh` script in the secured standard template. 

 

`"Timeout of 60000ms exceeded" error when loading the Agent pages in the AI Foundry project`

**Solution**: The AI Foundry project has issues communicating with Cosmos DB to create Agents. Verify connectivity to Cosmos DB (Private Endpoint and DNS).
When using a [firewall on the agents subnet](../how-to/virtual-networks.md#known-limitations), make sure it allows access to required Fully Qualified Domain Names (FQDNs).
These FQDNs are listed under **Managed Identity** in the [Integrate with Azure Firewall](/azure/container-apps/use-azure-firewall#application-rules) article. You can also add the Service Tag **AzureActiveDirectory**.

## Next steps

You've now successfully configured a network-secure account and project, use the [quickstart](../quickstart.md) to create your first agent. 
