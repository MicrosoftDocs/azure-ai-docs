---
title: 'Tutorial: Index Markdown blobs'
titleSuffix: Azure AI Search
description: Learn how to index and search semi-structured Azure JSON blobs using Azure AI Search REST APIs.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: tutorial
ms.date: 03/13/2024

---

# Tutorial: Index nested Markdown blobs from Azure Storage using REST

Azure AI Search can index Markdown documents and arrays in Azure Blob Storage using an [indexer](search-indexer-overview.md) that knows how to read Markdown data. 

This tutorial shows you to index Markdown files. It uses a REST client and the [Search REST APIs](/rest/api/searchservice/) to perform the following tasks:

> [!div class="checklist"]
> + Set up sample data and configure an `azureblob` data source
> + Create an Azure AI Search index to contain searchable content
> + Create and run an indexer to read the container and extract searchable content
> + Search the index you just created

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

## Prerequisites

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

+ [Azure Storage](/azure/storage/common/storage-account-create)

+ [Azure AI Search](search-what-is-azure-search.md). [Create](search-create-service-portal.md) or [find an existing Azure AI Search resource](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) under your current subscription.

> [!NOTE]
> You can use the free service for this tutorial. A free search service limits you to three indexes, three indexers, and three data sources. This tutorial creates one of each. Before starting, make sure you have room on your service to accept the new resources.

### Download files

