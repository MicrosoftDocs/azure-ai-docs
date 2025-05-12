---
title: Securely use playground chat
titleSuffix: Azure AI Foundry
description: Learn how to securely use the Azure AI Foundry portal playground chat on your own data. 
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/29/2025
ms.reviewer: meerakurup 
ms.author: larryfr
author: Blackmist
zone_pivot_groups: azure-ai-studio-sdk-cli
# Customer intent: As an administrator, I want to make sure that my data is handled securely when used in the playground chat.
---

# Use your data securely with the Azure AI Foundry portal playground

> [!NOTE]
> The information provided in this article is specific to a **[!INCLUDE [hub](../includes/hub-project-name.md)]**, and doesn't apply for a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

Use this article to learn how to securely use [Azure AI Foundry](https://ai.azure.com)'s playground chat on your data. The following sections provide our recommended configuration to protect your data and resources by using Microsoft Entra ID role-based access control, a managed network, and private endpoints. We recommend disabling public network access for Azure OpenAI resources, Azure AI Search resources, and storage accounts. Using selected networks with IP rules isn't supported because the services' IP addresses are dynamic.

> [!NOTE]
> Azure AI Foundry's managed virtual network settings apply only to Azure AI Foundry's managed compute resources, not platform as a service (PaaS) services like Azure OpenAI or Azure AI Search. When using PaaS services, there's no data exfiltration risk because the services are managed by Microsoft.

The following table summarizes the changes made in this article:

| Configurations | Default | Secure | Notes |
| ----- | ----- | ----- | ----- |
| Data sent between services | Sent over the public network | Sent through a private network | Data is sent encrypted using HTTPS even over the public network. |
| Service authentication | API keys | Microsoft Entra ID | Anyone with the API key can authenticate to the service. Microsoft Entra ID provides more granular and robust authentication. |
| Service permissions | API Keys | Role-based access control | API keys provide full access to the service. Role-based access control provides granular access to the service. |
| Network access | Public | Private | Using a private network prevents entities outside the private network from accessing resources secured by it. |

## Prerequisites

Ensure that the Azure AI Foundry hub is deployed with the __Identity-based access__ setting for the Storage account. This configuration is required for the correct access control and security of your Azure AI Foundry Hub. You can verify this configuration using one of the following methods:

- In the Azure portal, select the hub and then select __Settings__, __Properties__, and __Options__. At the bottom of the page, verify that __Storage account access type__ is set to __Identity-based access__.
- If deploying using Azure Resource Manager or Bicep templates, include the `systemDatastoresAuthMode: 'identity'` property in your deployment template.
- You must be familiar with using Microsoft Entra ID role-based access control to assign roles to resources and users. For more information, visit the [Role-based access control](/azure/role-based-access-control/overview) article.

## Configure Network Isolated Azure AI Foundry Hub

If you're __creating a new Azure AI Foundry hub__, use one of the following documents to create a hub with network isolation:

- [Create a secure Azure AI Foundry hub in Azure portal](create-secure-ai-hub.md)
- [Create a secure Azure AI Foundry hub using the Python SDK or Azure CLI](develop/create-hub-project-sdk.md)

If you have an __existing Azure AI Foundry hub__ that isn't configured to use a managed network, use the following steps to configure it to use one:

1. From the Azure portal, select the hub, then select __Settings__, __Networking__, __Public access__.
1. To disable public network access for the hub, set __Public network access__ to __Disabled__. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/hub-public-access-disable.png" alt-text="Screenshot of Azure AI Foundry hub settings with public access disabled.":::

1. Select __Workspace managed outbound access__ and then select either the __Allow Internet Outbound__ or __Allow Only Approved Outbound__ network isolation mode. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/select-network-isolation-configuration.png" alt-text="Screenshot of the Azure AI Foundry hub settings with allow internet outbound selected.":::

## Configure Azure AI services Resource

Depending on your configuration, you might use an Azure AI services resource that also includes Azure OpenAI or a standalone Azure OpenAI resource. The steps in this section configure an AI services resource. The same steps apply to an Azure OpenAI resource.

1. If you don't have an existing Azure AI services resource for your Azure AI Foundry hub, [create one](/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).
1. From the Azure portal, select the AI services resource, then select __Resource Management, __Identity__, and __System assigned__. 
1. To create a managed identity for the AI services resource, set the __Status__ to __On__. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-managed-identity.png" alt-text="Screenshot of setting the status of managed identity to on.":::

1. To disable public network access, select __Networking__, __Firewalls and virtual networks__, and then set __Allow access from__ to __Disabled__. Under __Exceptions__, make sure that __Allow Azure services on the trusted services list__ is enabled. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-public-access-disable.png" alt-text="Screenshot of AI services with public network access disabled.":::

1. To create a private endpoint for the AI services resource, select __Networking__, __Private endpoint connections__, and then select __+ Private endpoint__. This private endpoint is used to allow clients in your Azure Virtual Network to securely communicate with the AI services resource. For more information on using private endpoints with Azure AI services, visit the [Use private endpoints](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints) article.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-private-endpoint.png" alt-text="Screenshot of the private endpoint section for AI services.":::

    1. From the __Basics__ tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the __Resource__ tab, accept the target subresource of __account__.
    1. From the __Virtual Network__ tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Azure AI Foundry hub has a private endpoint connection to.
    1. From the __DNS__ tab, select the defaults for the DNS settings.
    1. Continue to the __Review + create__ tab, then select __Create__ to create the private endpoint.

1. Currently you can't disable local (shared key) authentication to Azure AI services through the Azure portal. Instead, you can use the following [Azure PowerShell](/powershell/azure/what-is-azure-powershell) cmdlet:

    ```azurepowershell
    Set-AzCognitiveServicesAccount -resourceGroupName "resourceGroupName" -name "AIServicesAccountName" -disableLocalAuth $true
    ```

    For more information, visit the [Disable local authentication in Azure AI services](/azure/ai-services/disable-local-auth) article.

## Configure Azure AI Search

You might want to consider using an Azure AI Search index when you either want to: 
 - Customize the index creation process. 
 - Reuse an index created before by ingesting data from other data sources. 

To use an existing index, it must have at least one searchable field. Ensure at least one valid vector column is mapped when using vector search. 

> [!IMPORTANT]
> The information in this section is only applicable for securing the Azure AI Search resource for use with Azure AI Foundry. If you're using Azure AI Search for other purposes, you might need to configure other settings. For related information on configuring Azure AI Search, visit the following articles:
>
> - [Configure network access and firewall rules](../../search/service-configure-firewall.md)
> - [Enable or disable role-based access control](/azure/search/search-security-enable-roles)
> - [Configure a search service to connect using a managed identity](/azure/search/search-howto-managed-identities-data-sources)

1. If you don't have an existing Azure AI Search resource for your Azure AI Foundry hub, [create one](/azure/search/search-create-service-portal).
1. From the Azure portal, select the AI Search resource, then select __Settings__, __Identity__, and __System assigned__.
1. To create a managed identity for the AI Search resource, set the __Status__ to __On__. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-managed-identity.png" alt-text="Screenshot of AI Search with a system-managed identity configuration.":::

1. To disable public network access, select __Settings__, __Networking__, and __Firewalls and virtual networks__. Set __Public network access__ to __Disabled__. Under __Exceptions__, make sure that __Allow Azure services on the trusted services list__ is enabled. Select __Save__ to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-public-access-disable.png" alt-text="Screenshot of AI Search with public network access disabled.":::

1. To create a private endpoint for the AI Search resource, select __Networking__, __Private endpoint connections__, and then select __+ Create a private endpoint__.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-private-endpoint.png" alt-text="Screenshot of the private endpoint section of AI Search.":::

    1. From the __Basics__ tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the __Resource__ tab, select the __Subscription__ that contains the resource, set the __Resource type__ to __Microsoft.Search/searchServices__, and select the Azure AI Search resource. The only available subresource is __searchService__.
    1. From the __Virtual Network__ tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Azure AI Foundry hub has a private endpoint connection to.
    1. From the __DNS__ tab, select the defaults for the DNS settings.
    1. Continue to the __Review + create__ tab, then select __Create__ to create the private endpoint.

1. To enable API access based on role-based access controls, select __Settings__, __Keys__, and then set __API Access control__ to __Role-based access control__ or __Both__. Select __Yes_ to apply the changes.

    > [!NOTE]
    > Select __Both__ if you have other services that use a key to access the Azure AI Search. Select __Role-based access control__ to disable key-based access.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/search-api-access-control.png" alt-text="Screenshot of AI Search with API access set to both.":::

## Configure Azure Storage (ingestion-only)

If you're using Azure Storage for the ingestion scenario with the Azure AI Foundry portal playground, you need to configure your Azure Storage Account.

1. Create a Storage Account resource 
1. From the Azure portal, select the Storage Account resource, then select __Security + networking__, __Networking__, and __Firewalls and virtual networks__.
1. To disable public network access and allow access from trusted services, set __Public network access__ to __Enabled from selected virtual networks and IP addresses__. Under __Exceptions__, make sure that __Allow Azure services on the trusted services list__ is enabled.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/storage-account-public-access-disable.png" alt-text="Screenshot of storage account network configuration.":::

1. Set __Public network access__ to __Disabled__ and then select __Save__ to apply the changes. The configuration to allow access from trusted services is still enabled.
1. To create a private endpoint for Azure Storage, select __Networking__, __Private endpoint connections__, and then select __+ Private endpoint__.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/storage-private-endpoint.png" alt-text="Screenshot of the private endpoint section for the storage account.":::

    1. From the __Basics__ tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the __Resource__ tab, set the __Target sub-resource__ to __blob__.
    1. From the __Virtual Network__ tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Azure AI Foundry hub has a private endpoint connection to.
    1. From the __DNS__ tab, select the defaults for the DNS settings.
    1. Continue to the __Review + create__ tab, then select __Create__ to create the private endpoint.

1. Repeat the previous step to create a private endpoint, however this time set the __Target sub-resource__ to __file__. The previous private endpoint allows secure communication to blob storage, and this private endpoint allows secure communication to file storage.
1. To disable local (shared key) authentication to storage, select __Configuration__, under __Settings__. Set __Allow storage account key access__ to __Disabled__, and then select __Save__ to apply the changes. For more information, visit the [Prevent authorization with shared key](/azure/storage/common/shared-key-authorization-prevent) article. 

## Configure Azure Key Vault

Azure AI Foundry uses Azure Key Vault to securely store and manage secrets. To allow access to the key vault from trusted services, use the following steps.

> [!NOTE]
> These steps assume that the key vault has already been configured for network isolation when you created your Azure AI Foundry Hub.

1. From the Azure portal, select the Key Vault resource, then select __Settings__, __Networking__, and __Firewalls and virtual networks__.
1. From the __Exception__ section of the page, make sure that __Allow trusted Microsoft services to bypass firewall__ is __enabled__.

## Configure connections to use Microsoft Entra ID

Connections from Azure AI Foundry to Azure AI services and Azure AI Search should use Microsoft Entra ID for secure access. Connections are created from [Azure AI Foundry](https://ai.azure.com) instead of the Azure portal.

> [!IMPORTANT]
> Using Microsoft Entra ID with Azure AI Search is currently a preview feature. For more information on connections, visit the [Add connections](connections-add.md#create-a-new-connection) article.

1. from Azure AI Foundry, select __Connections__. If you have existing connections to the resources, you can select the connection and then select the __pencil icon__ in the __Access details__ section to update the connection. Set the __Authentication__ field to __Microsoft Entra ID__, then select __Update__.
1. To create a new connection, select __+ New connection__, then select the resource type. Browse for the resource or enter the required information, then set __Authentication__ to __Microsoft Entra ID__. Select __Add connection__ to create the connection.

Repeat these steps for each resource that you want to connect to using Microsoft Entra ID.

## Assign roles to resources and users

The services need to authorize each other to access the connected resources. The admin performing the configuration needs to have the __Owner__ role on these resources to add role assignments. The following table lists the required role assignments for each resource. The __Assignee__ column refers to the system-assigned managed identity of the listed resource. The __Resource__ column refers to the resource that the assignee needs to access. For example, the Azure AI Search has a system-assigned managed identity that needs to be assigned the __Storage Blob Data Contributor__ role for the Azure Storage Account.

For more information on assigning roles, see [Tutorial: Grant a user access to resources](/azure/role-based-access-control/quickstart-assign-role-user-portal).

| Resource | Role | Assignee | Description |
|----------|------|----------|-------------|
| Azure AI Search | Search Index Data Contributor | Azure AI services/OpenAI | Read-write access to content in indexes. Import, refresh, or query the documents collection of an index. Only used for ingestion and inference scenarios. |
| Azure AI Search | Search Index Data Reader | Azure AI services/OpenAI | Inference service queries the data from the index. Only used for inference scenarios. |
| Azure AI Search | Search Service Contributor | Azure AI services/OpenAI | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). Inference service queries the index schema for auto fields mapping. Data ingestion service creates index, data sources, skill set, indexer, and queries the indexer status. |
| Azure AI services/OpenAI | Cognitive Services Contributor | Azure AI Search | Allow Search to create, read, and update AI Services resource. |
| Azure AI services/OpenAI | Cognitive Services OpenAI Contributor | Azure AI Search | Allow Search the ability to fine-tune, deploy, and generate text |
| Azure Storage Account | Storage Blob Data Contributor | Azure AI Search | Reads blob and writes knowledge store. |
| Azure Storage Account | Storage Blob Data Contributor | Azure AI services/OpenAI | Reads from the input container, and writes the preprocess result to the output container. |
| Azure Blob Storage private endpoint | Reader | Azure AI Foundry project | For your Azure AI Foundry project with managed network enabled to access Blob storage in a network restricted environment |
| Azure OpenAI Resource for chat model | Cognitive Services OpenAI User | Azure OpenAI resource for embedding model | [Optional] Required only if using two Azure OpenAI resources to communicate. |

> [!NOTE]
> The Cognitive Services OpenAI User role is only required if you're using two Azure OpenAI resources: one for your chat model and one for your embedding model. If this applies, enable Trusted Services AND ensure the Connection for your embedding model Azure OpenAI resource has EntraID enabled.  

### Assign roles to developers

To enable your developers to use these resources to build applications, assign the following roles to your developer's identity in Microsoft Entra ID. For example, assign the __Search Services Contributor__ role to the developer's Microsoft Entra ID for the Azure AI Search resource.

For more information on assigning roles, see [Tutorial: Grant a user access to resources](/azure/role-based-access-control/quickstart-assign-role-user-portal).

| Resource | Role | Assignee | Description |
|----------|------|----------|-------------|
| Azure AI Search | Search Services Contributor | Developer's Microsoft Entra ID | List API-Keys to list indexes from Azure AI Foundry portal. |
| Azure AI Search | Search Index Data Contributor | Developer's Microsoft Entra ID | Required for the indexing scenario. |
| Azure AI services/OpenAI | Cognitive Services OpenAI Contributor | Developer's Microsoft Entra ID | Call public ingestion API from Azure AI Foundry portal. |
| Azure AI services/OpenAI | Cognitive Services Contributor | Developer's Microsoft Entra ID | List API-Keys from Azure AI Foundry portal. |
| Azure AI services/OpenAI | Contributor | Developer's Microsoft Entra ID | Allows for calls to the control plane. |
| Azure Storage Account | Contributor | Developer's Microsoft Entra ID | List Account SAS to upload files from Azure AI Foundry portal. |
| Azure Storage Account | Storage Blob Data Contributor | Developer's Microsoft Entra ID | Needed for developers to read and write to blob storage. |
| Azure Storage Account | Storage File Data Privileged Contributor | Developer's Microsoft Entra ID | Needed to Access File Share in Storage for Promptflow data. |
| The resource group or Azure subscription where the developer need to deploy the web app to | Contributor | Developer's Microsoft Entra ID | Deploy web app to the developer's Azure subscription. |

## Use your data in Azure AI Foundry portal  

Now, the data you add to Azure AI Foundry is secured to the isolated network provided by your Azure AI Foundry hub and project. For an example of using data, visit the [build a question and answer copilot](../tutorials/copilot-sdk-build-rag.md) tutorial.

## Deploy web apps

For information on configuring web app deployments, visit the [Use Azure OpenAI on your data securely](/azure/ai-services/openai/how-to/use-your-data-securely#web-app) article.

## Limitations

When using the Chat playground in Azure AI Foundry portal, don't navigate to another tab within Studio. If you do navigate to another tab, when you return to the Chat tab you must remove your data and then add it back.

## Related content

- [Tutorial: Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md)
- [How to configure a managed network](configure-managed-network.md)
