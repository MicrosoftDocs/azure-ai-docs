---
title: "Tutorial: Getting started with DeepSeek-R1 reasoning model in Azure AI Foundry Models"
titleSuffix: Azure AI Foundry
description: Learn about the reasoning capabilities of DeepSeek-R1 in Azure AI Foundry Models.
manager: scottpolly
ms.service: azure-ai-model-inference
ms.topic: tutorial
ms.date: 06/26/2025
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Azure AI Foundry Models

In this tutorial, you learn:

* How to create and configure the Azure resources to use DeepSeek-R1 in Azure AI Foundry Models.
* How to configure the model deployment.
* How to use DeepSeek-R1 with the Azure AI Inference SDK or REST APIs.
* How to use DeepSeek-R1 with other SDKs.

## Prerequisites

To complete this article, you need:


* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI Foundry Models](../../model-inference/how-to/quickstart-github-models.md), if that applies to you.


[!INCLUDE [about-reasoning](../../foundry-models/includes/use-chat-reasoning/about-reasoning.md)]

## Create the resources


Foundry Models is a capability in Azure AI Foundry resources in Azure. You can create model deployments under the resource to consume their predictions. You can also connect the resource to Azure AI hubs and projects in Azure AI Foundry to create intelligent applications if needed.

To create an Azure AI project that supports deployment for DeepSeek-R1, follow these steps. You can also create the resources, using [Azure CLI](../how-to/quickstart-create-resources.md?pivots=programming-language-cli) or [infrastructure as code, with Bicep](../how-to/quickstart-create-resources.md?pivots=programming-language-bicep).


