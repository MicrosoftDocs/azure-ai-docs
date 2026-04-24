---
title: include file
description: include file
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include, classic-and-new
---

Foundry Agent Service offers a **Standard Setup with private networking** environment. This setup creates an isolated network environment that enables secure access to data while maintaining full control over your network infrastructure.

By default, the Standard Setup with private networking ensures:

- **No public egress**: Foundational infrastructure provides the right authentication and security for your agents and tools, without requiring trusted service bypass.
- **Subnet integration**: You provide a delegated subnet from your virtual network. The platform connects agent compute to this subnet, enabling local communication with your Azure resources within the same virtual network.
- **Private resource access**: If your resources are marked as private and nondiscoverable from the internet, the platform network can still access them when the necessary credentials and authorization are in place.

If you don't have an existing virtual network, the Standard Setup with private networking flow can provision the necessary network infrastructure for you.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope.
- The user creating this setup must also have permissions to assign roles to required resources (Azure Cosmos DB, Azure AI Search, Azure Storage).
    - The built-in role needed is **Role Based Access Administrator**.
    - Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    - The key permission needed is: `Microsoft.Authorization/roleAssignments/write`
- [Python 3.9 or later](https://www.python.org/)
- Once the agent environment is configured, ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI User** [RBAC role](../../concepts/rbac-foundry.md) for the project.
    - The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**
- Register providers. The following providers must be registered:
    - `Microsoft.KeyVault`
    - `Microsoft.CognitiveServices`
    - `Microsoft.Storage`
    - `Microsoft.MachineLearningServices`
    - `Microsoft.Search`
    - `Microsoft.Network`
    - `Microsoft.App`
    - `Microsoft.ContainerService`
    - To use Bing Search tool: `Microsoft.Bing`

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

## Configure a network-secured environment

You can create this setup in the Azure portal or deploy it by using Bicep or Terraform.

At a high level, the deployment involves these steps:

1. Choose the target Azure region for your Foundry resources.
1. Decide whether to bring your own VNet and subnet, or use auto-provisioned networking.
1. If you bring your own VNet, gather your VNet and subnet resource IDs.
1. Create the setup in the Azure portal, or deploy it by using Bicep or Terraform.
1. Verify the deployment (see [Verify the deployment](#verify-the-deployment)).

The setup provisions the following resources (unless you bring your own):

- A Foundry account and Foundry project.
- A gpt-4o model deployment.
- Azure Storage, Azure Cosmos DB, and Azure AI Search for storing files, threads, and vector data.
- These resources are connected to your project.
- Microsoft-managed encryption keys for Storage Account and Cognitive Account (Foundry) are used by default.

Select your preferred deployment method by using the following tabs:

# [Azure portal](#tab/portal)

1. From the [Azure portal](https://portal.azure.com), search for **Foundry** and select **Create a resource**.
1. After configuring the **Basics** tab, select the **Storage** tab and then select **Select resources** under **Agent service**.
    - Select or create a Storage account, Azure AI Search resource, and Azure Cosmos DB resource. If you're using virtual network injection, you must bring your own Storage, Azure AI Search, and Azure Cosmos DB resources to create a Standard Agent with end-to-end virtual network isolation.
1. After configuring the **Storage** tab, select the **Network** tab and then select the **Disabled** option for public access. 
1. In the **Private endpoint** section, select **+ Add private endpoint**.
1. When you go through the forms to create a private endpoint, be sure to:
    - From **Basics**, select the same **Region** as your virtual network.
    - From the **Virtual Network** form, select the virtual network and subnet that you want to connect to.
    > [!NOTE]
    > In the portal UI, the target to which you create the private endpoint should be labeled as an "account". Select your Foundry resource when prompted.
1. After setting your inbound private endpoint, a new dropdown appears for setting **Virtual network injection**. Select your **virtual network** in the first dropdown, then select your **subnet** that is delegated to **Microsoft.App/environments** with a subnet size of /27 or larger. This delegation and subnet size are required for the injection.
1. Continue through the forms to create the project. When you reach the **Review + create** tab, review your settings and select **Create** to create the project.
1. Continue with the checks in [Verify the deployment](#verify-the-deployment).

> [!NOTE]
> Private endpoints to Azure AI Search, Azure Storage, and Azure Cosmos DB are NOT auto-created when you deploy your Foundry resource. Please ensure to create private endpoints to these resources separately in their resource pages in the Azure portal.


# [Templates](#tab/templates)

Use one of the following infrastructure-as-code samples:

- **Bicep templates**: Follow instructions in [this sample from GitHub](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup).
- **Terraform configuration**: Follow instructions in [this sample from GitHub](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform/15b-private-network-standard-agent-setup-byovnet).

After deployment finishes, continue with the checks in [Verify the deployment](#verify-the-deployment).

---

## Verify the deployment

After deployment finishes, verify that all resources are configured correctly:

1. **Confirm subnet delegation**: In the Azure portal, navigate to your VNet > **Subnets** and verify the agent subnet shows delegation to `Microsoft.App/environments`.
1. **Check public network access**: Open each resource (Foundry, Azure AI Search, Azure Storage, Azure Cosmos DB) and confirm **Public network access** is set to **Disabled**.
1. **Validate private endpoint DNS resolution**: From a machine connected to the VNet, run `nslookup` against each endpoint listed in the [DNS zone configurations summary](#dns-zone-configurations-summary). Verify that each name resolves to a private IP address (10.x, 172.16-31.x, or 192.168.x).
1. **Test agent connectivity**: Access your Foundry project from within the VNet (see [Access your secured agents](#access-your-secured-agents)) and confirm you can create and run an agent.

## Limitations 

- **Subnet IP address limitation**: Both subnets must have IP ranges within valid RFC1918 private IPv4 ranges: `10.0.0.0/8`, `172.16-31.0.0/12`, or `192.168.0.0/16`. Public IP and CGNAT address ranges are not supported. 
- **Agent subnet exclusivity**: The agent subnet can't be shared by multiple Foundry resources. Each Foundry resource must use a dedicated agent subnet.
- **Agent subnet size**: The recommended size of the delegated Agent subnet is /24 (256 addresses) due to the delegation of the subnet to `Microsoft.App/environments`. For more on subnet sizing, see [Configuring virtual networks for Azure Container Apps](/azure/container-apps/custom-virtual-networks?tabs=workload-profiles-env#subnet).
- **Agent subnet egress firewall allowlisting**: If you're integrating an Azure Firewall with your private network secured standard agent, allow list the Fully Qualified Domain Names (FQDNs) listed under **Managed Identity** in the [Integrate with Azure Firewall](/azure/container-apps/use-azure-firewall#application-rules) article or add the Service Tag **AzureActiveDirectory**.
    - Verify that no TLS inspection happens in the Firewall that could add a self-signed certificate. During failures, inspect whether there's any traffic landing on the Firewall and what traffic is being blocked.
- **The Foundry resource must be deployed in the same region as the virtual network (VNet)**. Other Azure resources, such as Azure Cosmos DB, Azure AI Search, and Azure Storage, can be deployed in different regions. Consider the cost implications of cross-region deployments.
- **Region availability**:
  - For supported regions for model deployments, see: [Azure OpenAI model region support](../../foundry-models/concepts/models-sold-directly-by-azure.md).
- **Azure Blob Storage**: Using Azure Blob Storage files with the File Search tool isn't supported.
- **Grounding with Bing Search**: Only the following regions are supported: West Europe, Canada East, Switzerland North, Spain Central, UAE North, Korea Central, Poland Central, Southeast Asia, West US, West US 2, West US 3, East US, East US 2, Central US, South India, Japan East, UK South, France Central, Norway East, Australia East, Canada Central, Sweden Central, South Africa North, Italy North, Brazil South
- **Delete network injection**: If you want to delete your Foundry resource and Standard Agent with secured network setup, delete your Foundry resource and virtual network last. Before deleting the virtual network, delete and [purge](../../../ai-services/recover-purge-resources.md#purge-a-deleted-resource) your Foundry resource.
- **Hosted agent virtual network injection**: For hosted agents, the virtual network configuration (network injection) must be included when you first create the Foundry account. Adding network injection to an existing Foundry account after creation isn't supported for hosted agents. 
- **Hosted agent container registry behind a private network**: For hosted agents, the Azure Container Registry (ACR) that stores the agent's container image can't currently be placed behind a private network (private endpoint with public network access disabled). The ACR must be reachable over its public endpoint for the platform to pull the image.


## Architecture diagram

:::image type="content" source="../media/private-network-isolation.png" alt-text="Diagram showing the virtual network architecture for Foundry Agent Service private networking, including the agent subnet, private endpoint subnet, and private DNS zones.":::

## Review the provisioned networking resources

The following resources are automatically provisioned when you use Standard Setup with private networking, unless you bring your own:

**Network infrastructure**

- A virtual network (192.168.0.0/16)
- Agent Subnet (192.168.0.0/24): Hosts Agent client
- Private endpoint Subnet (192.168.1.0/24): Hosts private endpoints

### Virtual network capabilities

Your virtual network controls which endpoints can make API calls to your resources. The Azure service automatically rejects API calls from devices outside your defined network.

### Network rules

All accounts and their corresponding projects are protected by default with the **Public network access Disabled** flag, requiring explicit configuration to allow access through private endpoints. These rules apply to all protocols, including REST and WebSocket.

### DNS zone configurations summary

| Private Link Resource Type | Sub Resource | Private DNS Zone Name | Public DNS Zone Forwarders |
|----------------------------|--------------|------------------------|-----------------------------|
| **Foundry**       | account      | `privatelink.cognitiveservices.azure.com`<br>`privatelink.openai.azure.com`<br>`privatelink.services.ai.azure.com` | `cognitiveservices.azure.com`<br>`openai.azure.com`<br>`services.ai.azure.com` |
| **Azure AI Search**        | searchService| `privatelink.search.windows.net` | `search.windows.net` |
| **Azure Cosmos DB**        | Sql          | `privatelink.documents.azure.com` | `documents.azure.com` |
| **Azure Storage**          | blob         | `privatelink.blob.core.windows.net` | `blob.core.windows.net` |

To create a conditional forwarder in the DNS Server to the Azure DNS Virtual Server, use the list of zones mentioned in the above table. The Azure DNS Virtual Server IP address is 168.63.129.16.

### Access your secured agents

Once deployment is complete, you can access your Foundry project behind a virtual network using one of the following methods:
- **Azure VPN Gateway**: Connects on-premises networks to the virtual network over a private connection. Connection is made over the public internet. There are two types of VPN gateways that you might use:
    - **Point-to-site**: Each client computer uses a VPN client to connect to the virtual network.
    - **Site-to-site**: A VPN device connects the virtual network to your on-premises network.
- **ExpressRoute**: Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider.
- **Azure Bastion**: In this scenario, you create an Azure Virtual Machine (sometimes called a jump box) inside the virtual network. You then connect to the VM using Azure Bastion. Bastion allows you to connect to the VM using either an RDP or SSH session from your local web browser. You then use the jump box as your development environment. Since it's inside the virtual network, it can directly access the workspace.

## FAQ

### What address range should I use for the overall virtual network?

The virtual network address range can be any private IP range that leaves enough address space for both the delegated agent subnet and the private endpoint subnet.

### Can I use peered virtual networks or place resources in different virtual networks?

Peered virtual networks are supported, but data transfer costs can increase.

### Can multiple Foundry resources reuse the same virtual network and subnet?

Yes, the same VNET, but not the same subnet. Multiple Foundry resources can reuse the same virtual network. However, each Foundry resource requires its own dedicated agent runtime subnet. The agent subnet can't be shared across multiple Foundry resources.

### Does the virtual network need to be in the same resource group as the Foundry resource?

No. The virtual network and Foundry resource don't need to be in the same resource group, but they must be in the same region.

## Troubleshooting guide

Refer to this guide to resolve errors during or after a Standard Agent deployment, whether you used the Azure portal, Bicep, or Terraform.

### Deployment errors 

`"CreateCapabilityHostRequestDto is invalid: Agents CapabilityHost supports a single, non empty value for vectorStoreConnections property."` 

`"Agents CapabilityHost supports a single, non empty value for storageConnections property."`

`"Agents CapabilityHost supports a single, non empty value for threadStorageConnections property."`

**Solution**: Providing all connections to all Bring-your-Own (BYO) resources, requires connections to all BYO resources. You can't create a secured standard agent in Foundry without all three resources provided.

`"Provided subnet must be of the proper address space. Please provide a subnet which has address space in the range of 172 or 192."` 

**Solution**: You aren't using a proper IP range for your delegated agent subnet. Verify that you're using a valid private IP address space. Valid RFC1918 ranges include `10.0.0.0/8`, `172.16-31.0.0/12`, and `192.168.0.0/16`. The error message text might not list all valid ranges.

`"Subscripton is not registered with the required resource providers, please register with the resource providers Microsoft.App and Microsoft.ContainerService."` 

**Solution**: You're missing the correct resource registration. Ensure the required resources are registered in your tenant.

`"Failed to create Aml RP virtual workspace due to System.Exception: Failed async operation."` or `"The resource operation completed with terminal provisioning state 'Failed'. Capability host operation failed."` 

**Solution**: This is a catch-all error. Create a support ticket request to investigate your setup. Check the capability host for the error.

`"Subnet requires any of the following delegation(s) [Microsoft.App/environments] to reference service association link /subscriptions/11111-aaaaa-2222-bbbb-333333333/resourceGroups/agentRANGEChange/providers/Microsoft.Network/virtualNetworks/my-agent-vnet/subnets/agent-subnet/serviceAssociationLinks/legionservicelink."` 

**Solution**: This error appears when you try to delete your secured standard template setup in Azure and didn't correctly delete all resources. One solution is to navigate to your Foundry resource page in the Azure portal and select **Manage deleted resources**. From there, purge the resource that the agent was associated with for this virtual network. The other option is to run the `deleteCaphost.sh` script in the secured standard template.

`"Timeout of 60000ms exceeded" error when loading the Agent pages in the Foundry project`

**Solution**: The Foundry project has issues communicating with Azure Cosmos DB to create Agents. Verify connectivity to Azure Cosmos DB (Private Endpoint and DNS).

### Private endpoint DNS resolution fails

**Solution**: If resources aren't reachable through private endpoints, verify that each private DNS zone is linked to your virtual network. Confirm conditional forwarders point to the Azure DNS virtual server IP address `168.63.129.16`. From a machine connected to the VNet, run `nslookup <resource-fqdn>` and verify that each name resolves to a private IP address.

## Next steps

You've now successfully configured a network-secure account and project. Use the [quickstart](../quickstarts/quickstart-hosted-agent.md) to create your first agent.

For more on network isolation configuration and options, see [Configure network isolation](/azure/foundry/how-to/configure-private-link).
