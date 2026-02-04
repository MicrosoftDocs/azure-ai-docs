---
title: Observability in Generative AI
titleSuffix: Microsoft Foundry
description: Learn how Microsoft Foundry enables safe, high-quality generative AI through systematic evaluation and observability tools.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 01/16/2026
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - build-aifnd
  - build-2025
---

# Observability in generative AI

[!INCLUDE [version-banner](../includes/version-banner.md)]  

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The AI application lifecycle requires robust evaluation frameworks to ensure AI systems deliver accurate, relevant, and reliable outputs. Without rigorous assessment, AI systems risk generating responses that are inaccurate, inconsistent, poorly grounded, or potentially harmful. Observability enables teams to measure and improve both the quality and safety of AI outputs throughout the development lifecycle—from model selection through production monitoring.

[!INCLUDE [evaluation-preview](../includes/evaluation-preview.md)]

## What is observability?

AI observability refers to the ability to monitor, understand, and troubleshoot AI systems throughout their lifecycle. It involves collecting and analyzing signals such as evaluation metrics, logs, traces, and model and agent outputs to gain visibility into performance, quality, safety, and operational health.

## What are evaluators?

Evaluators are specialized tools that measure the quality, safety, and reliability of AI responses throughout the development lifecycle. The following evaluators provide comprehensive assessment capabilities:

### General purpose

| Evaluator | Purpose | Inputs |
|--|--|--|
| Coherence | Measures logical consistency and flow of responses.| Query, response |
| Fluency | Measures natural language quality and readability. | Response  |
| QA | Measures comprehensively various quality aspects in question-answering.| Query, context, response, ground truth |

To learn more, see [General purpose evaluators](./evaluation-evaluators/general-purpose-evaluators.md).

### Textual similarity

| Evaluator | Purpose | Inputs |
|--|--|--|
| Similarity | AI-assisted textual similarity measurement. | Query, context, ground truth |
| F1 Score | Harmonic mean of precision and recall in token overlaps between response and ground truth. | Response, ground truth |
| BLEU | Bilingual Evaluation Understudy score for translation quality measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| GLEU | Google-BLEU variant for sentence-level assessment measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| METEOR | Metric for Evaluation of Translation with Explicit Ordering measures overlaps in n-grams between response and ground truth. | Response, ground truth |

To learn more, see [Textual similarity evaluators](./evaluation-evaluators/textual-similarity-evaluators.md)

### RAG (retrieval augmented generation)

| Evaluator | Purpose | Inputs |
|--|--|--|
| Retrieval | Measures how effectively the system retrieves relevant information. | Query, context |
| Document Retrieval| Measures accuracy in retrieval results given ground truth. | Ground truth, retrieved documents |
| Groundedness | Measures how consistent the response is with respect to the retrieved context. |  Query (optional), context, response |
| Groundedness Pro (preview) | Measures whether the response is consistent with respect to the retrieved context. | Query, context, response |
| Relevance | Measures how relevant the response is with respect to the query. | Query, response| 
| Response Completeness | Measures to what extent the response is complete (not missing critical information) with respect to the ground truth. | Response, ground truth |

To learn more, see [Retrieval-augmented Generation (RAG) evaluators](./evaluation-evaluators/rag-evaluators.md).

### Safety and security

| Evaluator | Purpose | Inputs |
|--|--|--|
| Hate and Unfairness | Identifies biased, discriminatory, or hateful content. | Query, response |
| Sexual | Identifies inappropriate sexual content. | Query, response |
| Violence | Detects violent content or incitement. | Query, response |
| Self-Harm | Detects content promoting or describing self-harm.| Query, response |
| Content Safety | Comprehensive assessment of various safety concerns. | Query, response |
| Protected Materials | Detects unauthorized use of copyrighted or protected content. | Query, response |
| Code Vulnerability | Identifies security issues in generated code. |  Query, response |
| Ungrounded Attributes | Detects fabricated or hallucinated information inferred from user interactions. | Query, context, response |

To learn more, see [Risk and safety evaluators](./evaluation-evaluators/risk-safety-evaluators.md).

### Agents

::: moniker range="foundry-classic"

