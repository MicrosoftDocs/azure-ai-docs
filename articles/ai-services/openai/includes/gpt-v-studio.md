---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images and videos with the Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Use this article to get started using Azure OpenAI Studio to deploy and use the GPT-4 Turbo with Vision model.  
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions
ms.date: 11/02/2023
---

Start exploring GPT-4 Turbo with Vision capabilities with a no-code approach through Azure OpenAI Studio.

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- An Azure OpenAI Service resource with a GPT-4 Turbo with Vision model deployed. See [GPT-4 and GPT-4 Turbo Preview model availability](../concepts/models.md#gpt-4-and-gpt-4-turbo-model-availability) for available regions. For more information about resource creation, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).

> [!NOTE]
> It is currently not supported to turn off content filtering for the GPT-4 Turbo with Vision model.

## Go to Azure OpenAI Studio

Browse to [Azure OpenAI Studio](https://oai.azure.com/) and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

Under **Management** select **Deployments** and **Create** a GPT-4 Turbo with Vision deployment by selecting model name: **"gpt-4"** and model version **"vision-preview"**. For more information about model deployment, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).  

Under the **Playground** section select **Chat**.

## Playground

From this page, you can quickly iterate and experiment with the model's capabilities. 

For general help with assistant setup, chat sessions, settings, and panels, refer to the [Chat quickstart](/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-studio). 


## Start a chat session to analyze images or video

#### [Image prompts](#tab/image)

In this chat session, you're instructing the assistant to aid in understanding images that you input. 
1. To start, select your GPT-4 Turbo with Vision deployment from the dropdown.
2. In the **Assistant setup** pane, provide a System Message to guide the assistant. The default System Message is: "You are an AI assistant that helps people find information." You can tailor the System Message to the image or scenario that you're uploading. 

   > [!NOTE]
    > It is recommended to update the System Message to be specific to the task in order to avoid unhelpful responses from the model.

1. Save your changes, and when prompted to confirm updating the system message, select **Continue**.
1. In the **Chat session** pane, enter a text prompt like "Describe this image," and upload an image with the attachment button. You can use a different text prompt for your use case. Then select **Send**. 
1. Observe the output provided. Consider asking follow-up questions related to the analysis of your image to learn more.

:::image type="content" source="../media/quickstarts/studio-vision.png" lightbox="../media/quickstarts/studio-vision.png" alt-text="Screenshot of OpenAI studio chat playground.":::


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)
