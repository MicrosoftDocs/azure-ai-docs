---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. For knowledge sources that generate an index and indexer pipeline, all *generated objects* are also deleted. However, if you used an existing index to create a knowledge source, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-endpoint}}/knowledgebases?api-version=2025-11-01-preview&$select=name
    api-key: {{api-key}}
    ```

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
        {
            "name": "my-kb"
        },
        {
            "name": "my-kb-2"
        }
        ]
    }
   ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```

   An example response might look like the following:

   ```json
    {
      "name": "my-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": null,
      "knowledgeSources": [
        {
          "name": "my-blob-ks",
        }
      ],
      "models": [],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or [update the knowledge base](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) by removing the knowledge source if you have multiple sources. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-endpoint}}/knowledgesources/{{knowledge-source-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```