| Evaluator | Purpose | Inputs |
|--|--|--|
| Intent Resolution (preview) | Measures how accurately the agent identifies and addresses user intentions. | Query, response |
| Task Adherence (preview)| Measures how well the agent follows through on identified tasks. | Query, response, tool definitions (optional) |
| Tool Call Accuracy (preview) | Measures how well the agent selects and calls the correct tools to. | Query, either response or tool calls, tool definitions |

::: moniker-end

::: moniker range="foundry"

| Evaluator | Purpose | Inputs |
|--|--|--|
| Task Adherence (preview)  | Measures whether the agent follows through on identified tasks according to system instructions. | Query, Response, Tool definitions (Optional) |
| Task Completion (preview)| Measures whether the agent successfully completed the requested task end-to-end. | Query, Response, Tool definitions (Optional) |
| Intent Resolution (preview) | Measures how accurately the agent identifies and addresses user intentions. | Query, Response, Tool definitions (Optional)  |
| Task Navigation Efficiency (preview) | Determines whether the agent's sequence of steps matches an optimal or expected path to measure efficiency. | Response, Ground truth |
| Tool Call Accuracy (preview) | Measures the overall quality of tool calls including selection, parameter correctness, and efficiency. | Query, Tool definitions, Tool calls (Optional), Response |
| Tool Selection (preview) | Measures whether the agent selected the most appropriate and efficient tools for a task. | Query, Tool definitions, Tool calls (Optional), Response |
| Tool Input Accuracy (preview)| Validates that all tool call parameters are correct with strict criteria including grounding, type, format, completeness, and appropriateness. | Query, Response, Tool definitions |
| Tool Output Utilization (preview)| Measures whether the agent correctly interprets and uses tool outputs contextually in responses and subsequent calls. | Query, Response, Tool definitions (Optional) |
| Tool Call Success (preview) | Evaluates whether all tool calls executed successfully without technical failures. | Response, Tool definitions (Optional) |

::: moniker-end

To learn more, see [Agent evaluators](./evaluation-evaluators/agent-evaluators.md).

### Azure OpenAI graders

| Evaluator | Purpose |  Inputs |
|--|--|--|
| Model Labeler | Classifies content using custom guidelines and labels. | Query, response, ground truth |
| String Checker | Performs flexible text validations and pattern matching. | Response |
| Text Similarity | Evaluates the quality of text or determine semantic closeness. | Response, ground truth |
| Model Scorer| Generates numerical scores (customized range) for content based on custom guidelines. | Query, response, ground truth |

To learn more, see [Azure OpenAI Graders](./evaluation-evaluators/azure-openai-graders.md).

### Evaluators in the development lifecycle

These evaluators integrate into each stage of the AI lifecycle to ensure reliability, safety, and effectiveness.

:::image type="content" source="../media/evaluations/lifecycle.png" alt-text="Diagram of AI application lifecycle, showing model selection, building an AI application, and operationalizing." lightbox="../media/evaluations/lifecycle.png":::

## The three stages of AI application lifecycle evaluation

### Base model selection

Select the right foundation model by comparing quality, task performance, ethical considerations, and safety profiles across different models.

**Tools available**: [Microsoft Foundry benchmark](model-benchmarks.md) for comparing models on public datasets or your own data, and the Azure AI Evaluation SDK for [testing specific model endpoints](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

### Preproduction evaluation

Before deployment, thorough testing ensures your AI agent or application is production-ready. This stage validates performance through evaluation datasets, identifies edge cases, assesses robustness, and measures key metrics including task adherence, groundedness, relevance, and safety.

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of preproduction evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

**Evaluation tools and approaches:**

::: moniker range="foundry-classic"

- **Bring your own data**: Evaluate AI agents and applications using your own data with quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md). Use Foundry's evaluation wizard or [Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md) and [view results in the Foundry portal](../how-to/evaluate-results.md).

