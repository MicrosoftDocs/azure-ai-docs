---
title: Continuously Evaluate your AI agents
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to continuously evaluate AI agents.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: amibp
ms.author: lagayhar  
author: lgayhardt
---

# Continuously evaluate your AI agents (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Continuous evaluation for Agents provides near real-time observability and monitoring for your AI application. Once enabled, this feature continuously evaluates agent interactions at a set sampling rate to provide insights into quality, safety, and performance with metrics surfaced in the Foundry Observability dashboard. By using continuous evaluation, you're able to identify and troubleshoot issues early, optimize agent performance, and maintain safety. Evaluations are also connected to [traces](./develop/trace-application.md) to enable detailed debugging and root cause analysis.

## Getting Started

### Prerequisites
[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)] 

- An agent created within the project
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview)

### Steps to connect Application Insights

1. Navigate to your project in [Azure AI Foundry](https://ai.azure.com).
2. Select **Monitoring** on the left-hand menu and go to **Application Analytics**.
3. Connect your Application Insights resource to the project.

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
from azure.ai.projects.models import EvaluatorIds

evaluators={
"Relevance": {"Id": EvaluatorIds.Relevance.value},
"Fluency": {"Id": EvaluatorIds.Fluency.value},
"Coherence": {"Id": EvaluatorIds.Coherence.value},
},
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

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
import pandas as pd


credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

query = f"""
traces
| where message == "gen_ai.evaluation.result"
| where customDimensions["gen_ai.thread.run.id"] == "{run.id}"
"""

try:
    response = client.query_workspace(os.environ["LOGS_WORKSPACE_ID"], query, timespan=timedelta(days=1))
    if response.status == LogsQueryStatus.SUCCESS:
        data = response.tables
    else:
        # LogsQueryPartialResult - handle error here
        error = response.partial_error
        data = response.partial_data
        print(error)

    for table in data:
        df = pd.DataFrame(data=table.rows, columns=table.columns)
        key_value = df.to_dict(orient="records")
        pprint(key_value)
except HttpResponseError as err:
    print("something fatal happened")
    print(err)

```

### Capture reasoning explanations for your evaluation result

AI-assisted evaluators employ chain-of-thought reasoning to generate an explanation for the score in your evaluation result. To enable this on, set redact_score_properties to True in the AgentEvaluationRedactionConfiguration object and pass that as part of your request.

This helps you understand the reasoning behind the scores for each metric.

> [!NOTE]
> Reasoning explanations might mention sensitive information based on the content of the conversation.

```python

from azure.ai.projects.models import AgentEvaluationRedactionConfiguration
              
project.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(  
        thread=thread.id,  
        run=run.id,   
        evaluators=evaluators,  
        redaction_configuration=AgentEvaluationRedactionConfiguration(
            redact_score_properties=False,
       ),
        app_insights_connection_string=app_insights_connection_string,
    )
)

```

### Customize your sampling configuration

You can customize the sampling configuration by defining an `AgentEvaluationSamplingConfiguration` and specify your preferred sampling percent and maximum requests hour within the system limit of 1000/hour.

```python

from azure.ai.projects.models

sampling_config = AgentEvaluationSamplingConfiguration (  
    name = agent.id,  
    samplingPercent = 15,       # Percentage of sampling per hour (0-100)
    maxRequestRate = 250,       # Maximum request rate per hour (0-1000)
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
> If multiple AI applications send continuous evaluation data to the same Application Insights resource, it's recommended to use the service name to differentiate application data. See [Azure AI Tracing](./develop/trace-application.md) for details.

## Viewing continuous evaluation results

After you deployed your application to production with continuous evaluation setup, you can [monitor the quality and safety of your agent with Azure AI Foundry and Azure Monitor](./monitor-applications.md).

## Related content

- [Evaluate your AI agents locally with Azure AI Evaluation SDK](./develop/agent-evaluate-sdk.md)
