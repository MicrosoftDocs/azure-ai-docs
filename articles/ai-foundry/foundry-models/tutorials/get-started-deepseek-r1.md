---
title: "Tutorial: Getting started with DeepSeek-R1 reasoning model in Microsoft Foundry Models"
titleSuffix: Microsoft Foundry
description: "Learn how to deploy and use DeepSeek-R1 reasoning model in Microsoft Foundry Models. Get step-by-step guidance, code examples, and best practices for AI reasoning."
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: tutorial
ms.date: 01/09/2026
ms.author: mopeakande
author: msakande
ai-usage: ai-assisted
#CustomerIntent: As a developer or data scientist, I want to learn how to deploy and use the DeepSeek-R1 reasoning model in Microsoft Foundry Models so that I can build applications that leverage advanced reasoning capabilities for complex problem-solving tasks.
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Microsoft Foundry Models

[!INCLUDE [version-banner](../../includes/version-banner.md)]

In this tutorial, you learn how to deploy and use a DeepSeek reasoning model in Microsoft Foundry. This tutorial uses [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek?cid=learnDocs) for illustration. However, the content also applies to the newer [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek?cid=learnDocs) reasoning model.

The steps you perform in this tutorial are:

* Create and configure the Azure resources to use DeepSeek-R1 in Foundry Models.
* Configure the model deployment.
* Use DeepSeek-R1 with the next generation v1 Azure OpenAI APIs to consume the model in code.


## Prerequisites

To complete this article, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](../../model-inference/how-to/quickstart-github-models.md) if that applies to you.


[!INCLUDE [about-reasoning](../../foundry-models/includes/use-chat-reasoning/about-reasoning.md)]

## Create the resources

To create a Foundry project that supports deployment for DeepSeek-R1, follow these steps. You can also create the resources using [Azure CLI](../how-to/quickstart-create-resources.md?pivots=programming-language-cli) or [infrastructure as code, with Bicep](../how-to/quickstart-create-resources.md?pivots=programming-language-bicep).

::: moniker range="foundry-classic"

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. On the landing page, go to the "Explore models and capabilities" section and select **Go to full model catalog** to open the model catalog.
    :::image type="content" source="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png" alt-text="A screenshot of the homepage of the Foundry portal showing the model catalog section." lightbox="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png":::

1. Search for the **DeepSeek-R1** model and open its model card.
    1. Select **Use this model**. This action opens a wizard to create a Foundry project and resources for you to work in. You can keep the default name for the project or change it.


    > [!TIP]
    > **Are you using Azure OpenAI in Foundry Models?** When you're connected to the Foundry portal using an Azure OpenAI resource, only Azure OpenAI models show up in the catalog. To view the full list of models, including DeepSeek-R1, use the top **Announcements** section and locate the card with the option **Explore more models**.
    >
    > :::image type="content" source="../media/quickstart-get-started-deepseek-r1/explore-more-models.png" alt-text="Screenshot showing the card with the option to explore all the models from the catalog." lightbox="../media/quickstart-get-started-deepseek-r1/explore-more-models.png":::
    >
    > A new window opens with the full list of models. Select **DeepSeek-R1** from the list and select **Deploy**. The wizard asks to create a new project.

1. Select the dropdown in the "Advanced options" section of the wizard to see details about settings and other defaults created alongside the project. These defaults are selected for optimal functionality and include:

    | Property       | Description |
    | -------------- | ----------- |
    | Resource group | The main container for all the resources in Azure. This container helps you organize resources that work together. It also helps you have a scope for the costs associated with the entire project. |
    | Region     | The region of the resources that you're creating. |
    | Foundry resource    | The resource enabling access to the flagship models in the Foundry model catalog. In this tutorial, a new account is created, but Foundry resources (formerly known as Azure AI Services resource) can be shared across multiple hubs and projects. Hubs use a connection to the resource to have access to the model deployments available there. To learn how you can create connections to Foundry resources to consume models, see [Connect your AI project](../../model-inference/how-to/configure-project-connection.md). |

