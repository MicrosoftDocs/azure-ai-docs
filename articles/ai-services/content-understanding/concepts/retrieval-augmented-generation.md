---
title: Azure AI Content Understanding Multimodal Retrieval Augmented Generation 
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
# Multimodal Retrieval Augmented Generation with Content Understanding

# Introduction

Retrieval Augmented Generation (RAG) enhances Generative AI models by grounding their responses in external knowledge sources, significantly improving accuracy, relevance, and reliability. A key challenge in RAG is effectively extracting and preparing multimodal content – documents, images, audio, and video – so that it can be accurately retrieved and used to inform the LLM's responses. 

Azure AI Content Understanding addresses these challenges by providing sophisticated extraction capabilities across all content modalities, preserving semantic integrity and contextual relationships that traditional extraction methods often lose. This unified approach eliminates the need to manage separate workflows and models for different content types, streamlining implementation while ensuring optimal representation for retrieval and generation.

## Why Does Multimodal Data Matter for RAG?

In traditional content processing, simple text extraction was sufficient for many use cases. However, modern enterprise environments contain rich, diverse information spread across multiple formats—documents with complex layouts, images conveying visual insights, audio recordings of crucial conversations, and videos that combine all these elements. For truly comprehensive Retrieval Augmented Generation (RAG) systems, all of this content must be accurately processed and made available to generative AI models. This ensures that when users pose questions, the underlying RAG system can retrieve relevant information regardless of its original format—whether it's a complex table in a financial report, a technical diagram in a manual, insights from a recorded conference call, or explanations from a training video.

## Capabilities of Content Understanding for Multimodal RAG

Azure AI Content Understanding addresses the core challenges of multimodal RAG— complex data ingestion, data representation, and query optimization—by providing a solution that enhances the accuracy and relevance of retrieval and generation processes:

- **Simplified Multimodal Ingestion:** Content Understanding streamlines the processing of diverse content types—documents, images, audio, and video—into a unified workflow. By preserving structural integrity and contextual relationships, it eliminates the complexities of handling multimodal data, ensuring consistent representation across all modalities.

- **Enhanced Data Representation:** By transforming unstructured content into coherent, context-aware outputs in Markdown and JSON formats, Content Understanding ensures seamless integration with embedding models, vector stores, and generative AI systems. This approach preserves semantic richness, hierarchical structures, and cross-modal relationships, addressing issues like semantic fragmentation and enabling more accurate retrieval.

- **Customizable Field Extraction:** Users can define custom fields to generate targeted metadata, such as summaries, visual descriptions, or sentiment analysis, enriching knowledge bases with domain-specific insights. These enhancements complement standard content extraction and vector representations, improving retrieval precision and enabling more contextually relevant responses.

- **Optimized Query Performance:** Content Understanding mitigates modality bias and context fragmentation by providing structured, enriched data that supports sophisticated relevance ranking across modalities. This ensures that the most appropriate information is surfaced for user queries, improving the coherence and accuracy of generated responses.

## Building a Multimodal RAG Solution using Content Understanding

:::image type="content" source="../media/concepts/rag-architecture-2.png" alt-text="Screenshot of Content Understanding RAG architecture overview, process, and workflow with Azure AI Search and Azure Open AI.":::

## RAG Scenario: Corporate Training Knowledge Base

Imagine a corporate training program with a collection of documents, images, audio recordings, and videos covering topics such as compliance, safety, and technical skills. The goal is to create a system that retrieves relevant information from these multimodal sources based on user queries, enabling employees to access precise and contextually rich answers.

## Implementation
A high level summary of RAG implementation pattern looks like this:

1. Transform unstructured multimodal data into structured representation using Content Understanding.
2. Embed structured output using embedding models.
3. Store embedded vectors in database or search index.  
4. Use Generative AI chat models to query and generate responses from retrieval systems.

Here’s an overview of the implementation process, beginning with data extraction using Azure AI Content Understanding as the foundation for transforming raw multimodal data into structured, searchable formats optimized for RAG workflows:

### 1. Content Extraction: The Foundation for RAG with Content Understanding

Content extraction forms the foundation of effective RAG systems by transforming raw multimodal data into structured, searchable formats optimized for retrieval. The implementation varies by content type:
- **Document:** Extracts hierarchical structures, such as headers, paragraphs, tables, and page elements, preserving the logical organization of training materials.
- **Audio:** Generates speaker-aware transcriptions that accurately capture spoken content while automatically detecting and processing multiple languages. 
- **Video:** Segments video into meaningful units, transcribes spoken content, and provides scene descriptions while addressing context window limitations in generative AI models.

