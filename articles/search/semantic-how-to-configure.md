---
title: Configure semantic ranker
titleSuffix: Azure AI Search
description: Add a semantic configuration to a search index.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 11/21/2025
---

# Configure semantic ranker and return captions in search results

Semantic ranking iterates over an initial result set, applying an L2 ranking methodology that promotes the most semantically relevant results to the top of the stack. You can also get semantic captions, with highlights over the most relevant terms and phrases, and [semantic answers](semantic-answers.md).

This article explains how to configure a search index for semantic reranking.

> [!NOTE]
> If you have existing code that calls preview or previous API versions, see [Migrate semantic ranking code](semantic-code-migration.md) for help with modifying your code.

## Prerequisites

+ Azure AI Search in any [region that provides semantic ranking](search-region-support.md).

+ Semantic ranker [enabled on your search service](semantic-how-to-enable-disable.md).

+ An existing search index with rich text content. Semantic ranking applies to strings (nonvector) fields and works best on content that is informational or descriptive.

## Choose a client

You can specify a semantic configuration on new or existing indexes, using any of the following tools and software development kits (SDKs) to add a semantic configuration:

+ [Azure portal](https://portal.azure.com), using the index designer to add a semantic configuration.
+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) and a [Create or Update Index (REST) API](/rest/api/searchservice/indexes/create-or-update).
+ [Azure SDK for .NET](https://www.nuget.org/packages/Azure.Search.Documents)
+ [Azure SDK for Python](https://pypi.org/project/azure-search-documents)
+ [Azure SDK for Java](https://central.sonatype.com/artifact/com.azure/azure-search-documents)
+ [Azure SDK for JavaScript](https://www.npmjs.com/package/@azure/search-documents)

## Add a semantic configuration

Some workloads create a semantic configuration automatically. If you're using [agentic retrieval](agentic-retrieval-overview.md) and a [knowledge source that indexes content](agentic-knowledge-source-overview.md#supported-knowledge-sources) on Azure AI Search, your generated index already has a semantic configuration that works for your content.

For other workloads, you can set up a semantic configuration yourself. A *semantic configuration* is a section in your index that establishes the field inputs used for semantic ranking. You can add or update a semantic configuration at any time, no rebuild necessary. If you create multiple configurations, you can specify a default. At query time, specify a semantic configuration on a [query request](semantic-how-to-query-request.md), or leave it blank to use the default.

You can create up to 100 semantic configurations in a single index.

A semantic configuration has a name and the following properties:

| Property | Characteristics |
|----------|-----------------|
| Title field | A short string, ideally under 25 words. This field could be the title of a document, name of a product, or a unique identifier. If you don't have suitable field, leave it blank. | 
| Content fields | Longer chunks of text in natural language form, subject to [maximum token input limits](semantic-search-overview.md#how-the-system-collects-and-summarizes-inputs) on the machine learning models. Common examples include the body of a document, description of a product, or other free-form text. | 
| Keyword fields | A list of keywords, such as the tags on a document, or a descriptive term, such as the category of an item. | 

You can only specify one title field, but you can have as many content and keyword fields as you like. For content and keyword fields, list the fields in priority order because lower priority fields might get truncated.

Across all semantic configuration properties, the fields you assign must be:

+ Attributed as `searchable` and `retrievable`
+ Strings of type `Edm.String`, `Collection(Edm.String)`, string subfields of `Edm.ComplexType`

### [**Azure portal**](#tab/portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to a search service that has [semantic ranking enabled](semantic-how-to-enable-disable.md).

1. From **Indexes** on the left-navigation pane, select an index.

1. Select **Semantic configurations** and then select **Add semantic configuration**.

   :::image type="content" source="./media/semantic-search-overview/add-semantic-config.png" alt-text="Screenshot that shows the option to add a semantic configuration in the Azure portal." lightbox="./media/semantic-search-overview/add-semantic-config.png" border="true":::

1. On the **New semantic configuration** page, enter a semantic configuration name and select the fields to use in the semantic configuration. Only searchable and retrievable string fields are eligible. Make sure to list content fields and keyword fields in priority order.

   :::image type="content" source="./media/semantic-search-overview/create-semantic-config.png" alt-text="Screenshot that shows how to create a semantic configuration in the Azure portal." lightbox="./media/semantic-search-overview/create-semantic-config.png" border="true":::

1. Select **Save** to save the configuration settings.
1. Select **Save** again on the index page to save the semantic configuration in the index.

### [**REST API**](#tab/rest)

1. Formulate a [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) request.

1. Add a semantic configuration to the index definition, perhaps after `scoringProfiles` or `suggesters`. Specifying a default is optional but useful if you have more than one configuration.

    ```json
    "semantic": {
        "defaultConfiguration": "my-semantic-config-default",
        "configurations": [
            {
                "name": "my-semantic-config-default",
                "prioritizedFields": {
                    "titleField": {
                        "fieldName": "HotelName"
                    },
                    "prioritizedContentFields": [
                        {
                            "fieldName": "Description"
                        }
                    ],
                    "prioritizedKeywordsFields": [
                        {
                            "fieldName": "Tags"
                        }
                    ]
                }
            },
                        {
                "name": "my-semantic-config-desc-only",
                "prioritizedFields": {
                    "prioritizedContentFields": [
                        {
                            "fieldName": "Description"
                        }
                    ]
                }
            }
        ]
    }
    ```

### [**.NET SDK**](#tab/sdk)

Use the [SemanticConfiguration class](/dotnet/api/azure.search.documents.indexes.models.semanticconfiguration?view=azure-dotnet&branch=main&preserve-view=true) in the Azure SDK for .NET.

The following example is from the [semantic ranking sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample08_SemanticSearch.md) authored by the Azure SDK team.

```c#
string indexName = "hotel";
SearchIndex searchIndex = new(indexName)
{
    Fields =
    {
        new SimpleField("HotelId", SearchFieldDataType.String) { IsKey = true, IsFilterable = true, IsSortable = true, IsFacetable = true },
        new SearchableField("HotelName") { IsFilterable = true, IsSortable = true },
        new SearchableField("Description") { IsFilterable = true },
        new SearchableField("Category") { IsFilterable = true, IsSortable = true, IsFacetable = true },
    },
    SemanticSearch = new()
    {
        Configurations =
        {
            new SemanticConfiguration("my-semantic-config", new()
            {
                TitleField = new SemanticField("HotelName"),
                ContentFields =
                {
                    new SemanticField("Description")
                },
                KeywordsFields =
                {
                    new SemanticField("Category")
                }
            })
        }
    }
};
```

---

## Opt in for prerelease semantic ranking models

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Using [previewREST APIs](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) and preview Azure SDKs that provide the property, you can optionally configure an index to use prerelease semantic ranking models if one is deployed in your region. There's no mechanism for knowing if a prerelease is available, or if it was used on specific query. For this reason, we recommend that you use this property in test environments, and only if you're interested in trying out the very latest semantic ranking models.

The configuration property is `"flightingOptIn": true`, and it's set in the semantic configuration section of an index. The property is null or false by default. You can set it true on a create or update request at any time, and it affects semantic queries moving forward, assuming the query stipulates a semantic configuration that includes the property.

```rest
PUT https://myservice.search.windows.net/indexes('hotels')?allowIndexDowntime=False&api-version=2025-11-01-preview

{
  "name": "hotels",
  "fields": [ ],
  "scoringProfiles": [ ],
  "defaultScoringProfile": "geo",
  "suggesters": [ ],
  "analyzers": [ ],
  "corsOptions": { },
  "encryptionKey": { },
  "similarity": { },
  "semantic": {
    "configurations": [
      {
        "name": "semanticHotels",
        "prioritizedFields": {
          "titleField": {
            "fieldName": "hotelName"
          },
        "prioritizedContentFields": [
            {
              "fieldName": "description"
            },
            {
              "fieldName": "description_fr"
            }
          ],
        "prioritizedKeywordsFields": [
            {
              "fieldName": "tags"
            },
            {
              "fieldName": "category"
            }
          ],
        "flightingOptIn": true
        }
      }
    ]
  },
  "vectorSearch": {  }
}
```

## Next steps

Test your semantic configuration by running a semantic query.

> [!div class="nextstepaction"]
> [Create a semantic query](semantic-how-to-query-request.md)
