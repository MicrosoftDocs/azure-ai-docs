---
title: Run evaluations online in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use online evaluation to continuously monitor Generative AI Applications.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 01/16/2025
ms.reviewer: mesameki
ms.author: lagayhar  
author: lgayhardt
---

# How to run evaluations online with the Azure AI Foundry SDK

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to run evaluations online in a continuous manner with the Azure AI Foundry SDK. [Evaluations](./develop/evaluate-sdk.md) in pre-production environments is essential for ensuring that your application is safe, performant, and produces high-quality results. However, evaluation doesn't stop after your application is deployed. In production, various things can change, such as the types of queries users are sending to your application, which can influence your application's performance. To maintain a high degree of observability into your production generative AI application, it's important to [trace](./develop/trace-application.md) and continuously evaluate your application's data. By doing so, you can maintain confidence in your application's safety, quality, and performance.

## How online evaluation works

In this section, you'll learn how online evaluation works, how it integrates with [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview), and how you can use it to run continuous evaluations over [trace](https://opentelemetry.io/docs/concepts/signals/traces/) data from your generative AI applications.

After your application is instrumented to send trace data to Application Insights, set up an online evaluation schedule to continuously evaluate this data. Online evaluation is a service that uses Azure AI compute to continuously run a configurable set of evaluators. After you have set up an online evaluation schedule with the Azure AI Foundry SDK, it runs on a configurable schedule. Each time the scheduled job runs, it performs the following steps:

1. Query application trace data from the connected Application Insights resource using provided Kusto (KQL) query.
1. Run each evaluator over the trace data and calculate each metric (for example, *groundedness: 3*).
1. Write evaluation scores back to each trace using standardized semantic conventions.

> [!NOTE]
> Online evaluation supports the same metrics as Azure AI Evaluation. For more information on how evaluation works and which evaluation metrics are supported, see [Evaluate your Generative AI application with the Azure AI Evaluation SDK](./develop/evaluate-sdk.md).

For example, let’s say you have a deployed chat application that receives many customer questions on a daily basis. You want to continuously evaluate the quality of the responses from your application. You set up an online evaluation schedule with a daily recurrence. You configure the evaluators: **Groundedness**,  **Coherence**, and **Fluency**. Every day, the service computes the evaluation scores for these metrics and writes the data back to Application Insights for each trace that was collected during the recurrence time window (in this example, the past 24 hours). Then, the data can be queried from each trace and made accessible in Azure AI Foundry and Azure Monitor Application Insights.

The evaluation results written back to each trace within Application Insights follow the following conventions. A unique span is added to each trace for each evaluation metric:

| Property                                  | Application Insights Table | Fields for a given operation_ID               | Example value                        |
|-------------------------------------------|----------------------------|-----------------------------------------------|--------------------------------------|
| Evaluation metric                         | traces, AppTraces          | `customDimensions[“event.name”]`              | `gen_ai.evaluation.relevance`        |
| Evaluation metric score                   | traces, AppTraces          | `customDimensions[“gen_ai.evaluation.score”]` | `3`                                  |
| Evaluation metric comment (if applicable) | traces, AppTraces          | `message`                                     | `{“comment”: “I like the response”}` |

Now that you understand how online evaluation works and how it connects to Azure Monitor Application Insights, the next step is to set up the service.

## Set up online evaluation

In this section, you'll learn how to configure an online evaluation schedule to continuously monitor your deployed generative AI application. Azure AI Foundry SDK offers such capabilities via. A Python API and supports all of the features available in local evaluations. Use the following steps to submit your online evaluation schedule on your data using built-in or custom evaluators.

