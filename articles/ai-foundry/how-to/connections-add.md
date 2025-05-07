---
title: How to add a new connection in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to add a new connection in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 02/12/2025
ms.reviewer: larryfr
ms.author: larryfr
author: Blackmist
# Customer Intent: As an admin or developer, I want to understand how to add new connections in Azure AI Foundry portal.
---

# How to add a new connection in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to add a new connection in [Azure AI Foundry portal](https://ai.azure.com).

Connections are a way to authenticate and consume both Microsoft and other resources within your Azure AI Foundry projects. For example, connections can be used for prompt flow, training data, and deployments. [Connections can be created](../how-to/connections-add.md) exclusively for one project or shared with all projects in the same Azure AI Foundry hub. 

## Connection types

Here's a table of some of the available connection types in Azure AI Foundry portal. The __Preview__ column indicates connection types that are currently in preview.

| Service connection type | Preview | Description |
| --- |:---:| --- |
| Azure AI Search | |  Azure AI Search is an Azure resource that supports information retrieval over your vector and textual data stored in search indexes. |
| Azure Blob Storage | | Azure Blob Storage is a cloud storage solution for storing unstructured data like documents, images, videos, and application installers. |
| Azure Data Lake Storage Gen 2 | | Azure Data Lake Storage Gen2 is a set of capabilities dedicated to big data analytics, built on Azure Blob storage. |
| Azure Content Safety | | Azure AI Content Safety is a service that detects potentially unsafe content in text, images, and videos. |
| Azure OpenAI || Azure OpenAI is a service that provides access to OpenAI's models including the GPT-4o, GPT-4o mini, GPT-4, GPT-4 Turbo with Vision, GPT-3.5-Turbo, DALLE-3 and Embeddings model series with the security and enterprise capabilities of Azure. |
| Serverless Model | ✓ | Serverless Model connections allow you to [serverless API deployment](deploy-models-serverless.md). |
| Microsoft OneLake | | Microsoft OneLake provides open access to all of your Fabric items through Azure Data Lake Storage (ADLS) Gen2 APIs and SDKs.<br/><br/>In Azure AI Foundry portal, you can set up a connection to your OneLake data using a OneLake URI. You can find the information that Azure AI Foundry requires to construct a __OneLake Artifact URL__ (workspace and item GUIDs) in the URL on the Fabric portal. For information about the URI syntax, see [Connecting to Microsoft OneLake](/fabric/onelake/onelake-access-api). |
| API key || API Key connections handle authentication to your specified target on an individual basis. For example, you can use this connection with the SerpApi tool in prompt flow.  |
| Custom || Custom connections allow you to securely store and access keys while storing related properties, such as targets and versions. Custom connections are useful when you have many targets that or cases where you wouldn't need a credential to access. LangChain scenarios are a good example where you would use custom service connections. Custom connections don't manage authentication, so you have to manage authentication on your own. |

## Create a new connection

Follow these steps to create a new connection that's only available for the current project.

1. Go to your project in [Azure AI Foundry portal](https://ai.azure.com). If you don't have a project, [create a new project](./create-projects.md).
1. Select __Management center__ from the bottom left navigation.
1. Select __Connected resources__ from the __Project__ section.
1. Select __+ New connection__ from the __Connected resources__ section.

    :::image type="content" source="../media/data-connections/connection-add.png" alt-text="Screenshot of the button to add a new connection." lightbox="../media/data-connections/connection-add.png":::

1. Select the service you want to connect to from the list of available external resources. For example, select __Azure AI Search__.

    :::image type="content" source="../media/data-connections/connection-add-browse-azure-ai-search.png" alt-text="Screenshot of the page to select Azure AI Search from a list of other resources." lightbox="../media/data-connections/connection-add-browse-azure-ai-search.png":::

1. Browse for and select your Azure AI Search service from the list of available services and then select the type of __Authentication__ to use for the resource. Select __Add connection__.

    > [!TIP]
    > Different connection types support different authentication methods. Using Microsoft Entra ID might require specific Azure role-based access permissions for your developers. For more information, visit [Role-based access control](../concepts/rbac-azure-ai-foundry.md#scenario-connections-using-microsoft-entra-id-authentication).

    :::image type="content" source="../media/data-connections/connection-add-azure-ai-search-connect-entra-id.png" alt-text="Screenshot of the page to select the Azure AI Search service that you want to connect to." lightbox="../media/data-connections/connection-add-azure-ai-search-connect-entra-id.png":::

1. After the service is connected, select __Close__ to return to the __Settings__ page.
1. Select __Connected resources__ > __View all__ to view the new connection. You might need to refresh the page to see the new connection.

    :::image type="content" source="../media/data-connections/connections-all.png" alt-text="Screenshot of all connections after you add the Azure AI Search connection." lightbox="../media/data-connections/connections-all.png":::

## Network isolation

If your hub is configured for [network isolation](configure-managed-network.md), you might need to create an outbound private endpoint rule to connect to __Azure Blob Storage__, __Azure Data Lake Storage Gen2__, or __Microsoft OneLake__. A private endpoint rule is needed if one or both of the following are true:

- The managed network for the hub is configured to [allow only approved outbound traffic](configure-managed-network.md#configure-a-managed-virtual-network-to-allow-only-approved-outbound). In this configuration, you must explicitly create outbound rules to allow traffic to other Azure resources.
- The data source is configured to disallow public access. In this configuration, the data source can only be reached through secure methods, such as a private endpoint.

To create an outbound private endpoint rule to the data source, use the following steps:

1. Sign in to the [Azure portal](https://portal.azure.com), and select the Azure AI Foundry hub.
1. Select __Networking__, then __Workspace managed outbound access__.
1. To add an outbound rule, select __Add user-defined outbound rules__. From the __Workspace outbound rules__ sidebar, provide the following information:
    
    - __Rule name__: A name for the rule. The name must be unique for the Azure AI Foundry hub.
    - __Destination type__: Private Endpoint.
    - __Subscription__: The subscription that contains the Azure resource you want to connect to.
    - __Resource type__: `Microsoft.Storage/storageAccounts`. This resource provider is used for Azure Storage, Azure Data Lake Storage Gen2, and Microsoft OneLake.
    - __Resource name__: The name of the Azure resource (storage account).
    - __Sub Resource__: The sub-resource of the Azure resource. Select `blob` in the case of Azure Blob storage. Select `dfs` for Azure Data Lake Storage Gen2 and Microsoft OneLake. 
  
1. Select __Save__ to create the rule.

1. Select __Save__ at the top of the page to save the changes to the managed network configuration.

## Related content

- [Connections in Azure AI Foundry portal](../concepts/connections.md)
- [How to create vector indexes](../how-to/index-add.md)
- [How to configure a managed network](configure-managed-network.md)