While content extraction provides a strong foundation for indexing and retrieval, it may not fully address domain-specific needs or provide deeper contextual insights. Learn more about [content extraction](./capabilities.md#content-extraction) capabilities.

### 2. Field Extraction: Enhancing Knowledge Bases for Better Retrieval

Field extraction complements content extraction by generating targeted metadata that enriches the knowledge base and improves retrieval precision. The implementation varies by content type:
- **Document:** Extract key topics/fields to provide concise overviews of lengthy materials.
- **Image:** Converts visual information into searchable text by verbalizing diagrams, extracting embedded text, and identifying graphical components.
- **Audio:** Extract key topics or sentiment analysis from conversations and to provide additional context for queries.
- **Video:** Generate scene-level summaries, identify key topics, or analyze brand presence and product associations within video footage. 

By combining content extraction with field extraction, organizations can create a contextually rich knowledge base optimized for indexing, retrieval, and RAG scenarios, ensuring more accurate and meaningful responses to user queries. 

Learn more about [field extraction](./capabilities.md#field-extraction) capabilities.

#### Code Sample: Analyzer and Schema Configuration 
Below is an example of a analyzer and schema creation for various modalities in a multimodal RAG scenario. 

---

# [Document](#tab/document)
```json
{
  "description": "Training document analyzer",
  "scenario": "document",
  "config": {
    "returnDetails": true
  },
  "fieldSchema": {
    "fields": {
      "ChapterTitle": {
        "type": "string",
        "method": "extract",
        "description": "Training chapter title"
      },
      "ChapterAuthor": {
        "type": "string",
        "method": "extract",
        "description": "Training chapter author"
      },
      "ChapterPublishDate": {
        "type": "Date",
        "method": "extract",
        "description": "Training chapter publication date"
      }
    }
  }
}
```

# [Image](#tab/image)
```json
{
  "description": "Training images analyzer",
  "scenario": "image",
  "fieldSchema": {
    "fields": {
      "TrainingChartTitle": {
        "type": "string",
        "method": "extract",
        "description": "Training chart title or caption"
      },
      "TrainingChartType": {
        "type": "string",
        "method": "classify",
        "enum": [ "bar", "line", "pie" ]
      },
      "TrainingChartDescription": {
        "type": "string",
        "method": "extract",
        "description": "Training chart description"
      }
    }
  }
}
```

# [Audio](#tab/audio)
```json
{
  "description": "Training audio analyzer",
  "scenario": "audio",
  "config": {
    "returnDetails": true,
    "locales": ["en-US"]
  },
  "fieldSchema": {
    "fields": {
      "TrainingSummary": {
        "type": "string",
        "method": "generate",
        "description": "detailed summary of discussion in this segment "
      },
      "TrainingTopics": {
        "type": "array",
        "method": "generate",
        "description": "2-3 topics of discussion in this segment "
      },
      "People": {
        "type": "array",
        "description": "List of people mentioned",
        "items": {
          "type": "object",
          "properties": {
            "Name": { "type": "string" },
            "Role": { "type": "string" }
          }
        }
      }
    }
  }
}
```

# [Video](#tab/video)
```json
{
  "description": "Training video analyzer",
  "scenario": "video",
  "fieldSchema": {
    "fields": {
      "Description": {
        "type": "string",
        "method": "generate",
        "description": "Detailed summary of the video segment, focusing on product characteristics, and quality inspection requirements"
      },
      "KeyTopics": {
        "type": "array",
        "method": "generate",
        "description": "The key points or topics covered in this segment"
      }
    }
  }
}
```


---

#### Code Sample: Extraction Response
Below is an example showcasing the results of content and field extraction using Azure AI Content Understanding. These results demonstrate how multimodal data is transformed into structured, enriched formats, ready for indexing and retrieval in RAG workflows.

---

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
          "ChapterTitle": {
            "type": "string",
            "valueString": "Risks and Compliance regulations",
            "spans": [ { "offset": 0, "length": 12 } ],
            "confidence": 0.941,
            "source": "D(1,0.5729,0.6582,2.3353,0.6582,2.3353,0.8957,0.5729,0.8957)"
          },
          "ChapterAuthor": {
            "type": "string",
            "valueString": "John Smith",
            "spans": [ { "offset": 0, "length": 12 } ],
            "confidence": 0.941,
            "source": "D(1,0.5729,0.6582,2.3353,0.6582,2.3353,0.8957,0.5729,0.8957)"
          },
          "ChapterPublishDate": {
            "type": "Date",
            "valueString": "04-11-2017",
            "spans": [ { "offset": 0, "length": 12 } ],
            "confidence": 0.941,
            "source": "D(1,0.5729,0.6582,2.3353,0.6582,2.3353,0.8957,0.5729,0.8957)"
          },
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
               ....
              }, 
            ],
            "lines": [
              {
                ...
              }, 
            ]
          }
        ],

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
          "TrainingChartTitle": {
            "type": "string",
            "valueString": "Weekly Work Hours Distribution"
          },
          "TrainingChartType": {
            "type": "string",
            "valueString": "pie"
          },
          "TrainingChartDescription"{
            "type": "string",
            "valueString": "This chart shows the monthly sales data for the year 2025."
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
    "analyzerId": "training_audio_analyzer",
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
          "TrainingSummary": {
            "type": "string",
            "valueString": "Maria Smith contacted Contoso to inquire about her current point balance. Agent John Doe confirmed her identity and informed her that she has 599 points. Maria did not require any further information and the call ended on a positive note."
          },
          "TrainingTopics": {
						"type": "array",
						"valueArray": [
							{
								"type": "string",
								"valueString": "Compliance"
							},
							{
								"type": "string",
								"valueString": "Risk mitigation"
							},]
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
          
          "description": {
            "type": "string",
            "valueString": "The video begins with a view from a glass floor, showing a person's feet in white sneakers standing on it. The scene captures a downward view of a structure, possibly a tower, with a grid pattern on the floor and a clear view of the ground below. The lighting is bright, suggesting a sunny day, and the colors are dominated by the orange of the structure and the gray of the floor."
          },
          "KeyTopics": {
						"type": "array",
						"valueArray": [
							{
								"type": "string",
								"valueString": "Flight delay"
							},
							{
								"type": "string",
								"valueString": "Customer service"
							},
            ]
          }
        },
      ...
    ]
  }
}
```

---

After extracting data with Azure AI Content Understanding, the next steps focus on integration with Azure AI Search and Azure OpenAI. This integration demonstrates the seamless synergy between data extraction, retrieval, and generative AI, creating a comprehensive and efficient solution for RAG scenarios.

> [!div class="nextstepaction"]
> [View full code sample for Multimodal RAG on GitHub.](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_multimodal_RAG.ipynb)

## 3. Create a Unified Search Index
After processing multimodal content with Azure AI Content Understanding, create a comprehensive search infrastructure using your newly structured data. By embedding the markdown and JSON outputs with Azure OpenAI's embedding models and indexing them in Azure AI Search, you'll establish a unified knowledge repository spanning all content types.

Azure AI Search offers advanced search strategies for multimodal content. In this implementation, [hybrid search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview) combines vector and full-text indexing to blend keyword precision with semantic understanding—ideal for complex queries requiring both exact matching and contextual relevance. This approach significantly enhances the quality of information fed to generation models, producing more accurate, contextually appropriate responses

Below is a sample consolidated index that support vector and hybrid search and enables cross-modal search capabilities, allowing users to discover relevant information regardless of the original content format:

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

## 4. Utilize Azure OpenAI Models

Once your content is extracted and indexed, integrate [Azure OpenAI's embedding and chat models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions) to create an interactive question-answering system.

Content Understanding enables effective grounded responses with your actual content, enabling the model to answer questions by referencing specific document sections, describing relevant images, quoting from video transcripts, or citing speaker statements from audio recordings.

The combination of Content Understanding's extraction capabilities, Azure AI Search's retrieval functions, and Azure OpenAI's generation abilities creates a powerful end-to-end RAG solution that can seamlessly work with all your content types.

## Get started
Content Understanding supports the following development options:
* [REST API](../quickstart/use-rest-api.md) Quickstart.
* [Azure Foundry](../quickstart//use-ai-foundry.md) Portal Quickstart. 

## Next steps
* Try our RAG [code samples.]((https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples))
* Follow our [RAG Tutorial](../tutorial/RAG-tutorial.md)
* Learn more about [document](../document/overview.md), [image](../image/overview.md), [audio](../audio/overview.md), [video](../video/overview.md) capabilities.
* Learn more about Content Understanding [**best practices**](../concepts/best-practices.md) and [**capabilities**](../concepts/capabilities.md).
* Review Content Understanding [**code samples**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main)
