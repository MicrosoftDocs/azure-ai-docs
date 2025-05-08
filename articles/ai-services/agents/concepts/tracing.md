---
title: 'How to enable tracing in Azure AI Agents'
titleSuffix: Azure AI Foundry
description: Learn how to trace your AI agent's executions for debugging and evaluation.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 04/22/2025
author: aahill
ms.author: aahi
---

# Tracing agents

Determining the reasoning behind your agent's executions is important for troubleshooting and debugging. However, it can be difficult for complex agents for a number of reasons:
* There could be a high number of steps involved in generating a response, making it hard to keep track of all of them.
* The sequence of steps might vary based on user input.
* The inputs/outputs at each stage might be long and deserve more detailed inspection.
* Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Tracing solves this by allowing you to clearly see the inputs and outputs of each primitive involved in a particular agent run, in the order in which they were invoked.

## Tracing in the Azure AI Foundry Agents playground

The Agents playground in the Azure AI Foundry portal lets you trace threads and runs that your agents produce. To open a trace, select **Thread info** in an active thread. You can also optionally select **Metrics** to enable automatic evaluations of the model's performance across several dimensions of **AI quality** and **Risk and safety**. 

> [!NOTE]
> Evaluations are not available in the following regions.
> * australiaeast
> * japaneast
> * southindia
> * uksouth

:::image type="content" source="../media/ai-foundry-tracing.png" alt-text="A screenshot of the agent playground in the Azure AI Foundry portal." lightbox="../media/ai-foundry-tracing.png":::

After selecting **Thread info**, the screen that appears will be let you view the: thread, run, run steps and any tool calls that were made. You can view the inputs and outputs between the agent and user, as well the associated metadata and any evaluations you selected.

:::image type="content" source="../media/thread-trace.png" alt-text="A screenshot of a trace." lightbox="../media/thread-trace.png":::

> [!TIP]
> If you want to view the trace of a previous thread, select **Agent Playground**. Choose a thread in the **Create and debug your agents** screen, and then select **Try in playground**.
> :::image type="content" source="../media/thread-highlight.png" alt-text="A screenshot of the create and debug screen." lightbox="../media/thread-highlight.png":::
> You will be able to see the **Thread info** button at the top of the screen to view the trace. 


> [!NOTE]
> Observability features such as Risk and Safety Evaluation are billed based on consumption as listed in the [Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).


## Trace agents using OpenTelemetry and an Application Insights resource

Tracing lets you analyze your agent's performance and behavior by using OpenTelemetry and adding an Application Insights resource to your Azure AI Foundry project. 

To add an Application Insights resource, select **Observability** from the left pane in the [Azure AI Foundry portal](https://ai.azure.com/), select **Tracing**, and then and create a new resource if you don't already have one.

:::image type="content" source="../media/ai-foundry-observability.png" alt-text="A screenshot of the tracing screen in the Azure AI Foundry portal." lightbox="../media/ai-foundry-observability.png":::

Once created, you can get an Application Insights connection string, configure your agents, and observe the full execution path of your agent through Azure Monitor. Typically you want to enable tracing before you create an agent.

## Observe an agent

First, use `pip install` to install OpenTelemetry and the Azure SDK tracing plugin.

```bash
pip install opentelemetry-sdk
pip install azure-core-tracing-opentelemetry
```

You will also need an exporter to send results to your observability backend. You can print traces to the console or use a local viewer such as [Aspire Dashboard](/dotnet/aspire/fundamentals/dashboard/standalone?tabs=bash). To connect to Aspire Dashboard or another OpenTelemetry compatible backend, install the OpenTelemetry Protocol (OTLP) exporter.

```bash
pip install opentelemetry-exporter-otlp
```

Once you have the packages installed, you can use one the following Python samples to implement tracing with your agents. Samples that use console tracing display the results locally in the console. Samples that use Azure Monitor send the traces to the Azure Monitor in the [Azure AI Foundry portal](https://ai.azure.com/), in the **Observability** tab in the left pane for the portal.

> [!NOTE]
> There is a known bug in the agents tracing functionality. The bug will cause the agent's function tool to call related info (function names and parameter values, which could contain sensitive information) to be included in the traces even when content recording is not enabled.


**Using Azure Monitor**
* [Basic agent example](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_basics_with_azure_monitor_tracing.py)  
* [Agent example with function calling](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_functions_with_azure_monitor_tracing.py)
* [Example with a stream event handler](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_stream_eventhandler_with_azure_monitor_tracing.py)

**Using console tracing**
* [Basic agent example](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_basics_with_console_tracing.py)
* [Agent example with function calling](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_functions_with_console_tracing.py)
* [Example with a stream event handler](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_stream_eventhandler_with_console_tracing.py)