1. Select **Create** to create the Foundry project alongside the other defaults. Wait until the project creation is complete. This process takes a few minutes.

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
1. The project you're working on appears in the upper-left corner.  
1. To create a new project, select the project name, then  **Create new project**.
1. Give your project a name and select **Create project**.

::: moniker-end

## Deploy the model

::: moniker range="foundry-classic"

1. When you create the project and resources, a deployment wizard opens. DeepSeek-R1 is available as a Foundry Model sold directly by Azure. You can review the pricing details for the model by selecting the DeepSeek tab on the [Foundry Models pricing page](https://azure.microsoft.com/pricing/details/ai-foundry-models/deepseek/).

1. Configure the deployment settings. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for requests to route to this particular model deployment. This setup lets you configure specific names for your models when you attach specific configurations.

1. Foundry automatically selects the Foundry resource you created earlier with your project. Use the **Customize** option to change the connection based on your needs. DeepSeek-R1 is currently available under the **Global Standard** deployment type, which provides higher throughput and performance.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png" alt-text="Screenshot showing how to deploy the model." lightbox="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png":::

1. Select **Deploy**.

1. When the deployment finishes, the deployment **Details** page opens. Now the new model is ready for use.

::: moniker-end

::: moniker range="foundry"

1. Add a model to your project. Select **Build** in the middle of the page, then **Model**.
1. Select **Deploy base model** to open the model catalog.
1. Find and select the **DeepSeek-R1** model tile to open its model card and select **Deploy**. You can select **Quick deploy** to use the defaults, or select **Customize deployment** to see and change the deployment settings.

When the deployment finishes, you land on its playground, where you can start to interact with the deployment.

::: moniker-end


## Use the model in the playground

Get started by using the model in the playground to get an idea of the model's capabilities.

::: moniker range="foundry-classic"

1. On the deployment details page, select **Open in playground** in the top bar. This action opens the chat playground.

1. In the **Deployment** drop down of the chat playground, the deployment you created is already automatically selected.

1. Configure the system prompt as needed. In general, reasoning models don't use system messages in the same way as other types of models.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground, configure the system message, and test it out." lightbox="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png":::

1. Enter your prompt and see the outputs.

1. Select **View code** to see details about how to access the model deployment programmatically.

::: moniker-end

::: moniker range="foundry"

1. Enter your prompts, such as "How many languages are in the world?" in the playground.

::: moniker-end

[!INCLUDE [best-practices](../../foundry-models/includes/use-chat-reasoning/best-practices.md)]

## Use the model in code

Use the Foundry Models endpoint and credentials to connect to the model.

::: moniker range="foundry-classic"

:::image type="content" source="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png":::

::: moniker-end

::: moniker range="foundry"

1. Select the **Details** pane from the upper pane of the Playgrounds to see the deployment's details. Here, you can find the deployment's URI and API key. 
1. Get your resource name from the deployment's URI to use for inferencing the model via code. 

::: moniker-end

Use the next generation v1 Azure OpenAI APIs to consume the model in your code. These code examples use a secure, keyless authentication approach, Microsoft Entra ID, via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true).

[!INCLUDE [code-create-chat-client-request](../../foundry-models/includes/code-create-chat-client-request.md)]

Reasoning might generate longer responses and consume a larger number of tokens. See the [rate limits](../../model-inference/quotas-limits.md) that apply to DeepSeek-R1 models. Consider having a retry strategy to handle rate limits. You can also [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

### Reasoning content

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The reasoning associated with the completion is included in the response's content within the tags `<think>` and `</think>`. The model can select the scenarios for which to generate reasoning content. The following example shows how to generate the reasoning content, using Python:

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

In general, reasoning models don't support the following parameters that you find in chat completion models:

- Temperature
- Presence penalty
- Repetition penalty
- Parameter `top_p`

## Related content

- [How to generate chat completions with Foundry Models](../how-to/use-chat-completions.md)
- [Use chat reasoning models](../../model-inference/how-to/use-chat-reasoning.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)

