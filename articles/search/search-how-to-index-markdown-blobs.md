---
title: Search over Markdown blobs
titleSuffix: Azure AI Search
description: Extract searchable text from Markdown blobs using the blob indexer in Azure AI Search. Indexers provide indexing automation for supported data sources like Azure Blob Storage.

author: mdonovan
ms.author: mdonovan

ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 10/22/2024
---

# Index Markdown blobs and files in Azure AI Search

**Applies to**: [Blob indexers](search-howto-indexing-azure-blob-storage.md), [File indexers](search-file-storage-integration.md)

In Azure AI Search, indexers for Azure Blob Storage and Azure Files support a `markdown` parsing mode for Markdown files. Markdown files can be indexed in two ways: 
+ One-to-many parsing mode
+ One-to-one parsing mode

The blob indexer provides a `submode` parameter to determine the output of structure of the search documents. Markdown parsing mode provides the following submode options:

| parsingMode | submode | Search document | Description |
|--------------|-------------|-------------|--------------|
| **`markdown`** | **`oneToMany`** | Multiple per blob | (default) Breaks the Markdown into multiple search documents, each representing a content (nonheader) section of the Markdown file. |
| **`markdown`** | **`oneToOne`** | One per blob | Parses the Markdown into one search document, with sections mapped to specific headers in the Markdown file.|

For **`oneToMany`** submode, you should review [Indexing one blob to produce many search documents](search-howto-index-one-to-many-blobs.md) to understand how the blob indexer handles disambiguation of the document key for multiple search documents produced from the same blob.

Later sections describe each submode in more detail. If you're unfamiliar with indexer clients and concepts, see [Create a search indexer](search-howto-create-indexers.md). You should also be familiar with the details of [basic blob indexer configuration](search-howto-indexing-azure-blob-storage.md), which isn't repeated here.

## Additional Markdown parsing parameters

Parameters are case-sensitive.

| Parameter name     | Allowed Values | Description |
|--------------------|-------------|-------------|
| `markdownHeaderDepth` |`h1`, `h2`, `h3`, `h4`, `h5`, `h6(default)` | This parameter determines the deepest header level that is considered when parsing, allowing for flexible handling of document structure (for example, when `markdownHeaderDepth` is set to `h1`, the parser only recognizes top-level headers that begin with "#", and all lower-level headers are treated as plain text). If not specified, it defaults to `h6`. 

This setting can be changed after initial creation of the indexer, however the structure of the resulting search documents might change depending on the Markdown content.

## Supported Markdown elements
Markdown parsing will only split content based on headers. All other elements such as lists, code blocks, tables, etc., are treated as plaintext.

<a name="parsing-markdown-one-to-many"></a>

## Markdown one-to-many parsing mode (Markdown to Multiple Documents)

The **Markdown one-to-many parsing mode** parses Markdown files into multiple search documents, where each document corresponds to a specific content section of the Markdown file based on the header metadata at that point in the document. The Markdown is parsed based on headers into documents which contain the following content:

- `content`: A string that contains the raw Markdown found in a specific location, based on the header metadata at that point in the document.

- `sections`: An object that contains subfields for the header metadata up to the desired header level. For example, when `markdownHeaderDepth` is set to `h3`, contains string fields `h1`, `h2`, and `h3`. These fields are indexed by mirroring this structure in the index, or through field mappings in the format `/sections/h1`, `sections/h2`, etc. See index and indexer configurations in the following samples for in-context examples. The subfields contained are:
  - `h1` - A string containing the h1 header value. Empty string if not set at this point in the document.
  - (Optional) `h2`- A string containing the h2 header value. Empty string if not set at this point in the document.
  - (Optional) `h3`- A string containing the h3 header value. Empty string if not set at this point in the document.
  - (Optional) `h4`- A string containing the h4 header value. Empty string if not set at this point in the document.
  - (Optional) `h5`- A string containing the h5 header value. Empty string if not set at this point in the document.
  - (Optional) `h6`- A string containing the h6 header value. Empty string if not set at this point in the document.

- `ordinal_position`: An integer value indicating the position of the section within the document hierarchy. This field is used for ordering the sections in their original sequence as they appear in the document, beginning with an ordinal position of 1 and incrementing sequentially for each header. 

Consider the following Markdown content:

```md
# Section 1
Content for section 1.

## Subsection 1.1
Content for subsection 1.1.

# Section 2
Content for section 2.
```

### Index schema for one-to-many parsed Markdown files
An example index configuration might look something like this:
```http
{
  "name": "my-markdown-index",
  "fields": [
  {
    "name": "id",
    "type": "Edm.String",
    "key": true
  },
  {
    "name": "content",
    "type": "Edm.String",
    "retrievable": true,
    "searchable": true
  },
  {
    "name": "ordinal_position",
    "type": "Edm.Int32"
  },
  {
    "name": "sections",
    "type": "Edm.ComplexType",
    "fields": [
    {
      "name": "h1",
      "type": "Edm.String"
    },
    {
      "name": "h2",
      "type": "Edm.String"
    }]
  }]
}
```

