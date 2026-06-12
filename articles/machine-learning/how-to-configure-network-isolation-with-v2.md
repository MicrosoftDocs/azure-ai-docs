---
title: Network isolation change with the v2 API platform on Azure Resource Manager
titleSuffix: Azure Machine Learning
description: 'Explain network isolation changes with the v2 API platform on Azure Resource Manager and how to maintain network isolation'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.custom: devx-track-arm-template, dev-focus
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: shshubhe
ms.date: 03/19/2026
ai-usage: ai-assisted
---

# Network isolation change with the v2 API platform on Azure Resource Manager

[!INCLUDE [managed-vnet-note](includes/managed-vnet-note.md)]

In this article, you learn about network isolation changes with the v2 API platform on Azure Resource Manager (ARM) and the effect on network isolation.

> [!TIP]
> For new workspaces, consider using [workspace managed virtual network isolation](how-to-managed-network.md), which is the recommended approach for configuring network isolation.
 
## How the v2 API platform uses Azure Resource Manager (ARM)

> [!IMPORTANT]
> The v1 API is deprecated as of March 31, 2025. Support for CLI v1 ended on September 30, 2025. Support for SDK v1 ends on June 30, 2026. We recommend that you transition to the v2 API. For more information, see [Upgrade to v2](how-to-migrate-from-v1.md).

The v2 API routes most operations — including workspace, compute, datastore, job, environment, code, component, and endpoint management — through Azure Resource Manager (ARM). Only a small set of operations communicate directly within the workspace virtual network. This provides a consistent API, easier Azure role-based access control, and Azure Policy support.

The Azure Machine Learning CLI v2 uses the v2 API platform. Features such as [managed online endpoints](concept-endpoints.md) are only available through the v2 API.

In contrast, the deprecated v1 API routed most operations through the workspace, with only workspace and compute CRUD operations going through ARM.

## How the v2 API affects network isolation

Because the v2 API routes most operations through ARM, enabling a private endpoint on your workspace doesn't isolate those operations from public networks. Operations that use ARM communicate over public networks, and include any metadata (such as your resource IDs) or parameters used by the operation. For example, the [parameters](./reference-yaml-job-command.md).

Previously, with the v1 API, most operations used the workspace directly. A private endpoint on the workspace provided network isolation for everything except workspace and compute CRUD operations.

> [!IMPORTANT]
> For most people, using the public ARM communications is OK:
> * Public ARM communications is the standard for management operations with Azure services. For example, creating an Azure Storage Account or Azure Virtual Network uses ARM.
> * The Azure Machine Learning operations do not expose data in your storage account (or other storage in the VNet) on public networks. For example, a training job that runs on a compute cluster in the VNet, and uses data from a storage account in the VNet, would securely access the data directly using the VNet.
> * All communication with public ARM is encrypted using TLS 1.2.

If you need time to evaluate the v2 API before adopting it in your enterprise solutions, or have a company policy that prohibits sending communication over public networks, you can either:

- Use [Azure Private Link for managing Azure resources](/azure/azure-resource-manager/management/create-private-link-access-portal) to keep ARM communications private.
- Enable the *v1_legacy_mode* parameter. When enabled, this parameter disables the v2 API for your workspace.

> [!WARNING]
> Enabling v1_legacy_mode might prevent you from using features provided by the v2 API. For example, some features of Azure Machine Learning studio might be unavailable.

## Scenarios and required actions

To use v2 API features, set `v1_legacy_mode` to __false__. You only need `v1_legacy_mode` set to __true__ if you use a private endpoint with the workspace _and_ have a policy against public ARM communications.

If you don't use a private endpoint, or you're OK with operations communicating with public ARM, no action is needed — `v1_legacy_mode` doesn't affect your workspace.

> [!NOTE]
> For existing workspaces, the flag was automatically set to __true__ for workspaces with a private endpoint, and __false__ for public workspaces. For workspaces created with REST API version `2022-05-01` or newer, the default is __false__.

## How to update v1_legacy_mode parameter

To update v1_legacy_mode, use the following steps:

# [REST API](#tab/restapi)

Use the REST API to update the `v1LegacyMode` property on your workspace. This approach works with any HTTP client and doesn't require deprecated CLI or SDK extensions.

Send a PATCH request to your workspace resource:

```http
PATCH https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.MachineLearningServices/workspaces/{workspace-name}?api-version=2025-04-01
Content-Type: application/json

{
  "properties": {
    "v1LegacyMode": false
  }
}
```

To check the current value, send a GET request:

```http
GET https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.MachineLearningServices/workspaces/{workspace-name}?api-version=2025-04-01
```

In the response, check the `properties.v1LegacyMode` value.

# [Python SDK v1 (deprecated)](#tab/python)

> [!IMPORTANT]
> This code requires the Azure Machine Learning Python SDK v1 (`azureml-core`), which is deprecated. Support ends June 30, 2026. For a supported alternative, use the REST API tab. See [Upgrade to v2](how-to-migrate-from-v1.md).

To disable v1_legacy_mode, use [Workspace.update](/python/api/azureml-core/azureml.core.workspace(class)#update-friendly-name-none--description-none--tags-none--image-build-compute-none--service-managed-resources-settings-none--primary-user-assigned-identity-none--allow-public-access-when-behind-vnet-none-) and set `v1_legacy_mode=false`.

```python
from azureml.core import Workspace

ws = Workspace.from_config()
ws.update(v1_legacy_mode=False)
```

# [Azure CLI v1 (deprecated)](#tab/azurecliextensionv1)

> [!IMPORTANT]
> Support for Azure Machine Learning CLI v1 (`azure-cli-ml`) ended on September 30, 2025. For a supported alternative, use the REST API tab. See [Upgrade to CLI v2](how-to-configure-cli.md).

The Azure CLI [extension v1 for machine learning](./v1/reference-azure-machine-learning-cli.md) provides the [az ml workspace update](/cli/azure/ml(v1)/workspace#az-ml(v1)-workspace-update) command. To disable the parameter for a workspace, add the parameter `--v1-legacy-mode False`.

> [!NOTE]
> The `v1-legacy-mode` parameter requires version 1.41.0 or newer of the `azure-cli-ml` extension. The parameter is __not__ available in the v2 (`ml`) extension.

```azurecli
az ml workspace update -g <myresourcegroup> -w <myworkspace> --v1-legacy-mode False
```

To view the current state of the parameter:
 
```azurecli
az ml workspace show -g <myresourcegroup> -w <myworkspace> --query v1LegacyMode
```

---
    
> [!IMPORTANT]
> Note that it takes about 30 minutes to an hour or more for changing v1_legacy_mode parameter from __true__ to __false__ to be reflected in the workspace. Therefore, if you set the parameter to __false__ but receive an error that the parameter is __true__ in a subsequent operation, please try after a few more minutes.

## Next steps

* [Upgrade to v2](how-to-migrate-from-v1.md).
* [Workspace managed virtual network isolation](how-to-managed-network.md).
* [Use a private endpoint with Azure Machine Learning workspace](how-to-configure-private-link.md).
* [Create private link for managing Azure resources](/azure/azure-resource-manager/management/create-private-link-access-portal).
