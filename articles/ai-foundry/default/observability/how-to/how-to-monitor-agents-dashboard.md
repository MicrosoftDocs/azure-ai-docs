---
title: Monitor agents with the Agent Monitoring Dashboard
description: Learn how to monitor operational metrics, token usage, latency, and evaluation results for AI agents in Microsoft Foundry by using the Agent Monitoring Dashboard and Application Insights.
#customer intent: As an AI operations manager, I want to monitor the performance of my AI agents in real time so that I can ensure optimal functionality and compliance.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sonalimalik
ms.date: 01/08/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus, pilot-ai-workflow-jan-2026 
ai-usage: ai-assisted
---

# Monitor agents with the Agent Monitoring Dashboard (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Use the Agent Monitoring Dashboard in Microsoft Foundry to track operational metrics and evaluation results for your agents. This dashboard helps you understand token usage, latency, success rates, and evaluation outcomes for production traffic.

This article covers two approaches: viewing metrics in the Foundry portal and setting up continuous evaluation programmatically with the Python SDK.

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with at least one [agent](../../../agents/overview.md).
- An [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected to your project.
- Azure role-based access control (RBAC) access to the Application Insights resource. For log-based views, you also need access to the associated Log Analytics workspace. To verify access, open the Application Insights resource in the Azure portal, select **Access control (IAM)**, and confirm your account has an appropriate role. For log access, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader).

## Connect Application Insights

The Agent Monitoring Dashboard reads telemetry from the Application Insights resource connected to your Foundry project. If you haven't connected Application Insights yet, follow the tracing setup steps and then return to this article.

- [How to set up tracing in Microsoft Foundry](trace-agent-setup.md) 

## View agent metrics

To view metrics for an agent in the Foundry portal:

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]

2. Navigate to the **Build** page using the top navigation and select the agent you'd like to view data for.

3. Select the **Monitor** tab to view operational, evaluation, and red-teaming data for your agent.

 :::image type="content" source="../../media/observability/how-to-monitor-agents-dashboard/foundry-metrics-dashboard.png" alt-text="Screenshot of the Agent Monitoring Dashboard in Foundry showing summary cards at the top with high-level metrics and charts below displaying evaluation scores, agent run success rates, and token usage over time." lightbox="../../media/observability/how-to-monitor-agents-dashboard/foundry-metrics-dashboard.png":::

The dashboard is designed for quick insights and deep analysis of your agent's performance. It consists of two main areas:

- Summary cards at the top for high-level metrics.

- Charts and graphs below for granular details. These visualizations reflect data for the selected time range.

## Understand the dashboard metrics

Use these definitions to interpret the dashboard:

- **Token usage**: Token counts for agent traffic in the selected time range. High token usage might indicate verbose prompts or responses that could benefit from optimization.
- **Latency**: Response time for agent runs. Latency above 10 seconds might indicate model throttling, complex tool calls, or network issues.
- **Run success rate**: The percentage of runs that complete successfully. A rate below 95% warrants investigation into failed runs.
- **Evaluation metrics**: Scores produced by evaluators that run on sampled agent outputs. Scores vary by evaluator; review individual evaluator documentation for interpretation guidance.
- **Red teaming results**: Outcomes from scheduled red team scans, if enabled. Failed scans indicate potential security risks that require remediation.

> [!NOTE]
> Monitoring data is stored in the connected Application Insights resource. Retention and billing follow your Application Insights configuration.

## Configure settings

Use the Monitor settings panel to configure telemetry, evaluations, and security checks for your agents. These settings control which charts the dashboard shows and which evaluations run.

:::image type="content" source="../../media/observability/how-to-monitor-agents-dashboard/monitor-settings-panel.png" alt-text="Screenshot showing the Monitor Settings panel in Foundry with options for operational metrics, continuous evaluation, scheduled evaluations, red team scans, and alerts configuration." lightbox="../../media/observability/how-to-monitor-agents-dashboard/monitor-settings-panel.png":::

To access Monitor settings, select the gear icon on the **Monitor** tab. The following table describes each monitoring feature:

| Setting | Purpose | Configuration Options |
|---------|---------|----------------------|
| **Continuous evaluation** | Runs evaluations on sampled agent responses. | Enable or disable<br>Add evaluators<br>Set the sample rate |
| **Scheduled evaluations** | Runs evaluations on a schedule to validate performance against benchmarks. | Enable or disable<br>Select an evaluation template and run<br>Set a schedule |
| **Red team scans** | Runs adversarial tests to detect risks such as data leakage or prohibited actions. | Enable or disable<br>Select an evaluation template and run<br>Set a schedule |
| **Alerts** | Detects performance anomalies, evaluation failures, and security risks. | Configure alerts for latency, token usage, evaluation scores, or red team findings |

