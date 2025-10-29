---
title: "Quickstart: Analyze multimodal content with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/28/2025
ms.author: pafarley
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource</a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, [supported region](../../overview.md#region-availability), and supported pricing tier. Then select **Create**.
   * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. Copy the endpoint and either of the key values to a temporary location for later use.
* One of the following installed:
   * [cURL](https://curl.haxx.se/) for REST API calls.
   * [Python 3.x](https://www.python.org/) installed


## Analyze image with text

The following section walks through a sample multimodal moderation request with cURL.

### Prepare a sample image

Choose a sample image to analyze, and download it to your device. 

See [Input requirements](../../overview.md#input-requirements) for the image limitations. If your format is animated, the service will extract the first frame to do the analysis.

You can input your image by one of two methods: **local filestream** or **blob storage URL**.
- **Local filestream** (recommended): Encode your image to base64. You can use a website like [codebeautify](https://codebeautify.org/image-to-base64-converter) to do the encoding. Then save the encoded string to a temporary location. 
- **Blob storage URL**: Upload your image to an Azure Blob Storage account. Follow the [blob storage quickstart](/azure/storage/blobs/storage-quickstart-blobs-portal) to learn how to do this. Then open Azure Storage Explorer and get the URL to your image. Save it to a temporary location. 

### Analyze content 

Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with your resource endpoint URL.
1. Replace `<your_subscription_key>` with your key.
1. Populate the `"image"` field in the body with either a `"content"` field or a `"blobUrl"` field. For example: `{"image": {"content": "<base_64_string>"}` or `{"image": {"blobUrl": "<your_storage_url>"}`.
1. Optionally replace the value of the `"text"` field with your own text you'd like to analyze.

```shell
curl --location '<endpoint>/contentsafety/imageWithText:analyze?api-version=2024-09-15-preview ' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data '{
  "image": {
      "content": "<base_64_string>"
 },
  "categories": ["Hate","Sexual","Violence","SelfHarm"],
  "enableOcr": true,
  "text": "I want to kill you"
}'
```

> [!NOTE]
> If you're using a blob storage URL, the request body should look like this:
>
> ```
> {
>   "image": {
>     "blobUrl": "<your_storage_url>"
>   }
> }
> ```


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

Open a command prompt window and run the cURL command.


### Interpret the API response


You should see the image and text moderation results displayed as JSON data in the console. For example:

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
