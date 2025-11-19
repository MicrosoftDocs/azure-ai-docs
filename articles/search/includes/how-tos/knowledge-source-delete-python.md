---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/13/2025
---

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. For knowledge sources that generate an index and indexer pipeline, all *generated objects* are also deleted. However, if you used an existing index to create a knowledge source, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```python
    # Get knowledge bases
    import requests
    import json
    
    endpoint = "{search_url}/knowledgebases"
    params = {"api-version": "2025-11-01-preview", "$select": "name"}
    headers = {"api-key": "{api_key}"}
    
    response = requests.get(endpoint, params = params, headers = headers)
    print(json.dumps(response.json(), indent = 2))
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

    ```python
    # Get a knowledge base definition
    import requests
    import json
    
    endpoint = "{search_url}/knowledgebases/{knowledge_base_name}"
    params = {"api-version": "2025-11-01-preview"}
    headers = {"api-key": "{api_key}"}
    
    response = requests.get(endpoint, params = params, headers = headers)
    print(json.dumps(response.json(), indent = 2))
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

1. Either delete the knowledge base or [update the knowledge base](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to remove the knowledge source if you have multiple sources. This example shows deletion.

    ```python
    # Delete a knowledge base
    from azure.core.credentials import AzureKeyCredential 
    from azure.search.documents.indexes import SearchIndexClient
    
    index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
    index_client.delete_knowledge_base("knowledge_base_name")
    print(f"Knowledge base deleted successfully.")
    ```

1. Delete the knowledge source.

    ```python
    # Delete a knowledge source
    from azure.core.credentials import AzureKeyCredential 
    from azure.search.documents.indexes import SearchIndexClient
    
    index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
    index_client.delete_knowledge_source("knowledge_source_name")
    print(f"Knowledge source deleted successfully.")
    ```
