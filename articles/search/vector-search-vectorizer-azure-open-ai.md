---
title: Azure OpenAI Vectorizer
description: Connects to a deployed model on your Azure OpenAI resource at query time.
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 05/09/2026
ms.update-cycle: 365-days
---

# Azure OpenAI vectorizer

The **Azure OpenAI** vectorizer connects to an embedding model deployed to your [Azure OpenAI in Foundry Models](/azure/ai-services/openai/overview) resource or [Microsoft Foundry](/azure/ai-foundry/what-is-azure-ai-foundry) project to generate embeddings at query time. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

Although vectorizers are used at query time, you specify them in index definitions and reference them on vector fields through a vector profile. For more information, see [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md).

The Azure OpenAI vectorizer is called `AzureOpenAIVectorizer` in the REST API. Use the latest stable version of [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) or an Azure SDK package that provides the feature.

> [!NOTE]
> This vectorizer is bound to Azure OpenAI and is charged at the [Azure OpenAI Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing).

## Prerequisites

+ An [Azure OpenAI in Foundry Models resource](/azure/ai-foundry/openai/how-to/create-resource) or [Foundry project](/azure/ai-foundry/how-to/create-projects).

  + Your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://<resource-name>.openai.azure.com`. You can find this endpoint on the **Keys and Endpoint** page in the Azure portal and use it for the `resourceUri` property in this skill.

  + The [parent resource](/azure/ai-services/multi-service-resource) of your Foundry project provides access to multiple endpoints, including `https://<resource-name>.openai.azure.com`, `https://<resource-name>.services.ai.azure.com`, and `https://<resource-name>.cognitiveservices.azure.com`. You can find these endpoints on the **Keys and Endpoint** page in the Azure portal and use any of them for the `resourceUri` property in this skill.

+ An Azure OpenAI embedding model deployed to your resource or project. For supported models, see the next section.

## Vectorizer parameters

Parameters are case sensitive.

| Parameter name	 | Description |
|--------------------|-------------|
| `resourceUri` | (Required) The URI of the model provider. Supported domains are:<p><ul><li>`openai.azure.com`</li><li>`services.ai.azure.com`</li><li>`cognitiveservices.azure.com`</li></ul><p>[Azure API Management](/azure/api-management/api-management-key-concepts) endpoints are supported with URL `https://<resource-name>.azure-api.net`. Shared private links aren't supported for API Management endpoints. |
| `apiKey`   |  The secret key used to access the model. If you provide a key, leave `authIdentity` empty. If you set both `apiKey` and `authIdentity`, the `apiKey` is used on the connection. |
| `deploymentId`   | (Required) The ID of the deployed Azure OpenAI embedding model. This is the deployment name you specified when you deployed the model. |
| `authIdentity`   | A user-managed identity used by the search service for the connection. You can use either a [system- or user-managed identity](search-how-to-managed-identities.md). To use a system-managed identity, leave `apiKey` and `authIdentity` blank. The system-managed identity is used automatically. A managed identity must have [Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) permissions to send text to Azure OpenAI. |
| `modelName` | (Required) The name of the Azure OpenAI model deployed at the specified `deploymentId`. Supported values are:<p><ul><li>`text-embedding-ada-002`</li><li>`text-embedding-3-large`</li><li>`text-embedding-3-small`</li></ul> |

## Supported vector query types

The Azure OpenAI vectorizer only supports `text` vector queries.

## Expected field dimensions

The expected field dimensions for a field configured with an Azure OpenAI vectorizer depend on the `modelName` that is configured.

| `modelName` | Minimum dimensions | Maximum dimensions |
|--------------------|-------------|-------------|
| text-embedding-ada-002 | 1536 | 1536 |
| text-embedding-3-large | 1 | 3072 |
| text-embedding-3-small | 1 | 1536 |

## Sample definition

```json
"vectorizers": [
    {
        "name": "my-openai-vectorizer",
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
            "resourceUri": "https://my-fake-azure-openai-resource.openai.azure.com",
            "apiKey": "0000000000000000000000000000000000000",
            "deploymentId": "my-ada-002-deployment",
            "authIdentity": null,
            "modelName": "text-embedding-ada-002",
        },
    }
]
```

## Best practices

The following are some best practices you need to consider when utilizing this vectorizer:

- If you are hitting your Azure OpenAI TPM (Tokens per minute) limit, consider the [quota limits advisory](/azure/ai-services/openai/quotas-limits) so you can address accordingly. Refer to the [Azure OpenAI monitoring](/azure/ai-services/openai/how-to/monitoring) documentation for more information about your Azure OpenAI instance performance.

-	The Azure OpenAI embeddings model deployment you use for this vectorizer should be ideally separate from the deployment used for other use cases, including the [embedding skill](cognitive-search-skill-azure-openai-embedding.md). This helps each deployment to be tailored to its specific use case, leading to optimized performance and identifying traffic from the indexer and the index embedding calls easily.

- Your Azure OpenAI instance should be in the same region or at least geographically close to the region where your AI Search service is hosted. This reduces latency and improves the speed of data transfer between the services.

- To avoid experiencing 429 error codes often, consider implementing load balancing via [API Management](/azure/api-management/) by implementing a gateway [/azure/architecture/ai-ml/guide/azure-openai-gateway-multi-backend] in front of multiple Azure OpenAI embedding model deployments.

-	If you have a larger than default Azure OpenAI TPM (Tokens per minute) limit as published in [quotas and limits](/azure/ai-services/openai/quotas-limits) documentation, open a [support case](/azure/azure-portal/supportability/how-to-create-azure-support-request) with the Azure AI Search team, so this can be adjusted accordingly. This helps your indexing process not being unnecessarily slowed down by the documented default TPM limit, if you have higher limits.


## See also

+ [Integrated vectorization](vector-search-integrated-vectorization.md)
+ [How to configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
