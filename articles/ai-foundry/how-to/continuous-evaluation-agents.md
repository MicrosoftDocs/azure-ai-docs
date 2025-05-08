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

# Continuously evaluate your AI agents

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Continuous evaluation for Agents provides near real-time observability and monitoring for your AI application. Once enabled, this feature continuously evaluates agent interactions at a set sampling rate to provide insights into quality, safety and performance with metrics surfaced in the Foundry Observability dashboard. By leveraging continuous evaluation, you will be able to identify and troubleshoot issues early, optimize agent performance, and maintain safety. Evaluations are also connected to [traces](./develop/trace-local-sdk.md) to enable detailed debugging and root cause analysis.

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
from azure.core.exceptions import HttpResponseError  

from azure.identity import DefaultAzureCredential  

from azure.monitor.query import LogsQueryClient, LogsQueryStatus import pandas as pd 

credential = DefaultAzureCredential() client = LogsQueryClient(credential) 

query = "traces 

| where customDimensions["event.name"] startswith "gen_ai.evaluation" and customDimensions["event.name"] != "gen_ai.evaluation.user_feedback" 

| where ('*' in (application) or array_length(application) == 0 or cloud_RoleName in (application)) and timestamp {TimeRange}  // Replace {TimeRange} with your specific time filter 

| where customDimensions.["gen_ai.response.id"] in (response_ids) 

| project metric = extract("gen_ai\\.evaluation\\.(.*)", 1, tostring(customDimensions["event.name"])), score = toint(customDimensions["gen_ai.evaluation.score"]) 

| summarize TotalScores = count(), ScoresInTotal = sum(score) by tostring(metric) 

| extend Percentage = round(todouble(ScoresInTotal) / (TotalScores * 5) * 100) 

| join kind=inner ( 

traces 

| where customDimensions["event.name"] startswith "gen_ai.evaluation" and customDimensions["event.name"] != "gen_ai.evaluation.user_feedback" 

| where ('*' in (application) or array_length(application) == 0 or cloud_RoleName in (application)) and timestamp {TimeRange}  // Replace {TimeRange} with your specific time filter 

| where customDimensions.["gen_ai.response.id"] in (response_ids) 

| project metric = extract("gen_ai\\.evaluation\\.(.*)", 1, tostring(customDimensions["event.name"])), score = toint(customDimensions["gen_ai.evaluation.score"]), timestamp 

| summarize TotalScores = count(), ScoresInTotal = sum(score) by tostring(metric), bin(timestamp,1d) 

| extend Percentage = round(todouble(ScoresInTotal) / (TotalScores * 5) * 100) 

| summarize  

    initial_metric_percentage = todouble(arg_min(timestamp, Percentage).[1]),  

    final_metric_exception = todouble(arg_max(timestamp, Percentage).[1]) 

    by metric 

) on metric 

| extend PercentageChange = round(todouble(initial_metric_percentage - final_metric_exception)) 

| project metric=strcat(toupper(substring(metric, 0, 1)), substring(metric, 1)),initial_metric_percentage,final_metric_exception, Percentage,PercentageChange " 

try: response = client.query_workspace(os.environ["LOGS_WORKSPACE_ID"], query, timespan=timedelta(days=1)) if response.status == LogsQueryStatus.SUCCESS: data = response.tables else: # LogsQueryPartialResult - handle error here error = response.partial_error data = response.partial_data print(error) 

for table in data: 
    df = pd.DataFrame(data=table.rows, columns=table.columns) 
    key_value = df.to_dict(orient="records") 
    pprint(key_value) 
  

except HttpResponseError as err: print("something fatal happened") print(err) 
```

### Customize your sampling configuration

You can customize the sampling configuration by defining an `AgentEvaluationSamplingConfiguration` and specify your preferred sampling percent and maximum requests hour within the system limit of 1000/hour.

```python

from azure.ai.projects import AgentEvaluationSamplingConfiguration

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
> If multiple AI applications send continuous evaluation data to the same Application Insights resource, it's recommended to use the service name to differentiate application data. See [Azure AI Tracing](./develop/trace-local-sdk.md) for details.

## Viewing continuous evaluation results

After you deployed your application to production with continuous evaluation setup, you can begin monitoring your [evaluation results in Azure AI Foundry and Azure Monitor Application Insights](./evaluate-results.md).

<insert gif or image>
:::image type="content" source="../media/" alt-text="Screenshot of. " lightbox="../media/":::

## Related content

- [How to run evaluations online with the Azure AI Foundry SDK](./online-evaluation.md)
- [Evaluate your AI agents locally with Azure AI Evaluation SDK](./develop/agent-evaluate-sdk)