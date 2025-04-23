---
title: Azure AI Content Understanding retrieval-augmented generation Concept
titleSuffix: Azure AI services
description: Learn about retrieval-augmented generation
author: laujan
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 04/23/2025
---

# Retrieval-augmented generation with Content Understanding

Retrieval-Augmented Generation (RAG) expands the potential of Large Language Models (LLMs) by grounding their responses in external knowledge sources, ensuring both accuracy and contextual relevance. One of the central challenges in RAG lies in efficiently extracting and preparing multimodal content—such as documents, images, audio, and video—so it can be accurately retrieved and utilized to enhance the LLM's responses. 

Azure AI Content Understanding addresses these challenges by providing sophisticated content extraction capabilities across all modalities. The service seamlessly integrates advanced natural language processing, computer vision, and speech recognition into a unified framework simplifying the challenges of managing separate extraction pipelines. This approach ensures high-quality data handling for documents, images, audio, and video, enhancing precision and depth in information retrieval. Such an approach is beneficial for `RAG` applications, where the quality and relevance of responses depend heavily on context and interrelationships.

:::image type="content" source="../media/concepts/rag-architecture-1.png" alt-text="screenshot of Azure Content Understanding service architecture.":::

## Multimodal data and RAG

In traditional content processing, simple text extraction sufficed for many content processing use cases. Today's enterprise environments house a vast array of complex and diverse information across multiple formats—documents with intricate layouts, images rich in visual insights, audio recordings of important discussions, and videos that seamlessly integrate these elements. For retrieval-augmented generation (RAG) systems to deliver truly comprehensive outputs, all such content must be accurately processed and made accessible to generative AI models. This method guarantees that users receive pertinent answers to their queries, no matter the original format of the information. The RAG system ensures seamless retrieval and relevance in various scenarios. It can handle a comprehensive table from a financial report. It also supports technical diagrams extracted from manuals. Additionally, it draws insights from recorded conference calls. Finally, the system effectively manages explanations delivered through training videos.



## Effective RAG using Content Understanding

Chunking is key to effective RAG with multimodal content. It breaks large content into smaller, manageable parts for better processing and retrieval. However, different types of data present unique challenges:

* **Documents**. Layout and meaning must be preserved to avoid losing context.
* **Images**. Visual elements need accurate interpretation while maintaining their relationships.
* **Audio**. Speaker identification and time order are important to keep the narrative clear.
* **Video**: Scene boundaries and synchronization between modes must stay intact.

Semantic chunking prioritizes meaning and relationships over arbitrary splits. Chunking ensures retrieved chunks are relevant to queries, allowing for more accurate and coherent responses. Azure AI Content Understanding is built for multimodal RAG, processing various content types (documents, images, audio, video) while preserving context and meaning. Chunking also improves query relevance and downstream operations, making it ideal for enterprise use cases requiring deep content analysis and understanding.

## Content Understanding RAG capabilities

Azure AI Content Understanding addresses the core challenges of multimodal RAG—complex data ingestion, data representation, and query optimization—by providing a solution that enhances the accuracy and relevance of retrieval and generation processes:

* **Simplified Multimodal Ingestion:** Content Understanding streamlines the processing of diverse content types—documents, images, audio, and video—into a unified workflow. Preserving structural integrity and contextual relationships eliminates the complexities of handling multimodal data, ensuring consistent representation across all modalities.

* **Enhanced Data Representation:** Content Understanding transforms unstructured data into structured, context-rich formats such as Markdown and JSON. This transformation ensures smooth integration with embedding models, vector databases, and generative AI systems. Maintaining semantic depth, hierarchical structure, and cross-modal linkages, addresses issues like semantic fragmentation and enables more accurate information retrieval.

* **Customizable Field Extraction:** Users can define custom fields to generate targeted metadata, such as summaries, visual descriptions, or sentiment analysis, enriching knowledge bases with domain-specific insights. These enhancements complement standard content extraction and vector representations, improving retrieval precision and enabling more contextually relevant responses.

* **Optimized Query Performance:** Content Understanding mitigates modality bias and context fragmentation by providing structured, enriched data that supports sophisticated relevance ranking across modalities. This mitigation ensures that the most appropriate information is surfaced for user queries, improving the coherence and accuracy of generated responses.

:::image type="content" source="../media/concepts/rag-architecture-2.png" alt-text="Screenshot of Content Understanding RAG architecture overview, process, and workflow with Azure AI Search and Azure OpenAI.":::

## RAG implementation

A high level summary of the `RAG` implementation pattern looks like this:

1. Transform unstructured multimodal data into structured representation using Content Understanding.
2. Embed structured output using embedding models.
3. Store embedded vectors in database or search index.  
4. Use Generative AI chat models to query and generate responses from retrieval systems.

Here's an overview of the implementation process. It begins with data extraction using Azure AI Content Understanding. This approach serves as the foundation for transforming raw multimodal data into structured, searchable formats. These formats are optimized for RAG workflows.

### 1. Content Extraction: The Foundation for RAG with Content Understanding

Content extraction is ideal for transforming raw multimodal data into structured, searchable formats:

* **Documents:** Captures hierarchical structures, such as headers, paragraphs, tables, and page elements, preserving the logical organization of training materials.
* **Images**: Transforms visual information into searchable text by verbalizing diagrams and charts, extracting embedded text elements, and converting graphical data into structured formats. Technical illustrations are analyzed to identify components and their relationships.
* **Audio:** Produces speaker-aware transcriptions that accurately capture spoken content while automatically detecting and processing multiple languages. 
* **Video:** The system segments video content into meaningful units using scene detection and key frame extraction. It generates descriptive summaries for the footage. The system also transcribes spoken content and identifies key topics. Lastly, it analyzes sentiment indicators throughout the video. Transcribes spoken content and provides scene descriptions while addressing context window limitations in generative AI models.

While content extraction provides a strong foundation for indexing and retrieval, it may not fully address domain-specific needs or provide deeper contextual insights.

### 2. Field Extraction: Enhancing Knowledge Bases for Better Retrieval

Field extraction complements content extraction by generating targeted metadata that enriches the knowledge base and improves retrieval precision:
* **Document:** Extract key topics/fields to provide concise overviews of lengthy materials.
* **Image:** Converts visual information into searchable text by verbalizing diagrams, extracting embedded text, and identifying graphical components.
* **Audio:** Extract key topics or sentiment analysis from conversations and to provide added context for queries.
* **Video:** Generate scene-level summaries, identify key topics, or analyze brand presence and product associations within video footage. 

Organizations can create a contextually rich knowledge base optimized for indexing, retrieval, and RAG scenarios by combining content extraction with field extraction. This method ensures more accurate and meaningful responses to user queries.

Learn more about [content extraction](./capabilities.md#content-extraction) and [field extraction](./capabilities.md#field-extraction) capabilities.

#### Code Sample: Analyzer and Schema Configuration

The following code sample shows an analyzer and schema creation for various modalities in a multimodal RAG scenario. 

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

The following code sample showcases the results of content and field extraction using Azure AI Content Understanding. These results demonstrate how multimodal data is transformed into structured, enriched formats, ready for indexing and retrieval in RAG workflows.

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

After data is extracted using Azure AI Content Understanding, the next steps involve integrating it with Azure AI Search and Azure OpenAI. This integration demonstrates the seamless synergy between data extraction, retrieval, and generative AI, creating a comprehensive and efficient solution for RAG scenarios.

> [!div class="nextstepaction"]
> [View full code sample for RAG on GitHub.](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples)

## 3. Create a Unified Search Index

Once multimodal content is processed through Azure AI Content Understanding, the next crucial step is to build a robust search framework that capitalizes on this enriched structured data. You can use Azure OpenAI's embedding models to embed markdown and JSON outputs. By indexing these embeddings with [Azure AI Search](https://docs.azure.cn/en-us/search/tutorial-rag-build-solution-index-schema), you can create an integrated knowledge repository. This repository effortlessly bridges various content modalities.

Azure AI Search provides advanced search strategies to maximize the value of multimodal content:

- **Hybrid Search:** Combines semantic understanding and keyword matching to retrieve information based on both conceptual similarity and explicit terminology, ideal for multimodal content with varied expressions.
- **Vector Search:** Uses embeddings to uncover subtle semantic connections across modalities, even when terminology differs.
- **Semantic Ranking:** Prioritizes results based on deeper contextual understanding rather than keyword frequency, surfacing the most relevant information regardless of format.

By carefully selecting and configuring these search techniques based on your specific use case requirements, you can ensure that your RAG system retrieves the most relevant content across all modalities, significantly enhancing the quality and accuracy of generated responses.

> [!NOTE]
> For comprehensive guidance on implementing different search techniques, visit the [Azure AI Search documentation](../../../search/hybrid-search-overview.md).

The following JSON code sample shows a minimal consolidated index that support vector and hybrid search and enables cross-modal search capabilities, allowing users to discover relevant information regardless of the original content format:

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

Once your content is extracted and indexed, integrate [Azure OpenAI's embedding and chat models](../../openai/concepts/models.md) to create an interactive question-answering system:

1. **Retrieve relevant content** from your unified index when a user submits a query
2. **Create an effective prompt** that combines the user's question with the retrieved context
3. **Generate responses** using Azure OpenAI models that reference specific content from various modalities

This approach grounds the response with your actual content, enabling the model to answer questions by referencing specific document sections, describing relevant images, quoting from video transcripts, or citing speaker statements from audio recordings.

The combination of Content Understanding's extraction capabilities, Azure AI Search's retrieval functions, and Azure OpenAI's generation abilities creates a powerful end-to-end RAG solution that can seamlessly work with all your content types.

## Get started
Content Understanding supports the following development options:
* [REST API](../quickstart/use-rest-api.md) Quickstart.
* [Azure Foundry](../quickstart//use-ai-foundry.md) Portal Quickstart. 

## Next steps
* Try our RAG [code samples.](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples)
* Follow our [RAG Tutorial](../tutorial/build-rag-solution.md)
* Learn more about [document](../document/overview.md), [image](../image/overview.md), [audio](../audio/overview.md), [video](../video/overview.md) capabilities.
* Learn more about Content Understanding [**best practices**](../concepts/best-practices.md) and [**capabilities**](../concepts/capabilities.md).
* Review Content Understanding [**code samples**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python?tab=readme-ov-file#azure-ai-search-with-content-understanding-samples-python)