> [!NOTE]
> Evaluations are only supported in the same [regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#azure-ai-foundry-project-configuration-and-region-support) as AI-assisted risk and safety metrics.

### Prerequisites

Complete the following prerequisite steps to set up your environment and authentication to the necessary resources:

1. An [Azure Subscription](https://azure.microsoft.com/).
2. A [Resource Group](/azure/azure-resource-manager/management/manage-resource-groups-portal) in an Evaluation-supported region.
3. A new [User-assigned Managed Identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp) in the same resource group and region. Make a note of the `clientId`; you'll need it later.
4. An [Azure AI Hub](../concepts/ai-resources.md) in the same resource group and region.
5. An Azure AI project in this hub, see [Create a project in Azure AI Foundry portal](./create-projects.md).
6. An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/create-workspace-resource).
7. Navigate to the hub page in Azure portal and add Application Insights resource, see [Update Azure Application Insights and Azure Container Registry](./create-azure-ai-resource.md?tabs=portal#update-azure-application-insights-and-azure-container-registry).
8. Azure OpenAI Deployment with GPT model supporting `chat completion`, for example `gpt-4`.
9. `Connection String` for Azure AI project to easily create `AIProjectClient` object. You can get the **Project connection string** under **Project details** from the project's **Overview** page.
10. Navigate to your Application Insights resource in the Azure portal and use the **Access control (IAM)** tab to add the `Log Analytics Contributor` role to the User-assigned Managed Identity you created previously.
11. Attach the [User-assigned Managed Identity](../../machine-learning/how-to-identity-based-service-authentication.md#add-a-user-assigned-managed-identity-to-a-workspace-in-addition-to-a-system-assigned-identity) to your project.
12. Navigate to your Azure AI Services in the Azure portal and use the **Access control (IAM)** tab to add the `Cognitive Services OpenAI Contributor` role to the User-assigned Managed Identity you created previously.

### Installation Instructions

#### Install the Azure CLI and sign in

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

#### Create a new Python environment

[!INCLUDE [Install Python](../includes/install-python.md)]

You can also create a new Python environment using `conda`:

```bash
conda create -n online-evaluation
conda activate online-evaluation
```

#### Install the required packages:

```bash
pip install azure-identity azure-ai-projects azure-ai-ml
```

> [!TIP]
> Optionally, you can use `pip install azure-ai-evaluation` if you want a code-first experience to fetch evaluator ID for built-in evaluators in code. To learn how to do this, see [Specifying evaluators from evaluator library](./develop/cloud-evaluation.md#specifying-evaluators-from-evaluator-library).

### Set up tracing for your generative AI application

Prior to setting up online evaluation, ensure you have first [set up tracing for your generative AI application](./develop/trace-application.md).

#### Using service name in trace data

To identify your application via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is particularly useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them. For example, lets say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Groundedness**. You can use the service name to differentiate between the applications in your online evaluation configurations.

To set up the service name property, you can do so directly in your application code by following the steps, see  [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` prior to deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

For more information on using the service name to differentiate between your generative AI applications, see [tracing](./develop/trace-application.md).

### Query stored trace data in Application Insights

Using the [Kusto Query Language (KQL)](/kusto/query/?view=microsoft-fabric&preserve-view=true), you can query your generative AI application's trace data from Application Insights to use for continuous online evaluation. If you use the [Azure AI Tracing package](./develop/trace-application.md) to trace your generative AI application, you can use the following Kusto query:

> [!IMPORTANT]
> The KQL query used by the online evaluation service must output the following columns: `operation_Id`, `operation_ParentId`, and `gen_ai_response_id`. Additionally, each evaluator has its own input data requirements. The KQL query must output these columns to be used as inputs to the evaluators themselves. For a list of data requirements for evaluators, see [data requirements for built-in evaluators](./develop/evaluate-sdk.md#data-requirements-for-built-in-evaluators).

```kusto
let gen_ai_spans = (
    dependencies
    | where isnotnull(customDimensions["gen_ai.system"])
    | extend response_id = tostring(customDimensions["gen_ai.response.id"])
    | project id, operation_Id, operation_ParentId, timestamp, response_id
);
let gen_ai_events = (
    traces
    | where message in ("gen_ai.choice", "gen_ai.user.message", "gen_ai.system.message")
        or tostring(customDimensions["event.name"]) in ("gen_ai.choice", "gen_ai.user.message", "gen_ai.system.message")
    | project 
        id = operation_ParentId, 
        operation_Id, 
        operation_ParentId, 
        user_input = iff(
            message == "gen_ai.user.message" or tostring(customDimensions["event.name"]) == "gen_ai.user.message", 
            parse_json(iff(message == "gen_ai.user.message", tostring(customDimensions["gen_ai.event.content"]), message)).content, 
            ""
        ), 
        system = iff(
            message == "gen_ai.system.message" or tostring(customDimensions["event.name"]) == "gen_ai.system.message", 
            parse_json(iff(message == "gen_ai.system.message", tostring(customDimensions["gen_ai.event.content"]), message)).content, 
            ""
        ), 
        llm_response = iff(
            message == "gen_ai.choice", 
            parse_json(tostring(parse_json(tostring(customDimensions["gen_ai.event.content"])).message)).content, 
            iff(tostring(customDimensions["event.name"]) == "gen_ai.choice", parse_json(parse_json(message).message).content, "")
        )
    | summarize 
        operation_ParentId = any(operation_ParentId), 
        Input = maxif(user_input, user_input != ""), 
        System = maxif(system, system != ""), 
        Output = maxif(llm_response, llm_response != "") 
    by operation_Id, id
);
gen_ai_spans
| join kind=inner (gen_ai_events) on id, operation_Id
| project Input, System, Output, operation_Id, operation_ParentId, gen_ai_response_id = response_id
```

If you're using the `OTEL_SERVICE_NAME` environment variable in your generative AI application to set the service name, you can query for the `cloud_RoleName` within your online evaluation schedule by adding the following line to your Kusto (KQL) query:

```kusto
| where cloud_RoleName == "service_name"
```

Optionally, you can use the [sample operator](/kusto/query/sample-operator?view=azure-monitor&preserve-view=true) or [take operator](/kusto/query/take-operator?view=microsoft-fabric&preserve-view=true) in your Kusto query such that it only returns a subset of traces. Since AI-assisted evaluations can be costly at scale, this approach can help you control costs by only evaluating a random sample (or `n` traces) of your data.

### Set up online evaluation with Azure AI Project SDK

You can submit an online evaluation scheduled job with the Azure AI Project SDK via a Python API. See the below script to learn how to set up online evaluation with performance and quality (AI-assisted) evaluators. To view a comprehensive list of supported evaluators, see [Evaluate with the Azure AI Evaluation SDK](./develop/evaluate-sdk.md). To learn how to use custom evaluators, see [custom evaluators](./develop/cloud-evaluation.md#specifying-custom-evaluators).

Start by importing the required packages and configuring the required variables:

```python
from azure.ai.projects import AIProjectClient 
from azure.identity import DefaultAzureCredential 
from azure.ai.projects.models import ( 
    ApplicationInsightsConfiguration,
    EvaluatorConfiguration,
    EvaluationSchedule,
    RecurrenceTrigger,
)
from azure.ai.evaluation import CoherenceEvaluator 

# This sample includes the setup for an online evaluation schedule using the Azure AI Project SDK and Azure AI Evaluation SDK
# The schedule is configured to run daily over the collected trace data while running two evaluators: CoherenceEvaluator and RelevanceEvaluator
# This sample can be modified to fit your application's requirements

# Name of your online evaluation schedule
SAMPLE_NAME = "online_eval_name"

# Connection string to your Azure AI Foundry project
# Currently, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
PROJECT_CONNECTION_STRING = "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"

# Your Application Insights resource ID
APPLICATION_INSIGHTS_RESOURCE_ID = "appinsights_resource_id"

# Kusto Query Language (KQL) query to query data from Application Insights resource
# This query is compatible with data logged by the Azure AI Inferencing Tracing SDK (linked in documentation)
# You can modify it depending on your data schema
# The KQL query must output these required columns: operation_ID, operation_ParentID, and gen_ai_response_id
# You can choose which other columns to output as required by the evaluators you are using
KUSTO_QUERY = "let gen_ai_spans=(dependencies | where isnotnull(customDimensions[\"gen_ai.system\"]) | extend response_id = tostring(customDimensions[\"gen_ai.response.id\"]) | project id, operation_Id, operation_ParentId, timestamp, response_id); let gen_ai_events=(traces | where message in (\"gen_ai.choice\", \"gen_ai.user.message\", \"gen_ai.system.message\") or tostring(customDimensions[\"event.name\"]) in (\"gen_ai.choice\", \"gen_ai.user.message\", \"gen_ai.system.message\") | project id= operation_ParentId, operation_Id, operation_ParentId, user_input = iff(message == \"gen_ai.user.message\" or tostring(customDimensions[\"event.name\"]) == \"gen_ai.user.message\", parse_json(iff(message == \"gen_ai.user.message\", tostring(customDimensions[\"gen_ai.event.content\"]), message)).content, \"\"), system = iff(message == \"gen_ai.system.message\" or tostring(customDimensions[\"event.name\"]) == \"gen_ai.system.message\", parse_json(iff(message == \"gen_ai.system.message\", tostring(customDimensions[\"gen_ai.event.content\"]), message)).content, \"\"), llm_response = iff(message == \"gen_ai.choice\", parse_json(tostring(parse_json(tostring(customDimensions[\"gen_ai.event.content\"])).message)).content, iff(tostring(customDimensions[\"event.name\"]) == \"gen_ai.choice\", parse_json(parse_json(message).message).content, \"\")) | summarize operation_ParentId = any(operation_ParentId), Input = maxif(user_input, user_input != \"\"), System = maxif(system, system != \"\"), Output = maxif(llm_response, llm_response != \"\") by operation_Id, id); gen_ai_spans | join kind=inner (gen_ai_events) on id, operation_Id | project Input, System, Output, operation_Id, operation_ParentId, gen_ai_response_id = response_id"
```

Next, define a client and an Azure OpenAI GPT deployment (such as `GPT-4`) which will be used to run your online evaluation schedule. Also, connect to your Application Insights resource:

```python
# Connect to your Azure AI Foundry Project
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING
)

# Connect to your Application Insights resource 
app_insights_config = ApplicationInsightsConfiguration(
    resource_id=APPLICATION_INSIGHTS_RESOURCE_ID,
    query=KUSTO_QUERY
)

# Connect to your Azure OpenAI Service resource. You must use a GPT model deployment for this example.
deployment_name = "gpt-4"
api_version = "2024-08-01-preview"

# This is your Azure OpenAI Service connection name, which can be found in your Azure AI Foundry project under the 'Models + Endpoints' tab.
default_connection = project_client.connections._get_connection(
    "aoai_connection_name"
)

model_config = {
    "azure_deployment": deployment_name,
    "api_version": api_version,
    "type": "azure_openai",
    "azure_endpoint": default_connection.properties["target"]
}
```

Next, configure the evaluators you wish to use:

```python
# RelevanceEvaluator
# id for each evaluator can be found in your Azure AI Foundry registry - please see documentation for more information
# init_params is the configuration for the model to use to perform the evaluation
# data_mapping is used to map the output columns of your query to the names required by the evaluator
relevance_evaluator_config = EvaluatorConfiguration(
    id="azureml://registries/azureml-staging/models/Relevance-Evaluator/versions/4",
    init_params={"model_config": model_config},
    data_mapping={"query": "${data.Input}", "response": "${data.Output}"}
)

# CoherenceEvaluator
coherence_evaluator_config = EvaluatorConfiguration(
    id=CoherenceEvaluator.id,
    init_params={"model_config": model_config},
    data_mapping={"query": "${data.Input}", "response": "${data.Output}"}
)
```

Lastly, define the recurrence and create the schedule:

**Note: In the prerequisite steps, you created a User-assigned managed identity to authenticate the online evaluation schedule to your Application Insights resource. The `AzureMSIClientId` in the `properties` parameter of the `EvaluationSchedule` class is the `clientId` of this identity.**

```python
# Frequency to run the schedule
recurrence_trigger = RecurrenceTrigger(frequency="day", interval=1)

# Dictionary of evaluators
evaluators = {
    "relevance": relevance_evaluator_config,
    "coherence" : coherence_evaluator_config
}

name = SAMPLE_NAME
description = f"{SAMPLE_NAME} description"
# AzureMSIClientId is the clientID of the User-assigned managed identity created during set-up - see documentation for how to find it
properties = {"AzureMSIClientId": "your_client_id"}

# Configure the online evaluation schedule
evaluation_schedule = EvaluationSchedule(
    data=app_insights_config,
    evaluators=evaluators,
    trigger=recurrence_trigger,
    description=description,
    properties=properties)

# Create the online evaluation schedule 
created_evaluation_schedule = project_client.evaluations.create_or_replace_schedule(name, evaluation_schedule)
print(f"Successfully submitted the online evaluation schedule creation request - {created_evaluation_schedule.name}, currently in {created_evaluation_schedule.provisioning_state} state.")
```

#### Perform operations on an online evaluation schedule

You can get, list, and disable online evaluation schedules by adding the following code to your online evaluation configuration script:

**Warning: Please wait a small amount of time (~30 seconds) between creating an online evaluation schedule and running the `get_schedule()` API.**

Get an online evaluation schedule:

```python
name = "<my-online-evaluation-name>"
get_evaluation_schedule = project_client.evaluations.get_schedule(name)
```

List all online evaluation schedules:

```python
count = 0
for evaluation_schedule in project_client.evaluations.list_schedule():
    count += 1
        print(f"{count}. {evaluation_schedule.name} "
        f"[IsEnabled: {evaluation_schedule.is_enabled}]")
        print(f"Total evaluation schedules: {count}")
```

Disable (soft-delete) online evaluation schedule:

```python
name = "<my-online-evaluation-name>"
project_client.evaluations.disable_schedule(name)
```

## Related content

- [Monitor your generative AI applications](./monitor-applications.md)
- [Trace your application](./develop/trace-application.md)
- [Visualize your traces](./develop/visualize-traces.md)
- [Evaluation of Generative AI Models & Applications](../concepts/evaluation-approach-gen-ai.md)
- [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview)
- [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview)