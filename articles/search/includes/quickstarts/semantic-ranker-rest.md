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

+ [Add a semantic configuration to an index](#add-a-semantic-configuration-to-the-hotels-sample-index)
+ [Add semantic parameters to a query](#add-semantic-parameters-to-a-query)

### Add a semantic configuration to the hotels-sample-index

```https
TBD
```

### Add semantic parameters to a query

```https
TBD
```

## Explaining the code

This section explains the updates to the index and queries. If you're updating an existing index, the additional of a semantic configuration doesn't require a reindexing because the structure of your documents is unchanged.

### Index updates

To update the index, provide the existing schema in its entirety, plus the new `SemanticConfiguration` section. We recommend retrieving the index schema from the search service to ensure you're working with the current version. If the original and updated schemas differ in field definitions or other constructs, the update fails.

This example shows the JSON that adds a semantic configuration to an index.

```json
TBD
```

### Query parameters

Required semantic parameters include `query_type` and `semantic_configuration_name`. Here is an example of a basic semantic query using the minimum parameters.

```json
TBD
```

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions.

```json
TBD
```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To get a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

```json
TBD
```
