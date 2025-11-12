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

[!INCLUDE [how-to-prerequisites-csharp](../how-to-prerequisites-csharp.md)]

* An image embeddings model deployment. If you don't have one, read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add an embeddings model to your resource.

  * This example uses `Cohere-embed-v3-english` from Cohere.

## Use image embeddings

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
ImageEmbeddingsClient client = new ImageEmbeddingsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

If you configured the resource with **Microsoft Entra ID** support, you can use the following code snippet to create a client. Notice that `includeInteractiveCredentials` is set to `true` only for demonstration purposes so authentication can happen using the web browser. For production workloads, you should remove the parameter.

```csharp
TokenCredential credential = new DefaultAzureCredential(includeInteractiveCredentials: true);
AzureAIInferenceClientOptions clientOptions = new AzureAIInferenceClientOptions();
BearerTokenAuthenticationPolicy tokenPolicy = new BearerTokenAuthenticationPolicy(credential, new string[] { "https://cognitiveservices.azure.com/.default" });

clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);

ImageEmbeddingsClient client = new ImageEmbeddingsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    credential,
    clientOptions
);
```

### Create embeddings

To create image embeddings, you need to pass the image data as part of your request. Image data should be in PNG format and encoded as base64.

```csharp
List<ImageEmbeddingInput> input = new List<ImageEmbeddingInput>
{
    ImageEmbeddingInput.Load(imageFilePath:"sampleImage.png", imageFormat:"png")
};

var requestOptions = new ImageEmbeddingsOptions()
{
    Input = input,
    Model = "Cohere-embed-v3-english"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

> [!TIP]
> When creating a request, take into account the token's input limit for the model. If you need to embed larger portions of text, you would need a chunking strategy.

The response is as follows, where you can see the model's usage statistics:


```csharp
foreach (EmbeddingItem item in response.Value.Data)
{
    List<float> embedding = item.Embedding.ToObjectFromJson<List<float>>();
    Console.WriteLine($"Index: {item.Index}, Embedding: <{string.Join(", ", embedding)}>");
}
```

> [!IMPORTANT]
> Computing embeddings in batches might not be supported for all the models. For example, for `Cohere-embed-v3-english` model, you need to send one image at a time.

#### Embedding images and text pairs

Some models can generate embeddings from images and text pairs. In this case, you can use the `image` and `text` fields in the request to pass the image and text to the model. The following example shows how to create embeddings for images and text pairs:


```csharp
var image_input = ImageEmbeddingInput.Load(imageFilePath:"sampleImage.png", imageFormat:"png")
image_input.text = "A cute baby sea otter"

var requestOptions = new ImageEmbeddingsOptions()
{
    Input = new List<ImageEmbeddingInput>
    {
        image_input
    },
    Model = "Cohere-embed-v3-english"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

#### Create different types of embeddings

Some models can generate multiple embeddings for the same input depending on how you plan to use them. This capability allows you to retrieve more accurate embeddings for RAG patterns. 

The following example shows how to create embeddings for a document that will be stored in a vector database:


```csharp
var requestOptions = new EmbeddingsOptions()
{
    Input = image_input,
    InputType = EmbeddingInputType.DOCUMENT, 
    Model = "Cohere-embed-v3-english"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

When you work on a query to retrieve such a document, you can use the following code snippet to create the embeddings for the query and maximize the retrieval performance.


```csharp
var requestOptions = new EmbeddingsOptions()
{
    Input = image_input,
    InputType = EmbeddingInputType.QUERY,
    Model = "Cohere-embed-v3-english"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

Notice that not all the embedding models support indicating the input type in the request and on those cases a 422 error is returned.
