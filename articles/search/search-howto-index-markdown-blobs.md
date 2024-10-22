---
title: Search over markdown blobs
titleSuffix: Azure AI Search
description: Extract searchable text from Markdown blobs using the blob indexer in Azure AI Search. Indexers provide indexing automation for supported data sources like Azure Blob Storage.

author: mdonovan
ms.author: mdonovan

ms.service: cognitive-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 10/22/2024
---

# Index Markdown blobs and files in Azure AI Search

**Applies to**: [Blob indexers](search-howto-indexing-azure-blob-storage.md), [File indexers](search-file-storage-integration.md)

In Azure AI Search, indexers for Azure Blob Storage and Azure Files support a `markdown` parsing mode for markdown files. Markdown files can be indexed in two ways: 
+ One-To-Many Parsing Mode
+ One-To-One Parsing Mode

The blob indexer provides a `submode` parameter to determine the output of structure of the search document(s). Markdown parsing mode provides the following sub-mode options:

| parsingMode | submode | Search document | Description |
|--------------|-------------|-------------|--------------|
| **`markdown`** | **`oneToMany`** | Multiple per blob | (default) Breaks the markdown into multiple search documents, each representing a content (non-header) section of the markdown file. |
| **`markdown`** | **`oneToOne`** | One per blob | Parses the markdown into one search document, with sections mapped to specific headers in the markdown file.|

The blob indexer also provides a `markdownHeaderDepth` parameter, which accepts arguments in the form `h1` through `h6`, corresponding to the markdown headers "#" through "######". This parameter determines the deepest header level that will be considered when parsing, allowing for flexible handling of document structure (eg. if `markdownHeaderDepth` is set to `h1`, the parser will only recognize top-level headers that begin with "#", and all lower-level headers will be treated as plain content). If not specified, it defaults to `h6`, capturing all possible header depths. This setting can be changed after initial creation of the indexer, however the resulting search documents may be structured differently and may no longer fit the index depending on the content being indexed, so the indexex may need to be updated or recreated accordingly.
For **`oneToMany`** submode, you should review [Indexing one blob to produce many search documents](search-howto-index-one-to-many-blobs.md) to understand how the blob indexer handles disambiguation of the document key for multiple search documents produced from the same blob.

Within the indexer definition, you can optionally set [field mappings](search-indexer-field-mappings.md) to choose which properties of the source JSON document are used to populate your target search index. 

The following sections describe each mode in more detail. If you're unfamiliar with indexer clients and concepts, see [Create a search indexer](search-howto-create-indexers.md). You should also be familiar with the details of [basic blob indexer configuration](search-howto-indexing-azure-blob-storage.md), which isn't repeated here.

<a name="parsing-markdown-one-to-many"></a>

## Markdown One-To-Many Parsing Mode (Markdown Sections to Multiple Documents)

The **Markdown One-To-Many Parsing Mode** mode parses markdown files into multiple search documents, where each document corresponds to a specific section of the markdown file based on the header metadata at that point in the document.

Consider the following markdown content:

```md
# Section 1
Content for section 1.

## Subsection 1.1
Content for subsection 1.1.

# Section 2
Content for section 2.
```

The blob indexer parses the markdown document into one search document for each content section, providing all the header metadata at that point in the document. Given an index with a "content" field, as well as a complex "sections" field with subfields "h1" and "h2", the blob indexer can infer the correct mapping without a field mapping present in the request. This document would result in 3 search documents after indexing, due to the 3 content sections. The search document resulting from the first content section of the provided markdown document would contain the following values for "content", "sections", "h1", and "h2":

```http
    "content": "Content for section 1.\r\n",
    "sections": {
        "h1": "Section 1",
        "h2": ""
      }
    },
```

Note that there is no value for `h2`, because no `h2` is set at that point in the file.

For markdown `oneToMany` parsing, the indexer definition should look similar to the following example:
```http
POST https://[service name].search.windows.net/indexers?api-version=2024-07-01
Content-Type: text/markdown
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


## Map markdown one-to-many fields to search fields

Field mappings associate a source field with a destination field in situations where the field names and types aren't identical. But field mappings can also be used to match parts of a markdown document and "lift" them into top-level fields of the search document.

The following example illustrates this scenario. For more information about field mappings in general, see [field mappings](search-indexer-field-mappings.md). 

Assume a search index with the following fields: `raw_content` of type `Edm.String`, `h1_header` of type `Edm.String`, and `h2_header` of type `Edm.String`,`. To map your markdown into the desired shape, use the following field mappings:

```http
"fieldMappings" : [
    { "sourceFieldName" : "/content", "targetFieldName" : "raw_content" },
    { "sourceFieldName" : "/sections/h1", "targetFieldName" : "h1_header" },
    { "sourceFieldName" : "/sections/h2", "targetFieldName" : "h2_header" },
  ]
```

<a name="parsing-markdown-one-to-one"></a>

## Markdown One-To-One Parsing Mode (Markdown as a Single Document)

In **Markdown One-To-One Parsing Mode**, the entire markdown document is indexed as a single search document, preserving the hierarchy and structure of the original content. This is most useful when the files to be indexed share a common structure, so that you can leverage this common structure in the index to make the relevant fields searchable.

Within the indexer definition, set the `parsingMode` to "markdown" and use the optional `markdownHeaderDepth` parameter to define the maximum heading depth for chunking. If not specified, it defaults to `h6`, capturing all possible header depths.

The markdown will be parsed based on headers into documents which will contain the following content: 

- `document_content`: Contains the full markdown text as a single string. This serves as a raw representation of the input document. 

