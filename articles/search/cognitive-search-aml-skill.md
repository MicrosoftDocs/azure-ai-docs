---
title: Custom AML Skill in Skillsets
titleSuffix: Azure AI Search
description: Learn how to extend the capabilities of Azure AI Search skillsets with Microsoft Foundry or Azure Machine Learning models.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: concept-article
ms.date: 10/23/2025
ms.update-cycle: 180-days
---

# AML skill

> [!IMPORTANT]
> Support for indexer connections to the model catalog is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). Preview REST APIs support this capability.

Use the **AML** skill to extend AI enrichment with a deployed base embedding model from the [Microsoft Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md) or a custom [Azure Machine Learning](../machine-learning/overview-what-is-azure-machine-learning.md) (AML) model. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

You specify the AML skill in a skillset, which then integrates your deployed model into an AI enrichment pipeline. The AML skill is useful for performing processing or inference not supported by built-in skills. Examples include generating embeddings with your own model and applying custom machine learning logic to enriched content.

For AML online endpoints, use a stable API version or an equivalent Azure SDK to call the AML skill. For connections to the model catalog, use a preview API version.

## AML skill usage

Like other skills, the AML skill has inputs and outputs. The inputs are sent as a JSON object to a serverless deployment from the Foundry model catalog or an AML online endpoint. The output should include a success status code, JSON payload, and the parameters specified by your AML skill definition. Any other response is considered an error, and no enrichments are performed.

The indexer retries two times for the following HTTP status codes:

+ `503 Service Unavailable`
+ `429 Too Many Requests`

## AML skill for models in Microsoft Foundry

