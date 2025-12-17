---
title: Configure managed virtual network for Microsoft Foundry projects (preview)
ms.service: azure-ai-foundry
ms.date: 12/17/2025
ms.reviewer: meerakurup
ms.author: jburchel
author: jonburchel
description: Secure your Microsoft Foundry projects with managed virtual networks. Learn to enable outbound isolation and private endpoints for enhanced data protection.
ms.topic: how-to
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Configure managed virtual network for Microsoft Foundry projects

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article explains how to set-up a managed virtual network for your Foundry resource. Managed virtual network streamlines and automates network isolation for your Foundry resource by provisioning a Microsoft‑managed virtual network that secures the Agents service underlying compute within your Foundry projects. When enabled, Agents outbound network traffic is secured with this managed network boundary, and all the traffic is governed by the isolation mode you choose. You can create the required private endpoints to dependent Azure services and applies the necessary network rules, giving you a secure default without requiring you to build or maintain your own virtual network. This managed network restricts what your Agents can access, helping prevent data exfiltration while still allowing connectivity to approved Azure resources. 

Before continuing, please consider the [limitations](#limitations) of the offering and review the pre-requisites. This feature is currently in Public Preview so please consider preview conditions before enabling this network isolation method. If you are not allowed to use preview features in your enterprise, please use the existing GA supported [custom virtual network support for Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/virtual-networks?view=foundry-classic) in Foundry. 

## Understand isolation modes

When you enable managed virtual network isolation, a managed virtual network is created for the Foundry account. Any new Agent built in your projects will automatically use the managed virtual network for outbound traffic. The managed virtual network can use private endpoints for Azure resources that are used by your Agents, such as Azure Storage, Azure CosmosDB, and Azure AI Search. 

:::image type="content" source="media/managed-virtual-network/diagram-managed-network.png" alt-text="Diagram of managed virtual network configuration." lightbox="media/managed-virtual-network/diagram-managed-network.png":::

There are two different configuration modes for outbound traffic from the managed virtual network:

| Outbound mode | Description | Scenarios |
| --- | --- | --- |
| Allow internet outbound | Allows all outbound traffic to the internet. | Unrestricted outbound access is acceptable; broad connectivity required. |
| Allow only approved outbound | Restricts outbound using service tags, private endpoints, and optional FQDN rules (ports 80, 443) enforced via Azure Firewall. | Minimize data exfiltration risk; require curated list of destinations. |
| Disabled | Managed virtual network isolation not enabled, unless custom virtual network is used. | Need public outbound or plan to supply your own virtual network. |

Here is the architecture diagram for a managed network in allow internet outbound mode. 

:::image type="content" source="media/managed-virtual-network/diagram-aio-managed-network.png" alt-text="Diagram of managed virtual network configuration in allow internet outbound mode." lightbox="media/managed-virtual-network/diagram-aio-managed-network.png":::

Here is the architecture diagram for a managed network in allow only approved outbound mode. 

:::image type="content" source="media/managed-virtual-network/diagram-aoao-managed-network.png" alt-text="Diagram of managed virtual network configuration in allow only approved outbound mode." lightbox="media/managed-virtual-network/diagram-aoao-managed-network.png":::

Once a managed virtual network Foundry is configured to allow internet outbound, the resource cannot be reconfigured to disabled. Similarly, once a managed virtual network resource is configured to allow only approved outbound, the workspace cannot be reconfigured to allow internet outbound.

## Prerequisites

Before following the steps in this article, make sure you have the following prerequisites:

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.
* Azure CLI installed. Required to create outbound rules from the managed network. 
* The `Microsoft.Network`, `Microsoft.KeyVault`, `Microsoft.CognitiveServices`, `Microsoft.Storage`, `Microsoft.Search`, and `Microsoft.ContainerService` resource providers must be registered for your Azure subscription. 
* Preview feature registration for the flag `AI.ManagedVnetPreview` in the Azure Portal or through Azure CLI. It will take a few hours to approve your subscription.
* Permissions to deploy a managed network resource. Azure AI Accoutn Owner on account scope is needed to create a Foundry account and project. Owner or Role Based Access Administrator is needed to assign RBAC to the required resources. Azure AI User on project scope is required to create and edit Agents. 
* Sufficient quota for all resources in your target Azure region. If no parameters are passed in, this template creates a Foundry resource, Foundry project, Azure Cosmos DB for NoSQL, Azure AI Search, and Azure Storage account. 

## Limitations

Consider the following limitations before enabling managed network isolation for your Foundry resource. 

1. A managed network Foundry resource is only deployable via the Bicep template in the folder [18-managed-virtual-network-preview in foundry-samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network-preview).
1. If you create FQDN outbound rules when the managed virtual network is in Allow Only Approved Outbound mode, a managed Azure Firewall is created which comes with associated Firewall costs. For more on pricing see [Pricing](#pricing). The FQDN outbound rules only support ports 80 and 443. 
1. Managed virtual network isolation cannot be disabled after enabling. There is no upgrade path from custom virtual network set-up to managed virtual network. A Foundry resource redeployment is required. Deleting your Foundry resource deletes the managed virtual network.
1. Outbound rules from the managed network must be created through Azure CLI. For the end-to-end secured Agent service set-up with a managed virtual network, the template creates the managed private endpoint to the associated Storage account. Private endpoints are not created to CosmosDB or AI Search. Please use instructions in the [outbound rules CLI](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network-preview/update-outbound-rules-cli/outbound-rule-cli.md) file for information on how to create the managed private endpoints.
1. Support for managed virtual network is only in the following regions: **East US, East US2, Japan East, France Central, UAE North, Brazil South, Spain Central, Germany West Central, Italy North, South Central US, West Central US, Australia East, Sweden Central, Canada East, South Africa North, West Europe, West US, West US 3, South India, and UK South.**
1. If you require private access to on-premises resources for your Foundry resource, please use the to [Application Gatway](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/access-on-premises-resources?view=foundry-classic&viewFallbackFrom=foundry) to configure on-premises access. The same set-up with a private endpoint to Application Gateway and setting up backend pools is supported. Both L4 and L7 traffic are now supported with the Application Gateway in GA.
1. Supports only Standard BYO resources Agents v1 and the Foundry classic experience. Basic Agents do not require network isolation. Support in the new Agents v2 and the new Foundry UI is coming soon. 
1. End-to-end network isolation for Agent MCP tools with managed virtual network is currently not supported. Please use public MCP tools with managed network isolation Foundry. 


## Deploy managed virtual network isolation mode

Now to get started deploying a mangaed virutal network Foundry resource, follow the steps below. Further details are provided in the README.md file of the repository. 

1. Clone or download the `foundry-samples` repository containing [`18-managed-virtual-network-preview`](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network-preview).
1. Open the `managed-network.bicep` template in the folder `modules-network-secured`.
1. Set the isolation mode parameter `IsolationMode` depending on your selected isolation mode: `AllowInternetOutbound` or `AllowOnlyApprovedOutbound`
1. In the README.md file, select the "Deploy to Azure" button. This will open up the template in the Azure Portal for a quick deploy.
1. Complete all of your parameters before deploying such as region, resource group, virtual network name, and others. If you are bringing your own CosmosDB< Storage, or Search, ensure the resourceIDs are included as well.
1. Finally, deploy the template. Template deployment should take roughly 30 minutes. 

For more details on the parameters required for managed virtual network deployment, see [Microsoft.MachineLearningServices/workspaces/managedNetwork](https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces/managednetworks?pivots=deployment-language-bicep).

## Manage outbound rules

To update outbound rules from your managed virtual network after deployment, use the Azure CLI `az rest` command. Follow the instructions listed in the `outbound-rules-cli.md` file of the foundry-samples repository. 

For more details on the parameters required for managed virtual network outbound rules, see [Microsoft.MachineLearningServices/workspaces/managedNetwork/outboundRules](https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces/managednetworks/outboundrules?pivots=deployment-language-bicep).

## Select Azure Firewall version

For the managed virtual network, an Azure Firewall is provisioned automatically when you add an outbound FQDN rule in **Allow only approved outbound** mode.

The default SKU is Standard for the Firewall. You can select the Basic SKU instead for reduced cost if advanced features aren't required. For more on pricing, see [Pricing](#pricing). Once a firewall SKU is selected at deployment, it cannot be changed after deployment. Because this is a managed firewall, the Firewall is not in your tenant or in your control. The only setting you can control is the Firewall SKU. 

To select your SKU in the template, go to the `managed-network.bicep`, set the parameter `firewallSku` to either `Standard` or `Basic`.

## Review required service tags

Foundry requires a set of service tags for private networking. These ServiceTags are added by default when the mangaed network is created. You do not need ot create an outbound rule for this ServiceTag. 

* **AzureActiveDirectory.** Required for outbound authentication using Microsoft Entra ID. 

## Private endpoints

When you enable a managed virtual network, you can create managed private endpoints so Agents can securely reach required Azure resources without using the public internet. These private endpoints provide an isolated, private IP–based connection from the managed network to services such as Storage, AI Search, and other dependencies used in your Foundry projects. 

Below are the following resources you can create private endpoints to from the managed network. Private endpoints must be created through CLI. 

- Azure Application Gateway
    - To connect to your on-premises resources with L4 or L7 traffic
- Azure API Management
    - Supports only the Classic tier without VNet injection and the Standard V2 tier with virtual network integration. 
- Azure AI Search
- Azure Container Registry
- Azure CosmosDB 
- Azure Data Factory
- Azure Database for MariaDB
- Azure Database for MySQL
- Azure Database for PostgreSQL Single Server
- Azure Database for PostgreSQL Flexible Server
- Azure Databricks
- Azure Event Hubs
- Azure Key Vault
- Azure Machine Learning
- Azure Cache for Redis
- Azure SQL Server
- Azure Storage 
- Application Insights
    - Via Private Link scope
- Microsoft Foundry

When a managed private endpoint is created from the Foundry managed virtual network to a customer‑owned target resource, the **Foundry resource’s managed identity** must have the correct permissions on that target resource to create and approve private endpoint connections. This ensures that Foundry is explicitly authorized to establish a secure, private link to the resource.

To simplify this requirement, you can assign the `Azure AI Enterprise Network Connection Approver` role to the Foundry account’s managed identity. This role includes the necessary permissions for most commonly used Azure services and typically provides sufficient access for Foundry to create and approve private endpoints on your behalf. Once the connection is approved, the private endpoint is fully managed by Foundry and requires no additional customer configuration. 

## Apply scenario-specific outbound rules

### Agent service outbound rules

The required outbound rules for Standard BYO Resource Agent deployment include private endpoints to the following resources:
* Your CosmosDB resource
* Your Storage account
* Your AI Search resource

Ensure private endpoints are created from the managed virtual network to these resources.

## Pricing

The Foundry managed virtual network feature is free. However, you're charged for the following resources that are used by the managed virtual network:

* Azure Private Link - Private endpoints used to secure communications between the managed virtual network and Azure resources relies on Azure Private Link. For more information on pricing, see Azure Private Link pricing.

* FQDN outbound rules - FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. A standard version of Azure Firewall is used by default. Basic version can be selected. The firewall is not created until you add an outbound FQDN rule. 

For more on Azure pricing, see [Private Link Pricing](https://azure.microsoft.com/pricing/details/private-link) and [Azure Firewall Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-firewall/).


## Compare managed and custom (BYO) network

| Aspect | Managed network | Custom (BYO) network |
| --- | --- | --- |
| Benefits | Microsoft handles subnet range, IP selection, delegation. | Full control: bring custom firewall, set user-defined routes, network peering, delegate subnet. |
| Limitations | Cannot bring your own firewall for allow only approved outbound. Requires Application Gateway for secure on-premises (L7 and L4 traffic support by Application Gateway). No logging of outbound traffic support (coming soon). Does not support Evaluations compute security (coming soon). | More complex setup such as subnet delegation to Azure Container Apps. Requires correct CapHost creation.Requires private Class A, B, and C, not public. Requires minimum /27 subnet for Agent delegation. |

## Clean up resources

To clean up your managed virtual network Foundry resource, delete the Foundry resource. This action deletes the managed virtual network as well.

## Troubleshooting

1. Failure creating CapHost
   - Delete the faulty CapHost resource and redeploy the template.
1. FQDN rule not enforced
   - Confirm the firewall SKU is provisioned and verify ports are limited to 80 or 443.
1. Private endpoint conflicts
   - Remove any service endpoint configuration and use private endpoint only.
1. With UseMicrosoftManagedNetwork=true, Subscription should be registered with Microsoft.CognitiveServices/AI.ManagedVnetPreview!!!
   - Ensure your subscription is allowlisted for the managed virtual network preview feature. Complete this action in the Azure portal and wait for your subscription to be registered.  

