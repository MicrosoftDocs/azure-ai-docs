---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

```python
response = client.embed(
    input=[
        "Explain Riemann's conjecture in 1 paragraph",
    ],
    model="Cohere-embed-v3-multilingual"
)

print(response.data.embeddings)
```

# [JavaScript](#tab/javascript)

```javascript
var response = await client.path("/embeddings").post({
    body: {
        input: "Explain Riemann's conjecture in 1 paragraph",
        model: "Cohere-embed-v3-multilingual"
    }
});

console.log(response.data.embeddings)
```

# [C#](#tab/csharp)

```csharp
requestOptions = new EmbeddingsOptions()
{
    input = [
        "Explain Riemann's conjecture in 1 paragraph"
    ],
    Model = "Cohere-embed-v3-multilingual"
};

response = client.Embed(requestOptions);
Console.WriteLine($"Response: {response.Data.Embeddings}");
```

# [REST](#tab/rest)

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/models/embeddings?api-version=2024-05-01-preview
api-key: <api-key>
Content-Type: application/json
```

```JSON
{
    "input": [
        "Explain Riemann's conjecture in 1 paragraph"
    ],
    "model": "Cohere-embed-v3-multilingual"
}
```

__Response__

```json
{
  "data": [
    {
      "index": 0,
      "object": "embedding",
      "embedding": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    }
  ],
  "object": "list",
  "model": "Cohere-embed-v3-multilingual",
  "usage": {
    "prompt_tokens": 15,
    "total_tokens": 15
  }
}
```

---
