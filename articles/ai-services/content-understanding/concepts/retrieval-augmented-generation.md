---
title: Azure AI Content Understanding Retrieval Augmented Generation Concept
titleSuffix: Azure AI services
description: Learn about Retrieval Augmented Generation
author: laujan
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 03/16/2025
ms.custom: 2025-understanding-release
---
# Creating a Multimodal Retrieval Augmented Generation Solution with Content Understanding

# Introduction
Retrieval Augmented Generation (RAG) enhances Generative AI models by grounding their responses in external knowledge sources, significantly improving accuracy, relevance, and reliability. A key challenge in RAG is effectively extracting and preparing multimodal content – documents, images, audio, and video – so that it can be accurately retrieved and used to inform the LLM's responses. 

Azure AI Content Understanding addresses these challenges by providing sophisticated extraction capabilities across all content modalities, preserving semantic integrity and contextual relationships that traditional extraction methods often lose. This unified approach eliminates the need to manage separate workflows and models for different content types, streamlining implementation while ensuring optimal representation for retrieval and generation.

## Multimodal Data Processing with Content Understanding

## Why Does Multimodal Data Matter for RAG?

In traditional content processing, simple text extraction was sufficient for many use cases. However, modern enterprise environments contain rich, diverse information spread across multiple formats—documents with complex layouts, images conveying visual insights, audio recordings of crucial conversations, and videos that combine all these elements. For truly comprehensive Retrieval Augmented Generation (RAG) systems, all of this content must be accurately processed and made available to generative AI models. This ensures that when users pose questions, the underlying RAG system can retrieve relevant information regardless of its original format—whether it's a complex table in a financial report, a technical diagram in a manual, insights from a recorded conference call, or explanations from a training video.

## Challenges with Multimodal Data Processing for RAG Systems

### 1. Data Ingestion Challenges

Multimodal content presents unique ingestion challenges that can hinder RAG performance. Documents with complex layouts, such as multi-column formats, merged table cells, and embedded visuals, often disrupt linear content flow and fragment context. Images require more than basic OCR, as implicit visual information like object relationships and scene context is frequently overlooked. Audio data faces issues with speaker diarization, overlapping speech, and multilingual complexities, making it difficult to maintain narrative coherence. Videos, with their dense informational content, pose challenges in preserving temporal relationships and balancing visual, spoken, and textual elements. Addressing these challenges is critical to ensure accurate and context-rich data ingestion for effective RAG systems.

### 2. Data Representation Challenges

Traditional RAG systems struggle to effectively represent multimodal content due to inherent limitations. Standard embedding approaches often fail to capture the full semantic richness of multimodal data, particularly when implicit relationships exist across different content types. This leads to **semantic fragmentation**, where critical contextual relationships, hierarchical structures, and cross-modal connections are lost during conversion into flat text or embeddings. Additionally, establishing meaningful **cross-modal alignment**—such as linking text descriptions to images or synchronizing spoken commentary with visual content—requires sophisticated techniques that many systems lack. These challenges hinder the ability to create cohesive and contextually accurate representations essential for effective retrieval and generation.

### 3. Query Optimization Challenges

Multimodal RAG systems face unique challenges in retrieving and ranking relevant content. **Modality bias** often skews retrieval toward text-based content, overlooking valuable visual or audio information. **Context fragmentation** makes it difficult to maintain coherence when combining information from multiple modalities during the generation phase. Additionally, **relevance ranking across modalities** requires sophisticated mechanisms to evaluate and prioritize content based on cross-modal relationships, ensuring the most contextually appropriate information is surfaced for user queries.

These challenges significantly impact retrieval precision and response quality in RAG systems, necessitating advanced extraction techniques that maintain contextual integrity across diverse content types while optimizing for effective retrieval and generation.
 
## Multimodal Data Processing for RAG with Content Understanding

Content Understanding's dual extraction approach offers strategic advantages for RAG implementation that addresses ingestion, representation and query optimization challenges:

1. **Content extraction** transforms unstructured information into coherent, context-aware representations that preserve hierarchical relationships and structural elements critical for accurate retrieval. The output of content extraction delivers unified outputs in Markdown and JSON—formats designed to integrate seamlessly with vector stores and generative AI models—while maintaining crucial contextual integrity across all modalities.

