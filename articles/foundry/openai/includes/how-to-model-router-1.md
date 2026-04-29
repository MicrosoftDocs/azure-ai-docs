---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/10/2026
ms.custom: include, update-code1
---

## Test model router with Chat Completions and Foundry Responses SDKs

Call model router the same way you call any OpenAI chat model. Set the `model` parameter to the name of your model router deployment. You can use either the OpenAI Python SDK with the Chat Completions API or the Microsoft Foundry SDK with the Responses API.

> [!NOTE]
> Install the required packages before you run the samples:
> - **Chat Completions**: `pip install openai>=1.75.0`
> - **Foundry Responses**: `pip install azure-ai-projects>=2.0.0 azure-identity`

# [Chat Completions](#tab/chat-completions)

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions.py" id="chat_completion":::

# [Foundry Responses](#tab/foundry-responses)

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-foundry-responses.py" id="foundry_responses":::

---

> [!TIP]
> For the full runnable samples, see [Model Router samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/foundry-models/model-router) in the foundry-samples repository.

- Reference: [`AzureOpenAI` (OpenAI Python SDK)](https://pypi.org/project/openai/)
- Reference: [`AIProjectClient`](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient)
