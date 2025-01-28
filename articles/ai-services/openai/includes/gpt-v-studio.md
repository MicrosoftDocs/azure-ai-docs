---
title: 'Quickstart: Use images in chats with the Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Use this article to get started using Azure AI Foundry to deploy and use an image-capable model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions, ignite-2024
ms.date: 12/05/2024
---

Start using images in your AI chats with a no-code approach through Azure AI Foundry.

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- An Azure OpenAI Service resource. For more information about resource creation, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).

## Go to Azure AI Foundry

Browse to [Azure AI Foundry](https://ai.azure.com/) and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

Create a project or select an existing one. Navigate to the **Models + endpoints** option on the left, and select **Deploy model**. Choose an image-capable deployment by selecting model name: **gpt-4o** or **gpt-4o-mini**. For more information about model deployment, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).  

Select the new deployment and select **Open in playground**.

## Playground

From this page, you can quickly iterate and experiment with the model's capabilities. 

For general help with assistant setup, chat sessions, settings, and panels, refer to the [Chat quickstart](/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-studio). 


## Start a chat session to analyze images

In this chat session, you're instructing the assistant to aid in understanding images that you input. 
1. To start, make sure your image-capable deployment is selected in the **Deployment** dropdown.
2. In the **Setup** pane, provide a System Message to guide the assistant. The default System Message is: "You are an AI assistant that helps people find information." You can tailor the System Message to the image or scenario that you're uploading. 

   > [!NOTE]
    > We recommend you update the System Message to be specific to the task in order to avoid unhelpful responses from the model.

1. Save your changes, and when prompted to confirm updating the system message, select **Continue**.
1. In the **Chat session** pane, enter a text prompt like "Describe this image," and upload an image with the attachment button. You can use a different text prompt for your use case. Then select **Send**. 
1. Observe the output provided. Consider asking follow-up questions related to the analysis of your image to learn more.


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)
