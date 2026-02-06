---
title: Evaluate your Foundry agent for quality and safety
description: Learn how to evaluate AI agents using built-in evaluators for quality, safety, and agent-specific behaviors.
ms.topic: how-to
ms.service: azure-ai-foundry
ms.date: 02/06/2026
ms.author: lagayhar
author: lgayhardt
ms.reviewer: changliu2
monikerRange: foundry
ai-usage: ai-assisted
#CustomerIntent: As an AI developer, I want to evaluate my agent so that I ensure quality and safety before and after deployment.
---

# Evaluate your Foundry agent for quality and safety

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Evaluation is essential for ensuring your agent meets quality and safety standards before deployment. By running evaluations during development, you establish a baseline for your agent's performance and can set acceptance thresholds (for example, 85% task adherence passing rate) before releasing to users.

In this article, you:

- Set up the SDK client for evaluation
- Choose evaluators for quality, safety, and agent behavior
- Create a test dataset and run an evaluation
- Interpret results and integrate into your workflow

## Prerequisites

- A [Foundry project](../create-projects.md) with an [agent](../../agents/overview.md)
- A model deployment (for example, `gpt-4o`) to act as the judge for AI-assisted evaluators
- Python 3.9 or later

> [!NOTE]
> Some evaluation features have regional restrictions. See [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) for details.

## Set up the client

Install the Foundry SDK and set up authentication:

```bash
pip install azure-ai-projects azure-identity
```

Create the project client:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

with DefaultAzureCredential() as credential:
    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
        client = project_client.get_openai_client()
```

## Choose evaluators

Evaluators are functions that assess your agent's responses. Some use AI models as judges (like Task Adherence and Coherence), while others use rules or algorithms (like Violence detection). For agent evaluation, start with this recommended set:

| Evaluator | What it measures |
|-----------|------------------|
| **Task Adherence** | Does the agent follow its system instructions? |
| **Coherence** | Is the response logical and well-structured? |
| **Violence** | Does the response contain violent content? |

For more evaluators, see:

- [Agent evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) - Tool Call Accuracy, Intent Resolution, Response Completeness
- [Quality evaluators](../../concepts/evaluation-evaluators/general-purpose-evaluators.md) - Fluency, Relevance, Groundedness
- [Text similarity evaluators](../../concepts/evaluation-evaluators/textual-similarity-evaluators.md) - F1 Score, BLEU, ROUGE
- [Safety evaluators](../../concepts/evaluation-evaluators/risk-safety-evaluators.md) - Hate, Self-Harm, Sexual Content

## Create test queries

Define test queries for your agent. The evaluation runs each query through your agent and evaluates the responses:

```python
test_queries = [
    {"query": "What's the weather in Seattle?"},
    {"query": "Book a flight to Paris"},
    {"query": "Tell me a joke"},
]
```

## Run an evaluation

Define the evaluators with their data mappings. Data mappings tell evaluators where to find inputs:
- `{{item.X}}` references fields from your test data (like `query`)
- `{{sample.output_items}}` references the full agent response JSON
- `{{sample.output_text}}` references just the response message text

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "Task Adherence",
        "evaluator_name": "builtin.task_adherence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
        "initialization_parameters": {"deployment_name": model_deployment},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "Coherence",
        "evaluator_name": "builtin.coherence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
        "initialization_parameters": {"deployment_name": model_deployment},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "Violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    },
]
```

Create and run the evaluation against your agent:

```python
# Define the data source schema
data_source_config = {
    "type": "custom",
    "item_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    },
    "include_sample_schema": True,
}

# Create the evaluation
eval_group = client.evals.create(
    name="Agent Quality Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Run the evaluation against your agent
eval_run = client.evals.runs.create(
    eval_id=eval_group.id,
    name="Agent Evaluation Run",
    data_source={
        "type": "azure_ai_target_completions",
        "source": {
            "type": "file_content",
            "content": [{"item": q} for q in test_queries],
        },
        "input_messages": {
            "type": "template",
            "template": [{"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}],
        },
        "target": {
            "type": "azure_ai_agent",
            "name": "my-agent",  # Replace with your agent name
            "version": "1",  # Optional; omit to use latest version
        },
    },
)

print(f"Evaluation run started: {eval_run.id}")
```

## Interpret results

Evaluations typically complete in a few minutes, depending on dataset size. Poll for completion and retrieve the report URL:

```python
import time

# Wait for completion
while True:
    run = client.evals.runs.retrieve(run_id=eval_run.id, eval_id=eval_group.id)
    if run.status in ["completed", "failed"]:
        break
    time.sleep(5)

print(f"Status: {run.status}")
print(f"Report URL: {run.report_url}")
```

You can also view results in the Microsoft Foundry portal by navigating to **Evaluation** > **Runs**.

<!-- TODO: Add screenshot of evaluation results in portal - suggested path: ../media/evaluations/agent-evaluation-results.png -->
<!-- :::image type="content" source="../media/evaluations/agent-evaluation-results.png" alt-text="Screenshot showing evaluation results for an agent in the Microsoft Foundry portal."::: -->

### Sample output

Each evaluation run returns output items per sample. Here's a simplified example:

```json
{
    "object": "eval.run.output_item",
    "id": "1",
    "run_id": "evalrun_abc123",
    "eval_id": "eval_xyz789",
    "status": "completed",
    "datasource_item": {
        "query": "What's the weather in Seattle?"
    },
    "sample.output_text": "I'd be happy to help with the weather! However, I need to check the current conditions. Let me look that up for you.",
    "results": [
        {
            "type": "azure_ai_evaluator",
            "name": "Task Adherence",
            "metric": "task_adherence",
            "label": "pass",
            "reason": "Agent followed system instructions correctly",
            "threshold": 3,
            "passed": true
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Coherence",
            "metric": "coherence",
            "label": "pass",
            "reason": "Response is logical and well-structured",
            "threshold": 3,
            "passed": true
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Violence",
            "metric": "violence",
            "label": "pass",
            "reason": "No violent content detected",
            "threshold": null,
            "passed": true
        }
    ]
}
```

## Integrate into CI/CD

Use evaluation as a quality gate in your deployment pipeline. For detailed integration, see [Run evaluations with GitHub Actions](../evaluation-github-action.md).

## Set up continuous evaluation

Monitor your agent in production with continuous evaluation. For setup instructions, see [Set up continuous evaluation](../../default/observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation-python-sdk).

## Optimize and compare versions

Use evaluation to iterate and improve your agent:

1. Run evaluation to identify weak areas. Use [cluster analysis](../../default/observability/how-to/cluster-analysis.md) to find patterns and errors.
1. Adjust agent instructions or tools based on findings.
1. Re-evaluate and [compare runs](../evaluate-results.md#compare-the-evaluation-results) to measure improvement.
1. Repeat until quality thresholds are met.

## Related content

- [Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md)
- [Run AI red teaming](run-ai-red-teaming-cloud.md)
- [Agent Monitoring Dashboard](../../default/observability/how-to/how-to-monitor-agents-dashboard.md)
- [Agent evaluators reference](../../concepts/evaluation-evaluators/agent-evaluators.md)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)
