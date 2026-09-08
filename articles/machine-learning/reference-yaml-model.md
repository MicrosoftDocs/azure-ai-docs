---
title: 'CLI (v2) model YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) model YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: reference
ms.custom: cliv2

author: s-polly
ms.author: scottpolly
ms.date: 05/12/2026
ms.reviewer: sehan
ai-usage: ai-assisted
---

# CLI (v2) model YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

The source JSON schema can be found at https://azuremlschemas.azureedge.net/latest/model.schema.json.



[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values |
| --- | ---- | ----------- | -------------- |
| `$schema` | string | The YAML schema. | |
| `name` | string | **Required.** Name of the model. | |
| `version` | int | Version of the model. If omitted, Azure Machine Learning will autogenerate a version. | |
| `description` | string | Description of the model. | |
| `tags` | object | Dictionary of tags for the model. | |
| `path` | string | Either a local path to the model file(s), or the URI of a cloud path to the model file(s). This can point to either a file or a directory. | |
| `type` | string | Storage format type of the model. Applicable for no-code deployment scenarios. | `custom_model`, `mlflow_model`, `triton_model` |
| `flavors` | object | Flavors of the model. Each model storage format type may have one or more supported flavors. Applicable for no-code deployment scenarios. | |
| `default_deployment_template` | object | The default deployment template for the model. Applies to registry-scoped models only. When set, deployments that reference this model use the deployment template's settings (such as `environment`, `instance_type`, and probes) by default. | |
| `default_deployment_template.asset_id` | string | The asset ID of the deployment template. Format: `azureml://registries/<registry-name>/deploymenttemplates/<template-name>/versions/<version>`. | |
| `allowed_deployment_templates` | list of objects | Author guidance listing the deployment templates that a consumer is recommended to use as overrides when they deploy this model — a curated set of validated templates. It isn't enforced: an override specified at deployment time isn't required to be in this list. | |
| `allowed_deployment_templates[].asset_id` | string | The asset ID of an allowed deployment template. Format: `azureml://registries/<registry-name>/deploymenttemplates/<template-name>/labels/latest`. | |

## Remarks

The `az ml model` command can be used for managing Azure Machine Learning models.

## Examples

Examples are available in the [examples GitHub repository](https://github.com/Azure/azureml-examples/tree/main/cli/assets/model). Several are shown below.

## YAML: local file

:::code language="yaml" source="~/azureml-examples-main/cli/assets/model/local-file.yml":::

## YAML: local folder in MLflow format

:::code language="yaml" source="~/azureml-examples-main/cli/assets/model/local-mlflow.yml":::

## YAML: default deployment template

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/model.schema.json
name: my-model
version: 1
path: ./model
default_deployment_template:
  asset_id: azureml://registries/my-registry/deploymenttemplates/my-template/versions/1
```

## YAML: default and allowed deployment templates

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/model.schema.json
name: my-model
version: 1
type: custom_model
path: ./model
default_deployment_template:
  asset_id: azureml://registries/my-registry/deploymenttemplates/my-template/versions/1
allowed_deployment_templates:
  - asset_id: azureml://registries/my-registry/deploymenttemplates/my-template/labels/latest
  - asset_id: azureml://registries/my-registry/deploymenttemplates/my-template2/labels/latest
```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
- [What are deployment templates?](concept-deployment-template.md)
- [Manage models with deployment templates](how-to-manage-models-deployment-templates.md)
- [Deploy models that use deployment templates](how-to-deploy-models-deployment-template.md)
- [CLI (v2) deployment template YAML schema](reference-yaml-deployment-template.md)
- [CLI (v2) managed online deployment YAML schema](reference-yaml-deployment-managed-online.md)
