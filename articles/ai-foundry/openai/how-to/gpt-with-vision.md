---
title: How to use vision-enabled chat models
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how to use vision-enabled chat models in Azure OpenAI, including how to call the Chat Completion API and process images.
author: PatrickFarley #dereklegenzoff
ms.author: pafarley #delegenz
#customer intent: As a developer, I want to learn how to use vision-enabled chat models so that I can integrate image processing capabilities into my applications.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/29/2026
manager: nitinme
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted


---

# Use vision-enabled chat models

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Vision-enabled chat models are large multimodal models (LMM) developed by OpenAI that can analyze images and provide textual responses to questions about them. They incorporate both natural language processing and visual understanding. The current vision-enabled models are the [o-series reasoning models](./reasoning.md), GPT-5 series, GPT-4.1 series, GPT-4.5, GPT-4o series.

The vision-enabled models can answer general questions about what's present in the images you upload.

> [!TIP]
> To use vision-enabled models, you call the Chat Completion API on a supported model that you have deployed. If you're not familiar with the Chat Completion API, see the [Vision-enabled chat how-to guide](/azure/ai-foundry/openai/how-to/chatgpt?tabs=python&pivots=programming-language-chat-completions).


## Call the Chat Completion APIs

The following command shows the most basic way to use a vision-enabled chat model with code. If this is your first time using these models programmatically, we recommend starting with our [Chat with images quickstart](../gpt-v-quickstart.md). 

#### [REST](#tab/rest)

Send a POST request to `https://{RESOURCE_NAME}.openai.azure.com/openai/v1/chat/completions` where

- RESOURCE_NAME is the name of your Azure OpenAI resource 

**Required headers**: 
- `Content-Type`: application/json 
- `api-key`: {API_KEY} 

**Body**: 
The following is a sample request body. The format is the same as the chat completions API for GPT-4o, except that the message content can be an array containing text and images (either a valid publicly accessible HTTP or HTTPS URL to an image, or a base-64-encoded image).

> [!IMPORTANT]
> Remember to set a `"max_tokens"`, or `max_completion_tokens` value  or the return output will be cut off.

> [!IMPORTANT]
> When uploading images, there is a limit of 10 images per chat request.

```json
{
    "model": "MODEL-DEPLOYMENT-NAME",
    "messages": [ 
        {
            "role": "system", 
            "content": "You are a helpful assistant." 
        },
        {
            "role": "user", 
            "content": [
	            {
	                "type": "text",
	                "text": "Describe this picture:"
	            },
	            {
	                "type": "image_url",
	                "image_url": {
                        "url": "<image URL>"
                    }
                } 
           ] 
        }
    ],
    "max_tokens": 100, 
    "stream": false 
} 
```

#### [Python](#tab/python)

1. Define your Azure OpenAI `base_url` and `api-key`. 
1. Create a client object using those values.

    ```python
    import os
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    )
    ```

1. Then call the client's **create** method. The following code shows a sample request body. The format is the same as the chat completions API for GPT-4o, except that the message content can be an array containing text and images (either a valid HTTP or HTTPS URL to an image, or a base-64-encoded image). 

    > [!IMPORTANT]
    > Remember to set a `"max_tokens"`, or `max_completion_tokens` value  or the return output will be cut off.
    
    ```python
    response = client.chat.completions.create(
        model="MODEL-DEPLOYMENT-NAME",
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture:" 
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": "<image URL>"
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )
    print(response)
    ```

---

> [!TIP]
> ### Use a local image
>
> If you want to use a local image, you can use the following Python code to convert it to base64 so it can be passed to the API. Alternative file conversion tools are available online.
>
> ```python
> import base64
> from mimetypes import guess_type
> 
> # Function to encode a local image into data URL 
> def local_image_to_data_url(image_path):
>     # Guess the MIME type of the image based on the file extension
>     mime_type, _ = guess_type(image_path)
>     if mime_type is None:
>         mime_type = 'application/octet-stream'  # Default MIME type if none is found
> 
>     # Read and encode the image file
>     with open(image_path, "rb") as image_file:
>         base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
> 
>     # Construct the data URL
>     return f"data:{mime_type};base64,{base64_encoded_data}"
> 
> # Example usage
> image_path = '<path_to_image>'
> data_url = local_image_to_data_url(image_path)
> print("Data URL:", data_url)
> ```
>
> When your base64 image data is ready, you can pass it to the API in the request body like this:
> 
> ```json
> ...
> "type": "image_url",
> "image_url": {
>    "url": "data:image/jpeg;base64,<your_image_data>"
> }
> ...
> ```