The blob indexer can infer the mapping without a field mapping present in the request, so an indexer configuration corresponding to the provided index configuration might look like this:
```http
POST https://[service name].search.windows.net/indexers?api-version=2024-11-01-preview
Content-Type: application/json
api-key: [admin key]

{
  "name": "my-markdown-indexer",
  "dataSourceName": "my-blob-datasource",
  "targetIndexName": "my-target-index",
  "parameters": {
    "configuration": { "parsingMode": "markdown" }
  },
}
```

> [!NOTE]
> The `submode` does not need to be set explicitly here because `oneToMany` is the default. 

 This Markdown file would result in three search documents after indexing, due to the three content sections. The search document resulting from the first content section of the provided Markdown document would contain the following values for `content`, `sections`, `h1`, and `h2`:

```http
{
  {
    "content": "Content for section 1.\r\n",
    "sections": {
      "h1": "Section 1",
      "h2": ""
    },
    "ordinal_position": 1
  },
  {
    "content": "Content for subsection 1.1.\r\n",
    "sections": {
      "h1": "Section 1",
      "h2": "Subsection 1.1"
    },
    "ordinal_position": 2
  },
  {
    "content": "Content for section 2.\r\n",
    "sections": {
      "h1": "Section 2",
      "h2": ""
    },
    "ordinal_position": 3
  }
}   
```

## Map Markdown one-to-many fields to search fields

Field mappings associate a source field with a destination field in situations where the field names and types aren't identical. But field mappings can also be used to match parts of a Markdown document and "lift" them into top-level fields of the search document.

The following example illustrates this scenario. For more information about field mappings in general, see [field mappings](search-indexer-field-mappings.md). 

Assume a search index with the following fields: `raw_content` of type `Edm.String`, `h1_header` of type `Edm.String`, and `h2_header` of type `Edm.String`. To map your Markdown into the desired shape, use the following field mappings:

```http
"fieldMappings" : [
    { "sourceFieldName" : "/content", "targetFieldName" : "raw_content" },
    { "sourceFieldName" : "/sections/h1", "targetFieldName" : "h1_header" },
    { "sourceFieldName" : "/sections/h2", "targetFieldName" : "h2_header" },
  ]
```

The resulting search document in the index would look as follows:
```http
{
  {
    "raw_content": "Content for section 1.\r\n",
    "h1_header": "Section 1",
    "h2_header": "",
  },
  {
    "raw_content": "Content for section 1.1.\r\n",
    "h1_header": "Section 1",
    "h2_header": "Subsection 1.1",
  },
  {
    "raw_content": "Content for section 2.\r\n",
    "h1_header": "Section 2",
    "h2_header": "",
  }
}
```

<a name="parsing-markdown-one-to-one"></a>

## Markdown one-to-one parsing mode (Markdown to a single document)

In **Markdown one-to-one parsing mode**, the entire Markdown document is indexed as a single search document, preserving the hierarchy and structure of the original content. This mode is most useful when the files to be indexed share a common structure, so that you can leverage this common structure in the index to make the relevant fields searchable.

Within the indexer definition, set the `parsingMode` to "Markdown" and use the optional `markdownHeaderDepth` parameter to define the maximum heading depth for chunking. If not specified, it defaults to `h6`, capturing all possible header depths.

The Markdown is parsed based on headers into documents which contain the following content: 

- `document_content`: Contains the full Markdown text as a single string. This field serves as a raw representation of the input document. 

- `sections`: An array of objects that contains the hierarchical representation of the sections within the Markdown document. Each section is represented as an object within this array and captures the structure of the document in a nested manner corresponding to the headers and their respective content. The fields are accessible through field mappings by referencing the path, for example `/sections/content`. The objects in this array have the following properties: 

  - `header_level`: A string that indicates the level of the header (`h1`, `h2`, `h3`, etc.) in Markdown syntax. This field helps in understanding the hierarchy and structuring of the content. 

  - `header_name`: A string containing the text of the header as it appears in the Markdown document. This field provides a label or title for the section. 

  - `content`: A string containing text content that immediately follows the header, up to the next header. This field captures the detailed information or description associated with the header. If there is no content directly under a header, this is an empty string. 

  - `ordinal_position`: An integer value indicating the position of the section within the document hierarchy. This field is used for ordering the sections in their original sequence as they appear in the document, beginning with an ordinal position of 1 and incrementing sequentially for each content block. 

  - `sections`: An array that contains objects representing subsections nested under the current section. This array follows the same structure as the top-level `sections` array, allowing for the representation of multiple levels of nested content. Each subsection object also includes `header_level`, `header_name`, `content`, and `ordinal_position` properties, enabling a recursive structure that represents and hierarchy of the Markdown content. 

Consider the following Markdown content. We use this content to explain an index schema that's designed around it, and what the search documents might look like for each parsing mode.

```md
# Section 1
Content for section 1.

## Subsection 1.1
Content for subsection 1.1.

# Section 2
Content for section 2.
```

 ### Index schema for one-to-one parsed Markdown files
