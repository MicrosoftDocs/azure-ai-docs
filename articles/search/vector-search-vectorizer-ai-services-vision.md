---
title: Azure Vision vectorizer
titleSuffix: Azure AI Search
description: Connects to Azure Vision in Foundry Tools to generate embeddings at query time.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 10/23/2025
ms.update-cycle: 365-days
---

# Azure Vision vectorizer

> [!IMPORTANT]
> This vectorizer is in public preview under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). The [2024-05-01-Preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-Preview&preserve-view=true) and newer preview APIs support this feature.

The **Azure Vision** vectorizer connects to Azure Vision in Foundry Tools via a [Microsoft Foundry resource](/azure/ai-services/multi-service-resource). At query time, the vectorizer uses the [multimodal embeddings API](/azure/ai-services/computer-vision/concept-image-retrieval) to generate embeddings.

To determine where this model is accessible, see the [region availability for multimodal embeddings](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability). Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

> [!NOTE]
> This vectorizer is bound to Foundry Tools. Execution of the vectorizer is charged at the [Foundry Tools Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/).

## Vectorizer parameters

Parameters are case sensitive.

| Parameter name | Description |
|---------------------|-------------|
| `resourceUri` | The endpoint of the Foundry resource, which must have the the `https://<resource-name>.services.ai.azure.com` or `https://<resource-name>.cognitiveservices.azure.com` format. You can find this endpoint on the **Keys and Endpoint** page in the Azure portal. |
| `apiKey`   |  The API key of the Foundry resource. |
| `modelVersion` | (Required) The model version to be passed to the Azure Vision API for generating embeddings. It's important that all embeddings stored in a given index field are generated using the same `modelVersion`. For information about version support for this model refer to [multimodal embeddings](/azure/ai-services/computer-vision/concept-image-retrieval#what-are-vector-embeddings). |
| `authIdentity`   | A user-managed identity used by the search service for connecting to Foundry. You can use either a [system- or user-managed identity](search-how-to-managed-identities.md). To use a system-managed identity, leave `apiKey` and `authIdentity` blank. The system-managed identity is used automatically. A managed identity must have **Cognitive Services User** permissions to use this vectorizer. |

## Supported vector query types

The Azure Vision vectorizer supports `text`, `imageUrl`, and `imageBinary` vector queries.

## Expected field dimensions

A vector field configured with the Azure Vision vectorizer should have a dimensions value of 1024.

## Sample definition

```json
"vectorizers": [
    {
        "name": "my-ai-services-vision-vectorizer",
        "kind": "aiServicesVision",
        "aiServicesVisionParameters": {
            "resourceUri": "https://westus.api.cognitive.microsoft.com/",
            "apiKey": "0000000000000000000000000000000000000",
            "authIdentity": null,
            "modelVersion": "2023-04-15"
        },
    }
]
```

## See also

+ [Integrated vectorization](vector-search-integrated-vectorization.md)
+ [How to configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md)
