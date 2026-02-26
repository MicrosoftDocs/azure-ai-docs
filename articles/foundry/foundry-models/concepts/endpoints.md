---
title: "Endpoints for Microsoft Foundry Models (temp)"
description: "Learn how to access and use Microsoft Foundry Models endpoints for secure model inference, flexible deployments, and keyless authentication. (temp)"
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 11/21/2025
ms.author: mopeakande
ms.custom:
  - build-2025
  - classic-and-new
ai-usage: ai-assisted

#CustomerIntent: As a developer using Microsoft Foundry Models, I want to understand how to access and use Foundry Model endpoints so that I can integrate models into my applications with secure authentication and flexible deployment options.
---

# Endpoints for Microsoft Foundry Models (temp)

Microsoft Foundry Models enables you to access the most powerful models from leading model providers through a single endpoint and set of credentials. This capability lets you switch between models and use them in your application without changing any code.

This article explains how the Foundry services organize models and how to use the inference endpoint to access them.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Deployments

Foundry uses **deployments** to make models available. **Deployments** give a model a name and set specific configurations. You can access a model by using its deployment name in your requests.

A deployment includes:

* A model name
* A model version
* A provisioning or capacity type<sup>1</sup>
* A content filtering configuration<sup>1</sup>
* A rate limiting configuration<sup>1</sup>

<sup>1</sup> These configurations can change depending on the selected model.

A Foundry resource can have many model deployments. You only pay for inference performed on model deployments. Deployments are Azure resources, so they're subject to Azure policies.

For more information about creating deployments, see [Add and configure model deployments](../how-to/create-model-deployments.md).

## Azure OpenAI inference endpoint

The **Azure OpenAI API** exposes the full capabilities of OpenAI models and supports more features like assistants, threads, files, and batch inference. You might also access non-OpenAI models through this route.

Azure OpenAI endpoints, usually of the form `https://<resource-name>.openai.azure.com`, work at the deployment level and each deployment has its own associated URL. However, you can use the same authentication mechanism to consume the deployments. For more information, see the reference page for [Azure OpenAI API](/azure/foundry-classic/openai/reference).

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that's formed by concatenating the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

[!INCLUDE [code-create-openai-client](../includes/code-create-openai-client.md)]

[!INCLUDE [code-create-openai-chat-completion](../includes/code-create-openai-chat-completion.md)]

For more information about how to use the **Azure OpenAI endpoint**, see [Azure OpenAI in Foundry Models documentation](models-sold-directly-by-azure.md).

## Keyless authentication

Models deployed to Foundry Models in Foundry Tools support keyless authorization by using Microsoft Entra ID. Keyless authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. It makes keyless authorization a strong choice for organizations adopting secure and scalable identity management solutions.

To use keyless authentication, [configure your resource and grant access to users](../how-to/configure-entra-id.md) to perform inference. After you configure the resource and grant access, authenticate as follows:

[!INCLUDE [code-create-chat-client-entra](../../foundry-models/includes/code-create-chat-client-entra.md)]

## Related content

- [Foundry Models and capabilities](./models-sold-directly-by-azure.md)
- [Deployment types in Foundry Models](deployment-types.md)
- [Model and region availability for Foundry Models](/azure/foundry-classic/how-to/deploy-models-serverless-availability)
- [What is Azure OpenAI in Foundry Models?](models-sold-directly-by-azure.md)

