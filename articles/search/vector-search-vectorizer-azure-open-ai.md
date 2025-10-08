---
title: Azure OpenAI vectorizer
titleSuffix: Azure AI Search
description: Connects to a deployed model on your Azure OpenAI resource at query time.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: reference
ms.date: 10/06/2025
ms.update-cycle: 365-days
---

# Azure OpenAI vectorizer

The **Azure OpenAI** vectorizer connects to an embedding model deployed to your [Azure OpenAI](/azure/ai-services/openai/overview) resource or [Azure AI Foundry](/azure/ai-foundry/what-is-azure-ai-foundry) project to generate embeddings at query time. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

Although vectorizers are used at query time, you specify them in index definitions and reference them on vector fields through a vector profile. For more information, see [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md).

The Azure OpenAI vectorizer is called `AzureOpenAIVectorizer` in the REST API. Use the latest stable version of [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) or an Azure SDK package that provides the feature.

> [!NOTE]
> This vectorizer is bound to Azure OpenAI and is charged at the existing [Azure OpenAI Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing).

## Prerequisites

+ An [Azure OpenAI in Azure AI Foundry Models resource](/azure/ai-foundry/openai/how-to/create-resource) or [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects).

  + Your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://<resourcename>.openai.azure.com`. If you created the resource in the Azure portal, this subdomain was automatically generated during resource setup.

  + Your Azure AI Foundry project should have an Azure AI services endpoint with the `cognitiveservices.azure.com` domain. After you deploy an Azure OpenAI embedding model to the project, you must change the endpoint to use the `openai.azure.com` domain. For example, change the endpoint from `https://<resourcename>.cognitiveservices.azure.com` to `https://<resourcename>.openai.azure.com`. You can then use this updated endpoint for the `resourceUri` property in this vectorizer.

+ An Azure OpenAI embedding model deployed to your resource or project. For supported models, see the next section.

## Vectorizer parameters

Parameters are case-sensitive.

| Parameter name	 | Description |
|--------------------|-------------|
| `resourceUri` | The URI of the model provider. This parameter only supports URLs with the `openai.azure.com` domain, such as `https://<resourcename>.openai.azure.com`. [Azure API Management](/azure/api-management/api-management-key-concepts) endpoints are supported with URL `https://<resourcename>.azure-api.net`. Shared private links aren't supported for API Management endpoints. |
| `apiKey`   |  The secret key used to access the model. If you provide a key, leave `authIdentity` empty. If you set both the `apiKey` and `authIdentity`, the `apiKey` is used on the connection. |
| `deploymentId`   | The name of the deployed Azure OpenAI embedding model. The model should be an embedding model, such as text-embedding-ada-002. See the [List of Azure OpenAI models](/azure/ai-services/openai/concepts/models) for supported models.|
| `authIdentity`   | A user-managed identity used by the search service for connecting to Azure OpenAI. You can use either a [system or user managed identity](search-how-to-managed-identities.md). To use a system managed identity, leave `apiKey` and `authIdentity` blank. The system-managed identity is used automatically. A managed identity must have [Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) permissions to send text to Azure OpenAI. |
| `modelName` | (Required in API version 2024-05-01-Preview and later). The name of the Azure OpenAI embedding model that is deployed at the provided `resourceUri` and `deploymentId`. Currently, supported values are `text-embedding-ada-002`, `text-embedding-3-large`, and `text-embedding-3-small`. |

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

## See also

+ [Integrated vectorization](vector-search-integrated-vectorization.md)
+ [How to configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
