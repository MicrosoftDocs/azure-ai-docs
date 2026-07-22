---
title: Azure OpenAI embeddings guidance
description: Generate vector embeddings with Azure OpenAI by using current OpenAI SDKs for Python, C#, JavaScript, Java, and Go, or the REST API.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

An embedding is a vector of floating-point numbers that represents the semantic meaning of text. Similar text produces vectors that are close together, which makes embeddings useful for vector search, recommendations, classification, and clustering.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/) if you don't have one.
- An Azure OpenAI resource with an embedding model deployment.
- Your resource endpoint, such as `https://YOUR-RESOURCE-NAME.openai.azure.com`.
- Your resource API key. The v1 embeddings API limitation described in the next section requires key authentication for these examples.
- The runtime and package manager for the language you select.

For more language-specific setup guidance, see [Azure OpenAI supported programming languages](../supported-languages.md).

The `model` value in each request is your Azure model deployment name. The examples use `text-embedding-3-small`; replace it if your deployment has a different name.

## Generate an embedding

Send text to the embeddings endpoint, and read the vector from the first item in the response.

> [!NOTE]
> The Azure OpenAI embeddings API doesn't currently support Microsoft Entra ID with the v1 API. Use API key authentication for the examples in this article.

Set the API key environment variable before you run an SDK example:

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

# [Python](#tab/python-new)

Install the OpenAI package:

```bash
pip install openai
```

Generate an embedding and print its dimensions:

```python
import os
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
openai = OpenAI(
	base_url=endpoint,
	api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# Generate one embedding vector.
response = openai.embeddings.create(
	model="text-embedding-3-small",
	input="The quick brown fox jumped over the lazy dog.",
)
print(f"Embedding dimensions: {len(response.data[0].embedding)}")
```

```output
Embedding dimensions: <number>
```

