---
title: Create a custom analyzer with Azure AI Content Understanding using REST APIs
titleSuffix: Azure AI services
description: Learn to create a custom analyzer with Azure AI Content Understanding
author: laujan
ms.author: paulhsu
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Create a custom analyzer via REST APIs

Content Understanding analyzers define how to process and extract insights from your content. They ensure uniform processing and output structure across all your content to deliver reliable and predictable results. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. This guide shows how these analyzers can be customized to better fit your needs.

In this guide, we use the cURL command line tool. If it isn't installed, you can [download](https://everything.curl.dev/install/index.html) the appropriate version for your dev environment.

## Define an analyzer schema

# [Document](#tab/document)

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, we create an analyzer based on [prebuilt document analyzer](../concepts/prebuilt-analyzers.md) for processing a receipt.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample receipt analyzer",
  "baseAnalyzerId": "prebuilt-documentAnalyzer",
  "config": {
    "returnDetails": true,
    "enableFormula": false,
    "disableContentFiltering": false,
    "estimateFieldSourceAndConfidence": true,
    "tableFormat": "html"
  },
 "fieldSchema": {
    "fields": {
      "VendorName": {
        "type": "string",
        "method": "extract",
        "description": "Vendor issuing the receipt"
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

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, we create an analyzer based on [prebuilt image analyzer](../concepts/prebuilt-analyzers.md) for processing images of charts and graphs.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample image analyzer for charts and graphs",
  "baseAnalyzerId": "prebuilt-imageAnalyzer",
  "config": {
    "disableContentFiltering": false
 },
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

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, we create an analyzer based on [prebuilt call center analyzer](../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample customer support call analyzer",
  "baseAnalyzerId": "prebuilt-callCenter",
  "config": {
    "locales": ["en-US", "fr-FR"],
    "returnDetails": true,
    "disableContentFiltering": false
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
        "enum": ["Positive", "Neutral", "Negative"]
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

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, we create an analyzer based on [prebuilt video  analyzer](../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample product demo video analyzer",
  "baseAnalyzerId": "prebuilt-videoAnalyzer",
  "config": {
    "locales": ["en-US", "fr-FR"],
    "returnDetails": true,
    "enableFace": false,
    "disableFaceBlurring": false,
    "personDirectoryId": null,
    "segmentationMode": "auto",
    "disableContentFiltering": false
  },
   "fieldSchema": {
    "fields": {
      "Segments": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "SegmentId": {
              "type": "string"
            },
            "Description": {
              "type": "string",
              "method": "generate",
              "description": "Detailed summary of the video segment, focusing on product characteristics, lighting, and color palette."
            },
            "Sentiment": {
              "type": "string",
              "method": "classify",
              "enum": ["Positive", "Neutral", "Negative"]
            }
          }
        }
      }
    }
  }
}

```

---

## Build analyzer

### PUT request

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```

### PUT response

The 201 `Created` response includes an `Operation-Location` header containing a URL that you can use to track the status of this asynchronous analyzer creation operation.

```
201 Created
Operation-Location: {endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2025-05-01-preview
```

Upon completion, performing an HTTP GET on the operation location URL returns `"status": "succeeded"`.

```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Analyze file

### Send file

You can now use the custom analyzer you created to process files and extract the fields you defined in the schema.

Before running the cURL command, make the following changes to the HTTP request:

# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/receipt.png`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg`.

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav`.

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4`.

---

#### POST Request
```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"{fileUrl}\"}"
```

#### POST Response

The `202 Accepted` response includes the `{resultId}` which you can use to track the status of this asynchronous operation.

```
{
  "id": {resultId},
  "status": "Running",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": []
  }
}
```

### Get Analyze Result

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Foundry instance.
2. Replace `{resultId}` with the `resultId` in `POST` response.

#### GET Request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzerResults/{resultId}?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

#### GET Response

A `200 OK` response includes a `status` field that shows the operation's progress.  
- `status` is `Succeeded` if the operation is completed successfully.  
- If it's `running` or `notStarted`, call the API again manually or with a script: wait at least one second between requests.

##### Sample Response

# [Document](#tab/document)

```json
{
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "markdown": "Contoso\n\n123 Main Street\nRedmond, WA 98052\n\n987-654-3210\n\n6/10/2019 13:59\nSales Associate: Paul\n\n\n<table>\n<tr>\n<td>2 Surface Pro 6</td>\n<td>$1,998.00</td>\n</tr>\n<tr>\n<td>3 Surface Pen</td>\n<td>$299.97</td>\n</tr>\n</table> ...",
        "fields": {
          "VendorName": {
            "type": "string",
            "valueString": "Contoso",
            "spans": [{"offset": 0,"length": 7}],
            "confidence": 0.996,
            "source": "D(1,774.0000,72.0000,974.0000,70.0000,974.0000,111.0000,774.0000,113.0000)"
          },
          "Items": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Description": {
                    "type": "string",
                    "valueString": "2 Surface Pro 6",
                    "spans": [ { "offset": 115, "length": 15}],
                    "confidence": 0.423,
                    "source": "D(1,704.0000,482.0000,875.0000,482.0000,875.0000,508.0000,704.0000,508.0000)"
                  },
                  "Amount": {
                    "type": "number",
                    "valueNumber": 1998,
                    "spans": [{ "offset": 140,"length": 9}
                    ],
                    "confidence": 0.957,
                    "source": "D(1,952.0000,482.0000,1048.0000,482.0000,1048.0000,508.0000,952.0000,509.0000)"
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "pixel",
        "pages": [
          {
            "pageNumber": 1,
            "angle": -0.0848,
            "width": 1743,
            "height": 878,
            "spans": [
              {
                "offset": 0,
                "length": 375
              }
            ],
            "words": [
              {
                "content": "Contoso",
                "span": {"offset": 0,"length": 7 },
                "confidence": 0.995,
                "source": "D(1,774,72,974,70,974,111,774,113)"
              }, ...

            ],
            "lines": [
              {
                "content": "Contoso",
                "source": "D(1,774,71,973,70,974,111,774,113)",
                "span": {"offset": 0,"length": 7}
              }, ...
            ]
          }
        ],
        "paragraphs": [
          {
            "content": "Contoso",
            "source": "D(1,774,71,973,70,974,111,774,113)",
            "span": {"offset": 0,"length": 7}
          }, ...
        ],
        "sectios": [
          {
            "span": {"offset": 0,"length": 374 },
            "elements": ["/paragraphs/0","/paragraphs/1", ...]
          }
        ],
        "tables": [
          {
            "rowCount": 2,
            "columnCount": 2,
            "cells": [
              {
                "kind": "content",
                "rowIndex": 0,
                "columnIndex": 0,
                "rowSpan": 1,
                "columnSpan": 1,
                "content": "2 Surface Pro 6",
                "source": "D(1,691,471,911,470,911,514,691,515)",
                "span": {"offset": 115,"length": 15},
                "elements": ["/paragraphs/4"]
              }, ...
            ],
            "source": "D(1,759,593,1056,592,1057,741,760,742)",
            "span": {"offset": 223,"length": 151}
          }
        ]
      }
    ]
  }
}

