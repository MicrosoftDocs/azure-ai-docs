---
title: How to generate embeddings with Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to generate embeddings with Microsoft Foundry Models
author: msakande
reviewer: santiagxf
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 05/29/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use embeddings API with models deployed in Microsoft Foundry Models.

## Prerequisites

To use embedding models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-csharp](../how-to-prerequisites-csharp.md)]

* An embeddings model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add an embeddings model to your resource.


## Use embeddings

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
EmbeddingsClient client = new EmbeddingsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

If you configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client. Note that here `includeInteractiveCredentials` is set to `true` only for demonstration purposes so authentication can happen using the web browser. On production workloads, you should remove such parameter.

```csharp
TokenCredential credential = new DefaultAzureCredential(includeInteractiveCredentials: true);
AzureAIInferenceClientOptions clientOptions = new AzureAIInferenceClientOptions();
BearerTokenAuthenticationPolicy tokenPolicy = new BearerTokenAuthenticationPolicy(credential, new string[] { "https://cognitiveservices.azure.com/.default" });

clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);

client = new EmbeddingsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    credential,
    clientOptions,
);
```

### Create embeddings

Create an embedding request to see the output of the model.

```csharp
EmbeddingsOptions requestOptions = new EmbeddingsOptions()
{
    Input = {
        "The ultimate answer to the question of life"
    },
    Model = "text-embedding-3-small"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

> [!TIP]
> When creating a request, take into account the token's input limit for the model. If you need to embed larger portions of text, you would need a chunking strategy.

The response is as follows, where you can see the model's usage statistics:


```csharp
Console.WriteLine($"Embedding: {response.Value.Data}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
```

It can be useful to compute embeddings in input batches. The parameter `inputs` can be a list of strings, where each string is a different input. In turn the response is a list of embeddings, where each embedding corresponds to the input in the same position.


```csharp
EmbeddingsOptions requestOptions = new EmbeddingsOptions()
{
    Input = {
        "The ultimate answer to the question of life", 
        "The largest planet in our solar system is Jupiter"
    },
    Model = "text-embedding-3-small"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

The response is as follows, where you can see the model's usage statistics:

> [!TIP]
> When creating batches of request, take into account the batch limit for each of the models. Most models have a 1024 batch limit.

#### Specify embeddings dimensions

You can specify the number of dimensions for the embeddings. The following example code shows how to create embeddings with 1024 dimensions. Notice that not all the embedding models support indicating the number of dimensions in the request and on those cases a 422 error is returned.

#### Create different types of embeddings

Some models can generate multiple embeddings for the same input depending on how you plan to use them. This capability allows you to retrieve more accurate embeddings for RAG patterns. 

The following example shows how to create embeddings that are used to create an embedding for a document that will be stored in a vector database:


```csharp
var input = new List<string> { 
    "The answer to the ultimate question of life, the universe, and everything is 42"
};
var requestOptions = new EmbeddingsOptions()
{
    Input = input,
    InputType = EmbeddingInputType.DOCUMENT, 
    Model = "text-embedding-3-small"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

When you work on a query to retrieve such a document, you can use the following code snippet to create the embeddings for the query and maximize the retrieval performance.


```csharp
var input = new List<string> { 
    "What's the ultimate meaning of life?"
};
var requestOptions = new EmbeddingsOptions()
{
    Input = input,
    InputType = EmbeddingInputType.QUERY,
    Model = "text-embedding-3-small"
};

Response<EmbeddingsResult> response = client.Embed(requestOptions);
```

Notice that not all the embedding models support indicating the input type in the request and on those cases a 422 error is returned. By default, embeddings of type `Text` are returned.
