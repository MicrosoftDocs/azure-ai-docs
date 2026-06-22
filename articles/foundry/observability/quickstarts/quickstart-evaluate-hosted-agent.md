---
title: "Quickstart: Evaluate your hosted agent"
description: "Evaluate a deployed hosted agent in Foundry Agent Service by using the Microsoft Foundry SDK for Python or the Microsoft Foundry portal to create a test suite, run an evaluation, and review the results."
author: lgayhardt
ms.author: lagayhar
ms.date: 06/16/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Quickstart: Evaluate your hosted agent

> [!NOTE]
> Hosted agents are currently in preview.

In this quickstart, you evaluate the hosted agent you deployed in [Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md). You provide a test dataset, choose evaluators, run an evaluation against the deployed agent, and review the scores. Each step shows two ways to do the same task: the Python SDK and the Microsoft Foundry portal.

Evaluation establishes a quality baseline for your agent and lets you set acceptance thresholds, such as a task adherence passing rate, before you release changes to users.

## Prerequisites

Before you begin, you need:

* A deployed, invokable hosted agent from [Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md).
* The **Foundry User** role on the Foundry resource.
* To use the UI path, access to the [Foundry portal](https://ai.azure.com). For the SDK path, see the next requirements.
* [Python 3.9 or later](https://www.python.org/downloads/).
* The Azure CLI, signed in with `az login`, so that `DefaultAzureCredential` can authenticate. For installation, see [Install the Azure CLI](/cli/azure/install-azure-cli).

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

* A chat-completion model deployment in the same Foundry project to use as the judge model that scores responses. You can reuse the model deployment your agent already uses, including the one from the previous quickstart, so you don't need a separate deployment.

## Step 1: Confirm your deployed agent

Evaluation runs against a deployed, invokable agent. Confirm your agent is deployed and available before you set up the evaluation.

### [Python SDK](#tab/python)

Install the Foundry SDK:

```bash
pip install "azure-ai-projects>=2.0.0" azure-identity
```

Set two environment variables, then create the project client. Set `AZURE_AI_PROJECT_ENDPOINT` to your project endpoint and `AZURE_AI_MODEL_DEPLOYMENT_NAME` to a chat-completion deployment to use as the judge model. The following code samples assume you run them in this context:

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

Confirm your deployed agent is registered and available. Replace `<your-agent-name>` with your hosted agent's name:

```python
agent = project_client.agents.get("<your-agent-name>")
print(f"Found agent: {agent.name}")
```

The call returns the agent if it exists, or raises an error if the name is wrong or the agent isn't deployed.

### [Foundry portal](#tab/portal)

1. Open the [Foundry portal](https://ai.azure.com) and go to your project.
1. Select your agent, and then select the **Playground** tab.
1. Send a test prompt, such as `Write a haiku about deploying cloud applications.`

You should see a response within a few seconds.

:::image type="content" source="../../media/observability/agent-playground.png" alt-text="Screenshot of the agent Playground tab in the Foundry portal, showing the Setup panel with agent info on the left and a chat window for sending test prompts on the right." lightbox="../../media/observability/agent-playground.png":::

---

## Step 2: Set up built-in evaluators

Start with built-in evaluators to score your agent against a test dataset.

### [Python SDK](#tab/python)

First, create a JSONL file of test queries for your agent. Each line is a JSON object with a `query` field. Save it as `queries.jsonl`:

```json
{"query": "Write a haiku about deploying cloud applications."}
```

Upload the file as a dataset in your project:

```python
dataset = project_client.datasets.upload_file(
    name="agent-test-queries",
    version="1",
    file_path="./queries.jsonl",
)
```

Next, choose built-in evaluators and map their inputs. The `data_mapping` tells each evaluator where to find the query and the agent response. AI-assisted evaluators need a judge model in `initialization_parameters`; the value must be a chat-completion deployment in your project.

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="Intent Resolution",
        evaluator_name="builtin.intent_resolution",
        initialization_parameters={"model": model_deployment},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="Task Adherence",
        evaluator_name="builtin.task_adherence",
        initialization_parameters={"model": model_deployment},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    ),
]
```

Create the evaluation. It defines the test data schema and testing criteria, and serves as a container for one or more runs:

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
print(f"Evaluation created: {evaluation.id}")
```

### [Foundry portal](#tab/portal)

1. In the [Foundry portal](https://ai.azure.com), open your agent and select the **Evaluation** tab, then select **Create**.
1. For **Select evaluation target**, select **Agent**.
1. For **Select evaluation scope**, select **Individual turns**.
1. For **Select data source**, select **Existing dataset** and choose a CSV or JSONL file of test queries from your project's data assets.
1. If the **Configure agents** step appears, review the agent and accept the default user prompt, `{{item.query}}`. Adjust it only if your agent expects a different input format.
1. For **Select testing criteria**, select one or more agent evaluators, such as **Task Adherence** and **Intent Resolution**.

Keep the wizard open. You submit the evaluation in the next step.

:::image type="content" source="../../media/observability/agent-evaluation-create.png" alt-text="Screenshot of the Create new evaluation wizard in the Foundry portal with the Criteria step expanded, showing the Intent Resolution and Task Adherence agent evaluators selected and the dataset field mapping on the right." lightbox="../../media/observability/agent-evaluation-create.png":::

---

## Step 3: Run the evaluation

Run the suite against your deployed agent. The service sends each test query to the agent, captures the response, and scores it with your selected evaluators.

> [!NOTE]
> Target-based evaluation invokes your hosted agent directly. It works with agents that use the responses or invocations protocol with synchronous, non-streaming execution. To evaluate agents that use the A2A or Activity protocol, or other execution patterns such as long-running or streaming, evaluate the traces your agent emits instead. See [Trace evaluation](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview).

### [Python SDK](#tab/python)

Create a run that sends each test query to your agent and applies the evaluators. Replace `<your-agent-name>` with your hosted agent's name:

```python
eval_run = client.evals.runs.create(
    eval_id=evaluation.id,
    name="Agent Evaluation Run",
    data_source={
        "type": "azure_ai_target_completions",
        "source": {"type": "file_id", "id": dataset.id},
        "input_messages": {
            "type": "template",
            "template": [
                {
                    "type": "message",
                    "role": "user",
                    "content": {"type": "input_text", "text": "{{item.query}}"},
                }
            ],
        },
        "target": {
            "type": "azure_ai_agent",
            "name": "<your-agent-name>",
            # "version": "1",  # Optional; omit to use the latest version
        },
    },
)

print(f"Evaluation run started: {eval_run.id}")
```

### [Foundry portal](#tab/portal)

1. On the **Review and submit** step, enter a **name** for the evaluation.
1. Review the target, scope, data source, and selected evaluators.
1. Select **Submit** to start the run.

:::image type="content" source="../../media/observability/agent-evaluation-submit.png" alt-text="Screenshot of the Review step of the Create new evaluation wizard in the Foundry portal, showing the evaluation name field and a Summary panel with the agent target, scope, dataset, and evaluators, plus the Submit button." lightbox="../../media/observability/agent-evaluation-submit.png":::

---

## Step 4: Review the results

Evaluations typically complete in a few minutes, depending on the number of queries.

### [Python SDK](#tab/python)

Poll for completion, then print the status and the report URL that opens the results in the Foundry portal:

```python
import time

while True:
    run = client.evals.runs.retrieve(run_id=eval_run.id, eval_id=evaluation.id)
    if run.status in ["completed", "failed"]:
        break
    time.sleep(5)

print(f"Status: {run.status}")
print(f"Report URL: {run.report_url}")
```

At the run level, you can see aggregated pass and fail counts for each evaluator:

```python
print(run.result_counts)
for criteria in run.per_testing_criteria_results:
    print(criteria.testing_criteria, "passed:", criteria.passed, "failed:", criteria.failed)
```

```output
ResultCounts(errored=0, failed=0, passed=1, total=1, skipped=0)
Intent Resolution passed: 1 failed: 0
Task Adherence passed: 1 failed: 0
```

For row-level detail, list the output items. Each result includes the evaluator name, pass or fail, and a score:

```python
for item in client.evals.runs.output_items.list(run_id=eval_run.id, eval_id=evaluation.id):
    for result in item.results:
        print(item.id, result.name, "passed:", result.passed, "score:", result.score)
```

### [Foundry portal](#tab/portal)

1. The details page shows the target, dataset, status, token usage, and an aggregate score for each evaluator.
1. Select the run name to view row-level results: each query, the agent response, the evaluator score, and the score explanation.

---

## Clean up resources

This quickstart registers a dataset, an evaluation, and run history in your Foundry project. These assets incur little or no ongoing cost.

To remove the hosted agent and the Azure resources you created, follow the cleanup steps in [Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md#clean-up-resources).

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `ModuleNotFoundError` for `azure.ai.projects` or `azure.identity` | Install the SDK: `pip install "azure-ai-projects>=2.0.0" azure-identity`. |
| `AuthenticationError` or `DefaultAzureCredential` failure | Sign in with `az login`, and confirm you have the **Foundry User** role on the project. |
| Agent target not found | Verify the agent name and version with `project_client.agents.get("<your-agent-name>")` or `project_client.agents.list()`. |
| Many errored rows or unexpectedly low scores | Open the report URL and check whether rows failed with agent response or evaluator errors. Fix the underlying errors, then rerun the evaluation. |
| Eval model deployment not found | Verify that the deployment named in `AZURE_AI_MODEL_DEPLOYMENT_NAME` exists in your project under **Build** > **Deployments**. |

## What you learned

In this quickstart, you:

* Created a test dataset and chose evaluators for your hosted agent.
* Ran an evaluation against the deployed agent.
* Reviewed aggregated and row-level results.
* Completed each task with both the Python SDK and the Foundry portal.

## Next steps

> [!div class="nextstepaction"]
> [Optimize a hosted agent](../../agents/quickstarts/quickstart-optimize-hosted-agent.md)

Continue improving your evaluation workflow:

- [Set up continuous and scheduled evaluations](../how-to/how-to-monitor-agents-dashboard.md) to track your agent's quality in production.


## Related content

* [Evaluate your AI agents](../how-to/evaluate-agent.md)
* [Run batch evaluations from the SDK](../../how-to/develop/cloud-evaluation.md)
* [Generate a synthetic evaluation dataset](../how-to/evaluation-dataset-synthetic.md) to create test queries and evaluators automatically.
* [Troubleshoot evaluation and observability issues](../how-to/troubleshooting.md)
* [Agent evaluators reference](../../concepts/evaluation-evaluators/agent-evaluators.md)
* [What are hosted agents?](../../agents/concepts/hosted-agents.md)
