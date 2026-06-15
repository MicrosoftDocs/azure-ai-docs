---
ms.service: azure-ai-search
ms.topic: include
ms.date: 05/29/2026
---

When you create this knowledge source, Azure AI Search automatically generates a data source, skillset, indexer, and index. The creation response lists each object under `createdResources`.

These objects are generated according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names. Avoid editing these objects directly, as changes can introduce errors or incompatibilities that break the indexer pipeline.

You can use the Azure portal to validate object creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.

1. Check the data source to verify the connection to your data store. The connection uses either a connection string or a managed identity, depending on how you configured the knowledge source.

1. Check the skillset to see how your content is chunked and optionally vectorized.

1. Check the index to see how your content is indexed and exposed for retrieval, including which fields are searchable and filterable and which fields store vectors for similarity search. Use Search Explorer to run queries against the generated index.
