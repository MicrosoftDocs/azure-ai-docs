---
title: "Custom Evaluators"
description: "Learn how to create custom evaluators for your AI applications using code-based, prompt-based, or endpoint-based approaches."
author: lgayhardt
ms.author: lagayhar
ms.reviewer: dlozier
ms.date: 06/17/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
# customer intent: As a developer, I want to create custom evaluators so I can measure domain-specific quality metrics for my AI application's generations.
ai-usage: ai-assisted
---

# Custom evaluators (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Built-in evaluators provide an easy way to monitor the quality of your application's generations. To customize your evaluations, you can create your own code-based, prompt-based, or endpoint-based evaluators.

Custom evaluators let you define domain-specific quality metrics that go beyond the [built-in evaluator catalog](../built-in-evaluators.md). Use a custom evaluator when you need to measure criteria unique to your application, such as brand tone, domain-specific accuracy, or output format compliance.

You can create three types of custom evaluators:

| | Code-based | Prompt-based | Endpoint-based |
|---|---|---|---|
| **How it works** | A Python `grade()` function scores each item with deterministic logic. | A judge prompt instructs an LLM to score each item. | An external HTTP endpoint receives evaluation data and returns scores. |
| **Best for** | Rule-based checks, keyword matching, format validation, length limits. | Subjective quality judgments, semantic similarity, tone analysis. | Custom scoring logic hosted on your own infrastructure, proprietary models, or complex pipelines that need network access. |
| **Scoring method** | Continuous: float from 0.0 to 1.0 (higher is better). | Ordinal, continuous, or binary. You define the min/max range for ordinal and continuous scores. Higher is better for numeric scores. | Defined by your endpoint. Return a JSON object that conforms to the standard evaluation result schema. |
| **Output contract** | A single float value between 0.0 and 1.0. | A JSON object with `result` and `reason`. The type of `result` depends on the scoring method: integer for ordinal, float for continuous, or boolean for binary. | A JSON object with `score`, `reason`, `status`, and optional `properties`. See [Endpoint response schema](#endpoint-response-schema). |

After you create a custom evaluator, you can add it to the evaluator catalog in your Foundry project and use it in [batch evaluation runs](../../how-to/develop/cloud-evaluation.md).

## Code-based evaluators

A code-based evaluator is a Python function named `grade` that receives two dict parameters (`sample` and `item`) and returns a float score between 0.0 and 1.0 (higher is better). In practice, all data is accessed through `item`:

- **Dataset evaluation**: Input fields like `response` or `ground_truth` can be retrieved in the Python code like `item.get("response")` or `item.get("ground_truth")`.
- **Model or agent target evaluation**: To fetch generated response text, use `item.get("sample", {}).get("output_text")`.

> [!NOTE]
> Currently, generated response text from a model or agent target is accessed through `item.get("sample", {}).get("output_text")`. This access pattern is subject to change in a future API update.

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

> [!NOTE]
> If the `grade()` function raises an exception or times out, the service records that item's result as `0.0` and marks it as an error in the evaluation report. Design your function defensively — use `try/except` for risky operations and return a fallback score rather than letting exceptions propagate.

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

`pass_threshold` and `deployment_name` are required as initialization parameters when you create a code-based evaluator. Even though code-based evaluators don't call an LLM, the service API schema requires `deployment_name` for evaluation-run orchestration. You can pass any valid model deployment name from your project.

## Prompt-based evaluators

A prompt-based evaluator uses a judge prompt template that an LLM evaluates for each item. Template variables use double curly braces (for example, `{{query}}`) and map to your input data fields.

Prompt-based evaluators support three scoring methods:

- **Ordinal**: Integer scores on a discrete scale you define (for example, 1–5). Higher is better.
- **Continuous**: Float scores for fine-grained measurement on a range you define (for example, 0.0–1.0). Higher is better.
- **Binary** (true/false): Boolean result for threshold-based checks.

The evaluator must return a JSON object with `result` and `reason`. The type of `result` matches your scoring method: an integer for ordinal, a float for continuous, or a boolean for binary.

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

## Endpoint-based evaluators

An endpoint-based evaluator delegates scoring to an external HTTP endpoint that you own and operate. The evaluation service calls your endpoint for each item (or batch of items), passing the mapped input data as a JSON payload. Your endpoint processes the data using any logic you choose and returns a JSON response with scores.

Use an endpoint-based evaluator when you need:

- Network access to external services or databases during scoring.
- Proprietary models or ML pipelines hosted on your own infrastructure.
- Complex scoring logic that exceeds the sandboxed code-based evaluator limits.
- Integration with existing evaluation services or APIs.

### How it works

1. You deploy an HTTP endpoint that accepts POST requests with evaluation data.
1. You create a connection in your Foundry project that stores the endpoint URL and authentication credentials.
1. You register an endpoint-based evaluator that references the connection.
1. When an evaluation runs, the service resolves the connection, calls your endpoint with the input data, and records the response as the evaluation result.

### Endpoint request schema

The evaluation service sends a POST request to your endpoint with a JSON body containing evaluation metadata and the mapped input fields.

The following table describes the fields your endpoint receives:

| Field | Type | Description |
|---|---|---|
| `schema_version` | `string` | Version of the request schema. Currently `"0.0.1"`. |
| `evaluator_name` | `string` | The registered name of the evaluator being run. |
| `evaluator_version` | `string` | The version of the evaluator definition. |
| `evaluation_level` | `string` | Evaluation granularity: `"turn"` for per-item or `"conversation"` for full conversation. |
| `data` | `object` | Contains the evaluation input data. See `data.item` and `data.sample` below. |
| `data.item` | `object` | Input fields from the evaluation dataset, mapped through the `data_mapping` configuration. |
| `data.sample` | `object` | Generated output from the model or agent target. Present only when evaluating against a target. |

**Example request:**

```json
{
  "schema_version": "0.0.1",
  "evaluator_name": "my_endpoint_evaluator",
  "evaluator_version": "1",
  "evaluation_level": "turn",
  "data": {
    "item": {
      "query": "What is the capital of France?"
    },
    "sample": {
      "response": "Paris"
    }
  }
}
```

### Endpoint response schema

The following table describes the fields your endpoint can return:

| Field | Type | Description |
|---|---|---|
| `score` | `double` or `bool`, nullable | The evaluation score. Type is evaluator-dependent. Null when skipped or on error. |
| `reason` | `string`, nullable | Explanation for the score. Null for non-LLM evaluators. |
| `status` | `string` | Execution status: `"completed"`, `"error"`, or `"skipped"`. |
| `properties` | `object`, nullable | Key-value bag for evaluator-specific data not captured in standard fields. |
| `threshold` | `integer`, nullable | Pass/fail threshold. Null for evaluators that don't use a threshold. |
| `passed` | `bool`, nullable | Whether the score meets the threshold. Null when the evaluator errors or is skipped. |
| `schema_version` | `string` | Version of the response schema. Use `"0.0.1"`. |
| `error` | `object` | Error details when `status` is `"error"`. Contains `code` and `message`. Not included in success responses. |


**Success Response:**

Your endpoint must return a JSON object that conforms to the standard evaluation result schema:

```json
{
  "schema_version": "0.0.1",
  "score": 0.95,
  "reason": "The response accurately answers the question using the provided context.",
  "status": "completed",
  "properties": {
    "confidence": 0.87,
    "source_coverage": "full"
  },
  "threshold": 3,
  "passed": true
}
```

**Failure Reponse:**

In case of error, your endpoint needs to return a JSON object that conforms to the following schema:

```json
 {
   "schema_version": "0.0.1",
   "status": "error",
   "error": {
     "code": "500",
     "message": "Model inference failed"
   }
 }
 ```

### Authentication

Endpoint-based evaluators support two authentication methods through project connections:

| Method | How it works | Best for |
|---|---|---|
| **API Key** | The service passes the key in a request header when calling your endpoint. | Simple endpoints, Azure Functions with function-level keys, third-party APIs. |
| **Microsoft Entra ID** | The Azure Function acquires a managed identity token and passes it as a Bearer token. | Azure Functions with role-based access control, Azure Functions with Easy Auth. |

### Create the endpoint connection

Connections store the endpoint URL and authentication credentials. Create a connection using the Azure Cognitive Services management client:

#### API Key connection

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import ConnectionPropertiesV2BasicResource

mgmt_client = CognitiveServicesManagementClient(
    credential=credential,
    subscription_id=subscription_id,
)

connection = ConnectionPropertiesV2BasicResource(
    properties={
        "category": "ApiKey",
        "target": "https://your-endpoint.azurewebsites.net/api/evaluate",
        "authType": "ApiKey",
        "credentials": {
            "key": "<your-api-key>",
        },
    },
)

mgmt_client.account_connections.create(
    resource_group_name=resource_group,
    account_name=account_name,
    connection_name="my-endpoint-connection",
    connection=connection,
)
```

#### Microsoft Entra ID connection

```python
connection = ConnectionPropertiesV2BasicResource(
    properties={
        "category": "CustomKeys",
        "target": "https://your-endpoint.azurewebsites.net/api/evaluate",
        "authType": "AAD",
        "credentials": {
            "Audience": "api://<your-app-registration-client-id>",
        },
    },
)

mgmt_client.account_connections.create(
    resource_group_name=resource_group,
    account_name=account_name,
    connection_name="my-endpoint-entra-connection",
    connection=connection,
)
```

For Entra ID authentication, your endpoint must be configured to accept tokens issued by the project's managed identity. This typically involves:

- Registering an application in Microsoft Entra ID for your endpoint.
- Enabling Easy Auth (or equivalent token validation) on your endpoint.
- Granting the project's managed identity an app role assignment on the target application.

### Register the evaluator

After creating the connection, register an endpoint-based evaluator that references it:

```python
endpoint_evaluator = project_client.beta.evaluators.create_version(
    name="my-endpoint-evaluator",
    evaluator_version={
        "name": "my-endpoint-evaluator",
        "categories": [EvaluatorCategory.QUALITY],
        "display_name": "My Endpoint Evaluator",
        "description": "Scores responses using a custom evaluation endpoint",
        "definition": {
            "type": "endpoint",
            "connection_name": "my-endpoint-connection",
        },
    },
)
```

### Run an evaluation with an endpoint-based evaluator

Use the `data_mapping` field to specify which input data fields are sent to your endpoint:

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "endpoint_eval",
        "evaluator_name": "my-endpoint-evaluator",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "context": "{{item.context}}",
        },
    },
]
```

The `data_mapping` keys become the JSON fields your endpoint receives. Map them to the columns in your evaluation dataset using `{{item.<field_name>}}` syntax.

### Deploy your endpoint

Your evaluation endpoint can be any HTTP service that accepts POST requests and returns JSON. Common hosting options include:

- **Azure Functions**: Lightweight, serverless hosting for simple scoring logic.
- **Azure App Service**: Full web app hosting for complex evaluation pipelines.
- **Azure Container Apps**: Container-based hosting for ML model inference.

The endpoint must respond within the evaluation service timeout (30 seconds) and return a valid JSON response for each request.

## Create a custom evaluator with the SDK

### Prerequisites and setup

Install the SDK and set up your client:

```bash
pip install "azure-ai-projects>=2.0.0"
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

First, define the evaluator version schema:

```python
code_evaluator = project_client.beta.evaluators.create_version(
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
prompt_evaluator = project_client.beta.evaluators.create_version(
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

#### Clean up resources

Delete a custom evaluator version and the evaluation when you no longer need them:

```python
# Delete the custom evaluator version
project_client.beta.evaluators.delete_version(
    name="response_length_scorer",
    version=code_evaluator.version,
)

# Delete the evaluation
client.evals.delete(eval_id=eval_object.id)
```

For more information on data source options, evaluator mappings, and advanced scenarios, see [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md).

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

For detailed steps on running evaluations from the portal, see [Run evaluations from the portal](../../how-to/evaluate-generative-ai-app.md#create-an-evaluation).

## Conversation-level custom evaluators

Custom evaluators can score entire conversations instead of individual turns. To enable conversation-level evaluation:

1. Set `evaluation_level="conversation"` on the evaluation run
2. Design your `grade()` function to expect `item["messages"]` as a conversation array

When running at the conversation level, the `item` dict receives the full conversation messages array instead of a single query/response pair. This enables you to build custom metrics that assess the entire user interaction.

### Example: Session-level compliance check

This example checks whether the agent disclosed a required disclaimer at any point during the conversation:

```python
def grade(sample: dict, item: dict) -> float:
    """Check if agent disclosed required disclaimer during conversation."""
    messages = item.get("messages", [])
    
    for msg in messages:
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if isinstance(content, str) and "not financial advice" in content.lower():
                return 1.0
    
    return 0.0  # Disclaimer never provided
```

### Example: Conversation length scorer

This example scores conversations based on whether they resolved within a target number of turns:

```python
def grade(sample: dict, item: dict) -> float:
    """Score based on conversation length (prefer shorter resolutions)."""
    messages = item.get("messages", [])
    
    # Count user turns (excludes system messages)
    user_turns = sum(1 for msg in messages if msg.get("role") == "user")
    
    if user_turns <= 2:
        return 1.0  # Resolved quickly
    elif user_turns <= 4:
        return 0.7  # Reasonable length
    elif user_turns <= 6:
        return 0.4  # Getting long
    else:
        return 0.2  # Too many turns
```

## Related content

- [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md)
- [Built-in evaluators](../built-in-evaluators.md)
