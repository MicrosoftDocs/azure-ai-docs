---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/13/2025
---

Run the following code to monitor ingestion progress and health, including indexer status for knowledge sources that generate an indexer pipeline and populate a search index.

```python
# Check knowledge source ingestion status
import requests
import json

endpoint = "{search_url}/knowledgesources/{knowledge_source_name}/status"
params = {"api-version": "2025-11-01-preview"}
headers = {"api-key": "{api_key}"}

response = requests.get(endpoint, params = params, headers = headers)
print(json.dumps(response.json(), indent = 2))
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