2. **Field extraction** enhances knowledge bases through customizable schema definitions, enabling organizations to generate targeted metadata that captures domain-specific contextual elements with precision. This capability transforms unstructured content into rich, structured information in JSON formats tailored to specific business contexts and search requirements.

These modality-specific approaches directly address the fundamental challenges of multimodal RAG, transforming each content type's unique characteristics into structured, contextually rich representations:

- **Document:** Content Understanding's sophisticated layout analysis preserves document structure by intelligently converting complex layouts into clean markdown with hierarchical headings, properly formatted tables, and explicit element relationships. This structural preservation is crucial for effective RAG implementation because it maintains semantic relationships between content sections, improving both indexing precision and retrieval accuracy. The resulting structured markdown output enhances RAG performance in three key ways: it enables more targeted retrieval of relevant document segments rather than entire documents, preserves critical context between related elements that might otherwise be fragmented, and provides consistent formatting that simplifies integration with vector stores and search engines. These advantages ultimately lead to more precise, contextually appropriate responses when the system is queried.

- **Image:** Content Understanding enhances image processing for RAG by generating descriptive text summaries and classifications that can be indexed alongside vector representations. This dual approach—combining vectors with rich textual descriptions—provides broader contextual understanding and enables more precise retrieval. Using advanced vision capabilities to extract both explicit content (text through OCR) and implicit meaning (object relationships, scene context), transforming previously unsearchable visual content into fully accessible semantic representations that enrich knowledge bases and yield more informative query responses.

- **Audio:** Content Understanding enhances audio processing for RAG through advanced speaker-aware transcription that maintains attribution across conversations while preserving temporal flow. The system identifies multiple speakers, detects language switches, and captures paralinguistic features, transforming audio into structured markdown that retains both spoken content and conversational context. This intelligent processing ensures that complex audio data like earnings calls or multi-person interviews maintains speaker identity and semantic coherence. Beyond basic transcription, users can define custom fields to extract additional metadata—such as topics, summaries, and sentiment analysis—which can be used alongside the transcription to significantly enrich knowledge bases and improve semantic search relevance, ultimately enabling more precise and contextually appropriate responses to queries.

- **Video:** Content Understanding addresses video's inherent complexity through intelligent scene segmentation and temporal synchronization of visual and audio elements. The service outputs both markdown and JSON formats, both optimized for generative AI models and structured to fit within typical context window limitations. This is achieved by segmenting detected shots into instances that prevent token limit issues during retrieval. Beyond basic content extraction, customers can generate additional metadata—such as topics, summaries and sentiment analysis—which can be used alongside vector representations to significantly enrich knowledge bases and improve semantic search relevance, ultimately enhancing RAG performance for video content.


## Building a Multimodal Data RAG using Content Understanding

A high level summary of RAG pattern looks like this:

1. Transform unstructured multimodal data into structured representation using Content Understanding.
2. Embed structured output using embedding models.
3. Store embedded vectors in database or search index.  
4. Use Generative AI to prompt and generate responses from retrieval system.

:::image type="content" source="../media/concepts/ragarchitecture2.png" alt-text="Screenshot of Content Understanding RAG architecture overview, process, and workflow with Azure AI Search and Azure Open AI.":::

### Scenario

Let's consider a scenario where we have a collection of documents, images, videos, and audio files related to a corporate training program. We want to create a system that can retrieve relevant information from these multimodal sources based on user queries. 

### Implementation

To implement this scenario, you can use Azure AI Content Understanding to automate content extraction, Azure AI Search for indexing and retrieval, and Azure OpenAI chat models for chat completion. Here's a high-level overview of the implementation steps:

### 1. Content Extraction: Transforming Multimodal Content

 In this scenario, the training content data can be processed with modality-specific approaches while maintaining contextual relationships:

- **Document Processing**: Extracts hierarchical structures, preserving the logical organization of training materials including headers, paragraphs, tables, page elements etc.

- **Image Processing**: Transforms visual information into searchable text by verbalizing diagrams and charts, extracting embedded text elements, and converting graphical data into structured formats. Technical illustrations are analyzed to identify components and their relationships.

- **Audio Processing**: Creates rich textual representations of spoken content with speaker diarization technology, topic segmentation, and automated summaries that capture the essence of discussions, presentations, and Q&A sessions.

