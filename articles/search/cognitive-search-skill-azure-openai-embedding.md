---
title: Azure OpenAI Embedding skill
titleSuffix: Azure AI Search
description: Connects to a deployed model on your Azure OpenAI resource.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: reference
ms.date: 10/23/2025
---

#	Azure OpenAI Embedding skill

The **Azure OpenAI Embedding** skill connects to an embedding model deployed to your [Azure OpenAI in Foundry Models](/azure/ai-services/openai/overview) resource or [Microsoft Foundry](/azure/ai-foundry/what-is-foundry) project to generate embeddings during indexing. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

The [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) in the Azure portal uses the Azure OpenAI Embedding skill to vectorize content. You can run the wizard and review the generated skillset to see how the wizard builds the skill for embedding models.

> [!NOTE]
> This skill is bound to Azure OpenAI and is charged at the [Azure OpenAI Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing).

## Prerequisites

+ An [Azure OpenAI in Foundry Models resource](/azure/ai-foundry/openai/how-to/create-resource) or [Foundry project](/azure/ai-foundry/how-to/create-projects).

  + Your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://<resource-name>.openai.azure.com`. You can find this endpoint on the **Keys and Endpoint** page in the Azure portal and use it for the `resourceUri` property in this skill.

  + The [parent resource](/azure/ai-services/multi-service-resource) of your Foundry project provides access to multiple endpoints, including `https://<resource-name>.openai.azure.com`, `https://<resource-name>.services.ai.azure.com`, and `https://<resource-name>.cognitiveservices.azure.com`. You can find these endpoints on the **Keys and Endpoint** page in the Azure portal and use any of them for the `resourceUri` property in this skill.

