---
title: Map fields in indexers
titleSuffix: Azure AI Search
description: Configure field mappings in an indexer to account for differences in field names and data representations.

manager: nitinme
author: HeidiSteen
ms.author: heidist

ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 08/09/2024
---

# Field mappings and transformations using Azure AI Search indexers

![Indexer Stages](./media/search-indexer-field-mappings/indexer-stages-field-mappings.png "indexer stages")

This article explains how to set explicit field mappings that establish the data path between source fields in a supported data source and target fields in a search index.

## When to set a field mapping

When an [Azure AI Search indexer](search-indexer-overview.md) loads a search index, it determines the data path using source-to-destination field mappings. Implicit field mappings are internal and occur when field names and data types are compatible between the source and destination. If inputs and outputs don't match, you can define explicit *field mappings* to set up the data path, as described in this article. 

Field mappings can also be used for light-weight data conversions, such as encoding or decoding, through [mapping functions](#mappingFunctions). If more processing is required, consider [Azure Data Factory](/azure/data-factory/) to bridge the gap.

Field mappings apply to:

+ Physical data structures on both sides of the data path. Logical data structures created by skills reside only in memory. Use [outputFieldMappings](cognitive-search-output-field-mapping.md) to map in-memory nodes to output fields in a search index.

+ Parent AI Search indexes only. For "secondary" indexes with "child" documents or "chunks", refer to the [advanced field mapping scenarios](#advancedFieldMappingScenarios).
  
+ Top-level search fields only, where the `targetFieldName` is either a simple field or a collection. A target field can't be a complex type.

## Supported scenarios

Make sure you're using a [supported data source](search-indexer-overview.md#supported-data-sources) for indexer-driving indexing.

| Use-case | Description |
|----------|-------------|
| Name discrepancy | Suppose your data source has a field named `_city`. Given that Azure AI Search doesn't allow field names that start with an underscore, a field mapping lets you effectively map "_city" to "city". </p>If your indexing requirements include retrieving content from multiple data sources, where field names vary among the sources, you could use a field mapping to clarify the path.|
| Type discrepancy | Supposed you want a source integer field to be of type `Edm.String` so that it's searchable in the search index. Because the types are different, you'll need to define a field mapping in order for the data path to succeed. Note that Azure AI Search has a smaller set of [supported data types](/rest/api/searchservice/supported-data-types) than many data sources. If you're importing SQL data, a field mapping allows you to [map the SQL data type](search-how-to-index-sql-database.md#mapping-data-types) you want in a search index.|
| One-to-many data paths | You can populate multiple fields in the index with content from the same source field. For example, you might want to apply different analyzers to each field to support different use cases in your client app.|
| Encoding and decoding | You can apply [mapping functions](#mappingFunctions) to support Base64 encoding or decoding of data during indexing. |
| Split strings or recast arrays into collections | You can apply [mapping functions](#mappingFunctions) to split a string that includes a delimiter, or to send a JSON array to a search field of type `Collection(Edm.String)`.

> [!NOTE]
> If no field mappings are present, indexers assume data source fields should be mapped to index fields with the same name. Adding a field mapping overrides the default field mappings for the source and target field. Some indexers, such as the [blob storage indexer](search-howto-indexing-azure-blob-storage.md), add default field mappings for the index key field automatically.

Complex fields aren't supported in a field mapping. Your source structure (nested or hierarchical structures) must exactly match the complex type in the index so that the default mappings work. For more information, see [Tutorial: Index nested JSON blobs](search-semi-structured-data.md) for an example. If you get an error similar to `"Field mapping specifies target field 'Address/city' that doesn't exist in the index"`, it's because target field mappings can't be a complex type. 

Optionally, you might want just a few nodes in the complex structure. To get individual nodes, you can flatten incoming data into a string collection (see [outputFieldMappings](cognitive-search-output-field-mapping.md#flatten-complex-structures-into-a-string-collection) for this workaround).

## Define a field mapping

This section explains the steps for setting up field mappings.

### [**REST APIs**](#tab/rest)

1. Use [Create Indexer](/rest/api/searchservice/indexers/create) or [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update) or an equivalent method in an Azure SDK. Here's an example of an indexer definition.

   ```json
   {
      "name": "myindexer",
      "description": null,
      "dataSourceName": "mydatasource",
      "targetIndexName": "myindex",
      "schedule": { },
      "parameters": { },
      "fieldMappings": [],
      "disabled": false,
      "encryptionKey": { }
    }
    ```

1. Fill out the `fieldMappings` array to specify the mappings. A field mapping consists of three parts.

    ```json
    "fieldMappings": [
      {
        "sourceFieldName": "_city",
        "targetFieldName": "city",
        "mappingFunction": null
      }
    ]
    ```

    | Property | Description |
    |----------|-------------|
    | sourceFieldName | Required. Represents a field in your data source. |
    | targetFieldName | Optional. Represents a field in your search index. If omitted, the value of `sourceFieldName` is assumed for the target. Target fields must be top-level simple fields or collections. It can't be a complex type or collection. If you're handling a data type issue, a field's data type is specified in the index definition. The field mapping just needs to have the field's name.|
    | mappingFunction | Optional. Consists of [predefined functions](#mappingFunctions) that transform data.  |

#### Example: Name or type discrepancy

An explicit field mapping establishes a data path for cases where name and type aren't identical.

Azure AI Search uses case-insensitive comparison to resolve the field and function names in field mappings. This is convenient (you don't have to get all the casing right), but it means that your data source or index can't have fields that differ only by case. 

```JSON
PUT https://[service name].search.windows.net/indexers/myindexer?api-version=[api-version]
Content-Type: application/json
api-key: [admin key]
{
    "dataSourceName" : "mydatasource",
    "targetIndexName" : "myindex",
    "fieldMappings" : [ { "sourceFieldName" : "_city", "targetFieldName" : "city" } ]
}
```

#### Example: One-to-many or forked data paths

This example maps a single source field to multiple target fields ("one-to-many" mappings). You can "fork" a field, copying the same source field content to two different index fields that will be analyzed or attributed differently in the index.

```JSON

"fieldMappings" : [
    { "sourceFieldName" : "text", "targetFieldName" : "textStandardEnglishAnalyzer" },
    { "sourceFieldName" : "text", "targetFieldName" : "textSoundexAnalyzer" }
]
```

You can use a similar approach for [skills-generated content](cognitive-search-output-field-mapping.md).

### [**.NET SDK (C#)**](#tab/csharp)

In the Azure SDK for .NET, use the [FieldMapping](/dotnet/api/azure.search.documents.indexes.models.fieldmapping) class that provides `SourceFieldName` and `TargetFieldName` properties and an optional `MappingFunction` reference.

Specify field mappings when constructing the indexer, or later by directly setting [SearchIndexer.FieldMappings](/dotnet/api/azure.search.documents.indexes.models.searchindexer.fieldmappings). The following C# example sets the field mappings when constructing an indexer.

```csharp
var indexer = new SearchIndexer("hotels-sql-idxr", dataSource.Name, searchIndex.Name)
{
    Description = "SQL data indexer",
    Schedule = schedule,
    Parameters = parameters,
    FieldMappings =
    {
        new FieldMapping("_hotelId") {TargetFieldName = "HotelId", FieldMappingFunction.Base64Encode()},
        new FieldMapping("Amenities") {TargetFieldName = "Tags"}
    }
};

await indexerClient.CreateOrUpdateIndexerAsync(indexer);
```

---

<a name="mappingFunctions"></a>

## Mapping functions and examples

A field mapping function transforms the contents of a field before it's stored in the index. The following mapping functions are currently supported:

+ [base64Encode](#base64EncodeFunction)
+ [base64Decode](#base64DecodeFunction)
+ [extractTokenAtPosition](#extractTokenAtPositionFunction)
+ [jsonArrayToStringCollection](#jsonArrayToStringCollectionFunction)
+ [urlEncode](#urlEncodeFunction)
+ [urlDecode](#urlDecodeFunction)

Note that these functions are exclusively supported for parent indexes at this time. They aren't compatible with chunked index mapping, therefore, these functions can't be used for [index projections](index-projections-concept-intro.md).

<a name="base64EncodeFunction"></a>

### base64Encode function

Performs *URL-safe* Base64 encoding of the input string. Assumes that the input is UTF-8 encoded.

#### Example: Base-encoding a document key

Only URL-safe characters can appear in an Azure AI Search document key (so that you can address the document using the [Lookup API](/rest/api/searchservice/documents/get)). If the source field for your key contains URL-unsafe characters, such as `-` and `\`, use the `base64Encode` function to convert it at indexing time. 

The following example specifies the base64Encode function on `metadata_storage_name` to handle unsupported characters.

```http
PUT /indexers?api-version=2024-07-01
{
  "dataSourceName" : "my-blob-datasource ",
  "targetIndexName" : "my-search-index",
  "fieldMappings" : [
    { 
        "sourceFieldName" : "metadata_storage_name", 
        "targetFieldName" : "key", 
        "mappingFunction" : { 
            "name" : "base64Encode",
            "parameters" : { "useHttpServerUtilityUrlTokenEncode" : false }
        } 
    }
  ]
}
```

A document key (both before and after conversion) can't be longer than 1,024 characters. When you retrieve the encoded key at search time, use the `base64Decode` function to get the original key value, and use that to retrieve the source document.

#### Example: Make a base-encoded field "searchable"

There are times when you need to use an encoded version of a field like `metadata_storage_path` as the key, but also need an unencoded version for full text search. To support both scenarios, you can map `metadata_storage_path` to two fields: one for the key (encoded), and a second for a path field that we can assume is attributed as `searchable` in the index schema.

```http
PUT /indexers/blob-indexer?api-version=2024-07-01
{
    "dataSourceName" : " blob-datasource ",
    "targetIndexName" : "my-target-index",
    "schedule" : { "interval" : "PT2H" },
    "fieldMappings" : [
        { "sourceFieldName" : "metadata_storage_path", "targetFieldName" : "key", "mappingFunction" : { "name" : "base64Encode" } },
        { "sourceFieldName" : "metadata_storage_path", "targetFieldName" : "path" }
      ]
}
```

#### Example - preserve original values

The [blob storage indexer](search-howto-indexing-azure-blob-storage.md) automatically adds a field mapping from `metadata_storage_path`, the URI of the blob, to the index key field if no field mapping is specified. This value is Base64 encoded so it's safe to use as an Azure AI Search document key. The following example shows how to simultaneously map a *URL-safe* Base64 encoded version of `metadata_storage_path` to a `index_key` field and preserve the original value in a `metadata_storage_path` field:

```JSON
"fieldMappings": [
  {
    "sourceFieldName": "metadata_storage_path",
    "targetFieldName": "metadata_storage_path"
  },
  {
    "sourceFieldName": "metadata_storage_path",
    "targetFieldName": "index_key",
    "mappingFunction": {
       "name": "base64Encode"
    }
  }
]
```

If you don't include a parameters property for your mapping function, it defaults to the value `{"useHttpServerUtilityUrlTokenEncode" : true}`.

Azure AI Search supports two different Base64 encodings. You should use the same parameters when encoding and decoding the same field. For more information, see [base64 encoding options](#base64details) to decide which parameters to use.

<a name="base64DecodeFunction"></a>

### base64Decode function

Performs Base64 decoding of the input string. The input is assumed to be a *URL-safe* Base64-encoded string.

#### Example - decode blob metadata or URLs

Your source data might contain Base64-encoded strings, such as blob metadata strings or web URLs, that you want to make searchable as plain text. You can use the `base64Decode` function to turn the encoded data back into regular strings when populating your search index.

```JSON
"fieldMappings" : [
  {
    "sourceFieldName" : "Base64EncodedMetadata",
    "targetFieldName" : "SearchableMetadata",
    "mappingFunction" : { 
      "name" : "base64Decode", 
      "parameters" : { "useHttpServerUtilityUrlTokenDecode" : false }
    }
  }
]
```

If you don't include a parameters property, it defaults to the value `{"useHttpServerUtilityUrlTokenEncode" : true}`.

Azure AI Search supports two different Base64 encodings. You should use the same parameters when encoding and decoding the same field. For more information, see [base64 encoding options](#base64details) to decide which parameters to use.

<a name="base64details"></a>

#### base64 encoding options

Azure AI Search supports URL-safe base64 encoding and normal base64 encoding. A string that is base64 encoded during indexing should be decoded later with the same encoding options, or else the result won't match the original.

If the `useHttpServerUtilityUrlTokenEncode` or `useHttpServerUtilityUrlTokenDecode` parameters for encoding and decoding respectively are set to `true`, then `base64Encode` behaves like [HttpServerUtility.UrlTokenEncode](/dotnet/api/system.web.httpserverutility.urltokenencode) and `base64Decode` behaves like [HttpServerUtility.UrlTokenDecode](/dotnet/api/system.web.httpserverutility.urltokendecode).

> [!WARNING]
> If `base64Encode` is used to produce key values, `useHttpServerUtilityUrlTokenEncode` must be set to true. Only URL-safe base64 encoding can be used for key values. See [Naming rules](/rest/api/searchservice/naming-rules) for the full set of restrictions on characters in key values.

The .NET libraries in Azure AI Search assume the full .NET Framework, which provides built-in encoding. The `useHttpServerUtilityUrlTokenEncode` and `useHttpServerUtilityUrlTokenDecode` options apply this built-in functionality. If you're using .NET Core or another framework, we recommend setting those options to `false` and calling your framework's encoding and decoding functions directly.

The following table compares different base64 encodings of the string `00>00?00`. To determine the required processing (if any) for your base64 functions, apply your library encode function on the string `00>00?00` and compare the output with the expected output `MDA-MDA_MDA`.

| Encoding | Base64 encode output | Extra processing after library encoding | Extra processing before library decoding |
| --- | --- | --- | --- |
| Base64 with padding | `MDA+MDA/MDA=` | Use URL-safe characters and remove padding | Use standard base64 characters and add padding |
| Base64 without padding | `MDA+MDA/MDA` | Use URL-safe characters | Use standard base64 characters |
| URL-safe base64 with padding | `MDA-MDA_MDA=` | Remove padding | Add padding |
| URL-safe base64 without padding | `MDA-MDA_MDA` | None | None |

<a name="extractTokenAtPositionFunction"></a>

### extractTokenAtPosition function

Splits a string field using the specified delimiter, and picks the token at the specified position in the resulting split.

This function uses the following parameters:

+ `delimiter`: a string to use as the separator when splitting the input string.
+ `position`: an integer zero-based position of the token to pick after the input string is split.

For example, if the input is `Jane Doe`, the `delimiter` is `" "`(space) and the `position` is 0, the result is `Jane`; if the `position` is 1, the result is `Doe`. If the position refers to a token that doesn't exist, an error is returned.

#### Example - extract a name

Your data source contains a `PersonName` field, and you want to index it as two separate `FirstName` and `LastName` fields. You can use this function to split the input using the space character as the delimiter.

```JSON
"fieldMappings" : [
  {
    "sourceFieldName" : "PersonName",
    "targetFieldName" : "FirstName",
    "mappingFunction" : { "name" : "extractTokenAtPosition", "parameters" : { "delimiter" : " ", "position" : 0 } }
  },
  {
    "sourceFieldName" : "PersonName",
    "targetFieldName" : "LastName",
    "mappingFunction" : { "name" : "extractTokenAtPosition", "parameters" : { "delimiter" : " ", "position" : 1 } }
  }]
```

<a name="jsonArrayToStringCollectionFunction"></a>

### jsonArrayToStringCollection function

Transforms a string formatted as a JSON array of strings into a string array that can be used to populate a `Collection(Edm.String)` field in the index.

For example, if the input string is `["red", "white", "blue"]`, then the target field of type `Collection(Edm.String)` will be populated with the three values `red`, `white`, and `blue`. For input values that can't be parsed as JSON string arrays, an error is returned.

#### Example - populate collection from relational data

Azure SQL Database doesn't have a built-in data type that naturally maps to `Collection(Edm.String)` fields in Azure AI Search. To populate string collection fields, you can preprocess your source data as a JSON string array and then use the `jsonArrayToStringCollection` mapping function.

```JSON
"fieldMappings" : [
  {
    "sourceFieldName" : "tags", 
    "mappingFunction" : { "name" : "jsonArrayToStringCollection" }
  }]
```

<a name="urlEncodeFunction"></a>

### urlEncode function

This function can be used to encode a string so that it is "URL safe". When used with a string that contains characters that aren't allowed in a URL, this function will convert those "unsafe" characters into character-entity equivalents. This function uses the UTF-8 encoding format.

#### Example - document key lookup

`urlEncode` function can be used as an alternative to the `base64Encode` function, if only URL unsafe characters are to be converted, while keeping other characters as-is.

Say, the input string is `<hello>` - then the target field of type `(Edm.String)` will be populated with the value `%3chello%3e`

When you retrieve the encoded key at search time, you can then use the `urlDecode` function to get the original key value, and use that to retrieve the source document.

```JSON
"fieldMappings" : [
  {
    "sourceFieldName" : "SourceKey",
    "targetFieldName" : "IndexKey",
    "mappingFunction" : {
      "name" : "urlEncode"
    }
  }
]
 ```

 <a name="urlDecodeFunction"></a>

### urlDecode function

 This function converts a URL-encoded string into a decoded string using UTF-8 encoding format.

### Example - decode blob metadata

Some Azure storage clients automatically URL-encode blob metadata if it contains non-ASCII characters. However, if you want to make such metadata searchable (as plain text), you can use the `urlDecode` function to turn the encoded data back into regular strings when populating your search index.

```json
"fieldMappings" : [
  {
    "sourceFieldName" : "UrlEncodedMetadata",
    "targetFieldName" : "SearchableMetadata",
    "mappingFunction" : {
      "name" : "urlDecode"
    }
  }
]
```

<a name="fixedLengthEncodeFunction"></a>

### fixedLengthEncode function
 
 This function converts a string of any length to a fixed-length string.

### Example - map document keys that are too long

When errors occur that are related to document key length exceeding 1024 characters, this function can be applied to reduce the length of the document key.

 ```JSON

"fieldMappings" : [
  {
    "sourceFieldName" : "metadata_storage_path",
    "targetFieldName" : "your key field",
    "mappingFunction" : {
      "name" : "fixedLengthEncode"
    }
  }
]
 ```

<a name="toJsonFunction"></a>

### toJson function
 
This function converts a string into a formatted JSON object. This can be used for scenarios where the data source, such as Azure SQL, doesn't natively support compound or hierarchical data types, and then map it to complex fields.

### Example - map text content to a complex field

Assume there's a SQL row with a JSON string that needs to be mapped to a (correspondingly defined) complex field in the index, the `toJson` function can be used to achieve this. For instance, if a complex field in the index needs to be populated with the following data:

```JSON
{
    "id": "5",
    "info": {
        "name": "Jane",
        "surname": "Smith",
        "skills": [
            "SQL",
            "C#",
            "Azure"
        ],
        "dob": "2005-11-04T12:00:00"
    }
}
```
It can be achieved by using the `toJson` mapping function on a JSON string column in a SQL row that looks like this: `{"id": 5, "info": {"name": "Jane", "surname": "Smith", "skills": ["SQL", "C#", "Azure"]}, "dob": "2005-11-04T12:00:00"}`. 

The field mapping needs to be specified as shown below.

```JSON

"fieldMappings" : [
  {
    "sourceFieldName" : "content",
    "targetFieldName" : "complexField",
    "mappingFunction" : {
      "name" : "toJson"
    }
  }
]
 ```

<a name="advancedFieldMappingScenarios"></a>
## Advanced field mapping scenarios

In scenarios where you have "one-to-many" document relationships, such as data chunking or splitting, follow these guidelines for mapping fields from parent documents to "child" documents (chunks):

### 1. Skipping parent document indexing

If you are skipping the indexing of parent documents (by setting `projectionMode` to `skipIndexingParentDocuments` in the skillset's `indexProjections`), use [index projections](index-projections-concept-intro.md) to map fields from the parent documents to the "child" documents.

### 2. Indexing both parent and "child" documents

If you are indexing both parent documents and "child" documents:
+ Use field mappings to map fields to the parent documents.
+ Use [index projections](index-projections-concept-intro.md) to map fields to the "child" documents.

### 3. Mapping function-transformed values to parent and/or "child" documents

If a field in the parent document requires a transformation (using the [mapping functions](#mappingFunctions) such as encoding) and needs to be mapped to the parent and/or "child" documents:
+ Apply the transformation using field mappings' [functions](#mappingFunctions) in the indexer.
+ Use [index projections](index-projections-concept-intro.md) in the skillset to map the transformed field to the "child" documents.

## See also

+ [Supported data types in Azure AI Search](/rest/api/searchservice/supported-data-types)
+ [SQL data type map](search-how-to-index-sql-database.md#mapping-data-types)
