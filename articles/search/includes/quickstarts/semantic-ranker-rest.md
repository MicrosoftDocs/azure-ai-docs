---
manager: nitinme
author: haileytapia
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/27/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-search) to start with a finished project or follow these steps to create your own. 

## Set up the client

In this quickstart, you use a REST client and the [Azure AI Search REST APIs](/rest/api/searchservice) to configure and use a semantic ranker.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for this quickstart.

1. Start Visual Studio Code and create a new .http or .rest file.

1. At the top, set environment variables for your search service, authorization, and index name.

   + For @baseURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @token, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal identity token.

   + For @index-name, provide a unique name or use the default, *hotel-semantic-quickstart*.

1. To test the connection, send your first request. This GET request returns a list of existing indexes. You should get an HTTP 200 Success status code and a list of indexes, including hotels-sample-index used in this quickstart.

   ```http
   ### List existing indexes by name (verify the connection)
   GET  {{baseUrl}}/indexes?api-version=2024-07-01&$select=name  HTTP/1.1
   Content-Type: application/json
   Authorization: Bearer {{token}}
   ```

## Update and query the index

In this section, you make REST API calls to update a search index to include a semantic configuration, and then send a query that invokes semantic ranking. Visual Studio Code displays the response to each request in an adjacent pane. For more information about each step, see [Explaining the code](#explaining-the-code).

```json
TBD
```

## Explaining the code

This section explains the REST API calls that you made to:

+ [Update an index with a semantic configuration](#add-a-semantic-configuration-to-the-index)
+ [Query the index using semantic parameters](#add-semantic-ranking-to-queries)

### Update an index with a semantic configuration

TBD

### Query the index using semantic parameters

TBD