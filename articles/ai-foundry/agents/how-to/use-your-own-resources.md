---
title: 'Use your own resources in the Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to use resources that you already have with the Foundry Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/19/2026
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
---

# Use your own resources

[!INCLUDE [version-banner](../../includes/version-banner.md)]

By default, Foundry Agent Service manages storage for files, conversations, and vector stores. If your organization requires full data ownership, customer-managed keys (CMK), or network isolation, you can connect your own Azure resources instead. This article shows you how to configure the deployment templates to use existing Azure OpenAI, Azure Storage, Azure Cosmos DB, and Azure AI Search resources with Agent Service.

## Limitations

There are some limitations you should be aware of when you plan to use existing resources with the Foundry Agent Service.

### If you are using a hub-based project or Azure OpenAI Assistants

At this time, there is no direct upgrade path to migrate existing agents or their associated data assets such as files, conversations, or vector stores from a hub-based project to a Microsoft Foundry project. There is also no upgrade path to convert existing Azure OpenAI Assistants into Foundry Agents, nor a way to automatically migrate Assistants' files, conversations, or vector stores.

You can reuse your existing model deployments and quota from Foundry Tools or Azure OpenAI resources within a Foundry project.

### SDK usage with hub-based projects

Starting in May 2025, the Azure AI Agent Service uses an endpoint for [Foundry projects](../../what-is-foundry.md#types-of-projects) instead of the connection string that was used for hub-based projects before this time. Connection strings are no longer supported in current versions of the SDKs and REST API. We recommend creating a new foundry project.

If you want to continue using your hub-based project and connection string, you need to: 
* Use the connection string for your project located under **Connection string** in the overview of your project. 

    :::image type="content" source="../../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="A screenshot showing the legacy connection string for a hub-based project.":::

* Use one of the previous versions of the SDK and the associated sample code:
    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/feature/azure-ai-agents/sdk/ai/Azure.AI.Projects/samples): `1.0.0-beta.2` or earlier
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects-beta10/sdk/ai/azure-ai-projects/samples/agents): `1.0.0b10` or earlier

### Azure Cosmos DB for NoSQL to store conversations

