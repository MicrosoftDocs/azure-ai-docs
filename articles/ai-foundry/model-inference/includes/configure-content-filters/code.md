---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
---

## Account for content filtering in your code

Once content filtering has been applied to your model deployment, requests can be intercepted by the service depending on the inputs and outputs. When a content filter is triggered, a 400 error code is returned with the description of the rule triggered.

[!INCLUDE [code-create-chat-client](../code-create-chat-client.md)]

[!INCLUDE [code-manage-content-filtering](../code-manage-content-filtering.md)]

## Follow best practices

We recommend informing your content filtering configuration decisions through an iterative identification (for example, red team testing, stress-testing, and analysis) and measurement process to address the potential harms that are relevant for a specific model, application, and deployment scenario. After you implement mitigations such as content filtering, repeat measurement to test effectiveness.

Recommendations and best practices for Responsible AI for Azure OpenAI, grounded in the [Microsoft Responsible AI Standard](https://aka.ms/RAI) can be found in the [Responsible AI Overview for Azure OpenAI](/legal/cognitive-services/openai/overview?context=/azure/ai-services/openai/context/context).