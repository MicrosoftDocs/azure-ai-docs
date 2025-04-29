---
title: Azure AI Foundry architecture
titleSuffix: Azure AI Foundry
description: Learn about the architecture of Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 04/28/2025
ms.reviewer: deeikele
ms.author: larryfr
author: Blackmist
---

# Azure AI Foundry architecture 

> [!NOTE]
> The architecture discussed in this article is specific to a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).
    
Azure AI Foundry provides a unified experience for AI developers and data scientists to build, evaluate, and deploy AI models through a web portal, SDK, or CLI. Azure AI Foundry is built on capabilities and services provided by other Azure services.

:::image type="content" source="../media/concepts/ai-studio-architecture.png" alt-text="Diagram of the high-level architecture of Azure AI Foundry." lightbox="../media/concepts/ai-studio-architecture.png":::

At the top level, Azure AI Foundry provides access to the following resources:

- **Azure OpenAI**: Provides access to the latest OpenAI models. You can create secure deployments, try playgrounds, fine tune models, content filters, and batch jobs. The Azure OpenAI resource provider is `Microsoft.CognitiveServices/account` and the kind of resource is `OpenAI`. You can also connect to Azure OpenAI by using a kind of `AIServices`, which also includes other [Azure AI services](/azure/ai-services/what-are-ai-services).

    When you use Azure AI Foundry portal, you can directly work with Azure OpenAI without an Azure Studio project. Or you can use Azure OpenAI through a project.

    For more information, visit [Azure OpenAI in Azure AI Foundry portal](../azure-openai-in-azure-ai-foundry.md).

- **Management center**: The management center streamlines governance and management of Azure AI Foundry resources such as hubs, projects, connected resources, and deployments.

    For more information, visit [Management center](management-center.md).
- **Azure AI Foundry hub**: The hub is the top-level resource in Azure AI Foundry portal, and is based on the Azure Machine Learning service. The Azure resource provider for a hub is `Microsoft.MachineLearningServices/workspaces`, and the kind of resource is `Hub`. It provides the following features:
    - Security configuration including a managed network that spans projects and model endpoints.
    - Compute resources for interactive development, fine-tuning, open source, and serverless model deployments.
    - Connections to other Azure services such as Azure OpenAI, Azure AI services, and Azure AI Search. Hub-scoped connections are shared with projects created from the hub.
    - Project management. A hub can have multiple child projects.
    - An associated Azure storage account for data upload and artifact storage.
    
    For more information, visit [Hubs and projects overview](ai-resources.md).
- **Azure AI Foundry project**: A project is a child resource of the hub. The Azure resource provider for a project is `Microsoft.MachineLearningServices/workspaces`, and the kind of resource is `Project`. The project provides the following features:
    - Access to development tools for building and customizing AI applications.   
    - Reusable components including datasets, models, and indexes.
    - An isolated container to upload data to (within the storage inherited from the hub).
    - Project-scoped connections. For example, project members might need private access to data stored in an Azure Storage account without giving that same access to other projects.
    - Open source model deployments from catalog and fine-tuned model endpoints.

    :::image type="content" source="../media/concepts/resource-provider-connected-resources.svg" alt-text="Diagram of the relationship between Azure AI Foundry resources." :::

    For more information, visit [Hubs and projects overview](ai-resources.md).

- **Connections**: Azure AI Foundry hubs and projects use connections to access resources provided by other services. For example, data in an Azure Storage Account, Azure OpenAI or other Azure AI services.

    For more information, visit [Connections](connections.md).

## Azure resource types and providers

Azure AI Foundry is built on the Azure Machine Learning resource provider, and takes a dependency on several other Azure services. The resource providers for these services must be registered in your Azure subscription. The following table lists the resource types, provider, and kind:

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

When you create a new hub, a set of dependent Azure resources are required to store data, get access to models, and provide compute resources for AI customization. The following table lists the dependent Azure resources and their resource providers:

> [!TIP]
> If you don't provide a dependent resource when creating a hub, and it's a required dependency, Azure AI Foundry creates the resource for you.

