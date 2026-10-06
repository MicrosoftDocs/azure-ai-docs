---
title: include file
description: include file
author: fosteramanda
ms.author: fosteramanda
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/09/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Standard agent setup uses customer-managed, single-tenant Azure resources to store agent state and keep all agent data under your control. Use standard setup when you need full data sovereignty, compliance with enterprise security policies, or project-level isolation.

In this setup:

* Agent states (conversations, responses) are stored in your own Azure resources.
* You maintain complete control over data residency and access.

> [!TIP]
> For a simpler setup that uses Microsoft-managed resources, see [Environment setup](../environment-setup.md) and choose the basic agent setup option.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An [Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/) account. For throughput requirements, see [Cosmos DB throughput requirements](#cosmos-db-throughput-requirements).
- An [Azure Storage](/azure/storage/common/storage-account-overview) account.
- An [Azure AI Search](/azure/search/search-what-is-azure-search) resource.
- An [Azure Key Vault](/azure/key-vault/general/overview) resource for secrets management.
- Azure CLI version 2.50 or later. Run `az --version` to verify.
- Permissions for the identity that runs a capability settings deployment. Beyond creating the account and project, this identity needs **Storage Blob Data Contributor** on the storage account and **Cosmos DB Operator** on the Cosmos DB account. Azure AI Search doesn't require a caller role. See [Configure agent capability settings](../../how-to/configure-capability-settings.md#permissions).
- A deployed agent-compatible model (for example, gpt-4o).

## Resource overview

> [!IMPORTANT]
> **Standard setups require you to Bring Your Own (BYO) resources so that all agent data stays in your Azure tenant:**
>

| Resource | What it stores |
|----------|---------------|
| **Azure Storage** (BYO File Storage) | Files uploaded by developers and end-users |
| **Azure AI Search** (BYO Search) | Vector stores created by the agent |
| **Azure Cosmos DB** (BYO Thread Storage) | Messages, conversation history, and agent metadata |

All data processed by Foundry Agent Service is automatically stored at rest in these resources, helping you meet compliance requirements and enterprise security standards.

### Cosmos DB throughput requirements

Your Azure Cosmos DB for NoSQL account must have a total throughput limit of at least **3000 RU/s**. Both **Provisioned Throughput** and **Serverless** modes are supported.

The **Standard setup** provisions **five containers**, each requiring **1000 RU/s**:

| Container | Purpose |
|-----------|---------|
| `thread-message-store` | End-user conversations |
| `system-thread-message-store` | Internal system messages |
| `agent-entity-store` | Agent metadata (instructions, tools, name) |
| `agent-definitions-v1` | Agent metadata (instructions, tools, name, versions) |
| `run-state-v1` | Internal messages and end-user conversations |

`thread-message-store`, `system-thread-message-store`, and `agent-entity-store` are part of the **Foundry Agent Service (Classic)** Standard Setup.

**Foundry Agent Service (New)** uses **`agent-definitions-v1`** and **`run-state-v1`**.  

The older containers belong to the **Classic** experience and are not used by the new runtime.

>[!Warning]
>The **Classic** and **New** Foundry Agent Service runtimes use **different Cosmos DB containers**.  

## Project-level data isolation

Standard setup enforces project-level data isolation by default. Two blob storage containers are automatically provisioned in your storage account: one for files and one for intermediate system data (chunks, embeddings). Three containers are provisioned in your Cosmos DB account: one for user threads, one for system messages, and one for agent configuration data such as instructions, tools, and names. This default behavior reduces setup complexity while still enforcing strict data boundaries between projects.

## Capability settings

Capability settings are properties on the Foundry account and the project that declare which Azure resources hold agent state, vector data, and files. Set them on the account to establish defaults for its projects, and override an individual store on a project when that project needs a different resource.

Agent Service provisions the required underlying infrastructure and the connections to your resources during provisioning. These capability-settings-managed connections are immutable while in use, so you can't edit or delete them directly. You also can't update capability settings on an existing project. To change which resources a project uses, delete and recreate the project with the desired settings.

For the full settings list, permissions, and Bicep examples, see [Configure agent capability settings](../../how-to/configure-capability-settings.md).

## Provision resources step by step

### Manual provisioning

Follow these steps to manually provision all resources needed for standard agent setup. Allow approximately 30-45 minutes for the full provisioning process.

#### Phase 1: Create dependent resources

1. Create or reuse the following resources. You can create new resources or pass in the resource ID of existing ones:
    * Azure Cosmos DB for NoSQL account
    * Azure Storage account
    * Azure AI Search resource
    * Azure Key Vault resource (used for managing secrets and connection strings for the agent infrastructure)
    * [Optional] Azure Application Insights resource
    * [Optional] Existing Foundry resource

#### Phase 2: Create Foundry resources and capability settings

2. Create a Microsoft Foundry resource.
3. Create account-level connections:
    * Create an account connection to the Application Insights resource.
4. Deploy gpt-4o or another agent-compatible model.
5. Set capability settings on the account, referencing the resource IDs of your Cosmos DB account, Azure AI Search service, and Storage account.
6. Create a project. The project inherits the account capability settings unless you override an individual store. Agent Service provisions the required underlying infrastructure and the connections to your resources as part of this step.

#### Phase 3: Assign runtime roles to the project managed identity

The project managed identity includes both System-assigned Managed Identity (SMI) and User-assigned Managed Identity (UMI). These roles govern runtime access for running agents. They're separate from the permissions the deploying identity needs, and one doesn't substitute for the other.

7. Assign the project managed identity (for SMI) the following roles:
    * **Cosmos DB Operator** at the account level for the Cosmos DB resource.
    * **Storage Account Contributor** at the account level for the Storage Account resource.

#### Phase 4: Assign granular resource permissions

8. Assign the project managed identity (both SMI and UMI) the following roles on the specified resource scopes:
    * **Azure AI Search**:
        * Search Index Data Contributor
        * Search Service Contributor
    * **Azure Blob Storage Container**: `<workspaceId>-azureml-blobstore`
        * Storage Blob Data Contributor
    * **Azure Blob Storage Container**: `<workspaceId>-azureml-agent`
        * Storage Blob Data Owner
    * **Cosmos DB for NoSQL Database**: `enterprise_memory`
        * Cosmos DB Built-in Data Contributor
        * Scope: Database level to cover all containers (no individual container-specific role assignment is needed).

#### Phase 5: Grant developer access

9. Assign all developers who need to create or edit agents in the project the **Foundry User** role on the project scope.

   [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

### Use a Bicep template

Use an existing Azure OpenAI, Azure Storage account, Azure Cosmos DB for NoSQL account, or Azure AI Search resource by providing the full Azure Resource Manager (ARM) resource ID in the [standard agent template file](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/43-standard-agent-setup-with-customization/main.bicep).

#### Use an existing Azure OpenAI resource

1. Follow the steps in [Environment setup](../environment-setup.md) to get the Foundry Tools account resource ID.
1. In the standard agent template file, replace the following placeholder:

    ```console
    existingAoaiResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}
    ```

#### Use an existing Azure Storage account for file storage

1. Sign in to the Azure CLI and select the subscription with your storage account:

    ```console
    az login
    ```

1. Run the following command to get your storage account resource ID:

    ```console
    az storage account show --resource-group <your-resource-group> --name <your-storage-account> --query "id" --output tsv
    ```

    The output is the `aiStorageAccountResourceID` value you need in the template.

1. In the standard agent template file, replace the following placeholder:

    ```console
    aiStorageAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}
    ```

#### Use an existing Azure Cosmos DB for NoSQL account for thread storage

An Azure Cosmos DB for NoSQL account is created for each Foundry account. For throughput requirements and multi-project scaling, see [Cosmos DB throughput requirements](#cosmos-db-throughput-requirements).

> [!NOTE]
> Insufficient RU/s capacity in the Cosmos DB account causes provisioning failures during deployment.

1. Sign in to the Azure CLI and select the subscription with your Cosmos DB account:

    ```console
    az login
    ```

1. Run the following command to get your Azure Cosmos DB account resource ID:

    ```console
    az cosmosdb show --resource-group <your-resource-group> --name <your-cosmosdb-account> --query "id" --output tsv
    ```

    The output is the `cosmosDBResourceId` value you need in the template.

1. In the standard agent template file, replace the following placeholder:

    ```console
    cosmosDBResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmosDbAccountName}
    ```

#### Use an existing Azure AI Search resource

1. Sign in to the Azure CLI and select the subscription with your search resource:

    ```console
    az login
    ```

1. Run the following command to get your Azure AI Search resource ID:

    ```console
    az search service show --resource-group <your-resource-group> --name <your-search-service> --query "id" --output tsv
    ```

1. In the standard agent template file, replace the following placeholder:

    ```console
    aiSearchServiceResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}
    ```

## Verify your setup

After you complete provisioning, verify the setup is working correctly:

1. In the Azure portal, navigate to your Foundry project and confirm that all connections (Storage, Cosmos DB, AI Search) appear under the project settings.
1. Confirm that a GET on the project returns the capability settings you expect, including any values inherited from the account.
1. Verify role assignments by navigating to each resource's **Access control (IAM)** page and confirming the project managed identity has the expected roles.
1. Create a test agent to confirm end-to-end functionality.

## Troubleshoot common issues

| Symptom | Cause | Resolution |
| --- | --- | --- |
| Provisioning fails with a Cosmos DB throughput error | Insufficient Cosmos DB throughput | Ensure your Cosmos DB account has at least 3000 RU/s (1000 RU/s per container × 3 containers). For multiple projects, multiply by the number of projects. |
| `403 Forbidden` when the agent reads or writes files | Missing storage role assignments | Verify the project managed identity has **Storage Blob Data Contributor** on the `<workspaceId>-azureml-blobstore` container and **Storage Blob Data Owner** on the `<workspaceId>-azureml-agent` container. |
| `SearchIndexNotFound` or `403` on search operations | Missing search roles | Confirm that the project managed identity has both **Search Index Data Contributor** and **Search Service Contributor** on your Azure AI Search resource. |
| `AuthorizationFailed` when creating or editing agents | Missing user role | Assign the **Foundry User** role to the developer on the project scope. |
| Deployment fails before any resource is provisioned | The deploying identity is missing a provisioning role | Confirm the caller holds **Storage Blob Data Contributor** and **Cosmos DB Operator**. See [Configure agent capability settings](../../how-to/configure-capability-settings.md#permissions). |

## Related content

- [Set up your environment for Foundry Agent Service](../environment-setup.md)
- [Configure agent capability settings](../../how-to/configure-capability-settings.md)
- [Standard agent setup Bicep template](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/43-standard-agent-setup-with-customization/main.bicep)
