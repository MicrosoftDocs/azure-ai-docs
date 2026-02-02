---
manager: nitinme
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 08/29/2025
ms.topic: include
---

## Account for content filtering in your code

When you apply content filtering to your model deployment, the service can intercept requests based on the inputs and outputs. If a content filter triggers, the service returns a 400 error code with a description of the rule that triggered the error.

[!INCLUDE [code-create-chat-client](../code-create-chat-client.md)]

[!INCLUDE [code-manage-content-filtering](../code-manage-content-filtering.md)]

## Follow best practices

To address potential harms that are relevant for a specific model, application, and deployment scenario, use an iterative identification process (such as red team testing, stress-testing, and analysis) and a measurement process to inform your content filtering configuration decisions. After you implement mitigations like content filtering, repeat measurement to test effectiveness.

For recommendations and best practices on Responsible AI for Azure OpenAI, grounded in the [Microsoft Responsible AI Standard](https://aka.ms/RAI), see the [Responsible AI Overview for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/overview).