[!INCLUDE [Dependent Azure resources](../includes/dependent-resources.md)]

For information on registering resource providers, see [Register an Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider).

### Microsoft-hosted resources

While most of the resources used by Azure AI Foundry live in your Azure subscription, some resources are in an Azure subscription managed by Microsoft. The cost for these managed resources shows on your Azure bill as a line item under the Azure Machine Learning resource provider. The following resources are in the Microsoft-managed Azure subscription, and don't appear in your Azure subscription:

- **Managed compute resources**: Provided by Azure Batch resources in the Microsoft subscription.
- **Managed virtual network**: Provided by Azure Virtual Network resources in the Microsoft subscription. If FQDN rules are enabled, an Azure Firewall (standard) is added and charged to your subscription. For more information, see [Configure a managed virtual network for Azure AI Foundry](../how-to/configure-managed-network.md).
- **Metadata storage**: Provided by Azure Storage resources in the Microsoft subscription.  

    > [!NOTE]
    > If you use customer-managed keys, the metadata storage resources are created in your subscription. For more information, see [Customer-managed keys](encryption-keys-portal.md).

Managed compute resources and managed virtual networks exist in the Microsoft subscription, but you manage them. For example, you control which VM sizes are used for compute resources, and which outbound rules are configured for the managed virtual network.

Managed compute resources also require vulnerability management. Vulnerability management is a shared responsibility between you and Microsoft. For more information, see [vulnerability management](vulnerability-management.md).

## Centrally set up and govern using hubs

Hubs provide a central way for a team to govern security, connectivity, and computing resources across playgrounds and projects. Projects that are created using a hub inherit the same security settings and shared resource access. Teams can create as many projects as needed to organize work, isolate data, and/or restrict access.

Often, projects in a business domain require access to the same company resources such as vector indices, model endpoints, or repos. As a team lead, you can preconfigure connectivity with these resources within a hub, so developers can access them from any new project workspace without delay on IT.

[Connections](connections.md) let you access objects in Azure AI Foundry that are managed outside of your hub. For example, uploaded data on an Azure storage account, or model deployments on an existing Azure OpenAI resource. A connection can be shared with every project or made accessible to one specific project. Connections can be configured to use key-based access or Microsoft Entra ID passthrough to authorize access to users on the connected resource. As an administrator, you can  track, audit, and manage connections across the organization from a single view in Azure AI Foundry.

:::image type="content" source="../media/concepts/connected-resources-spog.png" alt-text="Screenshot of Azure AI Foundry showing an audit view of all connected resources across a hub and its projects." :::

### Organize for your team's needs

The number of hubs and projects you need depends on your way of working. You might create a single hub for a large team with similar data access needs. This configuration maximizes cost efficiency, resource sharing, and minimizes setup overhead. For example, a hub for all projects related to customer support.

If you require isolation between dev, test, and production as part of your LLMOps or MLOps strategy, consider creating a hub for each environment. Depending on the readiness of your solution for production, you might decide to replicate your project workspaces in each environment or just in one.

## Role-based access control and control plane proxy

Azure AI services including Azure OpenAI provide control plane endpoints for operations such as listing model deployments. These endpoints are secured using a separate Azure role-based access control (RBAC) configuration than the one used for a hub. 

To reduce the complexity of Azure RBAC management, Azure AI Foundry provides a *control plane proxy* that allows you to perform operations on connected Azure AI services and Azure OpenAI resources. Performing operations on these resources through the control plane proxy only requires Azure RBAC permissions on the hub. The Azure AI Foundry service then performs the call to the Azure AI services or Azure OpenAI control plane endpoint on your behalf.

For more information, see [Role-based access control in Azure AI Foundry portal](rbac-azure-ai-foundry.md).

## Attribute-based access control

Each hub you create has a default storage account. Each child project of the hub inherits the storage account of the hub. The storage account is used to store data and artifacts.