### Detail parameter settings  

You can optionally define a `"detail"` parameter in the `"image_url"` field. Choose one of three values, `low`, `high`, or `auto`, to adjust the way the model interprets and processes images. 
- `auto` setting: The default setting. The model decides between low or high based on the size of the image input.
- `low` setting: the model does not activate the "high res" mode, instead processes a lower resolution 512x512 version, resulting in quicker responses and reduced token consumption for scenarios where fine detail isn't crucial.
- `high` setting: the model activates "high res" mode. Here, the model initially views the low-resolution image and then generates detailed 512x512 segments from the input image. Each segment uses double the token budget, allowing for a more detailed interpretation of the image.

You set the value using the format shown in this example:

```json
{ 
    "type": "image_url",
    "image_url": {
        "url": "<image URL>",
        "detail": "high"
    }
}
```

For details on how the image parameters impact tokens used and pricing please see - [What is Azure OpenAI? Image Tokens](../../foundry-models/concepts/models-sold-directly-by-azure.md)


## Output

The API response should look like the following.

```json
{
    "id": "chatcmpl-8VAVx58veW9RCm5K1ttmxU6Cm4XDX",
    "object": "chat.completion",
    "created": 1702439277,
    "model": "gpt-4o",
    "prompt_filter_results": [
        {
            "prompt_index": 0,
            "content_filter_results": {
                "hate": {
                    "filtered": false,
                    "severity": "safe"
                },
                "self_harm": {
                    "filtered": false,
                    "severity": "safe"
                },
                "sexual": {
                    "filtered": false,
                    "severity": "safe"
                },
                "violence": {
                    "filtered": false,
                    "severity": "safe"
                }
            }
        }
    ],
    "choices": [
        {
            "finish_reason":"stop",
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The picture shows an individual dressed in formal attire, which includes a black tuxedo with a black bow tie. There is an American flag on the left lapel of the individual's jacket. The background is predominantly blue with white text that reads \"THE KENNEDY PROFILE IN COURAGE AWARD\" and there are also visible elements of the flag of the United States placed behind the individual."
            },
            "content_filter_results": {
                "hate": {
                    "filtered": false,
                    "severity": "safe"
                },
                "self_harm": {
                    "filtered": false,
                    "severity": "safe"
                },
                "sexual": {
                    "filtered": false,
                    "severity": "safe"
                },
                "violence": {
                    "filtered": false,
                    "severity": "safe"
                }
            }
        }
    ],
    "usage": {
        "prompt_tokens": 1156,
        "completion_tokens": 80,
        "total_tokens": 1236
    }
}
```

Every response includes a `"finish_reason"` field. It has the following possible values:
- `stop`: API returned complete model output.
- `length`: Incomplete model output due to the `max_tokens` input parameter or model's token limit.
- `content_filter`: Omitted content due to a flag from our content filters.




### Output

The chat responses you receive from the model should now include enhanced information about the image, such as object labels and bounding boxes, and OCR results. The API response should look like the following.

```json
{
    "id": "chatcmpl-8UyuhLfzwTj34zpevT3tWlVIgCpPg",
    "object": "chat.completion",
    "created": 1702394683,
    "model": "gpt-4o",
    "choices":
    [
        {
            "finish_reason": {
                "type": "stop",
                "stop": "<|fim_suffix|>"
            },
            "index": 0,
            "message":
            {
                "role": "assistant",
                "content": "The image shows a close-up of an individual with dark hair and what appears to be a short haircut. The person has visible ears and a bit of their neckline. The background is a neutral light color, providing a contrast to the dark hair."
            }
        }
    ],
    "usage":
    {
        "prompt_tokens": 816,
        "completion_tokens": 49,
        "total_tokens": 865
    }
}
```

