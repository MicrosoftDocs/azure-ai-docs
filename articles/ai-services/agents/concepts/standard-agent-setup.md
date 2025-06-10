---
title: Built-in enterprise readiness with standard agent setup
titleSuffix: Azure AI Foundry
description: Learn about the enterprise features of the standard setup
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 05/05/2025
ms.custom: azure-ai-agents
---

# Built-in enterprise readiness with standard agent setup 

Standard Agent Setup offers enterprise-grade security, compliance, and control. This configuration uses customer-managed, single-tenant resources to store agent state and ensures all data remains within your control.  

In this setup: 
* Agent states (files, threads, vector stores) are stored in your own Azure resources. 
* Available with both public networking and private networking (Bring Your Own virtual network) options. 

## Leveraging your own resources for storing customer data
Both standard setup configurations are designed to give you complete control over sensitive data by requiring the use of your own Azure resources. The required Bring Your Own (BYO) resources include:   
* BYO File Storage: All files uploaded by developers (during agent configuration) or end-users (during interactions) are stored directly in the customer’s Azure Storage account.   
* BYO Search: All vector stores created by the agent leverage the customer’s Azure AI Search resource.   
* BYO Thread Storage: All customer messages and conversation history will be stored in the customer’s own Azure Cosmos DB account.  

By bundling these BYO features (file storage, search, and thread storage), the standard setup guarantees that your deployment is secure by default. All data processed by Azure AI Foundry Agent Service is automatically stored at rest in your own Azure resources, helping you meet internal policies, compliance requirements, and enterprise security standards. 

### Azure Cosmos DB for NoSQL

Your existing Azure Cosmos DB for NoSQL Account used in standard setup must have a total throughput limit of at least **3000 RU/s**. Both **Provisioned Throughput** and **Serverless** modes are supported.

When you use standard setup, **three containers** will be provisioned in your existing Cosmos DB account, and **each container requires 1000 RU/s**.
* thread-message-store: End-user conversations
* system-thread-message-store: Internal system messages
* agent-entity-store: Agent metadata including their instructions, tools, name, etc.

## Project-Level Data Isolation
Standard setup enforces project-level data isolation by default. Two blob storage containers will automatically be provisioned in your storage account, one for files and one for intermediate system data (chunks, embeddings) and three containers will be provisioned in your Cosmos DB, one for user systems, one for system messages, and one for user inputs related to created agents such as their instructions, tools, name, etc. This default behavior was chosen to reduce setup complexity while still enforcing strict data boundaries between projects.

## Capability hosts
**Capability hosts** are sub-resources on both the Account and Project, enabling interaction with the Azure AI Foundry Agent Service. 
- **Account Capability Host**: The account capability host has an empty request body except for the parameter capabilityHostKind="Agents". 
- **Project Capability Host**: Specifies resources for storing agent state, either managed multitenant (basic setup) or customer-owned (standard setup), single-tenant resource. Think of project capability host as the project settings.

### Limitations
- **Update Not Supported**: Cannot update the capability host for a project or account.


## Step by Step Provisioning Process
1. Create project dependent resources for standard setup
    * Create new (or pass in resource ID of existing) Cosmos DB resource 
    * Create new (or pass in resource ID of existing) Azure Storage resource 
    * Create new (or pass in resource ID of existing) Azure AI Search resource 
    * Create a new Key Vault resource 
    * [Optional]: Create new application insights resource 
    * [Optional]: pass in resource ID of existing AI Foundry resource 
2. Create Azure AI Foundry Resource (cognitive service/accounts kind=AIServices) 
3. Create Account-level connections 
    * Create account connection to Application Insights resource 
4. Deploy gpt-4o or other agent compatible model 
5. Create Project (cognitive service/accounts/project) 
6. Create project connections 
    * [if provided] Project connection to AI Foundry resource 
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
    * Cosmos DB for NoSQL container: `<'${projectWorkspaceId}>-thread-message-store'`
        * Assign role: Cosmos DB Built-in Data Contributor 
    * Cosmos DB for NoSQL container: `<'${projectWorkspaceId}>-thread-message-store'` 
        * Assign role: Cosmos DB Built-in Data Contributor 
    * Cosmos DB for NoSQL container: `<'${projectWorkspaceId}>-agent-entity-store'` 
        * Assign role: Cosmos DB Built-in Data Contributor 
11. Once all resources are provisioned, all developers who want to create/edit agents in the project should be assigned the role: Azure AI User on the project scope.