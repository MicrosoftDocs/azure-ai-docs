---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/07/2025
---

If you no longer need the knowledge source or need to rebuild it on your search service, use this request to delete the object.

Before you can delete a knowledge source, you must delete any knowledge base that references it or remove the references in an update action. For knowledge sources that generate an indexer pipeline and an index, all *generated objects* are also deleted. In contrast, if you created a knowledge source using an existing index, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails, and a list of affected knowledge bases is returned.

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
        "@odata.context": "https://my-demo-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
        {
            "name": "earth-blob-kb"
        },
        {
            "name": "hotels-kb"
        }
        ]
    }
   ```

1. Get the individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```

   An example response might look like the following:

   ```json
    {
      "name": "{{knowledge-base-name}}",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": "answerSynthesis",
      "knowledgeSources": [
        {
          "name": "{{knowledge-source-name}}",
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
    DELETE {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source definition
    DELETE {{search-endpoint}}/knowledgesources/{{knowledge-source-name}}?api-version=2025-11-01-preview
    api-key: {{api-key}}
    ```
