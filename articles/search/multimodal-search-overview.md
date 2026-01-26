---
title: Multimodal Search Concepts and Guidance
titleSuffix: Azure AI Search
description: Learn what multimodal search is, how Azure AI Search supports it for text and image content, and where to find detailed concepts, tutorials, and samples.
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 11/21/2025
author: gmndrg
ms.author: gimondra
---

# Multimodal search in Azure AI Search

Multimodal search refers to the ability to ingest, understand, and retrieve information across multiple content types, including text, images, video, and audio. In Azure AI Search, multimodal search natively supports the ingestion of documents containing text and images and the retrieval of their content, enabling you to perform searches that combine both modalities.

Building a robust multimodal pipeline typically involves:

1. Extracting inline images and page text from documents.

1. Describing images in natural language.

1. Embedding both text and images into a shared vector space.

1. Storing the images for later use as annotations.

Multimodal search also requires preserving the order of information as it appears in the documents and executing [hybrid queries](hybrid-search-overview.md) that combine [full-text search](search-lucene-query-architecture.md) with [vector search](vector-search-overview.md) and [semantic ranking](semantic-search-overview.md).

In practice, an application that uses multimodal search can answer questions like "What is the process to have an HR form approved?" even when the only authoritative description of the process lives inside an embedded diagram in a PDF file.

## Why use multimodal search?

Traditionally, multimodal search requires separate systems for text and image processing, often requiring custom code and low-level configurations from developers. Maintaining these systems incurs higher costs, complexity, and effort.

Azure AI Search addresses these challenges by integrating images into the same retrieval pipeline as text. With a single multimodal pipeline, you can simplify setup and unlock information that resides in charts, screenshots, infographics, scanned forms, and other complex visuals.

Multimodal search is ideal for [retrieval-augmented generation (RAG)](retrieval-augmented-generation-overview.md) scenarios. By interpreting the structural logic of images, multimodal search makes your RAG application or AI agent less likely overlook important visual details. It also provides your users with detailed answers that can be traced back to their original sources, regardless of the source's modality.

## How does multimodal search work?

To simplify the creation of a multimodal pipeline, Azure AI Search offers the **Import data (new)** wizard in the Azure portal. The wizard helps you configure a data source, define extraction and enrichment settings, and generate a multimodal index that contains text, embedded image references, and vector embeddings. For more information, see [Quickstart: Multimodal search in the Azure portal](search-get-started-portal-image-search.md).

The wizard follows these steps to create a multimodal pipeline:

1. **Extract content:** Choose from the [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md), or [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md) to obtain page text, inline images, and structural metadata. Each skill offers different capabilities for metadata extraction, table handling, and file format support. For detailed comparisons, see [Options for multimodal content extraction](#options-for-multimodal-content-extraction).

1. **Chunk text:** The [Text Split skill](cognitive-search-skill-textsplit.md) breaks the extracted text into manageable chunks for use in the remaining pipeline, such as the embedding skill.

1. **Generate image descriptions:** The [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) verbalizes images, producing concise natural-language descriptions for text search and embedding using a large language model (LLM).

1. **Generate embeddings:** The embedding skill creates vector representations of text and images, enabling similarity and hybrid retrieval. You can call [Azure OpenAI](cognitive-search-skill-azure-openai-embedding.md), [Microsoft Foundry](cognitive-search-aml-skill.md), or [Azure Vision](cognitive-search-skill-vision-vectorize.md) embedding models natively.

   Alternatively, you can skip image verbalization and pass the extracted text and images directly to a multimodal embedding model through the [AML skill](cognitive-search-aml-skill.md) or [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md). For more information, see [Options for multimodal content embedding](#options-for-multimodal-content-embedding).

1. **Store extracted images:** The [knowledge store](knowledge-store-concept-intro.md) contains extracted images that can be returned directly to client applications. When you use the wizard, an image's location is stored directly in the multimodal index, enabling convenient retrieval at query time.

> [!TIP]
> To see multimodal search in action, plug your wizard-created index into the [multimodal RAG sample application](https://aka.ms/azs-multimodal-sample-app-repo). The sample demonstrates how a RAG application consumes a multimodal index and renders both textual citations and associated image snippets in the response. The sample also showcases the code-based process of data ingestion and indexing.

## Options for multimodal content extraction

A multimodal pipeline begins by cracking each source document into chunks of text, inline images, and associated metadata. For this step, Azure AI Search provides three built-in skills:

+ [Document Extraction skill](cognitive-search-skill-document-extraction.md)
+ [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md)
+ [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md)

| Characteristic | Document Extraction skill | Document Layout skill | Azure Content Understanding skill |
|--|--|--|--|
| Text location metadata extraction (pages and bounding polygons) | No | Yes | Yes |
| Image location metadata extraction (pages and bounding polygons) | Yes | Yes | Yes |
| Table extraction and preservation | No | No | Yes (including cross-page tables) |
| Cross-page semantic units | Not applicable | Single page only | Yes (spans page boundaries) |
| Location metadata extraction based on file type | PDFs only. | Multiple supported file types according to the [Azure Document Intelligence in Foundry Tools layout model](/azure/ai-services/document-intelligence/prebuilt/layout#supported-file-types). | [Multiple supported file types](/azure/ai-services/content-understanding/language-region-support), including PDF, DOCX, XLSX, and PPTX. |
| Billing for data extraction | Image extraction is billed according to [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/). | Billed according to [Document Layout pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/). | Billed according to [Azure Content Understanding pricing](https://azure.microsoft.com/pricing/details/content-understanding/). |
| Built-in chunking | No (use Text Split skill) | Yes (based on paragraph boundaries) | Yes (semantic chunking) |
| Recommended scenarios | Rapid prototyping or production pipelines where the exact position or detailed layout information isn't required. | RAG pipelines and agent workflows that need precise page numbers, on-page highlights, or diagram overlays in client apps. | Advanced document analysis requiring cross-page table extraction, semantic chunking, or consistent handling across document formats (PDF, DOCX, XLSX, PPTX). |

## Options for multimodal content embedding

In Azure AI Search, retrieving knowledge from images can follow two complementary paths: image verbalization or direct embeddings. Understanding the distinctions helps you align cost, latency, and answer quality with the needs of your application.

### Image verbalization followed by text embeddings

With this method, the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) invokes an LLM during ingestion to create a concise natural-language description of each extracted image, such as "Five-step HR access workflow that begins with manager approval." The description is stored as text and embedded alongside the surrounding document text, which you can then vectorize by calling the [Azure OpenAI](cognitive-search-skill-azure-openai-embedding.md), [Microsoft Foundry](cognitive-search-aml-skill.md), or [Azure Vision](cognitive-search-skill-vision-vectorize.md) embedding models.

Because the image is now expressed in language, Azure AI Search can:

+ Interpret the relationships and entities shown in a diagram.

+ Supply ready-made captions that an LLM can cite verbatim in a response.

+ Return relevant snippets for RAG applications or AI agent scenarios with grounded data.

The added semantic depth entails an LLM call for every image and a marginal increase in indexing time.

### Direct multimodal embeddings

A second option is to pass the document-extracted images and text to a multimodal embedding model that produces vector representations in the same vector space. Configuration is straightforward, and no LLM is required at indexing time. Direct embeddings are well suited to visual similarity and “find-me-something-that-looks-like-this” scenarios.

Because the representation is purely mathematical, it doesn't convey why two images are related, and it doesn't offer the LLM ready context for citations or detailed explanations.

### Combining both approaches

Many solutions need both encoding paths. Diagrams, flow charts, and other explanation-rich visuals are verbalized so that semantic information is available for RAG and AI agent grounding. Screenshots, product photos, or artwork are embedded directly for efficient similarity search. You can customize your Azure AI Search index and indexer skillset pipeline so it can store the two sets of vectors and retrieve them side by side.

## Options for querying multimodal content

If your multimodal pipeline is powered by the GenAI Prompt skill, you can run [hybrid queries](hybrid-search-overview.md) over both plain text and verbalized images in your search index. You can also use filters to narrow the search results to specific content types, such as only text or only images.

Although the GenAI Prompt skill supports text-to-vector queries via hybrid search, it doesn't support [image-to-vector queries](search-explorer.md#example-image-query). Only the multimodal embedding models provide the vectorizers that convert images into vectors at query time.

To use images as query inputs for your multimodal index, you must use the [AML skill](cognitive-search-aml-skill.md) or [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) with an equivalent vectorizer. For more information, see [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md).

## Tutorials and samples

To help you get started with multimodal search in Azure AI Search, here's a collection of content that demonstrates how to create and optimize multimodal indexes using Azure functionality.

| Content | Description |
|--|--|
| [Quickstart: Multimodal search in the Azure portal](search-get-started-portal-image-search.md) | Create and test a multimodal index in the Azure portal using the wizard and Search Explorer. |
| [Tutorial: Verbalize images using generative AI](tutorial-document-extraction-image-verbalization.md) | Extract text and images, verbalize diagrams, and embed the resulting descriptions and text into a searchable index. |
| [Tutorial: Vectorize images and text](tutorial-document-extraction-multimodal-embeddings.md) | Use a vision-text model to embed both text and images directly, enabling visual-similarity search over scanned PDFs. |
| [Tutorial: Verbalize images from a structured document layout](tutorial-document-layout-image-verbalization.md) | Apply layout-aware chunking and diagram verbalization, capture location metadata, and store cropped images for precise citations and page highlights. |
| [Tutorial: Vectorize from a structured document layout](tutorial-document-layout-multimodal-embeddings.md) | Combine layout-aware chunking with unified embeddings for hybrid semantic and keyword search that returns exact hit locations. |
| [Sample app: Multimodal RAG GitHub repository](https://aka.ms/azs-multimodal-sample-app-repo) | An end-to-end, code-ready RAG application with multimodal capabilities that surfaces both text snippets and image annotations. Ideal for jump-starting enterprise copilots. |