- Your existing Azure Cosmos DB for NoSQL account used in a [standard setup](#choose-basic-or-standard-agent-setup) must have a total throughput limit of at least 3000 RU/s. Both provisioned throughput and serverless are supported.
- Three containers will be provisioned in your existing Cosmos DB account, each requiring 1000 RU/s

> [!NOTE]
> * Make sure your Azure OpenAI resource and Foundry account and project are in the same region. 

## Prerequisites
* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* [Azure CLI](/cli/azure/install-azure-cli) (version 2.64 or later).
* Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope
* If configuring a [standard setup](#choose-basic-or-standard-agent-setup), the same individual must also have permissions to assign roles to required resources (Cosmos DB, Search, Storage). For more information about RBAC in Foundry, see [RBAC in Foundry](../../concepts/rbac-foundry.md).
    * The built-in role needed is **Role Based Access Administrator**.
    * Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    * The key permission needed is: `Microsoft.Authorization/roleAssignments/write`

* Register providers. The following providers must be registered:
    * `Microsoft.KeyVault`
    * `Microsoft.CognitiveServices`
    * `Microsoft.Storage`
    * `Microsoft.MachineLearningServices`
    * `Microsoft.Search`
    * `Microsoft.App`
    * `Microsoft.ContainerService`

:::moniker range="foundry-classic"

To use the [Grounding with Bing Search tool](../how-to/tools-classic/bing-grounding.md) the following provider must be registered: `Microsoft.Bing`

:::moniker-end

:::moniker range="foundry"

To use the [Grounding with Bing Search tool](../../default/agents/how-to/tools/bing-tools.md) the following provider must be registered: `Microsoft.Bing`

:::moniker-end

    ```console
    az provider register --namespace 'Microsoft.KeyVault'
    az provider register --namespace 'Microsoft.CognitiveServices'
    az provider register --namespace 'Microsoft.Storage'
    az provider register --namespace 'Microsoft.MachineLearningServices'
    az provider register --namespace 'Microsoft.Search'
    az provider register --namespace 'Microsoft.App'
    az provider register --namespace 'Microsoft.ContainerService'
    # only to use Grounding with Bing Search tool
    az provider register --namespace 'Microsoft.Bing'
    ```

## Choose basic or standard agent setup

To use your own resources, you can edit the parameters in the provided deployment templates. To start, determine if you want to edit the [basic agent setup template](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/42-basic-agent-setup-with-customization), or the [standard agent setup template](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/43-standard-agent-setup-with-customization).
   
**Basic Setup**

This setup is compatible with OpenAI Assistants and manages agent states using the platform's built-in storage. It includes the same tools and capabilities as the Assistants API, with added support for non-OpenAI models and tools such as Azure AI Search, and Bing. 

**Standard Setup**

Includes everything in the basic setup and fine-grained control over your data by allowing you to use your own Azure resources. All customer data—including files, conversations, and vector stores are stored in your own Azure resources, giving you full ownership and control.

## Basic agent setup: Use an existing Azure OpenAI resource 

Replace the parameter value for `existingAoaiResourceId`in the [template](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/42-basic-agent-setup-with-customization) with the full arm resource ID of the Azure OpenAI resource you want to use.

1. To get the Azure OpenAI account resource ID, sign in to the Azure CLI and select the subscription with your Foundry Tools account:
       
    ```console
    az login
    ``` 

2. Replace `<your-resource-group>` with the resource group containing your resource and `<your-ai-service-resource-name>` with the name of your Azure OpenAI or AI Services resource, and run:
    
    ```console
    az cognitiveservices account show --resource-group <your-resource-group> --name <your-ai-service-resource-name> --query "id" --output tsv
    ```

    The value returned is the `existingAoaiResourceId` you need to use in the template.

3. In the [basic agent template file](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/42-basic-agent-setup-with-customization/main.bicep), replace the following placeholder:
    
    ```console
    existingAoaiResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}
    ```

## Standard agent setup: Use existing service resources and storage accounts 

Use an existing Azure OpenAI, Azure Storage account, Azure Cosmos DB for NoSQL account and/or Azure AI Search resource by providing the full ARM resource ID in the [standard agent template file](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/43-standard-agent-setup-with-customization/main.bicep).

### Use an existing Azure OpenAI resource

1. Follow the steps in basic agent setup to get the Foundry Tools account resource ID.
2. In the standard agent template file, replace the following placeholders:
    
    ```console
    existingAoaiResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}

    ```

### Use an existing Azure Storage account for file storage

1. To get your storage account resource ID, sign in to the Azure CLI and select the subscription with your storage account: 
    
    ```console
    az login
    ``` 

2. Then run the command:

    ```console
    az storage account show --resource-group <your-resource-group> --name <your-storage-account> --query "id" --output tsv
    ```
   
     The output is the `azureStorageAccountResourceId` you need to use in the template.
   
3. In the standard agent template file, replace the following placeholder:
    
    ```console
    azureStorageAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}
    ```

### Use an existing Azure Cosmos DB for NoSQL account for conversation storage

An Azure Cosmos DB for NoSQL account is created for each Foundry account.

For every project under a Foundry account, three containers are deployed within the same Cosmos DB account. Each container requires a minimum of 1000 RU/s.

For example, if two projects are deployed under the same Foundry account, the Cosmos DB account must be configured with at least 6000 RU/s (3 containers × 1000 RU/s × 2 projects) to ensure sufficient throughput.

Both provisioned throughput and serverless modes are supported.

> [!NOTE]
> Insufficient RU/s capacity in the Cosmos DB account causes capability host provisioning failures during deployment.

1. To get your Azure Cosmos DB account resource ID, sign in to the Azure CLI and select the subscription with your account: 
    
    ```console
    az login
    ``` 
    
2. Then run the command:

    ```console
    az cosmosdb show --resource-group <your-resource-group> --name <your-cosmosdb-account> --query "id" --output tsv
    ```
    
     The output is the `azureCosmosDBAccountResourceId` you need to use in the template.

3. In the standard agent template file, replace the following placeholder:
    
    ```console
    azureCosmosDBAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmosDbAccountName}
    ```
    
### Use an existing Azure AI Search resource

1. To get your Azure AI Search resource ID, sign in to the Azure CLI and select the subscription with your search resource: 
    
    ```console
    az login
    ```

2. Then run the command:
    
    ```console
    az search service show --resource-group <your-resource-group> --name <your-search-service> --query "id" --output tsv
    ```

3. In the standard agent template file, replace the following placeholder:

    ```console
    aiSearchResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}
    ```

## See also

:::moniker range="foundry-classic"

* Learn about the different [tools](tools-classic/overview.md) agents can use. 

:::moniker-end

:::moniker range="foundry"

* Learn about the different [tools](../../default/agents/concepts/tool-catalog.md) agents can use. 

:::moniker-end
