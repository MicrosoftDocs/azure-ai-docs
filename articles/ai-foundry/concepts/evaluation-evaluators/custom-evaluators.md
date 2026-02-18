---
title: Custom Evaluators
titleSuffix: Microsoft Foundry
description: Learn how to create custom evaluators for your AI applications using code-based or prompt-based approaches.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: mithigpe
ms.date: 02/17/2026
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
# customer intent: As a developer, I want to create custom evaluators so I can measure domain-specific quality metrics for my AI application's generations.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Custom evaluators

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Built-in evaluators provide an easy way to monitor the quality of your application's generations. To customize your evaluations, you can create your own code-based or prompt-based evaluators.

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

## Code-based evaluators

You don't need a large language model for certain evaluation metrics. Code-based evaluators give you the flexibility to define metrics based on functions or callable classes. You can build your own code-based evaluator, for example, by creating a simple Python class that calculates the length of an answer in `answer_length.py` under the directory `answer_len/`, as in the following example.

### Code-based evaluator example: Answer length

```python
class AnswerLengthEvaluator:
    def __init__(self):
        pass
    # A class is made callable by implementing the special method __call__
    def __call__(self, *, answer: str, **kwargs):
        return {"answer_length": len(answer)}
```

Run the evaluator on a row of data by importing a callable class:

```python
from answer_len.answer_length import AnswerLengthEvaluator

answer_length_evaluator = AnswerLengthEvaluator()
answer_length = answer_length_evaluator(answer="What is the speed of light?")
```

### Code-based evaluator output: Answer length

```python
{"answer_length":27}
```

## Prompt-based evaluators

To build your own prompt-based large language model evaluator or AI-assisted annotator, create a custom evaluator based on a *Prompty* file.

Prompty is a file with the `.prompty` extension for developing prompt templates. The Prompty asset is a markdown file with a modified front matter. The front matter is in YAML format. It contains metadata fields that define model configuration and expected inputs of the Prompty.

To measure the friendliness of a response, create a custom evaluator named `FriendlinessEvaluator`:

### Prompt-based evaluator example: Friendliness evaluator

First, create a `friendliness.prompty` file that defines the friendliness metric and its grading rubric:

```md
---
name: Friendliness Evaluator
description: Friendliness Evaluator to measure warmth and approachability of answers.
model:
  api: chat
  configuration:
    type: azure_openai
    azure_endpoint: ${env:AZURE_OPENAI_ENDPOINT}
    azure_deployment: gpt-4o-mini
  parameters:
    model:
    temperature: 0.1
inputs:
  response:
    type: string
outputs:
  score:
    type: int
  explanation:
    type: string
---

system:
Friendliness assesses the warmth and approachability of the answer. Rate the friendliness of the response between one to five stars using the following scale:

One star: the answer is unfriendly or hostile

Two stars: the answer is mostly unfriendly

Three stars: the answer is neutral

Four stars: the answer is mostly friendly

Five stars: the answer is very friendly

Please assign a rating between 1 and 5 based on the tone and demeanor of the response.

**Example 1**
generated_query: I just don't feel like helping you! Your questions are getting very annoying.
output:
{"score": 1, "reason": "The response is not warm and is resisting to be providing helpful information."}
**Example 2**
generated_query: I'm sorry this watch is not working for you. Very happy to assist you with a replacement.
output:
{"score": 5, "reason": "The response is warm and empathetic, offering a resolution with care."}


**Here the actual conversation to be scored:**
generated_query: {{response}}
output:
```

Then create a class `FriendlinessEvaluator` to load the Prompty file and process the outputs with JSON format:

```python
import os
import json
import sys
from promptflow.client import load_flow


class FriendlinessEvaluator:
    def __init__(self, model_config):
        current_dir = os.path.dirname(__file__)
        prompty_path = os.path.join(current_dir, "friendliness.prompty")
        self._flow = load_flow(source=prompty_path, model={"configuration": model_config})

    def __call__(self, *, response: str, **kwargs):
        llm_response = self._flow(response=response)
        try:
            response = json.loads(llm_response)
        except Exception as ex:
            response = llm_response
        return response
```

Now, create your own Prompty-based evaluator and run it on a row of data:

```python
from friendliness.friend import FriendlinessEvaluator

friendliness_eval = FriendlinessEvaluator(model_config)

friendliness_score = friendliness_eval(response="I will not apologize for my behavior!")
```

### Prompt-based evaluator output: Friendliness evaluator

```python
{
    'score': 1, 
    'reason': 'The response is hostile and unapologetic, lacking warmth or approachability.'
}
```

::: moniker-end

::: moniker range="foundry"

