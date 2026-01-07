---
title: Monitor AI Agents with Microsoft Foundry Dashboard
description: Gain insights into your AI agents' performance with the Agent Monitoring Dashboard. Optimize operations, evaluate responses, and ensure compliance.
#customer intent: As an AI operations manager, I want to monitor the performance of my AI agents in real time so that I can ensure optimal functionality and compliance.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sonalimalik
ms.date: 01/08/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Monitor AI Agents with the Agent Monitoring Dashboard (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

The Agent Monitoring Dashboard in Microsoft Foundry provides real-time insights into the operational health, performance, and compliance of your AI agents. Use this dashboard to track token usage, latency, evaluation metrics, and security posture across multi-agent systems.

## Prerequisites

- A Foundry project. For more information, see [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).
- At least one deployed agent in your Foundry project.
- An Application Insights resource connected to your project.
- Azure role-based access control (RBAC): At minimum, "Reader" role on the Application Insights resource to view monitoring data.

### Grant Managed Identity Access

To allow your Azure Foundry project to authenticate and interact with Azure AI resources, you must grant its system-assigned managed identity the Azure AI User role

1. Open the Foundry Project Resource: In the Azure portal, navigate to the Azure resource associated with your Foundry project (for example, the project’s resource group or a specific service resource).
1. Go to Access Control (IAM): In the left-hand menu, select Access control (IAM).
1. Add a New Role Assignment.
1. Select the Azure AI User Role: In the *Role* dropdown, search for *Azure AI User*, then select it.
1. Choose the Managed Identity
    1. Under *Assign access to*, choose *Managed identity*.
    1. Select the system-assigned managed identity for your Foundry project from the list.
1. Review and Assign.

Once assigned, the project’s managed identity will have the necessary permissions to access and use Foundry Tools by default.

## View agent metrics in the portal

To view metrics for your agent in the Foundry portal:

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]

2. Navigate to the **Build** page using the top navigation and select the agent you'd like to view data for.

3. Select the **Monitor** tab to view operational, evaluation, and red-teaming data for your agent.

## View agent metrics

 :::image type="content" source="../../media/observability/how-to-monitor-agents-dashboard/foundry-metrics-dashboard.png" alt-text="Screenshot of the Agent Monitoring Dashboard in Foundry showing summary cards at the top with high-level metrics and charts below displaying evaluation scores, agent run success rates, and token usage over time." lightbox="../../media/observability/how-to-monitor-agents-dashboard/foundry-metrics-dashboard.png":::

The Agent Monitoring Dashboard in Foundry is designed for quick insights and deep analysis of your AI agents' performance. It consists of two main areas:

- Summary Cards at the top for high-level metrics. These cards provide an at-a-glance view of key metrics.

- Charts and graphs below for granular details. These visualizations reflect data for the selected time range. Use them to view key metrics including evaluation scores by day, agent run success rates, and token usage.

## Configure settings

The Monitor Settings panel allows you to enable and customize telemetry, evaluations, and security checks for your AI agents. These settings ensure that the dashboard displays accurate operational and quality metrics.

:::image type="content" source="../../media/observability/how-to-monitor-agents-dashboard/monitor-settings-panel.png" alt-text="Screenshot showing the Monitor Settings panel in Foundry with options for operational metrics, continuous evaluation, scheduled evaluations, red team scans, and alerts configuration." lightbox="../../media/observability/how-to-monitor-agents-dashboard/monitor-settings-panel.png":::

The following table describes the monitoring features available in the Monitor Settings panel:

| Setting | Purpose | Configuration Options |
|---------|---------|----------------------|
| **Continuous Evaluation** | Runs real-time checks on agent responses for runs real-time evaluations on agent responses. | Enable/Disable toggle<br>Add evaluators by name or import from past evaluations<br>Set sample rate (for example, 10 runs/hour) |
| **Scheduled Evaluations** | Performs periodic evaluations to validate agent performance against benchmarks. | Enable/Disable toggle<br>Select evaluation template<br>Select evaluation run<br>Set schedule frequency (weekly recommended) |
| **Red Team Scans** | Executes adversarial tests to identify vulnerabilities such as sensitive data leakage or prohibited actions. | Enable/Disable toggle<br>Select evaluation template<br>Select evaluation run<br>Set schedule frequency (weekly recommended) |
| **Alerts** | Monitors for performance anomalies, evaluation failures, and security risks. Integrates with Azure Monitor for automated notifications. | Configure alerts for:<br>- Performance anomalies (latency spikes, token overuse)<br>- Evaluation failures (low coherence scores)<br>- Security risks detected during red-teaming |

## Setup continuous evaluation

```python
 pip install "azure-ai-projects>=2.0.0b1" python-dotenv
```

 Set these environment variables with your own values:

- `AZURE_AI_PROJECT_ENDPOINT`: The Azure AI Project endpoint, as found in the Overview page of your Microsoft Foundry portal.
- `AZURE_AI_AGENT_NAME`: The name of the AI agent to use for evaluation.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The deployment name of the AI model.

### Create agent

```python
import os
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    EvaluationRule,
    ContinuousEvaluationRuleAction,
    EvaluationRuleFilter,
    EvaluationRuleEventType,
)

load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Create agent

    agent = project_client.agents.create_version(
        agent_name=os.environ["AZURE_AI_AGENT_NAME"],
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that answers general questions",
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

### Setup continuous evaluation rule

Next, you want to define the evaluation rule with an evaluation containing the evaluators you'd like to run continuously. To learn more about supported evaluators, see [What are evaluators?](../../../concepts/observability.md#what-are-evaluators)

```python
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

### Get the evaluation result

1. Invoke the agent.
1. View results from the agent evaluation tab.

## Full sample code

To view the full sample code, see:

- [Continuous evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_continuous_evaluation_rule.py).
- [Scheduled evaluation and Schedule AI red teaming evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_scheduled_evaluations.py).

## Next steps

- [Continuously evaluate your AI agents (preview)](/azure/ai-foundry/how-to/continuous-evaluation-agents)
- [Trace and observe AI agents in Foundry (preview)](/azure/ai-foundry/how-to/develop/trace-agents-sdk)
- [Monitor your generative AI applications (preview)](/azure/ai-foundry/how-to/monitor-applications)