- **Video Processing**: Segments video content into meaningful units through scene detection and key frame extraction, while generating descriptive summaries, transcribing spoken content, and identifying key topics and sentiment indicators throughout the footage.

This comprehensive extraction creates a rich knowledge base where each content type maintains its unique contextual elements while enabling cross-modal relationships.


## Sample Extraction Response

# [Document](#tab/document)

```json
{
  "id": "bcf8c7c7-03ab-4204-b22c-2b34203ef5db",
  "status": "Succeeded",
  "result": {
    "analyzerId": "training_document_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-13T07:15:46Z",
    "warnings": [],
    "contents": [
      {
        "markdown": "CONTOSO LTD.\n\n\n# Contoso Training Topics\n\nContoso Headquarters...",
        "fields": {
          "Business department": {
            "type": "string",
            "valueString": "Human resources",
            "spans": [ { "offset": 0, "length": 12 } ],
            "confidence": 0.941,
            "source": "D(1,0.5729,0.6582,2.3353,0.6582,2.3353,0.8957,0.5729,0.8957)"
          },
          "Items": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Topics": {
                    "type": "string",
                    "valueString": "Compliance and Safety",
                    "spans": [ { "offset": 909, "length": 19 } ],
                    "confidence": 0.971,
                    "source": "D(1,2.3264,5.673,3.6413,5.673,3.6413,5.8402,2.3264,5.8402)"
                  },
                  "Reading material": {
                    "type": "number",
                    "valueString": "Compliance in the workplace by John Smith",
                    "spans": [ { "offset": 995, "length": 6 } ],
                    "confidence": 0.989,
                    "source": "D(1,7.4507,5.6684,7.9245,5.6684,7.9245,5.8323,7.4507,5.8323)"
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "inch",
        "pages": [
          {
            "pageNumber": 1,
            "angle": -0.0039,
            "width": 8.5,
            "height": 11,
            "spans": [ { "offset": 0, "length": 1650 } ],
            "words": [
              {
                "content": "CONTOSO",
                "span": { "offset": 0, "length": 7 },
                "confidence": 0.997,
                "source": "D(1,0.5739,0.6582,1.7446,0.6595,1.7434,0.8952,0.5729,0.8915)"
              }, ...
            ],
            "lines": [
              {
                "content": "CONTOSO LTD.",
                "source": "D(1,0.5734,0.6563,2.335,0.6601,2.3345,0.8933,0.5729,0.8895)",
                "span": { "offset": 0, "length": 12 }
              }, ...
            ]
          }
        ],
        "paragraphs": [
          {
            "content": "CONTOSO LTD.",
            "source": "D(1,0.5734,0.6563,2.335,0.6601,2.3345,0.8933,0.5729,0.8895)",
            "span": { "offset": 0, "length": 12 }
          }, ...
        ],
        "sections": [
          {
            "span": { "offset": 0, "length": 1649 },
            "elements": [ "/sections/1", "/sections/2" ]
          },
          {
            "span": { "offset": 0, "length": 12 },
            "elements": [ "/paragraphs/0" ]
          }, ...
        ],
        "tables": [
          {
            "rowCount": 2,
            "columnCount": 6,
            "cells": [
              {
                "kind": "columnHeader",
                "rowIndex": 0,
                "columnIndex": 0,
                "rowSpan": 1,
                "columnSpan": 1,
                "content": "SALESPERSON",
                "source": "D(1,0.5389,4.5514,1.7505,4.5514,1.7505,4.8364,0.5389,4.8364)",
                "span": { "offset": 512, "length": 11 },
                "elements": [ "/paragraphs/19" ]
              }, ...
            ],
            "source": "D(1,0.4885,4.5543,8.0163,4.5539,8.015,5.1207,0.4879,5.1209)",
            "span": { "offset": 495, "length": 228 }
          }, ...
        ]
      }
    ]
  }
}
```

# [Image](#tab/image)

```json
{
  "id": "12fd421b-b545-4d63-93a5-01284081bbe1",
  "status": "Succeeded",
  "result": {
    "analyzerId": "training_image_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:41:00Z",
    "warnings": [],
    "contents": [
      {
        "markdown": "![image](image)\n",
        "fields": {
          "Title": {
            "type": "string",
            "valueString": "Weekly Work Hours Distribution"
          },
          "ChartType": {
            "type": "string",
            "valueString": "pie"
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "pixel",
        "pages": [
          {
            "pageNumber": 1,
            "width": 1283,
            "height": 617
          }
        ]
      }
    ]
  }
}
```

