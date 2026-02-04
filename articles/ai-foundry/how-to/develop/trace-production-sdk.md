---
title: Enable Tracing and Collect Feedback for a Flow Deployment
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to enable tracing and collect feedback for a flow deployment in the Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - hub-only
ms.topic: how-to
ms.date: 01/30/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Enable tracing and collect feedback for a flow deployment

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

After you deploy a generative AI application in production, you might want to enhance your understanding and optimize performance. Trace data for each request, aggregated metrics, and user feedback all play critical roles.

In this article, you learn to enable tracing, collect aggregated metrics, and collect user feedback during the inference time of your flow deployment.

> [!NOTE]
> For an improved way to perform continuous monitoring of deployed applications (other than prompt flow), consider using [Azure AI online evaluation](../monitor-applications.md).

## Prerequisites

[!INCLUDE [hub-only-prereq](../../includes/hub-only-prereq.md)]

- The Azure CLI and the Azure Machine Learning extension to the Azure CLI.
- A Microsoft Foundry project. If you don't already have a project, you can [create one](../../how-to/create-projects.md).
- An Application Insights resource. If you don't already have an Application Insights resource, you can [create one](/azure/azure-monitor/app/create-workspace-resource).
- Azure role-based access controls are used to grant access to operations in Azure Machine Learning. To perform the steps in this article, you must have Owner or Contributor permissions on the selected resource group. For more information, see [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md).

## Deploy a flow for real-time inference

