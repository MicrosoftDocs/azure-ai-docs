---
title: 'CLI (v2) deployment template YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) deployment template YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: reference
ms.custom: cliv2, update-code
author: s-polly
ms.author: scottpolly
ms.date: 01/12/2026
ms.reviewer: sehan
ai-usage: ai-assisted
---

# CLI (v2) deployment template YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

The source JSON schema can be found at https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json.

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `$schema` | string | The YAML schema. If you use the Azure Machine Learning VS Code extension to author the YAML file, including `$schema` at the top of your file enables you to invoke schema and resource completions. | | |
| `name` | string | **Required.** Name of the deployment template. | | |
| `version` | string or integer | Version of the deployment template. | | |
| `description` | string | Description of the deployment template. | | |
| `tags` | object | Dictionary of tags for the deployment template. | | |
| `type` | string | Type of the deployment template. | | |
| `deployment_template_type` | string | The deployment template type. | | |
| `environment` | string or object | The environment to use for the deployment template. This value can be either a reference to an existing versioned environment in a registry, or an inline environment specification. <br><br> To reference an existing environment in a registry, use the `azureml://registries/<registry-name>/environments/<environment-name>` syntax. <br><br> To define an environment inline, follow the [Environment schema](reference-yaml-environment.md#yaml-syntax). <br><br> As a best practice for production scenarios, you should create the environment separately and reference it here. | | |
| `environment_variables` | object | Dictionary of environment variable key-value pairs to set for the deployment. You can access these environment variables from your scoring scripts. | | |
| `instance_count` | integer | The number of instances to use for the deployment. Specify the value based on the workload you expect. | | |
| `default_instance_type` | string | The default instance type to use when deploying with this template. | | |
| `allowed_instance_types` | string | The allowed instance type that can be used when deploying with this template. | | |
| `model_mount_path` | string | The path to mount the model in the container. | | |
| `scoring_path` | string | The path for the scoring endpoint. | | |
| `scoring_port` | integer | The port for the scoring endpoint. | | |
| `liveness_probe` | object | Liveness probe settings for monitoring the health of the container regularly. See [ProbeSettings](#probesettings) for the set of configurable properties. | | |
| `readiness_probe` | object | Readiness probe settings for validating if the container is ready to serve traffic. See [ProbeSettings](#probesettings) for the set of configurable properties. | | |
| `request_settings` | object | Request settings for the deployment. See [RequestSettings](#requestsettings) for the set of configurable properties. | | |

### ProbeSettings

| Key | Type | Description | Default value |
| --- | ---- | ----------- | ------------- |
| `failure_threshold` | integer | When a probe fails, the system tries `failure_threshold` times before giving up. Giving up in the case of a liveness probe means the container is restarted. In the case of a readiness probe, the container is marked Unready. Minimum value is `1`. | `30` |
| `initial_delay` | integer | The number of seconds after the container has started before the probe is initiated. Minimum value is `1`. | `10` |
| `method` | string | The HTTP method to use for the probe. | |
| `path` | string | The path for the probe. | |
| `period` | integer | How often (in seconds) to perform the probe. | `10` |
| `port` | integer | The port to probe. | |
| `scheme` | string | The scheme to use for the probe (for example, HTTP or HTTPS). | |
| `success_threshold` | integer | The minimum consecutive successes for the probe to be considered successful after having failed. Minimum value is `1`. | `1` |
| `timeout` | integer | The number of seconds after which the probe times out. Minimum value is `1`. | `2` |

### RequestSettings

| Key | Type | Description | Default value |
| --- | ---- | ----------- | ------------- |
| `request_timeout_ms` | integer | The request timeout in milliseconds. | `5000` |
| `max_concurrent_requests_per_instance` | integer | The maximum number of concurrent requests per instance allowed for the deployment. | `1` |

## Remarks

Deployment templates provide a reusable configuration for deploying models. They define the environment, infrastructure settings, and probe configurations that can be applied when creating deployments.

## Examples

Examples are shown below.

## YAML: basic

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template
version: 1
description: Basic deployment template example
environment: azureml:my-environment:1
instance_count: 1
default_instance_type: Standard_DS3_v2
```

## YAML: with environment variables and probes

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template
version: 1
description: Deployment template with environment variables and health probes
environment: azureml://registries/azureml/environments/minimal-ubuntu20.04-py38-cpu-inference:latest
environment_variables:
  MODEL_PATH: /var/azureml-app/model
  SCORING_TIMEOUT: "60"
instance_count: 3
default_instance_type: Standard_DS3_v2
scoring_path: /score
scoring_port: 8080
liveness_probe:
  initial_delay: 30
  period: 10
  timeout: 2
  success_threshold: 1
  failure_threshold: 3
readiness_probe:
  initial_delay: 10
  period: 5
  timeout: 2
  success_threshold: 1
  failure_threshold: 3
request_settings:
  request_timeout_ms: 10000
  max_concurrent_requests_per_instance: 2
```

## YAML: with allowed instance type

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template-restricted
version: 1
description: Deployment template with instance type restrictions
environment: azureml:my-environment:1
instance_count: 1
default_instance_type: Standard_DS3_v2
allowed_instance_types: Standard_DS3_v2
```

## YAML: with inline environment

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template-inline-env
version: 1
description: Deployment template with inline environment definition
environment:
  name: inline-environment
  image: mcr.microsoft.com/azureml/minimal-ubuntu20.04-py38-cpu-inference:latest
  inference_config:
    liveness_route:
      path: /health
      port: 5001
    readiness_route:
      path: /ready
      port: 5001
    scoring_route:
      path: /score
      port: 5001
instance_count: 1
default_instance_type: Standard_DS3_v2
```

## YAML: with model mount path

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template-custom-mount
version: 1
description: Deployment template with custom model mount path
environment: azureml:my-environment:1
instance_count: 1
default_instance_type: Standard_DS3_v2
model_mount_path: /var/azureml-app/models
```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