To secure the shared storage account, Azure AI Foundry uses both Azure RBAC and Azure attribute-based access control (Azure ABAC). Azure ABAC is a security model that defines access control based on attributes associated with the user, resource, and environment. Each project has:

- A service principal that is assigned the Storage Blob Data Contributor role on the storage account.
- A unique ID (workspace ID).
- A set of containers in the storage account. Each container has a prefix that corresponds to the workspace ID value for the project.

The role assignment for each project's service principal has a condition that only allows the service principal access to containers with the matching prefix value. This condition ensures that each project can only access its own containers.

> [!NOTE]
> For data encryption in the storage account, the scope is the entire storage and not per-container. So all containers are encrypted using the same key (provided either by Microsoft or by the customer).

For more information on Azure access-based control, see [What is Azure attribute-based access control](/azure/role-based-access-control/conditions-overview).

## Containers in the storage account

The default storage account for a hub has the following containers. These containers are created for each project, and the `{workspace-id}` prefix matches the unique ID for the project. Projects access a container by using a [connection](connections.md).

> [!TIP]
> To find the ID for your project, go to the project in the [Azure portal](https://portal.azure.com/). Expand **Settings** and then select **Properties**. The **Workspace ID** is displayed.

| Container name | Connection name | Description |
| --- | --- | --- |
| `{workspace-ID}-azureml` | workspaceartifactstore | Storage for assets such as metrics, models, and components. |
| `{workspace-ID}-blobstore`| workspaceblobstore | Storage for data upload, job code snapshots, and pipeline data cache. |
| `{workspace-ID}-code` | NA | Storage for notebooks, compute instances, and prompt flow. |
| `{workspace-ID}-file` | NA | Alternative container for data upload. |

## Encryption

Azure AI Foundry uses encryption to protect data at rest and in transit. By default, Microsoft-managed keys are used for encryption. However you can use your own encryption keys. For more information, see [Customer-managed keys](../../ai-services/encryption/cognitive-services-encryption-keys-portal.md?context=/azure/ai-studio/context/context).

## Virtual network

A hub can be configured to use a *managed* virtual network. The managed virtual network secures communications between the hub, projects, and managed resources such as computes. If your dependency services (Azure Storage, Key Vault, and Container Registry) have public access disabled, a private endpoint for each dependency service is created to secure communication between the hub and project and the dependency service.

> [!NOTE]
> If you want to use a virtual network to secure communications between your clients and the hub or project, you must use an Azure Virtual Network that you create and manage. For example, an Azure Virtual Network that uses a VPN or ExpressRoute connection to your on-premises network.

For more information on how to configure a managed virtual network, see [Configure a managed virtual network for Azure AI Foundry](../how-to/configure-managed-network.md).

## Azure Monitor

Azure monitor and Azure Log Analytics provide monitoring and logging for the underlying resources used by Azure AI Foundry. Since Azure AI Foundry is built on Azure Machine Learning, Azure OpenAI, Azure AI services, and Azure AI Search, use the following articles to learn how to monitor the services:

| Resource | Monitoring and logging |
| --- | --- |
| Azure AI Foundry hub and project | [Monitor Azure Machine Learning](/azure/machine-learning/monitor-azure-machine-learning) |
| Azure OpenAI | [Monitor Azure OpenAI](/azure/ai-services/openai/how-to/monitoring) |
| Azure AI services | [Monitor Azure AI (training)](/training/modules/monitor-ai-services/) |
| Azure AI Search | [Monitor Azure AI Search](/azure/search/monitor-azure-cognitive-search) |

## Price and quota

For more information on price and quota, use the following articles:

- [Plan and manage costs](../how-to/costs-plan-manage.md)
- [Quota management](../how-to/quota.md)

## Next steps

Create a hub using one of the following methods:

- [Azure AI Foundry portal](../how-to/create-azure-ai-resource.md#create-a-hub-in-azure-ai-foundry-portal): Create a hub for getting started.
- [Azure portal](../how-to/create-secure-ai-hub.md): Create a hub with your own networking.
- [Bicep template](../how-to/create-azure-ai-hub-template.md).
