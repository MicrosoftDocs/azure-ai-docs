---
title: AI enrichment concepts
titleSuffix: Azure AI Search
description: Content extraction, natural language processing (NLP), and image processing can create searchable content in Azure AI Search indexes.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 10/06/2025
ms.update-cycle: 180-days
---

# AI enrichment in Azure AI Search

In Azure AI Search, *AI enrichment* refers to integration with [Foundry Tools](/azure/ai-services/what-are-ai-services) to process content that isn't searchable in its raw form. Through enrichment, analysis and inference are used to create searchable content and structure where none previously existed.

Because Azure AI Search is used for text and vector queries, the purpose of AI enrichment is to improve the utility of your content in search-related scenarios. Raw content must be text or images (you can't enrich vectors), but the output of an enrichment pipeline can be vectorized and indexed in a search index using skills like [Text Split skill](cognitive-search-skill-textsplit.md) for chunking and [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) for vector encoding. For more information about using skills in vector scenarios, see [Integrated data chunking and embedding](vector-search-integrated-vectorization.md).

AI enrichment is based on [*skills*](cognitive-search-working-with-skillsets.md).

[Built-in skills](cognitive-search-predefined-skills.md) tap Foundry Tools. They apply the following transformations and processing to raw content:

+ Translation and language detection for multilingual search.
+ Entity recognition to extract people names, places, and other entities from large chunks of text.
+ Key phrase extraction to identify and output important terms.
+ Optical character recognition (OCR) to recognize printed and handwritten text in binary files.
+ Image analysis to describe image content and output the descriptions as searchable text fields.
+ Text embeddings via Azure OpenAI for integrated vectorization.
+ Multimodal embeddings via Azure Vision in Foundry Tools for text and image vectorization.

Custom skills run your external code. You can use custom skills for any custom processing you want to include in the pipeline.

AI enrichment is an extension of an [indexer pipeline](search-indexer-overview.md) that connects to Azure data sources. An enrichment pipeline has all of the components of an indexer pipeline (indexer, data source, index) and a [skillset](cognitive-search-working-with-skillsets.md) that specifies atomic enrichment steps.

The following diagram shows the progression of AI enrichment:

  :::image type="content" source="media/cognitive-search-intro/cognitive-search-enrichment-architecture.png" alt-text="Diagram of an enrichment pipeline." border="true":::

**Import** is the first step. Here, the indexer connects to a data source and pulls content (documents) into the search service. [Azure Blob Storage](/azure/storage/blobs/storage-blobs-overview) is the most common resource used in AI enrichment scenarios, but any supported data source can provide content.

**Enrich & Index** covers most of the AI enrichment pipeline:

+ Enrichment starts when the indexer *[cracks documents](search-indexer-overview.md#document-cracking)* and extracts images and text. The type of processing that occurs next depends on your data and the skills you've added to a skillset. Images can be forwarded to [skills that perform image processing](cognitive-search-concept-image-scenarios.md). Text content is queued for text and natural language processing. Internally, skills create an *[enriched document](cognitive-search-working-with-skillsets.md#enrichment-tree)* that collects transformations as they occur.

+ Enriched content is generated during skillset execution and is temporary unless you save it. You can enable an [enrichment cache](enrichment-cache-how-to-configure.md) to persist skill outputs for reuse in future skillset executions.

+ To get content into a search index, the indexer must have mapping information for sending enriched content to target field. [Field mappings](search-indexer-field-mappings.md) (explicit or implicit) set the data path from source data to a search index. [Output field mappings](cognitive-search-output-field-mapping.md) set the data path from enriched documents to an index.

+ Indexing is the process wherein raw and enriched content is ingested into the physical data structures of a [search index](search-what-is-an-index.md) (its files and folders). Lexical analysis and tokenization occur in this step.

**Exploration** is the last step. Output is always a [search index](search-what-is-an-index.md) that you can query from a client app. Output can optionally be a [knowledge store](knowledge-store-concept-intro.md) consisting of blobs and tables in Azure Storage that are accessed through data exploration tools or downstream processes. If you're creating a knowledge store, [projections](knowledge-store-projection-overview.md) determine the data path for enriched content. The same enriched content can appear in both indexes and knowledge stores.

## When to use AI enrichment

Enrichment is useful if raw content is unstructured text, image content, or content that needs language detection and translation. Applying AI through the [built-in skills](cognitive-search-predefined-skills.md) can unlock this content for full-text search and data science applications.

You can also create [custom skills](cognitive-search-create-custom-skill-example.md) to provide external processing.
Open-source, third-party, or first-party code can be integrated into the pipeline as a custom skill. Classification models that identify salient characteristics of various document types fall into this category, but any external package that adds value to your content could be used.

### Use-cases for built-in skills

Built-in skills are based on the Foundry Tools APIs: [Azure Vision](/azure/ai-services/computer-vision/) and [Azure Language](/azure/ai-services/language-service/overview). Unless your content input is small, you are expected to [attach a billable Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) to run larger workloads.

A [skillset](cognitive-search-defining-skillset.md) that's assembled using built-in skills is well suited for the following application scenarios:

+ **Image processing** skills include [Optical Character Recognition (OCR)](cognitive-search-skill-ocr.md) and identification of [visual features](cognitive-search-skill-image-analysis.md), such as facial detection, image interpretation, image recognition (famous people and landmarks), or attributes like image orientation. These skills create text representations of image content for full-text search in Azure AI Search.

+ **Machine translation** is provided by the [Text Translation](cognitive-search-skill-text-translation.md) skill, often paired with [language detection](cognitive-search-skill-language-detection.md) for multi-language solutions.

+ **Natural language processing** analyzes chunks of text. Skills in this category include [Entity Recognition](cognitive-search-skill-entity-recognition-v3.md), [Sentiment Detection (including opinion mining)](cognitive-search-skill-sentiment-v3.md), and [Personal Identifiable Information Detection](cognitive-search-skill-pii-detection.md). With these skills, unstructured text is mapped as searchable and filterable fields in an index.

### Use-cases for custom skills

[Custom skills](cognitive-search-create-custom-skill-example.md) execute external code that you provide and wrap in the [custom skill web interface](cognitive-search-custom-skill-interface.md). Several examples of custom skills can be found in the [azure-search-power-skills](https://github.com/Azure-Samples/azure-search-power-skills/blob/main/README.md) GitHub repository.

Custom skills aren’t always complex. For example, if you have an existing package that provides pattern matching or a document classification model, you can wrap it in a custom skill.

## Storing output

In Azure AI Search, an indexer saves the output it creates. A single indexer run can create up to three data structures that contain enriched and indexed output.

| Data store | Required | Location | Description |
|------------|----------|----------|-------------|
| [searchable index](search-what-is-an-index.md) | Required | Search service | Used for full-text search and other query forms. Specifying an index is an indexer requirement. Index content is populated from skill outputs, plus any source fields that are mapped directly to fields in the index. |
| [knowledge store](knowledge-store-concept-intro.md) | Optional | Azure Storage | Used for downstream apps like knowledge mining, data science, and multimodal search. A knowledge store is defined within a skillset. Its definition determines whether your enriched documents are projected as tables or objects (files or blobs) in Azure Storage. For [multimodal search scenarios](multimodal-search-overview.md#how-does-multimodal-search-work), you can save extracted images to the knowledge store and reference them at query time, allowing the images to be returned directly to client apps. |
| [enrichment cache](enrichment-cache-how-to-configure.md) | Optional | Azure Storage | Used for caching enrichments for reuse in subsequent skillset executions. The cache stores imported, unprocessed content (cracked documents). It also stores the enriched documents created during skillset execution. Caching is helpful if you're using image analysis or OCR, and you want to avoid the time and expense of reprocessing image files. |

Indexes and knowledge stores are fully independent of each other. While you must attach an index to satisfy indexer requirements, if your sole objective is a knowledge store, you can ignore the index after it's populated.

## Exploring content

After you define and load a [search index](search-what-is-an-index.md) or [knowledge store](knowledge-store-concept-intro.md), you can explore its data.

### Query a search index

[Run queries](search-query-overview.md) to access the enriched content generated by the pipeline. The index is like any other you might create for Azure AI Search: you can supplement text analysis with custom analyzers, invoke fuzzy search queries, add filters, or experiment with scoring profiles to tune search relevance.

### Use data exploration tools on a knowledge store

In Azure Storage, a [knowledge store](knowledge-store-concept-intro.md) can assume the following forms: a blob container of JSON documents, a blob container of image objects, or tables in Table Storage. You can use [Storage Explorer](/azure/vs-azure-tools-storage-manage-with-storage-explorer), [Power BI](knowledge-store-connect-power-bi.md), or any app that connects to Azure Storage to access your content.

+ A blob container captures enriched documents in their entirety, which is useful if you're creating a feed into other processes.

+ A table is useful if you need slices of enriched documents, or if you want to include or exclude specific parts of the output. For analysis in Power BI, tables are the recommended data source for data exploration and visualization in Power BI.

## Availability and pricing

AI enrichment is available in regions that offer Foundry Tools. To check the availability of AI enrichment, see the [regions list](search-region-support.md).

Billing follows a Standard pricing model. Costs associated with built-in skills are incurred when you specify an Azure OpenAI in Foundry Models resource or Foundry resource key in the skillset. There are also costs associated with image extraction, as metered by Azure AI Search. However, text extraction and utility skills aren't billable. For more information, see [How you're charged for Azure AI Search](search-sku-manage-costs.md#how-youre-charged-for-the-base-service).

## Checklist: A typical workflow

An enrichment pipeline consists of [*indexers*](search-indexer-overview.md) that have [*skillsets*](cognitive-search-working-with-skillsets.md). Post-indexing, you can query an index to validate your results.

Start with a subset of data in a [supported data source](search-indexer-overview.md#supported-data-sources). Indexer and skillset design is an iterative process. The work goes faster with a small representative data set.

1. Create a [data source](/rest/api/searchservice/data-sources/create) that specifies a connection to your data.

1. [Create a skillset](cognitive-search-defining-skillset.md). Unless your project is small, you should [attach a Foundry resource](cognitive-search-attach-cognitive-services.md). If you're [creating a knowledge store](knowledge-store-create-rest.md), define it within the skillset.

1. [Create an index schema](search-how-to-create-search-index.md) that defines a search index.

1. [Create and run the indexer](search-howto-create-indexers.md) to bring all of the previous components together. This step retrieves the data, runs the skillset, and loads the index.

   An indexer is also where you specify field mappings and output field mappings that set up the data path to a search index.

   Optionally, [enable enrichment caching](enrichment-cache-how-to-configure.md) in the indexer configuration. This step allows you to reuse existing enrichments later on.

1. [Run queries](search-query-create.md) to evaluate results or [start a debug session](cognitive-search-how-to-debug-skillset.md) to work through any skillset issues.

To repeat any of the previous steps, [reset the indexer](search-howto-reindex.md) before you run it. Alternatively, you can delete and recreate the objects on each run (recommended if you're using the free tier). If you enabled caching, the indexer pulls from the cache if the source data is unchanged and if your edits to the pipeline don't invalidate the cache.

## Next steps

+ [Quickstart: Create a skillset for AI enrichment](search-get-started-skillset.md)
+ [Tutorial: Learn about the AI enrichment REST APIs](tutorial-skillset.md)
+ [Skillset concepts](cognitive-search-working-with-skillsets.md)
+ [Knowledge store concepts](knowledge-store-concept-intro.md)
+ [Create a skillset](cognitive-search-defining-skillset.md)
+ [Create a knowledge store](knowledge-store-create-rest.md)
