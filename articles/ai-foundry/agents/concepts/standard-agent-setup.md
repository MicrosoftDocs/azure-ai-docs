---
title: Built-in enterprise readiness with standard agent setup
titleSuffix: Microsoft Foundry
description: Learn about the enterprise features of the standard setup
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/19/2025
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
---

# Built-in enterprise readiness with standard agent setup 

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Standard Agent Setup uses customer-managed, single-tenant Azure resources to store agent state and keep all agent data under your control.  

In this setup: 
* Agent states (conversations, responses) are stored in your own Azure resources. 

## Leveraging your own resources for storing customer data
Both standard setup configurations are designed to give you complete control over sensitive data by requiring the use of your own Azure resources. The required Bring Your Own (BYO) resources include:   
* **BYO File Storage**: All files uploaded by developers (during agent configuration) or end-users (during interactions) are stored directly in the customer’s Azure Storage account.   
* **BYO Search**: All vector stores created by the agent leverage the customer’s Azure AI Search resource.   
* **BYO Thread Storage**: All customer messages and conversation history will be stored in the customer’s own Azure Cosmos DB account.  

By bundling these BYO features (file storage, search, and thread storage), the standard setup guarantees that your deployment is secure by default. All data processed by Foundry Agent Service is automatically stored at rest in your own Azure resources, helping you meet internal policies, compliance requirements, and enterprise security standards. 

### Azure Cosmos DB for NoSQL

Your existing Azure Cosmos DB for NoSQL Account used in standard setup must have a total throughput limit of at least **3000 RU/s**. Both **Provisioned Throughput** and **Serverless** modes are supported.

When you use standard setup, **three containers** will be provisioned in your existing Cosmos DB account, and **each container requires 1000 RU/s**.
* thread-message-store: End-user conversations
* system-thread-message-store: Internal system messages
* agent-entity-store: Agent metadata including their instructions, tools, name, etc.

## Project-Level Data Isolation
Standard setup enforces project-level data isolation by default. Two blob storage containers will automatically be provisioned in your storage account, one for files and one for intermediate system data (chunks, embeddings) and three containers will be provisioned in your Cosmos DB, one for user systems, one for system messages, and one for user inputs related to created agents such as their instructions, tools, name, etc. This default behavior was chosen to reduce setup complexity while still enforcing strict data boundaries between projects.

## Capability hosts
**[Capability hosts](./capability-hosts.md)** are sub-resources on both the Account and Project, enabling interaction with the Agent Service. 
- **Account Capability Host**: The account capability host has an empty request body except for the parameter capabilityHostKind="Agents". 
- **Project Capability Host**: Specifies resources for storing agent state, either managed multitenant (basic setup) or customer-owned (standard setup), single-tenant resource. Think of project capability host as the project settings.

### Limitations
- **Update Not Supported**: Cannot update the capability host for a project or account.


## Step by Step Provisioning Process

### Manual 
1. Create project dependent resources for standard setup
    * Create new (or pass in resource ID of existing) Cosmos DB resource 
    * Create new (or pass in resource ID of existing) Azure Storage resource 
    * Create new (or pass in resource ID of existing) Azure AI Search resource 
    * Create a new Key Vault resource 
    * [Optional]: Create new application insights resource 
    * [Optional]: pass in resource ID of existing Foundry resource 
2. Create Microsoft Foundry Resource (cognitive service/accounts kind=AIServices) 
3. Create Account-level connections 
    * Create account connection to Application Insights resource 
4. Deploy gpt-4o or other agent compatible model 
5. Create Project (cognitive service/accounts/project) 
6. Create project connections 
    * [if provided] Project connection to Foundry resource 
    * Create project connection to Azure Storage account 
    * Create project connection to Azure AI Search account 
    * Create project connection to Cosmos DB account 
7. Assign the project-managed identity (including for SMI) the following roles: 
    * Cosmos DB Operator at the scope of the account level for the Cosmos DB account resource 
    * Storage Account Contributor at the scope of the account level for the Storage Account resource 
8. Set Account capability host with empty properties section. 
9. Set Project capability host with properties Cosmos DB, Azure Storage, AI Search connections 
10. Assign the Project Managed Identity (both for SMI and UMI) the following roles on the specified resource scopes: 
    * Azure AI Search (can be assigned either before or after capHost creation) 
        * Assign roles: Search Index Data Contributor, Search Service Contributor 
    * Azure Blob Storage Container: `<workspaceId>-azureml-blobstore`
        * Assign role: Storage Blob Data Contributor 
    * Azure Blob Storage Container: `<workspaceId>- agents-blobstore` 
        * Assign role: Storage Blob Data Owner  
    * Cosmos DB for NoSQL Database: `enterprise_memory`
        * Assign role: Cosmos DB Built-in Data Contributor
        * Scope: Database level to cover all containers (no individual container specific role assignment). 

11. Once all resources are provisioned, all developers who want to create/edit agents in the project should be assigned the role: Azure AI User on the project scope.

### Use Bicep template

Use an existing Azure OpenAI, Azure Storage account, Azure Cosmos DB for NoSQL account and/or Azure AI Search resource by providing the full ARM resource ID in the [standard agent template file](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/43-standard-agent-setup-with-customization/main.bicep).

#### Use an existing Azure OpenAI resource

1. Follow the steps in basic agent setup to get the Foundry Tools account resource ID.
2. In the standard agent template file, replace the following placeholders:
    
    ```console
    existingAoaiResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}

    ```

#### Use an existing Azure Storage account for file storage

1. To get your storage account resource ID, sign in to the Azure CLI and select the subscription with your storage account: 
    
    ```az login``` 
2. Then run the command:

    ```az storage account show --resource-group  <your-resource-group> --name <your-storage-account>  --query "id" --output tsv```
   
     The output is the `aiStorageAccountResourceID` you need to use in the template.
   
3. In the standard agent template file, replace the following placeholders:
    
    ```
    aiStorageAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}
    ```

#### Use an existing Azure Cosmos DB for NoSQL account for thread storage

An Azure Cosmos DB for NoSQL account is created for each Foundry account.

For every project under a Foundry account, three containers are deployed within the same Cosmos DB account. Each container requires a minimum of 1000 RU/s.

For example, if two projects are deployed under the same Foundry account, the Cosmos DB account must be configured with at least 6000 RU/s (3 containers × 1000 RU/s × 2 projects) to ensure sufficient throughput.

Both provisioned throughput and serverless modes are supported.

> [!NOTE]
> Insufficient RU/s capacity in the Cosmos DB account will result in capability host provisioning failures during deployment.

1. To get your Azure Cosmos DB account resource ID, sign in to the Azure CLI and select the subscription with your account: 
    
    ```console
    az login
    ``` 
    
2. Then run the command:

    ```console
    az cosmosdb show --resource-group  <your-resource-group> --name <your-comosdb-account>  --query "id" --output tsv
    ```
    
     The output is the `cosmosDBResourceId` you need to use in the template.
3. In the standard agent template file, replace the following placeholders:
    
    `cosmosDBResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmosDbAccountName}`
    
#### Use an existing Azure AI Search resource

1. To get your Azure AI Search resource ID, sign into Azure CLI and select the subscription with your search resource: 
    
    ```az login```
2. Then run the command:
    
    ```az search service show --resource-group  <your-resource-group> --name <your-search-service>  --query "id" --output tsv```
3. In the standard agent template file, replace the following placeholders:

    ```
    aiSearchServiceResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}
    ```