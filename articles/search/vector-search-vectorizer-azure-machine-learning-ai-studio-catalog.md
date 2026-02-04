---
title: Microsoft Foundry model catalog vectorizer
titleSuffix: Azure AI Search
description: Connects to a deployed model from the Microsoft Foundry model catalog at query time.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 10/23/2025
ms.update-cycle: 365-days
---

# Microsoft Foundry model catalog vectorizer

> [!IMPORTANT]
> This vectorizer is in public preview under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). To use this feature, we recommend the latest preview version of [Indexes - Create Or Update (REST API)](/rest/api/searchservice/indexes/create-or-update).

The **Microsoft Foundry model catalog** vectorizer connects to an embedding model deployed from the [Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview) or an [Azure Machine Learning](../machine-learning/overview-what-is-azure-machine-learning.md) (AML) endpoint. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

If you're using integrated vectorization to create the vector arrays, the skillset should include an [AML skill](cognitive-search-aml-skill.md) that points to the same model specified in the vectorizer.

## Prerequisites

+ A [Microsoft Foundry hub-based project](/azure/ai-foundry/how-to/hub-create-projects) or an [AML workspace](../machine-learning/concept-workspace.md) for a custom model that you create.

+ For hub-based projects only, a serverless deployment of a [supported model](#vectorizer-parameters) from the Microsoft Foundry model catalog. You can use [use the Azure CLI](vector-search-integrated-vectorization-ai-studio.md#deploy-an-embedding-model-as-a-serverless-deployment) to provision the serverless deployment.

## Vectorizer parameters

Parameters are case sensitive. The parameters you use depend on what [authentication your model provider requires](#WhatParametersToUse), if any.

| Parameter name | Description |
|--------------------|-------------|
| `uri` | (Required for [key authentication](#WhatParametersToUse)) The target URI of the serverless deployment from the Microsoft Foundry model catalog or the [scoring URI of the AML online endpoint](../machine-learning/how-to-authenticate-online-endpoint.md). Only the HTTPS URI scheme is allowed. |
| `key` | (Required for [key authentication](#WhatParametersToUse)) The API key of the model provider. |
| `resourceId` | (Required for [token authentication](#WhatParametersToUse)) The Azure Resource Manager resource ID of the model provider. For an AML online endpoint, use the `subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.MachineLearningServices/workspaces/{workspace-name}/onlineendpoints/{endpoint_name}` format. |
| `modelName` | The name of the embedding model from the Microsoft Foundry model catalog deployed at the specified `uri`. Supported models (serverless deployments only) are:<p><ul><li>Cohere-embed-v3-english</li><li>Cohere-embed-v3-multilingual</li><li>Cohere-embed-v4</li></ul> |
| `region` | (Optional for [token authentication](#WhatParametersToUse)) The region in which the model provider is deployed. Required if the region is different from the region of the search service. |
| `timeout` | (Optional) The timeout for the HTTP client making the API call. It must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value). For example, `PT60S` for 60 seconds. If not set, a default value of 30 seconds is chosen. The timeout can be set to a maximum of 230 seconds and a minimum of 1 second. |

<!-- Supported models are:<p><ul><<li>Facebook-DinoV2-Image-Embeddings-ViT-Base </li><li>Facebook-DinoV2-Image-Embeddings-ViT-Giant </li><li>Cohere-embed-v3-english </li><li>Cohere-embed-v3-multilingual</li><li>Cohere-embed-v4</li></ul> -->

<a name="WhatParametersToUse"></a>

## What authentication parameters to use

The Microsoft Foundry model catalog vectorizer provides two authentication options:

+ **Key-based authentication**. You provide a static key to authenticate scoring requests from the vectorizer. Set the `uri` and `key` parameters for this connection.

+  **Token-based authentication**. The Foundry hub-based project or AML online endpoint is deployed using token-based authentication. The Azure AI Search service must have a [managed identity](/azure/active-directory/managed-identities-azure-resources/overview) and a role assignment on the model provider. The vectorizer then uses the search service identity to authenticate against the model provider, with no static keys required. The search service identity must have the **Owner** or **Contributor** role. Set the `resourceId` parameter, and if the search service is in a different region from the model provider, set the `region` parameter.

## Supported vector query types

Which vector query types are supported by the Microsoft Foundry model catalog vectorizer depends on the `modelName` that is configured.

| Embedding model | Supports `text` query | Supports `imageUrl` query | Supports `imageBinary` query |
|--------------------|-------------|-------------|-------------|
| Cohere-embed-v3-english | X |  | X |
| Cohere-embed-v3-multilingual | X |  | X |
| Cohere-embed-v4 | X |  | X |

<!--
| Facebook-DinoV2-Image-Embeddings-ViT-Base |  | X | X |
| Facebook-DinoV2-Image-Embeddings-ViT-Giant |  | X | X |
-->

## Expected field dimensions

The expected field dimensions for a vector field configured with a Microsoft Foundry model catalog vectorizer depend on the `modelName` that is configured.

| `modelName` | Expected dimensions |
|--------------------|-------------|
| Cohere-embed-v3-english | 1024 |
| Cohere-embed-v3-multilingual | 1024 |
| Cohere-embed-v4 | 256–1536 |

<!--
| Facebook-DinoV2-Image-Embeddings-ViT-Base | 768 |
| Facebook-DinoV2-Image-Embeddings-ViT-Giant | 1536 |
-->

## Sample definition

Suggested model names in the Foundry model catalog consist of the base model plus a random three-letter suffix. The name of your model will be different from the one shown in this example.

```json
"vectorizers": [
    {
        "name": "my-model-catalog-vectorizer",
        "kind": "aml",
        "amlParameters": {
            "uri": "https://Cohere-embed-v3-multilingual-hin.eastus.models.ai.azure.com",
            "key": "aaaaaaaa-0b0b-1c1c-2d2d-333333333333",
            "timeout": "PT60S",
            "modelName": "Cohere-embed-v3-multilingual-hin",
            "resourceId": null,
            "region": null,
        },
    }
]
```

## See also

+ [Integrated vectorization](vector-search-integrated-vectorization.md)
+ [Integrated vectorization with models from Foundry](vector-search-integrated-vectorization-ai-studio.md)
+ [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [AML skill](cognitive-search-aml-skill.md)
+ [Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview)