Azure AI Search provides the [Microsoft Foundry model catalog vectorizer](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md), which is also available in the [**Import data (new)** wizard](search-import-data-portal.md#skills), for query-time connections to the model catalog. If you want to use this vectorizer for queries, the AML skill is the *indexing counterpart* for generating embeddings using a model from the model catalog.

During indexing, the AML skill can connect to the model catalog to generate vectors for the index. At query time, queries can use a vectorizer to connect to the same model to vectorize text strings. You should use the AML skill and the Microsoft Foundry model catalog vectorizer together so that the same embedding model is used for indexing and queries. For more information, see [Use embedding models from the Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md).

We recommend using the [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) to generate a skillset that includes an AML skill for deployed embedding models in Foundry. The wizard generates the AML skill definition for inputs, outputs, and mappings, providing an easy way to test a model before writing any code.

## Prerequisites

+ A [Microsoft Foundry hub-based project](/azure/ai-foundry/how-to/hub-create-projects) or an [AML workspace](../machine-learning/concept-workspace.md) for a custom model that you create.

+ For hub-based projects only, a serverless deployment of a [supported model](#skill-parameters) from the Microsoft Foundry model catalog. You can use [use the Azure CLI](vector-search-integrated-vectorization-ai-studio.md#deploy-an-embedding-model-as-a-serverless-deployment) to provision the serverless deployment.

## @odata.type

Microsoft.Skills.Custom.AmlSkill

## Skill parameters

Parameters are case sensitive. The parameters you use depend on what [authentication your model provider requires](#WhatSkillParametersToUse), if any.

| Parameter name | Description |
|--------------------|-------------|
| `uri` | (Required for [key authentication](#WhatSkillParametersToUse)) The target URI of the serverless deployment from the Microsoft Foundry model catalog or the [scoring URI of the AML online endpoint](../machine-learning/how-to-authenticate-online-endpoint.md). Only the HTTPS URI scheme is allowed. Supported models from the model catalog (serverless deployments only) are:<ul><li>Cohere-embed-v3-english</li><li>Cohere-embed-v3-multilingual</li><li>Cohere-embed-v4</li></ul> |
| `key` | (Required for [key authentication](#WhatSkillParametersToUse)) The API key of the model provider. |
| `resourceId` | (Required for [token authentication](#WhatSkillParametersToUse)) The Azure Resource Manager resource ID of the model provider. For an AML online endpoint, use the `subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.MachineLearningServices/workspaces/{workspace-name}/onlineendpoints/{endpoint_name}` format. |
| `region` | (Optional for [token authentication](#WhatSkillParametersToUse)) The region in which the model provider is deployed. Required if the region is different from the region of the search service. |
| `timeout` | (Optional) The timeout for the HTTP client making the API call. It must be formatted as an XSD "dayTimeDuration" value, which is a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value. For example, `PT60S` for 60 seconds. If not set, a default value of 30 seconds is chosen. You can set the timeout to a minimum of 1 second and a maximum of 230 seconds. |
| `degreeOfParallelism` | (Optional) The number of calls the indexer makes in parallel to the endpoint you provide. You can decrease this value if your endpoint is failing under too high of a request load. You can raise it if your endpoint is able to accept more requests and you would like an increase in the performance of the indexer. If not set, a default value of 5 is used. You can set `degreeOfParallelism` to a minimum of 1 and a maximum of 10. |

<a name="WhatSkillParametersToUse"></a>

## Authentication

The AML skill provides two authentication options:

+ **Key-based authentication**. You provide a static key to authenticate scoring requests from the AML skill. Set the `uri` and `key` parameters for this connection.

+ **Token-based authentication**. The Foundry hub-based project or AML online endpoint is deployed using token-based authentication. The Azure AI Search service must have a [managed identity](/azure/active-directory/managed-identities-azure-resources/overview) and a role assignment on the model provider. The AML skill then uses the search service identity to authenticate against the model provider, with no static keys required. The search service identity must have the **Owner** or **Contributor** role. Set the `resourceId` parameter, and if the search service is in a different region from the model provider, set the `region` parameter.

## Skill inputs

Skill inputs are a node of the [enriched document](cognitive-search-working-with-skillsets.md#enrichment-tree) created during *document cracking*. For example, it might be the root document, a normalized image, or the content of a blob. There are no predefined inputs for this skill. For inputs, you should specify one or more nodes that are populated at the time of the AML skill's execution.

## Skill outputs

Skill outputs are new nodes of an enriched document created by the skill. There are no predefined outputs for this skill. For outputs, you should provide nodes that can be populated from the JSON response of your AML skill.

## Sample definition

```json
  {
    "@odata.type": "#Microsoft.Skills.Custom.AmlSkill",
    "description": "A custom model that detects the language in a document.",
    "uri": "https://language-model.models.contoso.com/score",
    "context": "/document",
    "inputs": [
      {
        "name": "text",
        "source": "/document/content"
      }
    ],
    "outputs": [
      {
        "name": "detected_language_code"
      }
    ]
  }
```

## Sample input JSON structure

This JSON structure represents the payload sent to your Foundry hub-based project or AML online endpoint. The top-level fields of the structure correspond to the "names" specified in the `inputs` section of the skill definition. The values of those fields are from the "sources" of those fields, which could be from a field in the document or another skill.

```json
{
  "text": "Este es un contrato en Inglés"
}
```

## Sample output JSON structure

The output corresponds to the response from your Foundry hub-based project or AML online endpoint. The model provider should only return a JSON payload (verified by looking at the `Content-Type` response header) and should be an object whose fields are enrichments matching the "names" in the `output` and whose value is considered the enrichment.

```json
{
    "detected_language_code": "es"
}
```

## Inline shaping sample definition

```json
  {
    "@odata.type": "#Microsoft.Skills.Custom.AmlSkill",
    "description": "A sample model that detects the language of sentence",
    "uri": "https://language-model.models.contoso.com/score",
    "context": "/document",
    "inputs": [
      {
        "name": "shapedText",
        "sourceContext": "/document",
        "inputs": [
            {
              "name": "content",
              "source": "/document/content"
            }
        ]
      }
    ],
    "outputs": [
      {
        "name": "detected_language_code"
      }
    ]
  }
```

## Inline shaping input JSON structure

```json
{
  "shapedText": { "content": "Este es un contrato en Inglés" }
}
```

## Inline shaping sample output JSON structure

```json
{
    "detected_language_code": "es"
}
```

## Error cases

In addition to your Foundry hub-based project or AML online endpoint being unavailable or sending nonsuccessful status codes, the following cases are considered errors:

* The model provider returns a success status code, but the response indicates that it isn't `application/json`. The response is thus invalid, and no enrichments are performed.

* The model provider returns invalid JSON.

If the model provider is unavailable or returns an HTTP error, a friendly error with any available details about the HTTP error is added to the indexer execution history.

## See also

+ [Create a skillset in Azure AI Search](cognitive-search-defining-skillset.md)
+ [Use embedding models from Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md)
+ [Troubleshoot Azure Machine Learning online endpoint deployment and scoring](../machine-learning/how-to-troubleshoot-online-endpoints.md)
