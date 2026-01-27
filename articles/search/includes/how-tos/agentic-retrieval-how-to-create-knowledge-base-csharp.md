---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/23/2026
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In Azure AI Search, a *knowledge base* is a top-level object that orchestrates [agentic retrieval](../../agentic-retrieval-overview.md). It defines which knowledge sources to query and the default behavior for retrieval operations. At query time, the [retrieve method](../../agentic-retrieval-how-to-retrieve.md) targets the knowledge base to run the configured retrieval pipeline.

You can create a knowledge base in a [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) workload in the Microsoft Foundry (new) portal. You also need a knowledge base in any agentic solutions that you create using the Azure AI Search APIs.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-bases?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.
+ An optional LLM that provides reasoning capabilities for query planning and answer formulation.
+ A retrieval reasoning effort that determines whether an LLM is invoked and manages cost, latency, and quality.
+ Custom properties that control routing, source selection, output format, and object encryption.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

> [!IMPORTANT]
> 2025-11-01-preview renames the 2025-08-01-preview "knowledge agent" to "knowledge base." This is a breaking change. We recommend [migrating existing code](../../agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). If you're using a [managed identity](../../search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic pricing tier or higher.

+ Azure OpenAI with a [supported LLM](#supported-models) deployment.

+ One or more [knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources) on your search service.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md). **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries. Alternatively, you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

+ The latest preview version of the [`Azure.Search.Documents` client library](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1) for the .NET SDK.

### Supported models

Use one of the following LLMs from Azure OpenAI in Foundry Models or an equivalent open-source model. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

## Configure access

Azure AI Search needs access to the LLM from Azure OpenAI. We recommend Microsoft Entra ID for authentication and role-based access for authorization. To assign roles, you must be an **Owner or User Access Administrator**. If you can't use roles, use key-based authentication instead.

### [**Use roles**](#tab/rbac)

