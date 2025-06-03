---
title: 'Direct preference optimization'
titleSuffix: Azure OpenAI
description: Learn how to use direct preference optimization technique to fine-tune Azure OpenAI models.
manager: nitinme
ms.service: azure-ai-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 05/25/2025
author: mrbullwinkle
ms.author: mbullwin
---

# Direct preference optimization (preview)

Direct preference optimization (DPO) is an alignment technique for large language models, used to adjust model weights based on human preferences. It differs from reinforcement learning from human feedback (RLHF) in that it does not require fitting a reward model and uses simpler binary data preferences for training. It is computationally lighter weight and faster than RLHF, while being equally effective at alignment.

## Why is DPO useful?

DPO is especially useful in scenarios where there's no clear-cut correct answer, and subjective elements like tone, style, or specific content preferences are important. This approach also enables the model to learn from both positive examples (what's considered correct or ideal) and negative examples (what's less desired or incorrect).

DPO is believed to be a technique that will make it easier for customers to generate high-quality training data sets. While many customers struggle to generate sufficient large data sets for supervised fine-tuning, they often have preference data already collected based on user logs, A/B tests, or smaller manual annotation efforts.

## Direct preference optimization dataset format

Direct preference optimization files have a different format than supervised fine-tuning. Customers provide a "conversation" containing the system message and the initial user message, and then "completions" with paired preference data. Users can only provide two completions.

Three top-level fields: `input`, `preferred_output` and `non_preferred_output`

- Each element in the preferred_output/non_preferred_output must contain at least one assistant message
- Each element in the preferred_output/non_preferred_output can only have roles in (assistant, tool)

```json
{  
  "input": {  
    "messages": {"role": "system", "content": ...},  
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

- `gpt-4o-2024-08-06` supports direct preference optimization in its respective fine-tuning regions. Latest region availability is updated in the [models page](../concepts/models.md#fine-tuning-models)

Users can use preference fine tuning with base models as well as models that have already been fine-tuned using supervised fine-tuning as long as they are of a supported model/version.

## How to use direct preference optimization fine-tuning

   :::image type="content" border="true" source="/azure/ai-services/openai/media/fine-tuning/preference-optimization.gif" alt-text="GIF of preference optimization fine-tuning steps.":::

1. Prepare `jsonl` datasets in the [preference format](#direct-preference-optimization-dataset-format).
2. Select the model and then select the method of customization **Direct Preference Optimization**.
3. Upload datasets – training and validation. Preview as needed.
4. Select hyperparameters, defaults are recommended for initial experimentation.
5. Review the selections and create a fine tuning job.


## Next steps

- Explore the fine-tuning capabilities in the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../concepts/models.md#fine-tuning-models)
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)