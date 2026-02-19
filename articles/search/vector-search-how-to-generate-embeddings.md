---
title: Generate Embeddings
titleSuffix: Azure AI Search
description: Learn how to generate embeddings for downstream indexing into an Azure AI Search index.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 08/06/2025
---

# Generate embeddings for search queries and documents

Azure AI Search doesn't host embedding models, so you're responsible for creating vectors for query inputs and outputs. Choose one of the following approaches:

| Approach | Description |
| --- | --- |
| [Integrated vectorization](vector-search-integrated-vectorization.md) | Use built-in data chunking and vectorization in Azure AI Search. This approach takes a dependency on indexers, skillsets, and built-in or custom skills that point to external embedding models, such as those in Microsoft Foundry. |
| Manual vectorization | Manage data chunking and vectorization yourself. For indexing, you [push prevectorized documents](vector-search-how-to-create-index.md#load-vector-data-for-indexing) into vector fields in a search index. For querying, you [provide precomputed vectors](#generate-an-embedding-for-an-improvised-query) to the search engine. For demos of this approach, see the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples/tree/main) GitHub repository. |

We recommend integrated vectorization for most scenarios. Although you can use any supported embedding model, this article uses Azure OpenAI models for illustration.

## How embedding models are used in vector queries

Embedding models generate vectors for both query inputs and query outputs. Query inputs include:

+ **Text or images that are converted to vectors during query processing**. As part of integrated vectorization, a [vectorizer](vector-search-how-to-configure-vectorizer.md) performs this task.

+ **Precomputed vectors**. You can generate these vectors by passing the query input to an embedding model of your choice. To avoid [rate limiting](/azure/ai-services/openai/quotas-limits), implement retry logic in your workload. Our [Python demo](https://github.com/Azure/azure-search-vector-samples/tree/93c839591bf92c2f10001d287871497b0f204a7c/demo-python) uses [tenacity](https://pypi.org/project/tenacity/).

Based on the query input, the search engine retrieves matching documents from your search index. These documents are the query outputs.

Your search index must already contain documents with one or more vector fields populated by embeddings. You can create these embeddings through integrated or manual vectorization. To ensure accurate results, use the same embedding model for indexing and querying.

## Tips for embedding model integration

+ **Identify use cases**. Evaluate specific use cases where embedding model integration for vector search features adds value to your search solution. Examples include [multimodal search](multimodal-search-overview.md) or matching image content with text content, multilingual search, and similarity search.

+ **Design a chunking strategy**. Embedding models have limits on the number of tokens they accept, so [data chunking](vector-search-how-to-chunk-documents.md) is necessary for large files.

+ **Optimize cost and performance**. Vector search is resource intensive and subject to maximum limits, so vectorize only the fields that contain semantic meaning. [Reduce vector size](vector-search-how-to-configure-compression-storage.md) to store more vectors for the same price.

+ **Choose the right embedding model**. Select a model for your use case, such as word embeddings for text-based searches or image embeddings for visual searches. Consider pretrained models, such as text-embedding-ada-002 from OpenAI or the Image Retrieval REST API from [Azure Vision in Foundry Tools](/azure/ai-services/computer-vision/how-to/image-retrieval).

+ **Normalize vector lengths**. To improve the accuracy and performance of similarity search, normalize vector lengths before you store them in a search index. Most pretrained models are already normalized.

+ **Fine-tune the model**. If needed, fine-tune the model on your domain-specific data to improve its performance and relevance to your search application.

+ **Test and iterate**. Continuously test and refine the embedding model integration to achieve your desired search performance and user satisfaction.

## Create resources in the same region

Although integrated vectorization with Azure OpenAI embedding models doesn't require resources to be in the same region, using the same region can improve performance and reduce latency.

To use the same region for your resources:

1. Check the [regional availability of text embedding models](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).

1. Check the [regional availability of Azure AI Search](search-region-support.md).

1. Create an Azure OpenAI resource and Azure AI Search service in the same region.

> [!TIP]
> Want to use [semantic ranking](semantic-how-to-query-request.md) for [hybrid queries](hybrid-search-overview.md) or a machine learning model in a [custom skill](cognitive-search-custom-skill-interface.md) for [AI enrichment](cognitive-search-concept-intro.md)? Choose an Azure AI Search region that provides those features.

## Choose an embedding model in Foundry

When you add knowledge to an agent workflow in the [Foundry portal](https://ai.azure.com/?cid=learnDocs), you have the option of creating a search index. A wizard guides you through the steps.

One step involves selecting an embedding model to vectorize your plain text content. The following models are supported:

+ text-embedding-3-small
+ text-embedding-3-large
+ text-embedding-ada-002
+ Cohere-embed-v3-english
+ Cohere-embed-v3-multilingual

Your model must already be deployed, and you must have permission to access it. For more information, see [Deployment overview for Foundry Models](/azure/ai-foundry/concepts/deployments-overview).

## Generate an embedding for an improvised query

If you don't want to use integrated vectorization, you can manually generate an embedding and paste it into the `vectorQueries.vector` property of a vector query. For more information, see [Create a vector query in Azure AI Search](vector-search-how-to-query.md).

The following examples assume the text-embedding-ada-002 model. Replace `YOUR-API-KEY` and `YOUR-OPENAI-RESOURCE` with your Azure OpenAI resource details.

### [.NET](#tab/dotnet)

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

class Program
{
    static async Task Main(string[] args)
    {
        var apiKey = "YOUR-API-KEY";
        var apiBase = "https://YOUR-OPENAI-RESOURCE.openai.azure.com";
        var apiVersion = "2024-02-01";
        var engine = "text-embedding-ada-002";

        var client = new HttpClient();
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");

        var requestBody = new
        {
            input = "How do I use C# in VS Code?"
        };

        var response = await client.PostAsync(
            $"{apiBase}/openai/deployments/{engine}/embeddings?api-version={apiVersion}",
            new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json")
        );

        var responseBody = await response.Content.ReadAsStringAsync();
        Console.WriteLine(responseBody);
    }
}
```

### [Java](#tab/java)

```java
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) {
        String apiKey = "YOUR-API-KEY";
        String apiBase = "https://YOUR-OPENAI-RESOURCE.openai.azure.com";
        String engine = "text-embedding-ada-002";
        String apiVersion = "2024-02-01";

        try {
            URL url = new URL(String.format("%s/openai/deployments/%s/embeddings?api-version=%s", apiBase, engine, apiVersion));
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey);
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String requestBody = "{\"input\": \"How do I use Java in VS Code?\"}";

            try (OutputStream os = connection.getOutputStream()) {
                os.write(requestBody.getBytes());
            }

            try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
                System.out.println(response);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### [JavaScript](#tab/javascript)

```javascript
const apiKey = "YOUR-API-KEY";
const apiBase = "https://YOUR-OPENAI-RESOURCE.openai.azure.com";
const engine = "text-embedding-ada-002";
const apiVersion = "2024-02-01";

async function generateEmbedding() {
  const response = await fetch(
    `${apiBase}/openai/deployments/${engine}/embeddings?api-version=${apiVersion}`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: "How do I use JavaScript in VS Code?",
      }),
    }
  );

  const data = await response.json();
  console.log(data.data[0].embedding);
}

generateEmbedding();
```

### [Python](#tab/python)

```python
!pip install openai

import openai

openai.api_type = "azure"
openai.api_key = "YOUR-API-KEY"
openai.api_base = "https://YOUR-OPENAI-RESOURCE.openai.azure.com"
openai.api_version = "2024-02-01"

response = openai.Embedding.create(
    input="How do I use Python in VS Code?",
    engine="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']
print(embeddings)
```

### [REST API](#tab/rest-api)

```http
POST https://YOUR-OPENAI-RESOURCE.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-02-01
  Authorization: Bearer YOUR-API-KEY
  Content-Type: application/json
    
  {
    "input": "How do I use REST APIs in VS Code?"
  }
```

---

The output is a vector array of 1,536 dimensions.

## Related content

+ [Understand embeddings in Azure OpenAI in Foundry Models](/azure/ai-services/openai/concepts/understand-embeddings)
+ [Generate embeddings with Azure OpenAI](/azure/ai-services/openai/how-to/embeddings?tabs=console)
+ [Tutorial: Explore Azure OpenAI embeddings and document search](/azure/ai-services/openai/tutorials/embeddings?tabs=command-line)
