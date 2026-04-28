---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

Run the following code to monitor ingestion progress and health, including the knowledge source kind and detailed indexing errors for knowledge sources that generate an indexer pipeline and populate a search index.

::: zone pivot="csharp"

```csharp
using Azure.Search.Documents.Indexes;
using System.Text.Json;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

// Get knowledge source ingestion status
var statusResponse = await indexClient.GetKnowledgeSourceStatusAsync(knowledgeSourceName);
var status = statusResponse.Value;

// Serialize to JSON for display
var json = JsonSerializer.Serialize(status, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine(json);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
# Check knowledge source ingestion status
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

status = index_client.get_knowledge_source_status("knowledge_source_name")
print(json.dumps(status.as_dict(), indent=2))
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### Check knowledge source ingestion status
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}/status?api-version={{api-version}}
api-key: {{api-key}}
Content-Type: application/json 
```

**Reference:** [Knowledge Sources - Get Status](/rest/api/searchservice/knowledge-sources/get-status?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

A response for a request that includes ingestion parameters and is actively ingesting content might look like the following example.

```json
{
  "kind": "azureBlob",
  "synchronizationStatus": "active",
  "synchronizationInterval": "1d",
  "currentSynchronizationState": {
    "startTime": "2026-04-10T19:30:00Z",
    "itemUpdatesProcessed": 1100,
    "itemsUpdatesFailed": 100,
    "itemsSkipped": 1100,
    "errors": [
      {
        "key": "Item id 1",
        "docURL": "https://contoso.blob.core.windows.net/contracts/2024/Q4/doc-00023.csv",
        "statusCode": 400,
        "componentName": "DocumentExtraction.AzureBlob.MyDataSource",
        "errorMessage": "Could not read the value of column 'foo' at index '0'.",
        "details": "The file could not be parsed.",
        "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2049388"
      }
    ]
  },
  "lastSynchronizationState": {
    "status": "partialSuccess",
    "startTime": "2026-04-09T19:30:00Z",
    "endTime": "2026-04-09T19:40:01Z",
    "itemUpdatesProcessed": 1100,
    "itemsUpdatesFailed": 100,
    "itemsSkipped": 1100,
    "errors": null
  },
  "statistics": {
    "totalSynchronizations": 25,
    "averageSynchronizationDuration": "00:15:20",
    "averageItemsProcessedPerSynchronization": 500
  }
}
```

> [!NOTE]
> The `kind` property and `currentSynchronizationState.errors[]` array with document-level error details are available starting with the 2026-04-01 API version. For earlier API versions, these fields aren't returned. The `lastSynchronizationState.status` field is also new in 2026-04-01.
