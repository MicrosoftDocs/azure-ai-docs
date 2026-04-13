---
title: Include file
description: Include file
author: msakande
ms.reviewer: sgilley
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Azure OpenAI inference endpoint

The **Azure OpenAI API** exposes the full capabilities of OpenAI models and supports more features like assistants, threads, files, and batch inference. You might also access non-OpenAI models through this route.

Azure OpenAI endpoints, usually of the form `https://<resource-name>.openai.azure.com`, work at the deployment level and each deployment has its own associated URL. However, you can use the same authentication mechanism to consume the deployments. For more information, see the reference page for [Azure OpenAI API](../../openai/reference.md).

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that's formed by concatenating the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

[!INCLUDE [code-create-openai-client](code-create-openai-client.md)]

[!INCLUDE [code-create-openai-chat-completion](code-create-openai-chat-completion.md)]

For more information about how to use the **Azure OpenAI endpoint**, see [Azure OpenAI in Foundry Models documentation](../concepts/models-sold-directly-by-azure.md).

## Keyless authentication

Models deployed to Foundry Models in Foundry Tools support keyless authorization by using Microsoft Entra ID. Keyless authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. It makes keyless authorization a strong choice for organizations adopting secure and scalable identity management solutions.

To use keyless authentication, [configure your resource and grant access to users](../how-to/configure-entra-id.md) to perform inference. After you configure the resource and grant access, authenticate as follows:

[!INCLUDE [code-create-chat-client-entra](code-create-chat-client-entra.md)]
