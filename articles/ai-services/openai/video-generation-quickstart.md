---
title: 'Quickstart: Generate video with Azure OpenAI'
titleSuffix: Azure OpenAI
description: Learn how to get started generating video clips with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 05/12/2025
---

# Quickstart: Generate video with Azure OpenAI

tbd 

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).
- Then, you need to deploy a `sora` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).


## Setup

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](environment-variables.md)]


POST: Create Video Generation Job 
`/deployments/{deployment-id}/video/generations/job`


GET: Get Video Generation Job /deployments/{deployment-id}/video/generations/jobs/{job-id}

GET: Get Video Generation /deployments/{deployment id}/video/generations/jobs/{generation-id}