# [Audio](#tab/audio)

```json
{
  "id": "247c369c-1aa5-4f92-b033-a8e4318e1c02",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_audio_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:42:58Z",
    "warnings": [],
    "contents": [
      {
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 32182,
        "markdown": "```WEBVTT\n\n00:00.080 --> 00:00.640\n<v Agent>Good day...",
        "fields": {
          "Sentiment": {
            "type": "string",
            "valueString": "Positive"
          },
          "Summary": {
            "type": "string",
            "valueString": "Maria Smith contacted Contoso to inquire about her current point balance. Agent John Doe confirmed her identity and informed her that she has 599 points. Maria did not require any further information and the call ended on a positive note."
          },
          "People": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Name": {
                    "type": "string",
                    "valueString": "Maria Smith"
                  },
                  "Role": {
                    "type": "string",
                    "valueString": "Customer"
                  }
                }
              }, ...
            ]
          }
        },
        "transcriptPhrases": [
          {
            "speaker": "Agent 1",
            "startTimeMs": 80,
            "endTimeMs": 640,
            "text": "Good day.",
            "confidence": 0.932,
            "words": [
              {
                "startTimeMs": 80,
                "endTimeMs": 280,
                "text": "Good"
              }, ...
            ],
            "locale": "en-US"
          }, ...
        ]
      }
    ]
  }
}
```

# [Video](#tab/video)

```json
{
  "id": "204fb777-e961-4d6d-a6b1-6e02c773d72c",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_video_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:57:21Z",
    "warnings": [],
    "contents": [
      {
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 2800,
        "width": 540,
        "height": 960,
        "markdown": "# Shot 0:0.0 => 0:1.800\n\n## Transcript\n\n```\n\nWEBVTT\n\n0:0.80 --> 0:10.560\n<v Speaker>When I was planning my trip...",
        "fields": {
          "sentiment": {
            "type": "string",
            "valueString": "Neutral"
          },
          "description": {
            "type": "string",
            "valueString": "The video begins with a view from a glass floor, showing a person's feet in white sneakers standing on it. The scene captures a downward view of a structure, possibly a tower, with a grid pattern on the floor and a clear view of the ground below. The lighting is bright, suggesting a sunny day, and the colors are dominated by the orange of the structure and the gray of the floor."
          }
        }
      },
      ...
    ]
  }
}
```
---

### 2. Create a Unified Search Index

After processing multimodal content with Azure AI Content Understanding, the next step is to create a comprehensive search infrastructure that leverages this richly structured data. By embedding the markdown and JSON outputs using Azure OpenAI's embedding models and indexing them with [Azure AI Search](https://docs.azure.cn/en-us/search/tutorial-rag-build-solution-index-schema), you can create a unified knowledge repository that seamlessly spans all content modalities.

This approach transforms traditionally siloed content types into an integrated information ecosystem, enabling sophisticated cross-modal search capabilities that allow users to discover relevant information regardless of its original format. Whether users need information from documents, insights from images, key points from audio recordings, or explanations from video content, a unified search index delivers consistent, contextually relevant results.

The following sample demonstrates how to embed and index the unified output from Content Understanding:


```python
def embed_and_index_chunks(output):
    aoai_embeddings = AzureOpenAIEmbeddings(
        azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
        openai_api_version=AZURE_OPENAI_EMBEDDING_API_VERSION,  # e.g., "2023-12-01-preview"
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_ad_token_provider=token_provider
    )

    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
        azure_search_key=None,
        index_name=AZURE_SEARCH_INDEX_NAME,
        embedding_function=aoai_embeddings.embed_query
    )
    vector_store.add_documents(documents=output)
    return vector_store


# embed and index the output:
vector_store = embed_and_index_chunks(output)

