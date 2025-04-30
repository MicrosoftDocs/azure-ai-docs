---
title: 'Quickstart: Use Azure OpenAI Service via Azure AI Foundry'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with Azure AI Foundry. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/26/2025
---

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource with a model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

## Go to the Azure AI Foundry

Navigate to the <a href="https://ai.azure.com/" target="_blank">Azure AI Foundry portal</a> and sign-in with credentials that have access to your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

## Playground

Start exploring Azure OpenAI capabilities with a no-code approach through the completions playground. It's simply a text box where you can submit a prompt to generate a completion. From this page, you can quickly iterate and experiment with the capabilities. 

:::image type="content" source="../media/quickstarts/playground-load-new.png" alt-text="Screenshot of the playground page of AI Foundry playground with sections highlighted." lightbox="../media/quickstarts/playground-load-new.png":::

You can select a deployment and choose from a few pre-loaded examples to get started. If your resource doesn't have a deployment, select **Create a deployment** and follow the instructions provided by the wizard. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

You can experiment with the configuration settings such as temperature and pre-response text to improve the performance of your task. You can read more about each parameter in the [REST API](../reference.md).

- Selecting the **Generate** button will send the entered text to the completions API and stream the results back to the text box.
- Select the **Undo** button to undo the prior generation call.
- Select the **Regenerate** button to complete an undo and generation call together.

Azure OpenAI also performs content moderation on the prompt inputs and generated outputs. The prompts or responses may be filtered if harmful content is detected. For more information, see the [content filter](../concepts/content-filter.md) article.

In the Completions playground you can also view Python and curl code samples pre-filled according to your selected settings. Just select **View code** next to the examples dropdown. You can write an application to complete the same task with the OpenAI Python SDK, curl, or other REST API client.

### Try text summarization

To use the Azure OpenAI for text summarization in the Completions playground, follow these steps:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. Select the subscription and OpenAI resource to work with. 
1. Select **Completions playground** on the landing page.
1. Select your deployment from the **Deployments** dropdown. If your resource doesn't have a deployment, select **Create a deployment** and then revisit this step.
1. Enter a prompt for the model.

    :::image type="content" source="../media/quickstarts/summarize-text-new.png" alt-text="Screenshot of the playground page of Azure AI Foundry with a text summarization example." lightbox="../media/quickstarts/summarize-text-new.png":::

1. Select `Generate`. Azure OpenAI will attempt to capture the context of text and rephrase it succinctly. You should get a result that resembles the following text:

The accuracy of the response can vary per model. The `gpt-35-turbo-instruct` based model in this example is well-suited to this type of summarization, though in general we recommend using the alternate chat completions API unless you have a particular use case that is particularly suited to the completions API.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to generate the best completion in our [How-to guide on completions](../how-to/completions.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