Custom evaluators let you define domain-specific quality metrics that go beyond the [built-in evaluator catalog](built-in-evaluators.md). Use a custom evaluator when you need to measure criteria unique to your application, such as brand tone, domain-specific accuracy, or output format compliance.

You can create two types of custom evaluators:

| | Code-based | Prompt-based |
|---|---|---|
| **How it works** | A Python `grade()` function scores each item with deterministic logic. | A judge prompt instructs an LLM to score each item. |
| **Best for** | Rule-based checks, keyword matching, format validation, length limits. | Subjective quality judgments, semantic similarity, tone analysis. |
| **Scoring method** | Continuous: float from 0.0 to 1.0 (higher is better). | Ordinal (1–5), continuous (0.0–1.0), or binary (pass/fail). Higher is better for numeric scores. |
| **Output contract** | A single float value. | A JSON object: `{"result": <int, float, or boolean>, "reason": "<explanation>"}` |

After you create a custom evaluator, you can register it to the evaluator catalog in your Foundry project and use it in [cloud evaluation runs](../../how-to/develop/cloud-evaluation.md).

## Code-based evaluators

A code-based evaluator is a Python function named `grade` that receives two parameters and returns a float score between 0.0 and 1.0 (higher is better):

- **`item`**: Contains your input data fields from the dataset (such as `query`, `response`, and `ground_truth`). Access fields with `item.get("field_name")`.
- **`sample`**: Contains fields from response generation when you run evaluations against a model or agent target (such as `output_text`). For dataset-only evaluations, `sample` is empty.

> [!NOTE]
> Due to a known issue, `sample` fields aren't directly accessible in the `grade()` function. As a workaround, map sample fields into the `item` namespace by using `{{item.sample.output_text}}` in your `data_mapping` configuration, then access them as `item.get("sample", {}).get("output_text")` in your code.

The following example checks whether a response contains harmful keywords and scores based on relevance to the query and similarity to the ground truth:

```python
def grade(sample: dict, item: dict) -> float:
    """Score response quality based on content safety and relevance."""
    response = item.get("response", "").lower()
    ground_truth = item.get("ground_truth", "").lower()
    query = item.get("query", "").lower()

    if not response:
        return 0.0

    # Flag harmful content
    harmful_keywords = ["harmful", "dangerous", "unsafe", "illegal"]
    if any(keyword in response for keyword in harmful_keywords):
        return 0.0

    # Check query relevance
    query_words = query.split()[:5]
    relevance = 0.7 if any(w in response for w in query_words) else 0.3

    # Check ground truth overlap
    if ground_truth:
        truth_words = set(ground_truth.split())
        overlap = len(truth_words & set(response.split())) / len(truth_words)
        similarity = min(1.0, overlap)
    else:
        similarity = 0.5

    return round((relevance * 0.4) + (similarity * 0.6), 2)
```

### Sandbox environment

Code-based evaluators run in a sandboxed Python environment with the following constraints:

- Code size must be less than 256 KB.
- Execution is limited to 2 minutes per grading call.
- No network access is available at runtime.
- Memory limit is 2 GB, disk limit is 1 GB, and CPU is limited to 2 cores.

The following third-party packages are available:

| Package | Version |
|---|---|
| `numpy` | 2.2.4 |
| `scipy` | 1.15.2 |
| `pandas` | 2.2.3 |
| `scikit-learn` | 1.6.1 |
| `rapidfuzz` | 3.10.1 |
| `sympy` | 1.13.3 |
| `jsonschema` | 4.23.0 |
| `pydantic` | 2.10.6 |
| `deepdiff` | 8.4.2 |
| `nltk` | 3.9.1 |
| `rouge-score` | 0.1.2 |
| `pyyaml` | 6.0.2 |

The NLTK corpora `punkt`, `stopwords`, `wordnet`, `omw-1.4`, and `names` are preloaded.

### Runtime parameters

Both `deployment_name` and `pass_threshold` are required as initialization parameters when you register a code-based evaluator. Code-based evaluators don't use the model deployment, but the parameter is currently required.

## Prompt-based evaluators

A prompt-based evaluator uses a judge prompt template that an LLM evaluates for each item. Template variables use double curly braces (for example, `{{query}}`) and map to your input data fields.

Prompt-based evaluators support three scoring methods:

- **Ordinal** (1–5): Integer scores on a discrete scale. Higher is better.
- **Continuous** (0.0–1.0): Float scores for fine-grained measurement. Higher is better.
- **Binary** (pass/fail): Boolean result for threshold-based checks.

The LLM must return a JSON object matching the output contract: `{"result": <int, float, or boolean>, "reason": "<explanation>"}`.

