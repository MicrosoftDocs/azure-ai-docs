---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 10/31/2025
---

If you no longer need the knowledge source or need to rebuild it on your search service, use this request to delete the object.

Before you can delete a knowledge source, you must delete any knowledge base that references it or remove the references in an update action. For knowledge sources that generate an indexer pipeline and an index, those are standalone objects and don't need to be deleted or updated with the knowledge source.

If you try to delete a knowledge source that's in use, the action fails, and a list of affected knowledge bases is returned.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-endpoint}}/knowledgebases?api-version=2025-11-01-preview&$select=name
    api-key: {{api-key}}
    Content-Type: application/json
    ```

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-demo-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
        {
            "name": "earth-blob-kb"
        },
        {
            "name": "hotels-sample-kb"
        }
        ]
    }
   ```

1. Get the individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-endpoint}}/knowledgebases/hotels-sample-kb?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

   An example response might look like the following:

   ```json
    {
      "name": "hotels-sample-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": "answerSynthesis",
      "knowledgeSources": [
        {
          "name": "hotels-sample-ks",
        }
      ],
      "models": [ TRIMMED FOR BREVITY ],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or [update the knowledge base](/rest/api/searchservice/knowledgebases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) by removing the knowledge source if you have multiple sources. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-endpoint}}/knowledgebases/hotels-sample-kb?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source definition
    DELETE {{search-endpoint}}/knowledgesources/hotels-sample-ks?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```
