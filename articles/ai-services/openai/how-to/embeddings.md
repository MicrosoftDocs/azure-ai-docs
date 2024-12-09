---
title: 'How to generate embeddings with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to generate embeddings with Azure OpenAI
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.custom: devx-track-python
ms.topic: how-to
ms.date: 08/29/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---
# Learn how to generate embeddings with Azure OpenAI

An embedding is a special format of data representation that can be easily utilized by machine learning models and algorithms. The embedding is an information dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating point numbers, such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar. Embeddings power vector similarity search in Azure Databases such as [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search) , [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search) or [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector).

## How to get embeddings

To obtain an embedding vector for a piece of text, we make a request to the embeddings endpoint as shown in the following code snippets:

# [console](#tab/console)
```console
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings?api-version=2024-02-01\
  -H 'Content-Type: application/json' \
  -H 'api-key: YOUR_API_KEY' \
  -d '{"input": "Sample Document goes here"}'
```

# [OpenAI Python 1.x](#tab/python-new)

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-06-01",
  azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
)

response = client.embeddings.create(
    input = "Your text string goes here",
    model= "text-embedding-3-large"
)

print(response.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

[!INCLUDE [Deprecation](../includes/deprecation.md)]

```python
import openai

openai.api_type = "azure"
openai.api_key = "YOUR_API_KEY"
openai.api_base = "https://YOUR_RESOURCE_NAME.openai.azure.com"
openai.api_version = "2024-06-01"

response = openai.Embedding.create(
    input="Your text string goes here",
    engine="YOUR_DEPLOYMENT_NAME"
)
embeddings = response['data'][0]['embedding']
print(embeddings)
```

# [C#](#tab/csharp)
```csharp
using Azure;
using Azure.AI.OpenAI;

Uri oaiEndpoint = new ("https://YOUR_RESOURCE_NAME.openai.azure.com");
string oaiKey = "YOUR_API_KEY";

AzureKeyCredential credentials = new (oaiKey);

OpenAIClient openAIClient = new (oaiEndpoint, credentials);

EmbeddingsOptions embeddingOptions = new()
{
    DeploymentName = "text-embedding-3-large",
    Input = { "Your text string goes here" },
};

var returnValue = openAIClient.GetEmbeddings(embeddingOptions);

foreach (float item in returnValue.Value.Data[0].Embedding.ToArray())
{
    Console.WriteLine(item);
}
```

# [PowerShell](#tab/PowerShell)
```powershell-interactive
# Azure OpenAI metadata variables
$openai = @{
    api_key     = $Env:AZURE_OPENAI_API_KEY
    api_base    = $Env:AZURE_OPENAI_ENDPOINT # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version = '2024-02-01' # this may change in the future
    name        = 'YOUR-DEPLOYMENT-NAME-HERE' #This will correspond to the custom name you chose for your deployment when you deployed a model.
}

$headers = [ordered]@{
    'api-key' = $openai.api_key
}

$text = 'Your text string goes here'

$body = [ordered]@{
    input = $text
} | ConvertTo-Json

$url = "$($openai.api_base)/openai/deployments/$($openai.name)/embeddings?api-version=$($openai.api_version)"

$response = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json'
return $response.data.embedding
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
* Learn more about the [underlying models that power Azure OpenAI](../concepts/models.md).
* Store your embeddings and perform vector (similarity) search using your choice of service:
  * [Azure AI Search](/azure/search/vector-search-overview)
  * [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search)
  * [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search)
  * [Azure Cosmos DB for NoSQL](/azure/cosmos-db/vector-search)
  * [Azure Cosmos DB for PostgreSQL](/azure/cosmos-db/postgresql/howto-use-pgvector)
  * [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector)  
  * [Azure Cache for Redis](/azure/azure-cache-for-redis/cache-tutorial-vector-similarity)
  * [Use Eventhouse as a vector database - Real-Time Intelligence in Microsoft Fabric](/fabric/real-time-intelligence/vector-database)
