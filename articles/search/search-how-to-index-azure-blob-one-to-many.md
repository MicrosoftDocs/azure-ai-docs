---
title: Index blobs containing multiple documents
titleSuffix: Azure AI Search
description: Crawl Azure blobs for text content using the Azure blob indexer, where each blob might yield one or more search index documents.
manager: nitinme
author: arv100kri
ms.author: arjagann
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/14/2026
ms.update-cycle: 365-days
---

# Indexing blobs and files to produce multiple search documents

**Applies to**: [Blob indexers](search-how-to-index-azure-blob-storage.md), [File indexers](search-file-storage-integration.md)

By default, an indexer treats the contents of a blob or file as a single search document. If you want a more granular representation in a search index, you can set **parsingMode** values to create multiple search documents from one blob or file. The **parsingMode** values that result in many search documents include `delimitedText` (for [CSV](search-how-to-index-azure-blob-csv.md)), `jsonArray` or `jsonLines` (for [JSON](search-how-to-index-azure-blob-json.md)), or `markdown` with sub-mode `oneToMany` for [markdown](search-how-to-index-azure-blob-markdown.md).

When you use any of these parsing modes, the new search documents that emerge must have unique document keys, and a problem arises in determining where that value comes from. The parent blob has at least one unique value in the form of `metadata_storage_path property`, but if it contributes that value to more than one search document, the key is no longer unique in the index.

To address this problem, the blob indexer generates an `AzureSearch_DocumentKey` that uniquely identifies each child search document created from the single blob parent. This article explains how this feature works.


## One-to-many document key

A document key uniquely identifies each document in an index. When no parsing mode is specified, and if there's no [explicit field mapping](search-indexer-field-mappings.md) in the indexer definition for the search document key, the blob indexer automatically maps the `metadata_storage_path property` as the document key. This default mapping ensures that each blob appears as a distinct search document. It also eliminates the need for you to manually create this field mapping. Normally, fields with identical names and types are the only ones mapped automatically.

In a one-to-many search document scenario, an implicit document key based on `metadata_storage_path property` isn't possible. As a workaround, Azure AI Search can generate a document key for each individual entity extracted from a blob. The system generates a key called `AzureSearch_DocumentKey` and adds it to each search document. The indexer keeps track of the "many documents" created from each blob, and can target updates to the search index when source data changes over time.

By default, when no explicit field mappings for the key index field are specified, the `AzureSearch_DocumentKey` is mapped to it, using the `base64Encode` field-mapping function.

## Example

Assume an index definition with the following fields:

+ `id`
+ `temperature`
+ `pressure`
+ `timestamp`

And your blob container has blobs with the following structure:

_Blob1.json_

```json
{ "temperature": 100, "pressure": 100, "timestamp": "2024-02-13T00:00:00Z" }
{ "temperature" : 33, "pressure" : 30, "timestamp": "2024-02-14T00:00:00Z" }
```

_Blob2.json_

```json
{ "temperature": 1, "pressure": 1, "timestamp": "2023-01-12T00:00:00Z" }
{ "temperature" : 120, "pressure" : 3, "timestamp": "2022-05-11T00:00:00Z" }
```

When you create an indexer and set the **parsingMode** to `jsonLines` - without specifying any explicit field mappings for the key field, the following mapping is applied implicitly.

```http
{
    "sourceFieldName" : "AzureSearch_DocumentKey",
    "targetFieldName": "id",
    "mappingFunction": { "name" : "base64Encode" }
}
```

This setup results in disambiguated document keys, similar to the following illustration (base64-encoded ID shortened for brevity).

| ID | temperature | pressure | timestamp |
|----|-------------|----------|-----------|
| aHR0 ... YjEuanNvbjsx | 100 | 100 | 2024-02-13T00:00:00Z |
| aHR0 ... YjEuanNvbjsy | 33 | 30 | 2024-02-14T00:00:00Z |
| aHR0 ... YjIuanNvbjsx | 1 | 1 | 2023-01-12T00:00:00Z |
| aHR0 ... YjIuanNvbjsy | 120 | 3 | 2022-05-11T00:00:00Z |

## Custom field mapping for index key field

Assuming the same index definition as the previous example, suppose your blob container has blobs with the following structure:

_Blob1.json_

```json
recordid, temperature, pressure, timestamp
1, 100, 100,"2024-02-13T00:00:00Z" 
2, 33, 30,"2024-02-14T00:00:00Z" 
```

_Blob2.json_

```json
recordid, temperature, pressure, timestamp
1, 1, 1,"20123-01-12T00:00:00Z" 
2, 120, 3,"2022-05-11T00:00:00Z" 
```

When you create an indexer with `delimitedText` **parsingMode**, it might feel natural to set up a field-mapping function to the key field as follows:

```http
{
    "sourceFieldName" : "recordid",
    "targetFieldName": "id"
}
```

However, this mapping doesn't result in four documents showing up in the index because the `recordid` field isn't unique _across blobs_. Hence, we recommend you to make use of the implicit field mapping applied from the `AzureSearch_DocumentKey` property to the key index field for "one-to-many" parsing modes.

If you do want to set up an explicit field mapping, make sure that the _sourceField_ is distinct for each individual entity **across all blobs**.

> [!NOTE]
> The approach used by `AzureSearch_DocumentKey` of ensuring uniqueness per extracted entity is subject to change and therefore you shouldn't rely on its value for your application's needs.

## Specify the index key field in your data

Assuming the same index definition as the previous example and **parsingMode** is set to `jsonLines` without specifying any explicit field mappings so the mappings look like in the first example, suppose your blob container has blobs with the following structure:

_Blob1.json_

```json
id, temperature, pressure, timestamp
1, 100, 100,"2024-02-13T00:00:00Z" 
2, 33, 30,"2024-02-14T00:00:00Z"
```

_Blob2.json_

```json
id, temperature, pressure, timestamp
1, 1, 1,"2023-01-12T00:00:00Z" 
2, 120, 3,"2022-05-11T00:00:00Z" 
```

Each document contains the `id` field, which is defined as the `key` field in the index. In this situation, the system generates a unique AzureSearch_DocumentKey` for the document, but it isn't used as the "key." Instead, the value of the `id` field is mapped to the `key` field.

Similar to the previous example, this mapping doesn't result in four documents showing up in the index because the `id` field isn't unique _across blobs_. When this situation occurs, any JSON entry that specifies an `id` causes a merge with the existing document instead of uploading a new one. The index then reflects the latest state of the entry with the specified `id`.

## Limitations

When a document entry in the index is created from a line in a file, as explained in this article, deleting that line from the file doesn't automatically remove the corresponding entry from the index. To delete the document entry, you must manually submit a deletion request to the index using the [REST API deletion operation](/rest/api/searchservice/addupdate-or-delete-documents).

## Next steps

If you aren't already familiar with the basic structure and workflow of blob indexing, you should review [Indexing Azure Blob Storage with Azure AI Search](search-how-to-index-azure-blob-json.md) first. For more information about parsing modes for different blob content types, review the following articles.

> [!div class="nextstepaction"]
> [Indexing  CSV blobs](search-how-to-index-azure-blob-csv.md)
> [Indexing JSON blobs](search-how-to-index-azure-blob-json.md)
