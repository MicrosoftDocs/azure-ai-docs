---
title: View Trace Results for AI Applications using OpenAI SDK
titleSuffix: Microsoft Foundry
description: View trace results for AI applications using OpenAI SDK with OpenTelemetry in Microsoft Foundry. See execution traces, diagnose issues, and monitor application performance.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ai-usage: ai-assisted
---

# View trace results for AI applications using OpenAI SDK

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Learn how to view trace results that provide visibility into AI application execution. Use traces to diagnose inaccurate tool calls, misleading prompts, latency bottlenecks, and low-quality evaluation scores.

In this article, you learn how to:

- Enable tracing for a project.
- Instrument the OpenAI SDK.
- Capture message content (optional).
- View trace timelines and spans.
- Connect tracing with evaluation loops.

This article explains how to view trace results for AI applications using **OpenAI SDK** with OpenTelemetry in Microsoft Foundry.

## Prerequisites

You need the following to complete this tutorial:

* A Foundry project created.

* An AI application that uses **OpenAI SDK** to make calls to models hosted in Foundry.

## Enable tracing in your project

Foundry stores traces in Azure Application Insights using OpenTelemetry. New resources don't provision Application Insights automatically. Associate (or create) a resource once per Foundry resource.

The following steps show how to configure your resource:

1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs) and navigate to your project.

1. On the side navigation bar, select **Tracing**.

1. If an Azure Application Insights resource isn't associated with your Foundry resource, associate one. If you already have an Application Insights resource associated, you won't see the enable page below and you can skip this step.

    :::image type="content" source="../../media/how-to/develop/trace-application/configure-app-insight.png" alt-text="A screenshot showing how to configure Azure Application Insights to the Foundry resource." lightbox="../../media/how-to/develop/trace-application/configure-app-insight.png":::

    1. To reuse an existing Azure Application Insights, use the drop-down **Application Insights resource name** to locate the resource and select **Connect**.

        > [!TIP]
        > To connect to an existing Azure Application Insights, you need at least contributor access to the Foundry resource (or Hub).

    1. To connect to a new Azure Application Insights resource, select the option **Create new**.

        1. Use the configuration wizard to configure the new resource's name.

        1. By default, the new resource is created in the same resource group where the Foundry resource was created. Use the **Advance settings** option to configure a different resource group or subscription.

            > [!TIP]
            > To create a new Azure Application Insights resource, you also need contributor role to the resource group you selected (or the default one).

        1. Select **Create** to create the resource and connect it to the Foundry resource.

    1. Once the connection is configured, you're ready to use tracing in any project within the resource.

    > [!TIP]
    > Make sure you have the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader) assigned in your Application Insights resource. To learn more on how to assign roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal). Use [Microsoft Entra groups](../../concepts/rbac-foundry.md#use-microsoft-entra-groups-with-foundry) to more easily manage access for users.

1. Go to the landing page of your project and copy the project's endpoint URI. You need it later.

    :::image type="content" source="../../media/how-to/projects/fdp-project-overview.png" alt-text="A screenshot showing how to copy the project endpoint URI." lightbox="../../media/how-to/projects/fdp-project-overview.png":::

    > [!IMPORTANT]
    > Using a project's endpoint requires configuring Microsoft Entra ID in your application. If you don't have Entra ID configured, use the Azure Application Insights connection string as indicated in step 3 of the tutorial.

## View trace results in Foundry portal

Once you have tracing configured and your application is instrumented, you can view trace results in the Foundry portal:

1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs) and navigate to your project.

1. On the side navigation bar, select **Tracing**.

1. You'll see a list of trace results from your instrumented applications. Each trace shows:
   - **Trace ID**: Unique identifier for the trace
   - **Start time**: When the trace began
   - **Duration**: How long the operation took
   - **Status**: Success or failure status
   - **Operations**: Number of spans in the trace

1. Select any trace to view detailed trace results including:
   - Complete execution timeline
   - Input and output data for each operation
   - Performance metrics and timing
   - Error details if any occurred
   - Custom attributes and metadata

## Instrument the OpenAI SDK

When developing with the OpenAI SDK, you can instrument your code so traces are sent to Foundry. Follow these steps to instrument your code:

1. Install packages:

    ```bash
    pip install azure-ai-projects azure-monitor-opentelemetry opentelemetry-instrumentation-openai-v2
    ```

2. (Optional) Capture message content:

    - PowerShell: `setx OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT true`
    - Bash: `export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`

3. Get the connection string for the linked Application Insights resource (Project > Tracing > Manage data source > Connection string):

    ```python
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    project_client = AIProjectClient(
         credential=DefaultAzureCredential(),
         endpoint="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>",
    )
    connection_string = project_client.telemetry.get_application_insights_connection_string()
    ```

4. Configure Azure Monitor and instrument OpenAI SDK:

    ```python
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

    configure_azure_monitor(connection_string=connection_string)
    OpenAIInstrumentor().instrument()
    ```

5. Send a request:

    ```python
    client = project_client.get_openai_client()
    response = client.chat.completions.create(
         model="gpt-4o-mini", 
         messages=[{"role": "user", "content": "Write a short poem on open telemetry."}],
    )
    print(response.choices[0].message.content)
    ```

