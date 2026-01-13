---
title: Administer data authentication
titleSuffix: Azure Machine Learning
description: Learn how to manage data access and how to handle authentication operations in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: shshubhe
ms.date: 09/06/2024
ms.custom: engagement-fy23

# Customer intent: As an administrator, I need to administer data access and set up authentication methods for data scientists.
---

# Data administration

Learn how to manage data access and how to authenticate in Azure Machine Learning.
[!INCLUDE [sdk/cli v2](includes/machine-learning-dev-v2.md)]

> [!IMPORTANT]
> This article is intended for Azure administrators who want to create the required infrastructure for an Azure Machine Learning solution.

## Credential-based data authentication

In general, credential-based data authentication involves these checks:
* Check that the user who accesses data from the credential-based datastore has an assigned role with role-based access control (RBAC) that contains `Microsoft.MachineLearningServices/workspaces/datastores/listsecrets/action`

    - This permission is required to retrieve credentials from the datastore for the user.
    - Built-in roles that already contain this permission:
    
      - [Contributor](/azure/role-based-access-control/built-in-roles/general#contributor)
      - Azure AI Developer
      - [Azure Machine Learning Data Scientist](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azureml-data-scientist)
      - Alternatively, if a custom role is applied, this permission must be added to that custom role
    
    - You must know *which* specific user wants to access the data. A specific user can be a real user with a user identity. It can also be a computer with compute managed identity (MSI). For more information, visit the [Scenarios and authentication options](#scenarios-and-authentication-options) section to determine the identity that needs the added permission.

* Does the stored credential (service principal, account key, or shared access signature token) have access to the data resource?

## Identity-based data authentication

In general, identity-based data authentication involves these checks:

* Which user wants to access the resources?
    - Different types of authentication are available, depending on the context at the time the data is accessed. For example:
      -  User identity
      -  Compute managed identity
      -  Workspace managed identity
    - Jobs, including the dataset `Generate Profile` option, run on a compute resource in *your subscription*, and access the data from that location. The compute managed identity needs permission to access the storage resource, instead of the identity of the user who submitted the job.
    - For authentication based on a user identity, you must know *which* specific user tried to access the storage resource. For more information about *user* authentication, visit [Authentication for Azure Machine Learning](how-to-setup-authentication.md). For more information about service-level authentication, visit [Authentication between Azure Machine Learning and other services](how-to-identity-based-service-authentication.md).
* Does this user have read permission for the resource?
    - Does the user identity or the compute managed identity have the necessary permissions for that storage resource? Permissions are granted by using Azure RBAC.
    - The storage account [Reader](/azure/role-based-access-control/built-in-roles#reader) reads the storage metadata.
    - The [Storage Blob Data Reader](/azure/role-based-access-control/built-in-roles#storage-blob-data-reader) reads and lists storage containers and blobs.
    - The [Storage File Data Privileged Reader](/azure/role-based-access-control/built-in-roles#storage-file-data-privileged-reader) reaeds and lists files and directories in Azure file shares.
    - For more information, visit [Azure built-in roles for storage](/azure/role-based-access-control/built-in-roles/storage).
* Does this user have write permission for the resource?
    - Does the user identity or the compute managed identity have the necessary permissions for that storage resource? Permissions are granted by using Azure RBAC.
    - The storage account [Reader](/azure/role-based-access-control/built-in-roles#reader) reads the storage metadata.
    - The [Storage Blob Data Contributor](/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor) reads, writes, and deletes Azure Storage containers and blobs.
    - The [Storage File Data Privileged Contributor](/azure/role-based-access-control/built-in-roles#storage-file-data-privileged-contributor) reads, writes, deletes, and modifies access control lists on files and directories in Azure file shares.
    - For more information, visit [Azure built-in roles for storage](/azure/role-based-access-control/built-in-roles/storage).

## Other general checks for authentication

* What exactly will access the resource?
    - **User**: Is the client IP address in the virtual network/subnet range?
    - **Workspace**: Is the workspace public, or does it have a private endpoint in a virtual network/subnet?
    - **Storage**: Does the storage allow public access, or does it restrict access through a service endpoint or a private endpoint?
* What is the planned operation?
    - Azure Machine Learning handles
      - **C**reate
      - **R**ead
      - **U**pdate
      - **D**elete
    (CRUD) operations on a data store/dataset.
    - Archive operations on data assets in Azure Machine Learning studio require this RBAC operation: `Microsoft.MachineLearningServices/workspaces/datasets/registered/delete`
    - Data access calls (for example, preview or schema) go to the underlying storage and require extra permissions.
* Will this operation run in an Azure subscription compute resources, or resources hosted in a Microsoft subscription?
    - All calls to dataset and datastore services (except the `Generate Profile` option) use resources hosted in a *Microsoft subscription* to run the operations.
    - Jobs, including the dataset `Generate Profile` option, run on a compute resource in *your subscription* and access the data from that location. The compute identity needs permission to the storage resource, instead of the identity of the user who submitted the job.

This diagram shows the general flow of a data access call. Here, a user tries to make a data access call through a Machine Learning workspace, without use of a compute resource.

:::image type="content" source="./media/how-to-administrate-data-authentication/data-access-flow.svg" alt-text="Diagram that shows the logic flow when accessing data.":::

## Scenarios and authentication options

This table lists the identities to use for specific scenarios:

| Configuration | SDK local/notebook virtual machine | Job | Dataset Preview | Datastore browse |
| -- | -- | -- | -- | -- |
| Credential + Workspace MSI | Credential | Credential | Workspace MSI | Credential (only account key and shared access signature token) |
| No Credential + Workspace MSI | Compute MSI/User identity | Compute MSI/User identity | Workspace MSI | User identity |
| Credential + No Workspace MSI | Credential | Credential | Credential (not supported for Dataset Preview under private network) | Credential (only account key and shared access signature token) |
| No Credential + No Workspace MSI | Compute MSI/User identity | Compute MSI/User identity | User identity | User identity |

For SDK V1, data authentication in a job always uses compute MSI. For SDK V2, data authentication in a job depends on your job setting. It can be user identity or compute MSI, based on that job setting.

> [!TIP]
> To access data from outside Machine Learning - for example, with Azure Storage Explorer - that access probably relies on the *user* identity. For specific information, review the documentation for the tool or service you plan to use. For more information about how Machine Learning works with data, visit [Set up authentication between Azure Machine Learning and other services](how-to-identity-based-service-authentication.md).

## Virtual network specific requirements

This information helps you set up data authentication from a Machine Learning workspace, to access data behind a virtual network.

### Add permissions of a storage account to a Machine Learning workspace managed identity

When you use a storage account from the studio, if you want to see Dataset Preview, you must enable **Use workspace managed identity for data preview and profiling in Azure Machine Learning studio** in the datastore setting. Then add these storage account Azure RBAC roles to the workspace managed identity:

* [Blob Data Reader](/azure/role-based-access-control/built-in-roles#storage-blob-data-reader)
* If the storage account uses a private endpoint to connect to the virtual network, you must grant the [Reader](/azure/role-based-access-control/built-in-roles#reader) role for the storage account private endpoint to the managed identity.

For more information, visit [Use Azure Machine Learning studio in an Azure virtual network](how-to-enable-studio-virtual-network.md).

These sections explain the limitations of using a storage account, with your workspace, in a virtual network.

### Secure communication with a storage account

To secure communication between Machine Learning and storage accounts, configure the storage to [grant access to trusted Azure services](/azure/storage/common/storage-network-security#grant-access-to-trusted-azure-services).

### Azure Storage firewall

For a storage account located behind a virtual network, the storage firewall can normally allow your client to directly connect over the internet. However, when you use the studio, your client doesn't connect to the storage account. The Machine Learning service that makes the request connects to the storage account. The IP address of the service isn't documented, and it changes frequently. Enabling the storage firewall doesn't allow the studio to access the storage account in a virtual network configuration.

### Azure Storage endpoint type

When the workspace uses a private endpoint, and the storage account is also in the virtual network, extra validation requirements arise when you use the studio.

* If the storage account uses a *service endpoint*, the workspace private endpoint and storage service endpoint must be located in the same subnet of the virtual network.
* If the storage account uses a *private endpoint*, the workspace private endpoint and storage private endpoint must be in located in the same virtual network. In this case, they can be in different subnets.

## Azure Data Lake Storage Gen1

When you use Azure Data Lake Storage Gen1 as a datastore, you can only use POSIX-style access control lists. You can assign the workspace's managed identity access to resources, like any other security principal. For more information, visit [Access control in Azure Data Lake Storage Gen1](/azure/data-lake-store/data-lake-store-access-control).

## Azure Data Lake Storage Gen2

When you use Azure Data Lake Storage Gen2 as a datastore, you can use both Azure RBAC and POSIX-style access control lists (ACLs) to control data access inside a virtual network.

- **To use Azure RBAC**: Follow the steps described in [Datastore: Azure Storage account](how-to-enable-studio-virtual-network.md#datastore-azure-storage-account). Data Lake Storage Gen2 is based on Azure Storage, so the same steps apply when you use Azure RBAC.
- **To use ACLs**: The managed identity of the workspace can be assigned access like any other security principal. For more information, visit [Access control lists on files and directories](/azure/storage/blobs/data-lake-storage-access-control#access-control-lists-on-files-and-directories).

## Next steps

For information about how to enable the studio in a network, see [Use Azure Machine Learning studio in an Azure virtual network](how-to-enable-studio-virtual-network.md).
