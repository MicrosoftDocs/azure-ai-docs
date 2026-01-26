---
title: Skills reference
titleSuffix: Azure AI Search
description: Data extraction, natural language, and image processing skills add semantics and structure to raw content in an Azure AI Search enrichment pipeline. Data chunking and vectorization skills support vector search scenarios.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: reference
ms.date: 11/04/2025
ms.update-cycle: 365-days
---

# Skills for extra processing during indexing (Azure AI Search)

This article describes the skills in Azure AI Search that you can include in a [skillset](cognitive-search-working-with-skillsets.md) to access external processing.

A *skill* is an atomic operation that transforms content in some way. Often, it's an operation that recognizes or extracts text, but it can also be a utility skill that reshapes existing enrichments. The output is usually text-based for use in [full-text search](search-lucene-query-architecture.md) or vectors for use in [vector search](vector-search-overview.md).

Skills are organized into the following categories:

* A *built-in skill* wraps API calls to another Azure resource, where the inputs, outputs, and processing steps are well understood. Some built-in skills require an attached resource solely for billing, while others use your Azure-hosted model or resource for both billing and processing.

* A *custom skill* provides custom code that executes externally to the search service. It's accessed through a URI. Custom code is often made available through an Azure function app. To attach an open-source or third-party vectorization model, use a custom skill.

* A *utility skill* is internal to Azure AI Search, with no dependency on external resources or outbound connections. Most utility skills are nonbillable.

## Built-in skills

There are two types of built-in skills:

+ Skills that connect to a [Microsoft Foundry resource](#foundry-resource) (for billing only)
+ Skills that connect to an [Azure-hosted model or resource](#azure-hosted-model-or-resource) (for billing and processing)

### Foundry resource

Skills in this category call subservices of Foundry Tools. For billing rather than processing, you must [attach a Foundry resource to your skillset](cognitive-search-attach-cognitive-services.md). Azure AI Search uses internal resources to execute these skills and only uses your Foundry resource for billing purposes.

A small quantity of processing is nonbillable, but at larger volumes, processing is billable. These skills are based on pretrained models from Foundry Tools, which means you can't train the models using your own data.

These skills are billed at the Standard rate.

| Skill  | Description | Metered by |
|-------|-------------|-------------|
| [Azure Vision multimodal embeddings](cognitive-search-skill-vision-vectorize.md) | Multimodal image and text vectorization. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Custom Entity Lookup](cognitive-search-skill-custom-entity-lookup.md) | Looks for text from a custom, user-defined list of words and phrases.| Azure AI Search ([pricing](https://azure.microsoft.com/pricing/details/search/)) |
| [Entity Linking](cognitive-search-skill-entity-linking-v3.md) | This skill uses a pretrained model to generate links for recognized entities to articles in Wikipedia. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Entity Recognition](cognitive-search-skill-entity-recognition-v3.md) | This skill uses a pretrained model to establish entities for a fixed set of categories: `"Person"`, `"Location"`, `"Organization"`, `"Quantity"`, `"DateTime"`, `"URL"`, `"Email"`, `"PersonType"`, `"Event"`, `"Product"`, `"Skill"`, `"Address"`, `"Phone Number"` and `"IP Address"` fields. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Image Analysis](cognitive-search-skill-image-analysis.md) | This skill uses an image detection algorithm to identify the content of an image and generate a text description. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Key Phrase Extraction](cognitive-search-skill-keyphrases.md) | This skill uses a pretrained model to detect important phrases based on term placement, linguistic rules, proximity to other terms, and how unusual the term is within the source data. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Language Detection](cognitive-search-skill-language-detection.md)  | This skill uses a pretrained model to detect which language is used (one language ID per document). When multiple languages are used within the same text segments, the output is the LCID of the predominantly used language. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [OCR](cognitive-search-skill-ocr.md) | Optical character recognition. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [PII Detection](cognitive-search-skill-pii-detection.md)  | This skill uses a pretrained model to extract personal information from a given text. The skill also gives various options for masking the detected personal information entities in the text.  | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Sentiment](cognitive-search-skill-sentiment-v3.md)  | This skill uses a pretrained model to assign sentiment labels (such as "negative", "neutral" and "positive") based on the highest confidence score found by the service at a sentence and document-level on a record by record basis. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |
| [Text Translation](cognitive-search-skill-text-translation.md) | This skill uses a pretrained model to translate the input text into various languages for normalization or localization use cases. | Foundry Tools ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)) |

