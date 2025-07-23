---
title: Azure AI Foundry architecture
titleSuffix: Azure AI Foundry
description: Learn about the architecture of Azure AI Foundry.
manager: scottpolly
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

Azure AI Foundry provides a comprehensive set of tools to support development teams in building, customizing, evaluating and operating AI Agents and its composing models and tools.

This article is intended to provide IT security teams with details on the Azure service architecture, its components, and its relation with related Azure resource types. Use this information to guide how to [customize](how-to/configure-private-link.md) your Foundry deployment to your organization's requirements. For additional guidance on how to roll out AI Foundry in your organization, see [Azure AI Foundry Rollout](concepts/planning.md).

## Azure AI resource types and providers

Within the Azure AI product family, we distinguish three [Azure resource providers]() supporting user needs at different layers in the stack.

| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing pre-built models. | Azure AI Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 
| Microsoft.MachineLearningServices | Train, deploy and operate custom and open source machine learning models | Azure AI Hub (and its projects); Azure Machine Learning Workspace | 

[Resource provider registration](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) is required in your Azure subscription before you are able to create the above resource types.

Azure AI Foundry resource is the primary resource for Azure AI and is recommended for most use cases. It is built on the same [Azure resource provider](#LINK) and [resource type](#LINK) as Azure OpenAI service, Azure Speech, Azure Vision, and Azure Language service. It provides access to the superset of capabilities from each individual services combined. 

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

Resource types under the same provider namespace use similar [Azure RBAC](#link) actions, networking configurations and aliases for Azure Policy configuration. If you are upgrading from Azure OpenAI to Azure AI Foundry, this means your existing custom Azure policies and Azure RBAC options apply. 

## Security-driven separation of concerns

Azure AI Foundry enforces a clear separation between management and development operations to ensure secure and scalable AI workloads.

- **Top-Level Resource Governance:** Management operations—such as configuring security, establishing connectivity with other Azure services, and managing deployments—are scoped to the top-level Azure AI Foundry resource. Development activities are isolated within dedicated project containers, which encapsulate use cases and provide boundaries for access control, files, agents, and evaluations.

- **Role-Based Access Control (RBAC):** Azure RBAC actions are designed to reflect this separation of concerns. Control plane actions (e.g., creating deployments and projects) are distinct from data plane actions (e.g., building agents, running evaluations, uploading files). RBAC assignments can be scoped at both the top-level resource and individual project level. Managed identities can also be assigned at either scope to support secure automation and service access.

- **Monitoring and Observability:** Azure Monitor metrics are segmented by scope. Management and usage metrics are available at the top-level resource, while project-specific metrics—such as evaluation performance or agent activity—are scoped to the individual project containers.

## Computing infrastructure

Azure AI Foundry leverages a flexible compute architecture to support diverse model hosting and workload execution scenarios.

- Model Hosting Architecture: Models are hosted using different compute stacks depending on their origin:

  - **Microsoft-hosted** models are served directly by Microsoft's model serving infrastructure.
  - **Partner models** are served by Microsoft's model serving infrastructure.
  - **Open-source models** are deployed on managed compute through the Azure ML stack, accessible via AI Hub and hub-based projects. To learn more, see [this link](#some-link) These rely on Azure Batch infrastructure within Microsoft subscriptions, with support for managed virtual networking.

- **Workload Execution:** Agents and Evaluations are executed on Azure Container Apps compute, fully managed by Microsoft. This ensures scalability and operational consistency across use cases.

- **Networking Integration:** For enhanced security and compliance, Agents can be injected into your own virtual network (VNet). Evaluations, however, currently do not support VNet injection during the preview phase.

## Data storage

Azure AI Foundry provides flexible and secure data storage options to support a wide range of AI workloads.

* **Managed Storage (Default Configuration)**:
In the default setup, Azure AI Foundry uses Microsoft-managed, multi-tenant storage accounts. These accounts offer per-tenant isolation and support direct file uploads for select use cases—such as OpenAI models, Assistants, and Agents—without requiring a customer-provided storage account.

* **Bring Your Own Storage (Optional)**:
Users can optionally connect their own Azure Storage accounts. Foundry tools can read inputs from and write outputs to these accounts, depending on the tool and use case.

* **Agent Data Storage:**

  * In the basic configuration, the Agent service stores threads, messages, and files in Microsoft-managed multi-tenant storage, with tenant-level isolation.
  * With the Agent standard setup, users can bring their own storage for thread and message data. In this configuration, data is isolated by project within the customer’s storage account. For details on the container format, refer to the documentation [link to container format doc].

* **Customer-Managed Key Encryption:**
  When using customer-managed keys, data remains stored in Microsoft-managed multi-tenant infrastructure, encrypted using the customer’s keys. To support in-product search and optimized query performance, a dedicated Azure Search instance is provisioned for metadata indexing.

## Credential storage

When configuring Azure AI Foundry tools to connect with external Azure or non-Azure services, certain scenarios require storing sensitive credentials such as connection strings or API keys.

* **Default Configuration:**
  By default, secrets are stored in Microsoft-managed Key Vault instances.

* **Bring Your Own Key Vault (Preview):**
  As an optional configuration (preview), you can integrate your own Azure Key Vault instance for credential storage. This allows for greater control over secret management and aligns with enterprise-specific security policies.

## Next steps

* Rollout doc
* CMK docs
* Networking odcs
* AGent standar set up docs