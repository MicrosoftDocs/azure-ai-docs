---
title: Azure OpenAI Graders for generative AI
titleSuffix: Microsoft Foundry
description: Learn about Azure OpenAI Graders for evaluating AI model outputs, including label grading, string checking, text similarity, and custom grading.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: mithigpe
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Azure OpenAI graders

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Azure OpenAI graders are a new set of evaluation tools in the Microsoft Foundry SDK that evaluate the performance of AI models and their outputs. These graders include:

::: moniker range="foundry-classic"

- [Label grader](#label-grader)
- [String checker](#string-checker)
- [Text similarity](#text-similarity)
- [Python grader](#python-grader)

::: moniker-end

::: moniker range="foundry"

| Name                  | Type             | What it does                                                                 |
|-----------------------|------------------|------------------------------------------------------------------------------|
| `label_grader`        | `label_model`   | Classifies sentiment as **positive**, **neutral**, or **negative** using an LLM. |
| `text_check_grader`   | `text_similarity`| Compares ground truth and response using BLEU score for similarity.          |
| `string_check_grader` | `string_check`  | Performs a string equality check between two values.                         |
| `score`               | `score_model`   | Assigns a similarity score (1–5) based on semantic and structural comparison. |

::: moniker-end

You can run graders locally or remotely. Each grader assesses specific aspects of AI models and their outputs.

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

## Model configuration for AI-assisted grader

The following code snippet shows the model configuration used by the AI-assisted grader:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    api_key=os.environ.get("AZURE_API_KEY"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION")
)
```

## Label grader

`AzureOpenAILabelGrader` uses your custom prompt to instruct a model to classify outputs based on labels you define. It returns structured results with explanations for why each label was chosen.

> [!NOTE]
> We recommend using Azure OpenAI o3-mini for the best results.

Here's an example of `data.jsonl` used in the following code snippets:

```json
[
    {
        "query": "What is the importance of choosing the right provider in getting the most value out of your health insurance plan?",
        "ground_truth": "Choosing an in-network provider helps you save money and ensures better, more personalized care. [Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Choosing the right provider is key to maximizing your health insurance benefits. In-network providers reduce costs, offer better coverage, and support continuity of care, leading to more effective and personalized treatment. [Northwind_Health_Plus_Benefits_Details.pdf][Northwind_Standard_Benefits_Details.pdf]"
    },
    {
        "query": "What should you do when choosing an in-network provider for your health care needs?",
        "ground_truth": "Check with Northwind Health Plus to confirm the provider is in-network, as this helps reduce costs.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "To choose an in-network provider, confirm they are part of your plan using the Northwind website or by calling their office. Also consider location, availability, and office hours. [Northwind_Standard_Benefits_Details.pdf]"
    },
    {
        "query": "What range of in-network providers does Northwind Health Plus offer?",
        "ground_truth": "Northwind Health Plus offers a wide range of in-network providers, including doctors, specialists, hospitals, and pharmacies.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Northwind Health Plus offers a wide range of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies [Northwind_Health_Plus_Benefits_Details.pdf]. The exact range of in-network providers may vary depending on the area, but the Northwind Health Plus website provides a searchable directory of all in-network providers in your area [Northwind_Health_Plus_Benefits_Details.pdf]. It is important to check with Northwind Health Plus to ensure that the provider you are considering is in-network [Northwind_Health_Plus_Benefits_Details.pdf]."
    },
    {
        "query": "What is the limitation of in-network providers?",
        "ground_truth": "The limitation of in-network providers is that they may not always be available in every area.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "The limitation of in-network providers is that they may not accept the amount of payment offered by Northwind Health, which means you may be responsible for a greater portion of the cost [Northwind_Standard_Benefits_Details.pdf]. Additionally, out-of-network providers may not offer additional services or discounts that are available to in-network providers [Northwind_Standard_Benefits_Details.pdf]. It is recommended to choose an in-network provider whenever possible to ensure the best value for your health care expenses [Northwind_Standard_Benefits_Details.pdf].\n\nSources:\n- Northwind_Standard_Benefits_Details.pdf"
    },
    {
        "query": "What resource does Northwind Health Plus provide to find in-network providers in your area?",
        "ground_truth": "The Northwind Health Plus website offers a searchable directory of all in-network providers in your area. This directory is regularly updated, so you can be sure that you are choosing from in-network providers that are available.\n[Northwind_Health_Plus_Benefits_Details-3.pdf]",
        "response": "Northwind Health Plus provides a variety of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies [Northwind_Health_Plus_Benefits_Details.pdf]."
    }
]
```

### Label grader example

```python
from azure.ai.evaluation import AzureOpenAILabelGrader, evaluate

data_file_name="data.jsonl"

#  Evaluation criteria: Determine if the response column contains text that is "too short," "just right," or "too long," and pass if it is "just right."
label_grader = AzureOpenAILabelGrader(
    model_config=model_config,
    input=[{"content": "{{item.response}}", "role": "user"},
           {"content": "Any text including space that's more than 600 characters is too long, less than 500 characters is too short; 500 to 600 characters is just right.", "role": "user", "type": "message"}],
    labels=["too short", "just right", "too long"],
    passing_labels=["just right"],
    model="gpt-4o",
    name="label",
)

label_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "label": label_grader
    },
)
```

### Label grader output

For each set of sample data in the data file, an evaluation result of `True` or `False` is returned, signifying if the output matches the defined passing label. The `score` is `1.0` for `True` cases, and `0.0` for `False` cases. The reason the model provided the label for the data is in `content` under `outputs.label.sample`.

```python
'outputs.label.sample':
...
...
    'output': [{'role': 'assistant',
      'content': '{"steps":[{"description":"Calculate the number of characters in the user\'s input including spaces.","conclusion":"The provided text contains 575 characters."},{"description":"Evaluate if the character count falls within the given ranges (greater than 600 too long, less than 500 too short, 500 to 600 just right).","conclusion":"The character count falls between 500 and 600, categorized as \'just right.\'"}],"result":"just right"}'}],
...
...
'outputs.label.passed': True,
'outputs.label.score': 1.0
```

In addition to individual data evaluation results, the grader returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'label.pass_rate': 0.2}, #1/5 in this case
```

## String checker

Compares input text to a reference value, checking for exact or partial matches with optional case insensitivity. Useful for flexible text validations and pattern matching.

### String checker example

```python
from azure.ai.evaluation import AzureOpenAIStringCheckGrader

# Evaluation criteria: Pass if the query column contains "What is"
string_grader = AzureOpenAIStringCheckGrader(
    model_config=model_config,
    input="{{item.query}}",
    name="starts with what is",
    operation="like", # "eq" for equal, "ne" for not equal, "like" for contains, "ilike" for case-insensitive contains
    reference="What is",
)

string_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "string": string_grader
    },
)
```

### String checker output

For each set of sample data in the data file, an evaluation result of `True` or `False` is returned, indicating whether the input text matches the defined pattern-matching rules. The `score` is `1.0` for `True` cases while `score` is `0.0` for `False` cases.

```python
'outputs.string.passed': True,
'outputs.string.score': 1.0
```

The grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'string.pass_rate': 0.4}, # 2/5 in this case
```

## Text similarity

Evaluates how closely input text matches a reference value using similarity metrics like `fuzzy_match`, `BLEU`, `ROUGE`, or `METEOR`. This is useful for assessing text quality or semantic closeness.

### Text similarity example

```python
from azure.ai.evaluation import AzureOpenAITextSimilarityGrader

# Evaluation criteria: Pass if response column and ground_truth column similarity score >= 0.5 using "fuzzy_match"
sim_grader = AzureOpenAITextSimilarityGrader(
    model_config=model_config,
    evaluation_metric="fuzzy_match", # support evaluation metrics including: "fuzzy_match", "bleu", "gleu", "meteor", "rouge_1", "rouge_2", "rouge_3", "rouge_4", "rouge_5", "rouge_l", "cosine",
    input="{{item.response}}",
    name="similarity",
    pass_threshold=0.5,
    reference="{{item.ground_truth}}",
)

sim_grader_evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "similarity": sim_grader
    },
)
sim_grader_evaluation
```

### Text similarity output

For each set of sample data in the data file, a numerical similarity score is generated. This score ranges from 0 to 1 and indicates the degree of similarity, with higher scores representing greater similarity. An evaluation result of `True` or `False` is also returned, signifying whether the similarity score meets or exceeds the specified threshold based on the evaluation metric defined in the grader.

```python
'outputs.similarity.passed': True,
'outputs.similarity.score': 0.6117136659436009
```

The grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'similarity.pass_rate': 0.4}, # 2 out of 5 in this case
```

## Python grader

Advanced users can create or import custom Python grader functions and integrate them into the Azure OpenAI Python grader. This enables evaluations tailored to specific areas of interest beyond the capabilities of the existing Azure OpenAI graders. The following example demonstrates how to import a custom similarity grader function and configure it to run as an Azure OpenAI Python grader using the Microsoft Foundry SDK.

### Python grader example

```python
from azure.ai.evaluation import AzureOpenAIPythonGrader
 
python_similarity_grader = AzureOpenAIPythonGrader(
    model_config=model_config_aoai,
    name="custom_similarity",
    image_tag="2025-05-08",
    pass_threshold=0.3,
    source="""
    def grade(sample, item) -> float:
     \"\"\"
     Custom similarity grader using word overlap.
     Note: All data is in the 'item' parameter.
     \"\"\"
     # Extract from item, not sample!
     response = item.get("response", "") if isinstance(item, dict) else ""
     ground_truth = item.get("ground_truth", "") if isinstance(item, dict) else ""
    
     # Simple word overlap similarity
     response_words = set(response.lower().split())
     truth_words = set(ground_truth.lower().split())
    
     if not truth_words:
     return 0.0
    
     overlap = response_words.intersection(truth_words)
     similarity = len(overlap) / len(truth_words)
    
     return min(1.0, similarity)
""",
)

file_name = "eval_this.jsonl"
evaluation = evaluate(
    data=data_file_name,
    evaluators={
        "custom_similarity": python_similarity_grader,
    },
    #azure_ai_project=azure_ai_project,
)
evaluation
```

