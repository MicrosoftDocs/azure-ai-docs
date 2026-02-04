---
title: Add a new connection to your project
titleSuffix: Microsoft Foundry
description: Learn how to add a new connection to your Foundry project.
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 11/06/2025
ms.reviewer: meerakurup
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# Customer Intent: As an admin or developer, I want to understand how to add new connections in my project.

---

# Add a new connection to your project

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"
> [!TIP]
> An alternate hub-scoped connections article is available: [Create and manage connections (Hubs)](hub-connections-add.md).
::: moniker-end

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to add a new connection in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

Connections are a way to authenticate and consume both Microsoft and other resources within your Foundry projects. They're required for scenarios such as building Standard Agents or building with Agent knowledge tools. Certain connections can be created in the Foundry UI while others require deployment through code in Bicep template. See our [foundry-samples on GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/01-connections). Read the table descriptions below to learn more. 

## Prerequisites

* If you don't have one, [create a project](./create-projects.md).

## Connection types

::: moniker range="foundry"

| Service connection type       | Preview | Description                                                                                                                                                                                                                     |
|-------------------------------|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Azure AI Search               |         | Azure AI Search is an Azure resource that supports information retrieval over your vector and textual data stored in search indexes. Required for Standard Agent deployment.                                                  |
| Azure Storage                 |         | Azure Storage is a cloud storage solution for storing unstructured data like documents, images, videos, and application installers. Required for Standard Agent deployment.                                                   |
| Azure Cosmos DB               | ✅       | Azure Cosmos DB is a globally distributed, multi-model database service that offers low latency, high availability, and scalability across multiple geographical regions. Required for Standard Agent deployment. Connection creation only supported through code.              |
| Azure OpenAI                  |     | Azure OpenAI is a service that provides access to OpenAI's models including the GPT-5, GPT-4o, DALLE-3, and Embeddings model series with the security and enterprise capabilities of Azure. |
| Application Insights          |     | Azure Application Insights is a service that enables developers to automatically detect performance anomalies, diagnose issues, and gain deep insights into application usage and behavior. |
| Azure Key Vault|  | Azure service for securely storing and accessing secrets. (See limitations below) |
| Foundry |       | Connect to other Foundry resources.|
| OpenAI |       | Connect to your OpenAI  models. |
| Serp |       | Serp connects to Search Engine Results Pages (SERP) for real-time data access. Supports scenarios that need the latest search results.|
| API key                       |       | API Key connections handle authentication to your specified target on an individual basis. |
| Custom key                    |      | Custom connections allow you to securely store and access keys while storing related properties, such as targets and versions. Custom connections are useful when you have many targets or cases where you wouldn't need a credential to access. LangChain scenarios are a good example where you would use custom service connections. Custom connections don't manage authentication, so you have to manage authentication on your own. |
| Grounding with Bing Search | | Connects to Bing Search to provide real-time web grounding for queries. Enables AI agents to reference current web data in responses.
| Serverless Model              |    ✅     | Serverless Model connections allow you to serverless API deployment. Connection creation only supported through code. |
| Azure Databricks              |    ✅   | Azure Databricks connector allows you to connect your Foundry Agents to Azure Databricks to access workflows and Genie Spaces during runtime. Connection creation only supported through code. |
| Sharepoint |    ✅   | Sharepoint is a Microsoft platform for document storage and collaboration. It allows agents to access and manage organizational documents. Connection creation only supported through code. |
| Microsoft Fabric |    ✅   |  AI skills allow you to create your own conversational Q&A systems on Fabric using generative AI. Connection creation only supported through code.|
| Grounding with Bing Custom Search |    ✅   |  Integrates with a custom Bing search instance for tailored web grounding. Connection creation only supported through code.|	
| Azure APIM |    ✅   | APIM allows for governance of AI Models called in the Foundry Agent service. Connection creation only supported through code. |
| Model Gateway |    ✅   |  Model Gateway allows for governance of AI Models called in the Foundry Agent service. Connection creation only supported through code.|

