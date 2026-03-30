---
title: Include file
description: Include file
author: msakande
ms.reviewer: rasavage
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Troubleshooting

If you encounter issues while following this tutorial, use the following guidance to resolve common problems.

### Authentication errors (401/403)

- **Ensure you're signed in to Azure CLI.** For local development, run `az login` before executing your code. `DefaultAzureCredential` uses your Azure CLI credentials as a fallback when no other credentials are available.
- **Verify role assignments.** Your Azure account needs the **Cognitive Services User** role (or higher) on the Foundry resource to make inference calls with Microsoft Entra ID. If you haven't assigned this role yet, see the Prerequisites section.
- **Check the endpoint format.** The endpoint URL must follow the format `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`. Verify the resource name matches your Foundry resource.

### Deployment issues

- **Deployment name vs. model name.** The `model` parameter in API calls refers to your **deployment name**, not the model name. If you customized the deployment name during creation, use that name instead of `DeepSeek-R1`.
- **Deployment not ready.** If you receive a 404 error, verify that the deployment status shows **Succeeded** in the Foundry portal before making API calls.

### Rate limiting (429 errors)

- **Implement retry logic.** Reasoning models generate longer responses that consume more tokens. Use exponential backoff to handle 429 (Too Many Requests) errors.
- **Monitor token usage.** DeepSeek-R1 reasoning content (within `<think>` tags) counts toward your token limit. See [quotas and limits](../quotas-limits.md) for the current rate limits.
- **Request quota increases.** If you consistently hit rate limits, [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

### Package installation issues

- **Python.** Install both required packages: `pip install openai azure-identity`. The `azure-identity` package is required for `DefaultAzureCredential`.
- **JavaScript.** Install both required packages: `npm install openai @azure/identity`.
- **.NET.** Install the Azure Identity package: `dotnet add package Azure.Identity`.

## What you learned

In this tutorial, you accomplished the following:

> [!div class="checklist"]
> * Created Foundry resources for hosting AI models
> * Deployed the DeepSeek-R1 reasoning model
> * Made authenticated API calls using Microsoft Entra ID
> * Sent inference requests and received reasoning outputs
> * Parsed reasoning content from model responses to understand the model's thought process

## Related content

- [Azure OpenAI in Microsoft Foundry Models v1 API](../../openai/api-version-lifecycle.md)
- [Use chat reasoning models](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Microsoft Foundry Models quotas and limits](../quotas-limits.md)
