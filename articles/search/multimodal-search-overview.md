---
title: Multimodal search concepts and guidance in Azure AI Search
titleSuffix: Azure AI Search
description: Learn what multimodal search is, how Azure AI Search supports it for text + image content, and where to find detailed concepts, tutorials, and samples.
ms.service: azure-ai-search
ms.topic: conceptual
ms.date: 05/11/2025
author: gmndrg
ms.author: gimondra
---

# Multimodal search in Azure AI Search

Multimodal search is the ability to ingest, understand, and retrieve documents that contain text and images, enabling you to perform searches that combine various modalities, such as querying with text to find information embedded in relevant complex images. In practice, this means an application using multimodal search can answer a question such as “What is the process to have an HR form approved?” even when the only authoritative description of the workflow lives inside an embedded diagram of a PDF file.  

Diagrams, scanned forms, screenshots, and infographics often contain the decisive details that make or break an answer.  Multimodal search helps closing that gap by bringing visual content into the same retrieval pipeline, so your AI agent doesn't overlook a critical image, and your users can trace every provided answer back to its original source.

Building a robust multimodal pipeline typically requires multiple moving parts: extracting inline images and page text, describing an image in natural language, embedding both modalities into a common vector space, storing extracted images for later display, preserving the order of the information as displayed in the document and finally executing hybrid queries that combine keyword and vector search with semantic ranking.

Azure AI Search simplifies the construction of a multimodal pipeline through a guided experience in the Azure portal:

1. [Azure portal multimodal functionality](search-get-started-portal-image-search.md): The step-by-step multimodal functionality under "Import and vectorize data" wizard accepts document inputs, applies data extraction and enrichment settings, and produces a fully operational index that contains page text, inline embedded images references, and vector embeddings.  
2. [Reference GitHub multimodal RAG sample application](https://aka.ms/azs-multimodal-sample-app-repo):A companion repository on GitHub with end-to-end sample code that demonstrates how a [Retrieval Augmented Generation (RAG)](retrieval-augmented-generation-overview.md) application consumes the multimodal index and renders both textual citations and associated image snippets in the response. This wizard also provides an end-to-end code-ready app deployment in case you'd like to a code-only approach for data ingestion and processing as well.

## Functionality enabling multimodality

The functionality behind the "Import and vectorize data" wizard's multimodality option is powered by managed, configurable AI skills and the Azure Search knowledge store:

+ [Document Intelligence layout skill](cognitive-search-skill-document-intelligence-layout.md) and [Document extraction skill](cognitive-search-skill-document-extraction.md) obtain page text, inline images, and structural metadata.  The Document Extraction skill doesn't support polygon extraction or page number extraction. Also, the range of supported file types may vary. To ensure optimal alignment with your specific use case, check each skill documentation for detailed information on compatibility and capabilities.
+ [Split skill](cognitive-search-skill-textsplit.md) chunks the extracted text for utilization in the remaining pipeline functionality (such as embedding skills). 
+ [Gen AI prompt skill](cognitive-search-skill-genai-prompt.md) verbalizes images, producing concise natural-language descriptions suitable for text search and embedding using a Large Language Model (LLM). 
+ Text/image (or multimodal) embedding skills create embeddings for text and images, enabling similarity and hybrid retrieval. You can call [Azure OpenAI](cognitive-search-skill-azure-openai-embedding.md), [AI Foundry](cognitive-search-aml-skill.md) or [AI Vision](cognitive-search-skill-vision-vectorize.md) embedding models natively.
+ [Knowledge store](knowledge-store-concept-intro.md) stores extracted images that can be returned directly to client applications. When you use the 'Import and vectorize data' wizard with the multimodality option, an image's location is stored directly within the index, enabling convenient retrieval at a query time.


## Selecting an ingestion skill

A multimodal pipeline begins by cracking each source document into chunks of text, inline images, and associated metadata. Azure AI Search provides two built-in skills for this step. Both enable textual and image extraction, but they differ in the layout detail and metadata they return, and in how their billing works.

| Characteristic | Document Intelligence layout skill | Document extraction skill |
|----------------|------------------------------------|---------------------------|
| Location metadata extraction (page, bounding polygon) | Yes | No |
| Data-extraction billing | Billed according to [Document Intelligence layout-model pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/). | Image extraction is billed as outlined in the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/). |
| Recommended scenarios | RAG pipelines and agent workflows that need precise page numbers, on-page highlights, or diagram overlays in client apps. | Rapid prototyping or production pipelines where the exact position or detailed layout information is not required. |

