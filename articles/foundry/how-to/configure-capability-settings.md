---
title: "Configure agent capability settings for Foundry"
description: "Declare the Azure Cosmos DB, Azure AI Search, and Azure Storage resources that Foundry Agent Service uses for agent state, vector data, and files."
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: how-to
ms.date: 09/22/2026
ms.custom:
  - doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a platform engineer, I want to declare the Azure resources my agents use on the Foundry account and project so that I don't have to provision and bind each storage dependency myself.
---

# Configure agent capability settings (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Use capability settings to declare the Azure resources that Foundry Agent Service uses for agent state, vector data, and files. Set these resources on a Microsoft Foundry account to establish defaults for its projects. Each project either inherits those defaults or overrides an individual store.

When an account uses agent network injection, Agent Service provisions the required underlying infrastructure and the connections to your resources as part of project provisioning. You don't create or bind those resources yourself.

> [!IMPORTANT]
> Capability settings use API version `2026-07-15-preview`.
>
> Regional availability follows a phased rollout. Capability settings are currently available in UK South and Canada Central.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Cosmos DB for NoSQL account with a total throughput limit of at least 3,000 RU/s. For container and throughput details, see [Standard agent setup](../agents/concepts/standard-agent-setup.md).
- An Azure Storage account.
- An Azure AI Search service, if you use Azure AI Search for vector data.
- The permissions described in [Permissions](#permissions). The identity that submits the deployment needs more than account creation rights.

## Supported settings

Each setting takes the full Azure resource ID of the resource you want Agent Service to use.

| Setting | What it stores | Supported resource |
| --- | --- | --- |
| `documentStore` | Agent threads and runtime state | Azure Cosmos DB for NoSQL |
| `vectorStore` | Retrieval and vector indexes | Azure Cosmos DB for NoSQL or Azure AI Search |
| `blobStore` | Agent files and artifacts | Azure Storage |

## Permissions

Capability settings and the backward-compatible capability host flow use different provisioning identities. Choose the permissions that match your deployment path.

### Caller permissions for provisioning

For an ARM REST or Bicep request that uses API version `2026-07-15-preview`, Foundry provisions capability settings in the caller context. The caller can be an interactive user, a CI/CD service principal, or a workload identity.

In addition to permission to create or update the Foundry account and project, assign only the following roles. Azure AI Search doesn't require a caller role. Assign each role at the narrowest scope that contains the referenced resource.

| Role | Scope | Why the caller needs it |
| --- | --- | --- |
| **Storage Blob Data Contributor** | Each Azure Storage account referenced by `blobStore` | Provision the required blob containers and storage setup |
| **Cosmos DB Operator** | Each Azure Cosmos DB account referenced by `documentStore`, and by `vectorStore` when the vector store is Azure Cosmos DB | Provision the required Cosmos DB resources |

A caller that can create the Foundry account but lacks **Storage Blob Data Contributor** or **Cosmos DB Operator** fails provisioning.

> [!NOTE]
> Portal deployments and calls to the legacy capability host REST API continue to use the project managed identity for provisioning. For that path, grant the project managed identity the provisioning and runtime roles described in [Standard agent setup](../agents/concepts/standard-agent-setup.md).

### Project managed identity permissions for runtime

The project managed identity is required after provisioning finishes. Agent Service uses it so that running agents and the generated connections can reach your document, vector, and blob stores.

Grant the project managed identity its data-plane roles before agents run. Storage Blob Data Contributor and Cosmos DB Operator on the caller enable capability settings provisioning only; they don't replace the roles the project managed identity needs at runtime. For the per-resource role list, see [Standard agent setup](../agents/concepts/standard-agent-setup.md) and [Foundry administrator guide](../concepts/administrator-guide.md).

## Configure account defaults

Declare the parameters your template needs.

```bicep
@description('Name of the Foundry account. The name must be globally unique.')
param accountName string

@description('Azure region for the account and its projects.')
param location string = resourceGroup().location

@description('Resource ID of the Azure Cosmos DB for NoSQL account that stores agent state.')
param documentStoreId string

@description('Resource ID of the Azure AI Search service that stores vector data.')
param vectorStoreId string

@description('Resource ID of the Azure Storage account that stores agent files.')
param blobStoreId string
```

Set `capabilitySettings` on the account. Projects created in this account inherit every setting they don't override.

```bicep
resource account 'Microsoft.CognitiveServices/accounts@2026-07-15-preview' = {
  name: accountName
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: accountName
    capabilitySettings: {
      documentStore: documentStoreId
      vectorStore: vectorStoreId
      blobStore: blobStoreId
    }
  }
}
```

### Add capability settings to a network-injected account

Agent network injection and capability settings work together. Set both at creation time, because you can't add `networkInjections` to an existing account. The following `properties` block replaces the one in the previous example, where `agentSubnetId` is the resource ID of a subnet delegated to `Microsoft.App/environments`.

If you reuse an existing account, it must already have agent network injection configured. A deployment can reference that account and set capability settings on its projects, but it can't add account-level network injection.

```bicep
properties: {
  allowProjectManagement: true
  customSubDomainName: accountName
  networkInjections: [
    {
      scenario: 'agent'
      subnetArmId: agentSubnetId
      useMicrosoftManagedNetwork: false
    }
  ]
  capabilitySettings: {
    documentStore: documentStoreId
    vectorStore: vectorStoreId
    blobStore: blobStoreId
  }
}
```

For networking requirements and deployment methods, see [Set up private networking for Foundry Agent Service](../agents/how-to/virtual-networks.md).

## Override a store on a project

Set only the settings a project needs to change. In the following example, the project uses its own Azure Storage account and inherits `documentStore` and `vectorStore` from the account.

```bicep
@description('Name of the project.')
param projectName string

@description('Resource ID of the Azure Storage account this project uses instead of the account default.')
param projectBlobStoreId string

resource project 'Microsoft.CognitiveServices/accounts/projects@2026-07-15-preview' = {
  parent: account
  name: projectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: projectName
    capabilitySettings: {
      blobStore: projectBlobStoreId
    }
  }
}
```

You can't add or update capability settings on an existing project. To apply different settings, delete and recreate the project with the desired `capabilitySettings` values. When you recreate the project, reuse its `location`, `displayName`, and `description` values if you want to preserve them.

## Inheritance and lifecycle

Capability settings follow these rules:

- Omit a setting on a project to inherit that value from the account.
- A GET on the project returns the effective configuration: inherited account values plus any project overrides.
- Changing account defaults doesn't update existing projects. To use the changed defaults, delete and recreate each affected project.
- Agent Service provisions and owns the connections derived from these settings. These capability-settings-managed connections are immutable while in use, so you can't edit or delete them directly.
- A project that has neither its own settings nor inherited settings uses service-owned data stores for agent context and artifacts.

## Troubleshoot

Provisioning failures and runtime failures have different causes. Check which identity the error refers to before you change role assignments.

### Provisioning errors

| Symptom | Cause | Resolution |
| --- | --- | --- |
| Error that names `blobStore` and a storage account scope | The caller lacks **Storage Blob Data Contributor** on that storage account | Assign the role to the caller at the storage account scope and redeploy. |
| Error that names `documentStore` or `vectorStore` and a Cosmos DB account scope | The caller lacks **Cosmos DB Operator** on that Cosmos DB account | Assign the role to the caller at the Cosmos DB account scope and redeploy. |

### Runtime errors

| Symptom | Cause | Resolution |
| --- | --- | --- |
| Provisioning succeeds, but agents can't read or write agent state, vectors, or files | The project managed identity is missing a runtime role | Grant the project managed identity the data-plane roles for the affected store. This is a runtime access failure, not a provisioning authorization failure. |
| A request to change or delete a generated connection fails | Connections derived from capability settings are service-managed and immutable while in use | Don't edit or delete the connection directly. To change the resources a project uses, delete and recreate the project with the desired `capabilitySettings` values. |

## Related content

- [Standard agent setup](../agents/concepts/standard-agent-setup.md)
- [Set up private networking for Foundry Agent Service](../agents/how-to/virtual-networks.md)
- [Create a project for Microsoft Foundry](create-projects.md)
- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
