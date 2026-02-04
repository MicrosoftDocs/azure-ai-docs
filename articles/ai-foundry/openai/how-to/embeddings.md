---
title: 'How to generate embeddings with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to generate embeddings with Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-python
ms.topic: how-to
ms.date: 11/26/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
monikerRange: 'foundry-classic || foundry'
---

# Learn how to generate embeddings

An embedding is a special format of data representation that can be easily utilized by machine learning models and algorithms. The embedding is an information dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating point numbers, such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar. Embeddings power vector similarity search in Azure Databases such as [Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/vector-search), [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search), [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search) or [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector).

## How to get embeddings

To obtain an embedding vector for a piece of text, make a request to the embeddings endpoint as shown in the following code snippets:

> [!NOTE]
> The Azure OpenAI embeddings API does not currently support Microsoft Entra ID with the v1 API.

# [C#](#tab/csharp)

```csharp
using OpenAI;
using OpenAI.Embeddings;
using System.ClientModel;

EmbeddingClient client = new(
    "text-embedding-3-small",
    credential: new ApiKeyCredential("API-KEY"),
    options: new OpenAIClientOptions()
    {

        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

string input = "This is a test";

OpenAIEmbedding embedding = client.GenerateEmbedding(input);
ReadOnlyMemory<float> vector = embedding.ToFloats();
Console.WriteLine($"Embeddings: [{string.Join(", ", vector.ToArray())}]");
```

# [Go](#tab/go)

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/option"
)

func main() {
	// Get API key from environment variable
	apiKey := os.Getenv("AZURE_OPENAI_API_KEY")
	if apiKey == "" {
		panic("AZURE_OPENAI_API_KEY environment variable is not set")
	}

	// Create a client with Azure OpenAI endpoint and API key
	client := openai.NewClient(
		option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
		option.WithAPIKey(apiKey),
	)

	ctx := context.Background()
	text := "The attention mechanism revolutionized natural language processing"

	// Make an embedding request
	embedding, err := client.Embeddings.New(ctx, openai.EmbeddingNewParams{
		Input: openai.EmbeddingNewParamsInputUnion{OfString: openai.String(text)},
		Model: "text-embedding-3-large", // Use your deployed model name on Azure
	})
	if err != nil {
		panic(err.Error())
	}

	// Print embedding information
	fmt.Printf("Model: %s\n", embedding.Model)
	fmt.Printf("Number of embeddings: %d\n", len(embedding.Data))
	fmt.Printf("Embedding dimensions: %d\n", len(embedding.Data[0].Embedding))
	fmt.Printf("Usage - Prompt tokens: %d, Total tokens: %d\n", embedding.Usage.PromptTokens, embedding.Usage.TotalTokens)
	
	// Print first few values of the embedding vector
	fmt.Printf("First 10 embedding values: %v\n", embedding.Data[0].Embedding[:10])
}
```

# [JavaScript](#tab/javascript)

```javascript
import OpenAI from "openai";
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: process.env['OPENAI_API_KEY'] //Your Azure OpenAI API key
});

const embedding = await client.embeddings.create({
  model: "text-embedding-3-small",
  input: "Your text string goes here",
});

console.log(embedding);
```


# [Python](#tab/python-new)

```python
import os
from openai import OpenAI

client = OpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
)

response = client.embeddings.create(
    input = "Your text string goes here",
    model= "text-embedding-3-large"
)

print(response.model_dump_json(indent=2))
```

# [PowerShell](#tab/PowerShell)

```powershell-interactive
# Azure OpenAI metadata variables
$openai = @{
    api_key     = $Env:AZURE_OPENAI_API_KEY
    api_base    = $Env:AZURE_OPENAI_ENDPOINT # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    name        = 'YOUR-DEPLOYMENT-NAME-HERE' #This will correspond to the custom name you chose for your deployment when you deployed a model.
}

$headers = [ordered]@{
    'api-key' = $openai.api_key
}

$text = 'Your text string goes here'

$body = [ordered]@{
    input = $text
} | ConvertTo-Json

$url = "$($openai.api_base)/openai/v1/embeddings"

$response = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json'
return $response.data.embedding
```

# [REST](#tab/console)

```console
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/embeddings \
  -H 'Content-Type: application/json' \
  -H 'api-key: YOUR_API_KEY' \
  -d '{"input": "Sample Document goes here"}'
```

---

## Best practices

### Verify inputs don't exceed the maximum length

- The maximum length of input text for our latest embedding models is 8,192 tokens. You should verify that your inputs don't exceed this limit before making a request.
- If sending an array of inputs in a single embedding request the max array size is 2048.
- When sending an array of inputs in a single request, remember that the number of tokens per minute in your requests must remain below the quota limit that was assigned at model deployment. By default, the latest generation 3 embeddings models are subject to a 350 K TPM per region limit.  


## Limitations & risks

Our embedding models may be unreliable or pose social risks in certain cases, and may cause harm in the absence of mitigations. Review our Responsible AI content for more information on how to approach their use responsibly.

## Next steps

* Learn more about using Azure OpenAI and embeddings to perform document search with our [embeddings tutorial](../tutorials/embeddings.md).
* Learn more about the [underlying models that power Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md).
* Store your embeddings and perform vector (similarity) search using your choice of service:
  * [Azure AI Search](/azure/search/vector-search-overview)
  * [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search)
  * [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search)
  * [Azure Cosmos DB for NoSQL](/azure/cosmos-db/vector-search)
  * [Azure Cosmos DB for PostgreSQL](/azure/cosmos-db/postgresql/howto-use-pgvector)
  * [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector)  
  * [Azure Cache for Redis](/azure/azure-cache-for-redis/cache-tutorial-vector-similarity)
  * [Use Eventhouse as a vector database - Real-Time Intelligence in Microsoft Fabric](/fabric/real-time-intelligence/vector-database)
