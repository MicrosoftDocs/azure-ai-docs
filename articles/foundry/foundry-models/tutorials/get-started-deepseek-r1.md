---
title: "Tutorial: Get started with DeepSeek-R1 in Foundry Models"
description: "Learn how to deploy and use DeepSeek-R1 reasoning model in Microsoft Foundry Models. Get step-by-step guidance, code examples, and best practices for AI reasoning."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: tutorial
ms.date: 02/17/2026
ms.author: mopeakande
author: msakande
ms.reviewer: rasavage
reviewer: rsavage2
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer or data scientist, I want to learn how to deploy and use the DeepSeek-R1 reasoning model in Microsoft Foundry Models so that I can build applications that leverage advanced reasoning capabilities for complex problem-solving tasks.
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Microsoft Foundry Models

[!INCLUDE [get-started-deepseek-r1 1](../includes/tutorials-get-started-deepseek-r1-1.md)]

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

When the deployment finishes, you land on its playground, where you can start to interact with the deployment. Confirm your deployment is ready by verifying the deployment status shows **Succeeded**. Note the **deployment name** and **endpoint URI** from the deployment details—you need both for the code section.

If you prefer to explore the model interactively first, skip to [Use the model in the playground](#use-the-model-in-the-playground).

## Use the model in code

Use the Foundry Models endpoint and credentials to connect to the model.

1. Select the **Details** pane from the upper pane of the Playgrounds to see the deployment's details. Here, you can find the deployment's URI and API key. 
1. Get your resource name from the deployment's URI to use for inferencing the model via code. 

Use the next generation v1 Azure OpenAI APIs to consume the model in your code. These code examples use a secure, keyless authentication approach, Microsoft Entra ID, via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet).

The following code examples demonstrate how to:
1. Authenticate with Microsoft Entra ID using `DefaultAzureCredential`, which automatically attempts multiple authentication methods (environment variables, managed identity, Azure CLI, and others). The exact order depends on the Azure Identity SDK version you're using.
    
    > [!TIP]
    > For local development, ensure you're authenticated with Azure CLI by running `az login`. For production deployments in Azure, configure managed identity for your application.

1. Create a chat completion client connected to your model deployment
1. Send a basic prompt to the DeepSeek-R1 model
1. Receive and display the response

**Expected output:** A JSON response containing the model's answer, reasoning process (within `<think>` tags), token usage statistics (prompt tokens, completion tokens, total tokens), and model information.

[!INCLUDE [code-create-chat-client-request](../../foundry-models/includes/code-create-chat-client-request.md)]

> [!TIP]
> After running the code, you should see a JSON response that includes `choices[0].message.content` with the model's answer. If the model generates reasoning, the response contains content wrapped in `<think>...</think>` tags followed by the final answer.

**API Reference:**
- [OpenAI Python client](https://github.com/openai/openai-python)
- [OpenAI JavaScript client](https://github.com/openai/openai-node)
- [OpenAI .NET client](https://github.com/openai/openai-dotnet)
- [DefaultAzureCredential class](/dotnet/api/azure.identity.defaultazurecredential)
- [Chat completions API reference](../../openai/latest.md#create-chat-completion)
- [Azure Identity library overview](/dotnet/api/overview/azure/identity-readme)

Reasoning might generate longer responses and consume a larger number of tokens. DeepSeek-R1 supports up to 5,000 requests per minute and 5,000,000 tokens per minute. See the [rate limits](../quotas-limits.md) that apply to DeepSeek-R1 models. Consider having a retry strategy to handle rate limits. You can also [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

[!INCLUDE [get-started-deepseek-r1 2](../includes/tutorials-get-started-deepseek-r1-2.md)]

## Use the model in the playground

Use the model in the playground to get an idea of the model's capabilities.

As soon as the deployment completes, you land on the model's playground, where you can start to interact with the deployment. For example, you can enter your prompts, such as "How many languages are in the world?" in the playground.

[!INCLUDE [get-started-deepseek-r1 3](../includes/tutorials-get-started-deepseek-r1-3.md)]
