---
title: How to use the GPT-4 Turbo with Vision model
titleSuffix: Azure OpenAI Service
description: Learn about the options for using GPT-4 Turbo with Vision
author: PatrickFarley #dereklegenzoff
ms.author: pafarley #delegenz
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 08/21/2024
manager: nitinme
---

# Use GPT-4 Turbo with Vision


GPT-4 Turbo with Vision is a large multimodal model (LMM) developed by OpenAI that can analyze images and provide textual responses to questions about them. It incorporates both natural language processing and visual understanding.

The GPT-4 Turbo with Vision model answers general questions about what's present in images.

> [!TIP]
> To use GPT-4 Turbo with Vision, you call the Chat Completion API on a GPT-4 Turbo with Vision model that you have deployed. If you're not familiar with the Chat Completion API, see the [GPT-4 Turbo & GPT-4 how-to guide](/azure/ai-services/openai/how-to/chatgpt?tabs=python&pivots=programming-language-chat-completions).

## GPT-4 Turbo model upgrade

[!INCLUDE [GPT-4 Turbo](../includes/gpt-4-turbo.md)]

## Call the Chat Completion APIs

The following command shows the most basic way to use the GPT-4 Turbo with Vision model with code. If this is your first time using these models programmatically, we recommend starting with our [GPT-4 Turbo with Vision quickstart](../gpt-v-quickstart.md). 

#### [REST](#tab/rest)

Send a POST request to `https://{RESOURCE_NAME}.openai.azure.com/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview` where 

- RESOURCE_NAME is the name of your Azure OpenAI resource 
- DEPLOYMENT_NAME is the name of your GPT-4 Turbo with Vision model deployment 

**Required headers**: 
- `Content-Type`: application/json 
- `api-key`: {API_KEY} 



**Body**: 
The following is a sample request body. The format is the same as the chat completions API for GPT-4, except that the message content can be an array containing text and images (either a valid HTTP or HTTPS URL to an image, or a base-64-encoded image). 

> [!IMPORTANT]
> Remember to set a `"max_tokens"` value, or the return output will be cut off.

> [!IMPORTANT]
> When uploading images, there is a limit of 10 images per chat request.

```json
{
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

1. Define your Azure OpenAI resource endpoint and key. 
1. Enter the name of your GPT-4 Turbo with Vision model deployment.
1. Create a client object using those values.

    ```python
    api_base = '<your_azure_openai_endpoint>' # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_key="<your_azure_openai_key>"
    deployment_name = '<your_deployment_name>'
    api_version = '2024-02-15-preview' # this might change in the future
    
    client = AzureOpenAI(
        api_key=api_key,  
        api_version=api_version,
        base_url=f"{api_base}openai/deployments/{deployment_name}",
    )
    ```

1. Then call the client's **create** method. The following code shows a sample request body. The format is the same as the chat completions API for GPT-4, except that the message content can be an array containing text and images (either a valid HTTP or HTTPS URL to an image, or a base-64-encoded image). 

    > [!IMPORTANT]
    > Remember to set a `"max_tokens"` value, or the return output will be cut off.
    
    ```python
    response = client.chat.completions.create(
        model=deployment_name,
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

### Output

The API response should look like the following.

```json
{
    "id": "chatcmpl-8VAVx58veW9RCm5K1ttmxU6Cm4XDX",
    "object": "chat.completion",
    "created": 1702439277,
    "model": "gpt-4",
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

### Detail parameter settings in image processing: Low, High, Auto  

The _detail_ parameter in the model offers three choices: `low`, `high`, or `auto`, to adjust the way the model interprets and processes images. The default setting is auto, where the model decides between low or high based on the size of the image input. 
- `low` setting: the model does not activate the "high res" mode, instead processes a lower resolution 512x512 version, resulting in quicker responses and reduced token consumption for scenarios where fine detail isn't crucial.
- `high` setting: the model activates "high res" mode. Here, the model initially views the low-resolution image and then generates detailed 512x512 segments from the input image. Each segment uses double the token budget, allowing for a more detailed interpretation of the image.''

For details on how the image parameters impact tokens used and pricing please see - [What is Azure OpenAI? Image Tokens](../overview.md#image-tokens)



### Output

The chat responses you receive from the model should now include enhanced information about the image, such as object labels and bounding boxes, and OCR results. The API response should look like the following.

```json
{
    "id": "chatcmpl-8UyuhLfzwTj34zpevT3tWlVIgCpPg",
    "object": "chat.completion",
    "created": 1702394683,
    "model": "gpt-4",
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



### Create a video retrieval index

1. Get an Azure AI Vision resource in the same region as the Azure OpenAI resource you're using.
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


## Next steps

* [Learn more about Azure OpenAI](../overview.md).
* [GPT-4 Turbo with Vision quickstart](../gpt-v-quickstart.md)
* [GPT-4 Turbo with Vision frequently asked questions](../faq.yml#gpt-4-turbo-with-vision)
* [GPT-4 Turbo with Vision API reference](https://aka.ms/gpt-v-api-ref)
