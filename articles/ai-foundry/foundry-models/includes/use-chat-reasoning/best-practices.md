---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/31/2025
ms.author: fasantia
author: santiagxf
---

### Prompt reasoning models

When building prompts for reasoning models, take the following into consideration:

> [!div class="checklist"]
> * Use simple instructions and avoid using chain-of-thought techniques.
> * Built-in reasoning capabilities make simple zero-shot prompts as effective as more complex methods. 
> * When providing additional context or documents, like in RAG scenarios, including only the most relevant information may help preventing the model from over-complicating its response.
> * Reasoning models may support the use of system messages. However, they may not follow them as strictly as other non-reasoning models.
> * When creating multi-turn applications, consider only appending the final answer from the model, without it's reasoning content as explained at [Reasoning content](#reasoning-content) section.

Notice that reasoning models can take longer times to generate responses. They use long reasoning chains of thought that enabled deeper and more structured problem-solving. They also perform self-verification to cross-check its own answers and correct its own mistakes, showcasing emergent self-reflective behaviors.