```

# [Image](#tab/image)

```json
{
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
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
            "spans": []
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
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Audio: 00:00.000 => 01:54.670\nTranscript\n```\n<v Agent>Thank you for calling Woodgrove Travel...\n<v Customer>Hi Isabella, my name is John Smith...\n<v Agent>Could you provide flight details?\n<v Customer>Contoso Airways, flight CA123...\n<v Agent>Sorry to 
                     hear that...\n<v Customer>Flight delay made me miss meeting...\n<v Agent>We’ll offer a partial refund...\n<v Customer>Thanks, appreciate your help!\n```",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "John Smith contacted Woodgrove Travel to report a negative experience with a flight on Contoso Airways ..."
          },
          "Sentiment": {
            "type": "string",
            "valueString": "Positive"
          },
          "People": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Name": {
                    "type": "string",
                    "valueString": "Isabella Taylor"
                  },
                  "Role": {
                    "type": "string",
                    "valueString": "Agent"
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 114670,
        "transcriptPhrases": [
          {
            "speaker": "Agent",
            "startTimeMs": 80,
            "endTimeMs": 2160,
            "text": "Thank you for calling Woodgrove Travel.",
            "words": []
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
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SS",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Video: 00:00 => 00:43\n## Segment 1: Island view\nTranscript\n```\n00:01 --> 00:06\n<Speaker 1>Good data improves TTS.\n```\nKey Frames: ![](keyFrame.726.jpg) ## Segment 2: Data center\nTranscript\n```\n00:07 --> 00:13\n<Speaker 2>We trained on 3,000   
                     hours.\n```\nKey Frames: ![](keyFrame.2046.jpg) ![](keyFrame.4884.jpg)",
        "fields": {
          "Segments": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Sentiment": {
                    "type": "string",
                    "valueString": "Positive"
                  },
                  "SegmentId": {
                    "type": "string",
                    "valueString": "1"
                  },
                  "Description": {
                    "type": "string",
                    "valueString": "The video begins with a scenic aerial view of an island, showcasing the collaboration between Flight Simulator and Microsoft Azure AI."
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 43866,
        "width": 1080,
        "height": 608,
        "KeyFrameTimesMs": [726, ... , 43230],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 1400,
            "endTimeMs": 6560,
            "text": "When it comes to the neural TTS, in order to get a good voice, it's better to have good data.",
            "words": []
          }, ...
        ],
        "cameraShotTimesMs": [1467, ...  42033],
        "segments": [
          {
            "startTimeMs": 0,
            "endTimeMs": 1467,
            "description": "The video begins with a scenic aerial view of an island, showcasing the collaboration between Flight Simulator and Microsoft Azure AI.",
            "segmentId": "1"
          }, ...
        ]
      }
    ]
  }
}
```

## Next steps

* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Try processing your document content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
