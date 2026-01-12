---
title: 'CLI (v2) Foundry Tools connection YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) Foundry Tools connections YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.custom:
  - build-2024
ms.topic: reference

author: s-polly
ms.author: scottpolly
ms.date: 08/29/2024
ms.reviewer: ambadal
---

# CLI (v2) Foundry Tools connection YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `$schema` | string | The YAML schema. If you use the Azure Machine Learning Visual Studio Code extension to author the YAML file, include `$schema` at the top of your file to invoke schema and resource completions. | | |
| `name` | string | **Required.** The connection name. | | |
| `description` | string | The connection description. | | |
| `tags` | object | The connection tag dictionary. | | |
| `type` | string | **Required.** The connection type. | `azure_ai_services` | `azure_ai_services` |
| `is_shared` | boolean | `true` if the connection is shared across other projects in the hub; otherwise, `false`. | | `true` |
| `endpoint` | string | **Required.** The URL of the endpoint. | | |
| `api_key` | string | The API key used to authenticate the connection. If not provided, the connection is authenticated via Microsoft Entra ID (credential-less authentication). | | |
| `ai_services_resource_id` | string | **Required.** The fully qualified Azure resource ID of the Foundry Tools resource. | | |


## Remarks

There are two ways to create connections to Foundry Tools:

- One connection for all Foundry Tools except Azure AI Search.
- One connection for each individual Foundry Tool.

The schema described in this article is for **one connection for all Foundry Tools except Azure AI Search**.

While the `az ml connection` commands can be used to manage both Azure Machine Learning and Microsoft Foundry connections, the Foundry Tools connection is specific to Foundry.

## Examples

These examples would be in the form of YAML files and used from the CLI. For example, `az ml connection create -f <file-name>.yaml`. 

### YAML: API key

```yml
#AzureAIServiceConnection.yml

name: myazai_ei
type: azure_ai_services
endpoint: https://contoso.cognitiveservices.azure.com/
api_key: XXXXXXXXXXXXXXX
```


### YAML: Microsoft Entra ID

```yml
#AzureAIServiceConnection.yml

name: myazai_apk
type: azure_ai_services
endpoint: https://contoso.cognitiveservices.azure.com/

```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
