---
title: "Tutorial: Getting started with DeepSeek-R1 reasoning model in Microsoft Foundry Models (temp)"
description: "Learn how to deploy and use DeepSeek-R1 reasoning model in Microsoft Foundry Models. Get step-by-step guidance, code examples, and best practices for AI reasoning. (temp)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: tutorial
ms.date: 01/15/2026
ms.author: mopeakande
author: msakande
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
#CustomerIntent: As a developer or data scientist, I want to learn how to deploy and use the DeepSeek-R1 reasoning model in Microsoft Foundry Models so that I can build applications that leverage advanced reasoning capabilities for complex problem-solving tasks.
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Microsoft Foundry Models (temp)

In this tutorial, you learn how to deploy and use a DeepSeek reasoning model in Microsoft Foundry. This tutorial uses [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek?cid=learnDocs) for illustration. However, the content also applies to the newer [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek?cid=learnDocs) reasoning model.

**What you'll accomplish:**

In this tutorial, you'll deploy the DeepSeek-R1 reasoning model, send inference requests programmatically using code, and parse the reasoning output to understand how the model arrives at its answers.

The steps you perform in this tutorial are:

* Create and configure the Azure resources to use DeepSeek-R1 in Foundry Models.
* Configure the model deployment.
* Use DeepSeek-R1 with the next generation v1 Azure OpenAI APIs to consume the model in code.

## Prerequisites

To complete this article, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can [upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) and create an Azure subscription in the process.

- Access to Microsoft Foundry with appropriate permissions to create and manage resources. Typically requires Contributor or Owner role on the resource group for creating resources and deploying models.

- Install the Azure OpenAI SDK for your programming language:
  - **Python**: `pip install openai azure-identity`
  - **.NET**: `dotnet add package Azure.Identity` and install the OpenAI package
  - **JavaScript**: `npm install openai @azure/identity`
  - **Java**: Add the Azure Identity package (see code examples for details)

