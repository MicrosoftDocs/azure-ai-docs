---
title: Custom AML skill in skillsets
titleSuffix: Azure AI Search
description: Extend capabilities of Azure AI Search skillsets with Azure Machine Learning models.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: reference
ms.date: 09/15/2025
ms.update-cycle: 180-days
---

# AML skill in an Azure AI Search enrichment pipeline

> [!IMPORTANT]
> Support for indexer connections to the Azure AI Foundry model catalog is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). Preview REST APIs support this capability.

Use the **AML** skill to extend AI enrichment with a deployed base embedding model from the [Azure AI Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md) or a custom [Azure Machine Learning](../machine-learning/overview-what-is-azure-machine-learning.md) (AML) model. After an AML model is [trained and deployed](../machine-learning/concept-azure-machine-learning-architecture.md#workspace), the **AML** skill integrates the model into a skillset.

## AML skill usage

Like other built-in skills, a custom **AML** skill has inputs and outputs. The inputs are sent to a deployed AML online endpoint as a JSON object. The output of the endpoint must be a JSON payload in the response, along with a success status code. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed. The response should provide the outputs specified by your **AML** skill definition. Any other response is considered an error, and no enrichments are performed.

> [!NOTE]
> The indexer retries two times for certain standard HTTP status codes returned from the AML online endpoint. These HTTP status codes are:
>
> * `503 Service Unavailable`
> * `429 Too Many Requests`

You can call the **AML** skill with the stable REST API version or an equivalent Azure SDK. For connections to the model catalog in the Azure AI Foundry portal, use a preview API version.

## AML skill for models in Azure AI Foundry

Starting in the 2024-05-01-preview REST API and the Azure portal, which also targets the 2024-05-01-preview, Azure AI Search provides the [Azure AI Foundry model catalog vectorizer](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md) for query-time connections to the model catalog in the Azure AI Foundry portal. If you want to use that vectorizer for queries, the **AML** skill is the *indexing counterpart* for generating embeddings using a model from the model catalog.

During indexing, the **AML** skill can connect to the model catalog to generate vectors for the index. At query time, queries can use a vectorizer to connect to the same model to vectorize text strings for a vector query. In this workflow, you should use the **AML** skill and the model catalog vectorizer together so that the same embedding model is used for indexing and queries. For more information, including a list of supported embedding models, see [Use embedding models from Azure AI Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md).

We recommend using the [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) to generate a skillset that includes an AML skill for deployed embedding models in Azure AI Foundry. The wizard generates the AML skill definition for inputs, outputs, and mappings, providing an easy way to test a model before writing any code.

## Prerequisites

* An [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry) for an embedding model deployed from the catalog, or an [AML workspace](../machine-learning/concept-workspace.md) for a custom model that you create.
* The model endpoint for an embedding model deployed from the catalog, or an [online endpoint (real-time)](../machine-learning/concept-endpoints-online.md) of your AML workspace for a custom model.

## @odata.type

Microsoft.Skills.Custom.AmlSkill

## Skill parameters

Parameters are case sensitive. The parameters you use depend on what [authentication your AML online endpoint requires](#WhatSkillParametersToUse), if any.

| Parameter name | Description |
|--------------------|-------------|
| `uri` | (Required for [key authentication](#WhatSkillParametersToUse)) The [scoring URI of the AML online endpoint](../machine-learning/how-to-authenticate-online-endpoint.md) to which the _JSON_ payload is sent. Only the **https** URI scheme is allowed. For embedding models in the Azure AI Foundry model catalog, this is the target URI.|
| `key` | (Required for [key authentication](#WhatSkillParametersToUse)) The [key for the AML online endpoint](../machine-learning/how-to-authenticate-online-endpoint.md) or the  |
| `resourceId` | (Required for [token authentication](#WhatSkillParametersToUse)). The Azure Resource Manager resource ID of the AML online endpoint. Use the format `subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.MachineLearningServices/workspaces/{workspace-name}/onlineendpoints/{endpoint_name}`. |
| `region` | (Optional for [token authentication](#WhatSkillParametersToUse)). The [region](https://azure.microsoft.com/global-infrastructure/regions/) the AML online endpoint is deployed in. |
| `timeout` | (Optional) When specified, indicates the timeout for the http client making the API call. It must be formatted as an XSD "dayTimeDuration" value, which is a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value. For example, `PT60S` for 60 seconds. If not set, a default value of 30 seconds is chosen. You can set the timeout to a minimum of 1 second and a maximum of 230 seconds. |
| `degreeOfParallelism` | (Optional) When specified, indicates the number of calls the indexer makes in parallel to the endpoint you provide. You can decrease this value if your endpoint is failing under too high of a request load. You can raise it if your endpoint is able to accept more requests and you would like an increase in the performance of the indexer. If not set, a default value of 5 is used. You can set the degreeOfParallelism to a minimum of 1 and a maximum of 10. |

<a name="WhatSkillParametersToUse"></a>

## Authentication

AML online endpoints provide two authentication options:

* [Key-based authentication](../machine-learning/how-to-authenticate-online-endpoint.md). A static key is provided to authenticate scoring requests from AML skills. Set the `uri` and `key` parameters for this connection.

* [Token-based authentication](../machine-learning/how-to-authenticate-online-endpoint.md), where the AML online endpoint is deployed using token-based authentication. The Azure AI Search service must have a [managed identity](/azure/active-directory/managed-identities-azure-resources/overview) and a role assignment on the AML workspace. The AML skill then uses the service's managed identity to authenticate against the AML online endpoint, with no static keys required. The search service identity must have the **Owner** or **Contributor** role. Set the `resourceId` parameter, and if the search service is in a different region from the AML workspace, set the `region` parameter.

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

This _JSON_ structure represents the payload sent to your AML online endpoint. The top-level fields of the structure correspond to the "names" specified in the `inputs` section of the skill definition. The values of those fields are from the "sources" of those fields, which could be from a field in the document or another skill.

```json
{
  "text": "Este es un contrato en Inglés"
}
```

## Sample output JSON structure

The output corresponds to the response from your AML online endpoint. The AML online endpoint should only return a _JSON_ payload (verified by looking at the `Content-Type` response header) and should be an object where the fields are enrichments matching the "names" in the `output` and whose value is considered the enrichment.

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

In addition to your AML being unavailable or sending nonsuccessful status codes, the following cases are considered errors:

* The AML online endpoint returns a success status code, but the response indicates that it isn't `application/json`. The response is thus invalid, and no enrichments are performed.

* The AML online endpoint returns invalid JSON.

If the AML online endpoint is unavailable or returns an HTTP error, a friendly error with any available details about the HTTP error is added to the indexer execution history.

## See also

+ [Create a skillset in Azure AI Search](cognitive-search-defining-skillset.md)
+ [Use embedding models from Azure AI Foundry model catalog](vector-search-integrated-vectorization-ai-studio.md)
+ [Troubleshoot Azure Machine Learning online endpoint deployment and scoring](../machine-learning/how-to-troubleshoot-online-endpoints.md)
