---
title: Azure AI Foundry architecture
titleSuffix: Azure AI Foundry
description: Learn about the architecture of Azure AI Foundry.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 07/22/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
---

# Azure AI Foundry architecture 

Azure AI Foundry provides a comprehensive set of tools to support development teams in building, customizing, evaluating, and operating AI Agents and its composing models and tools.

This article is intended to provide IT security teams with details on the Azure service architecture, its components, and its relation with related Azure resource types. Use this information to guide how to [customize](../how-to/configure-private-link.md) your Foundry deployment to your organization's requirements. For more information on how to roll out AI Foundry in your organization, see [Azure AI Foundry Rollout](planning.md).

## Azure AI resource types and providers

Within the Azure AI product family, we distinguish three [Azure resource providers](/azure/azure-resource-manager/management/resource-providers-and-types) supporting user needs at different layers in the stack.

| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Azure AI Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 
| Microsoft.MachineLearningServices | Train, deploy, and operate custom and open source machine learning models | Azure AI Hub (and its projects); Azure Machine Learning Workspace | 

The Azure AI Foundry resource is the primary resource for Azure AI and is recommended for most use cases. It's built on the same [Azure resource provider and resource type](/azure/azure-resource-manager/management/resource-providers-and-types) as the Azure OpenAI, Azure Speech, Azure Vision, and Azure Language services. It provides access to the superset of capabilities from each of the individual services combined.

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

Resource types under the same provider namespaces share the same management APIs, and use similar [Azure Role Based Access Control](/azure/role-based-access-control/overview) actions, networking configurations and aliases for Azure Policy configuration. If you're upgrading from Azure OpenAI to Azure AI Foundry, your existing custom Azure policies and Azure Role Based Access Control actions continue to apply.

## Security-driven separation of concerns

Azure AI Foundry enforces a clear separation between management and development operations to ensure secure and scalable AI workloads.

- **Top-Level Resource Governance:** Management operations, such as configuring security, establishing connectivity with other Azure services, and managing deployments, are scoped to the top-level Azure AI Foundry resource. Development activities are isolated within dedicated project containers, which encapsulate use cases and provide boundaries for access control, files, agents, and evaluations.

- **Role-Based Access Control (RBAC):** Azure RBAC actions are designed to reflect this separation of concerns. Control plane actions (for example creating deployments and projects) are distinct from data plane actions (for example building agents, running evaluations, and uploading files). RBAC assignments can be scoped at both the top-level resource and individual project level. [Managed identities](/entra/identity/managed-identities-azure-resources/overview) can be assigned at either scope to support secure automation and service access.

- **Monitoring and Observability:** Azure Monitor metrics are segmented by scope. Management and usage metrics are available at the top-level resource, while project-specific metrics—such as evaluation performance or agent activity—are scoped to the individual project containers.

## Computing infrastructure

Azure AI Foundry applies a flexible compute architecture to support diverse [model access](../concepts/foundry-models-overview.md) and workload execution scenarios. 

- Model Hosting Architecture: Foundry models access is provided in different ways:
  
  - [Standard deployment in Azure AI Foundry resources](deployments-overview.md#standard-deployment-in-azure-ai-foundry-resources)
  - [Deployment to serverless API endpoints in Azure AI Hub resources](deployments-overview.md#serverless-api-endpoint)
  - [Deployment to managed computes in Azure AI Hub resources](deployments-overview.md#managed-compute)

  For an overview of data, privacy, and security considerations with these deployment options, see [Data, privacy, and security for use of models](../how-to/concept-data-privacy.md)

- **Workload Execution:** Agents, Evaluations, and Batch jobs are executed as managed container compute, fully managed by Microsoft. 

- **Networking Integration:** For enhanced security and compliance when your Agents connect with external systems, [container injection](../agents/how-to/virtual-networks.md) allows the platform network to host APIs and inject a subnet into your network, enabling local communication of your Azure resources within the same virtual network. 

## Data storage

Azure AI Foundry provides flexible and secure data storage options to support a wide range of AI workloads.

* **Managed storage for file upload**:
In the default setup, Azure AI Foundry uses Microsoft-managed storage accounts that are logically separated and support direct file uploads for select use cases, such as OpenAI models, Assistants, and Agents, without requiring a customer-provided storage account.

* **Bring Your Own Storage (Optional)**:
Users can optionally connect their own Azure Storage accounts. Foundry tools can read inputs from and write outputs to these accounts, depending on the tool and use case.

* **Bring-your-own storage for storing Agent state:**

  * In the basic configuration, the Agent service stores threads, messages, and files in Microsoft-managed multi-tenant storage, with logical separation.
  * With the [Agent standard setup](../agents/how-to/use-your-own-resources.md), you can bring your own storage for thread and message data. In this configuration, data is isolated by project within the customer’s storage account.

* **Customer-Managed Key Encryption:**
  By default, Azure services use Microsoft-managed encryption keys to encrypt data in transit and at rest. Data is encrypted and decrypted using FIPS 140-2 compliant 256-bit AES encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

  When using customer-managed keys, your data on Microsoft-managed infrastructure is encrypted using your keys.
  
  To learn more about data encryption, see [customer-managed keys for encryption with Azure AI Foundry](encryption-keys-portal.md).

## Next steps

* [Azure AI Foundry rollout across my organization](planning.md)
* [Customer-managed keys for encryption with Azure AI Foundry](encryption-keys-portal.md)
* [How to configure a private link for Azure AI Foundry](../how-to/configure-private-link.md)
* [Bring-your-own resources with the Agent service](../agents/how-to/use-your-own-resources.md)
