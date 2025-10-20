---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 02/10/2025
ms.author: scottpolly
---

When creating an Azure Machine Learning workspace, or a resource used by the workspace, you might get an error that's similar to one of these:

* `No registered resource provider found for location {location}`
* `The subscription is not registered to use namespace {resource-provider-namespace}`

Most resource providers are automatically registered, but not all of them. If you see this message, you need to register a provider.

The following table contains a list of resource providers required by Azure Machine Learning:

| Resource provider | Why it's needed |
| ----- | ----- |
| __Microsoft.MachineLearningServices__ | Creating the Azure Machine Learning workspace. |
| __Microsoft.Storage__ | An Azure Storage account is used as the default storage for the workspace. |
| __Microsoft.ContainerRegistry__ | Azure Container Registry is used by the workspace to build Docker images. |
| __Microsoft.KeyVault__ | Azure Key Vault is used by the workspace to store secrets. |
| __Microsoft.Notebooks__ | An Azure Machine Learning compute instance uses integrated notebooks. |
| __Microsoft.ContainerService__ | You want to deploy trained models to Azure Kubernetes Services. |

If you want to use a customer-managed key with Azure Machine Learning, you must register the following service providers:

| Resource provider | Why it's needed |
| ----- | ----- |
| __Microsoft.DocumentDB__ | An Azure Cosmos DB instance logs metadata for the workspace. |
| __Microsoft.Search__ | Azure Search provides indexing capabilities for the workspace. |

If you want to use a managed virtual network with Azure Machine Learning, you must register the __Microsoft.Network__ resource provider. This resource provider is used by the workspace when private endpoints for the managed virtual network are created.

For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).