The following example prompt uses ordinal scoring (1–5) to evaluate how well a response is grounded in the provided ground truth:

```text
You are a Groundedness Evaluator.

Your task is to evaluate how well the given response is grounded in the provided ground truth.
Groundedness means the response's statements are factually supported by the ground truth.
Evaluate factual alignment only — ignore grammar, fluency, or completeness.

### Input:
Query:
{{query}}

Response:
{{response}}

Ground Truth:
{{ground_truth}}

### Scoring Scale (1-5):
5 - Fully grounded. All claims supported by ground truth.
4 - Mostly grounded. Minor unsupported details.
3 - Partially grounded. About half the claims supported.
2 - Mostly ungrounded. Only a few details supported.
1 - Not grounded. Almost all information unsupported.

### Output Format (JSON):
{
  "result": <integer from 1 to 5>,
  "reason": "<brief explanation for the score>"
}
```

### Runtime parameters

Both `deployment_name` and `threshold` are required as initialization parameters when you register a prompt-based evaluator.

## Register a custom evaluator with code

### Prerequisites and setup

Install the SDK and set up your client:

```bash
pip install "azure-ai-projects>=2.0.0b1" azure-identity openai
```

```python
import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import EvaluatorCategory, EvaluatorDefinitionType
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)

# Azure AI Project endpoint
# Example: https://<account_name>.services.ai.azure.com/api/projects/<project_name>
endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

# Model deployment name (required for prompt-based evaluators)
# Example: gpt-5-mini
model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "")

# Create the project client
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Get the OpenAI client for evaluation API
client = project_client.get_openai_client()
```

### Register a code-based evaluator

Pass the `grade()` function as a string in the `code_text` field. Define the `data_schema` to declare the input fields your function expects, and the `metrics` to describe the score your function returns. Code-based evaluators use the `continuous` metric type with a range of 0.0 to 1.0.

```python
code_evaluator = project_client.evaluators.create_version(
    name="response_quality_scorer",
    evaluator_version={
        "name": "response_quality_scorer",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Response Quality Scorer",
        "description": "Scores response quality based on content safety and ground truth relevance",
        "definition": {
            "type": EvaluatorDefinitionType.CODE,
            "code_text": (
                'def grade(sample: dict, item: dict) -> float:\n'
                '    """Score response quality based on content safety and relevance."""\n'
                '    response = item.get("response", "").lower()\n'
                '    ground_truth = item.get("ground_truth", "").lower()\n'
                '    query = item.get("query", "").lower()\n'
                '    if not response:\n'
                '        return 0.0\n'
                '    harmful_keywords = ["harmful", "dangerous", "unsafe", "illegal"]\n'
                '    if any(kw in response for kw in harmful_keywords):\n'
                '        return 0.0\n'
                '    query_words = query.split()[:5]\n'
                '    relevance = 0.7 if any(w in response for w in query_words) else 0.3\n'
                '    if ground_truth:\n'
                '        truth_words = set(ground_truth.split())\n'
                '        overlap = len(truth_words & set(response.split())) / len(truth_words)\n'
                '        similarity = min(1.0, overlap)\n'
                '    else:\n'
                '        similarity = 0.5\n'
                '    return round((relevance * 0.4) + (similarity * 0.6), 2)\n'
            ),
            "init_parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "pass_threshold": {"type": "number"},
                },
                "required": ["deployment_name", "pass_threshold"],
            },
            "metrics": {
                "result": {
                    "type": "continuous",
                    "desirable_direction": "increase",
                    "min_value": 0.0,
                    "max_value": 1.0,
                }
            },
            "data_schema": {
                "type": "object",
                "required": ["item"],
                "properties": {
                    "item": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "response": {"type": "string"},
                            "ground_truth": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
)
```

### Register a prompt-based evaluator

Pass the judge prompt in the `prompt_text` field. The `init_parameters` declare the model deployment and any thresholds the evaluator needs at runtime.

