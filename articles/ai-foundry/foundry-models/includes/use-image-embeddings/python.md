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

[!INCLUDE [how-to-prerequisites-python](../how-to-prerequisites-python.md)]

* An image embeddings model deployment. If you don't have one, read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add an embeddings model to your resource.

  * This example uses `Cohere-embed-v3-english` from Cohere.


## Use image embeddings

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.ai.inference import ImageEmbeddingsClient
from azure.core.credentials import AzureKeyCredential

client = ImageEmbeddingsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    model="Cohere-embed-v3-english"
)
```

If you configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

```python
import os
from azure.ai.inference import ImageEmbeddingsClient
from azure.identity import DefaultAzureCredential

client = ImageEmbeddingsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    model="Cohere-embed-v3-english"
)
```

### Create embeddings

To create image embeddings, you need to pass the image data as part of your request. Image data should be in PNG format and encoded as base64.

```python
from azure.ai.inference.models import ImageEmbeddingInput

image_input= ImageEmbeddingInput.load(image_file="sample1.png", image_format="png")
response = client.embed(
    input=[ image_input ],
)
```

> [!TIP]
> When creating a request, take into account the token's input limit for the model. If you need to embed larger portions of text, you would need a chunking strategy.

The response is as follows, where you can see the model's usage statistics:


```python
import numpy as np

for embed in response.data:
    print("Embedding of size:", np.asarray(embed.embedding).shape)

print("Model:", response.model)
print("Usage:", response.usage)
```

> [!IMPORTANT]
> Computing embeddings in batches may not be supported for all the models. For example, for `Cohere-embed-v3-english` model, you need to send one image at a time.

#### Embedding images and text pairs

Some models can generate embeddings from images and text pairs. In this case, you can use the `image` and `text` fields in the request to pass the image and text to the model. The following example shows how to create embeddings for images and text pairs:


```python
text_image_input= ImageEmbeddingInput.load(image_file="sample1.png", image_format="png")
text_image_input.text = "A cute baby sea otter"
response = client.embed(
    input=[ text_image_input ],
)
```

#### Create different types of embeddings

Some models can generate multiple embeddings for the same input depending on how you plan to use them. This capability allows you to retrieve more accurate embeddings for RAG patterns. 

The following example shows how to create embeddings that are used to create an embedding for a document that will be stored in a vector database:


```python
from azure.ai.inference.models import EmbeddingInputType

response = client.embed(
    input=[ image_input ],
    input_type=EmbeddingInputType.DOCUMENT,
)
```

When you work on a query to retrieve such a document, you can use the following code snippet to create the embeddings for the query and maximize the retrieval performance.


```python
from azure.ai.inference.models import EmbeddingInputType

response = client.embed(
    input=[ image_input ],
    input_type=EmbeddingInputType.QUERY,
)
```

Notice that not all the embedding models support indicating the input type in the request and on those cases a 422 error is returned.