DeepSeek-R1 is a reasoning model that generates explanations alongside answers—see [About reasoning models](#about-reasoning-models) for details.

## Create the resources

To create a Foundry project that supports deployment for DeepSeek-R1, follow these steps. You can also create the resources using [Azure CLI](../../quickstarts/get-started-code.md?pivots=programming-language-cli) or [infrastructure as code, with Bicep](../../quickstarts/get-started-code.md?pivots=programming-language-bicep).

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
1. The project you're working on appears in the upper-left corner.  
1. To create a new project, select the project name, then  **Create new project**.
1. Give your project a name and select **Create project**.

## Deploy the model

1. Add a model to your project. Select **Build** in the middle of the page, then **Model**.
1. Select **Deploy base model** to open the model catalog.
1. Find and select the **DeepSeek-R1** model tile to open its model card and select **Deploy**. You can select **Quick deploy** to use the defaults, or select **Customize deployment** to see and change the deployment settings.

When the deployment finishes, you land on its playground, where you can start to interact with the deployment.

If you prefer to explore the model interactively first, skip to [Use the model in the playground](#use-the-model-in-the-playground).

## Use the model in code

Use the Foundry Models endpoint and credentials to connect to the model.

1. Select the **Details** pane from the upper pane of the Playgrounds to see the deployment's details. Here, you can find the deployment's URI and API key. 
1. Get your resource name from the deployment's URI to use for inferencing the model via code. 

Use the next generation v1 Azure OpenAI APIs to consume the model in your code. These code examples use a secure, keyless authentication approach, Microsoft Entra ID, via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet).

The following code examples demonstrate how to:
1. Authenticate with Microsoft Entra ID using `DefaultAzureCredential`, which automatically attempts multiple authentication methods in sequence:

    1. **Environment variables** - Checks for service principal credentials in environment variables
    1. **Managed identity** - Uses managed identity if running in Azure (App Service, Functions, VM, etc.)
    1. **Azure CLI** - Falls back to Azure CLI credentials if you're authenticated locally
    1. **Other methods** - Continues through additional authentication methods as needed
    
    > [!TIP]
    > For local development, ensure you're authenticated with Azure CLI by running `az login`. For production deployments in Azure, configure managed identity for your application.

1. Create a chat completion client connected to your model deployment
1. Send a basic prompt to the DeepSeek-R1 model
1. Receive and display the response

**Expected output:** A JSON response containing the model's answer, reasoning process (within `<think>` tags), token usage statistics (prompt tokens, completion tokens, total tokens), and model information.

[!INCLUDE [code-create-chat-client-request](../../foundry-models/includes/code-create-chat-client-request.md)]

**API Reference:**
- [OpenAI Python client](https://github.com/openai/openai-python)
- [OpenAI JavaScript client](https://github.com/openai/openai-node)
- [OpenAI .NET client](https://github.com/openai/openai-dotnet)
- [DefaultAzureCredential class](/dotnet/api/azure.identity.defaultazurecredential)
- [Chat completions API reference](../../openai/latest.md#create-chat-completion)
- [Azure Identity library overview](/dotnet/api/overview/azure/identity-readme)

<!-- CLASSIC-ONLY: Reasoning might generate longer responses and consume a larger number of tokens. See the [rate limits](../quotas-limits.md) that apply to DeepSeek-R1 models. Consider having a retry strategy to handle rate limits. You can also [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits). -->

## About reasoning models

Reasoning models can reach higher levels of performance in domains like math, coding, science, strategy, and logistics. The way these models produce outputs is by explicitly using chain of thought to explore all possible paths before generating an answer. They verify their answers as they produce them, which helps to arrive at more accurate conclusions. As a result, reasoning models might require less context prompts in order to produce effective results. 

Reasoning models produce two types of content as outputs:

* Reasoning completions
* Output completions

Both of these completions count towards content generated from the model. Therefore, they contribute to the token limits and costs associated with the model. Some models, like `DeepSeek-R1`, might respond with the reasoning content. Others, like `o1`, output only the completions.

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
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start by recalling the general consensus from linguistic sources. I remember that the number often cited is around 7,000, but maybe I should check some reputable organizations.\n\nEthnologue is a well-known resource for language data, and I think they list about 7,000 languages. But wait, do they update their numbers? It might be around 7,100 or so. Also, the exact count can vary because some sources might categorize dialects differently or have more recent data. \n\nAnother thing to consider is language endangerment. Many languages are endangered, with some having only a few speakers left. Organizations like UNESCO track endangered languages, so mentioning that adds context. Also, the distribution isn't even. Some countries or regions have hundreds of languages, like Papua New Guinea with over 800, while others have just a few. \n\nA user might also wonder why the exact number is hard to pin down. It's because the distinction between a language and a dialect can be political or cultural. For example, Mandarin and Cantonese are considered dialects of Chinese by some, but they're mutually unintelligible, so others classify them as separate languages. Also, some regions are under-researched, making it hard to document all languages. \n\nI should also touch on language families. The 7,000 languages are grouped into families like Indo-European, Sino-Tibetan, Niger-Congo, etc. Maybe mention a few of the largest families. But wait, the question is just about the count, not the families. Still, it's good to provide a bit more context. \n\nI need to make sure the information is up-to-date. Let me think – recent estimates still hover around 7,000. However, languages are dying out rapidly, so the number decreases over time. Including that note about endangerment and language extinction rates could be helpful. For instance, it's often stated that a language dies every few weeks. \n\nAnother point is sign languages. Does the count include them? Ethnologue includes some, but not all sources might. If the user is including sign languages, that adds more to the count, but I think the 7,000 figure typically refers to spoken languages. For thoroughness, maybe mention that there are also over 300 sign languages. \n\nSummarizing, the answer should state around 7,000, mention Ethnologue's figure, explain why the exact number varies, touch on endangerment, and possibly note sign languages as a separate category. Also, a brief mention of Papua New Guinea as the most linguistically diverse country/region. \n\nWait, let me verify Ethnologue's current number. As of their latest edition (25th, 2022), they list 7,168 living languages. But I should check if that's the case. Some sources might round to 7,000. Also, SIL International publishes Ethnologue, so citing them as reference makes sense. \n\nOther sources, like Glottolog, might have a different count because they use different criteria. Glottolog might list around 7,000 as well, but exact numbers vary. It's important to highlight that the count isn't exact because of differing definitions and ongoing research. \n\nIn conclusion, the approximate number is 7,000, with Ethnologue being a key source, considerations of endangerment, and the challenges in counting due to dialect vs. language distinctions. I should make sure the answer is clear, acknowledges the variability, and provides key points succinctly.

Answer: The exact number of languages in the world is challenging to determine due to differences in definitions (e.g., distinguishing languages from dialects) and ongoing documentation efforts. However, widely cited estimates suggest there are approximately **7,000 languages** globally.
Model: DeepSeek-R1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```

**API Reference:**
- [Python re module documentation](https://docs.python.org/3/library/re.html)
- [ChatCompletion object reference](https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion.py)

[!INCLUDE [best-practices](../../foundry-models/includes/use-chat-reasoning/best-practices.md)]

### Parameters

Reasoning models support a subset of the standard chat completion parameters to maintain the integrity of their reasoning process.

**Supported parameters:**
- `max_tokens` - Maximum number of tokens to generate in the response
- `stop` - Sequences where the API stops generating tokens
- `stream` - Enable streaming responses
- `n` - Number of completions to generate
- `frequency_penalty` - Reduces repetition of token sequences

**Unsupported parameters** (reasoning models don't support these):
- `temperature` - Fixed to optimize reasoning quality
- `top_p` - Not configurable for reasoning models
- `presence_penalty` - Not available
- `repetition_penalty` - Use `frequency_penalty` instead

**Example using `max_tokens`:**

```python
response = client.chat.completions.create(
    model="DeepSeek-R1",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    max_tokens=1000  # Limit response length
)
```

For the complete list of supported parameters, see the [Chat completions API reference](../../openai/latest.md#create-chat-completion).

## Use the model in the playground

Use the model in the playground to get an idea of the model's capabilities.

As stated previously, immediately a model deployment is complete, you land on the model's playground, where you can start to interact with the deployment. For example, you can enter your prompts, such as "How many languages are in the world?" in the playground.

## What you learned

In this tutorial, you accomplished the following:

> [!div class="checklist"]
> * Created Foundry resources for hosting AI models
> * Deployed the DeepSeek-R1 reasoning model
> * Made authenticated API calls using Microsoft Entra ID
> * Sent inference requests and received reasoning outputs
> * Parsed reasoning content from model responses to understand the model's thought process

## Related content

- [How to generate chat completions with Foundry Models](../../openai/api-version-lifecycle.md)
<!-- CLASSIC-ONLY: - [Use chat reasoning models](../how-to/use-chat-reasoning.md) -->
<!-- CLASSIC-ONLY: - [Azure OpenAI supported programming languages](../../openai/supported-languages.md) -->

