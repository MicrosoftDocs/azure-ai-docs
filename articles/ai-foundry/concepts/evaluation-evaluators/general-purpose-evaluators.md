---
title: General Purpose Evaluators for Generative AI
titleSuffix: Microsoft Foundry
description: Learn about general-purpose evaluators for generative AI, including coherence, fluency, and question-answering composite evaluation.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# General purpose evaluators

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

AI systems might generate textual responses that are incoherent, or lack the general writing quality beyond minimum grammatical correctness. To address these issues, Microsoft Foundry supports evaluating coherence and fluency.

::: moniker range="foundry-classic"

If you have a question-answering (QA) scenario with both `context` and `ground truth` data in addition to `query` and `response`, you can also use our [QAEvaluator](#question-answering-composite-evaluator), which is a composite evaluator that uses relevant evaluators for judgment.

## Model configuration for AI-assisted evaluators

For reference in the following code snippet, the AI-assisted evaluators use a model configuration as follows:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get("AZURE_API_KEY"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

### Evaluator model support

Foundry supports  AzureOpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and non-reasoning models for the large language model judge (LLM-judge) depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o, etc.) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other evaluators| Not Supported | Supported | -- |

For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `4.1-mini` with a balance of reasoning performance and cost efficiency.

::: moniker-end 


## Coherence

The coherence evaluator measures the logical and orderly presentation of ideas in a response, which allows the reader to easily follow and understand the writer's train of thought. A *coherent* response directly addresses the question with clear connections between sentences and paragraphs, using appropriate transitions and a logical sequence of ideas. Higher scores mean better coherence.

::: moniker range="foundry-classic"

### Coherence example

```python
from azure.ai.evaluation import CoherenceEvaluator

coherence = CoherenceEvaluator(model_config=model_config, threshold=3)
coherence(
    query="Is Marie Curie is born in Paris?", 
    response="No, Marie Curie is born in Warsaw."
)
```

### Coherence output

The numerical score on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), it also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
    "coherence": 4.0,
    "gpt_coherence": 4.0,
    "coherence_reason": "The RESPONSE is coherent and directly answers the QUERY with relevant information, making it easy to follow and understand.",
    "coherence_result": "pass",
    "coherence_threshold": 3
}
```

::: moniker-end

## Fluency

The fluency evaluator measures the effectiveness and clarity of written communication. This measure focuses on grammatical accuracy, vocabulary range, sentence complexity, coherence, and overall readability. It assesses how smoothly ideas are conveyed and how easily the reader can understand the text.

::: moniker range="foundry-classic"

### Fluency example

```python
from azure.ai.evaluation import FluencyEvaluator

fluency = FluencyEvaluator(model_config=model_config, threshold=3)
fluency(
    response="No, Marie Curie is born in Warsaw."
)
```

### Fluency output

The numerical score on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), it also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
    "fluency": 3.0,
    "gpt_fluency": 3.0,
    "fluency_reason": "The response is clear and grammatically correct, but it lacks complexity and variety in sentence structure, which is why it fits the \"Competent Fluency\" level.",
    "fluency_result": "pass",
    "fluency_threshold": 3
}
```

## Question answering composite evaluator

`QAEvaluator` measures comprehensively various aspects in a question-answering scenario:

- Relevance
- Groundedness
- Fluency
- Coherence
- Similarity
- F1 score

### QA example

```python
from azure.ai.evaluation import QAEvaluator

qa_eval = QAEvaluator(model_config=model_config, threshold=3)
qa_eval(
    query="Where was Marie Curie born?", 
    context="Background: 1. Marie Curie was a chemist. 2. Marie Curie was born on November 7, 1867. 3. Marie Curie is a French scientist.",
    response="According to wikipedia, Marie Curie was not born in Paris but in Warsaw.",
    ground_truth="Marie Curie was born in Warsaw."
)
```

### QA output

While F1 score outputs a numerical score on 0-1 float scale, the other evaluators output numerical scores on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), it also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
    "f1_score": 0.631578947368421,
    "f1_result": "pass",
    "f1_threshold": 3,
    "similarity": 4.0,
    "gpt_similarity": 4.0,
    "similarity_result": "pass",
    "similarity_threshold": 3,
    "fluency": 3.0,
    "gpt_fluency": 3.0,
    "fluency_reason": "The input Data should get a Score of 3 because it clearly conveys an idea with correct grammar and adequate vocabulary, but it lacks complexity and variety in sentence structure.",
    "fluency_result": "pass",
    "fluency_threshold": 3,
    "relevance": 3.0,
    "gpt_relevance": 3.0,
    "relevance_reason": "The RESPONSE does not fully answer the QUERY because it fails to explicitly state that Marie Curie was born in Warsaw, which is the key detail needed for a complete understanding. Instead, it only negates Paris, which does not fully address the question.",
    "relevance_result": "pass",
    "relevance_threshold": 3,
    "coherence": 2.0,
    "gpt_coherence": 2.0,
    "coherence_reason": "The RESPONSE provides some relevant information but lacks a clear and logical structure, making it difficult to follow. It does not directly answer the question in a coherent manner, which is why it falls into the \"Poorly Coherent Response\" category.",
    "coherence_result": "fail",
    "coherence_threshold": 3,
    "groundedness": 3.0,
    "gpt_groundedness": 3.0,
    "groundedness_reason": "The response attempts to answer the query about Marie Curie's birthplace but includes incorrect information by stating she was not born in Paris, which is irrelevant. It does provide the correct birthplace (Warsaw), but the misleading nature of the response affects its overall groundedness. Therefore, it deserves a score of 3.",
    "groundedness_result": "pass",
    "groundedness_threshold": 3
}
```

::: moniker-end 

::: moniker range="foundry"

## Using general-purpose evaluators

General-purpose evaluators assess the quality of AI-generated text independent of specific use cases.

Examples:

- [Coherence sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_coherence.py)
- [Fluency sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_fluency.py)

Configure them in your `testing_criteria`:

| Evaluator | What it measures | Required inputs | Required parameters |
|-----------|------------------|-----------------|---------------------|
| `builtin.coherence` | Logical flow and organization of ideas | `query`, `response` | `deployment_name` |
| `builtin.fluency` | Grammatical accuracy and readability | `response` | `deployment_name` |

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example input

Your test dataset should contain the fields referenced in your data mappings. For general-purpose evaluators, include `query` and `response` fields:

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

### Example output

These evaluators return scores on a 1-5 Likert scale (1 = very poor, 5 = excellent). The default pass threshold is 3. Scores at or above the threshold result in `passed: true`. Key output fields:

```json
{
    "type": "azure_ai_evaluator",
    "name": "coherence",
    "score": 4,
    "passed": true,
    "reason": "The response directly addresses the question with clear, logical connections between ideas."
}
```

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)

::: moniker-end
