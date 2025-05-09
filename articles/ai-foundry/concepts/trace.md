---
title: Trace your application with Azure AI Foundry project library
titleSuffix: Azure AI Foundry
description: This article provides an overview of tracing with the Azure AI Foundry project library.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: conceptual
ms.date: 03/31/2025
ms.reviewer: truptiparkar
ms.author: lagayhar
author: lgayhardt
---

# Trace your application with Azure AI Foundry project library overview (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Tracing is a powerful tool that offers developers an in-depth understanding of the execution process of their generative AI applications. It provides a detailed view of the execution flow of the application. This essential information proves critical while debugging complex applications or optimizing performance.

Tracing with the Azure AI Inference SDK offers enhanced visibility and simplified troubleshooting for LLM-based applications, effectively supporting development, iteration, and production monitoring. Tracing follows the OpenTelemetry semantic conventions, capturing and visualizing the internal execution details of any AI application, enhancing the overall development experience.

## Key features

- **Enhanced Observability**: Offers clear insights into the Gen AI Application lifecycle.
- **User-Centric Design**: Simplifies telemetry enablement, focusing on improving developer workflow and productivity.
- **Seamless Instrumentation**: Seamlessly instruments Azure AI Inference API for enabling telemetry.
- **OTEL based tracing for User-defined functions**: Allows adding local variables and intermediate results to trace decorator for detailed tracing capabilities for user defined functions.
- **Secure Data Handling**: Provides options to prevent sensitive or large data logging as per open telemetry standards.
- **Feedback Logging**: Users can collect & attach user feedback and evaluative data to enrich trace data with qualitative insights.

## Concepts

### Traces

Traces record specific events or the state of an application during execution. It can include data about function calls, variable values, system events and more. Whether your application is a monolith with a single database or a sophisticated mesh of services, traces are essential to understanding the full "path" a request takes in your application. To learn more, see [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/).

### Semantic conventions

OpenTelemetry defines Semantic Conventions, sometimes called Semantic attributes, that specify common names for different kinds of operations and data. The benefit of using Semantic conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. By adhering to these conventions, Azure AI ensures that trace data is consistent and can be easily interpreted by observability tools. This consistency is crucial for effective monitoring, debugging, and optimization of Gen AI applications. To learn more, see [OpenTelemetry's Semantic Conventions for Generative AI systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

### Spans

Spans are the building blocks of traces. Each span represents a single operation within a trace, capturing the start and end time, and any attributes or metadata associated with the operation. Spans can be nested to represent hierarchical relationships, allowing developers to see the full call stack and understand the sequence of operations. To learn more, see [OpenTelemetry's Spans](https://opentelemetry.io/docs/concepts/signals/traces/#spans).

### Attributes

Attributes are key-value pairs that provide additional information about a trace or span. Attributes can be used to record contextual data such as function parameters, return values, or custom annotations. This metadata enriches the trace data, making it more informative and useful for analysis.

Attributes have the following rules that each language SDK implements:

- Keys must be non-null string values.
- Values must be a non-null string, boolean, floating point value, integer, or an array of these values.

To learn more, see [OpenTelemetry's Attributes](https://opentelemetry.io/docs/concepts/signals/traces/#attributes).

### Trace exporters

Trace exporters are responsible for sending trace data to a backend system for storage and analysis. Azure AI supports exporting traces to various observability platforms, including Azure Monitor and other OpenTelemetry-compatible backends.

### Trace visualization

Trace visualization refers to the graphical representation of trace data. Azure AI integrates with visualization tools like Azure AI Foundry Tracing, Aspire dashboard, and Prompty Trace viewer  to provide developers with an intuitive way to explore and analyze traces, helping them to quickly identify issues and understand the behavior of their applications.

## Enable tracing

In order to enable tracing, you need to add an Application Insights resource to your Azure AI Foundry project. To add an Application Insights resource, navigate to the **Tracing** tab in the [Azure AI Foundry portal](https://ai.azure.com/), and create a new resource if you don't already have one.

:::image type="content" source="../../ai-services/agents/media/ai-foundry-tracing.png" alt-text="A screenshot of the tracing screen in the Azure AI Foundry portal." lightbox="../../ai-services/agents/media/ai-foundry-tracing.png":::

## Conclusion

Azure AI's tracing capabilities are designed to empower developers with the tools they need to gain deep insights into their AI applications. By providing a robust, intuitive, and scalable tracing feature, Azure AI helps reduce debugging time, enhance application reliability, and improve overall performance. With a focus on user experience and system observability, Azure AI's tracing solution is set to revolutionize the way developers interact with and understand their Gen AI applications.

## Related content

- [Trace your application with Azure AI Foundry project library](../how-to/develop/trace-local-sdk.md)
- [Visualize your traces](../how-to/develop/visualize-traces.md)
