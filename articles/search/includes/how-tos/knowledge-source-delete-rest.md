---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 10/10/2025
---

If you no longer need the knowledge source, or if you need to rebuild it on the search service, use this request to delete the current object.

Before you can delete a knowledge source, you must delete any knowledge agent that references it, or remote the references in an update action. The associated index and any indexer pipeline objects created from the knowledge source are standalone objects and don't need to be deleted or updated in tandem with the knowledge source.

If you try to delete a knowledge source that's in use, the action fails and a list of affected knowledge agents is returned.

1. Start by getting a list of all knowledge agents. This request returns all knowledge agents on your search service.

    ```http
    ### Get the knowledge agent
    GET {{search-endpoint}}/agents?api-version=2025-08-01-preview&$select=name
    api-key: {{api-key}}
    Content-Type: application/json
    ```

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-demo-search-service.search.windows.net/$metadata#agents(name)",
        "value": [
        {
            "name": "earth-blob-ka"
        },
        {
            "name": "hotels-sample-ka"
        }
        ]
    }
   ```

1. Get the individual knowledge agent definition to check for knowledge source references.

    ```http
    GET {{search-endpoint}}/agents/hotels-sample-ka?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

   An example response might look like the following:

   ```json
    {
      "name": "hotels-sample-ka",
      "description": null,
      "retrievalInstructions": null,
      "knowledgeSources": [
        {
          "name": "hotels-sample-ks",
          "alwaysQuerySource": false,
          "includeReferences": true,
          "includeReferenceSourceData": false,
          "maxSubQueries": null,
          "rerankerThreshold": null
        }
      ],
      "models": [ trimmed for brevity ],
      "outputConfiguration": { trimmed for brevity },
      "requestLimits": { trimmed for brevity},
      "encryptionKey": null
    }
   ```

1. Either [update the knowledge agent](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true) by removing the knowledge source if you have multiple sources, or delete the knowledge agent. This example shows deletion.

    ```http
    ### Delete knowledge agent
    DELETE {{search-endpoint}}/agents/hotels-sample-ka?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source definition
    GET {{search-endpoint}}/knowledgeSources/hotels-sample-ks?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```
