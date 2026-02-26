---
title: Create a custom analyzer with Azure Content Understanding in Foundry Tools using REST APIs
titleSuffix: Foundry Tools
description: Learn to create a custom analyzer with Azure Content Understanding in Foundry Tools
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 01/30/2026
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Create a custom analyzer using REST APIs

Content Understanding analyzers define how to process and extract insights from your content. They ensure uniform processing and output structure across all your content, so you get reliable and predictable results. For common use cases, you can use the [prebuilt analyzers](../concepts/prebuilt-analyzers.md). This guide shows how you can customize these analyzers to better fit your needs.

In this guide, you use the cURL command line tool. If it isn't installed, you can [download](https://everything.curl.dev/install/index.html) the appropriate version for your developer environment.

## Prerequisites
To get started, make sure you have the following resources and permissions:
* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* After you get your Azure subscription, create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. Be sure to create it in a [supported region](/azure/ai-services/content-understanding/language-region-support).
   * The portal lists this resource under **Foundry** > **Foundry**.
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Define an analyzer schema

# [Document](#tab/document)

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, you create an analyzer based on the [prebuilt document analyzer](../concepts/prebuilt-analyzers.md) for processing a receipt.

Create a JSON file named `receipt.json` with the following content:
```json
{
  "description": "Sample receipt analyzer",
  "baseAnalyzerId": "prebuilt-document",
  "models": {
      "completion": "gpt-4.1",
      "embedding": "text-embedding-ada-002"

    },
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

If you have various types of documents you need to process, but you want to categorize and analyze only the receipts, create an analyzer that categorizes the document first. Then, route it to the analyzer you created earlier with the following schema.

Create a JSON file named `categorize.json` with the following content:
```json
{
  "baseAnalyzerId": "prebuilt-document",
  // Use the base analyzer to invoke the document specific capabilities.

  //Specify the model the analyzer should use. This is one of the supported completion models and one of the supported embeddings model. The specific deployment used during analyze is set on the resource or provided in the analyze request.
  "models": {
      "completion": "gpt-4.1",
      "embedding": "text-embedding-ada-002"

    },
  "config": {
    // Enable splitting of the input into segments. Set this property to false if you only expect a single document within the input file. When specified and enableSegment=false, the whole content will be classified into one of the categories.
    "enableSegment": false,

    "contentCategories": {
      // Category name.
      "receipt": {
        // Description to help with classification and splitting.
        "description": "Any images or documents of receipts",

        // Define the analyzer that any content classified as a receipt should be routed to
        "analyzerId": "receipt"
      },

      "invoice": {
        "description": "Any images or documents of invoice",
        "analyzerId": "prebuilt-invoice"
      },
      "policeReport": {
        "description": "A police or law enforcement report detailing the events that lead to the loss."
        // Don't perform analysis for this category.
      }

    },

    // Omit original content object and only return content objects from additional analysis.
    "omitContent": true
  }

  //You can use fieldSchema here to define fields that are needed from the entire input content.

}
```


# [Image](#tab/image)

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, you create an analyzer based on a [prebuilt image analyzer](../concepts/prebuilt-analyzers.md) for processing images of charts and graphs.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample image analyzer for charts and graphs",
  "baseAnalyzerId": "prebuilt-image",
  "models": {
      "completion": "gpt-4.1"
    },
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

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, you create an analyzer based on a [prebuilt call center analyzer](../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample customer support call analyzer",
  "baseAnalyzerId": "prebuilt-audio",
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

To create a custom analyzer, define a field schema that describes the structured data you want to extract. In the following example, you create an analyzer based on a [prebuilt video  analyzer](../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

Create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample product demo video analyzer",
  "baseAnalyzerId": "prebuilt-video",
  "models": {
      "completion": "gpt-4.1"
    },
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

## Create an analyzer

### PUT request

# [Document](#tab/document)

Create a receipt analyzer first, and then create the categorize analyzer.

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @receipt.json
```

# [Image](#tab/image)

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```

# [Audio](#tab/audio)

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```

# [Video](#tab/video)

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```

---

### PUT response

The `201 Created` response includes an `Operation-Location` header with a URL that you can use to track the status of this asynchronous analyzer creation operation.

```
201 Created
Operation-Location: {endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2025-05-01-preview
```

When the operation finishes, an HTTP GET on the operation location URL returns `"status": "succeeded"`.

```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Analyze a file

### Submit the file

You can now use the custom analyzer you created to process files and extract the fields you defined in the schema.

Before running the cURL command, make the following changes to the HTTP request:

# [Document](#tab/document)


1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer you created with the `categorize.json` file.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/receipt.png`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer you created.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg`.

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer you created.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav`.

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Foundry instance.
1. Replace `{analyzerId}` with the name of the custom analyzer you created.
1. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4`.

---

#### POST Request

# [Document](#tab/document)

This example uses the custom analyzer you created with the `categorize.json` file to analyze a receipt.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/receipt.png"
          }          
        ]
      }'  
```

# [Image](#tab/image)

This example uses the custom analyzer you created to analyze a chart or graph image.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg"
          }          
        ]
      }'  
```

# [Audio](#tab/audio)

This example uses the custom analyzer you created to analyze a customer support call recording.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav"
          }          
        ]
      }'  
```

# [Video](#tab/video)

This example uses the custom analyzer you created to analyze a product demo video.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4"
          }          
        ]
      }'  
```

---

#### POST Response

The `202 Accepted` response includes the `{resultId}` which you can use to track the status of this asynchronous operation.

```
{
  "id": {resultId},
  "status": "Running",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": []
  }
}
```

### Get analyze result

Use the `Operation-Location` from the `POST` response to get the result of the analysis.

#### GET request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzerResults/{resultId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

#### GET response

A `200 OK` response includes a `status` field that shows the operation's progress.  
- The `status` is `Succeeded` if the operation completes successfully.  
- If the status is `running` or `notStarted`, call the API again manually or use a script. Wait at least one second between requests.

##### Sample response

# [Document](#tab/document)

```json
{
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "path": "input1/segment1",
        "category": "receipt",
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
            "angle": -0.0944,
            "width": 1743,
            "height": 878
          }
        ],
        "analyzerId": "{analyzerId}",
        "mimeType": "image/png"
      }
    ]
  },
  "usage": {
    "documentPages": 1,
    "tokens": {
      "contextualization": 1000
    }
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
    "apiVersion": "2025-11-01",
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
            "pageNumber": 1
          }
        ],
        "analyzerId": "{analyzerId}",
        "mimeType": "image/jpeg"
      }
    ]
  },
  "usage": {
    "tokens": {
      "contextualization": 1000
    }
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
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
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
  },
  "usage": {
    "audioHours": 0.032,
    "tokens": {
      "contextualization": 3194.445
    }
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
    "apiVersion": "2025-11-01",
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
                  
                  "SegmentId": {
                    "type": "string",
                    "valueString": "00:00:00.000-00:00:01.467"
                  },
                  "Description": {
                    "type": "string",
                    "valueString": "The video opens with a dramatic aerial shot of a small airplane flying over a tropical island surrounded by turquoise waters. The logos for 'Flight Simulator' and 'Microsoft Azure AI' are prominently displayed, indicating a collaboration or feature integration between the two."
                  },
                  "Sentiment": {
                    "type": "string",
                    "valueString": "Positive"
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
        "KeyFrameTimesMs": [733, ... , 43233],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 1360,
            "endTimeMs": 6640,
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
  },
  "usage": {
    "videoHours": 0.013,
    "tokens": {
      "contextualization": 12222.223
    }
  }
}
```

---

## Related content

* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Try processing your document content using Content Understanding in [Foundry](https://aka.ms/cu-landing).
