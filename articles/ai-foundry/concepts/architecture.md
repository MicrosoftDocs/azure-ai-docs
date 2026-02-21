---
title: Microsoft Foundry architecture
titleSuffix: Microsoft Foundry
description: Learn about the architecture of Microsoft Foundry.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 01/06/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

---

# Microsoft Foundry architecture 

[!INCLUDE [version-banner](../includes/version-banner.md)]

Microsoft Foundry provides a comprehensive set of tools to help development teams build, customize, evaluate, and operate AI agents and the models and tools they use.

This article provides IT operations and security teams with details on the Foundry resource and underlying Azure service architecture, its components, and its relation with other Azure resource types. Use this information to guide how to [customize](../how-to/configure-private-link.md) your Foundry deployment to your organization's requirements. For more information on how to roll out Foundry in your organization, see [Foundry Rollout](planning.md).

## Azure AI resource types and providers

Within the Azure AI product family, you can use these [Azure resource providers](/azure/azure-resource-manager/management/resource-providers-and-types) that support user needs at different layers in the stack.

::: moniker range="foundry-classic"
| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 
| Microsoft.MachineLearningServices | Train, deploy, and operate custom and open source machine learning models | Azure AI Hub (and its projects); Azure Machine Learning Workspace | 
::: moniker-end

::: moniker range="foundry"
| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 
::: moniker-end


For many scenarios, the Foundry resource is the recommended starting point. Foundry resources share the Microsoft.CognitiveServices provider namespace with services such as Azure OpenAI, Azure Speech, Azure Vision, and Azure Language. This shared provider namespace helps align management APIs, access control patterns, networking, and policy behavior across related AI resources.

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

Resource types under the same provider namespaces share the same management APIs, and use similar [Azure Role Based Access Control](/azure/role-based-access-control/overview) actions, networking configurations, and aliases for Azure Policy configuration. If you're upgrading from Azure OpenAI to Foundry, your existing custom Azure policies and Azure Role Based Access Control actions continue to apply.

## How resources relate in Foundry

Use this model when planning architecture and access boundaries:

- **Foundry resource**: Top-level Azure resource where you manage governance settings such as networking, security, and model deployments.
- **Project**: Development boundary inside the Foundry resource where teams build and evaluate use cases.
- **Project assets**: Files, agents, evaluations, and related artifacts scoped to a project.

This separation lets IT teams apply centralized controls at the resource level while development teams work within project-level boundaries.

## Security-driven separation of concerns

Foundry enforces a clear separation between management and development operations to ensure secure and scalable AI workloads.

- **Top-Level Resource Governance:** Management operations, such as configuring security, establishing connectivity with other Azure services, and managing deployments, are scoped to the top-level Foundry resource. Development activities are isolated within dedicated project containers, which encapsulate use cases and provide boundaries for access control, files, agents, and evaluations.

- **Role-Based Access Control (RBAC):** Azure RBAC actions reflect this separation of concerns. Control plane actions, such as creating deployments and projects, are distinct from data plane actions, such as building agents, running evaluations, and uploading files. You can scope RBAC assignments at both the top-level resource and individual project level. Assign [managed identities](/entra/identity/managed-identities-azure-resources/overview) at either scope to support secure automation and service access. For more information, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).

  Common starter assignments for least-privilege onboarding include:

  - **Azure AI User** for each developer user principal at the Foundry resource scope.
  - **Azure AI User** for each project managed identity at the Foundry resource scope.

  For role definitions and scope planning guidance, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).

- **Monitoring and Observability:** Azure Monitor metrics are segmented by scope. You can view management and usage metrics at the top-level resource, while project-specific metrics, such as evaluation performance or agent activity, are scoped to the individual project containers.

## Computing infrastructure

::: moniker range="foundry-classic"
Foundry uses a flexible compute architecture to support different [model access](../concepts/foundry-models-overview.md) and workload execution scenarios. 

