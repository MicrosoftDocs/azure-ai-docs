---
title: 'CLI (v2) feature store YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) feature store YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: reference
author: s-polly
ms.author: scottpolly
ms.reviewer: soumyapatro
ms.date: 09/12/2024
ms.custom: cliv2, build-2023
---

# CLI (v2) feature store YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
|--|--|--|--|--|
| $schema | string | The YAML schema. If you use the Azure Machine Learning VS Code extension to author the YAML file, including $schema at the top of your file enables you to invoke schema and resource completions. |  |  |
| name | string | **Required.** Name of the feature store. |  |  |
| compute_runtime | object | The compute runtime configuration used for materialization job. |  |  |
| compute_runtime.spark_runtime_version | string | The Azure Machine Learning Spark runtime version. | 3.4 | 3.4 |
| offline_store | object |  |  |  |
| offline_store.type | string | **Required** if offline_store is provided. The type of offline store. Only data lake gen2 type of storage is supported. | azure_data_lake_gen2 |  |
| offline_store.target | string | **Required** if offline_store is provided. The datalake Gen2 storage URI in the format of `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default/containers/<container>`. |  |  |
| online_store | object |  |  |  |
| online_store.type | string | **Required** if online_store is provided. The type of online store. Only redis cache is supported. | redis |  |
| online_store.target | string | **Required** if online_store is provided. The Redis Cache URI in the format of `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Cache/Redis/<redis-name>`. |  |  |
| materialization_identity | object | The user-assigned managed identity that used for the materialization job. This identity needs to be granted necessary roles to access Feature Store service, the data source, and the offline storage. |  |  |
| materialization_identity.client_id | string | The client ID for your user-assigned managed identity. |  |  |
| materialization_identity.resource_id | string | The resource ID for your user-assigned managed identity. |  |  |
| materialization_identity.principal_id | string | the principal ID for your user-assigned managed identity.|  |  |
| description | string | Description of the feature store. |  |  |
| tags | object | Dictionary of tags for the feature store. |  |  |
| display_name | string | Display name of the feature store in the studio UI. Can be nonunique within the resource group. |  |  |
| location | string | The location of the feature store. |  | The resource group location. |
| resource_group | string |The resource group containing the feature store. If the resource group doesn't exist, a new one is created. |  |  |

You can include other [workspace properties](reference-yaml-workspace.md).

## Remarks

The `az ml feature-store` command can be used for managing Azure Machine Learning feature store workspaces.
## Examples

Examples are available in the [examples GitHub repository](https://github.com/Azure/azureml-examples/tree/main/cli). Some common examples are shown here:

## YAML basic

```yaml
$schema: http://azureml/sdk-2-0/FeatureStore.json
name: mktg-feature-store
location: eastus
```

## YAML with offline store configuration

```yaml
$schema: http://azureml/sdk-2-0/FeatureStore.json
name: mktg-feature-store

compute_runtime:
    spark_runtime_version: 3.2

offline_store:
    type: azure_data_lake_gen2
    target: /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account_name>/blobServices/default/containers/<container_name>

materialization_identity:
    client_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    resource_id: /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<uai-name>

# Many of workspace parameters will also be supported:
location: eastus
display_name: marketing feature store
tags:
  foo: bar
```

## Configure the online store in the CLI with YAML

```yaml
$schema: http://azureml/sdk-2-0/FeatureStore.json
name: mktg-feature-store

compute_runtime:
  spark_runtime_version: 3.4

online_store:
  type: redis
  target: "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Cache/Redis/<redis-name>"

materialization_identity:
  client_id: 00001111-aaaa-2222-bbbb-3333cccc4444
  principal_id: aaaaaaaa-bbbb-cccc-1111-222222222222
  resource_id: /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<uai-name>

# Many of workspace parameters will also be supported:
location: eastus
display_name: marketing feature store
tags:
  foo: bar
```

## Configure the online store in the CLI with Python

```python
redis_arm_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Cache/Redis/{redis_name}"
online_store = MaterializationStore(type="redis", target=redis_arm_id)
 
fs = FeatureStore(
    name=featurestore_name,
    location=location,
    online_store=online_store,
)
 
# wait for feature store creation
fs_poller = ml_client.feature_stores.begin_create(fs)

# move the feature store to a YAML file

yaml_path = root_dir + "/featurestore/featurestore_with_online.yaml"
fs.dump(yaml_path)

```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
- [Troubleshoot managed feature store](troubleshooting-managed-feature-store.md)