+ An Azure OpenAI embedding model deployed to your resource or project. For supported models, see the [Skill parameters](#skill-parameters) section.

## @odata.type  

Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill

## Data limits

The maximum size of a text input should be 8,000 tokens. If input exceeds the maximum allowed, the model throws an invalid request error. For more information, see the [tokens](/azure/ai-services/openai/overview#tokens) key concept in the Azure OpenAI documentation. Consider using the [Text Split skill](cognitive-search-skill-textsplit.md) if you need data chunking.

## Skill parameters

Parameters are case sensitive.

| Inputs | Description |
|---------------------|-------------|
| `resourceUri` | (Required) The URI of the model provider. Supported domains are:<p><ul><li>`openai.azure.com`</li><li>`services.ai.azure.com`</li><li>`cognitiveservices.azure.com`</li></ul><p>This field is required if your resource is deployed behind a private endpoint or uses virtual network (VNet) integration. [Azure API Management](/azure/api-management/api-management-key-concepts) endpoints are supported with URL `https://<resource-name>.azure-api.net`. Shared private links aren't supported for API Management endpoints. |
| `apiKey`   |  The secret key used to access the model. If you provide a key, leave `authIdentity` empty. If you set both `apiKey` and `authIdentity`, the `apiKey` is used on the connection. |
| `deploymentId`   | (Required) The ID of the deployed Azure OpenAI embedding model. This is the deployment name you specified when you deployed the model. |
| `authIdentity`   | A user-managed identity used by the search service for the connection. You can use either a [system- or user-managed identity](search-how-to-managed-identities.md). To use a system-managed identity, leave `apiKey` and `authIdentity` blank. The system-managed identity is used automatically. A managed identity must have [Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) permissions to send text to Azure OpenAI. |
| `modelName` | (Required) The name of the Azure OpenAI model deployed at the specified `deploymentId`. Supported values are:<p><ul><li>`text-embedding-ada-002`</li><li>`text-embedding-3-large`</li><li>`text-embedding-3-small`</li></ul> |
| `dimensions` | (Optional) The dimensions of embeddings that you want to generate, assuming the model [supports a range of dimensions](#supported-dimensions-by-modelname). The default is the maximum dimensions for each model. For skillsets created with REST API versions prior to the 2023-10-01-preview, the dimensions are fixed at 1536. If you set the `dimensions` property in this skill, set the `dimensions` property on the [vector field definition](vector-search-how-to-create-index.md#add-a-vector-field-to-the-fields-collection) to the same value. |

## Supported dimensions by `modelName`

The supported dimensions for an Azure OpenAI Embedding skill depend on the `modelName` that is configured.

| `modelName` | Minimum dimensions | Maximum dimensions |
|--------------------|-------------|-------------|
| text-embedding-ada-002 | 1536 | 1536 |
| text-embedding-3-large | 1 | 3072 |
| text-embedding-3-small | 1 | 1536 |

## Skill inputs

| Input	 | Description |
|--------------------|-------------|
| `text` | The input text to be vectorized. If you're using data chunking, the source might be `/document/pages/*`. |

## Skill outputs

| Output	 | Description |
|--------------------|-------------|
| `embedding` | Vectorized embedding for the input text. |

## Sample definition

Consider a record that has the following fields:

```json
{
    "content": "Microsoft released Windows 10."
}
```

Then your skill definition might look like this:

```json
{
  "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
  "description": "Connects a deployed embedding model.",
  "resourceUri": "https://my-demo-openai-eastus.openai.azure.com/",
  "deploymentId": "my-text-embedding-ada-002-model",
  "modelName": "text-embedding-ada-002",
  "dimensions": 1536,
  "inputs": [
    {
      "name": "text",
      "source": "/document/content"
    }
  ],
  "outputs": [
    {
      "name": "embedding"
    }
  ]
}
```

## Sample output

For the given input text, a vectorized embedding output is produced.

```json
{
  "embedding": [
        0.018990106880664825,
        -0.0073809814639389515,
        .... 
        0.021276434883475304,
      ]
}
```

The output resides in memory. To send this output to a field in the search index, you must define an [outputFieldMapping](cognitive-search-output-field-mapping.md) that maps the vectorized embedding output (which is an array) to a [vector field](vector-search-how-to-create-index.md). Assuming the skill output resides in the document's **embedding** node, and **content_vector** is the field in the search index, the outputFieldMapping in indexer should look like:

```json
  "outputFieldMappings": [
    {
      "sourceFieldName": "/document/embedding/*",
      "targetFieldName": "content_vector"
    }
  ]
```

## Best practices

The following are some best practices you need to consider when utilizing this skill:

- If you are hitting your Azure OpenAI TPM (Tokens per minute) limit, consider the [quota limits advisory](/azure/ai-services/openai/quotas-limits) so you can address accordingly. Refer to the [Azure OpenAI monitoring](/azure/ai-services/openai/how-to/monitoring) documentation for more information about your Azure OpenAI instance performance.

-	The Azure OpenAI embeddings model deployment you use for this skill should be ideally separate from the deployment used for other use cases, including the [query vectorizer](vector-search-how-to-configure-vectorizer.md). This helps each deployment to be tailored to its specific use case, leading to optimized performance and identifying traffic from the indexer and the index embedding calls easily.

- Your Azure OpenAI instance should be in the same region or at least geographically close to the region where your AI Search service is hosted. This reduces latency and improves the speed of data transfer between the services.

-	If you have a larger than default Azure OpenAI TPM (Tokens per minute) limit as published in [quotas and limits](/azure/ai-services/openai/quotas-limits) documentation, open a [support case](/azure/azure-portal/supportability/how-to-create-azure-support-request) with the Azure AI Search team, so this can be adjusted accordingly. This helps your indexing process not being unnecessarily slowed down by the documented default TPM limit, if you have higher limits.

- For examples and working code samples using this skill, see the following links:

  - [Integrated vectorization (Python)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/integrated-vectorization/readme.md)
  - [Integrated vectorization (C#)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-dotnet/DotNetIntegratedVectorizationDemo/readme.md)
  - [Integrated vectorization (Java)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-java/demo-integrated-vectorization/readme.md)

## Errors and warnings

| Condition | Result |
|-----------|--------|
| Null or invalid URI | Error |
| Null or invalid deploymentID | Error |
| Text is empty | Warning |
| Text is larger than 8,000 tokens | Error |

## See also

+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [How to define output fields mappings](cognitive-search-output-field-mapping.md)