::: moniker-end

::: moniker range="foundry-classic"
| Service connection type       | Preview | Description                                                                                                                                                                                                                    |
|-------------------------------|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Azure AI Search               |         | Azure AI Search is an Azure resource that supports information retrieval over your vector and textual data stored in search indexes. Required for Standard Agent deployment.                                                 |
| Azure Storage                 |         | Azure Storage is a cloud storage solution for storing unstructured data like documents, images, videos, and application installers. Required for Standard Agent deployment.                                                  |
| Azure Cosmos DB               | ✅       | Azure Cosmos DB is a globally distributed, multi-model database service that offers low latency, high availability, and scalability across multiple geographical regions. Required for Standard Agent deployment. Connection creation not supported in Foundry Management center.               |
| Azure OpenAI                  |     | Azure OpenAI is a service that provides access to OpenAI's models including the GPT-5, GPT-4o, DALLE-3, and Embeddings model series with the security and enterprise capabilities of Azure. |
| Application Insights          |    | Azure Application Insights is a service that enables developers to automatically detect performance anomalies, diagnose issues, and gain deep insights into application usage and behavior. |
| Azure Key Vault|  | Azure service for securely storing and accessing secrets. (See limitations below) |
| Foundry |      | Connect to other Foundry resources.|
| OpenAI |       | Connect to your OpenAI  models. |
| Serp |       | Serp connects to Search Engine Results Pages (SERP) for real-time data access. Supports scenarios that need the latest search results.|
| API key                       |       | API Key connections handle authentication to your specified target on an individual basis. |
| Custom key                    |      | Custom connections allow you to securely store and access keys while storing related properties, such as targets and versions. Custom connections are useful when you have many targets or cases where you wouldn't need a credential to access. LangChain scenarios are a good example where you would use custom service connections. Custom connections don't manage authentication, so you have to manage authentication on your own. |
| Grounding with Bing Search | | Connects to Bing Search to provide real-time web grounding for queries. Enables AI agents to reference current web data in responses.
| Serverless Model              |    ✅     | Serverless Model connections allow you to serverless API deployment.                                                                                                   |
| Azure Databricks              |    ✅   | Azure Databricks connector allows you to connect your Foundry Agents to Azure Databricks to access workflows and Genie Spaces during runtime.  |
| Sharepoint |    ✅   | Sharepoint is a Microsoft platform for document storage and collaboration. It allows agents to access and manage organizational documents.  |
| Microsoft Fabric |   ✅   |  AI skills allow you to create your own conversational Q&A systems on Fabric using generative AI. |
| Grounding with Bing Custom Search |    ✅   | Integrates with a custom Bing search instance for tailored web grounding. |     

::: moniker-end



### Azure Key Vault limitations

Foundry stores connections details in a managed Azure Key Vault if no Key Vault connection is created. Users that prefer to manage their secrets themselves can bring their own Azure Key Vault via a connection. All Foundry projects use a managed Azure Key Vault (not shown in your subscription). If you bring your own Azure Key Vault, note:

- Only one Azure Key Vault connection per Foundry resource at a time.
- You can delete an Azure Key Vault connection only if there are no other existing connections on the Foundry resource or project level.
- Secret migration isn't supported; recreate connections after attaching the Key Vault.
- Deleting the underlying Azure Key Vault breaks the Foundry resource (connections depend on stored secrets).
- Deleting secrets in your BYO Key Vault may break connections to other services.

### Azure Databricks connection (preview) limitations

