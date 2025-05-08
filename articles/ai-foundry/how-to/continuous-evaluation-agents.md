---
title: Continuously Evaluate your Generative AI agent application
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to continuously evaluate Generative AI agent application.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/16/2025
ms.reviewer: amibp
ms.author: lagayhar  
author: lgayhardt
---

# Continuously evaluate your agent application

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Continuous evaluations enable near-real-time monitoring of your agent's performance, helping you identify and troubleshoot issues early.

## Getting Started

### Prerequisites

- An Azure AI Foundry project
- An agent created within the project
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview)

### Steps to connect Application Insights

1. Navigate to your project in [Azure AI Foundry](https://ai.azure.com).
2. Select **Observability** on the left-hand menu and go to **Application Analytics**.
3. Connect your Application Insights resource to the project.

*(Add screenshot or GIF here)*
:::image type="content" source="../media/" alt-text="Screenshot of. " lightbox="../media/":::

## Set up continuous evaluations with Azure AI projects client library

```python
pip install azure-ai-projects azure-identity
```

### Create agent run

```python
import os, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-assistant",
    instructions="You are helpful assistant",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)

# Create thread and process user message
thread = project.agents.create_thread()
project.agents.create_message(thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?")
run = project.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)

# Handle run status
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Print thread messages
for message in project.agents.list_messages(thread_id=thread.id).text_messages:
    print(message)

```

### Select evaluators

Next, you want to define the set of evaluators you'd like to run continuously. To learn more about supported evaluators, see [What are evaluators?](../concepts/observability.md#what-are-evaluators)

```python
from azure.ai.projects import EvaluatorIds

evaluators=[
    evaluatorIds.AGENT_QUALITY_EVALUATOR,
    evaluatorIds.TOOL_CALL_ACCURACY,
    evaluatorIds.RELEVANCE,
]
```

### Continuously evaluate your agent run by creating an `AgentEvaluationRequest`

```python
                      
project.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(  
        thread=thread.id,  
        run=run.id,   
        evaluators=evaluators,
        appInsightsConnectionString = project.telemetry.get_connection_string(),
    )
)

```

> [!NOTE]
> Application Insights must be connected to your project otherwise the service won't run. To connect an Application Insights resource, see to [Steps to connect Application Insights](#steps-to-connect-application-insights).

### Get the evaluation result using Application Insights

```python

```

### Customize your sampling configuration

You can customize the sampling configuration by defining an `AgentEvaluationSamplingConfiguration` and specify your preferred sampling percent and maximum requests per hour.

```python

from azure.ai.projects import AgentEvaluationSamplingConfiguration

sampling_config = AgentEvaluationSamplingConfiguration (  
    name = agent.id,  
    samplingPercent = 15,       # Percentage of sampling per hour (0-100)
    maxRequestRate = 250,       # Maximum request rate per hour (0-10000)
)                                
project.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(  
        thread=thread.id,  
        run=run.id,   
        evaluators=evaluators,  
        samplingConfiguration = sampling_config,  
        appInsightsConnectionString = project.telemetry.get_connection_string(),
    )
)
```

> [!NOTE]
> If multiple AI applications send continuous evaluation data to the same Application Insights resource, it's recommended to use the service name to differentiate application data. See [Azure AI Tracing](./develop/trace-local-sdk.md) for details.

## Viewing continuous evaluation results

After you deployed your application to production with continuous evaluation setup, you can begin monitoring your [evaluation results in Azure AI Foundry and Azure Monitor Application Insights](./evaluate-results.md).

<insert gif or image>
:::image type="content" source="../media/" alt-text="Screenshot of. " lightbox="../media/":::

## Related content

- [How to run evaluations online with the Azure AI Foundry SDK](./online-evaluation.md)
- [Evaluate your AI agents locally with Azure AI Evaluation SDK](./develop/agent-evaluate-sdk)