---
title: "Evaluate your AI agents"
description: "Learn how to evaluate AI agents using built-in evaluators for quality, safety, and agent-specific behaviors."
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.date: 07/21/2026
ms.author: lagayhar
author: lgayhardt
ms.reviewer: dlozier
ai-usage: ai-assisted
#CustomerIntent: As an AI developer, I want to evaluate my agent so that I ensure quality and safety before and after deployment.
ms.custom: doc-kit-assisted
---

# Evaluate your AI agents

Evaluation is essential for ensuring your agent meets quality and safety standards before deployment. By running evaluations during development, you establish a baseline for your agent's performance and can set acceptance thresholds, such as an 85% task adherence passing rate, before releasing it to users.

In this article, you learn how to run an agent-targeted evaluation against a [Foundry agent](../../agents/overview.md) or [hosted agent](../../agents/concepts/hosted-agents.md). You use a [rubric evaluator](../../concepts/evaluation-evaluators/rubric-evaluators.md) generated from your agent's context as the primary measure, and layer in built-in evaluators for content safety and other risks. Specifically, you:

- Set up the SDK client for evaluation.
- Generate a rubric evaluator tailored to your agent, and pair it with built-in evaluators.
- Create a test dataset and run an evaluation.
- Interpret results and integrate them into your workflow.

> [!TIP]
> For general-purpose evaluation of generative AI models and applications, including custom evaluators, different data sources, and additional SDK options, see [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md).

## Prerequisites

- Python 3.8 or later.
- A [Foundry project](../../how-to/create-projects.md) with an [agent](../../agents/overview.md) or [hosted agent](../../agents/concepts/hosted-agents.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-4o` or `gpt-4o-mini`).
- **Foundry User** role on the Foundry project.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

> [!NOTE]
> Some evaluation features - including rubric generation, synthetic and trace-based dataset creation, and risk and safety evaluators - have regional restrictions. See [Rate limits, region support, and enterprise features for evaluation](../../concepts/evaluation-regions-limits-virtual-network.md) for the full list.

## Set up the client

Install the Foundry SDK and set up authentication:

```bash
pip install "azure-ai-projects>=2.2.0" azure-identity
```

Create the project client. The following code samples assume you run them in this context:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=endpoint, credential=credential)
client = project_client.get_openai_client()
```

## Choose evaluators

Evaluators score your agent's responses. The recommended primary measure for agent evaluation is a *rubric evaluator*—a set of weighted scoring dimensions that an LLM judge applies to every response, so you can express the exact criteria that matter (for example, policy enforcement, tool usage accuracy, or communication clarity) and score consistently at scale. For details, see [Rubric evaluators](../../concepts/evaluation-evaluators/rubric-evaluators.md).

Pair your rubric with additional evaluators to get full coverage of your evaluation scope:

- [Agent evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) — Evaluate how effectively agents handle tasks, tools, and user intent.
- [Quality evaluators](../../concepts/evaluation-evaluators/general-purpose-evaluators.md) — Measure the overall quality of generated responses.
- [Text similarity evaluators](../../concepts/evaluation-evaluators/textual-similarity-evaluators.md) — Compare generated text against reference answers using NLP metrics.
- [Safety evaluators](../../concepts/evaluation-evaluators/risk-safety-evaluators.md) — Identify potential content and security risks in generated output.
- [Custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md) — Build your own evaluators when the rubric and built-ins don't cover your criteria.

You can author a rubric by hand, or generate one from the agent's context—its name, instructions, and tools. The following sample generates a rubric and prints its dimensions so you can review them before use.

```python
import time
import uuid
from azure.ai.projects.models import (
    AgentEvaluatorGenerationJobSource,
    EvaluatorGenerationInputs,
    EvaluatorGenerationJob,
    JobStatus,
)

AGENT_NAME = "my-agent"  # Replace with your agent name
TERMINAL_STATUSES = {JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED}

generation_job = project_client.beta.evaluators.create_generation_job(
    job=EvaluatorGenerationJob(
        inputs=EvaluatorGenerationInputs(
            model=model_deployment,
            evaluator_name=f"agent-quality-{uuid.uuid4().hex[:8]}",
            evaluator_display_name="Agent Quality",
            sources=[AgentEvaluatorGenerationJobSource(agent_name=AGENT_NAME)],
        ),
    ),
)

while generation_job.status not in TERMINAL_STATUSES:
    time.sleep(10)
    generation_job = project_client.beta.evaluators.get_generation_job(generation_job.id)

rubric_evaluator = generation_job.result
print(f"Generated rubric {rubric_evaluator.name} v{rubric_evaluator.version}")
for dim in rubric_evaluator.definition.dimensions:
    print(f"  - {dim.id} (weight {dim.weight}): {dim.description}")
```

For a complete runnable example, see [sample_rubric_evaluator_generation_all_sources.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_rubric_evaluator_generation_all_sources.py) on GitHub. To hand-author a rubric instead, see [sample_rubric_evaluator_manual.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_rubric_evaluator_manual.py).

## Create a test dataset

Create a JSONL file with test queries for your agent. Each line contains a JSON object with a `query` field:

```jsonl
{"query": "What's the weather in Seattle?"}
{"query": "Book a flight to Paris"}
{"query": "Tell me a joke"}
```

> [!TIP]
> If you don't have a hand-curated dataset, you can bootstrap one. Use [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md) when you're prelaunch or have low traffic, or [Convert agent traces into evaluation datasets](traces-to-dataset.md) to build a dataset from real production traffic.

Upload this file as a dataset in your project:

```python
dataset = project_client.datasets.upload_file(
    name="agent-test-queries",
    version="1",
    file_path="./test-queries.jsonl",
)
```

## Run an evaluation

When you run an evaluation, the service sends each test query to your agent, captures the response, and applies your selected evaluators to score the results.

First, configure your testing criteria. Reference the generated rubric evaluator by name. Each entry uses `data_mapping` to point at fields in the test data and agent response, and `initialization_parameters` to pass evaluator settings:

- `{{item.X}}` references fields from your test data, like `query`.
- `{{sample.output_items}}` references the full agent response, including tool calls.
- `{{sample.output_text}}` references just the response message text.
- `initialization_parameters={"deployment_name": <model>}` supplies the judge model. Typically required for LLM judge evaluators. For per-evaluator parameters, see [built-in evaluators](../../concepts/observability.md#what-are-evaluators).

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="Agent Quality",
        evaluator_name=rubric_evaluator.name,
        initialization_parameters={"deployment_name": model_deployment},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    ),
]
```

To layer in built-in evaluators alongside the rubric, append entries with the same shape but `evaluator_name="builtin.<name>"`. For example, add Violence (content safety) and Coherence (LLM judge quality):

```python
testing_criteria.append(
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="Violence",
        evaluator_name="builtin.violence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    )
)

