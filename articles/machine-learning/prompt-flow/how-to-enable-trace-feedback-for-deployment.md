---
title: Enable trace and collect feedback for a flow deployment
titleSuffix: Azure Machine Learning
description: Learn how to enable trace and collect feedback during inference time of a flow deployment
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 06/30/2026
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
ms.update-cycle: 365-days
ai-usage: ai-assisted
---

# Enable trace and collect feedback for a flow deployment (preview)

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

> [!NOTE]
> This feature is currently in public preview. This preview is provided without a service-level agreement, and it's not recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

After deploying a generative AI app in production, app developers seek to enhance their understanding and optimize performance. Trace data for each request, aggregated metrics, and user feedback play critical roles.

In this article, you learn how to enable trace, collect aggregated metrics, and gather user feedback during inference time of your flow deployment.

## Prerequisites

- The Azure CLI and the Azure Machine Learning extension to the Azure CLI. For more information, see [Install, set up, and use the CLI (v2)](../how-to-configure-cli.md).
- An Azure Machine Learning workspace. If you don't have one, use the steps in the [Quickstart: Create workspace resources article](../quickstart-create-resources.md) to create one.
- An Application Insights. Usually a machine learning workspace has a default linked Application Insights. If you want to use a new one, you can [create an Application Insights resource](/azure/azure-monitor/app/create-workspace-resource).
- Python 3.9 or later, if you plan to use the Python code samples in this article.
- Learn [how to build and test a flow in the prompt flow](get-started-prompt-flow.md).
- Have a basic understanding of managed online endpoints. Managed online endpoints work with powerful CPU and GPU machines in Azure in a scalable, fully managed way that frees you from the overhead of setting up and managing the underlying deployment infrastructure. For more information on managed online endpoints, see [Online endpoints and deployments for real-time inference](../concept-endpoints-online.md#online-endpoints).
- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure Machine Learning. To perform the steps in this article, your user account must be assigned the owner or contributor role for the Azure Machine Learning workspace, or a custom role allowing "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/". If you use studio to create and manage online endpoints and deployments, you need another permission "Microsoft.Resources/deployments/write" from the resource group owner. For more information, see [Manage access to an Azure Machine Learning workspace](../how-to-assign-roles.md).

## Deploy a flow for real-time inference

After you test your flow properly, either a flex flow or a DAG flow, you can deploy the flow in production. In this article, use [deploy a flow to Azure Machine Learning managed online endpoints](./how-to-deploy-to-code.md) as an example. For flex flows, you need to [prepare the `flow.flex.yaml` file instead of `flow.dag.yaml`](https://microsoft.github.io/promptflow/how-to-guides/develop-a-flex-flow/index.html).

You can also [deploy to other platforms, such as Docker container, Kubernetes cluster, and more](https://microsoft.github.io/promptflow/how-to-guides/deploy-a-flow/index.html).

> [!IMPORTANT]
> Prompt flow container images no longer receive updates, including security and package updates. If you're planning a new deployment, see the [Prompt flow migration guide](migrate-prompt-flow-to-agent-framework.md) for supported alternatives.

## Enable trace and collect system metrics for your deployment

If you use the studio UI to deploy, turn on **Application Insights diagnostics** in Advanced settings > Deployment step in the deploy wizard. This setting collects tracing data and system metrics to the workspace linked Application Insights.

If you use SDK or CLI, add the property `app_insights_enabled: true` in the deployment YAML file to collect data to the workspace linked Application Insights. You can also specify another Application Insights by using the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING` in the deployment YAML file as shown in the following example. You can find the connection string of your Application Insights in the **Overview** page in Azure portal.

```yaml
# below is the property in deployment yaml
# app_insights_enabled: true

# you can also use the environment variable
environment_variables:
  APPLICATIONINSIGHTS_CONNECTION_STRING: <connection_string>
```

> [!NOTE]
> If you set `app_insights_enabled: true` but your workspace doesn't have a linked Application Insights, your deployment doesn't fail but no data is collected.
>
> If you specify both `app_insights_enabled: true` and the preceding environment variable at the same time, the tracing data and metrics are sent to the workspace linked Application Insights. To specify a different Application Insights, keep only the environment variable.
> 
> If you deploy to other platforms, you can also use the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING: <connection_string>` to collect trace data and metrics to the specified Application Insights.

## View tracing data in Application Insights

Traces record specific events or the state of an application during execution. They can include data about function calls, variable values, system events, and more. Traces help break down an application's components into discrete inputs and outputs, which is crucial for debugging and understanding an application. To learn more, see [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/). The trace data follows [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/).

You can view the detailed trace in the specified Application Insights. The following screenshot shows an example of an event of a deployed flow containing multiple nodes. In Application Insights, select **Search** under the **Investigate** category in the resource menu. Select each node to view its detailed trace.

The **Dependency** type events record calls from your deployments. The name of that event is the name of the flow folder. To learn more, see [Transaction search and diagnostics in Application Insights](/azure/azure-monitor/app/transaction-search-and-diagnostics).

:::image type="content" source="./media/how-to-enable-trace-feedback-for-deployment/tracing-app-insights.png" alt-text="Screenshot of tracing data in application insights. " lightbox = "./media/how-to-enable-trace-feedback-for-deployment/tracing-app-insights.png":::


## View system metrics in Application Insights

| Metrics Name                         | Type      | Dimensions                                | Description                                                                     |
|--------------------------------------|-----------|-------------------------------------------|---------------------------------------------------------------------------------|
| token_consumption                    | counter   | - flow <br> - node<br> - llm_engine<br> - token_type:  `prompt_tokens`: LLM API input tokens;  `completion_tokens`: LLM API response tokens; `total_tokens` = `prompt_tokens + completion tokens`          | OpenAI token consumption metrics                                                |
| flow_latency                         | histogram | flow, response_code, streaming, response_type| request execution cost, response_type means whether it's full/firstbyte/lastbyte|
| flow_request                         | counter   | flow, response_code, exception, streaming    | flow request count                                                              |
| node_latency                         | histogram | flow, node, run_status                      | node execution cost                                                             |
| node_request                         | counter   | flow, node, exception, run_status            | node execution count                                                    |
| rpc_latency                          | histogram | flow, node, api_call                        | rpc cost                                                                        |
| rpc_request                          | counter   | flow, node, api_call, exception              | rpc count                                                                       |
| flow_streaming_response_duration     | histogram | flow                                      | streaming response sending cost, from sending first byte to sending last byte   |

You can find the workspace default Application Insights in your workspace overview page in Azure portal.

Open Application Insights, and select **Usage and estimated cost** from the left navigation. Under **Send custom metrics to Azure Metric Store**, select **With dimensions**, and save the change.

:::image type="content" source="./media/how-to-enable-trace-feedback-for-deployment/enable-multidimensional-metrics.png" alt-text="Screenshot of enable multidimensional metrics. " lightbox = "./media/how-to-enable-trace-feedback-for-deployment/enable-multidimensional-metrics.png":::

Select **Metrics** tab in the left navigation. Select **promptflow standard metrics** from the **Metric Namespace**, and you can explore the metrics from the **Metric** dropdown list with different aggregation methods.

:::image type="content" source="./media/how-to-enable-trace-feedback-for-deployment/prompt-flow-metrics.png" alt-text="Screenshot of prompt flow endpoint metrics. " lightbox = "./media/how-to-enable-trace-feedback-for-deployment/prompt-flow-metrics.png":::


## Collect feedback and send to Application Insights

Prompt flow serving provides a new `/feedback` API to help you collect feedback. The feedback payload can be any JSON format data. PF serving just helps you save the feedback data to a trace span. The data is saved to the trace exporter target you configure. It also supports OpenTelemetry standard trace context propagation, so it respects the trace context set in the request header and uses that context as the request parent span context. You can leverage the distributed tracing functionality to correlate the feedback trace to its chat request trace. 

The following sample code shows how to score a flow deployed managed endpoint enabled tracing and send the feedback to the same trace span of scoring request. The flow has inputs `question` and `chat_history`, and output `answer`. After scoring the endpoint, you collect feedback and send it to Application Insights specified when deploying the flow. You need to fill in the `api_key` value or modify the code according to your use case.

```python
import urllib.request
import json
import os
from opentelemetry import trace, context
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider

# Initialize your tracer
tracer = trace.get_tracer("my.genai.tracer")
trace.set_tracer_provider(TracerProvider())

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://learn.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data = {
    "question": "hello",
    "chat_history": []
}

body = str.encode(json.dumps(data))

url = 'https://basic-chat-endpoint.eastus.inference.ml.azure.com/score'
feedback_url = 'https://basic-chat-endpoint.eastus.inference.ml.azure.com/feedback'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = ''
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
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

        # Now you can process the answer and collect feedback
        feedback = "thumbdown"  # Example feedback (modify as needed)

        # Make another request to save the feedback
        feedback_body = str.encode(json.dumps(feedback))
        feedback_req = urllib.request.Request(feedback_url, feedback_body, headers)
        urllib.request.urlopen(feedback_req)


except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))

```

You can view the trace of the request along with feedback in Application Insights.

:::image type="content" source="./media/how-to-enable-trace-feedback-for-deployment/feedback-trace.png" alt-text="Screenshot of feedback and trace data of a request in Application Insights. " lightbox = "./media/how-to-enable-trace-feedback-for-deployment/feedback-trace.png":::


## Advanced usage: Export trace to custom OpenTelemetry collector service

In some cases, you might want to export the trace data to your deployed OTel collector service. Enable this export by setting `OTEL_EXPORTER_OTLP_ENDPOINT`. Use this exporter when you want to customize your own span processing logic and your own trace persistent target.

## Next steps

- [Migrate prompt flow to Microsoft Agent Framework](migrate-prompt-flow-to-agent-framework.md)
- [Troubleshoot errors of managed online endpoints](./how-to-troubleshoot-prompt-flow-deployment.md)