### Azure-hosted model or resource

Skills in this category call Azure-hosted models or resources that you own for both billing and processing. Although Azure Content Understanding is part of Foundry Tools, the Azure Content Understanding skill connects to your deployed resource for processing, not just billing.

These skills are billed at the Standard rate.

| Skill  | Description | Metered by |
|-------|-------------|-------------|
| [Azure Content Understanding](cognitive-search-skill-content-understanding.md) | Connects to Azure Content Understanding for advanced document analysis and semantic chunking. | Azure Content Understanding ([pricing](https://azure.microsoft.com/pricing/details/content-understanding/)) |
| [Azure OpenAI Embedding](cognitive-search-skill-azure-openai-embedding.md) | Connects to a deployed Azure OpenAI embedding model for integrated vectorization. | Azure OpenAI ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing)) |
| [GenAI Prompt](cognitive-search-skill-genai-prompt.md) | Extends an AI enrichment pipeline with a Foundry chat completion model. | Azure OpenAI ([pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing)) |

## Custom skills

Skills in this category wrap external code that you design, develop, and deploy to the web. You can then call the module from within a skillset as a custom skill.

For guidance on creating a custom skill, see [Define a custom interface](cognitive-search-custom-skill-interface.md) and [Example: Creating a custom skill for AI enrichment](cognitive-search-create-custom-skill-example.md).

| Skill  | Description | Metered by |
|-------|-------------|-------------|
| [AML](cognitive-search-aml-skill.md) | Extends an AI enrichment pipeline with a Foundry or Azure Machine Learning model. | None, unless your solution uses a metered Azure service. |
| [Custom Entity Lookup](cognitive-search-skill-custom-entity-lookup.md) | Extends an AI enrichment pipeline by detecting user-defined entities. | None, unless your solution uses a metered Azure service. |
| [Web API](cognitive-search-custom-skill-web-api.md) | Extends an AI enrichment pipeline by making an HTTP call into a custom Web API. | None, unless your solution uses a metered Azure service. |

## Utility skills

Skills in this category execute only on Azure AI Search, iterate mostly on nodes in the enrichment cache, and are mostly nonbillable.

| Skill  | Description | Metered by |
|-------|-------------|-------------|
| [Conditional](cognitive-search-skill-conditional.md) | Allows filtering, assigning a default value, and merging data based on a condition. | Not applicable |
| [Document Extraction](cognitive-search-skill-document-extraction.md) | Extracts content from a file within the enrichment pipeline. | Azure AI Search ([pricing](https://azure.microsoft.com/pricing/details/search/)) for image extraction |
| [Shaper](cognitive-search-skill-shaper.md) | Maps output to a complex type (a multi-part data type, which might be used for a full name, a multi-line address, or a combination of last name and a personal identifier.) | Not applicable |
| [Text Merge](cognitive-search-skill-textmerger.md) | Consolidates text from a collection of fields into a single field.  | Not applicable |
| [Text Split](cognitive-search-skill-textsplit.md) | Splits text into pages so that you can enrich or augment content incrementally. | Not applicable |

## Related content

+ [Create a skillset](cognitive-search-defining-skillset.md)
+ [Add a custom skill to an AI enrichment pipeline](cognitive-search-custom-skill-interface.md)
+ [Tutorial: Enriched indexing with AI](tutorial-skillset.md)
