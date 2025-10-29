---
title: 'CLI (v2) data YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) data YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: reference
ms.custom: cliv2

author: s-polly
ms.author: scottpolly
ms.date: 04/15/2024
ms.reviewer: yogipandey
---

# CLI (v2) data YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

You can find the source JSON schema at https://azuremlschemas.azureedge.net/latest/data.schema.json.

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `$schema` | string | The YAML schema. If you use the Azure Machine Learning Visual Studio Code extension to author the YAML file, include `$schema` at the top of your file to invoke schema and resource completions. | | |
| `name` | string | **Required.** The data asset name. | | |
| `version` | string | The dataset version. If omitted, Azure Machine Learning autogenerates a version. | | |
| `description` | string | The data asset description. | | |
| `tags` | object | The datastore tag dictionary. | | |
| `type` | string | The data asset type. Specify `uri_file` for data that points to a single file source, or `uri_folder` for data that points to a folder source. | `uri_file`, `uri_folder` | `uri_folder` |
| `path` | string | Either a local path to the data source file or folder, or the URI of a cloud path to the data source file or folder. Ensure that the source provided here is compatible with the `type` specified. <br><br> Supported URI types are `azureml`, `https`, `wasbs`, `abfss`, and `adl`. To use the `azureml://` URI format, see [Core yaml syntax](reference-yaml-core-syntax.md). | | |

## Remarks

The `az ml data` commands can be used to manage Azure Machine Learning data assets.

## Examples

Visit [this GitHub resource](https://github.com/Azure/azureml-examples/tree/main/cli/assets/data) for examples. Several are shown:

## YAML: datastore file

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-file.yml":::

## YAML: datastore folder

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-folder.yml":::

## YAML: https file

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-file-https.yml":::

## YAML: https folder

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-folder-https.yml":::

## YAML: wasbs file

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-file-wasbs.yml":::

## YAML: wasbs folder

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/cloud-folder-wasbs.yml":::

## YAML: local file

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/local-file.yml":::

## YAML: local folder

:::code language="yaml" source="~/azureml-examples-main/cli/assets/data/local-folder.yml":::

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)