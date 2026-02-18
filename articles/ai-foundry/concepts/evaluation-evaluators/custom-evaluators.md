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

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

Built-in evaluators provide an easy way to monitor the quality of your application's generations. To customize your evaluations, you can create your own code-based or prompt-based evaluators.

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

Custom evaluators let you define domain-specific quality metrics that go beyond the [built-in evaluator catalog](../built-in-evaluators.md). Use a custom evaluator when you need to measure criteria unique to your application, such as brand tone, domain-specific accuracy, or output format compliance.

You can create two types of custom evaluators:

| | Code-based | Prompt-based |
|---|---|---|
| **How it works** | A Python `grade()` function scores each item with deterministic logic. | A judge prompt instructs an LLM to score each item. |
| **Best for** | Rule-based checks, keyword matching, format validation, length limits. | Subjective quality judgments, semantic similarity, tone analysis. |
| **Scoring method** | Continuous: float from 0.0 to 1.0 (higher is better). | Ordinal, continuous, or binary. You define the min/max range for ordinal and continuous scores. Higher is better for numeric scores. |
| **Output contract** | A single float value between 0.0 and 1.0. | A JSON object with `result` and `reason`. The type of `result` depends on the scoring method: integer for ordinal, float for continuous, or boolean for binary. |

After you create a custom evaluator, you can add it to the evaluator catalog in your Foundry project and use it in [cloud evaluation runs](../../how-to/develop/cloud-evaluation.md).

## Code-based evaluators

A code-based evaluator is a Python function named `grade` that receives two dict parameters (`sample` and `item`) and returns a float score between 0.0 and 1.0 (higher is better). In practice, all data is accessed through `item`:

- **Dataset evaluation**: Input fields like `response` or `ground_truth` can be retrieved in the Python code like `item.get("response")` or `item.get("ground_truth")`.
- **Model or agent target evaluation**: To fetch generated response text, use `item.get("sample", {}).get("output_text")`.

> [!NOTE]
> In a future update, generated response fields will move to the `sample` parameter directly. For now, access them through `item.get("sample")`.

The following example scores responses based on length, preferring responses between 50 and 500 characters:

```python
def grade(sample: dict, item: dict) -> float:
    """Score based on response length (prefer 50-500 chars)."""
    # For dataset evaluation, access fields directly from item:
    response = item.get("response", "")

    # For model/agent target evaluation, use item.get("sample") instead:
    # response = item.get("sample", {}).get("output_text", "")

    if not response:
        return 0.0

    length = len(response)
    if length < 50:
        return 0.2
    elif length > 500:
        return 0.5
    return 1.0
```

### Supported packages and limits

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

`pass_threshold` and `deployment_name` are required as initialization parameters when you create a code-based evaluator.

## Prompt-based evaluators

A prompt-based evaluator uses a judge prompt template that an LLM evaluates for each item. Template variables use double curly braces (for example, `{{query}}`) and map to your input data fields.

Prompt-based evaluators support three scoring methods:

- **Ordinal**: Integer scores on a discrete scale you define (for example, 1–5). Higher is better.
- **Continuous**: Float scores for fine-grained measurement on a range you define (for example, 0.0–1.0). Higher is better.
- **Binary** (true/false): Boolean result for threshold-based checks.

The LLM must return a JSON object with `result` and `reason`. The type of `result` matches your scoring method: an integer for ordinal, a float for continuous, or a boolean for binary.

The following example prompt uses ordinal scoring (1–5) to evaluate the friendliness of a response:

```text
Friendliness assesses the warmth and approachability of the response.
Rate the friendliness of the response between one and five using the following scale:

1 - Unfriendly or hostile
2 - Mostly unfriendly
3 - Neutral
4 - Mostly friendly
5 - Very friendly

Assign a rating based on the tone and demeanor of the response.

Response:
{{response}}

Output Format (JSON):
{
  "result": <integer from 1 to 5>,
  "reason": "<brief explanation for the score>"
}
```

### Runtime parameters

Both `deployment_name` and `threshold` are required as initialization parameters when you create a prompt-based evaluator.

## Create a custom evaluator with the SDK

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

### Create a code-based evaluator

Pass the `grade()` function as a string in the `code_text` field. Define the `data_schema` to declare the input fields your function expects, and the `metrics` to describe the score your function returns. Code-based evaluators use the `continuous` metric type with a range of 0.0 to 1.0.

```python
code_evaluator = project_client.evaluators.create_version(
    name="response_length_scorer",
    evaluator_version={
        "name": "response_length_scorer",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Response Length Scorer",
        "description": "Scores responses based on length, preferring 50-500 characters",
        "definition": {
            "type": EvaluatorDefinitionType.CODE,
            "code_text": (
                'def grade(sample: dict, item: dict) -> float:\n'
                '    """Score based on response length (prefer 50-500 chars)."""\n'
                '    response = item.get("response", "")\n'
                '    if not response:\n'
                '        return 0.0\n'
                '    length = len(response)\n'
                '    if length < 50:\n'
                '        return 0.2\n'
                '    elif length > 500:\n'
                '        return 0.5\n'
                '    return 1.0\n'
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
                            "response": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
)
```

