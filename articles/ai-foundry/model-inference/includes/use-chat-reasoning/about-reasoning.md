---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/31/2025
ms.author: fasantia
author: santiagxf
---

## Reasoning models

Reasoning models can reach higher levels of performance in domains like math, coding, science, strategy, and logistics. The way these models produces outputs is by explicitly using chain of thought to explore all possible paths before generating an answer. They verify their answers as they produce them which helps them to arrive to better more accurate conclusions. This means that reasoning models may require less context in prompting in order to produce effective results. 

Such way of scaling model's performance is referred as *inference compute time* as it trades performance against higher latency and cost. It contrasts to other approaches that scale through *training compute time*. 

Reasoning models then produce two types of outputs:

> [!div class="checklist"]
> * Reasoning completions
> * Output completions

Both of these completions count towards content generated from the model and hence, towards the token limits and costs associated with the model. Some models may output the reasoning content, like `DeepSeek-R1`. Some others, like `o1`, only outputs the output piece of the completions.