- **Simulators and AI red teaming agent**: Generate evaluation data through [Azure AI Evaluation SDK simulators](..//how-to/develop/simulator-interaction-data.md):
  - [AI red teaming agent](../how-to/develop/run-scans-ai-red-teaming-agent.md): Simulates complex adversarial attacks using Microsoft's PyRIT framework to identify safety and security vulnerabilities. Best used with human-in-the-loop processes.
  - [Adversarial simulators](../how-to/develop/simulator-interaction-data.md#generate-adversarial-simulations-for-safety-evaluation): Inject queries mimicking security attacks like jailbreaks to test edge cases.
  - [Context-appropriate simulators](../how-to/develop/simulator-interaction-data.md#generate-synthetic-data-and-simulate-non-adversarial-tasks): Generate realistic user conversations to test quality metrics including groundedness, relevance, coherence, and fluency.

Alternatively, you can also use [the Foundry portal](../how-to/evaluate-generative-ai-app.md) for testing your generative AI applications.

::: moniker-end

::: moniker range="foundry"

- **Bring your own data**: Evaluate AI applications using your own data with quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md). Use Foundry's evaluation wizard or [Foundry SDK](../how-to/develop/evaluate-sdk.md) and [view results in the Foundry portal](../how-to/evaluate-results.md).

- **Simulators and AI red teaming agent**: Generate evaluation data through simulators that test model responses to realistic or adversarial queries. The [AI red teaming agent](../how-to/develop/run-scans-ai-red-teaming-agent.md) simulates complex attacks using Microsoft's PyRIT framework to identify safety and security vulnerabilities before deployment. Best used with human-in-the-loop processes.

You can also use [the Foundry portal](../how-to/evaluate-generative-ai-app.md) for testing generative AI applications.

::: moniker-end

### Post-production monitoring

::: moniker range="foundry-classic"
After deployment, continuous monitoring ensures your AI application maintains quality in real-world conditions:
::: moniker-end
::: moniker range="foundry"
After deployment, [continuous monitoring](../default/agents/how-to/how-to-monitor-agents-dashboard.md) ensures your AI application maintains quality in real-world conditions:
::: moniker-end

- **Operational metrics**: Regular measurement of key AI agent operational metrics
- **Continuous evaluation**: Quality and safety evaluation of production traffic at a sampled rate
- **Scheduled evaluation**: Scheduled quality and safety evaluation using test datasets to detect system drift
- **Scheduled red teaming**: Scheduled adversarial testing to probe for safety and security vulnerabilities
- **Azure Monitor alerts**: Notifications when outputs fail quality thresholds or produce harmful content

Integrated with Azure Monitor Application Insights, the Foundry Observability dashboard delivers real-time insights into performance, safety, and quality metrics, enabling rapid issue resolution and maintaining user trust.

## Building trust through systematic evaluation

Systematic evaluation at each stage—from model selection through production monitoring—ensures AI solutions are powerful, trustworthy, and safe.

### Evaluation cheat sheet

::: moniker range="foundry-classic"

| Purpose | Process | Parameters, guidance, and samples |
| -----| -----| ----|
| What are you evaluating for? | Identify or build relevant evaluators | - [Quality and performance sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py) <br> </br> - [Agents Response Quality](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/evaluate/Supported_Evaluation_Metrics/Agent_Evaluation) <br> </br> - [Safety and Security](./evaluation-evaluators/risk-safety-evaluators.md) ([Safety and Security sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluatesafetyrisks.py)) <br> </br> - [Custom](./evaluation-evaluators/custom-evaluators.md) ([Custom sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py)) |
| What data should you use?  | Upload or generate relevant dataset | - [Generic simulator for measuring Quality and Performance](./concept-synthetic-data.md) ([Generic simulator sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/finetune/Llama-notebooks/datagen/synthetic-data-generation.ipynb)) <br></br> - [Adversarial simulator for measuring Safety and Security](../how-to/develop/simulator-interaction-data.md) ([Adversarial simulator sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/simulate_and_evaluate_online_endpoint.ipynb)) <br></br> - AI red teaming agent for running automated scans to assess safety and security vulnerabilities ([AI red teaming agent sample notebook](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/AI_RedTeaming/AI_RedTeaming.ipynb))|
| How to run evaluations on a dataset? | Run evaluation | - [Agent evaluation runs](../how-to/develop/agent-evaluate-sdk.md) <br></br>- [Remote cloud run](../how-to/develop/cloud-evaluation.md) <br></br> - [Local run](../how-to/develop/evaluate-sdk.md) |
| How did my model/app perform? | Analyze results  | - [View aggregate scores, view details, score details, compare evaluation runs](..//how-to/evaluate-results.md) |
| How can I improve? | Make changes to model, app, or evaluators | - If evaluation results didn't align to human feedback, adjust your evaluator. <br></br> - If evaluation results aligned to human feedback but didn't meet quality/safety thresholds, apply targeted mitigations. Example of mitigations to apply: [Azure AI Content Safety](../ai-services/content-safety-overview.md) |

::: moniker-end

::: moniker range="foundry"

| Purpose | Process | Parameters, guidance, and samples  |
| -----| -----| ----|
| What are you evaluating for? | Identify or build relevant evaluators | - [RAG Quality](https://aka.ms/rag-evaluators-samples) <br> </br> - [Agents Quality](https://aka.ms/agent-evaluator-samples) <br> </br> - [Safety and Security](./evaluation-evaluators/risk-safety-evaluators.md) ([Safety and Security sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluatesafetyrisks.py)) <br> </br> - [Custom](./evaluation-evaluators/custom-evaluators.md) ([Custom sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py)) |
| What data should you use?  | Upload or generate relevant dataset | - [Synthetic dataset generation](../how-to/evaluate-generative-ai-app.md#select-or-create-a-dataset) <br></br> - AI red teaming agent for running automated scans to assess safety and security vulnerabilities ([AI red teaming agent sample notebook](https://aka.ms/airedteamingagent-sample))|
| How to run evaluations on a dataset? | Run evaluation | - [Agent evaluation runs](../how-to/develop/agent-evaluate-sdk.md) <br></br> - [Remote cloud run](../how-to/develop/cloud-evaluation.md) |
| How did my model/app perform? | Analyze results  | - [View aggregate scores, view details, score details, compare evaluation runs](..//how-to/evaluate-results.md) |
| How can I improve? | Make changes to model, app, or evaluators | - If evaluation results didn't align to human feedback, adjust your evaluator. <br></br> - If evaluation results aligned to human feedback but didn't meet quality/safety thresholds, apply targeted mitigations. Example of mitigations to apply: [Azure AI Content Safety](../ai-services/content-safety-overview.md) |

::: moniker-end

## Bring your own virtual network for evaluation

For network isolation purposes you can bring your own virtual network for evaluation. To learn more, see [How to configure a private link](../how-to/configure-private-link.md).

> [!NOTE]
> Evaluation data is sent to Application Insights if Application Insights is connected. Virtual network support for Application Insights and tracing isn't available. Inline datasource is not supported.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Azure AI User role to the project's Managed Identity during initial project setup.

### Virtual network region support

Bring your own virtual network for evaluation is supported in all regions except for Central India, East Asia, North Europe and Qatar Central.

## Region support

Currently certain AI-assisted evaluators are available only in the following regions:

| Region | Hate and unfairness, Sexual, Violent, Self-harm, Indirect attack, Code vulnerabilities, Ungrounded attributes | Groundedness Pro | Protected material |
|--|--|--|--|
| East US 2 | Supported | Supported | Supported |
| Sweden Central | Supported | Supported | N/A |
| US North Central | Supported | N/A | N/A |
| France Central | Supported | N/A | N/A |
| Switzerland West | Supported | N/A | N/A |

> [!NOTE]
> Red teaming agent is only available in regions where risk and safety evaluators are supported.

### Agent playground evaluation region support

| Region | Status |
|--|--|
| East US | Supported |
| East US 2 | Supported |
| West US | Supported |
| West US 2 | Supported |
| West US 3 | Supported |
| France Central | Supported |
| Norway East | Supported |
| Sweden Central | Supported |

## Pricing

Observability features such as Risk and Safety Evaluations and Continuous Evaluations are billed based on consumption as listed in [our Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

## Related content

::: moniker range="foundry-classic"

- [Evaluate with the Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md)
- [Evaluate generative AI apps by using Foundry](../how-to/evaluate-generative-ai-app.md)
- [See evaluation results in the Foundry portal](../how-to/evaluate-results.md)
- [Foundry Transparency Note](safety-evaluations-transparency-note.md)

::: moniker-end

::: moniker range="foundry"

- [Foundry control plane](../default/control-plane/overview.md)
- [Evaluate generative AI apps by using Foundry](../how-to/evaluate-generative-ai-app.md)
- [See evaluation results in the Foundry portal](../how-to/evaluate-results.md)
- [Foundry Transparency Note](safety-evaluations-transparency-note.md)

::: moniker-end