For a complete example, see the [code-based evaluator Python SDK sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_eval_catalog_code_based_evaluators.py).

### Create a prompt-based evaluator

Pass the judge prompt in the `prompt_text` field. Define the `data_schema` to declare the input fields your prompt expects, and the `metrics` to describe the scoring method and range. The `init_parameters` declare the model deployment and threshold the evaluator needs at runtime.

```python
prompt_evaluator = project_client.evaluators.create_version(
    name="friendliness_evaluator",
    evaluator_version={
        "name": "friendliness_evaluator",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "Friendliness Evaluator",
        "description": "Evaluates the warmth and approachability of a response",
        "definition": {
            "type": EvaluatorDefinitionType.PROMPT,
            "prompt_text": (
                "Friendliness assesses the warmth and approachability of the response.\n"
                "Rate the friendliness of the response between one and five "
                "using the following scale:\n\n"
                "1 - Unfriendly or hostile\n"
                "2 - Mostly unfriendly\n"
                "3 - Neutral\n"
                "4 - Mostly friendly\n"
                "5 - Very friendly\n\n"
                "Assign a rating based on the tone and demeanor of the response.\n\n"
                "Response:\n{{response}}\n\n"
                "Output Format (JSON):\n"
                '{\n  "result": <integer from 1 to 5>,\n'
                '  "reason": "<brief explanation for the score>"\n}\n'
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
                    "response": {"type": "string"},
                },
                "required": ["response"],
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

For a complete example, see the [prompt-based evaluator Python SDK sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_eval_catalog_prompt_based_evaluators.py).

### Run an evaluation with a custom evaluator

After you create custom evaluators, use them in an evaluation run the same way you use built-in evaluators. You can include multiple evaluators in a single run.

The following example runs both the code-based `response_length_scorer` and the prompt-based `friendliness_evaluator` together.

#### Define and run the evaluation

```python
# Define the data schema
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "response": {"type": "string"},
        },
        "required": ["response"],
    },
)

# Reference both custom evaluators in testing criteria
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "response_length_scorer",
        "evaluator_name": "response_length_scorer",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "pass_threshold": 0.5,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "friendliness_evaluator",
        "evaluator_name": "friendliness_evaluator",
        "data_mapping": {
            "response": "{{item.response}}",
        },
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
            "threshold": 3,
        },
    },
]

# Create the evaluation
eval_object = client.evals.create(
    name="custom-eval-test",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Run the evaluation with inline data
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="custom-eval-run-01",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileContent(
            type="file_content",
            content=[
                SourceFileContentContent(
                    item={
                        "response": "I'm sorry this watch isn't working for you. I'd be happy to help you with a replacement!",
                    }
                ),
                SourceFileContentContent(
                    item={
                        "response": "I will not apologize for my behavior!",
                    }
                ),
            ],
        ),
    ),
)
```

#### Get results

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

For additional examples including listing, updating, and deleting evaluators, see the [evaluator catalog management Python SDK sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_eval_catalog.py).

## Create a custom evaluator in the portal

You can create custom evaluators directly in the Azure AI Foundry portal without writing SDK code.

1. In your Foundry project, go to **Evaluation** > **Evaluator catalog**.
1. Select **Custom evaluator** > **Create**.
1. Fill in the following fields:

| Field | Description |
|---|---|
| **Name** | A unique identifier for the evaluator (for example, `response_length_scorer`). |
| **Display name** | A human-readable name shown in the evaluator catalog. |
| **Description** | A short summary of what the evaluator measures. |
| **Type** | **Code-based** or **Prompt-based**. Determines whether you provide a Python `grade()` function or a judge prompt. |
| **Scoring method** | Code-based evaluators use continuous (0.0–1.0). Prompt-based evaluators can use ordinal, continuous, or binary scoring with a custom range. |
| **Code or Prompt** | For code-based, write a `grade()` function in the code editor. For prompt-based, write a judge prompt in the prompt editor. See the code-based and prompt-based evaluator sections earlier in this article for examples and requirements. |

### Use a custom evaluator in a portal evaluation

After you create a custom evaluator, use it in an evaluation run from the portal:

1. In your Foundry project, go to **Evaluation** and select **Create**.
1. Follow the evaluation creation wizard. On the **Criteria** step, select **Add evaluator**.
1. Choose your custom evaluator from the evaluator catalog.
1. Supply the required initialization parameters. For prompt-based evaluators, provide the **model deployment** and **threshold**. For code-based evaluators, provide the **pass threshold**.
1. Complete the wizard and start the evaluation run.

For detailed steps on running evaluations from the portal, see [Run evaluations from the portal](../../how-to/evaluate-generative-ai-app.md#create-an-evaluation-with-built-in-evaluation-metrics).

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md)
- [Built-in evaluators](../built-in-evaluators.md)

::: moniker-end