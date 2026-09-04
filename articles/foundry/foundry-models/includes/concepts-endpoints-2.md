---
title: Include file
description: Include file
author: msakande
ms.author: mopeakande
reviewer: achandmsft
ms.reviewer: achand
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/31/2026
ms.custom: include
ai-usage: ai-assisted
---

## Azure OpenAI inference endpoint

The **Azure OpenAI API** exposes the full capabilities of OpenAI models and supports more features like assistants, threads, files, and batch inference. You can also use it to access non-OpenAI models.

Azure OpenAI endpoints are formatted as `https://<resource-name>.openai.azure.com`. Endpoints map to deployments, and each deployment has its own associated URL. However, you can use the same authentication mechanism to consume more than one deployment. For more information, see the reference page for [Azure OpenAI API](/rest/api/microsoft-foundry/azureopenai/responses).

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Deployment URLs are formed by concatenating the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`. When you use the OpenAI v1 API, call the `/openai/v1/` route on the base URL, `https://<resource-name>.openai.azure.com/openai/v1/`, and pass the deployment name in the `model` field of your request. The `/openai/v1/` route uses implicit versioning, so you don't pass an `api-version`.

The following examples use the [Responses API](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true), which supports the latest inference features.

> [!NOTE]
> The Responses API works with Azure OpenAI models and with [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md) that support it, such as DeepSeek, Llama, and Grok models. If a deployment doesn't support the Responses API, the request returns `400 Model not supported`. In that case, use the Chat Completions API by calling `client.chat.completions.create` instead.

### Use API key authentication

You can authenticate inference requests with an API key from your Foundry resource. API keys are quick to set up, but they grant full access to the resource, are hard to scope to specific users or actions, and require manual rotation to stay secure. For production workloads, use [keyless authentication](#use-keyless-authentication) with Microsoft Entra ID instead.

In the following example, `deepseek-v3-0324` is the name of a model deployment in the Microsoft Foundry resource. Replace it with your own deployment name, and store your API key in the `AZURE_INFERENCE_CREDENTIAL` environment variable.

[!INCLUDE [code-create-openai-client](code-create-openai-client.md)]

For more information about how to use the **Azure OpenAI endpoint**, see [Azure OpenAI SDK language support](../../openai/supported-languages.md).

### Use keyless authentication

Deployed Foundry Models support keyless authorization with Microsoft Entra ID. Keyless authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support. Use keyless authorization if your organization uses secure and scalable identity management solutions.

To use keyless authentication, [configure your resource and grant access to users](../how-to/configure-entra-id.md) to perform inference. After you configure the resource and grant access, authenticate as follows:

[!INCLUDE [code-create-chat-client-entra](code-create-chat-client-entra.md)]