Download a zip file of the sample data repository and extract the contents. [Learn how](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

+ [sample-markdown-free](https://github.com/Azure-Samples/azure-search-sample-data)

Sample data is a single JSON file containing a JSON array and 1,521 nested JSON elements. Sample data originates from [NY Philharmonic Performance History](https://www.kaggle.com/datasets/nyphil/perf-history) on Kaggle. We chose one JSON file to stay under the storage limits of the free tier.

Here's the first nested JSON in the file. The remainder of the file includes 1,520 other instances of concert performances.

```md
# Project Documentation

## Introduction
This document provides a complete overview of the **Markdown Features** used within this project. The following sections demonstrate the richness of Markdown formatting, with examples of lists, tables, links, images, blockquotes, inline styles, and more.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Text Formatting](#basic-text-formatting)
3. [Lists](#lists)
4. [Blockquotes](#blockquotes)
5. [Images](#images)
6. [Links](#links)
7. [Tables](#tables)
8. [Horizontal Rules](#horizontal-rules)
9. [Inline Elements](#inline-elements)
10. [Escaping Characters](#escaping-characters)
11. [HTML Elements](#html-elements)
12. [Emojis](#emojis)
13. [Footnotes](#footnotes)
14. [Task Lists](#task-lists)
15. [Conclusion](#conclusion)

---

## Basic Text Formatting
You can apply various styles to your text:
- **Bold**: Use double asterisks or underscores: `**bold**` or `__bold__`.
- *Italic*: Use single asterisks or underscores: `*italic*` or `_italic_`.
- ~~Strikethrough~~: Use double tildes: `~~strikethrough~~`.

## Lists

### Ordered List
1. First item  
2. Second item  
3. Third item  

### Unordered List
- Item A  
- Item B  
- Item C  

### Nested List
1. Parent item  
   - Child item  
   - Child item  

## Blockquotes
> This is a blockquote.  
> Blockquotes are great for emphasizing important information.  
>> Nested blockquotes are also possible!

## Images
![Markdown Logo](https://markdown-here.com/img/icon256.png)

## Links
[Visit Markdown Guide](https://www.markdownguide.org)

## Tables

| Syntax      | Description | Example       |
|-------------|-------------|---------------|
| Header      | Title       | Header Cell   |
| Paragraph   | Text block  | Row Content   |

## Horizontal Rules
Use three or more dashes or underscores to create a horizontal rule.

---
___

## Inline Elements
Sometimes, it’s useful to include `inline code` to highlight code-like content.  

You can also emphasize text like *this* or make it **bold**.

## Escaping Characters
To render special Markdown characters, use backslashes:
- \*Asterisks\*
- \#Hashes\#
- \[Brackets\]

## HTML Elements
You can mix HTML tags with Markdown:

<table>
  <tr>
    <th>HTML Table</th>
    <th>With Markdown</th>
  </tr>
  <tr>
    <td>Row 1</td>
    <td>Data 1</td>
  </tr>
</table>

## Emojis
Markdown supports some basic emojis:
- :smile: 😄  
- :rocket: 🚀  
- :checkered_flag: 🏁  

## Footnotes
This is an example of a footnote[^1]. Footnotes allow you to add notes without cluttering the main text.

[^1]: This is the content of the footnote.

## Task Lists
- [x] Complete the introduction  
- [ ] Add more examples  
- [ ] Review the document

### Example of h3
#### Example of h4
This section exists to show the functionality of the markdownHeaderDepth.

## Conclusion
Markdown is a lightweight yet powerful tool for writing documentation. It supports a variety of formatting options while maintaining simplicity and readability.

Thank you for reviewing this example!

---
Generated with Markdown 📝
```

### Upload sample data to Azure Storage

1. In Azure Storage, create a new container and name it *sample-markdown*.

1. [Upload the sample data files](/azure/storage/blobs/storage-quickstart-blobs-portal).

1. Get a storage connection string so that you can formulate a connection in Azure AI Search.

   1. On the left, select **Access keys**.

   1. Copy the connection string for either key one or key two. The connection string is similar to the following example:

      ```http
      DefaultEndpointsProtocol=https;AccountName=<your account name>;AccountKey=<your account key>;EndpointSuffix=core.windows.net
      ```

### Copy a search service URL and API key

For this tutorial, connections to Azure AI Search require an endpoint and an API key. You can get these values from the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com), navigate to the search service **Overview** page, and copy the URL. An example endpoint might look like `https://mydemo.search.windows.net`.

1. Under **Settings** > **Keys**, copy an admin key. Admin keys are used to add, modify, and delete objects. There are two interchangeable admin keys. Copy either one.

   :::image type="content" source="media/search-get-started-rest/get-url-key.png" alt-text="Screenshot of the URL and API keys in the Azure portal.":::

## Set up your REST file

1. Start Visual Studio Code and create a new file

1. Provide values for variables used in the request: 

   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
   @apiKey = PUT-YOUR-ADMIN-API-KEY-HERE
   @storageConnection = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
   @blobContainer = PUT-YOUR-CONTAINER-NAME-HERE
   ```

1. Save the file using a `.rest` or `.http` file extension.

See [Quickstart: Text search using REST](search-get-started-rest.md) if you need help with the REST client.

## Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
### Create a data source
POST {{baseUrl}}/datasources?api-version=2024-11-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

    {
        "name" : "sample-markdown-ds",
        "description": null,
        "type": "azureblob",
        "subtype": null,
        "credentials": {
            "connectionString": "{{storageConnectionString}}"
        },
        "container": {
            "name": "{{blobContainer}}",
            "query": null
        },
        "dataChangeDetectionPolicy": null,
        "dataDeletionDetectionPolicy": null
    }
```

Send the request. The response should look like:

```json
HTTP/1.1 201 Created
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
ETag: "0x8DC43A5FDB8448F"
Location: https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net:443/datasources('sample-markdown-ds')?api-version=2024-11-01
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: 7ca53f73-1054-4959-bc1f-616148a9c74a
elapsed-time: 111
Date: Wed, 13 Nov 2024 21:38:58 GMT
Connection: close

{
  "@odata.context": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/$metadata#datasources/$entity",
  "@odata.etag": "\"0x8DC43A5FDB8448F\"",
  "name": "sample-markdownc-ds",
  "description": null,
  "type": "azureblob",
  "subtype": null,
  "credentials": {
    "connectionString": null
  },
  "container": {
    "name": "sample-markdown",
    "query": null
  },
  "dataChangeDetectionPolicy": null,
  "dataDeletionDetectionPolicy": null,
  "encryptionKey": null
}
```

## Create an index

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a search index on your search service. An index specifies all the parameters and their attributes.

This implementation will leverage [field mappings](search-indexer-field-mappings.md) in the indexer to map from the fields in the enriched document to the index. See [index markdown blobs](search-how-to-index-markdown-blobs.md) for more information on the parsed one-to-many document structure.

```http
### Create an index
POST {{baseUrl}}/indexes?api-version=2024-11-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

    {
      "name": "sample-markdown-index",  
      "fields": [
        {"name": "section_id", "type": "Edm.String", "key": true, "searchable": true, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
        {"name": "content", "type": "Edm.String", "key": false, "searchable": true, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
        {"name": "h1", "type": "Edm.String", "searchable": true, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
        {"name": "h2_subheader", "type": "Edm.String", "searchable": true, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
        {"name": "h3_subheader", "type": "Edm.String", "searchable": true, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
        {"name": "ordinal_position", "type": "Edm.Int32", "searchable": false, "retrievable": true, "filterable": true, "facetable": true, "sortable": true},
      ]
    }
```

**Key points**:

+ In the raw content, `Date` and `Time` are strings, so the corresponding data types in the index are also strings. 

## Create and run an indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads and indexes data, and optionally provides a schedule to automate the data refresh.

The indexer configuration includes the `jsonArray` parsing mode and a `documentRoot`.

```http
### Create and run an indexer
POST {{baseUrl}}/indexers?api-version=2024-11-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

    {
      "name": "sample-markdown-indexer",
      "dataSourceName": "sample-markdown-ds",
      "targetIndexName": "sample-markdown-index",
      "parameters" : { 
        "configuration": { 
          "parsingMode": "markdown",
          "parsingMode": "oneToMany",
          "markdownHeaderDepth": "h3"
          }
        },
      "fieldMappings" : [ 
        {
          "sourceFieldName": "/sections/h1",
          "targetFieldName": "title",
          "mappingFunction": null
        },
        {
          "sourceFieldName": "/sections/h2",
          "targetFieldName": "h2_subheader",
          "mappingFunction": null
        },
        {
          "sourceFieldName": "/sections/h3",
          "targetFieldName": "h3_subheader",
          "mappingFunction": null
        }
      ]
    }
```

**Key points**:

+ The indexer will only parse headers up to `h3`. Any lower-level headers (`h4`,`h5`,`h6`) will be treated as plain text. This is why the index and field mappings only exist up to a depth of `h3`.

+ The `content` field requires no field mappings as it exists in the enriched document.

## Run queries

You can start searching as soon as the first document is loaded.

```http
### Query the index
POST {{baseUrl}}/indexes/sample-markdown-index/docs/search?api-version=2024-11-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
  {
    "search": "*",
    "count": true
  }
```

Send the request. This is an unspecified full text search query that returns all of the fields marked as retrievable in the index, along with a document count. The response should look like:

```json
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Content-Encoding: gzip
Vary: Accept-Encoding
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: ecc8cec3-1e2b-44ed-92db-f88bdf014d4f
elapsed-time: 13
Date: Thu, 24 Oct 2024 22:23:23 GMT
Connection: close

{
  "@odata.context": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes('sample-markdown-index')/$metadata#docs(*)",
  "@odata.count": 19,
  "value": [
    ...
    <19 search documents here>
    ...
  ]
}
```

Add a `search` parameter to search on a string. 

```http
### Query the index
POST {{baseUrl}}/indexes/sample-markdown-index/docs/search?api-version=2024-11-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
  {
    "search": "h4",
    "count": true,
  }
```

HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Content-Encoding: gzip
Vary: Accept-Encoding
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: 179f8bce-7ac8-4ebd-b4dd-0fb714e4a439
elapsed-time: 33
Date: Thu, 24 Oct 2024 22:27:05 GMT
Connection: close

{
  "@odata.context": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes('sample-markdown-index')/$metadata#docs(*)",
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 0.26286605,
      "section_id": "aHR0cHM6Ly9hcmphZ2Fubmpma2ZpbGVzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tYXJrZG93bi10dXRvcmlhbC9zYW1wbGVfbWFya2Rvd24ubWQ7MTg1",
      "content": "#### Example of h4\r\nThis section exists to show the functionality of the markdownHeaderDepth.\r\n",
      "title": "Project Documentation",
      "h2_subheader": "Task Lists",
      "h3_subheader": "Example of h3",
      "ordinal_position": 18
    }
  ]
}

