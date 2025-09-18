---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
---

### Prompt reasoning models

When building prompts for reasoning models, take the following into consideration:

> [!div class="checklist"]
> * Use simple instructions and avoid using chain-of-thought techniques.
> * Built-in reasoning capabilities make simple zero-shot prompts as effective as more complex methods. 
> * When providing additional context or documents, like in RAG scenarios, including only the most relevant information might help prevent the model from over-complicating its response.
> * Reasoning models may support the use of system messages. However, they might not follow them as strictly as other non-reasoning models.
> * When creating multi-turn applications, consider appending only the final answer from the model, without it's reasoning content, as explained in the [Reasoning content](#reasoning-content) section.

Notice that reasoning models can take longer times to generate responses. They use long reasoning chains of thought that enable deeper and more structured problem-solving. They also perform self-verification to cross-check their answers and correct their mistakes, thereby showcasing emergent self-reflective behaviors.