6. Return to **Tracing** in the portal to view new traces.

    :::image type="content" source="../../media/how-to/develop/trace-application/tracing-display-simple.png" alt-text="Screenshot that shows a trace view of a chat completion request showing spans and latency." lightbox="../../media/how-to/develop/trace-application/tracing-display-simple.png":::

7. It might be useful to capture sections of your code that mixes business logic with models when developing complex applications. OpenTelemetry uses the concept of spans to capture sections you're interested in. To start generating your own spans, get an instance of the current **tracer** object.

    ```python
    from opentelemetry import trace

    tracer = trace.get_tracer(__name__)
    ```

8. Then, use decorators in your method to capture specific scenarios in your code that you're interested in. These decorators generate spans automatically. The following code example instruments a method called `assess_claims_with_context` that iterates over a list of claims and verifies if the claim is supported by the context using an LLM. All the calls made in this method are captured within the same span:

    ```python
    def build_prompt_with_context(claim: str, context: str) -> str:
        return [{'role': 'system', 'content': "I will ask you to assess whether a particular scientific claim, based on evidence provided. Output only the text 'True' if the claim is true, 'False' if the claim is false, or 'NEE' if there's not enough evidence."},
                {'role': 'user', 'content': f"""
                    The evidence is the following: {context}

                    Assess the following claim on the basis of the evidence. Output only the text 'True' if the claim is true, 'False' if the claim is false, or 'NEE' if there's not enough evidence. Do not output any other text.

                    Claim:
                    {claim}

                    Assessment:
                """}]

    @tracer.start_as_current_span("assess_claims_with_context")
    def assess_claims_with_context(claims, contexts):
        responses = []
        for claim, context in zip(claims, contexts):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=build_prompt_with_context(claim=claim, context=context),
            )
            responses.append(response.choices[0].message.content.strip('., '))

        return responses
    ```

9. Trace results look as follows:

    :::image type="content" source="../../media/how-to/develop/trace-application/tracing-display-decorator.png" alt-text="A screenshot showing how a method using a decorator is displayed in the trace." lightbox="../../media/how-to/develop/trace-application/tracing-display-decorator.png":::

10. You might also want to add extra information to the current span. OpenTelemetry uses the concept of **attributes** for that. Use the `trace` object to access them and include extra information. See how the `assess_claims_with_context` method has been modified to include an attribute:

    ```python
    @tracer.start_as_current_span("assess_claims_with_context")
    def assess_claims_with_context(claims, contexts):
        responses = []
        current_span = trace.get_current_span()

        current_span.set_attribute("operation.claims_count", len(claims))

        for claim, context in zip(claims, contexts):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=build_prompt_with_context(claim=claim, context=context),
            )
            responses.append(response.choices[0].message.content.strip('., '))

        return responses
    ```

## Trace to console

It might be useful to also trace your application and send the traces to the local execution console. This approach might be beneficial when running unit tests or integration tests in your application using an automated CI/CD pipeline. Traces can be sent to the console and captured by your CI/CD tool for further analysis.

Configure tracing as follows:

1. Instrument the OpenAI SDK as usual:

    ```python
    from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

    OpenAIInstrumentor().instrument()
    ```

1. Configure OpenTelemetry to send traces to the console:

    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

    span_exporter = ConsoleSpanExporter()
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)
    ```

1. Use OpenAI SDK as usual:

    ```python
    response = client.chat.completions.create(
        model="deepseek-v3-0324",
        messages=[
            {"role": "user", "content": "Write a short poem on open telemetry."},
        ],
    )
    ```

    ```console
    {
        "name": "chat deepseek-v3-0324",
        "context": {
            "trace_id": "0xaaaa0a0abb1bcc2cdd3d",
            "span_id": "0xaaaa0a0abb1bcc2cdd3d",
            "trace_state": "[]"
        },
        "kind": "SpanKind.CLIENT",
        "parent_id": null,
        "start_time": "2025-06-13T00:02:04.271337Z",
        "end_time": "2025-06-13T00:02:06.537220Z",
        "status": {
            "status_code": "UNSET"
        },
        "attributes": {
            "gen_ai.operation.name": "chat",
            "gen_ai.system": "openai",
            "gen_ai.request.model": "deepseek-v3-0324",
            "server.address": "my-project.services.ai.azure.com",
            "gen_ai.response.model": "DeepSeek-V3-0324",
            "gen_ai.response.finish_reasons": [
                "stop"
            ],
            "gen_ai.response.id": "aaaa0a0abb1bcc2cdd3d",
            "gen_ai.usage.input_tokens": 14,
            "gen_ai.usage.output_tokens": 91
        },
        "events": [],
        "links": [],
        "resource": {
            "attributes": {
                "telemetry.sdk.language": "python",
                "telemetry.sdk.name": "opentelemetry",
                "telemetry.sdk.version": "1.31.1",
                "service.name": "unknown_service"
            },
            "schema_url": ""
        }
    }
    ```

## Trace locally with AI Toolkit

AI Toolkit offers a simple way to trace locally in VS Code. It uses a local OTLP-compatible collector, making it perfect for development and debugging without needing cloud access.

The toolkit supports the OpenAI SDK and other AI frameworks through OpenTelemetry. You can see traces instantly in your development environment.

For detailed setup instructions and SDK-specific code examples, see [Tracing in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing).

## Related content

- [Trace agents using Microsoft Foundry SDK](trace-agents-sdk.md)