After you test your flow properly (either a flex flow or a DAG flow), you can deploy the flow in production. In this article, we use [Deploy a flow for real-time inference](../../how-to/flow-deploy.md) as the example. For flex flows, you need to [prepare the `flow.flex.yaml` file instead of `flow.dag.yaml`](https://microsoft.github.io/promptflow/how-to-guides/develop-a-flex-flow/index.html).

You can also [deploy to other platforms, such as Docker container and Kubernetes cluster](https://microsoft.github.io/promptflow/how-to-guides/deploy-a-flow/index.html).

Use the latest prompt flow base image to deploy the flow so that it supports the tracing and feedback collection API.

## Enable trace and collect system metrics for your deployment

If you're using the Foundry portal to deploy, select **Deployment** > **Application Insights diagnostics** > **Advanced settings** in the deployment wizard. By using this method, you collect tracing data and system metrics to the project linked to Application Insights.

If you're using the SDK or the CLI, add the `app_insights_enabled: true` property in the deployment .yaml file to collect data to the project linked to Application Insights.

```yaml
app_insights_enabled: true
```

You can also specify other application insights by the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING` in the deployment .yaml file. You can find the connection string for Application Insights on the **Overview** page in the Azure portal.

```yaml
environment_variables:
  APPLICATIONINSIGHTS_CONNECTION_STRING: <connection_string>
```

> [!NOTE]
> If you set only `app_insights_enabled: true` but your project doesn't have a linked Application Insights resource, your deployment doesn't fail but no data is collected.
>
> If you specify both `app_insights_enabled: true` and the previous environment variable at the same time, the tracing data and metrics are sent to the project linked to Application Insights. If you want to specify different application insights, keep the environment variable only.
> 
> If you deploy to other platforms, you can also use the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING: <connection_string>` to collect trace data and metrics to the application insights that you specified.

## View tracing data in Application Insights

Traces record specific events or the state of an application during execution. They can include data about function calls, variable values, and system events. Traces help to break down an application's components into discrete inputs and outputs. This process is crucial for debugging and understanding an application. To learn more about traces, see [this website](https://opentelemetry.io/docs/concepts/signals/traces/). The trace data follows the [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/).

You can view the detailed trace in the application insights that you specified. The following screenshot shows an example of an event of a deployed flow that contains multiple nodes. Select **Application Insights** > **Investigate** > **Transaction search**, and then select each node to view its detailed trace.

The **Dependency** type event records calls from your deployments. The name of the event is the name of the flow folder. To learn more, see [Transaction search and diagnostics in Application Insights](/azure/azure-monitor/app/transaction-search-and-diagnostics).

## View system metrics in Application Insights

| Metric name                         | Type      | Dimensions                                | Description                                                                     |
|--------------------------------------|-----------|-------------------------------------------|---------------------------------------------------------------------------------|
| `token_consumption`                    | counter   | - `flow` <br> - `node`<br> - `llm_engine`<br> - `token_type`:  `prompt_tokens`: LLM API input tokens;  `completion_tokens`: LLM API response tokens; `total_tokens` = `prompt_tokens + completion tokens`          | OpenAI token consumption metrics.                                                |
| `flow_latency`                         | histogram | `flow`, `response_code`, `streaming`, `response_type` | The request execution cost, `response_type`, means whether it's full or first byte or last byte.|
| `flow_request`                         | counter   | `flow`, `response_code`, `exception`, `streaming`    | The flow request count.                                                              |
| `node_latency`                         | histogram | `flow`, `node`, `run_status`                      | The node execution cost.                                                             |
| `node_request`                         | counter   | `flow`, `node`, `exception`, `run_status`            | The node execution count.                                                    |
| `rpc_latency`                          | histogram | `flow`, `node`, `api_call`                        | The Remote Procedure Call cost.                                                                        |
| `rpc_request`                          | counter   | `flow`, `node`, `api_call`, `exception`              | The Remote Procedure Call count.                                                                       |
| `flow_streaming_response_duration`     | histogram | `flow`                                      | The streaming response sending cost, ranging from sending the first byte to sending the last byte.   |

You can find the workspace default Application Insights metrics on your workspace overview page in the Azure portal.

1. Open Application Insights and select **Usage and estimated costs** in the left pane. Select **Custom metrics (Preview)** > **With dimensions**, and save the change.
1. Select the **Metrics** tab in the left pane. From **Metric Namespace**, select **promptflow standard metrics**. You can explore the metrics from the **Metric** dropdown list with different aggregation methods.

## Collect feedback and send to Application Insights

Prompt flow serving provides a new `/feedback` API to help customers collect the feedback. The feedback payload can be any JSON format data. Prompt flow serving helps the customer save the feedback data to a trace span. Data is saved to the trace exporter target that the customer configured. Prompt flow serving also supports OpenTelemetry standard trace context propagation. It respects the trace context set in the request header and uses that context as the request parent span context. You can use the distributed tracing functionality to correlate the feedback trace to its chat request trace.

The following sample code shows how to score a flow deployed to a managed endpoint that was enabled for tracing and send the feedback to the same trace span of a scoring request. The flow has the inputs `question` and `chat_history`. The output is `answer`. After the endpoint is scored, feedback is collected and sent to Application Insights as specified when you deploy the flow.

```python
import urllib.request
import json
import os
import ssl
from opentelemetry import trace, context
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider

# Initialize your tracer.
tracer = trace.get_tracer("my.genai.tracer")
trace.set_tracer_provider(TracerProvider())

# Request data goes here.
# The example below assumes JSON formatting, which might be updated
# depending on the format your endpoint expects.
data = {
    "question": "hello",
    "chat_history": []
}

body = str.encode(json.dumps(data))

url = 'https://basic-chat-endpoint-0506.eastus.inference.ml.azure.com/score'
feedback_url = 'https://basic-chat-endpoint-0506.eastus.inference.ml.azure.com/feedback'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint.
api_key = ''
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules.
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'basic-chat-deployment' }

try:
    with tracer.start_as_current_span('genai-request') as span:

        ctx = context.get_current()
        TraceContextTextMapPropagator().inject(headers, ctx)
        print(headers)
        print(ctx)
        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)

        # Now you can process the answer and collect feedback.
        feedback = "thumbdown"  # Example feedback (modify as needed).

        # Make another request to save the feedback.
        feedback_body = str.encode(json.dumps(feedback))
        feedback_req = urllib.request.Request(feedback_url, feedback_body, headers)
        urllib.request.urlopen(feedback_req)


except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure.
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))

```

You can view the trace of the request along with feedback in Application Insights.

## Advanced usage: Export trace to custom OpenTelemetry collector service

In some cases, you might want to export the trace data to your deployed OpenTelemetry collector service. To enable this service, set `OTEL_EXPORTER_OTLP_ENDPOINT`. Use this exporter when you want to customize your own span processing logic and your own trace persistent target.

## Related content

- [Get started building a chat app by using the prompt flow SDK](../../quickstarts/get-started-code.md)
- [Work with the Foundry for Visual Studio Code extension (Preview)](get-started-projects-vs-code.md)
