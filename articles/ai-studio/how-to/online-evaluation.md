---
title: Continuously Monitor your Generative AI Applications
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use online and remote evaluation to continuously monitor Generative AI Applications.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 11/19/2024
ms.reviewer: alehughes
ms.author: lagayhar  
author: lgayhardt
---

# Continuously monitor your generative AI applications

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Continuous advancements in Generative AI have led organizations to build increasingly complex applications to solve various problems (chat-bots, RAG systems, agentic systems, etc.). These applications are being used to drive innovation, improve customer experiences, and enhance decision-making. Although the models (for example, GPT-4) powering these Generative AI applications are extremely capable, continuous monitoring has never been more important to ensure high-quality, safe, and reliable results. Continuous monitoring is effective when multiple perspectives are considered when observing an application. These perspectives include token usage and cost, operational metrics – latency, request count, etc. - and, importantly, continuous evaluation. To learn more about evaluation, see [Evaluation of generative AI applications](../concepts/evaluation-approach-gen-ai.md).

Azure AI and Azure Monitor provide tools for you to continuously monitor the performance of your Generative AI applications from multiple perspectives. With Azure AI Online Evaluation, you can continuously evaluate your application agnostic of where it's deployed or what orchestration framework it's using (for example, LangChain). You can use various [built-in evaluators](../concepts/evaluation-metrics-built-in.md) which maintain parity with the [Azure AI Evaluation SDK](./develop/evaluate-sdk.md) or define your own custom evaluators. By continuously running the right evaluators over your collected trace data, your team can more effectively identify and mitigate security, quality, and safety concerns as they arise, either in pre-production or post-production. Azure AI Online Evaluation provides full integration with the comprehensive suite of observability tooling available in [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview), enabling you to build custom dashboards, visualize your evaluation results over time, and configure alerting for advanced application monitoring.

In summary, monitoring your generative AI applications has never been more important, due to the complexity and rapid evolvement of the AI industry. Azure AI Online Evaluation, integrated with Azure Monitor Application Insights, enables you to continuously evaluate your deployed applications to ensure that they're performant, safe, and produce high-quality results in production.

## How online evaluation works

In this section, you'll learn how Azure AI Online Evaluation works, how it integrates with [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview), and how you can use it to run continuous evaluations over [trace](https://opentelemetry.io/docs/concepts/signals/traces/) data from your generative AI applications.

### Tracing your generative AI application

The first step in continuously monitoring your application is to ensure that its telemetry data is captured and stored for analysis. To accomplish this, you'll need to instrument your generative AI application’s code to use the [Azure AI Tracing package](./develop/trace-local-sdk.md) to log trace data to an Azure Monitor Application Insights resource of your choice. This package fully conforms with the OpenTelemetry standard for observability. After you have instrumented your application's code, the trace data will be logged to your Application Insights resource.

