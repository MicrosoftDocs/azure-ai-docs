---
title: Continuously Evaluate your AI agents
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to continuously evaluate AI agents.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 12/08/2025
ms.reviewer: amibp
ms.author: lagayhar  
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Continuously evaluate your AI agents (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Continuous evaluation for Agents provides near real-time observability and monitoring for your AI application. Once enabled, this feature continuously evaluates agent interactions at a set sampling rate to provide insights into quality, safety, and performance with metrics surfaced in the Foundry Observability dashboard. By using continuous evaluation, you're able to identify and troubleshoot issues early, optimize agent performance, and maintain safety. Evaluations are also connected to traces. to enable detailed debugging and root cause analysis.

## Prerequisites

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)] 

- An agent created within the project
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview)

### Steps to connect Application Insights

::: moniker range="foundry-classic"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. Select **Monitoring** on the left-hand menu and go to **Application Analytics**.

1. Connect your Application Insights resource to the project.

::: moniker-end

::: moniker range="foundry"

To view continuous evaluations in Foundry: 

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. Select **Build** from the upper-right navigation. 

1. Select **Agents** from the left pane. Select the agent you'd like to evaluate. 

1. Select the **Monitor** tab to view the agent monitoring dashboard.

1. Open the **Settings** wizard to begin configuring continuous evaluations.

1. Use the *Add Evaluator* dropdown to include one or more evaluators. You can add evaluators in two ways: 

    - **Evaluator Name**
    
        - Select evaluators by name from your available list. 
    
    - **Importing from Past Evaluation**
    
        - Reuse evaluators from previous evaluation runs for consistency.

1. Set *Sample Rate* by defining how many runs per hour will be evaluated.

1. Apply changes.

1. Select **Verify + Submit** to save your configuration.

After configuring your continuous evaluation settings, you will be able to view top-level metrics on the summary cards and associated charts with more granular data.

::: moniker-end

## Microsoft Foundry project configuration and region support

Since the evaluators use hosted evaluation LLMs in the Foundry evaluation service, they require your Foundry project information to be instantiated. The Foundry project must be in a supported region:

> [!div class="mx-tdCol2BreakAll"]
> | Region | Code Vulnerability, Coherence, Fluency, Hate/Unfairness, Indirect Attack, Intent Resolution, Relevance, Self-Harm, Sexual, Task Adherence, Tool Call Accuracy, Violence |
> |--|--|
> | East US | Supported | 
> | East US 2 | Supported  | 
> | West US | Supported |
> | West US 2 | Supported | 
> | West US 3 | Supported |
> | France Central | Supported | 
> | Norway East | Supported  |
> | Sweden Central| Supported  | 

## Set up continuous evaluations with Azure AI Projects client library

```python
pip install azure-ai-projects azure-identity
```

### Create agent run

```python
import os, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    credential=DefaultAzureCredential(), endpoint=os.environ["PROJECT_ENDPOINT"]
)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)

# Create thread and process user message
thread = project_client.agents.threads.create()
project_client.agents.messages.create(thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?")
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

# Handle run status
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Print thread messages
for message in project_client.agents.messages.list(thread_id=thread.id).text_messages:
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
                      
project_client.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(  
        thread=thread.id,  
        run=run.id,   
        evaluators=evaluators,
        appInsightsConnectionString = project_client.telemetry.get_application_insights_connection_string(),
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

AI-assisted evaluators employ chain-of-thought reasoning to generate an explanation for the score in your evaluation result. To enable this, set redact_score_properties to False in the AgentEvaluationRedactionConfiguration object and pass that as part of your request.

This helps you understand the reasoning behind the scores for each metric.

> [!NOTE]
> Reasoning explanations might mention sensitive information based on the content of the conversation.

```python

from azure.ai.projects.models import AgentEvaluationRedactionConfiguration
              
project_client.evaluation.create_agent_evaluation(
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

You can customize the sampling configuration by defining an `AgentEvaluationSamplingConfiguration` and specify your preferred sampling percent and maximum requests per hour within the system limit of 1000/hour.

```python

from azure.ai.projects.models 

sampling_config = AgentEvaluationSamplingConfiguration (  
    name = agent.id,  
    samplingPercent = 100,       # Percentage of sampling per hour (0-100)
    maxRequestRate = 250,       # Maximum request rate per hour (0-1000)
)                                
project_client.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(  
        thread=thread.id,  
        run=run.id,   
        evaluators=evaluators,  
        samplingConfiguration = sampling_config,  
        appInsightsConnectionString = project_client.telemetry.get_application_insights_connection_string(),
    )
)
```

::: moniker range="foundry-classic"

> [!NOTE]
> If multiple AI applications send continuous evaluation data to the same Application Insights resource, it's recommended to use the service name to differentiate application data. See [Azure AI Tracing](./develop/trace-application.md) for details.

::: moniker-end

::: moniker range="foundry"

> [!NOTE]
> If multiple AI applications send continuous evaluation data to the same Application Insights resource, it's recommended to use the service name to differentiate application data.

::: moniker-end

::: moniker range="foundry-classic"

## Viewing continuous evaluation results

After you deploy your application to production with continuous evaluation setup, you can [monitor the quality and safety of your agent with Foundry and Azure Monitor](./monitor-applications.md).

::: moniker-end

## Related content

- [Evaluate your AI agents locally with Azure AI Evaluation SDK](./develop/agent-evaluate-sdk.md)
