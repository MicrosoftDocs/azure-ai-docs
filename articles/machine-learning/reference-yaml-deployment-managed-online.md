---
title: 'CLI (v2) managed online deployment YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) managed online deployment YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: reference
ms.custom: cliv2, build-2023, update-code
author: msakande
ms.author: mopeakande
ms.date: 10/19/2023
ms.reviewer: sehan
---

# CLI (v2) managed online deployment YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

The source JSON schema can be found at https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json.

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `$schema` | string | The YAML schema. If you use the Azure Machine Learning VS Code extension to author the YAML file, including `$schema` at the top of your file enables you to invoke schema and resource completions. | | |
| `name` | string | **Required.** Name of the deployment. <br><br> Naming rules are defined [here](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).| | |
| `description` | string | Description of the deployment. | | |
| `tags` | object | Dictionary of tags for the deployment. | | |
| `endpoint_name` | string | **Required.** Name of the endpoint to create the deployment under. | | |
| `model` | string or object | The model to use for the deployment. This value can be either a reference to an existing versioned model in the workspace or an inline model specification. <br><br> To reference an existing model, use the `azureml:<model-name>:<model-version>` syntax. <br><br> To define a model inline, follow the [Model schema](reference-yaml-model.md#yaml-syntax). <br><br> As a best practice for production scenarios, you should create the model separately and reference it here. <br><br> This field is optional for [custom container deployment](how-to-deploy-custom-container.md) scenarios.| | |
| `model_mount_path` | string | The path to mount the model in a custom container. Applicable only for [custom container deployment](how-to-deploy-custom-container.md) scenarios. If the `model` field is specified, it's mounted on this path in the container. | | |
| `code_configuration` | object | Configuration for the scoring code logic. <br><br> This field is optional for [custom container deployment](how-to-deploy-custom-container.md) scenarios. | | |
| `code_configuration.code` | string | Local path to the source code directory for scoring the model. | | |
| `code_configuration.scoring_script` | string | Relative path to the scoring file in the source code directory. | | |
| `environment_variables` | object | Dictionary of environment variable key-value pairs to set in the deployment container. You can access these environment variables from your scoring scripts. | | |
| `environment` | string or object | **Required.** The environment to use for the deployment. This value can be either a reference to an existing versioned environment in the workspace or an inline environment specification. <br><br> To reference an existing environment, use the `azureml:<environment-name>:<environment-version>` syntax. <br><br> To define an environment inline, follow the [Environment schema](reference-yaml-environment.md#yaml-syntax). <br><br> As a best practice for production scenarios, you should create the environment separately and reference it here. | | |
| `instance_type` | string | **Required.** The VM size to use for the deployment. For the list of supported sizes, see [Managed online endpoints SKU list](reference-managed-online-endpoints-vm-sku-list.md). | | |
| `instance_count` | integer | **Required.** The number of instances to use for the deployment. Specify the value based on the workload you expect. For high availability, Microsoft recommends you set it to at least `3`. <br><br> `instance_count` can be updated after deployment creation using `az ml online-deployment update` command. <br><br> We reserve an extra 20% for performing upgrades. For more information, see [virtual machine quota allocation for deployment](how-to-manage-quotas.md#virtual-machine-quota-allocation-for-deployment). | | |
| `app_insights_enabled` | boolean | Whether to enable integration with the Azure Application Insights instance associated with your workspace. | | `false` |
| `scale_settings` | object | The scale settings for the deployment. Currently only the `default` scale type is supported, so you don't need to specify this property. <br><br> With this `default` scale type, you can either manually scale the instance count up and down after deployment creation by updating the `instance_count` property, or create an [autoscaling policy](how-to-autoscale-endpoints.md). | | |
| `scale_settings.type` | string | The scale type. | `default` | `default` |
| `data_collector` | object | Data collection settings for the deployment. See [DataCollector](#datacollector) for the set of configurable properties. | | |
| `request_settings` | object | Scoring request settings for the deployment. See [RequestSettings](#requestsettings) for the set of configurable properties. | | |
| `liveness_probe` | object | Liveness probe settings for monitoring the health of the container regularly. See [ProbeSettings](#probesettings) for the set of configurable properties. | | |
| `readiness_probe` | object | Readiness probe settings for validating if the container is ready to serve traffic. See [ProbeSettings](#probesettings) for the set of configurable properties. | | |
| `egress_public_network_access` | string |**Note:** This key is applicable when you use the [legacy network isolation method](concept-secure-online-endpoint.md#secure-outbound-access-with-legacy-network-isolation-method) to secure outbound communication for a deployment. We strongly recommend that you secure outbound communication for deployments using [a workspace managed VNet](concept-secure-online-endpoint.md) instead. <br><br>This flag secures the deployment by restricting communication between the deployment and the Azure resources used by it. Set to `disabled` to ensure that the download of the model, code, and images needed by your deployment are secured with a private endpoint. This flag is applicable only for managed online endpoints. | `enabled`, `disabled` | `enabled` |

### RequestSettings

| Key | Type | Description | Default value |
| --- | ---- | ----------- | ------------- |
| `request_timeout_ms` | integer | The scoring timeout in milliseconds. Note that the maximum value allowed is `180000` milliseconds. See [limits for online endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints) for more. | `5000` |
| `max_concurrent_requests_per_instance` | integer | The maximum number of concurrent requests per instance allowed for the deployment. <br><br> **Note:** If you're using [Azure Machine Learning Inference Server](how-to-inference-server-http.md) or [Azure Machine Learning Inference Images](concept-prebuilt-docker-images-inference.md), your model must be configured to handle concurrent requests. To do so, pass `WORKER_COUNT: <int>` as an environment variable. For more information about `WORKER_COUNT`, see [Azure Machine Learning Inference Server Parameters](how-to-inference-server-http.md#review-inference-server-parameters) <br><br> **Note:** Set to the number of requests that your model can process concurrently on a single node. Setting this value higher than your model's actual concurrency can lead to higher latencies. Setting this value too low might lead to under utilized nodes. Setting too low might also result in requests being rejected with a 429 HTTP status code, as the system will opt to fail fast. For more information, see [Troubleshooting online endpoints: HTTP status codes](how-to-troubleshoot-online-endpoints.md#http-status-codes). | `1` |
| `max_queue_wait_ms` | integer | (Deprecated) The maximum amount of time in milliseconds a request will stay in the queue. (Now increase `request_timeout_ms` to account for any networking/queue delays) | `500` |

### ProbeSettings

| Key | Type | Description | Default value |
| --- | ---- | ----------- | ------------- |
| `initial_delay` | integer | The number of seconds after the container has started before the probe is initiated. Minimum value is `1`. | `10` |
| `period` | integer | How often (in seconds) to perform the probe. | `10` |
| `timeout` | integer | The number of seconds after which the probe times out. Minimum value is `1`. | `2` |
| `success_threshold` | integer | The minimum consecutive successes for the probe to be considered successful after having failed. Minimum value is `1` for readiness probe. The value for liveness probe is fixed as `1`. | `1` |
| `failure_threshold` | integer | When a probe fails, the system will try `failure_threshold` times before giving up. Giving up in the case of a liveness probe means the container will be restarted. In the case of a readiness probe the container will be marked Unready. Minimum value is `1`. | `30` |

### DataCollector

| Key | Type | Description | Default value |
| --- | ---- | ----------- | ------------- |
| `sampling_rate` | float | The percentage, represented as a decimal rate, of data to collect. For instance, a value of 1.0 represents collecting 100% of data. | `1.0` |
| `rolling_rate` | string | The rate to partition the data in storage. Value can be: Minute, Hour, Day, Month, Year. | `Hour` |
| `collections` | object | Set of individual `collection_name`s and their respective settings for this deployment. | |
| `collections.<collection_name>` | object | Logical grouping of production inference data to collect (example: `model_inputs`). There are two reserved names: `request` and `response`, which respectively correspond to HTTP request and response payload data collection. All other names are arbitrary and definable by the user. <br><br> **Note**: Each `collection_name` should correspond to the name of the `Collector` object used in the deployment `score.py` to collect the production inference data. For more information on payload data collection and data collection with the provided Python SDK, see [Collect data from models in production](how-to-collect-production-data.md). | |
| `collections.<collection_name>.enabled` | boolean | Whether to enable data collection for the specified `collection_name`. | `'False''` |
| `collections.<collection_name>.data.name` | string | The name of the data asset to register with the collected data. | `<endpoint>-<deployment>-<collection_name>` |
| `collections.<collection_name>.data.path` | string | The full Azure Machine Learning datastore path where the collected data should be registered as a data asset. | `azureml://datastores/workspaceblobstore/paths/modelDataCollector/<endpoint_name>/<deployment_name>/<collection_name>` |
| `collections.<collection_name>.data.version` | integer | The version of the data asset to be registered with the collected data in Blob storage. | `1` |

## Remarks

The `az ml online-deployment` commands can be used for managing Azure Machine Learning managed online deployments.

## Examples

Examples are available in the [examples GitHub repository](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online). Several are shown below.

## YAML: basic

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/sample/blue-deployment.yml":::

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/sample/green-deployment.yml":::

## YAML: system-assigned identity

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/managed-identities/2-sai-deployment.yml":::

## YAML: user-assigned identity

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/managed-identities/2-uai-deployment.yml":::

## YAML: data_collector

```yml
$schema: http://azureml/sdk-2-0/OnlineDeployment.json

endpoint_name: my_endpoint 
name: blue 
model: azureml:my-model-m1:1 
environment: azureml:env-m1:1 
data_collector:
   collections:
       model_inputs:
           enabled: 'True' 
       model_outputs:
           enabled: 'True'
```

```yml
$schema: http://azureml/sdk-2-0/OnlineDeployment.json

endpoint_name: my_endpoint
name: blue 
model: azureml:my-model-m1:1 
environment: azureml:env-m1:1 
data_collector:
   collections:
     request: 
         enabled: 'True'
         data: 
           name: my_request_data_asset 
           path: azureml://datastores/workspaceblobstore/paths/modelDataCollector/my_endpoint/blue/request 
           version: 1 
     response:
         enabled: 'True' 
         data: 
           name: my_response_data_asset
           path: azureml://datastores/workspaceblobstore/paths/modelDataCollector/my_endpoint/blue/response
           version: 1 
     model_inputs:
         enabled: 'True'
         data: 
           name: my_model_inputs_data_asset
           path: azureml://datastores/workspaceblobstore/paths/modelDataCollector/my_endpoint/blue/model_inputs
           version: 1 
     model_outputs:
         enabled: 'True'
         data: 
           name: my_model_outputs_data_asset
           path: azureml://datastores/workspaceblobstore/paths/modelDataCollector/my_endpoint/blue/model_outputs
           version: 1
```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
