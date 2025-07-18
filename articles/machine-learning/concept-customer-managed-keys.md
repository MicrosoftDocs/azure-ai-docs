---
title: Customer-managed keys
titleSuffix: Azure Machine Learning
description: 'Learn about using customer-managed keys to improve data security with Azure Machine Learning.'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: concept-article
ms.author: scottpolly
author: s-polly
ms.reviewer: deeikele
ms.date: 01/28/2025
ms.custom: engagement-fy23, build-2024
monikerRange: 'azureml-api-2 || azureml-api-1'
---
# Customer-managed keys for Azure Machine Learning

Azure Machine Learning is built on top of multiple Azure services. Although the stored data is encrypted through encryption keys that Microsoft provides, you can enhance security by also providing your own (customer-managed) keys. The keys that you provide are stored in Azure Key Vault. Your data can be stored on a set of other resources that you manage in your Azure subscription, or [service-side on Microsoft managed resources](#service-side-encryption-of-metadata).

In addition to customer-managed keys (CMK), Azure Machine Learning provides an [high business impact configuration](/python/api/azure-ai-ml/azure.ai.ml.entities.workspace) for highly sensitive data workloads. Enabling this configuration reduces the amount of data that Microsoft collects for diagnostic purposes and enables [extra encryption in Microsoft-managed environments](/azure/security/fundamentals/encryption-atrest). 

## Prerequisites

* An Azure subscription.
* An Azure Key Vault instance. The key vault contains the keys for encrypting your services.

The key vault must enable soft delete and purge protection. The managed identity for the services that you help secure by using a customer-managed key must have the following permissions to the key vault:

* Wrap Key
* Unwrap Key
* Get

For example, the managed identity for Azure Cosmos DB would need to have those permissions to the key vault.

## Limitations

* After workspace creation, the customer-managed encryption key for resources that the workspace depends on can only be updated to another key in the original Azure Key Vault resource.
* Unless you are using the [service-side](#service-side-encryption-of-metadata), the encrypted data is stored on resources in a Microsoft-managed resource group in your subscription. You can't create these resources up front or transfer ownership of them to you. The data lifecycle is managed indirectly via the Azure Machine Learning APIs as you create objects in the Azure Machine Learning service.
* If you are using the [service-side](#service-side-encryption-of-metadata), Azure charges will continue to accrue during the soft delete retention period.
* You can't delete Microsoft-managed resources that you use for customer-managed keys without also deleting your workspace.
* You can't encrypt the compute cluster's OS disk by using your customer-managed keys. You must use Microsoft-managed keys.

> [!WARNING]
> Don't delete the resource group that contains the Azure Cosmos DB instance, or any of the resources that are automatically created in this group. If you need to delete the resource group or Microsoft-managed services in it, you must delete the Azure Machine Learning workspace that uses it. The resource group's resources are deleted when you delete the associated workspace.

## Customer-managed keys

When you *don't* use a customer-managed key, Microsoft creates and manages resources in a Microsoft-owned Azure subscription and uses a Microsoft-managed key to encrypt the data.

When you use a customer-managed key, there are two possible configurations:

- [Service-side encryption](#service-side-encryption-of-metadata): The resources are stored service-side on Microsoft-managed resources. This configuration reduces costs and also reduces the chance of conflict with policies you may have set for your Azure subscription.
- [Subscription-side encryption (classic)](#subscription-side-encryption-of-metadata-classic): The resources are hosted in your Azure subscription and encrypted with your key. While these resources exist in your subscription, Microsoft manages them. These resources are automatically created and configured when you create your Azure Machine Learning workspace.

## Service-side encryption of metadata

In this configuration, encrypted data is stored service-side on Microsoft-managed resources instead of in your subscription. Using service-side encryption reduces costs compared to the subscription-side encryption, and mitigates the likelihood of Azure policy conflicts.

Data is stored in multitenant Microsoft-managed resources with document-level encryption using your encryption key. Search indices are stored on Microsoft-managed resources that are provisioned dedicated for you per workspace. The cost of the Azure AI search instance is charged under your Azure Machine Learning workspace in Microsoft Cost Management.

Pipelines metadata is stored on the storage account in your subscription that is associated to the Azure Machine Learning workspace. Since this Azure Storage resource is managed separately in your subscription, you're responsible to configure encryption settings on it.


:::image type="content" source="./media/concept-customer-managed-keys/cmk-service-side-encryption.png" alt-text="Screenshot of the encryption tab with the option for server side encryption selected." lightbox="./media/concept-customer-managed-keys/cmk-service-side-encryption.png":::

> [!NOTE]
> - When you use service-side encryption, Azure charges will continue to accrue during the soft delete retention period.

For templates that create a workspace with service-side encryption of metadata, see 

- [Bicep template for creating default workspace](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-cmk-service-side-encryption).
- [Bicep template for creating hub workspace](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aistudio-cmk-service-side-encryption).

### Subscription-side encryption of metadata (classic)

When you bring your own encryption key, service metadata is stored on dedicated resources in your Azure subscription. Microsoft creates a separate resource group in your subscription for this purpose: *azureml-rg-workspacename_GUID*. Only Microsoft can modify the resources in this managed resource group. 

If your Azure Machine Learning workspace uses a private endpoint, this resource group also contains a Microsoft-managed Azure virtual network. This virtual network helps secure communication between the managed services and the workspace. You *can't provide your own virtual network* for use with the Microsoft-managed resources. You also *can't modify the virtual network*. For example, you can't change the IP address range that it uses.

Microsoft creates the following resources to store metadata for your workspace:

| Service | Usage | Example data |
| ----- | ----- | ----- |
| Azure Cosmos DB | Stores job history data, compute metadata, and asset metadata. | Data can include job name, status, sequence number, and status; compute cluster name, number of cores, and number of nodes; datastore names and tags, and descriptions on assets like models; and data label names. |
| Azure AI Search | Stores indexes that help with querying your machine learning content. | These indexes are built on top of the data stored in Azure Cosmos DB. |
| Azure Storage | Stores metadata related to Azure Machine Learning pipeline data. | Data can include designer pipeline names, pipeline layout, and execution properties. |

> [!TIP]
> The [Request Units](/azure/cosmos-db/request-units) for Azure Cosmos DB automatically scale as needed.

> [!IMPORTANT]
> If your subscription doesn't have enough quota for these services, a failure will occur.
>
> When you use a customer-managed key, the costs for your subscription are higher because these resources are in your subscription. To estimate the cost, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

From the perspective of data lifecycle management, data in the preceding resources is created and deleted as you create and delete corresponding objects in Azure Machine Learning.

Your Azure Machine Learning workspace reads and writes data by using its managed identity. This identity is granted access to the resources through a role assignment (Azure role-based access control) on the data resources. The encryption key that you provide is used to encrypt data that stored on Microsoft-managed resources. At runtime, the key is also used to create indexes for Azure AI Search.

Extra networking controls are configured when you create a private link endpoint on your workspace to allow for inbound connectivity. This configuration includes the creation of a private link endpoint connection to the Azure Cosmos DB instance. Network access is restricted to only trusted Microsoft services.

## Encryption of data on compute resources 

Azure Machine Learning uses compute resources to train and deploy machine learning models. The following table describes the compute options and how each one encrypts data:

:::moniker range="azureml-api-1"
| Compute | Encryption |
| ----- | ----- |
| Azure Container Instances | Data is encrypted with a Microsoft-managed key or a customer-managed key. </br>For more information, see [Encrypt deployment data](/azure/container-instances/container-instances-encrypt-data). |
| Azure Kubernetes Service | Data is encrypted with a Microsoft-managed key or a customer-managed key. </br>For more information, see [Bring your own keys with Azure disks in Azure Kubernetes Service](/azure/aks/azure-disk-customer-managed-keys). |
| Azure Machine Learning compute instance | The local scratch disk is encrypted if you enable the `hbi_workspace` flag for the workspace. |
| Azure Machine Learning compute cluster | The OS disk is encrypted in Azure Storage with Microsoft-managed keys. The temporary disk is encrypted if you enable the `hbi_workspace` flag for the workspace. |
:::moniker-end
:::moniker range="azureml-api-2"
| Compute | Encryption |
| ----- | ----- |
| Azure Kubernetes Service | Data is encrypted with a Microsoft-managed key or a customer-managed key. </br>For more information, see [Bring your own keys with Azure disks in Azure Kubernetes Service](/azure/aks/azure-disk-customer-managed-keys). |
| Azure Machine Learning compute instance | The local scratch disk is encrypted if you enable the `hbi_workspace` flag for the workspace. |
| Azure Machine Learning compute cluster | The OS disk is encrypted in Azure Storage with Microsoft-managed keys. The temporary disk is encrypted if you enable the `hbi_workspace` flag for the workspace. |
:::moniker-end

### Compute cluster

Compute clusters have local OS disk storage and can mount data from storage accounts in your subscription during a job. When you're mounting data from your own storage account in a job, you can enable customer-managed keys on those storage accounts for encryption.

The OS disk for each compute node is stored in Azure Storage, and is always encrypted with Microsoft-managed keys in Azure Machine Learning storage accounts, and not with customer-managed keys. This compute target is ephemeral, so data stored on the OS disk is deleted after the cluster scales down. Clusters typically scale down when no jobs are queued, autoscaling is on, and the minimum node count is set to zero. The underlying virtual machine is deprovisioned, and the OS disk is deleted.

Azure Disk Encryption isn't supported for the OS disk. Each virtual machine also has a local temporary disk for OS operations. If you want, you can use the disk to stage training data. If you create the workspace with the `hbi_workspace` parameter set to `TRUE`, the temporary disk is encrypted. This environment is short lived (only during your job), and encryption support is limited to system-managed keys only.

### Compute instance

The OS disk for a compute instance is encrypted with Microsoft-managed keys in Azure Machine Learning storage accounts. If you create the workspace with the `hbi_workspace` parameter set to `TRUE`, the local temporary disk on the compute instance is encrypted with Microsoft-managed keys. Customer-managed key encryption isn't supported for OS and temporary disks.
  
## High business impact (HBI) configuration

In standard workspace configurations, Azure Machine Learning collects diagnostic information for performance monitoring and improvement, as well as the troubleshooting of your compute clusters. For example, when two jobs are run on the same compute cluster using the same docker image, then the same image will be reusable between jobs without having to be rebuild or pulled twice reducing job start times.

When handling highly sensitive data workloads, you may opt-out from the above behavior by setting the `hbi` flag on your workspace. This flag enables the following behaviors:
* It reduces the amount of data that Microsoft collects for diagnostic purposes from your compute clusters and enables [extra encryption in Microsoft-managed environments](/azure/security/fundamentals/encryption-atrest). 
* Starts encrypting the local scratch disk in your Azure Machine Learning compute cluster. This behavior is only enforced if you didn't create any previous clusters in that subscription. Otherwise, you are required to raise a support ticket to enable encryption of the scratch disk for your compute clusters.
* Cleans up your local scratch disk between jobs. For example, this cleans up cached docker images and may affect job startup speed.
* Passes credentials for your storage account, container registry, and Secure Shell (SSH) account from the execution layer to your compute clusters by using your Azure key vault.

Note that `hbi_workspace` flag doesn't affect encryption in transit. It affects only encryption at rest.

You can set the `hbi_workspace` flag only when you create a workspace. You can't change it for an existing workspace.

When you set this flag to `TRUE`, it might increase the difficulty of troubleshooting problems because less telemetry data is sent to Microsoft. There's less visibility into success rates or problem types. Microsoft might not be able to react as proactively when this flag is `TRUE`.

To enable the `hbi_workspace` flag when you're creating an Azure Machine Learning workspace, follow the steps in one of the following articles:

* [Create and manage a workspace by using the Azure portal or the Python SDK](how-to-manage-workspace.md)
* [Create and manage a workspace by using the Azure CLI](how-to-manage-workspace-cli.md)
* [Create a workspace by using HashiCorp Terraform](how-to-manage-workspace-terraform.md)
* [Create a workspace by using Azure Resource Manager templates](how-to-create-workspace-template.md)

## Next steps

* [Configure customer-managed keys with Azure Machine Learning](how-to-setup-customer-managed-keys.md)