```python
prompt_evaluator = project_client.evaluators.create_version(
    name="groundedness_judge",
    evaluator_version={
        "name": "groundedness_judge",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Groundedness Judge",
        "description": "Evaluates how well a response is grounded in the provided ground truth",
        "definition": {
            "type": EvaluatorDefinitionType.PROMPT,
            "prompt_text": (
                "You are a Groundedness Evaluator.\n\n"
                "Your task is to evaluate how well the given response is grounded in the provided ground truth.\n"
                "Groundedness means the response's statements are factually supported by the ground truth.\n"
                "Evaluate factual alignment only — ignore grammar, fluency, or completeness.\n\n"
                "### Input:\n"
                "Query:\n{{query}}\n\n"
                "Response:\n{{response}}\n\n"
                "Ground Truth:\n{{ground_truth}}\n\n"
                "### Scoring Scale (1-5):\n"
                "5 - Fully grounded. All claims supported by ground truth.\n"
                "4 - Mostly grounded. Minor unsupported details.\n"
                "3 - Partially grounded. About half the claims supported.\n"
                "2 - Mostly ungrounded. Only a few details supported.\n"
                "1 - Not grounded. Almost all information unsupported.\n\n"
                "### Output Format (JSON):\n"
                '{\n  "result": <integer from 1 to 5>,\n  "reason": "<brief explanation for the score>"\n}\n'
            ),
            "init_parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "threshold": {"type": "number"},
                },
                "required": ["deployment_name", "threshold"],
            },
            "data_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "response": {"type": "string"},
                    "ground_truth": {"type": "string"},
                },
                "required": ["query", "response", "ground_truth"],
            },
            "metrics": {
                "custom_prompt": {
                    "type": "ordinal",
                    "desirable_direction": "increase",
                    "min_value": 1,
                    "max_value": 5,
                }
            },
        },
    },
)
```

## Run an evaluation with a custom evaluator

After you register a custom evaluator, use it in an evaluation run the same way you use a built-in evaluator. The following example uses the prompt-based `groundedness_judge` evaluator registered earlier, but the same pattern applies to code-based evaluators — just change the `evaluator_name` and `initialization_parameters`.

### Define and run the evaluation

```python
# Define the data schema
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "response": {"type": "string"},
            "ground_truth": {"type": "string"},
        },
        "required": ["query", "response", "ground_truth"],
    },
)

# Reference the custom evaluator in testing criteria
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "groundedness_judge",
        "evaluator_name": "groundedness_judge",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "ground_truth": "{{item.ground_truth}}",
        },
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "threshold": 3,
        },
    }
]

# Create the evaluation
eval_object = client.evals.create(
    name="custom-eval-groundedness-test",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Run the evaluation with inline data
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="groundedness-run-01",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileContent(
            type="file_content",
            content=[
                SourceFileContentContent(
                    item={
                        "query": "What is the largest city in France?",
                        "ground_truth": "The largest city in France is Paris.",
                        "response": "The largest city in France is Paris.",
                    }
                ),
                SourceFileContentContent(
                    item={
                        "query": "Explain quantum computing",
                        "ground_truth": "Quantum computing uses quantum mechanics principles like superposition and entanglement.",
                        "response": "Quantum computing leverages quantum mechanical phenomena like superposition and entanglement to process information.",
                    }
                ),
            ],
        ),
    ),
)
```

### Get results

Poll the evaluation run until it finishes, then retrieve the per-item results and report URL.

```python
while True:
    run = client.evals.runs.retrieve(run_id=eval_run.id, eval_id=eval_object.id)
    if run.status in ("completed", "failed"):
        break
    time.sleep(5)

# Get per-item results
output_items = list(
    client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id)
)

print(f"Status: {run.status}")
print(f"Report: {run.report_url}")
```

For more information on data source options, evaluator mappings, and advanced scenarios, see [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md).

## Create a custom evaluator in the portal

You can also create custom evaluators directly in the Azure AI Foundry portal without writing SDK code.

1. In your Foundry project, go to **Evaluation** > **Evaluator catalog**.
1. Select **Custom evaluator** > **Create**.
1. Choose the evaluator type: **Code-based** or **Prompt-based**.

### Code-based evaluator example

In the code editor, write a Python `grade()` function. The following example checks whether a response matches expected persona keywords:

```python
def grade(sample: dict, item: dict) -> float:
    """
    Check if model response aligns with persona keywords.
    Returns 1.0 if all keywords match, otherwise a proportional score.
    """
    response = item.get("response", "").lower()
    expected_keywords = item.get("expected_keywords", "").lower().split(",")
    if not expected_keywords or not expected_keywords[0]:
        return 0.0
    matches = sum(1 for kw in expected_keywords if kw.strip() in response)
    return round(matches / len(expected_keywords), 2)
```

### Prompt-based evaluator example

<!-- [TODO: Add portal-specific prompt evaluator details when available from user] -->

In the prompt editor, write a judge prompt that instructs the model how to score each item. Use template variables like `{{query}}` and `{{response}}` to reference your input data fields.

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md)
- [Built-in evaluators](built-in-evaluators.md)
- [Prompt-based evaluator sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_eval_catalog_prompt_based_evaluators.py)
- [Code-based evaluator sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_eval_catalog_code_based_evaluators.py)

::: moniker-end