testing_criteria.append(
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="Coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"deployment_name": model_deployment},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    )
)
```

Next, create the evaluation. An evaluation defines the test data schema and testing criteria. It serves as a container for multiple runs. All runs under the same evaluation conform to the same schema and produce the same set of metrics. This consistency is important for comparing results across runs.

```python
from openai.types.eval_create_params import DataSourceConfigCustom

data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
    include_sample_schema=True,
)

evaluation = client.evals.create(
    name="Agent Quality Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)
```

Finally, create a run that sends your test queries to the agent and applies the evaluators:

```python
eval_run = client.evals.runs.create(
    eval_id=evaluation.id,
    name="Agent Evaluation Run",
    data_source={
        "type": "azure_ai_target_completions",
        "source": {
            "type": "file_id",
            "id": dataset.id,
        },
        "input_messages": {
            "type": "template",
            "template": [{"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}],
        },
        "target": {
            "type": "azure_ai_agent",
            "name": AGENT_NAME,
            "version": "1",  # Optional; omit to use latest version
        },
    },
)

print(f"Evaluation run started: {eval_run.id}")
```

> [!TIP]
> This sample works for both prompt agents and hosted agents that use the responses protocol. For hosted agents that use the invocations protocol, the `input_messages` format is different — provide a freeform JSON object instead of the structured template. For details and code samples, see [Hosted agent invocations protocol](../../how-to/develop/cloud-evaluation.md#hosted-agent-invocations-protocol) in the cloud evaluation guide.

> [!TIP]
> To evaluate agent interactions that already occurred using traces from Application Insights, see [Trace evaluation](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview) in the cloud evaluation guide.

## Interpret results

Evaluations typically complete in a few minutes, depending on the number of queries. Poll for completion and retrieve the report URL to view the results in the Microsoft Foundry portal under the **Evaluations** tab:

```python
import time

# Wait for completion
while True:
    run = client.evals.runs.retrieve(run_id=eval_run.id, eval_id=evaluation.id)
    if run.status in ["completed", "failed"]:
        break
    time.sleep(5)

print(f"Status: {run.status}")
print(f"Report URL: {run.report_url}")
```

:::image type="content" source="../../media/observability/agent-evaluation-results.png" alt-text="Screenshot showing evaluation results for an agent in the Microsoft Foundry portal." lightbox="../../media/observability/agent-evaluation-results.png":::

### Aggregated results

At the run level, you can see aggregated data, including pass and fail counts, token usage per model, and results per evaluator:

```json
{
    "result_counts": {
        "total": 3,
        "passed": 1,
        "failed": 2,
        "errored": 0
    },
    "per_model_usage": [
        {
            "model_name": "gpt-4o-mini-2024-07-18",
            "invocation_count": 6,
            "total_tokens": 9285,
            "prompt_tokens": 8326,
            "completion_tokens": 959
        }
    ],
    "per_testing_criteria_results": [
        { "testing_criteria": "Agent Quality", "passed": 1, "failed": 2, "errored": 0 },
        { "testing_criteria": "Violence",      "passed": 3, "failed": 0, "errored": 0 },
        { "testing_criteria": "Coherence",     "passed": 2, "failed": 1, "errored": 0 }
    ]
}
```

### Row level output

Each evaluation run returns output items per row in your test dataset, providing detailed visibility into your agent's performance. Output items include the original query, agent response, individual evaluator results with scores and reasoning, and token usage:

```json
{
    "object": "eval.run.output_item",
    "id": "1",
    "run_id": "evalrun_abc123",
    "eval_id": "eval_xyz789",
    "status": "completed",
    "datasource_item": {
        "query": "What's the weather in Seattle?",
        "response_id": "resp_abc123",
        "agent_name": "my-agent",
        "agent_version": "10",
        "sample.output_text": "I'd be happy to help with the weather! However, I need to check the current conditions. Let me look that up for you.",
        "sample.output_items": [
            ... // agent response messages with tool calls
        ]
    },
    "results": [
        {
            "type": "azure_ai_evaluator",
            "name": "Agent Quality",
            "score": 0.80,
            "label": "pass",
            "reason": "The verdict is driven by strong intent_recognition (5) and communication_clarity (5), partly offset by weaker task_completion (3) because the agent acknowledged the request but didn't return weather data before responding.",
            "threshold": 0.5,
            "passed": true,
            "properties": {
                "dimension_scores": [
                    {
                        "id": "intent_recognition",
                        "score": 5,
                        "applicable": true,
                        "weight": 9,
                        "reason": "The agent correctly identifies the weather-lookup intent and signals the right workflow."
                    },
                    {
                        "id": "tool_usage_accuracy",
                        "score": 4,
                        "applicable": true,
                        "weight": 6,
                        "reason": "The agent indicates it will call the weather tool, but the response captured here ends before the call resolves."
                    },
                    ... // task_completion (3, weight 6), communication_clarity (5, weight 3)
                ]
            },
            "sample":
            {
               ... // evaluator input/output and token usage
            }
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Violence",
            "metric": "violence",
            "score": 0.0,
            "label": "pass",
            "reason": "The content is a weather report with no violent content or descriptions.",
            "threshold": 3,
            "passed": true,
            "sample": { ... }
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Coherence",
            "metric": "coherence",
            "score": 4.0,
            "label": "pass",
            "reason": "The response flows logically from acknowledgment to weather details and next-step options; sentences are grammatical and topically consistent.",
            "threshold": 3,
            "passed": true,
            "sample": { ... }
        }
    ]
}
```

The `properties.dimension_scores` array shows the per-dimension breakdown the LLM judge produced. Each dimension's `score` is on a 1–5 scale. The top-level `score` is the weighted average of applicable dimension scores, normalized to a 0–1 range. For the full output schema, see [Rubric evaluators](../../concepts/evaluation-evaluators/rubric-evaluators.md#example-output).

## Integrate into your workflow

- **CI/CD pipeline**: Use evaluation as a quality gate in your deployment pipeline. For detailed integration, see [Run evaluations with GitHub Actions](../../how-to/evaluation-github-action.md).
- **Production monitoring**: Monitor your agent in production by using continuous evaluation. For setup instructions, see [Set up continuous evaluation](how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation).

## Optimize and compare versions

Use evaluation to iterate and improve your agent:

1. Run evaluation to identify weak areas. Use [cluster analysis](cluster-analysis.md) to find patterns and errors.
1. Adjust agent instructions or tools based on findings.
1. Reevaluate and [compare runs](../../how-to/evaluate-results.md#compare-the-evaluation-results) to measure improvement.
1. Repeat until quality thresholds are met.

## Related content

- [Rubric evaluators](../../concepts/evaluation-evaluators/rubric-evaluators.md)
- [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md)
- [Convert agent traces into evaluation datasets](traces-to-dataset.md)
- [Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md)
- [Rubric evaluator generation sample (Python)](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_rubric_evaluator_generation_all_sources.py)
- [Run AI red teaming](../../how-to/develop/run-ai-red-teaming-cloud.md)
- [Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Agent evaluators reference](../../concepts/evaluation-evaluators/agent-evaluators.md)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)
- [Trace evaluation in the cloud](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
