---
title: How to trace AI applications using OpenAI SDK
titleSuffix: Azure AI Foundry
description: Learn how to trace applications that uses OpenAI SDK in Azure AI Foundry
author: lgayhardt
ms.author: lagayhar
manager: scottpolly
ms.reviewer: amibp
ms.date: 05/19/2025
ms.service: azure-ai-foundry
ms.topic: how-to
---

# Trace AI applications using OpenAI SDK

Tracing provides deep visibility into execution of your application by capturing detailed telemetry at each execution step. This helps diagnose issues and enhance performance by identifying problems such as inaccurate tool calls, misleading prompts, high latency, low-quality evaluation scores, and more.  

This article explains how to implement tracing for AI applications using OpenAI SDK with OpenTelemetry in Azure AI Foundry.

## Prerequisites

To complete this tutorial you need:

* An Azure AI Foundry project created.

* An AI application that uses **OpenAI SDK** to make calls to models hosted in Azure AI Foundry.


## Enable tracing in your project

Azure AI Foundry stores traces in Azure Application Insight resources using OpenTelemetry. By default, new Azure AI Foundry resources don't provision these resources. You can connect them to an existing Azure Application Insights resource or create a new one from within the project. You only need to do this once per each Azure AI Foundry resource.

The following steps show how to configure:

1. Go to [Azure AI Foundry portal](https://ai.azure.com) and navigate to your project.

2. On the side navigation bar, select **Tracing**.

3. If an Azure Application Insights resource has not been associated with your resource, associate one.

    :::image type="content" source="../../media/how-to/develop/trace-application/configure-app-insight.png" alt-text="A screenshot showing how to configure Azure Application Insights to the Azure AI Foundry resource." lightbox="../../media/how-to/develop/trace-application/configure-app-insight.png":::

4. To reuse an existing Azure Application Insights, use the drop down **Application Insights resource name** to locate the resource and select **Connect**.

    > [!TIP]
    > To connect to an existing Azure Application Insights, you need at least contributor access to the Azure AI Foundry resource (or Hub). 

5. To connect to a new Azure Application Insights resource, select the option **Create new**.

    1. Use the configuration wizard to configure the new resource's name.

    2. By default, the new resource is created in the same resource group where the Azure AI Foundry resource was created. Use the **Advance settings** option to configure a different resource group or subscription.

        > [!TIP]
        > To create a new Azure Application Insight resource, you also need contributor role to the resource group you have selected (or the default one).

    3. Select **Create** to create the resource and connect it to the Azure AI Foundry resource.

4. Once the connection is configured, you are ready to use tracing in this project.

5. Go to the landing page of your project and copy the project's endpoint URI. You'll need it later in the tutorial.

    :::image type="content" source="../../media/how-to/projects/fdp-project-overview.png" alt-text="A screenshot showing how to copy the project endpoint URI." lightbox="../../media/how-to/projects/fdp-project-overview.png":::

    > [!IMPORTANT]
    > Using a project's endpoint requires configuring Microsoft Entra ID in your application. If you don't have Entra ID configured, use the Azure Application Insights connection string as indicated in step 3 of the tutorial.


## Instrument the OpenAI SDK

If you are using the OpenAI SDK to develop intelligent applications you can instrument it so traces are sent to Azure AI Foundry. Follow this steps:

1. Install `azure-ai-projects`, `azure-monitor-opentelemetry`, and `opentelemetry-instrumentation-openai-v2` in your environment. The following example uses `pip`:

    ```console
    pip install azure-ai-projects azure-monitor-opentelemetry opentelemetry-instrumentation-openai-v2
    ```

1. Instrument the OpenAI SDK by using `OpenAIInstrumentor()`:

    ```python
    from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

    OpenAIInstrumentor().instrument()
    ```

1. Get the connection string to the Azure Application Insights resource to your project:

    ```python
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        endpoint="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>",
    )

    connection_string = project_client.telemetry.get_connection_string()
    ```

    > [!TIP]
    > Connection strings to Azure Application Insights looks like `InstrumentationKey=aaaa0a0a-bb1b-cc2c-dd3d-eeeee4e4e4e;...`. You can also access the connection string used in your project from the section **Tracing** in Azure AI Foundry portal. In the top navigation bar, select **Manage data source** and copy the **Connection string**. Configure your connection string in an environment variable.
    >
    > :::image type="content" source="../../media/how-to/develop/trace-application/tracing-copy-connection-string.png" alt-text="A screenshot showing how to copy the connection string to the underlying Azure Application Insights resource from a project." lightbox="../../media/how-to/develop/trace-application/tracing-copy-connection-string.png":::

1. We want to send tracing information to Azure AI Foundry. To do that, we need to create an OpenTelemetry exporter and configure it with the connection string to the Azure Application Insights that is used by our project.

    ```python
    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor(connection_string=connection_string)
    ```

1. By default, OpenTelemetry doesn't capture the inputs and outputs. To enable that, use the environment variable `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`. Ensure this environment variable is configure in the environment level where you code is running.

1. Use the OpenAI SDK in the same way you are used to:

    ```python
    client = project_client.get_azure_openai_client()

    response = client.chat.completions.create(
        model="deepseek-v3-0324",
        messages=[
            {"role": "user", "content": "Write a short poem on open telemetry."},
        ],
    )
    ```

1. If you go back to Azure AI Foundry portal, you should see the trace displayed:

    :::image type="content" source="../../media/how-to/develop/trace-application/tracing-display-simple.png" alt-text="A screenshot showing how a simple chat completion request is displayed in the trace." lightbox="../../media/how-to/develop/trace-application/tracing-display-simple.png":::

1. When developing complex applications, it may be useful to capture sections of your code that mixes business logic with models. You can do that by first getting an instance of the current tracer.

    ```python
    from opentelemetry import trace

    tracer = trace.get_tracer(__name__)
    ```

1. Then, use decorators in your method to capture specific scenarios in your code that you are interested in. The following example assess if a list of claims with a list of contexts.

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
                model="gpt-4.5-preview",
                messages=build_prompt_with_context(claim=claim, context=context),
            )
            responses.append(response.choices[0].message.content.strip('., '))

        return responses
    ```

1. Then, traces will look as follow:

    :::image type="content" source="../../media/how-to/develop/trace-application/tracing-display-decorator.png" alt-text="A screenshot showing how a method using a decorator is displayed in the trace." lightbox="../../media/how-to/develop/trace-application/tracing-display-decorator.png":::

1. You may also want to add extra information as attributes to the current span. Use the `trace` object to access it and include extra information. See how the `assess_claims_with_context` method has been modified to include an attribute:

    ```python
    @tracer.start_as_current_span("assess_claims_with_context")
    def assess_claims_with_context(claims, contexts):
        responses = []
        current_span = trace.get_current_span()

        current_span.set_attribute("operation.claims_count", len(claims))

        for claim, context in zip(claims, contexts):
            response = client.chat.completions.create(
                model="gpt-4.5-preview",
                messages=build_prompt_with_context(claim=claim, context=context),
            )
            responses.append(response.choices[0].message.content.strip('., '))

        return responses
    ``` 


## Trace to console

It may be useful to also trace your application and send the traces to the local execution console. Such approach may result beneficial when running unit tests or integration tests in your application using an automated CI/CD pipeline. Traces can be sent to the console and captured by your CI/CD tool to further analysis.

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

## Next steps

* [Trace agents using Azure AI Foundry SDK](trace-agents-sdk.md)