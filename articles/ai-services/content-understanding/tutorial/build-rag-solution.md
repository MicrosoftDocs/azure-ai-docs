---
title: Build a retrieval-augmented generation solution with Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn to build a retrieval-augmented generation solution with Content Understanding
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build a retrieval-augmented generation solution 

This tutorial explains how to create a retrieval-augmented generation (RAG) solution using Azure Content Understanding in Foundry Tools. It covers the key steps to build a strong RAG system, offers tips to improve relevance and accuracy, and shows how to connect with other Azure services. By the end, you can use Content Understanding to handle multimodal data, improve retrieval, and help AI models provide accurate and meaningful responses.

## Exercises included in this tutorial

* **[Create analyzers](#create-analyzers)**. Learn how to create reusable analyzers to extract structured content from multimodal data using content extraction.
* **[Generate targeted metadata with field extraction](#content-and-field-extraction)**. Discover how to use AI to generate further metadata, such as summaries or key topics, to enrich extracted content.
* **[Preprocess extracted content](#preprocessing-output-from-content-understanding)**. Explore ways to transform extracted content into vector embeddings for semantic search and retrieval.
* **[Design a unified index](#embed-and-index-extracted-content)**. Develop a unified Azure AI Search index that integrates and organizes multimodal data for efficient retrieval.
* **[Semantic chunk retrieval](#semantic-chunk-retrieval)**. Extract contextually relevant information to deliver more precise and meaningful answers to user queries.
* **[Interact with data using chat models](#use-openai-to-interact-with-data)** Use Azure OpenAI chat models to engage with your indexed data, enabling conversational search, querying, and answering.

## Prerequisites

To get started, you need **An active Azure subscription**. If you don't have an Azure account, you can [create a free subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* Once you have your Azure subscription, create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.

   * This resource is listed under **Foundry** > **Foundry** in the portal.

     :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

* **Azure AI Search Resource:** Set up an [Azure AI Search resource](../../../search/search-create-service-portal.md) to enable indexing and retrieval of multimodal data.
* **Azure OpenAI Chat Model Deployment:** Deploy an [Azure OpenAI chat model](../../../ai-foundry/foundry-models/concepts/deployment-types.md) that enables conversational interactions.
* **Embedding Model Deployment:** Ensure you have an embedding model deployed to generate vector representations for semantic search.
* **API Version:** This tutorial uses the latest preview [API version](/rest/api/contentunderstanding/operation-groups?preserve-view=true).
* **Python Environment:** Install [Python 3.11](https://www.python.org/downloads/) to execute the provided code samples and scripts.
* This tutorial follows this sample code can be found in our [Python notebook](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples). Follow the [README](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/README.md) to create essential resources, grant resources the right Access control(IAM) roles and install all packages needed for this tutorial.
* The multimodal data used in this tutorial consists of documents, images, audio, and video. They're designed to guide you through the process of building a robust RAG solution with Azure Content Understanding in Foundry Tools.

## Extract data

Retrieval-augmented generation (*RAG**) is a method that enhances the functionality of Large Language Models (**LLM**) by integrating data from external knowledge sources. Building a robust multimodal RAG solution begins with extracting and structuring data from diverse content types. Azure Content Understanding provides three key components to facilitate this process: **content extraction**, **field extraction**, and **analyzers**. Together, these components form the foundation for creating a unified, reusable, and enhanced data pipeline for RAG workflows.

## Implementation steps

To implement data extraction in Content Understanding, follow these steps:

1. **Create an Analyzer:** Define an analyzer using REST APIs or our Python code samples.

1. **Perform Content Extraction:** Use the analyzer to process files and extract structured content.

1. **(Optional) Enhance with Field Extraction:** Optionally, specify AI-generated fields to enrich the extracted content with added metadata.

## Create analyzers

Analyzers are reusable components in Content Understanding that streamline the data extraction process. Once an analyzer is created, it can be used repeatedly to process files and extract content or fields based on predefined schemas. An analyzer acts as a blueprint for how data should be processed, ensuring consistency and efficiency across multiple files and content types.

The following code samples demonstrate how to create analyzers for each modality, specifying the structured data to be extracted, such as key fields, summaries, or classifications. These analyzers serve as the foundation for extracting and enriching content in your RAG solution.

#### Load all environment variables and necessary libraries from Langchain

``` python

import os
from dotenv import load_dotenv
load_dotenv()

# Load and validate Foundry Tools configs
AZURE_AI_SERVICE_ENDPOINT = os.getenv("AZURE_AI_SERVICE_ENDPOINT")
AZURE_AI_SERVICE_API_VERSION = os.getenv("AZURE_AI_SERVICE_API_VERSION") or "2024-12-01-preview"
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION") or "2024-11-30"

# Load and validate Azure OpenAI configs
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_CHAT_API_VERSION = os.getenv("AZURE_OPENAI_CHAT_API_VERSION") or "2024-08-01-preview"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDING_API_VERSION = os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION") or "2023-05-15"

# Load and validate Azure Search Services configs
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME") or "sample-doc-index"

# Import libraries from Langchain
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores.azuresearch import AzureSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
import requests
import json
import sys
import uuid
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Add the parent directory to the path to use shared modules
parent_dir = Path(Path.cwd()).parent
sys.path.append(str(parent_dir))

```
---

#### Code sample: Create analyzer

``` python
from pathlib import Path
from python.content_understanding_client import AzureContentUnderstandingClient
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

#set analyzer configs
analyzer_configs = [
    {
        "id": "doc-analyzer" + str(uuid.uuid4()),
        "template_path": "../analyzer_templates/content_document.json",
        "location": Path("../data/sample_layout.pdf"),
    },
    {
        "id": "image-analyzer" + str(uuid.uuid4()),
        "template_path": "../analyzer_templates/image_chart_diagram_understanding.json",
        "location": Path("../data/sample_report.pdf"),
    },
    {
        "id": "audio-analyzer" + str(uuid.uuid4()),
        "template_path": "../analyzer_templates/call_recording_analytics.json",
        "location": Path("../data/callCenterRecording.mp3"),
    },
    {
        "id": "video-analyzer" + str(uuid.uuid4()),
        "template_path": "../analyzer_templates/video_content_understanding.json",
        "location": Path("../data/FlightSimulator.mp4"),
    },
]

# Create Content Understanding client
content_understanding_client = AzureContentUnderstandingClient(
    endpoint=AZURE_AI_SERVICE_ENDPOINT,
    api_version=AZURE_AI_SERVICE_API_VERSION,
    token_provider=token_provider,
    x_ms_useragent="azure-ai-content-understanding-python/content_extraction", # This header is used for sample usage telemetry, please comment out this line if you want to opt out.
)

# Iterate through each config and create an analyzer
for analyzer in analyzer_configs:
    analyzer_id = analyzer["id"]
    template_path = analyzer["template_path"]

    try:

        # Create the analyzer using the content understanding client
        response = content_understanding_client.begin_create_analyzer(
            analyzer_id=analyzer_id,
            analyzer_template_path=template_path
        )
        result = content_understanding_client.poll_result(response)
        print(f"Successfully created analyzer: {analyzer_id}")

    except Exception as e:
        print(f"Failed to create analyzer: {analyzer_id}")
        print(f"Error: {e}")

```
---

**Note:** Field extraction schemas are optional and not required for performing content extraction. To execute content extraction and create analyzers without defining field schemas, just provide the analyzer ID and the file to be analyzed.

Schemas were used in this tutorial. Here's an example of a schema definition

# [Document](#tab/document)

In the following example, we define a schema for extracting basic information from an invoice document.

```json
{
  "description": "Sample invoice analyzer",
  "scenario": "document",
  "config": {
    "returnDetails": true
  },
  "fieldSchema": {
    "fields": {
      "VendorName": {
        "type": "string",
        "method": "extract",
        "description": "Vendor issuing the invoice"
      },
      "Items": {
        "type": "array",
        "method": "extract",
        "items": {
          "type": "object",
          "properties": {
            "Description": {
              "type": "string",
              "method": "extract",
              "description": "Description of the item"
            },
            "Amount": {
              "type": "number",
              "method": "extract",
              "description": "Amount of the item"
            }
          }
        }
      }
    }
  }
}
```

# [Image](#tab/image)

In the following example, we define a schema for identifying chart types in an image.


```json
{
  "description": "Sample chart analyzer",
  "scenario": "image",
  "fieldSchema": {
    "fields": {
      "Title": {
        "type": "string"
      },
      "ChartType": {
        "type": "string",
        "method": "classify",
        "enum": [ "bar", "line", "pie" ]
      }
    }
  }
}
```

# [Audio](#tab/audio)

In the following example, we define a schema for extracting basic information from call transcripts.

```json
{
  "description": "Sample call transcript analyzer",
  "scenario": "callCenter",
  "config": {
    "returnDetails": true,
    "locales": ["en-US"]
  },
  "fieldSchema": {
    "fields": {
      "Summary": {
        "type": "string",
        "method": "generate"
      },
      "Sentiment": {
        "type": "string",
        "method": "classify",
        "enum": [ "Positive", "Neutral", "Negative" ]
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

In the following example, we define a schema for extracting basic information from marketing videos.

```json
{
  "description": "Sample marketing video analyzer",
  "scenario": "videoShot",
  "fieldSchema": {
    "fields": {
      "Description": {
        "type": "string",
        "description": "Detailed summary of the video segment, focusing on product characteristics, lighting, and color palette."
      },
      "Sentiment": {
        "type": "string",
        "method": "classify",
        "enum": [ "Positive", "Neutral", "Negative" ]
      }
    }
  }
}
```

---

## Content and field extraction

**Content extraction** is the first step in the RAG implementation process. It transforms raw multimodal data into structured, searchable formats. This foundational step ensures that the content is organized and ready for indexing and retrieval. While content extraction provides the baseline for indexing and retrieval, it may not fully address domain-specific needs or provide deeper contextual insights.
[Learn more]() about content extraction capabilities for each modality.

**Field extraction** builds on content extraction by using AI to generate further metadata that enriches the knowledge base. This step allows you to define custom fields tailored to your specific use case, enabling more precise retrieval and enhanced search relevance. Field extraction complements content extraction by adding depth and context, making the data more actionable for RAG scenarios.
[Learn more]() about field extraction capabilities for each modality.

With the analyzers created for each modality, we can now process files to extract structured content and AI-generated metadata based on the defined schemas. This section demonstrates how to use the analyzers to analyze multimodal data and provides a sample of the results returned by the APIs. These results showcase the transformation of raw data into actionable insights, forming the foundation for indexing, retrieval, and RAG workflows.

---

#### Analyze files

``` python

#Iterate through each analyzer created and analyze content for each modality

analyzer_results =[]
extracted_markdown = []
analyzer_content = []
for analyzer in analyzer_configs:
    analyzer_id = analyzer["id"]
    template_path = analyzer["template_path"]
    file_location = analyzer["location"]
    try:
           # Analyze content
            response = content_understanding_client.begin_analyze(analyzer_id, file_location)
            result = content_understanding_client.poll_result(response)
            analyzer_results.append({"id":analyzer_id, "result": result["result"]})
            analyzer_content.append({"id": analyzer_id, "content": result["result"]["contents"]})

    except Exception as e:
            print(e)
            print("Error in creating analyzer. Please double-check your analysis settings.\nIf there is a conflict, you can delete the analyzer and then recreate it, or move to the next cell and use the existing analyzer.")

print("Analyzer Results:")
for analyzer_result in analyzer_results:
    print(f"Analyzer ID: {analyzer_result['id']}")
    print(json.dumps(analyzer_result["result"], indent=2))

# Delete the analyzer if it is no longer needed
#content_understanding_client.delete_analyzer(ANALYZER_ID)
```

---
### Extraction results

The following code samples demonstrate the output of content and field extraction using Azure Content Understanding. The JSON response contains multiple fields, each serving a specific purpose in representing the extracted data.

- **Markdown Field**: The `markdown` field provides a simplified, human-readable representation of the extracted content. It's especially useful for quick previews or for integrating the extracted data into applications that require structured text, such as knowledge bases or search interfaces. For example, with a document, the `markdown` field might include headers, paragraphs, and other structural elements formatted for easy readability.

- **JSON Output**: The full JSON output provides a comprehensive representation of the extracted data, including both the content and the metadata generated during the extraction process including the following properties:

  - **Fields:** AI-generated metadata such as summaries, key topics, or classifications, tailored to the specific schema defined in the analyzer.
  - **Confidence Scores:** Indicators of the reliability of the extracted data.
  - **Spans:** Information about the location of the extracted content within the source file.
  - **Additional Metadata:** Details such as page numbers, dimensions, and other contextual information.

---

# [Document](#tab/document)
The result shows the extraction of headers, paragraphs, tables, and other structural elements while maintaining the logical organization of the content. Additionally, it showcases the ability to extract key fields, providing concise extractions of lengthy materials.

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
The result shows the conversion of visual information into searchable text by verbalizing diagrams, extracting embedded text, and identifying graphical components.

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
The result shows the extraction of speaker-aware transcriptions, capturing spoken content and detecting multiple languages. Additionally field extraction extracts sentiment analysis and key topics from conversations to provide added context for queries.

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
The result shows the extraction of video segments into meaningful units, spoken content transcription, and scene descriptions. Additionally generating scene-level summaries, key topics identification, and brand presence analysis with field extraction.

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

## Preprocessing output from Content Understanding

Once the data is extracted using Azure Content Understanding, the next step is to prepare the analysis output for embedding within a search system. Preprocessing the output ensures that the extracted content is transformed into a format suitable for indexing and retrieval. This step involves converting the JSON output from the analyzers into structured strings, preserving both the content and metadata for seamless integration into downstream workflows.

The following example demonstrates how to preprocess the output data from the analyzers, including documents, images, audio, and video. The process of converting each JSON output into a structured string lays the groundwork for embedding the data into a vector-based search system, enabling efficient retrieval and enhanced RAG workflows.

---

``` python

def convert_values_to_strings(json_obj):
    return [str(value) for value in json_obj]

#process all content and convert to string
def process_allJSON_content(all_content):

    # Initialize empty list to store string of all content
    output = []

    document_splits = [
        "This is a json string representing a document with text and metadata for the file located in "+str(analyzer_configs[0]["location"])+" "
        + v
        + "```"
        for v in convert_values_to_strings(all_content[0]["content"])
    ]
    docs = [Document(page_content=v) for v in document_splits]
    output += docs

    #convert image json object to string and append file metadata to the string
    image_splits = [
       "This is a json string representing an image verbalization and OCR extraction for the file located in "+str(analyzer_configs[1]["location"])+" "
       + v
       + "```"
       for v in convert_values_to_strings(all_content[1]["content"])
    ]
    image = [Document(page_content=v) for v in image_splits]
    output+=image

    #convert audio json object to string and append file metadata to the string
    audio_splits = [
        "This is a json string representing an audio segment with transcription for the file located in "+str(analyzer_configs[2]["location"])+" "
       + v
       + "```"
       for v in convert_values_to_strings(all_content[2]["content"])
    ]
    audio = [Document(page_content=v) for v in audio_splits]
    output += audio

    #convert video json object to string and append file metadata to the string
    video_splits = [
        "The following is a json string representing a video segment with scene description and transcript for the file located in "+str(analyzer_configs[3]["location"])+" "
        + v
        + "```"
        for v in convert_values_to_strings(all_content[3]["content"])
    ]
    video = [Document(page_content=v) for v in video_splits]
    output+=video

    return output

all_splits = process_allJSON_content(analyzer_content)

print("There are " + str(len(all_splits)) + " documents.")
# Print the content of all doc splits
for doc in all_splits:
    print(f"doc content", doc.page_content)
```

---
## Embed and index extracted content

After preprocessing the extracted data from Azure Content Understanding is complete, the next step is to embed and index the content for efficient retrieval. This step involves transforming the structured strings into vector embeddings using an embedding model and storing them within an Azure AI Search system. By embedding the content, you enable semantic search capabilities, allowing the system to retrieve the most relevant information based on meaning rather than exact keyword matches. This step is critical for building a robust RAG solution, as it ensures that the extracted content is optimized for advanced search and retrieval workflows.


``` python
# Embed the splitted documents and insert into Azure Search vector store
def embed_and_index_chunks(docs):
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
    vector_store.add_documents(documents=docs)
    return vector_store


# embed and index the docs:
vector_store = embed_and_index_chunks(all_splits)
```
---

## Semantic chunk retrieval

With the extracted content embedded and indexed, the next step is to use the power of similarity and vector search to retrieve the most relevant chunks of information. This section demonstrates how to execute both similarity and hybrid searches, enabling the system to surface content based on semantic meaning rather than exact keyword matches. By retrieving contextually relevant chunks, you can enhance the precision of your RAG workflows and provide more accurate, meaningful responses to user queries.

``` python
# Set your query
query = "japan"

# Perform a similarity search
docs = vector_store.similarity_search(
    query=query,
    k=3,
    search_type="similarity",
)
for doc in docs:
    print(doc.page_content)

# Perform a hybrid search using the search_type parameter
docs = vector_store.hybrid_search(query=query, k=3)
for doc in docs:
    print(doc.page_content)

```
---

## Use OpenAI to interact with data

With the extracted content embedded and indexed, the final step in building a robust RAG solution is enabling conversational interactions using OpenAI chat models. This section demonstrates how to query your indexed data and apply OpenAI chat models to provide concise, contextually rich answers. By integrating conversational AI, you can transform your RAG solution into an interactive system that delivers meaningful insights and enhances user engagement. The following examples guide you through setting up a retrieval-augmented conversational flow, ensuring seamless integration between your data and OpenAI chat models.

---

```python
# Setup rag chain
prompt_str = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:"""


def setup_rag_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", k=3)

    prompt = ChatPromptTemplate.from_template(prompt_str)
    llm = AzureChatOpenAI(
        openai_api_version=AZURE_OPENAI_CHAT_API_VERSION,
        azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        azure_ad_token_provider=token_provider,
        temperature=0.7,
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


# Setup conversational search
def conversational_search(rag_chain, query):
    print(rag_chain.invoke(query))


rag_chain = setup_rag_chain(vector_store)
while True:
    query = input("Enter your query: ")
    if query=="":
        break
    conversational_search(rag_chain, query)
```

---


## Next steps

* [Explore our RAG Python code samples](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples)

* [Try a multimodal content solution accelerator](https://github.com/microsoft/content-processing-solution-accelerator)

* [Learn more Content Understanding analyzers](../concepts/analyzer-templates.md)