### Output

For each set of sample data in the data file, the Python grader returns a numerical score based on the defined function. Given a numerical threshold defined as part of the custom grader, we also output `True` if the score >= threshold, or `False` otherwise.

For example:

```python
"outputs.custom_similarity.passed": false,
"outputs.custom_similarity.score": 0.0
```

Aside from individual data evaluation results, the grader also returns a metric indicating the overall dataset pass rate.

```python
'metrics': {'custom_similarity.pass_rate': 0.0}, #0/5 in this case
```

::: moniker-end

::: moniker range="foundry"

## Using Azure OpenAI graders

Azure OpenAI graders provide flexible evaluation using LLM-based or deterministic approaches:

- **Model-based graders** (`label_model`, `score_model`) - Use an LLM to evaluate outputs
- **Deterministic graders** (`string_check`, `text_similarity`) - Use algorithmic comparison

Examples:

- [Azure OpenAI graders sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_graders.py)

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

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

### String check grader

The string check grader (`string_check`) performs deterministic string comparisons. Use it for exact match validation where responses must match a reference exactly.

```python
{
    "type": "string_check",
    "name": "exact_match",
    "input": "{{item.response}}",
    "reference": "{{item.expected}}",
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
| `rouge_*` | N-gram overlap variants (`rouge_1`, `rouge_2`, ..., `rouge_l`) |

**Output:** Returns a similarity score as a float (higher means more similar). The grader passes if the score meets or exceeds `pass_threshold`.

### Example output

Graders return results with pass/fail status. The following snippet shows representative fields from the full output object:

```json
{
    "type": "score_model",
    "name": "quality_score",
    "score": 0.85,
    "passed": true
}
```

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [Complete working sample.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_graders.py#L9)
- [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)

::: moniker-end
