---
title: "Azure OpenAI Graders for generative AI"
description: "Learn about Azure OpenAI Graders for evaluating AI model outputs, including label grading, string checking, text similarity, and custom grading."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: dlozier
ms.date: 04/02/2026
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
---

# Azure OpenAI graders

Azure OpenAI graders are evaluation tools in the Microsoft Foundry SDK that assess the performance of AI models and their outputs using either LLM-based scoring or deterministic comparison. These graders include:

| Grader | What it measures | Required parameters | Output |
|--------|------------------|---------------------|--------|
| `label_model` | Classifies text into predefined categories | `model`, `name`, `input`, `labels`, `passing_labels` | Pass/Fail based on label |
| `score_model` | Assigns a numeric score based on criteria | `model`, `name`, `input` | 0-1 float |
| `string_check` | Exact or pattern string matching | `input`, `reference`, `operation` | Pass/Fail |
| `text_similarity` | Similarity between two text strings | `input`, `reference`, `evaluation_metric`, `pass_threshold` | 0-1 float |

You can run graders locally or remotely. Each grader assesses specific aspects of AI models and their outputs.

## Configure and run graders

Azure OpenAI graders use the OpenAI Evals API and are configured differently from [built-in evaluators](../built-in-evaluators.md), which use the `azure_ai_evaluator` type. Use graders when you need custom LLM-based classification or scoring with full control over the prompt, or when you need deterministic string or similarity checks without an LLM judge.

Azure OpenAI graders provide flexible evaluation using LLM-based or deterministic approaches:

- **Model-based graders** (`label_model`, `score_model`) - Use an LLM to evaluate outputs
- **Deterministic graders** (`string_check`, `text_similarity`) - Use algorithmic comparison

Examples:

- [Azure OpenAI graders sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_graders.py)

See [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example input

Your test dataset should contain the fields referenced in your grader configurations.

```jsonl
{"query": "What is the weather like today?", "response": "It's sunny and warm with clear skies.", "ground_truth": "Today is sunny with temperatures around 75°F."}
{"query": "Summarize the meeting notes.", "response": "The team discussed Q3 goals and assigned action items.", "ground_truth": "Meeting covered quarterly objectives and task assignments."}
```

### Label grader

The label grader (`label_model`) uses an LLM to classify text into predefined categories. Use it for sentiment analysis, content classification, or any multi-class labeling task.

```python
{
    "type": "label_model",
    "name": "sentiment_check",
    "model": model_deployment,
    "input": [
        {"role": "developer", "content": "Classify the sentiment as 'positive', 'neutral', or 'negative'"},
        {"role": "user", "content": "Statement: {{item.query}}"},
    ],
    "labels": ["positive", "neutral", "negative"],
    "passing_labels": ["positive", "neutral"],
}
```

**Output:** Returns the assigned label from your defined set. The grader passes if the label is in `passing_labels`.

### Score grader

The score grader (`score_model`) uses an LLM to assign a numeric score to model outputs, reflecting quality, correctness, or similarity to a reference. Use it for nuanced evaluation requiring reasoning.

```python
{
    "type": "score_model",
    "name": "quality_score",
    "model": model_deployment,
    "input": [
        {"role": "system", "content": "Rate the response quality from 0 to 1. 1 = perfect, 0 = completely wrong."},
        {"role": "user", "content": "Response: {{item.response}}\nGround Truth: {{item.ground_truth}}"},
    ],
    "pass_threshold": 0.7,
    "range": [0, 1]
}
```

**Output:** Returns a float score (for example, `0.85`). The grader passes if the score meets or exceeds `pass_threshold`.

> [!NOTE]
> `range` defaults to `[0, 1]` if omitted. `pass_threshold` is optional; if not set, the grader scores but doesn't produce a pass/fail result.

### String check grader

The string check grader (`string_check`) performs deterministic string comparisons. Use it for exact match validation where responses must match a reference exactly.

```python
{
    "type": "string_check",
    "name": "exact_match",
    "input": "{{item.response}}",
    "reference": "{{item.ground_truth}}",
    "operation": "eq",
}
```

**Operations:**

| Operation | Description |
|-----------|-------------|
| `eq` | Exact match (case-sensitive) |
| `ne` | Not equal |
| `like` | Pattern match with wildcards |
| `ilike` | Case-insensitive pattern match |

**Output:** Returns a score of `1` for match, `0` for no match.

### Text similarity grader

The text similarity grader (`text_similarity`) compares two text strings using similarity metrics. Use it for open-ended or paraphrase matching where exact match is too strict.

```python
{
    "type": "text_similarity",
    "name": "similarity_check",
    "input": "{{item.response}}",
    "reference": "{{item.ground_truth}}",
    "evaluation_metric": "bleu",
    "pass_threshold": 0.8,
}
```

**Metrics:**

| Metric | Description |
|--------|-------------|
| `fuzzy_match` | Approximate string matching using edit distance |
| `bleu` | N-gram overlap score, commonly used for translation |
| `gleu` | Google's variant of BLEU with sentence-level scoring |
| `meteor` | Alignment-based metric considering synonyms and paraphrases |
| `cosine` | Cosine similarity on vectorized text |
| `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | N-gram overlap variants (unigram through 5-gram and longest common subsequence) |

**Output:** Returns a similarity score as a float (higher means more similar). The grader passes if the score meets or exceeds `pass_threshold`.

### Example output

Graders return results with pass/fail status. Key output fields:

```json
{
    "type": "score_model",
    "name": "quality_score",
    "score": 0.85,
    "passed": true
}
```

## Related content

- [Azure OpenAI graders sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_graders.py)
- [How to run agent evaluation](../../observability/how-to/evaluate-agent.md)
- [How to run batch evaluation](../../how-to/develop/cloud-evaluation.md)
