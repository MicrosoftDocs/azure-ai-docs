---
title: "General Purpose Evaluators for Generative AI"
description: "Learn about general-purpose evaluators for generative AI, including coherence, fluency, and question-answering composite evaluation."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 02/25/2026
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
---

# General purpose evaluators
AI systems might generate textual responses that are incoherent, or lack the general writing quality beyond minimum grammatical correctness. To address these issues, Microsoft Foundry supports evaluating coherence and fluency.

## Coherence

The coherence evaluator measures the logical and orderly presentation of ideas in a response, which allows the reader to easily follow and understand the writer's train of thought. A *coherent* response directly addresses the question with clear connections between sentences and paragraphs, using appropriate transitions and a logical sequence of ideas. Higher scores mean better coherence.

## Fluency

The fluency evaluator measures the effectiveness and clarity of written communication. This measure focuses on grammatical accuracy, vocabulary range, sentence complexity, coherence, and overall readability. It assesses how smoothly ideas are conveyed and how easily the reader can understand the text.

## Using general-purpose evaluators

General-purpose evaluators assess the quality of AI-generated text independent of specific use cases.

Examples:

- [Coherence sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_coherence.py)
- [Fluency sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_fluency.py)

| Evaluator | What it measures | Required inputs | Required parameters |
|-----------|------------------|-----------------|---------------------|
| `builtin.coherence` | Logical flow and organization of ideas | `query`, `response` | `deployment_name` |
| `builtin.fluency` | Grammatical accuracy and readability | `response` | `deployment_name` |

### Example input

Your test dataset should contain the fields referenced in your data mappings:

```jsonl
{"query": "What are the benefits of renewable energy?", "response": "Renewable energy reduces carbon emissions, lowers long-term costs, and provides energy independence."}
{"query": "How does photosynthesis work?", "response": "Plants convert sunlight, water, and carbon dioxide into glucose and oxygen through chlorophyll in their leaves."}
```

### Configuration example

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_text}}` references response text generated or retrieved during evaluation. Use this when evaluating with a model target or agent target.

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "fluency",
        "evaluator_name": "builtin.fluency",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {"response": "{{item.response}}"},
    },
]
```

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example output

These evaluators return scores on a 1-5 Likert scale (1 = very poor, 5 = excellent). The default pass threshold is 3. Scores at or above the threshold are considered passing. Key output fields:

```json
{
    "type": "azure_ai_evaluator",
    "name": "Coherence",
    "metric": "coherence",
    "score": 4,
    "label": "pass",
    "reason": "The response directly addresses the question with clear, logical connections between ideas.",
    "threshold": 3,
    "passed": true
}
```

## Related content

- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
