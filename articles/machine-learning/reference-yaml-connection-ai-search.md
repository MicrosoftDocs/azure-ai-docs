---
title: 'CLI (v2) AI Search connection YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) AI Search connections YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.custom:
  - build-2024
ms.topic: reference

author: Blackmist
ms.author: larryfr
ms.date: 08/29/2024
ms.reviewer: ambadal
---

# CLI (v2) Azure AI Search connection YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `$schema` | string | The YAML schema. If you use the Azure Machine Learning Visual Studio Code extension to author the YAML file, include `$schema` at the top of your file to invoke schema and resource completions. | | |
| `name` | string | **Required.** The connection name. | | |
| `description` | string | The connection description. | | |
| `tags` | object | The connection tag dictionary. | | |
| `type` | string | **Required.** The connection type. | `azure_ai_search` | `azure_ai_search` |
| `is_shared` | boolean | `true` if the connection is shared across other projects in the hub; otherwise, `false`. | | `true` |
| `endpoint` | string | **Required.** The URL of the endpoint. | | |
| `api_key` | string | The API key used to authenticate the connection. If not provided, the connection is authenticated via Microsoft Entra ID (credential-less authentication). | | |

## Remarks

While the `az ml connection` commands can be used to manage both Azure Machine Learning and Azure AI Foundry connections, the Azure AI Search connection is specific to Azure AI Foundry.

## Examples

These examples would be in the form of YAML files and used from the CLI. For example, `az ml connection create -f <file-name>.yaml`. 

### YAML: API key

```yml
#AzureContentSafetyConnection.yml

name: myazaics_apk
type: azure_ai_search

endpoint: https://contoso.search.windows.net/
api_key: XXXXXXXXXXXXXXX
```

### YAML: Microsoft Entra ID (preview)

```yml
#AzureContentSafetyConnection.yml

name: myazaics_ei
type: azure_ai_search

endpoint: https://contoso.search.windows.net/
```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