After you have included tracing in your application code, you can view the trace data in Azure AI Foundry or in your Azure Monitor Application Insights resource. To learn more about how to do this, see [monitor your generative AI application](#monitor-your-generative-ai-application).

### Online Evaluation

After your application is instrumented to send trace data to Application Insights, it’s time to set up an Online Evaluation schedule to continuously evaluate this data. Azure AI Online Evaluation is a service that uses Azure AI compute to continuously run a set of evaluators. After you have set up an Online Evaluation schedule with the Azure AI Project SDK, it runs on a customizable schedule. Each time the service runs, it performs the following steps:

1. Query application trace data from the connected Application Insights resource using provided Kusto query.
1. Run each evaluator over the trace data and calculate each metric (for example, *groundedness: 3*).
1. Write evaluation scores back to each trace using standardized semantic conventions.

> [!NOTE]
> Azure AI Online Evaluation supports the same metrics as Azure AI Evaluation. For more information on how evaluation works and which evaluation metrics are supported, see [Evaluate your Generative AI application with the Azure AI Evaluation SDK](./develop/evaluate-sdk.md)

For example, let’s say you have a deployed chat application that receives many customer questions on a daily basis. You want to continuously evaluate the quality of the responses from your application. You set up an Online Evaluation schedule with a daily recurrence. You configure the evaluators: **Groundedness**,  **Coherence**, and **Fluency**. Every day, the service computes the evaluation scores for these metrics and writes the data back to Application Insights for each trace that was collected during the recurrence time window (in this example, the past 24 hours). Then, the data can be queried from each trace and made accessible in Azure AI Foundry and Azure Monitor Application Insights.

The evaluation results written back to each trace within Application Insights follow the following conventions. A unique span will be added to each trace for each evaluation metric.

| Property                                  | Application Insights Table | Fields for a given operation_ID               | Example value                        |
|-------------------------------------------|----------------------------|-----------------------------------------------|--------------------------------------|
| Evaluation metric                         | traces, AppTraces          | `customDimensions[“event.name”]`              | `gen_ai.evaluation.relevance`        |
| Evaluation metric score                   | traces, AppTraces          | `customDimensions[“gen_ai.evaluation.score”]` | `3`                                  |
| Evaluation metric comment (if applicable) | traces, AppTraces          | `message`                                     | `{“comment”: “I like the response”}` |

Now that you understand how Azure AI Online Evaluation works and how it connects to Azure Monitor Application Insights, it’s time to learn how to set up the service.

## Set up Online Evaluation

In this section, you'll learn how to configure an Online Evaluation schedule to continuously monitor your deployed generative AI application. Azure AI Project SDK offers such capabilities via a Python API and supports all of the features available in local evaluations. Use the following steps to submit your Online Evaluation schedule on your data using built-in or custom evaluators.

> [!NOTE]
> Evaluations are only supported in the same [regions](./develop/evaluate-sdk.md#region-support) as AI-assisted risk and safety metrics.

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
13. Make sure you're first logged into your Azure subscription by running `az login`.

### Installation Instructions

1. Create a virtual environment of your choice. To create one using conda, run the following command:

```bash
conda create -n online-evaluation
conda activate online-evaluation
```

2. Install the required packages by running the following command:

```bash
pip install azure-identity azure-ai-projects azure-ai-ml
```

> [!TIP]
> Optionally, you can `pip install azure-ai-evaluation` if you want a code-first experience to fetch evaluator id for built-in evaluators in code. To learn how to do this, see [Specifying evaluators from evaluator library](./develop/evaluate-sdk.md#specifying-evaluators-from-evaluator-library).

### Set up tracing for your generative AI application

The first step in monitoring your application is to set up tracing. To learn how to do so such that data is logged to Application Insights, see [set up tracing for your generative AI application](./develop/trace-local-sdk.md).

#### Using service name in trace data

To identify your service via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is particularly useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them. For example, lets say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Groundedness**. You can use the service name to differentiate between the applications in your Online Evaluation configurations.

To set up the service name property, you can do so directly in your application code by following the steps, see  [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` prior to deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

To query trace data for a given service name, query for the `cloud_roleName` property. Add the following line to the KQL query you use within your Online Evaluation set-up:

```sql
| where cloud_RoleName == "service_name"
```

### Query stored trace data in Application Insights

Using the [Kusto Query Language (KQL)](/kusto/query/?view=microsoft-fabric&preserve-view=true), you can query your generative AI application's trace data from Application Insights to use for continuous Online Evaluation. If you use the [Azure AI Tracing package](./develop/trace-local-sdk.md) to trace your generative AI application, you can use the following Kusto query to view the data in Application Insights:

> [!IMPORTANT]
> The KQL query used by the Online Evaluation service must output the following columns: `operation_Id`, `operation_ParentId`, and `gen_ai_response_id`. Additionally, each evaluator has its own input data requirements. The KQL query must output these columns to be used as inputs to the evaluators themselves. For a list of data requirements for evaluators, see [data requirements for built-in evaluators](./develop/evaluate-sdk.md#data-requirements-for-built-in-evaluators).

```SQL
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

Optionally, you can use the [sample operator](/kusto/query/sample-operator?view=azure-monitor&preserve-view=true) or [take operator](/kusto/query/take-operator?view=microsoft-fabric&preserve-view=true) in your Kusto query such that it only returns a subset of traces. Since AI-assisted evaluations can be costly at scale, this approach can help you control costs by only evaluating a random sample (or `n` traces) of your data.

### Set up Online Evaluation with Azure AI Project SDK

You can submit an Online Evaluation scheduled job with the Azure AI Project SDK via a Python API. See the below script to learn how to set up Online Evaluation with performance and quality (AI-assisted) evaluators. To view a comprehensive list of supported evaluators, see [Evaluate with the Azure AI Evaluation SDK](./develop/evaluate-sdk.md). To learn how to use custom evaluators, see [custom evaluators](./develop/evaluate-sdk.md#specifying-custom-evaluators).

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

# Name of your generative AI application (will be available in trace data in Application Insights)
SERVICE_NAME = "service_name"

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

Next, define a client and an Azure OpenAI GPT deployment (such as `GPT-4`) which will be used to run your Online Evaluation schedule. Also, connect to your Application Insights resource:

```python
# Connect to your Azure AI Foundry Project
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING
)

# Connect to your Application Insights resource 
app_insights_config = ApplicationInsightsConfiguration(
    resource_id=APPLICATION_INSIGHTS_RESOURCE_ID,
    query=KUSTO_QUERY,
    service_name=SERVICE_NAME
)

# Connect to your AOAI resource, you must use an AOAI GPT model
deployment_name = "gpt-4"
api_version = "2024-08-01-preview"

# This is your AOAI connection name, which can be found in your Azure AI Foundry project under the 'Models + Endpoints' tab
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

**Note: In the prerequisite steps, you created a User-assigned managed identity to authenticate the Online Evaluation schedule to your Application Insights resource. The `AzureMSIClientId` in the `properties` parameter of the `EvaluationSchedule` class is the `clientId` of this identity.**

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

#### Perform operations on an Online Evaluation schedule

You can get, list, and disable Online Evaluation schedules by adding the following code to your Online Evaluation configuration script:

**Warning: Please wait a small amount of time (~30 seconds) between creating an Online Evaluation schedule and running the `get_schedule()` API.**

Get an Online Evaluation schedule:

```python
name = "<my-online-evaluation-name>"
get_evaluation_schedule = project_client.evaluations.get_schedule(name)
```

List all Online Evaluation schedules:

```python
count = 0
for evaluation_schedule in project_client.evaluations.list_schedule():
    count += 1
        print(f"{count}. {evaluation_schedule.name} "
        f"[IsEnabled: {evaluation_schedule.is_enabled}]")
        print(f"Total evaluation schedules: {count}")
```

Disable (soft-delete) Online Evaluation schedule:

```python
name = "<my-online-evaluation-name>"
project_client.evaluations.disable_schedule(name)
```

## Monitor your generative AI application

In this section, you'll learn how Azure AI integrates with Azure Monitor Application Insights to give you an out-of-the-box dashboard view that is tailored with insights regarding your generative AI app so you can stay updated with the latest status of your application.

### Insights for your generative AI application  

If you haven’t set this up, here are some quick steps:

1. Navigate to your project in [Azure AI Foundry](https://ai.azure.com).
1. Select the Tracing page on the left-hand side.
1. Connect your Application Insights resource to your project.

If you already set up tracing in Azure AI Foundry portal, all you need to do is select the link to **Check out your Insights for Generative AI application dashboard**.

Once you have your data streaming into your Application Insights resource, you automatically can see it get populated in this customized dashboard.

:::image type="content" source="../media/how-to/online-evaluation/open-generative-ai-workbook.gif" alt-text="Animation of an Azure workbook showing Application Insights." lightbox="../media/how-to/online-evaluation/open-generative-ai-workbook.gif":::

This view is a great place for you to get started with your monitoring needs.

- You can view token consumption over time to understand if you need to increase your usage limits or do additional cost analysis.
- You can view evaluation metrics as trend lines to understand the quality of your app on a daily basis.
- You can debug when exceptions take place and drill into traces using the **Azure Monitor End-to-end transaction details view** to figure out what went wrong.

:::image type="content" source="../media/how-to/online-evaluation/custom-generative-ai-workbook.gif" alt-text="Animation of an Azure workbook showing graphs and end to end transaction details." lightbox="../media/how-to/online-evaluation/custom-generative-ai-workbook.gif":::

This is an Azure Workbook that is querying data stored in your Application Insights resource. You can customize this workbook and tailor this to fit your business needs.
To learn more, see [editing Azure Workbooks](/azure/azure-monitor/visualize/workbooks-create-workbook).

This allows you to add additional custom evaluators that you might have logged or other markdown text to share summaries and use for reporting purposes.

You can also share this workbook with your team so they stay informed with the latest!

:::image type="content" source="../media/how-to/online-evaluation/share-azure-workbook.png" alt-text="Screenshot of an Azure Workbook showing the share button and share tab." lightbox="../media/how-to/online-evaluation/share-azure-workbook.png":::

> [!NOTE]
> When sharing this workbook with your team members, they must have atleast 'Reader' role to the connected Application Insights resource to view the displayed information.

## Related content

- [Trace your application with Azure AI Inference SDK](./develop/trace-local-sdk.md)
- [Visualize your traces](./develop/visualize-traces.md)
- [Evaluation of Generative AI Models & Applications](../concepts/evaluation-approach-gen-ai.md)
- [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview)
- [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview)