[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. Sign in to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Go to the preview features icon on the header of the landing page and make sure that the **Deploy models to Azure AI Foundry resources** feature is turned on.

    :::image type="content" source="../media/quickstart-get-started-deepseek-r1/enable-foundry-resource-deployment.png" alt-text="A screenshot showing the steps to enable deployment to a Foundry resource." lightbox="../media/quickstart-get-started-deepseek-r1/enable-foundry-resource-deployment.png":::

1. On the landing page, go to the "Explore models and capabilities" section and select **Go to full model catalog** to open the model catalog.
    :::image type="content" source="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png" alt-text="A screenshot of the homepage of the Foundry portal showing the model catalog section." lightbox="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png":::

1. Search for the **DeepSeek-R1** model and open its model card.
    
1. Select **Use this model**. This action opens up a wizard to create an Azure AI Foundry project and resources that you'll work in. You can keep the default name for the project or change it.

    > [!TIP]
    > **Are you using Azure OpenAI in Azure AI Foundry Models?** When you're connected to Azure AI Foundry portal using an Azure OpenAI resource, only Azure OpenAI models show up in the catalog. To view the full list of models, including DeepSeek-R1, use the top **Announcements** section and locate the card with the option **Explore more models**.
    >
    > :::image type="content" source="../media/quickstart-get-started-deepseek-r1/explore-more-models.png" alt-text="Screenshot showing the card with the option to explore all the models from the catalog." lightbox="../media/quickstart-get-started-deepseek-r1/explore-more-models.png":::
    >
    > A new window shows up with the full list of models. Select **DeepSeek-R1** from the list and select **Deploy**. The wizard asks to create a new project.

1. Select the dropdown in the "Advanced options" section of the wizard to see the details of other defaults created alongside the project. These defaults are selected for optimal functionality and include:

    | Property       | Description |
    | -------------- | ----------- |
    | Resource group | The main container for all the resources in Azure. This helps get resources that work together organized. It also helps to have a scope for the costs associated with the entire project. |
    | Region     | The region of the resources that you're creating. |
    | AI Foundry resource    | The resource enabling access to the flagship models in Azure AI model catalog. In this tutorial, a new account is created, but Azure AI Foundry resources (formerly known as Azure AI Services resource) can be shared across multiple hubs and projects. Hubs use a connection to the resource to have access to the model deployments available there. To learn how you can create connections to Azure AI Foundry resources to consume models, see [Connect your AI project](../../model-inference/how-to/configure-project-connection.md). |

1. Select **Create** to create the Foundry project alongside the other defaults. Wait until the project creation is complete. This process takes a few minutes.

## Deploy the model

1. Once the project and resources are created, a deployment wizard appears. DeepSeek-R1 is offered as a Microsoft first party consumption service. You can review our privacy and security commitments under [Data, privacy, and Security](../../../ai-studio/how-to/concept-data-privacy.md). 

1. Review the pricing details for the model by selecting the [Pricing and terms tab](https://aka.ms/DeepSeekPricing).

1. Select **Agree and Proceed** to continue with the deployment.

1. You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for requests to route to this particular model deployment. This allows you to also configure specific names for your models when you attach specific configurations.

1. Azure AI Foundry automatically selects the Foundry resource created earlier with your project. Use the **Customize** option to change the connection based on your needs. DeepSeek-R1 is currently offered under the **Global Standard** deployment type, which offers higher throughput and performance.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png" alt-text="Screenshot showing how to deploy the model." lightbox="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png":::

1. Select **Deploy**.

1. Once the deployment completes, the deployment **Details** page opens up. Now the new model is ready to be used.


## Use the model in the playground

You can get started by using the model in the playground to have an idea of the model's capabilities.

1. On the deployment details page, select **Open in playground** in the top bar. This action opens the chat playground.

2. In the **Deployment** drop down of the chat playground, the deployment you created is already automatically selected.

3. Configure the system prompt as needed. In general, reasoning models don't use system messages in the same way as other types of models.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground, configure the system message, and test it out." lightbox="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png":::

4. Type your prompt and see the outputs.

5. Additionally, you can use **View code** to see details about how to access the model deployment programmatically.

[!INCLUDE [best-practices](../../foundry-models/includes/use-chat-reasoning/best-practices.md)]

## Use the model in code

Use the Foundry Models endpoint and credentials to connect to the model:

:::image type="content" source="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png":::


You can use the Azure AI Model Inference package to consume the model in code:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

[!INCLUDE [code-chat-reasoning](../../foundry-models/includes/code-create-chat-reasoning.md)]

Reasoning might generate longer responses and consume a larger number of tokens. You can see the [rate limits](../../model-inference/quotas-limits.md) that apply to DeepSeek-R1 models. Consider having a retry strategy to handle rate limits being applied. You can also [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

### Reasoning content

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind it. The reasoning associated with the completion is included in the response's content within the tags `<think>` and `</think>`. The model might select the scenarios for which to generate reasoning content. The following example shows how to generate the reasoning content, using Python:

```python
import re

match = re.match(r"<think>(.*?)</think>(.*)", response.choices[0].message.content, re.DOTALL)

print("Response:", )
if match:
    print("\tThinking:", match.group(1))
    print("\tAnswer:", match.group(2))
else:
    print("\tAnswer:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
```

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start by recalling the general consensus from linguistic sources. I remember that the number often cited is around 7,000, but maybe I should check some reputable organizations.\n\nEthnologue is a well-known resource for language data, and I think they list about 7,000 languages. But wait, do they update their numbers? It might be around 7,100 or so. Also, the exact count can vary because some sources might categorize dialects differently or have more recent data. \n\nAnother thing to consider is language endangerment. Many languages are endangered, with some having only a few speakers left. Organizations like UNESCO track endangered languages, so mentioning that adds context. Also, the distribution isn't even. Some countries have hundreds of languages, like Papua New Guinea with over 800, while others have just a few. \n\nA user might also wonder why the exact number is hard to pin down. It's because the distinction between a language and a dialect can be political or cultural. For example, Mandarin and Cantonese are considered dialects of Chinese by some, but they're mutually unintelligible, so others classify them as separate languages. Also, some regions are under-researched, making it hard to document all languages. \n\nI should also touch on language families. The 7,000 languages are grouped into families like Indo-European, Sino-Tibetan, Niger-Congo, etc. Maybe mention a few of the largest families. But wait, the question is just about the count, not the families. Still, it's good to provide a bit more context. \n\nI need to make sure the information is up-to-date. Let me think – recent estimates still hover around 7,000. However, languages are dying out rapidly, so the number decreases over time. Including that note about endangerment and language extinction rates could be helpful. For instance, it's often stated that a language dies every few weeks. \n\nAnother point is sign languages. Does the count include them? Ethnologue includes some, but not all sources might. If the user is including sign languages, that adds more to the count, but I think the 7,000 figure typically refers to spoken languages. For thoroughness, maybe mention that there are also over 300 sign languages. \n\nSummarizing, the answer should state around 7,000, mention Ethnologue's figure, explain why the exact number varies, touch on endangerment, and possibly note sign languages as a separate category. Also, a brief mention of Papua New Guinea as the most linguistically diverse country. \n\nWait, let me verify Ethnologue's current number. As of their latest edition (25th, 2022), they list 7,168 living languages. But I should check if that's the case. Some sources might round to 7,000. Also, SIL International publishes Ethnologue, so citing them as reference makes sense. \n\nOther sources, like Glottolog, might have a different count because they use different criteria. Glottolog might list around 7,000 as well, but exact numbers vary. It's important to highlight that the count isn't exact because of differing definitions and ongoing research. \n\nIn conclusion, the approximate number is 7,000, with Ethnologue being a key source, considerations of endangerment, and the challenges in counting due to dialect vs. language distinctions. I should make sure the answer is clear, acknowledges the variability, and provides key points succinctly.

Answer: The exact number of languages in the world is challenging to determine due to differences in definitions (e.g., distinguishing languages from dialects) and ongoing documentation efforts. However, widely cited estimates suggest there are approximately **7,000 languages** globally.
Model: DeepSeek-R1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```


### Parameters

In general, reasoning models don't support the following parameters that you can find in chat completion models:

* Temperature
* Presence penalty
* Repetition penalty
* Parameter `top_p`

## Related content

* [Use chat reasoning models](../../model-inference/how-to/use-chat-reasoning.md)
* [Use image embedding models](../../model-inference/how-to/use-image-embeddings.md)
* [Model Inference API](../../model-inference/reference/reference-model-inference-api.md)