It supports three connection types - __Jobs__, __Genie__, and __Other__. You can pick the Job or Genie space you want associated with this connection while setting up the connection in the Foundry UI. You can also use the Other connection type and allow your agent to access workspace operations in Azure Databricks. Authentication is handled through Microsoft Entra ID for users or service principals. For examples of using this connector, see [Jobs](https://github.com/Azure-Samples/AI-Foundry-Connections/blob/main/src/samples/python/sample_agent_adb_job.py) and [Genie](https://github.com/Azure-Samples/AI-Foundry-Connections/blob/main/src/samples/python/sample_agent_adb_genie.py). Note: Usage of this connection is available only via the Foundry SDK in code and is integrated into agents as a FunctionTool (please see the samples above for details). Usage of this connection in Foundry Playground is currently not supported.

## Create a new connection 

Use the portal or a Bicep template to add a connection.

# [Foundry portal](#tab/foundry-portal)

Follow these steps to create a new connection that's available for the current project.

::: moniker range="foundry-classic"

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)] 
1. Select __Management center__ from the bottom left navigation.
1. Select __Connected resources__ from the __Project__ section.
1. Select __+ New connection__ from the __Connected resources__ section.

    :::image type="content" source="../media/data-connections/connection-add.png" alt-text="Screenshot of the button to add a new connection." lightbox="../media/data-connections/connection-add.png":::

1. Select the service you want to connect to from the list of available external resources. For example, select __Azure AI Search__.

    :::image type="content" source="../media/data-connections/connection-add-browse-azure-ai-search.png" alt-text="Screenshot of the page to select Azure AI Search from a list of other resources." lightbox="../media/data-connections/connection-add-browse-azure-ai-search.png":::

1. Browse for and select your Azure AI Search service from the list of available services and then select the type of __Authentication__ to use for the resource. Select __Add connection__.

    > [!TIP]
    > Different connection types support different authentication methods. Using Microsoft Entra ID might require specific Azure role-based access permissions for your developers. For more information, visit [Role-based access control](../concepts/rbac-foundry.md).

    :::image type="content" source="../media/data-connections/connection-add-azure-ai-search-connect-entra-id.png" alt-text="Screenshot of the page to select the Azure AI Search service that you want to connect to." lightbox="../media/data-connections/connection-add-azure-ai-search-connect-entra-id.png":::

1. After the service is connected, select __Close__.

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)] 
1. Select **Operate** in the upper-right navigation.
1. Select **Admin** in the left pane.
1. Select your project name in the **Manage all projects** list.
1. Select **Add connection** in the upper-right corner.
1. Select the service you want to connect to from the list of available external resources. For example, select __Azure AI Search__.
1. Browse for and select your Azure AI Search service from the list of available services and then select the type of __Authentication__ to use for the resource. Select __Add connection__.

    > [!TIP]
    > Different connection types support different authentication methods. Using Microsoft Entra ID might require specific Azure role-based access permissions for your developers. For more information, visit [Role-based access control](../concepts/rbac-foundry.md).

::: moniker-end

# [Bicep](#tab/bicep)

See [Connection templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/01-connections) for examples of common connection templates.

---

## Network isolation

For end-to-end [network isolation](configure-private-link.md) with Foundry, you need private endpoints to connect to your connected resource. For example, if your Azure Storage account is set to public network access as __Disabled__, then a private endpoint should be deployed in your virtual network to access in Foundry. 

For more on how to set private endpoints to your connected resources, see the following documentation:
    
| Private resource      | Documentation                                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| Azure Storage         | [Use private endpoints](/azure/storage/common/storage-private-endpoints)                                       |
| Azure Cosmos DB        | [Configure Azure Private Link for Azure Cosmos DB](/azure/cosmos-db/how-to-configure-private-endpoints?tabs=arm-bicep) |
| Azure AI Search       | [Create a private endpoint for a secure connection](/azure/search/service-create-private-endpoint)             |
| Azure OpenAI          | [Securing Azure OpenAI inside a virtual network with private endpoints](/azure/ai-foundry/openai/how-to/network) |
| Application Insights  | [Use Azure Private Link to connect networks to Azure Monitor](/azure/azure-monitor/logs/private-link-security) |

> [!NOTE]
> Cross-subscription connections used for model deployment are not supported (Foundry, Azure OpenAI). You can't connect to resources from different subscriptions for model deployments.

## Related content

- [How to create vector indexes](../how-to/index-add.md)
:::moniker range="foundry-classic"
- [How to configure a managed network](configure-managed-network.md)
:::moniker-end
