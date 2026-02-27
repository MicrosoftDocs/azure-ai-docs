---
title: How to generate image embeddings with Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to generate embeddings with Microsoft Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: malpande
reviewer: mpande98
ms.custom: generated
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use image embeddings API with Microsoft Foundry Models.


## Prerequisites

To use embedding models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* An image embeddings model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add an embeddings model to your resource.

  * This example uses `Cohere-embed-v3-english` from Cohere.

## Use image embeddings

To use the text embeddings, use the route `/images/embeddings` appended to your base URL along with your credential indicated in `api-key`. `Authorization` header is also supported with the format `Bearer <key>`.

```http
POST https://<resource>.services.ai.azure.com/models/images/embeddings?api-version=2024-05-01-preview
Content-Type: application/json
api-key: <key>
```

If you have configured the resource with **Microsoft Entra ID** support, pass you token in the `Authorization` header with the format `Bearer <token>`. Use scope `https://cognitiveservices.azure.com/.default`. 

```http
POST https://<resource>.services.ai.azure.com/models/images/embeddings?api-version=2024-05-01-preview
Content-Type: application/json
Authorization: Bearer <token>
```

Using Microsoft Entra ID may require additional configuration in your resource to grant access. Learn how to [configure key-less authentication with Microsoft Entra ID](../../how-to/configure-entra-id.md).

### Create embeddings

To create image embeddings, you need to pass the image data as part of your request. Image data should be in PNG format and encoded as base64.

```json
{
    "model": "Cohere-embed-v3-english",
    "input": [
        {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUh..."
        }
    ]
}
```

> [!TIP]
> When creating a request, take into account the token's input limit for the model. If you need to embed larger portions of text, you would need a chunking strategy.

The response is as follows, where you can see the model's usage statistics:


```json
{
    "id": "0ab1234c-d5e6-7fgh-i890-j1234k123456",
    "object": "list",
    "data": [
        {
            "index": 0,
            "object": "embedding",
            "embedding": [
                0.017196655,
                // ...
                -0.000687122,
                -0.025054932,
                -0.015777588
            ]
        }
    ],
    "model": "Cohere-embed-v3-english",
    "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 0,
        "total_tokens": 9
    }
}
```

> [!IMPORTANT]
> Computing embeddings in batches may not be supported for all the models. For example, for `Cohere-embed-v3-english` model, you need to send one image at a time.

#### Embedding images and text pairs

Some models can generate embeddings from images and text pairs. In this case, you can use the `image` and `text` fields in the request to pass the image and text to the model. The following example shows how to create embeddings for images and text pairs:


```json
{
    "model": "Cohere-embed-v3-english",
    "input": [
        {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUh...",
            "text": "A photo of a cat"
        }
    ]
}
```

#### Create different types of embeddings

Some models can generate multiple embeddings for the same input depending on how you plan to use them. This capability allows you to retrieve more accurate embeddings for RAG patterns. 

The following example shows how to create embeddings that are used to create an embedding for a document that will be stored in a vector database:


```json
{
    "model": "Cohere-embed-v3-english",
    "input": [
        {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUh..."
        }
    ],
    "input_type": "document"
}
```

When you work on a query to retrieve such a document, you can use the following code snippet to create the embeddings for the query and maximize the retrieval performance.


```json
{
    "model": "Cohere-embed-v3-english",
    "input": [
        {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUh..."
        }
    ],
    "input_type": "query"
}
```

Notice that not all the embedding models support indicating the input type in the request and on those cases a 422 error is returned.
