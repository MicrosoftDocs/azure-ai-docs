---
title: General purpose evaluators for generative AI
titleSuffix: Azure AI Foundry
description: Learn about general-purpose evaluators for generative AI, including coherence, fluency, and question-answering composite evaluation.
author: lgayhardt
ms.author: lagayhar
manager: scottpolly
ms.reviewer: changliu2
ms.date: 05/19/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# General purpose evaluators

AI systems might generate textual responses that are incoherent, or lack the general writing quality you might desire beyond minimum grammatical correctness. To address these issues, use [Coherence](#coherence) and [Fluency](#fluency).

If you have a question-answering (QA) scenario with both `context` and `ground truth` data in addition to `query` and `response`, you can also use our [QAEvaluator](#question-answering-composite-evaluator) a composite evaluator that uses relevant evaluators for judgment.

## Model configuration for AI-assisted evaluators

For reference in the following code snippet, the AI-assisted evaluators use a model configuration as follows:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get["AZURE_API_KEY"],
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

> [!TIP]
> We recommend using `o3-mini` for a balance of reasoning capability and cost efficiency.

## Coherence

`CoherenceEvaluator` measures the logical and orderly presentation of ideas in a response, allowing the reader to easily follow and understand the writer's train of thought. A coherent response directly addresses the question with clear connections between sentences and paragraphs, using appropriate transitions and a logical sequence of ideas. Higher scores mean better coherence.

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

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "coherence": 4.0,
    "gpt_coherence": 4.0,
    "coherence_reason": "The RESPONSE is coherent and directly answers the QUERY with relevant information, making it easy to follow and understand.",
    "coherence_result": "pass",
    "coherence_threshold": 3
}
```

## Fluency

`FluencyEvaluator`measures the effectiveness and clarity of written communication, focusing on grammatical accuracy, vocabulary range, sentence complexity, coherence, and overall readability. It assesses how smoothly ideas are conveyed and how easily the reader can understand the text.

### Fluency example

```python
from azure.ai.evaluation import FluencyEvaluator

fluency = FluencyEvaluator(model_config=model_config, threshold=3)
fluency(
    response="No, Marie Curie is born in Warsaw."
)
```

### Fluency output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

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

While F1 score outputs a numerical score on 0-1 float scale, the other evaluators output numerical scores on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

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

## Related content

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
