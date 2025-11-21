---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/19/2025
---

Run the following code to monitor ingestion progress and health, including [indexer status](/dotnet/api/azure.search.documents.indexes.models.knowledgesourcestatus?view=azure-dotnet-preview&preserve-view=true) for knowledge sources that generate an indexer pipeline and populate a search index.

```csharp
// Get knowledge source ingestion status
using Azure.Search.Documents.Indexes;
using System.Text.Json;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

// Get the knowledge source status
var statusResponse = await indexClient.GetKnowledgeSourceStatusAsync(knowledgeSourceName);
var status = statusResponse.Value;

// Serialize to JSON for display
var json = JsonSerializer.Serialize(status, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine(json);
```

A response for a request that includes ingestion parameters and is actively ingesting content might look like the following example.

```json
{ 
  "synchronizationStatus": "active", // creating, active, deleting 
  "synchronizationInterval" : "1d", // null if no schedule 
  "currentSynchronizationState" : { // spans multiple indexer "runs" 
    "startTime": "2025-10-27T19:30:00Z", 
    "itemUpdatesProcessed": 1100, 
    "itemsUpdatesFailed": 100, 
    "itemsSkipped": 1100, 
  }, 
  "lastSynchronizationState" : {  // null on first sync 
    "startTime": "2025-10-27T19:30:00Z", 
    "endTime": "2025-10-27T19:40:01Z", // this value appears on the activity record on each /retrieve 
    "itemUpdatesProcessed": 1100, 
    "itemsUpdatesFailed": 100, 
    "itemsSkipped": 1100, 
  }, 
  "statistics": {  // null on first sync 
    "totalSynchronization": 25, 
    "averageSynchronizationDuration": "00:15:20", 
    "averageItemsProcessedPerSynchronization" : 500 
  } 
} 
```
