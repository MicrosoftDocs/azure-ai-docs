---
title: Search over CSV blobs using delimitedText parsing
titleSuffix: Azure AI Search
description: Extract CSV blobs from Azure Blob Storage or Azure Files, and import as search documents into Azure AI Search using the delimitedText parsing mode.

manager: nitinme
author: HeidiSteen
ms.author: heidist

ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 10/23/2024
---

# Index CSV blobs and files using delimitedText parsing mode

**Applies to**: [Blob storage indexers](search-howto-indexing-azure-blob-storage.md), [Files indexers](search-file-storage-integration.md)

In Azure AI Search, indexers for Azure Blob Storage and Azure Files support a `delimitedText` parsing mode for CSV files that treats each line in the CSV as a separate search document. For example, given the following comma-delimited text, the `delimitedText` parsing mode would result in two documents in the search index: 

```text
id, datePublished, tags
1, 2016-01-12, "azure-search,azure,cloud"
2, 2016-07-07, "cloud,mobile"
```

If a field inside the CSV file contains the delimiter, it should be wrapped in quotes. If the field contains a quote, it must be escaped using double quotes (`""`).

```text
id, datePublished, tags
1, 2020-01-05, "tags,with,""quoted text"""
```

Without the `delimitedText` parsing mode, the entire contents of the CSV file would be treated as one search document.

Whenever you create multiple search documents from a single blob, be sure to review [Indexing blobs to produce multiple search documents](search-howto-index-one-to-many-blobs.md) to understand how document key assignments work. The blob indexer is capable of finding or generating values that uniquely define each new document. Specifically, it can create a transitory `AzureSearch_DocumentKey` when a blob is parsed into smaller parts, where the value is then used as the search document's key in the index.

## Set up CSV indexing

To index CSV blobs, create or update an indexer definition with the `delimitedText` parsing mode on a [Create Indexer](/rest/api/searchservice/indexers/create) request.

Only UTF-8 encoding is supported.

```http
{
  "name" : "my-csv-indexer",
  ... other indexer properties
  "parameters" : { "configuration" : { "parsingMode" : "delimitedText", "firstLineContainsHeaders" : true } }
}
```

`firstLineContainsHeaders` indicates that the first (nonblank) line of each blob contains headers. If blobs don't contain an initial header line, the headers should be specified in the indexer configuration: 

```http
"parameters" : { "configuration" : { "parsingMode" : "delimitedText", "delimitedTextHeaders" : "id,datePublished,tags" } } 
```

You can customize the delimiter character using the `delimitedTextDelimiter` configuration setting. For example:

```http
"parameters" : { "configuration" : { "parsingMode" : "delimitedText", "delimitedTextDelimiter" : "|" } }
```

> [!NOTE]
> In delimited text parsing mode, Azure AI Search assumes that all blobs are CSV. If you have a mix of CSV and non-CSV blobs in the same data source, consider using [file extension filters](search-blob-storage-integration.md#controlling-which-blobs-are-indexed) to control which files are imported on each indexer run.

## Request examples

Putting it all together, here are the complete payload examples. 

Datasource: 

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-07-01
Content-Type: application/json
api-key: [admin key]
{
    "name" : "my-blob-datasource",
    "type" : "azureblob",
    "credentials" : { "connectionString" : "DefaultEndpointsProtocol=https;AccountName=<account name>;AccountKey=<account key>;" },
    "container" : { "name" : "my-container", "query" : "<optional, my-folder>" }
}   
```

Indexer:

```http
POST https://[service name].search.windows.net/indexers?api-version=2024-07-01
Content-Type: application/json
api-key: [admin key]
{
  "name" : "my-csv-indexer",
  "dataSourceName" : "my-blob-datasource",
  "targetIndexName" : "my-target-index",
  "parameters" : { "configuration" : { "parsingMode" : "delimitedText", "delimitedTextHeaders" : "id,datePublished,tags" } }
}
```

## Related content

+ [Index data from Azure Blob Storage](search-howto-indexing-azure-blob-storage.md)
+ [Index data from Azure Files](search-file-storage-integration.md)