You can also call directly [Content Understanding](/azure/ai-services/content-understanding/concepts/retrieval-augmented-generation) for multimodality content extraction purposes using a [custom skill](cognitive-search-custom-skill-web-api.md) since it isn't supported natively yet in Azure AI Search. 

## Choosing an embedding strategy: image verbalization or direct embeddings
Retrieving knowledge from images can follow two complementary paths in Azure AI Search. Understanding the distinctions helps you align cost, latency, and answer quality with the needs of your application.

### Image verbalization followed by text embeddings
With this method, the Gen AI prompt skill invokes an LLM during ingestion to create a concise natural-language description of each extracted image—for example “Five-step HR access workflow that begins with manager approval.” The description is stored as text and embedded alongside the surrounding document text. Because the image is now expressed in language, Azure AI Search can:

- Interpret the relationships and entities shown in a diagram.
- Supply ready-made captions that an LLM can cite verbatim in a response.
- Return relevant snippets for RAG applications/AI agent scenarios with grounded data.

The added semantic depth entails an LLM call for every image and a marginal increase in indexing time.

### Direct vision–text embeddings
A second option is to pass the document extracted images and text to a multimodal embedding model that produces vector representations in the same vector space. Configuration is straightforward and no LLM is required at indexing time. Direct embeddings are well suited to visual similarity and “find-me-something-that-looks-like-this” scenarios.

Because the representation is purely mathematical, it does not convey why two images are related, and it offers the LLM no ready context for citations or detailed explanations.

### Combining both approaches
Many solutions need both encoding paths. Diagrams, flow charts, and other explanation-rich visuals are verbalized so that semantic information is available for RAG and AI agent grounding. Screenshots, product photos, or artwork are embedded directly for efficient similarity search. You can customize your Azure AI Search index and indexer skillset pipeline so it can store the two sets of vectors and retrieve them side by side.


### Tutorials and samples

To help you get started with multimodal search in Azure AI Search, here's a collection of tutorials and samples that demonstrate how to create and optimize multimodal indexes using Azure functionalities and capabilities. 

| Tutorial / sample                                                                                                                  | Description                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Quickstart: Multimodal search in the Azure portal](search-get-started-portal-image-search.md)                                     | Create and test a multimodal index in the Azure portal using the wizard and Search Explorer.                                                          |
| [Tutorial: Image verbalization + document extraction](tutorial-multimodal-indexing-with-image-verbalization-and-doc-extraction.md) | Extract text and images, verbalize diagrams, and embed the resulting descriptions and text into a searchable index.                                   |
| [Tutorial: Multimodal embeddings + document extraction](tutorial-multimodal-indexing-with-embedding-and-doc-extraction.md)         | Use a vision-text model to embed both text and images directly, enabling visual-similarity search over scanned PDFs.                                  |
| [Tutorial: Image verbalization + layout skill](tutorial-multimodal-index-image-verbalization-skill.md)                             | Apply layout-aware chunking and diagram verbalization, capture location metadata, and store cropped images for precise citations and page highlights. |
| [Tutorial: Multimodal embeddings + layout skill](tutorial-multimodal-index-embeddings-skill.md)                                    | Combine layout-aware chunking with unified embeddings for hybrid semantic + keyword search that returns exact hit locations.                          |
| [Sample app: Multimodal RAG GitHub repository](https://aka.ms/azs-multimodal-sample-app-repo)                                             | An end-to-end RAG application code with multimodal capabilities that surfaces both text snippets and image annotations—ideal for jump-starting enterprise copilots.             |





