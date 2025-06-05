---
title: 'Quickstart: Use GPT-4o and GPT-4o mini via Azure AI Foundry'
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with Azure AI Foundry. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 09/19/2024
---

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true).
- An Azure OpenAI in Azure AI Foundry Models resource with either `gpt-4o` or the `gpt-4o-mini` models deployed. We recommend using standard or global standard model [deployment types](../how-to/deployment-types.md) for initial exploration. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

## Go to Azure AI Foundry

Navigate to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and sign-in with credentials that have access to your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

From Azure AI Foundry, select **Chat playground**.

## Playground

Start exploring Azure OpenAI capabilities with a no-code approach through the Azure AI Foundry Chat playground. From this page, you can quickly iterate and experiment with the capabilities.

:::image type="content" source="../media/quickstarts/chatgpt-playground-load-new.png" alt-text="Screenshot of the Chat playground page." lightbox="../media/quickstarts/chatgpt-playground-load-new.png":::

### Setup

You can use the **Prompt samples* dropdown to select a few pre-loaded **System message** examples to get started.

**System messages** give the model instructions about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses.

At any time while using the Chat playground you can select **View code** to see Python, curl, and json code samples pre-populated based on your current chat session and settings selections. You can then take this code and write an application to complete the same task you're currently performing with the playground.

### Chat session

Selecting the **Enter** button or selecting the right arrow icon sends the entered text to the chat completions API and the results are returned back to the text box.

Select the **Clear chat** button to delete the current conversation history.

### Key settings

| **Name**            | **Description**   |
|:--------------------|:-------------------------------------------------------------------------------|
| Deployments         | Your deployment name that is associated with a specific model. |
| Add your data | 
| Parameters | Custom parameters that alter the model responses. When you are starting out we recommend to use the defaults for most parameters |
| Temperature         | Controls randomness. Lowering the temperature means that the model produces more repetitive and deterministic responses. Increasing the temperature results in more unexpected or creative responses. Try adjusting temperature or Top P but not both. |
| Max response (tokens) | Set a limit on the number of tokens per model response. The API on the latest models supports a maximum of 128,000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly four characters for typical English text.|
| Top p   | Similar to temperature, this controls randomness but uses a different method. Lowering Top P narrows the model’s token selection to likelier tokens. Increasing Top P lets the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.|
| Stop sequences      | Stop sequence make the model end its response at a desired point. The model response ends before the specified sequence, so it won't contain the stop sequence text. For GPT-35-Turbo, using `<|im_end|>` ensures that the model response doesn't generate a follow-up user query. You can include as many as four stop sequences.|

## View code

Once you have experimented with chatting with the model select the **</> View Code** button. This will give you a replay of the code behind your entire conversation so far:

:::image type="content" source="../media/quickstarts/chat-view-code.png" alt-text="Screenshot of view code experience." lightbox="../media/quickstarts/chat-view-code.png":::

### Understanding the prompt structure

If you examine the sample from **View code** you'll notice that the conversation is broken into three distinct roles `system`, `user`, `assistant`. Each time you message the model the entire conversation history up to that point is resent. When using the chat completions API the model has no true memory of what you have sent to it in the past so you provide the conversation history for context to allow the model to respond properly.

The [Chat completions how-to guide](../how-to/chatgpt.md) provides an in-depth introduction into the new prompt structure and how to use chat completions models effectively.

[!INCLUDE [deploy-web-app](deploy-web-app.md)]

## Clean up resources

Once you're done testing out the Chat playground, if you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to work with the new `gpt-35-turbo` model with the [GPT-35-Turbo & GPT-4 how-to guide](../how-to/chatgpt.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