If you are not utilizing field mappings, the shape of the index should reflect the shape of the Markdown content. Based on  the  previous Markdown, the index should look similar to the following example:
```http
{
  "name": "my-markdown-index",
  "fields": [
  {
    "name": "document_content",
    "type": "Edm.String",
  {
    "name": "sections",
    "type": "Edm.ComplexType",
    "fields": [
    {
      "name": "header_level",
      "type": "Edm.String",
    },
    {
      "name": "header_name",
      "type": "Edm.String",
    },
    {
      "name": "content",
      "type": "Edm.String"
    },
    {
      "name": "ordinal_position",
      "type": "Edm.Int"
    },
    {
      "name": "sections",
      "type": "Edm.ComplexType",
      "fields": [
      {
        "name": "header_level",
        "type": "Edm.String",
      },
      {
        "name": "header_name",
        "type": "Edm.String",
      },
      {
        "name": "content",
        "type": "Edm.String"
      },
      {
        "name": "ordinal_position",
        "type": "Edm.Int"
      }]
    }]
  }
}
```

Because the Markdown we want to index only goes to a depth of `h2` ("##"), we need `sections` fields nested to a depth of 2 to match that. This configuration would result in the following data in the index:

```http
  "document_content": "# Section 1\r\nContent for section 1.\r\n## Subsection 1.1\r\nContent for subsection 1.1.\r\n# Section 2\r\nContent for section 2.\r\n",
  "sections": [
    {
      "header_level": "h1",
      "header_name": "Section 1",
      "content": "Content for section 1.",
      "ordinal_position": 1,
      "sections": [
        {
          "header_level": "h2",
          "header_name": "Subsection 1.1",
          "content": "Content for subsection 1.1.",
          "ordinal_position": 2,
        }]
    }],
    {
      "header_level": "h1",
      "header_name": "Section 2",
      "content": "Content for section 2.",
      "ordinal_position": 3,
      "sections": []
    }]
  }
```

As you can see, the ordinal position increments based on the location of the content within the document.

It should also be noted that if header levels are skipped in the content, then structure of the resulting document reflects the headers that are present in the Markdown content, not necessarily containing nested sections for `h1` through `h6` consecutively. For example, when the document begins at `h2`, then the first element in the top-level sections array is `h2`. 

```http
POST https://[service name].search.windows.net/indexers?api-version=2024-07-01
Content-Type: application/json
api-key: [admin key]

{
  "name": "my-markdown-indexer",
  "dataSourceName": "my-blob-datasource",
  "targetIndexName": "my-target-index",
  "parameters": {
    "configuration": {
      "parsingMode": "markdown",
      "markdownParsingSubmode": "oneToMany",
    }
  }
}
```
## Map Markdown one-to-one fields to search fields
If you would like to extract fields with custom names from the document, you can use field mappings to do so. Using the same Markdown sample as before, consider the following index configuration:

```http
{
  "name": "my-markdown-index",
  "fields": [
    {
      "name": "document_content",
      "type": "Edm.String",
    },
    {
      "name": "document_title",
      "type": "Edm.String",
    },
    {
      "name": "opening_subsection_title"
      "type": "Edm.String",
    }
    {
      "name": "summary_content",
      "type": "Edm.String",
    }
  ]
}
```

Extracting specific fields from the parsed Markdown is handled similar to how the document paths are in (outputFieldMappings)[https://learn.microsoft.com/en-us/azure/search/cognitive-search-output-field-mapping?tabs=rest], except the path begins with `/sections`  instead of  `/document`. So, for example, `/sections/0/content` would map to the content under the item at position 0 in the sections array.

An example of a strong use case might look something like this: all Markdown files have a document title in the first `h1`, a subsection title in the first `h2`, and a summary in the content of the final paragraph underneath the final `h1`. You could use the following field mappings to index only that content:

```http
"fieldMappings" : [
  { "sourceFieldName" : "/content", "targetFieldName" : "raw_content" },
  { "sourceFieldName" : "/sections/0/header_name", "targetFieldName" : "document_title" },
  { "sourceFieldName" : "/sections/0/sections/header_name", "targetFieldName" : "opening_subsection_title" },
  { "sourceFieldName" : "/sections/1/content", "targetFieldName" : "summary_content" },
]
```

Here you would extract only the relevant pieces from that document. To most effectively use this functionality, documents you plan to index should share the same hierarchical header structure.

The resulting search document in the index would look as follows:
```http
{
  "content": "Content for section 1.\r\n",
  "document_title": "Section 1",
  "opening_subsection_title": "Subsection 1.1",
  "summary_content": "Content for section 2."
}
```

> [!NOTE]
> These examples specify how to use these parsing modes entirely with or without field mappings, but you can leverage both in one scenario if that suits your needs.

## Next steps

+ [Configure blob indexers](search-howto-indexing-azure-blob-storage.md)
+ [Define field mappings](search-indexer-field-mappings.md)
+ [Indexers overview](search-indexer-overview.md)
+ [How to index CSV blobs with a blob indexer](search-howto-index-csv-blobs.md)
+ [Tutorial: Search Markdown data from Azure Blob Storage](search-markdown-data-tutorial.md)
