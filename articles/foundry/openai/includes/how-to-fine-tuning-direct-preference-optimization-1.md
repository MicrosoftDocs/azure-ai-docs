---
title: Include file
description: Include file
author: ssalgadodev
ms.reviewer: sgilley
ms.author: ssalgado
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Direct preference optimization (DPO) is an alignment technique for large language models, used to adjust model weights based on human preferences. It differs from reinforcement learning from human feedback (RLHF) in that it does not require fitting a reward model and uses simpler binary data preferences for training. It is computationally lighter weight and faster than RLHF, while being equally effective at alignment.

## Why is DPO useful?

DPO is especially useful in scenarios where there's no clear-cut correct answer, and subjective elements like tone, style, or specific content preferences are important. This approach also enables the model to learn from both positive examples (what's considered correct or ideal) and negative examples (what's less desired or incorrect).

DPO makes it easier for you to generate high-quality training datasets. While many organizations struggle to generate sufficiently large datasets for supervised fine-tuning, they often have preference data already collected based on user logs, A/B tests, or smaller manual annotation efforts.

## Direct preference optimization dataset format

Direct preference optimization files have a different format than supervised fine-tuning. You provide a "conversation" containing the system message and the initial user message, and then "completions" with paired preference data. You can only provide two completions.

The dataset uses three top-level fields:

| Field | Required | Description |
|-------|----------|-------------|
| `input` | Yes | Contains the system message and initial user message |
| `preferred_output` | Yes | Must contain at least one assistant message (roles: assistant, tool only) |
| `non_preferred_output` | Yes | Must contain at least one assistant message (roles: assistant, tool only) |

```json
{  
  "input": {  
    "messages": [{"role": "system", "content": ...}],  
    "tools": [...],  
    "parallel_tool_calls": true  
  },  
  "preferred_output": [{"role": "assistant", "content": ...}],  
  "non_preferred_output": [{"role": "assistant", "content": ...}]  
}  
```

Training datasets must be in `jsonl` format:

```jsonl
{{"input": {"messages": [{"role": "system", "content": "You are a chatbot assistant. Given a user question with multiple choice answers, provide the correct answer."}, {"role": "user", "content": "Question: Janette conducts an investigation to see which foods make her feel more fatigued. She eats one of four different foods each day at the same time for four days and then records how she feels. She asks her friend Carmen to do the same investigation to see if she gets similar results. Which would make the investigation most difficult to replicate? Answer choices: A: measuring the amount of fatigue, B: making sure the same foods are eaten, C: recording observations in the same chart, D: making sure the foods are at the same temperature"}]}, "preferred_output": [{"role": "assistant", "content": "A: Measuring The Amount Of Fatigue"}], "non_preferred_output": [{"role": "assistant", "content": "D: making sure the foods are at the same temperature"}]}
}
```

## Direct preference optimization model support

The following models support direct preference optimization fine-tuning:

| Model | DPO support | Region availability |
|-------|-------------|---------------------|
| `gpt-4o-2024-08-06` | Yes | [See fine-tuning models](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models) |
| `gpt-4.1-2025-04-14` | Yes | [See fine-tuning models](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models) |
| `gpt-4.1-mini-2025-04-14` | Yes | [See fine-tuning models](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models) |

You can use preference fine-tuning with base models and with models already fine-tuned using supervised fine-tuning, as long as they're a supported model and version.