Every response includes a `"finish_reason"` field. It has the following possible values:
- `stop`: API returned complete model output.
- `length`: Incomplete model output due to the `max_tokens` input parameter or model's token limit.
- `content_filter`: Omitted content due to a flag from our content filters.

<!--

### Create a video retrieval index

1. Get an Azure Vision in Foundry Tools resource in the same region as the Azure OpenAI resource you're using.
1. Create an index to store and organize the video files and their metadata. The example command below demonstrates how to create an index named `my-video-index` using the **[Create Index](/azure/ai-services/computer-vision/reference-video-search)** API. Save the index name to a temporary location; you'll need it in later steps. 

    > [!TIP]
    > For more detailed instructions on creating a video index, see [Do video retrieval using vectorization](/azure/ai-services/computer-vision/how-to/video-retrieval).

    > [!IMPORTANT]
    > A video index name can be up to 24 characters long, unless it's a GUID, which can be 36 characters.
        
    ```bash
    curl.exe -v -X PUT "https://<YOUR_ENDPOINT_URL>/computervision/retrieval/indexes/my-video-index?api-version=2023-05-01-preview" -H "Ocp-Apim-Subscription-Key: <YOUR_SUBSCRIPTION_KEY>" -H "Content-Type: application/json" --data-ascii "
    {
      'metadataSchema': {
        'fields': [
          {
            'name': 'cameraId',
            'searchable': false,
            'filterable': true,
            'type': 'string'
          },
          {
            'name': 'timestamp',
            'searchable': false,
            'filterable': true,
            'type': 'datetime'
          }
        ]
      },
      'features': [
        {
          'name': 'vision',
          'domain': 'surveillance'
        },
        {
          'name': 'speech'
        }
      ]
    }"
    ```

1. Add video files to the index with their associated metadata. The example below demonstrates how to add two video files to the index using SAS URLs with the **[Create Ingestion](/azure/ai-services/computer-vision/reference-video-search)** API. Save the SAS URLs and `documentId` values to a temporary location; you'll need them in later steps.
    
    ```bash
    curl.exe -v -X PUT "https://<YOUR_ENDPOINT_URL>/computervision/retrieval/indexes/my-video-index/ingestions/my-ingestion?api-version=2023-05-01-preview" -H "Ocp-Apim-Subscription-Key: <YOUR_SUBSCRIPTION_KEY>" -H "Content-Type: application/json" --data-ascii "
    {
      'videos': [
        {
          'mode': 'add',
          'documentId': '02a504c9cd28296a8b74394ed7488045',
          'documentUrl': 'https://example.blob.core.windows.net/videos/02a504c9cd28296a8b74394ed7488045.mp4?sas_token_here',
          'metadata': {
            'cameraId': 'camera1',
            'timestamp': '2023-06-30 17:40:33'
          }
        },
        {
          'mode': 'add',
          'documentId': '043ad56daad86cdaa6e493aa11ebdab3',
          'documentUrl': '[https://example.blob.core.windows.net/videos/043ad56daad86cdaa6e493aa11ebdab3.mp4?sas_token_here',
          'metadata': {
            'cameraId': 'camera2'
          }
        }
      ]
    }"
    ```

1. After you add video files to the index, the ingestion process starts. It might take some time depending on the size and number of files. To ensure the ingestion is complete before performing searches, you can use the **[Get Ingestion](/en-us/azure/ai-services/computer-vision/reference-video-search)** API to check the status. Wait for this call to return `"state" = "Completed"` before proceeding to the next step. 
    
    ```bash
    curl.exe -v -X GET "https://<YOUR_ENDPOINT_URL>/computervision/retrieval/indexes/my-video-index/ingestions?api-version=2023-05-01-preview&$top=20" -H "ocp-apim-subscription-key: <YOUR_SUBSCRIPTION_KEY>"
    ```
-->

## Related content

* [Learn more about Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md).
* [Vision-enabled chats quickstart](../gpt-v-quickstart.md)
* [Vision chats frequently asked questions](../faq.yml#gpt-4-turbo-with-vision)
* [Chat completions API reference](https://aka.ms/gpt-v-api-ref)
