---
title: "Quickstart: Analyze multimodal content"
titleSuffix: Azure AI services
description: Get started using Azure AI Content Safety to analyze text content in images for objectionable material.
#services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 09/19/2024
ms.author: pafarley
# zone_pivot_groups: programming-languages-content-safety
---

# Quickstart: Analyze multimodal content (Preview) 

The Multimodal API analyzes materials containing both image content and text content to help make applications and services safer from harmful user-generated or AI-generated content.

For more information on Multimodal, see the [Multimodal concept page](./concepts/Multimodal.md). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview. 

> [!IMPORTANT]
> This feature is only available in certain Azure regions. See [Region availability](./overview.md#region-availability).


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource</a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, [supported region](./overview.md#region-availability), and supported pricing tier. Then select **Create**.
   * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. Copy the endpoint and either of the key values to a temporary location for later use.
* One of the following installed:
   * [cURL](https://curl.haxx.se/) for REST API calls.
   * [Python 3.x](https://www.python.org/) installed


## Analyze image with text

The following section walks through a sample image moderation request with cURL. 

### Prepare a sample image

Choose a sample image to analyze, and download it to your device. 

We support JPEG, PNG, GIF, BMP, TIFF, or WEBP image formats. The maximum size for image submissions is 4 MB, and image dimensions must be between 50 x 50 pixels and 7,200 x 7,200 pixels. If your format is animated, we'll extract the first frame to do the detection.

You can input your image by one of two methods: **local filestream** or **blob storage URL**.
- **Local filestream** (recommended): Encode your image to base64. You can use a website like [codebeautify](https://codebeautify.org/image-to-base64-converter) to do the encoding. Then save the encoded string to a temporary location. 
- **Blob storage URL**: Upload your image to an Azure Blob Storage account. Follow the [blob storage quickstart](/azure/storage/blobs/storage-quickstart-blobs-portal) to learn how to do this. Then open Azure Storage Explorer and get the URL to your image. Save it to a temporary location. 

### Analyze image with text 

Paste the command below into a text editor, and make the following changes.

1. Substitute the `<endpoint>` with your resource endpoint URL.
1. Replace `<your_subscription_key>` with your key.
1. Populate the `"image"` field in the body with either a `"content"` field or a `"blobUrl"` field. For example: `{"image": {"content": "<base_64_string>"}` or `{"image": {"blobUrl": "<your_storage_url>"}`.

```shell
curl --location '<Endpoint>contentsafety/imageWithText:analyze?api-version=2024-09-15-preview ' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>7' \
--header 'Content-Type: application/json' \
--data '{
  "image": {
      "content": "<image base 64 code>"
 },
  "categories": ["Hate","Sexual","Violence","SelfHarm"],
  "enableOcr": true,
  "text": "I want to kill you"
}'
```

> [!NOTE]
> If you're using a blob storage URL, please replace "content" to "blobUrl":
>
> ```
> {
>   "image": {
>     "blobUrl": "<your_storage_url>"
>   }
> }
> ```
Open a command prompt window and run the cURL command.

The below fields must be included in the URL:

| Name      |Required?  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. Current version is: `api-version=2024-09-15`. Example: `<endpoint>/contentsafety/imageWithText:analyze?api-version=2024-09-15` | String |

The parameters in the request body are defined in this table:

| Name                   | Description                                                  | Type    |
| :--------------------- | :----------------------------------------------------------- | ------- |
| **content or blobUrl** | (Required) The content or blob URL of the image. I can be either base64-encoded bytes or a blob URL. If both are given, the request is refused. The maximum allowed size of the image is 7,200 x 7,200 pixels, and the maximum file size is 4 MB. The minimum size of the image is 50 pixels x 50 pixels. | String  |
| **text**               | (Optional) The text attached to the image. We support at most 1000 characters (unicode code points) in one text request. | String  |
| **enableOcr**          | (Required) When set to true, our service will perform OCR and analyze the detected text with input image at the same time. We will recognize at most 1000 characters (unicode code points) from input image. The others will be truncated. | Boolean |
| **categories**         | (Optional) This is assumed to be an array of category names. See the [Harm categories guide](../../concepts/harm-categories.md) for a list of available category names. If no categories are specified, all four categories are used. We use multiple categories to get scores in a single request. | Enum    |




### Output

You should see the image with text moderation results displayed as JSON data in the console. For example:

```json
{
  "categoriesAnalysis": [
    {
      "category": "Hate",
      "severity": 2
    },
    {
      "category": "SelfHarm",
      "severity": 0
    },
    {
      "category": "Sexual",
      "severity": 0
    },
    {
      "category": "Violence",
      "severity": 0
    }
  ]
}
```

The JSON fields in the output are defined here:

| Name     | Description   | Type   |
| :------------- | :--------------- | ------ |
| **categoriesAnalysis**   | Each output class that the API predicts. Classification can be multi-labeled. For example, when an image is uploaded to the image moderation model, it could be classified as both sexual content and violence. [Harm categories](../../concepts/harm-categories.md)| String |
| **Severity** | The severity level of the flag in each harm category. [Harm categories](../../concepts/harm-categories.md)  | Integer |