Reference: [`embeddings.create`](https://github.com/openai/openai-python/blob/main/src/openai/resources/embeddings.py)

# [C#](#tab/csharp)

Install the OpenAI package:

```dotnetcli
dotnet add package OpenAI
```

Generate an embedding and print its dimensions:

```csharp
using OpenAI;
using OpenAI.Embeddings;
using System.ClientModel;

var endpoint = new Uri(
	"https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/");
var apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
	?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY is required.");
var openAIClient = new EmbeddingClient(
	model: "text-embedding-3-small",
	credential: new ApiKeyCredential(apiKey),
	options: new OpenAIClientOptions { Endpoint = endpoint });

// Generate one embedding vector.
OpenAIEmbedding embedding = openAIClient.GenerateEmbedding(
	"The quick brown fox jumped over the lazy dog.");
Console.WriteLine($"Embedding dimensions: {embedding.ToFloats().Length}");
```

```output
Embedding dimensions: <number>
```

Reference: [`EmbeddingClient.GenerateEmbedding`](https://github.com/openai/openai-dotnet/blob/main/OpenAI/src/Custom/Embeddings/EmbeddingClient.cs)

# [JavaScript](#tab/javascript)

Install the OpenAI package:

```bash
npm install openai
```

Generate an embedding and print its dimensions:

```javascript
import OpenAI from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
if (!apiKey) throw new Error("AZURE_OPENAI_API_KEY is required.");
const openai = new OpenAI({ baseURL: endpoint, apiKey });

// Generate one embedding vector.
const response = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: "The quick brown fox jumped over the lazy dog.",
});
console.log(`Embedding dimensions: ${response.data[0].embedding.length}`);
```

```output
Embedding dimensions: <number>
```

Reference: [`embeddings.create`](https://github.com/openai/openai-node/blob/main/src/resources/embeddings.ts)

# [Java](#tab/java)

Add the current `com.openai:openai-java` package to your Maven or Gradle project. For package setup, see [Azure OpenAI Java support](../supported-languages.md?pivots=programming-language-java#install-the-packages).

Generate an embedding and print its dimensions:

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.EmbeddingCreateParams;

public class EmbeddingsExample {
	public static void main(String[] args) {
		String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
		String apiKey = System.getenv("AZURE_OPENAI_API_KEY");
		if (apiKey == null) throw new IllegalStateException(
				"AZURE_OPENAI_API_KEY is required.");
		OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
				.baseUrl(endpoint).apiKey(apiKey).build();

		// Generate one embedding vector.
		EmbeddingCreateParams params = EmbeddingCreateParams.builder()
				.model("text-embedding-3-small")
				.input("The quick brown fox jumped over the lazy dog.")
				.encodingFormat(EmbeddingCreateParams.EncodingFormat.FLOAT)
				.build();
		int dimensions = openAIClient.embeddings().create(params)
				.data().get(0).embedding().size();
		System.out.println("Embedding dimensions: " + dimensions);
	}
}
```

```output
Embedding dimensions: <number>
```

Reference: [`EmbeddingCreateParams`](https://github.com/openai/openai-java/blob/main/openai-java-example/src/main/java/com/openai/example/EmbeddingsExample.java)

# [Go](#tab/go)

Install version 3 of the OpenAI Go module:

```bash
go get github.com/openai/openai-go/v3
```

Generate an embedding and print its dimensions:

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
)

func main() {
	apiKey := os.Getenv("AZURE_OPENAI_API_KEY")
	if apiKey == "" { panic("AZURE_OPENAI_API_KEY is required") }
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(
		option.WithBaseURL(endpoint), option.WithAPIKey(apiKey))

	// Generate one embedding vector.
	response, err := openaiClient.Embeddings.New(context.Background(), openai.EmbeddingNewParams{
		Model: "text-embedding-3-small",
		Input: openai.EmbeddingNewParamsInputUnion{OfString: openai.String(
			"The quick brown fox jumped over the lazy dog.")},
	})
	if err != nil { panic(err) }
	fmt.Printf("Embedding dimensions: %d\n", len(response.Data[0].Embedding))
}
```

```output
Embedding dimensions: <number>
```

Reference: [`Embeddings.New`](https://github.com/openai/openai-go/blob/main/embedding.go)

# [PowerShell](#tab/PowerShell)

Store your resource endpoint in `AZURE_OPENAI_ENDPOINT` and your API key in `AZURE_OPENAI_API_KEY`. Then generate an embedding:

```powershell
$Env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com"
$Env:AZURE_OPENAI_API_KEY = "<your-api-key>"
```

```powershell
$endpoint = "$($env:AZURE_OPENAI_ENDPOINT.TrimEnd('/'))/openai/v1/embeddings"
$headers = @{ "api-key" = $env:AZURE_OPENAI_API_KEY }

# Generate one embedding vector.
$body = @{
    model = "text-embedding-3-small"
    input = "The quick brown fox jumped over the lazy dog."
} | ConvertTo-Json
$response = Invoke-RestMethod `
    -Uri $endpoint `
    -Method Post `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
Write-Output "Embedding dimensions: $($response.data[0].embedding.Count)"
```

```output
Embedding dimensions: <number>
```

Reference: [`Invoke-RestMethod`](/powershell/module/microsoft.powershell.utility/invoke-restmethod)

# [REST](#tab/console)

Set `AZURE_OPENAI_API_KEY` to your resource key, and send a request to the v1 embeddings endpoint:

```bash
curl "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/embeddings" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{"model":"text-embedding-3-small","input":"The quick brown fox."}'
```

```output
{"data":[{"embedding":[<vector-values>]}]}
```

---

## Best practices

> [!TIP]
> Embedding requests return HTTP 400 when the **sum** of input tokens exceeds 300,000, even if every individual input is under the per-input limit. Split large batches into smaller requests.

### Verify inputs don't exceed the maximum length

- The maximum input length for the current embedding models is 8,192 tokens. Check each input before sending the request.
- If you send an array of inputs in a single embedding request, the maximum array size is 2,048.
- Each `/embeddings` request has a 300,000-token aggregate limit across all inputs. Requests above this limit fail with HTTP 400.
- Keep the total tokens per minute below the quota assigned to your model deployment. For current limits, see [Azure OpenAI quotas and limits](../quotas-limits.md).

## Troubleshooting

- For a `401` or `403` response, confirm that the API key belongs to the intended Azure OpenAI resource.
- For a `404` response, confirm that the endpoint includes `/openai/v1/` and that `model` contains a valid deployment name.
- For a `400` response, check the request body, each input's token count, the number of inputs, and the aggregate token count.

## Limitations and risks

Embedding models might be unreliable or pose social risks in certain cases. They might cause harm if used without mitigations. For more information about how to approach their use responsibly, see the [Responsible AI](/azure/foundry/responsible-use-of-ai-overview) content.

## Next steps

- [Explore embeddings and document search](../tutorials/embeddings.md).
- [Review available Azure OpenAI models](../../foundry-models/concepts/models-sold-directly-by-azure.md).
- Choose a service to store and search vectors:
	- [Azure AI Search](/azure/search/vector-search-overview)
	- [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search)
	- [Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/vector-search)
	- [Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/how-to-use-pgvector)
	- [Azure Managed Redis](/azure/redis/overview-vector-similarity)
	- [Eventhouse in Microsoft Fabric](/fabric/real-time-intelligence/vector-database)
