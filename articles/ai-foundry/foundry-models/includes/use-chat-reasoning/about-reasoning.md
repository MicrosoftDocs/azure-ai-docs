---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 01/09/2026
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
---

## Reasoning models

Reasoning models can reach higher levels of performance in domains like math, coding, science, strategy, and logistics. The way these models produce outputs is by explicitly using chain of thought to explore all possible paths before generating an answer. They verify their answers as they produce them, which helps to arrive at more accurate conclusions. As a result, reasoning models might require less context prompts in order to produce effective results. 

Reasoning models produce two types of content as outputs:

* Reasoning completions
* Output completions

Both of these completions count towards content generated from the model. Therefore, they contribute to the token limits and costs associated with the model. Some models, like `DeepSeek-R1`, might respond with the reasoning content. Others, like `o1`, output only the completions.