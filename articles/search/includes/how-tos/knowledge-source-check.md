---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

::: zone pivot="csharp"

```csharp
// List knowledge sources by name and type
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
var knowledgeSources = indexClient.GetKnowledgeSourcesAsync();

Console.WriteLine("Knowledge Sources:");

await foreach (var ks in knowledgeSources)
{
    Console.WriteLine($"  Name: {ks.Name}, Type: {ks.GetType().Name}");
}
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="python"

```python
# List knowledge sources by name and type
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

for ks in index_client.list_knowledge_sources():
    print(f"  - {ks.name} ({ks.kind})")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version={{api-version}}&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list)

::: zone-end

You can also return a single knowledge source by name to review its JSON definition.

::: zone pivot="csharp"

```csharp
using Azure.Search.Documents.Indexes;
using System.Text.Json;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

// Specify the knowledge source name to retrieve
string ksNameToGet = "earth-knowledge-source";

// Get its definition
var knowledgeSourceResponse = await indexClient.GetKnowledgeSourceAsync(ksNameToGet);
var ks = knowledgeSourceResponse.Value;

// Serialize to JSON for display
var jsonOptions = new JsonSerializerOptions 
{ 
    WriteIndented = true,
    DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.Never
};
Console.WriteLine(JsonSerializer.Serialize(ks, ks.GetType(), jsonOptions));
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="python"

```python
# Get a knowledge source definition
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

ks = index_client.get_knowledge_source("knowledge_source_name")
print(json.dumps(ks.as_dict(), indent = 2))
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get)

::: zone-end