One document is returned in the response. 

**Key points**:

+ Because the `markdownHeaderDepth` is set to `h3`, `h4` headers are treated as plaintext. That is why it shows up in the `content` field here.

+ Ordinal position here is 18 and there are 19 total documents, which makes sense because is the 2nd to last content block in the markdown document.

Add a `select` parameter to limit the results to fewer fields. Add a `filter` to further narrow the search.

HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Content-Encoding: gzip
Vary: Accept-Encoding
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: f4f6fb04-7b69-4dbf-98dc-908a04fa0aaa
elapsed-time: 53
Date: Thu, 24 Oct 2024 22:39:52 GMT
Connection: close

{
  "@odata.context": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes('sample-markdown-index')/$metadata#docs(*)",
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 0.7492743,
      "content": "Markdown is a lightweight yet powerful tool for writing documentation. It supports a variety of formatting options while maintaining simplicity and readability.\r\n\r\nThank you for reviewing this example!\r\n\r\n---\r\nGenerated with Markdown \ud83d\udcdd\r\n",
      "title": "Project Documentation",
      "h2_subheader": "Conclusion"
    }
  ]
}

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Create a query](search-query-simple-examples.md).

> [!NOTE]
> The `$filter` parameter only works on fields that were marked filterable at the creation of your index.

## Reset and rerun

Indexers can be reset, clearing execution history, which allows a full rerun. The following GET requests are for reset, followed by rerun.

```http
### Reset the indexer
POST {{baseUrl}}/indexers/sample-markdown-indexer/reset?api-version=2024-11-01  HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Run the indexer
POST {{baseUrl}}/indexers/sample-markdown-indexer/run?api-version=2024-11-01  HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Check indexer status 
GET {{baseUrl}}/indexers/sample-markdown-indexer/status?api-version=2024-11-01  HTTP/1.1
  api-key: {{apiKey}}
```

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can use the portal to delete indexes, indexers, and data sources.

## Next steps

Now that you're familiar with the basics of Azure Blob indexing, let's take a closer look at indexer configuration for JSON blobs in Azure Storage.

> [!div class="nextstepaction"]
> [Configure Markdown blob indexing](search-how-to-index-markdown-blobs.md)