- **Model Hosting Architecture**: Foundry models access is provided in different ways:
  
  - [Standard deployment in Foundry resources](deployments-overview.md#standard-deployment-in-foundry-resources)
  - [Deployment to serverless API endpoints in Azure AI Hub resources](deployments-overview.md#serverless-api-endpoint)
  - [Deployment to managed computes in Azure AI Hub resources](deployments-overview.md#managed-compute)

  For an overview of data, privacy, and security considerations with these deployment options, see [Data, privacy, and security for use of models](../how-to/concept-data-privacy.md).

::: moniker-end

::: moniker range="foundry"
- **Model Hosting Architecture** is provided by standard deployment in Foundry resources.   For an overview of data, privacy, and security considerations with deployment, see [Data, privacy, and security for use of models](../how-to/concept-data-privacy.md).

::: moniker-end


- **Workload Execution:** Agents, Evaluations, and Batch jobs run as managed container compute, fully managed by Microsoft. 

- **Networking Integration:** For enhanced security and compliance when your Agents connect with external systems, [container injection](../agents/how-to/virtual-networks.md) allows the platform network to host APIs and inject a subnet into your network. This setup enables local communication of your Azure resources within the same virtual network. 

  If you require end-to-end network isolation, review current limitations before rollout. In the new Foundry portal experience, end-to-end isolation scenarios aren't fully supported. Use the classic experience, SDK, or CLI guidance for network-isolated deployments. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).

## Data storage

Foundry provides flexible and secure data storage options to support a wide range of AI workloads.

* **Managed storage for file upload**:
In the default setup, Foundry uses Microsoft-managed storage accounts that are logically separated and support direct file uploads for select use cases, such as OpenAI models, Assistants, and Agents, without requiring a customer-provided storage account.

* **Bring your own storage (optional)**:
Users can optionally connect their own Azure Storage accounts. Foundry tools can read inputs from and write outputs to these accounts, depending on the tool and use case.

* **Bring your own storage for storing Agent state**:

  * In the basic configuration, the Agent service stores threads, messages, and files in Microsoft-managed multitenant storage, with logical separation.
  * With the [Agent standard setup](../agents/how-to/use-your-own-resources.md), you can bring your own storage for thread and message data. In this configuration, data is isolated by project within the customer’s storage account.

* **Customer-managed key encryption**:
  By default, Azure services use Microsoft-managed encryption keys to encrypt data in transit and at rest. Data is encrypted and decrypted using FIPS 140-2 compliant 256-bit AES encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

  Before you enable customer-managed keys for Foundry, confirm these prerequisites:

  - Key Vault is deployed in the same Azure region as your Foundry resource.
  - Soft delete and purge protection are enabled on Key Vault.
  - Managed identities have required key permissions, such as the **Key Vault Crypto User** role when using Azure RBAC.

* **Bring your own Key Vault**:
  By default, Foundry stores all API key-based connection secrets in a managed Azure Key Vault. For users that prefer to manage this themselves, they can connect their key vault to the Foundry resource. One Azure Key Vault connection manages all project and resource level connection secrets. For more information, see [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).

  When you use customer-managed keys, your data on Microsoft-managed infrastructure is encrypted by using your keys.
  
  To learn more about data encryption, see [customer-managed keys for encryption with Foundry](encryption-keys-portal.md).

## Validate architecture decisions

Before rollout, validate the following for your target environment:

1. Confirm that required models and features are available in your deployment regions. For details, see [Feature availability across cloud regions](../reference/region-support.md).
1. Confirm that role assignments are scoped correctly at both the Foundry resource and project levels. For details, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).
1. Confirm network isolation requirements and private access paths. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).
1. Confirm encryption and secret-management requirements, including customer-managed keys and Azure Key Vault integration. For details, see [Customer-managed keys for encryption with Foundry](encryption-keys-portal.md) and [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).

## Related content

* [Foundry rollout across my organization](planning.md)
* [Role-based access control for Microsoft Foundry](rbac-foundry.md).
* [Customer-managed keys for encryption with Foundry](encryption-keys-portal.md)
* [How to configure a private link for Foundry](../how-to/configure-private-link.md)
* [Bring-your-own resources with the Agent service](../agents/how-to/use-your-own-resources.md)