- `sections`: An array that contains the hierarchical representation of the sections within the markdown document. Each section is represented as an object within this array and captures the structure of the document in a nested manner corresponding to the headers and their respective content. The objects in this array have the following properties: 

  - `header_level`: Indicates the level of the header (`h1`, `h2`, `h3`, etc.) in markdown syntax. This helps in understanding the hierarchy and structuring of the content. 

  - `header_name`: The text of the header as it appears in the markdown document. This provides a label or title for the section. 

  - `content`: The text content that immediately follows the header, up to the next header. This captures the detailed information or description associated with the header. If there is no content directly under a header, this field is represented by an empty string. 

  - `ordinal_position`: A numerical value indicating the position of the section within the document hierarchy. This is used for ordering the sections in their original sequence as they appear in the document. The root level sections start with an ordinal position of 0, and the value increments sequentially for each subsection. 

  - `sections`: An array that contains objects representing subsections nested under the current section. This array follows the same structure as the top-level sections array, allowing for the representation of multiple levels of nested content. Each subsection object also includes header_level, header_name, content, and ordinal_position properties, enabling a recursive structure that accurately represents the depth and organization of the markdown content. 

  Consider the following markdown content:

```md
# Section 1
Content for section 1.

## Subsection 1.1
Content for subsection 1.1.

# Section 2
Content for section 2.
```

### One-to-one parsing not utilizing field mappings
If not utilizing field mappings, the shape of the index should reflect the shape of the markdown content. So using the markdown above, the index should look similar to the following:
{
  "name": "markdown-onetoone-no-fieldmappings",
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
            }
          ]
        }
      ]
    }
  ]
}
```

Because the markdown we want to index only goes to a depth of h2 ("##"), we need `sections` fields nested to a depth of 2 to match that. This would result in the following data in index:

```http
    "document_content": "# Section 1\r\nContent for section 1.\r\n## Subsection 1.1\r\nContent for subsection 1.1.\r\n# Section 2\r\nContent for section 2.\r\n",
    "sections": {
      [
        "header_level": "h1",
        "header_name": "Section 1",
        "content": "Content for section 1.",
        "ordinal_position": 1,
        "sections": {
          "header_level": "h2",
          "header_name": "Subsection 1.1",
          "content": "Content for subsection 1.1.",
          "ordinal_position": 2,
        }
      ],
      [
        "header_level": "h1",
        "header_name": "Section 2",
        "content": "Content for section 2.",
        "ordinal_position": 3,
        "sections": {
          []
        }
      ]
      }
    },
```

As you can see, the ordinal position increments based on the location of the content within the document.

It should also be noted that if header levels are skipped in the content, for example, the document begins at "h2", then the first element in the top-level sections array will be "h2. In other words, the structure of the resulting document reflects the headers that are present in the markdown content, not necessarily containing nested sections for `h1` through `h6` consecutively.

```http
POST https://[service name].search.windows.net/indexers?api-version=2024-07-01
Content-Type: text/markdown
api-key: [admin key]

{
  "name": "my-markdown-indexer",
  "dataSourceName": "my-blob-datasource",
  "targetIndexName": "my-target-index",
  "parameters": {
    "configuration": {
      "parsingMode": "markdown",
      "markdownParsingSubmode": "oneToMany",
      "markdownHeaderDepth": "h3"
    }
  }
}
```
## Map markdown one-to-one fields to search fields
If you would like to extract fields with custom names from the document, you can use field mappings to do so. Using the same markdown file from above, consider the following index configuration:

{
  "name": "markdown-onetoone-with-fieldmappings",
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

In order to extract the relevant pieces, you can access the fields similar to how paths are handled in (outputFieldMappings)[https://learn.microsoft.com/en-us/azure/search/cognitive-search-output-field-mapping?tabs=rest]. The difference being you are accessing `sections` object, so `/sections/0/content` would map to the content underneath the very first header in the document.
This would be useful in the case where the markdown files all have a document title in the very first `h1`, a subsection title in the first `h2`, and a summary in the content of the final paragraph underneath the final `h1`. You could use the following field mappings to index only that content:

```http
"fieldMappings" : [
    { "sourceFieldName" : "/content", "targetFieldName" : "raw_content" },
    { "sourceFieldName" : "/sections/0/header_name", "targetFieldName" : "document_title" },
    { "sourceFieldName" : "/sections/0/sections/header_name", "targetFieldName" : "opening_subsection_title" },
    { "sourceFieldName" : "/sections/1/content", "targetFieldName" : "summary_content" },
  ]
```

Here you would extract only the relevant pieces from that document. To most effectively leverage this functionality, it is important that all the documents you plan to index share the same hierarchical header structure.

The resulting search document in the index would look as follows:
```http
    "content": "Content for section 1.\r\n",
    "document_title": "Section 1",
    "opening_subsection_title": "Subsection 1.1",
    "summary_content": "Content for section 2."
```

> [!NOTE]
> These examples specify how to use these parsing modes entirely with or without field mappings, but you can leverage both in one scenario if that suits your needs. (TODO-review: unlikely use case but may be worth acknowleding)
> As with all indexers, if fields do not clearly match, you should expect to explicitly specify individual [field mappings](search-indexer-field-mappings.md) unless you are using the implicit fields mappings available for blob content and metadata, as described in [basic blob indexer configuration](search-howto-indexing-azure-blob-storage.md).

## Next steps

+ [Configure blob indexers](search-howto-indexing-azure-blob-storage.md)
+ [Define field mappings](search-indexer-field-mappings.md)
+ [Indexers overview](search-indexer-overview.md)
+ [How to index CSV blobs with a blob indexer](search-howto-index-csv-blobs.md)
+ [Tutorial: Search semi-structured data from Azure Blob Storage](search-semi-structured-data.md)
