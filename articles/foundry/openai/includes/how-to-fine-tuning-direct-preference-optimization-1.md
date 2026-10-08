---
title: Include file
description: Prepare training and validation datasets for preference fine-tuning.
author: ssalgadodev
ms.reviewer: sgilley
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
ai-usage: ai-assisted
---

<a id="direct-preference-optimization-dataset-format"></a>

## Prepare preference data

Start with the [Orca preference-pair sample dataset on GitHub](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Direct_Preference_Optimization/orca_dpo_pairs), or prepare your own data.

Save separate `training.jsonl` and `validation.jsonl` files, with one example per line. Each example contains an input and exactly two outputs:

| Field | Content |
| --- | --- |
| `input` | A `messages` array with the prompt. Optional `tools` and `parallel_tool_calls` also belong here. |
| `preferred_output` | The preferred response, including at least one assistant message. |
| `non_preferred_output` | The rejected response to the same input, including at least one assistant message. |

Output messages use the `assistant` or `tool` role. Both responses must answer the same prompt, and the preference must match your intended task.

```jsonl
{"input": {"messages": [{"role": "system", "content": "You are a chatbot assistant. Given a user question with multiple choice answers, provide the correct answer."}, {"role": "user", "content": "Question: Janette conducts an investigation to see which foods make her feel more fatigued. She eats one of four different foods each day at the same time for four days and then records how she feels. She asks her friend Carmen to do the same investigation to see if she gets similar results. Which would make the investigation most difficult to replicate? Answer choices: A: measuring the amount of fatigue, B: making sure the same foods are eaten, C: recording observations in the same chart, D: making sure the foods are at the same temperature"}]}, "preferred_output": [{"role": "assistant", "content": "A: measuring the amount of fatigue"}], "non_preferred_output": [{"role": "assistant", "content": "D: making sure the foods are at the same temperature"}]}
```

Reference: [DPO dataset examples](https://github.com/microsoft-foundry/fine-tuning/tree/main/Demos/DPO_Intel_Orca).

Keep validation and final test examples out of the training set. Check [supported models](../../fine-tuning/overview.md#supported-models) before using a base model or an SFT-fine-tuned model for DPO.
