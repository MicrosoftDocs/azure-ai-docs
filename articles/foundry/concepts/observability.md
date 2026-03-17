---
title: "Observability in Generative AI"
description: "Learn how Microsoft Foundry enables safe, high-quality generative AI through systematic evaluation and observability tools."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 02/10/2026
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
  - doc-kit-assisted
---

# Observability in generative AI
[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The AI application lifecycle requires robust evaluation frameworks to ensure AI systems deliver accurate, relevant, and reliable outputs. Without rigorous assessment, AI systems risk generating responses that are inaccurate, inconsistent, poorly grounded, or potentially harmful. Observability enables teams to measure and improve both the quality and safety of AI outputs throughout the development lifecycle—from model selection through production monitoring.

[!INCLUDE [evaluation-preview](../includes/evaluation-preview.md)]

## What is observability?

AI observability refers to the ability to monitor, understand, and troubleshoot AI systems throughout their lifecycle. Teams can trace, evaluate, integrate automated quality gates into CI/CD pipelines, and collect signals such as evaluation metrics, logs, traces, and model outputs to gain visibility into performance, quality, safety, and operational health.

## Core observability capabilities

Microsoft Foundry provides three core capabilities that work together to deliver comprehensive observability across the AI application lifecycle:

### Evaluation

Evaluators measure the quality, safety, and reliability of AI responses throughout development. Microsoft Foundry provides built-in evaluators for general-purpose quality metrics (coherence, fluency), RAG-specific metrics (groundedness, relevance), safety and security (hate/unfairness, violence, protected materials), and agent-specific metrics (tool call accuracy, task completion). Teams can also build custom evaluators tailored to their domain-specific requirements.

For a complete list of built-in evaluators, see [Built-in evaluators reference](built-in-evaluators.md).

### Monitoring (preview)

Production monitoring ensures your deployed AI applications maintain quality and performance in real-world conditions. Integrated with Azure Monitor Application Insights, Microsoft Foundry delivers real-time dashboards tracking operational metrics, token consumption, latency, error rates, and quality scores. Teams can set up alerts when outputs fail quality thresholds or produce harmful content, enabling rapid issue resolution.

For details on setting up production monitoring, see [Monitor agents dashboard](../observability/how-to/how-to-monitor-agents-dashboard.md).

### Tracing (preview)

Distributed tracing captures the execution flow of AI applications, providing visibility into LLM calls, tool invocations, agent decisions, and inter-service dependencies. Built on OpenTelemetry standards and integrated with Application Insights, tracing enables debugging complex agent behaviors, identifying performance bottlenecks, and understanding multi-step reasoning chains. Microsoft Foundry supports tracing for popular frameworks including LangChain, Semantic Kernel, and the OpenAI Agents SDK.

For guidance on implementing tracing, see [Trace your application](../../foundry-classic/how-to/develop/trace-application.md) and [Trace with Agents SDK](../../foundry-classic/how-to/develop/trace-agents-sdk.md).

## What are evaluators?

Evaluators are specialized tools that measure the quality, safety, and reliability of AI responses throughout the development lifecycle.

For a complete list of built-in evaluators, see [Built-in evaluators reference](built-in-evaluators.md).

Evaluators integrate into each stage of the AI lifecycle to ensure reliability, safety, and effectiveness.

:::image type="content" source="../media/evaluations/lifecycle.png" alt-text="Diagram of AI application lifecycle, showing model selection, building an AI application, and operationalizing." lightbox="../media/evaluations/lifecycle.png":::

## The three stages of AI application lifecycle evaluation

### Base model selection

Select the right foundation model by comparing quality, task performance, ethical considerations, and safety profiles across different models.

**Tools available**: [Microsoft Foundry benchmark](model-benchmarks.md) for comparing models on public datasets or your own data, and the Azure AI Evaluation SDK for [testing specific model endpoints](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

### Pre-production evaluation

Before deployment, thorough testing ensures your AI agent or application is production-ready. This stage validates performance through evaluation datasets, identifies edge cases, assesses robustness, and measures key metrics including task adherence, groundedness, relevance, and safety. For building production-ready agents with multi-turn conversations, tool calling, and state management, see [Foundry Agent Service](../agents/overview.md).

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of Pre-production evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

**Evaluation tools and approaches:**

- **Bring your own data**: Evaluate AI applications using your own data with quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md). Use the [Foundry portal](../how-to/evaluate-generative-ai-app.md) evaluation wizard or [Foundry SDK](../how-to/develop/cloud-evaluation.md) and [view results in the Foundry portal](../how-to/evaluate-results.md).

- **AI red teaming agent**: The [AI red teaming agent](../how-to/develop/run-ai-red-teaming-cloud.md) simulates complex attacks using Microsoft's PyRIT framework to identify safety and security vulnerabilities before deployment. Best used with human-in-the-loop processes.

### Post-production monitoring

After deployment, [continuous monitoring](../observability/how-to/how-to-monitor-agents-dashboard.md) ensures your AI application maintains quality in real-world conditions:

- **Operational metrics**: Regular measurement of key AI agent operational metrics
- **Continuous evaluation**: Quality and safety evaluation of production traffic at a sampled rate
- **Scheduled evaluation**: Scheduled quality and safety evaluation using test datasets to detect system drift
- **Scheduled red teaming**: Scheduled adversarial testing to probe for safety and security vulnerabilities
- **Azure Monitor alerts**: Notifications when outputs fail quality thresholds or produce harmful content

Integrated with Azure Monitor Application Insights, the Foundry Observability dashboard delivers real-time insights into performance, safety, and quality metrics, enabling rapid issue resolution and maintaining user trust.

## Evaluation cheat sheet

| Purpose | Process | Parameters, guidance, and samples |
| -----| -----| ----|
| How to set up tracing? | Configure distributed tracing | [Trace overview](../observability/concepts/trace-agent-concept.md) <br></br> [Trace with Agents SDK](../observability/how-to/trace-agent-setup.md) |
| What are you evaluating for? | Identify or build relevant evaluators | [Built-in evaluators](built-in-evaluators.md) <br></br> [Custom evaluators](./evaluation-evaluators/custom-evaluators.md) <br></br> [Python SDK samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md) <br></br> [C# SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/tests/Samples/Evaluation) |
| What data should you use? | Upload or generate relevant dataset | [Select or create a dataset](../how-to/evaluate-generative-ai-app.md#select-or-create-a-dataset) |
| How to run evaluations? | Run evaluation | [Agent evaluation runs](../observability/how-to/evaluate-agent.md) <br></br> [Remote cloud run](../how-to/develop/cloud-evaluation.md) |
| How did my model/AI application perform? | Analyze results | [View evaluation results](../how-to/evaluate-results.md) <br></br> [Cluster analysis](../observability/how-to/cluster-analysis.md) |
| How can I improve? | Analyze results and optimize agents | Analyze evaluation failures with [cluster analysis](../observability/how-to/cluster-analysis.md). <br></br> Optimize agents and [re-evaluate](../observability/how-to/evaluate-agent.md). <br></br> Review [evaluation results](../how-to/evaluate-results.md). |

## Region support, rate limits, and virtual network support

To learn which regions support AI-assisted evaluators, the rate limits that apply to evaluation runs, and how to configure virtual network support for network isolation, see [region support, rate limits, and virtual network support for evaluation](evaluation-regions-limits-virtual-network.md).

## Pricing

Observability features such as risk and safety evaluations and evaluations in the agent playground are billed based on consumption as listed in [our Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

[!INCLUDE [evaluations-agent-playground](../includes/evaluations-agent-playground.md)]

## Related content

- [Built-in evaluators reference](built-in-evaluators.md)
- [Virtual network support for evaluation](evaluation-regions-limits-virtual-network.md)
- [Foundry control plane](../control-plane/overview.md)
- [Evaluate generative AI apps by using Foundry](../how-to/evaluate-generative-ai-app.md)
- [See evaluation results in the Foundry portal](../how-to/evaluate-results.md)
- [Foundry Transparency Note](safety-evaluations-transparency-note.md)
