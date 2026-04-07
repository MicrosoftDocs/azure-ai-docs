---
title: "How to use function calling with Azure OpenAI in Microsoft Foundry Models"
description: "Learn how to use function calling with OpenAI models."
author: mrbullwinkle #dereklegenzoff
ms.author: mbullwin #delegenz
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - devx-track-python
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 02/10/2026
manager: nitinme
ai-usage: ai-assisted
---

# How to use function calling with Azure OpenAI in Microsoft Foundry Models

[!INCLUDE [function-calling 1](../includes/how-to-function-calling-1.md)]

## Function calling support

### Parallel function calling

* `gpt-4` (`2024-04-09`)
* `gpt-4o` (`2024-05-13`)
* `gpt-4o` (`2024-08-06`)
* `gpt-4o` (`2024-11-20`)
* `gpt-4o-mini` (`2024-07-18`)
* `gpt-4.1` (`2025-04-14`)
* `gpt-4.1-mini` (`2025-04-14`)
* `gpt-5` (`2025-08-07`)
* `gpt-5-mini` (`2025-08-07`)
* `gpt-5-nano` (`2025-08-07`)
* `gpt-5-codex` (`2025-09-11`)
* `gpt-5.1` (`2025-11-13`)
* `gpt-5.1-chat` (`2025-11-13`)
* `gpt-5.1-codex` (`2025-11-13`)
* `gpt-5.1-codex-mini` (`2025-11-13`)
* `gpt-5.1-codex-max` (`2025-12-04`)
* `gpt-5.2` (`2025-12-11`)
* `gpt-5.2-chat` (`2025-12-11`)
* `gpt-5.2-codex` (`2026-01-14`)
* `gpt-5.2-chat` (`2026-02-10`)
* `gpt-5.3-codex` (`2026-02-24`)
* `gpt-5.3-chat` (`2026-03-03`)
* `gpt-5.4` (`2026-03-05`)
* `gpt-5.4` (`2026-03-05`)
* `gpt-5.4-mini` (`2026-03-17`)
* `gpt-5.4-nano` (`2026-03-17`)

Support for parallel function was first added in API version [`2023-12-01-preview`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2023-12-01-preview/inference.json)

### Basic function calling with tools

* All the models that support parallel function calling
* `gpt-5.4-pro` (`2026-03-05`)
* `gpt-5-pro` (`2025-10-06`)
* `codex-mini` (`2025-05-16`)
* `o3-pro` (`2025-06-10`)
* `o4-mini` (`2025-04-16`)
* `o3` (`2025-04-16`)
* `gpt-4.1-nano` (`2025-04-14`)
* `o3-mini` (`2025-01-31`)
* `o1` (`2024-12-17`)

> [!NOTE]
> The `tool_choice` parameter is now supported with `o3-mini` and `o1`. For more information, see the [reasoning models guide](./reasoning.md).

> [!IMPORTANT]
> Tool/function descriptions are currently limited to 1,024 characters with Azure OpenAI. We'll update this article if this limit is changed.

[!INCLUDE [function-calling 2](../includes/how-to-function-calling-2.md)]