## Set up continuous evaluation (Python SDK)

Use the Python SDK to set up continuous evaluation rules for agent responses. This section requires Python 3.9 or later.

```bash
pip install "azure-ai-projects>=2.0.0b1" python-dotenv
```

Set these environment variables with your own values:

- `AZURE_AI_PROJECT_ENDPOINT`: The Foundry project endpoint, as found on the project overview page in the Foundry portal.
- `AZURE_AI_AGENT_NAME`: The name of the agent to use for evaluation.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The deployment name of the model.

### Assign permissions for continuous evaluation

To enable continuous evaluation rules, assign the project managed identity the **Azure AI User** role.

1. In the Azure portal, open the resource for your Foundry project.
1. Select **Access control (IAM)**, and then select **Add**.
1. Create a role assignment for **Azure AI User**.
1. For the member, select your Foundry project's managed identity.

### Create an agent

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
)

load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    agent = project_client.agents.create_version(
        agent_name=os.environ["AZURE_AI_AGENT_NAME"],
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that answers general questions",
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

### Create a continuous evaluation rule

Define the evaluation and the rule that runs when a response completes. To learn more about supported evaluators, see [What are evaluators?](../../../concepts/observability.md#what-are-evaluators).

```python
from azure.ai.projects.models import (
    EvaluationRule,
    ContinuousEvaluationRuleAction,
    EvaluationRuleFilter,
    EvaluationRuleEventType,
)

data_source_config = {"type": "azure_ai_source", "scenario": "responses"}
testing_criteria = [
    {"type": "azure_ai_evaluator", "name": "violence_detection", "evaluator_name": "builtin.violence"}
]
eval_object = openai_client.evals.create(
    name="Continuous Evaluation",
    data_source_config=data_source_config,  # type: ignore
    testing_criteria=testing_criteria,  # type: ignore
)
print(f"Evaluation created (id: {eval_object.id}, name: {eval_object.name})")

continuous_eval_rule = project_client.evaluation_rules.create_or_update(
    id="my-continuous-eval-rule",
    evaluation_rule=EvaluationRule(
        display_name="My Continuous Eval Rule",
        description="An eval rule that runs on agent response completions",
        action=ContinuousEvaluationRuleAction(eval_id=eval_object.id, max_hourly_runs=100),
        event_type=EvaluationRuleEventType.RESPONSE_COMPLETED,
        filter=EvaluationRuleFilter(agent_name=agent.name),
        enabled=True,
    ),
)
print(
    f"Continuous Evaluation Rule created (id: {continuous_eval_rule.id}, name: {continuous_eval_rule.display_name})"
)
```

References: [EvaluationRuleEventType](/python/api/azure-ai-projects/azure.ai.projects.models.evaluationruleeventtype), [EvaluationRule](/python/api/azure-ai-projects/azure.ai.projects.models.evaluationrule)

## Verify continuous evaluation results

1. Generate agent traffic (for example, run your app or test the agent in the portal).
1. In the Foundry portal, open the agent and select **Monitor**.
1. Review evaluation-related charts for the selected time range.

If the setup is successful, the evaluation-related charts display scores for your selected time range, and the evaluation runs list shows entries with status **Completed**.

You can also list recent evaluation runs and open the report URL:

```python
eval_run_list = openai_client.evals.runs.list(
    eval_id=eval_object.id,
    order="desc",
    limit=10,
)

if len(eval_run_list.data) > 0 and eval_run_list.data[0].report_url:
    print(f"Report URL: {eval_run_list.data[0].report_url}")
```

## Full sample code

To view the full sample code, see:

- [Continuous evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_continuous_evaluation_rule.py).
- [Scheduled evaluation and Schedule AI red teaming evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_scheduled_evaluations.py).

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Dashboard charts are empty | No recent traffic, time range excludes data, or ingestion delay | Generate new agent traffic, expand the time range, and refresh after a few minutes. |
| You see authorization errors | Missing RBAC permissions on Application Insights or Log Analytics | Confirm access in **Access control (IAM)** for the connected resources. For log access, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). |
| Continuous evaluation results don't appear | Continuous evaluation isn't enabled or rule creation failed | Confirm that your rule is enabled and that agent traffic is flowing. If you use the Python SDK setup, confirm the project managed identity has the **Azure AI User** role. |
| Evaluation runs are skipped | Hourly run limit reached | Increase `max_hourly_runs` in the evaluation rule configuration or wait for the next hour. The default limit is 100 runs per hour. |

## Related content

- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Run AI Red Teaming Agent in the cloud](../../../how-to/develop/run-ai-red-teaming-cloud.md)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Tracing integrations](trace-agent-framework.md)
