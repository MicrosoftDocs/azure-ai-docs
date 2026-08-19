---
title: "How to use function calling with Microsoft Foundry Models"
description: "Learn how to use function calling with Foundry Models that support the Chat Completions API."
author: alvinashcraft #dereklegenzoff
ms.author: aashcraft #delegenz
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.custom:
  - devx-track-python
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 05/13/2026
manager: mcleans
ai-usage: ai-assisted
---

# How to use function calling with Microsoft Foundry Models

[!INCLUDE [function-calling 1](../includes/how-to-function-calling-1.md)]

## Function calling support

Function calling is supported by Foundry Models through the Chat Completions API or the Responses API. Support varies by model, API, deployment type, and model version.

To find a model that supports function calling, review the following catalogs:

- [Foundry Models sold by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Foundry Models from partners and community](../../foundry-models/concepts/models-from-partners.md)

In the model details, look for the following capabilities:

- **Chat Completions API** or **Responses API**, depending on the API you plan to use.
- **Functions** or **tools** for function calling support.
- **Parallel tool calling** if your application needs the model to request multiple function calls in one response.

This article shows how to implement function calling with the Chat Completions API. For the Responses API request and response format, see [Use the Azure OpenAI Responses API](./responses.md).

> [!NOTE]
> The `tool_choice` parameter is now supported with `o3-mini` and `o1`. For more information, see the [reasoning models guide](./reasoning.md).

> [!IMPORTANT]
> Tool and function descriptions are currently limited to 1,024 characters. We'll update this article if this limit is changed.

[!INCLUDE [function-calling 2](../includes/how-to-function-calling-2.md)]
