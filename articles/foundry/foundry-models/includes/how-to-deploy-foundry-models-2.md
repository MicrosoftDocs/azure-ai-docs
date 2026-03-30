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

## Use the model with code

To run inference on the deployed model, see the following examples:

- To use the **Responses API with Foundry Models sold directly by Azure**, such as Microsoft AI, DeepSeek, and Grok models, see [How to generate text responses with Microsoft Foundry Models](../how-to/generate-responses.md).

- To use the **Responses API with OpenAI models**, see [Getting started with the responses API](../../openai/how-to/responses.md).

- To use the **Chat completions API with models sold by partners**, such as the Llama model deployed in this article, see [Model support for chat completions](../../openai/api-version-lifecycle.md#model-support).

## Regional availability and quota limits of a model

For Foundry Models, the default quota varies by model and region. Certain models might only be available in some regions. For more information on availability and quota limits, see [Azure OpenAI in Microsoft Foundry Models quotas and limits](../../openai/quotas-limits.md) and [Microsoft Foundry Models quotas and limits](../quotas-limits.md).

## Quota for deploying and running inference on a model

For Foundry Models, deploying and running inference consume quota that Azure assigns to your subscription on a per-region, per-model basis in units of Tokens-per-Minute (TPM). When you sign up for Foundry, you receive default quota for most of the available models. Then, you assign TPM to each deployment as you create it, which reduces the available quota for that model. You can continue to create deployments and assign them TPMs until you reach your quota limit.

When you reach your quota limit, you can only create new deployments of that model if you:

- Request more quota by submitting a [quota increase form](https://aka.ms/oai/stuquotarequest).
- Adjust the allocated quota on other model deployments in the Foundry portal, to free up tokens for new deployments.

For more information about quota, see [Microsoft Foundry Models quotas and limits](../quotas-limits.md) and [Manage Azure OpenAI quota](../../../foundry-classic/openai/how-to/quota.md?tabs=rest).

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Quota exceeded | [Request more quota](https://aka.ms/oai/stuquotarequest) or reallocate TPM from existing deployments. |
| Region not supported | Check [regional availability](../quotas-limits.md) and deploy in a supported region. |
| Marketplace subscription error | Verify you have the [required permissions](../how-to/configure-marketplace.md) to subscribe to Azure Marketplace offerings. |
| Deployment status shows **Failed** | Confirm that the model is available in your selected region and that you have sufficient quota. |

## Related content

- [How to generate text responses with Microsoft Foundry Models](../how-to/generate-responses.md)
- [Deployment types for Foundry Models](../concepts/deployment-types.md)
- [Deploy models using Azure CLI and Bicep](../how-to/create-model-deployments.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
