---
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

Use [Knowledge Sources - Status (REST API)](/rest/api/searchservice/knowledge-sources/get-status) to monitor ingestion progress and health, including indexer status for knowledge sources that generate an indexer pipeline and populate a search index.

```http
### Check knowledge source ingestion status
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}/status?api-version=2025-11-01-preview
api-key: {{api-key}}
Content-Type: application/json 
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