```
---

Below is a minimal consolidated index that support vector and hybrid search and enables cross-modal search capabilities, allowing users to discover relevant information regardless of the original content format:

```json
{
"name": "unified_training_index",
"fields": [
    # Document content fields
    {"name": "document_content", "type": "Edm.String", "searchable": true, "retrievable": true},
    {"name": "document_headers", "type": "Edm.String", "searchable": true, "retrievable": true},
    
    # Image-derived content
    {"name": "visual_descriptions", "type": "Edm.String", "searchable": true, "retrievable": true}, 
    { "name": "chunked_content_vectorized", "type": "Edm.Single", "dimensions": 1536, "vectorSearchProfile": "my-vector-profile", "searchable": true, "retrievable": false, "stored": false },   

    # Video content components
    {"name": "video_transcript", "type": "Edm.String", "searchable": true, "retrievable": true},
    {"name": "scene_descriptions", "type": "Edm.String", "searchable": true, "retrievable": true},
    {"name": "video_topics", "type": "Edm.String", "searchable": true, "retrievable": true},
    { "name": "chunked_content_vectorized", "type": "Edm.Single", "dimensions": 1536, "vectorSearchProfile": "my-vector-profile", "searchable": true, "retrievable": false, "stored": false },
    
    # Audio processing results
    {"name": "audio_transcript", "type": "Edm.String", "searchable": true, "retrievable": true},
    {"name": "speaker_attribution", "type": "Edm.String", "searchable": true, "retrievable": true},
    {"name": "conversation_topics", "type": "Edm.String", "searchable": true, "retrievable": true}
],

  "vectorSearch": {
      "algorithms": [
          { "name": "my-algo-config", "kind": "hnsw", "hnswParameters": { }  }
      ],
      "profiles": [ 
        { "name": "my-vector-profile", "algorithm": "my-algo-config" }
      ]
  }
}
```
---
### 3. Optimize Retrieval with Advanced Search Techniques

The effectiveness of a RAG system depends significantly on its ability to retrieve the most relevant content for each query. Azure AI Search offers multiple sophisticated search strategies to maximize the value of your multimodal content:

**Hybrid search** combines the strengths of semantic understanding and keyword matching, enabling the system to retrieve information based on both conceptual similarity and explicit terminology. This approach is particularly valuable for multimodal content where concepts may be expressed differently across various content types.

**Vector search** leverages the dimensional relationships between embeddings to find content with similar meaning, even when terminology differs. This technique excels at uncovering subtle semantic connections across different modalities.

**Semantic ranking** enhances result relevance by prioritizing content based on deeper understanding rather than keyword frequency, helping surface the most contextually appropriate information regardless of its original format.

By carefully selecting and configuring these search techniques based on your specific use case requirements, you can ensure that your RAG system retrieves the most relevant content across all modalities, significantly enhancing the quality and accuracy of generated responses.

> [!NOTE]
> For comprehensive guidance on implementing different search techniques, visit the [Azure AI Search documentation](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview).

In this sample, we use hybrid search to combine full text and vector queries against the unified search index containing both searchable plain text content and generated embeddings.

``` python

# Perform a hybrid search using the search_type parameter
output = vector_store.hybrid_search(query=query, k=3)
for item in items:
    print(item.page_content)
```
---
> [!div class="nextstepaction"]
> [View full code sample for RAG on GitHub.](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples)

### 4. Utilize Azure OpenAI Models

Once your content is extracted and indexed, integrate [Azure OpenAI's embedding and chat models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions) to create an interactive question-answering system:

1. **Retrieve relevant content** from your unified index when a user submits a query
2. **Create an effective prompt** that combines the user's question with the retrieved context
3. **Generate responses** using Azure OpenAI models that reference specific content from various modalities

This approach grounds responses with your actual content, enabling the model to answer questions by referencing specific document sections, describing relevant images, quoting from video transcripts, or citing speaker statements from audio recordings.

The combination of Content Understanding's extraction capabilities, Azure AI Search's retrieval functions, and Azure OpenAI's generation abilities creates a powerful end-to-end RAG solution that can seamlessly work with all your content types.

## Get started
Content Understanding supports the following development options:
* [REST API](../quickstart/use-rest-api.md) Quickstart.
* [Azure Foundry](../quickstart//use-ai-foundry.md) Portal Quickstart. 

## Next steps
* Try our RAG [code samples.]((https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples))
* Follow our RAG How to guide
* Learn more about [document](../document/overview.md), [image](../image/overview.md), [audio](../audio/overview.md), [video](../video/overview.md) capabilities.
* Learn more about Content Understanding [**best practices**](../concepts/best-practices.md) and [**capabilities**](../concepts/capabilities.md).
* Review Content Understanding [**code samples**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main)
