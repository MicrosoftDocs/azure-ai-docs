---
title: 'Quickstart: Generate video with Sora'
titleSuffix: Azure OpenAI
description: Learn how to get started generating video clips with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 05/22/2025
---

# Quickstart: Generate a video with Sora (preview)

In this Quickstart, you generate video clips using the Azure OpenAI service. The example uses the Sora model, which is a video generation model that creates realistic and imaginative video scenes from text instructions. This guide shows how to create a video generation job, poll for its status, and retrieve the generated video.


## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).
- Then, you need to deploy a `sora` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](./how-to/create-resource.md).


## Setup

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="./media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](./includes/environment-variables.md)]




## Create a video generation job

Send a POST request to create a new video generation job.

```bash
curl -X POST "{endpoint}/openai/v1/video/generations/jobs?api-version=preview" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer {Azure_OpenAI_Auth_Token}" ^
  -H "api-key: {Your-API-Key}" ^
  -d "{
    \"prompt\": \"A cat playing piano in a jazz bar.\",
    \"model\": \"sora\"
  }"
```



## Poll for job status

Send a GET request with the `job-id` from the previous step to check the job status.

```bash
curl -X GET "{endpoint}/openai/v1/video/generations/jobs/{job-id}?api-version=preview" ^
  -H "Authorization: Bearer {Azure_OpenAI_Auth_Token}" ^
  -H "api-key: {Your-API-Key}"
```

Repeat this step until the status is `succeeded`. Then you can retrieve the generated video ID from the `"generations"` field.

## Retrieve the generated video

Once the job status is `succeeded`, use the generation ID from the job result to get the generated video.

```bash
curl -X GET "{endpoint}/openai/v1/video/generations/{generation-id}?api-version=preview" ^
  -H "Authorization: Bearer {Azure_OpenAI_Auth_Token}" ^
  -H "api-key: {Your-API-Key}"
```

The response contains the download URL for your generated video.