1. [Configure Azure AI Search to use a managed identity](../../search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](../../search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

    ```csharp
    using Azure.Search.Documents.Indexes;
    using Azure.Identity;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
    ```

### [**Use keys**](#tab/keys)

1. [Copy an Azure AI Search admin API key](../../search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request. Your code should look similar to the following example:

    ```csharp
    using Azure.Search.Documents.Indexes;
    using Azure;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));
    ```

---

> [!IMPORTANT]
> Code snippets in this article use API keys. If you use role-based authentication, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

## Check for existing knowledge bases

Knowing about existing knowledge bases is helpful for either reusing them or naming new objects. Any 2025-08-01-preview knowledge agents are returned in the knowledge bases collection.

Run the following code to list existing knowledge bases by name.

```csharp
// List knowledge bases by name
  using Azure.Search.Documents.Indexes;
  
  var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
  var knowledgeBases = indexClient.GetKnowledgeBasesAsync();
  
  Console.WriteLine("Knowledge Bases:");
  
  await foreach (var kb in knowledgeBases)
  {
      Console.WriteLine($"  - {kb.Name}");
  }
```

You can also return a single knowledge base by name to review its JSON definition.

```csharp
using Azure.Search.Documents.Indexes;
using System.Text.Json;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

// Specify the knowledge base name to retrieve
string kbNameToGet = "earth-knowledge-base";

// Get a specific knowledge base definition
var knowledgeBaseResponse = await indexClient.GetKnowledgeBaseAsync(kbNameToGet);
var kb = knowledgeBaseResponse.Value;

// Serialize to JSON for display
string json = JsonSerializer.Serialize(kb, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine(json);
```

The following JSON is an example of a knowledge base.

```json
{
  "Name": "earth-knowledge-base",
  "KnowledgeSources": [
    {
      "Name": "earth-knowledge-source"
    }
  ],
  "Models": [
    {}
  ],
  "RetrievalReasoningEffort": {},
  "OutputMode": {},
  "ETag": "\u00220x8DE278629D782B3\u0022",
  "EncryptionKey": null,
  "Description": null,
  "RetrievalInstructions": null,
  "AnswerInstructions": null
}
```

## Create a knowledge base

A knowledge base drives the agentic retrieval pipeline. In application code, other agents or chatbots call it.

A knowledge base connects knowledge sources (searchable content) to an LLM deployment from Azure OpenAI. Properties on the LLM establish the connection, while properties on the knowledge source establish defaults that inform query execution and the response.

Run the following code to create a knowledge base.

```csharp
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

// Create a knowledge base
var knowledgeBase = new KnowledgeBase(
    name: knowledgeBaseName,
    knowledgeSources: new KnowledgeSourceReference[] { new KnowledgeSourceReference(knowledgeSourceName) }
)
{
    RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort(),
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis,
    Models = { model }
};
await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBaseName}' created or updated successfully.");
```

```csharp
# Create a knowledge base
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var aoaiParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel
};

var knowledgeBase = new KnowledgeBase(
    name: "my-kb",
    knowledgeSources: new KnowledgeSourceReference[] 
    { 
        new KnowledgeSourceReference("hotels-sample-knowledge-source"),
        new KnowledgeSourceReference("earth-knowledge-source")
    }
)
{
    Description = "This knowledge base handles questions directed at two unrelated sample indexes.",
    RetrievalInstructions = "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    AnswerInstructions = "Provide a two sentence concise and informative answer based on the retrieved documents.",
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis,
    Models = { new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: aoaiParams) },
    RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort()
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBase.Name}' created or updated successfully.");
```

### Knowledge base properties

Pass the following properties to create a knowledge base.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `knowledgeSources` | One or more [supported knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `Description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `RetrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | Yes |
| `AnswerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](../../agentic-retrieval-how-to-answer-synthesis.md). | String | Yes |
| `OutputMode` | Valid values are `AnswerSynthesis` for an LLM-formulated answer or `ExtractedData` for full search results that you can pass to an LLM as a downstream step. | String | Yes |
| `Models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `Models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. Provide the parameters by using the [KnowledgeBaseAzureOpenAIModel class](/dotnet/api/azure.search.documents.indexes.models.knowledgebaseazureopenaimodel?view=azure-dotnet-preview&preserve-view=true). You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Foundry](/azure/ai-foundry/how-to/deploy-models-openai). | Object | No |
| `RetrievalReasoningEffort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](../../agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

## Query a knowledge base

Set up the instructions and messages to send to the LLM.

```csharp
string instructions = @"
Use the earth at night index to answer the question. If you can't find relevant content, say you don't know.
";

var messages = new List<Dictionary<string, string>>
{
    new Dictionary<string, string>
    {
        { "role", "system" },
        { "content", instructions }
    }
};
```

Call the `retrieve` action on the knowledge base to verify the LLM connection and return results. For more information about the `retrieve` request and response schema, see [Retrieve data using a knowledge base in Azure AI Search](../../agentic-retrieval-how-to-retrieve.md).

Replace "Where does the ocean look green?" with a query string that's valid for your knowledge sources.

```csharp
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var baseClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri(searchEndpoint),
    knowledgeBaseName: knowledgeBaseName,
    tokenCredential: new DefaultAzureCredential()
);

messages.Add(new Dictionary<string, string>
{
    { "role", "user" },
    { "content", @"Where does the ocean look green?" }
});

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
foreach (Dictionary<string, string> message in messages) {
    if (message["role"] != "system") {
        retrievalRequest.Messages.Add(new KnowledgeBaseMessage(content: new[] { new KnowledgeBaseMessageTextContent(message["content"]) }) { Role = message["role"] });
    }
}
retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
var retrievalResult = await baseClient.RetrieveAsync(retrievalRequest);

messages.Add(new Dictionary<string, string>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text }
});

(retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text 

// Print the response, activity, and references
Console.WriteLine("Response:");
Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text);
```

**Key points:**

+ [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true) is the input contract for the retrieval request.

+ [RetrievalReasoningEffort](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest.retrievalreasoningeffort?view=azure-dotnet-preview#azure-search-documents-knowledgebases-models-knowledgebaseretrievalrequest-retrievalreasoningeffort&preserve-view=true) is required. Setting it to `minimal` excludes LLMs from the query pipeline and only intents are used for the query input. The default is `low` and it supports LLM-based query planning and answer synthesis with messages and context.

+ [`knowledgeSourceParams`](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest.knowledgesourceparams?view=azure-dotnet-preview&preserve-view=true) are used to overwrite default parameters at query time.

The response to the sample query might look like the following example:

```http
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "The ocean appears green off the coast of Antarctica due to phytoplankton flourishing in the water, particularly in Granite Harbor near Antarctica’s Ross Sea, where they can grow in large quantities during spring, summer, and even autumn under the right conditions [ref_id:0]. Additionally, off the coast of Namibia, the ocean can also look green due to blooms of phytoplankton and yellow-green patches of sulfur precipitating from bacteria in oxygen-depleted waters [ref_id:1]. In the Strait of Georgia, Canada, the waters turned bright green due to a massive bloom of coccolithophores, a type of phytoplankton [ref_id:5]. Furthermore, a milky green and blue bloom was observed off the coast of Patagonia, Argentina, where nutrient-rich waters from different currents converge [ref_id:6]. Lastly, a large bloom of cyanobacteria was captured in the Baltic Sea, which can also give the water a green appearance [ref_id:9]."
        }
      ]
    }
  ]
```

## Delete a knowledge base

If you no longer need the knowledge base or need to rebuild it on your search service, use this request to delete the object.

```csharp
using Azure.Search.Documents.Indexes;
var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

await indexClient.DeleteKnowledgeBaseAsync(knowledgeBaseName);
System.Console.WriteLine($"Knowledge base '{knowledgeBaseName}' deleted successfully.");
```
