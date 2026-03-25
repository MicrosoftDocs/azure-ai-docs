---
title: "Tutorial: Get started with DeepSeek-R1 in Foundry Models (classic)"
description: "Learn how to deploy and use DeepSeek-R1 reasoning model in Microsoft Foundry Models. Get step-by-step guidance, code examples, and best practices for AI reasoning. (classic)"
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
ai-usage: ai-assisted
#CustomerIntent: As a developer or data scientist, I want to learn how to deploy and use the DeepSeek-R1 reasoning model in Microsoft Foundry Models so that I can build applications that leverage advanced reasoning capabilities for complex problem-solving tasks.
ROBOTS: NOINDEX, NOFOLLOW
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Microsoft Foundry Models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/tutorials/get-started-deepseek-r1.md)

[!INCLUDE [get-started-deepseek-r1 1](../../../foundry/foundry-models/includes/tutorials-get-started-deepseek-r1-1.md)]

## Create the resources

To create a Foundry project that supports deployment for DeepSeek-R1, follow these steps. You can also create the resources using [Azure CLI](../../quickstarts/get-started-code.md?pivots=programming-language-cli) or [infrastructure as code, with Bicep](../../quickstarts/get-started-code.md?pivots=programming-language-bicep).

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. On the landing page, go to the "Explore models and capabilities" section.

    :::image type="content" source="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png" alt-text="A screenshot of the homepage of the Foundry portal showing the model catalog section." lightbox="../media/quickstart-get-started-deepseek-r1/foundry-homepage-model-catalog-section.png":::

1. Use the search box on the screen to search for the **DeepSeek-R1** model and open its model card.

   Select **Use this model**. This action opens a wizard to create a Foundry project and resources for you to work in. You can keep the default name for the project or change it.

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
    | Foundry resource    | The resource enabling access to the flagship models in the Foundry model catalog. In this tutorial, a new account is created, but Foundry resources (formerly known as Azure AI Services resource) can be shared across multiple hubs and projects. Hubs use a connection to the resource to have access to the model deployments available there. To learn how you can create connections to Foundry resources to consume models, see [Connect your AI project](../how-to/configure-project-connection.md). |

1. Select **Create** to create the Foundry project alongside the other defaults. Wait until the project creation is complete. This process takes a few minutes.

## Deploy the model

1. When you create the project and resources, a deployment wizard opens. DeepSeek-R1 is available as a Foundry Model sold directly by Azure. You can review the pricing details for the model by selecting the DeepSeek tab on the [Foundry Models pricing page](https://azure.microsoft.com/pricing/details/ai-foundry-models/deepseek/).

1. Configure the deployment settings. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for requests to route to this particular model deployment. This setup lets you configure specific names for your models when you attach specific configurations.

    1. Foundry automatically selects the Foundry resource you created earlier with your project. Use the **Customize** option to change the connection based on your needs. DeepSeek-R1 is available under the **Global Standard** and **Global Provisioned** deployment types, which provide higher throughput and performance.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png" alt-text="Screenshot showing how to deploy the model." lightbox="../media/quickstart-get-started-deepseek-r1/deployment-wizard.png":::

1. Select **Deploy**.

1. When the deployment finishes, the deployment **Details** page opens. Now the new model is ready for use.

If you prefer to explore the model interactively first, skip to [Use the model in the playground](#use-the-model-in-the-playground).

## Use the model in code

Use the Foundry Models endpoint and credentials to connect to the model.

:::image type="content" source="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/quickstart-get-started-deepseek-r1/endpoint-target-and-key.png":::

Use the next generation v1 Azure OpenAI APIs to consume the model in your code. These code examples use a secure, keyless authentication approach, Microsoft Entra ID, via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet).

The following code examples demonstrate how to:
1. Authenticate with Microsoft Entra ID using `DefaultAzureCredential`, which automatically attempts multiple authentication methods (environment variables, managed identity, Azure CLI, and others). The exact order depends on the Azure Identity SDK version you're using.
    
    > [!TIP]
    > For local development, ensure you're authenticated with Azure CLI by running `az login`. For production deployments in Azure, configure managed identity for your application.

1. Create a chat completion client connected to your model deployment
1. Send a basic prompt to the DeepSeek-R1 model
1. Receive and display the response

**Expected output:** A JSON response containing the model's answer, reasoning process (within `<think>` tags), token usage statistics (prompt tokens, completion tokens, total tokens), and model information.

[!INCLUDE [code-create-chat-client-request](../../../foundry/foundry-models/includes/code-create-chat-client-request.md)]

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

[!INCLUDE [get-started-deepseek-r1 2](../../../foundry/foundry-models/includes/tutorials-get-started-deepseek-r1-2.md)]

## Use the model in the playground

Use the model in the playground to get an idea of the model's capabilities.

1. On the deployment details page, select **Open in playground** in the top bar. This action opens the chat playground.

1. In the **Deployment** drop down of the chat playground, the deployment you created is already automatically selected.

1. Configure the system prompt as needed.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground, configure the system message, and test it out." lightbox="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png":::

1. Enter your prompt and see the outputs.

1. Select **View code** to see details about how to access the model deployment programmatically.

[!INCLUDE [get-started-deepseek-r1 3](../../../foundry/foundry-models/includes/tutorials-get-started-deepseek-r1-3.md)]
