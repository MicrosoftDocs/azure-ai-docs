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

In today's AI-driven world, Generative AI Operations (GenAIOps) is revolutionizing how organizations build and deploy intelligent systems. As companies increasingly use AI agents and applications to transform decision-making, enhance customer experiences, and fuel innovation, one element stands paramount: robust evaluation frameworks. Evaluation isn't just a checkpoint. It's the foundation of quality and trust in AI applications. Without rigorous assessment and monitoring, AI systems can produce content that's:

- Fabricated or ungrounded in reality
- Irrelevant or incoherent
- Harmful in perpetuating content risks and stereotypes
- Dangerous in spreading misinformation
- Vulnerable to security exploits

This is where observability becomes essential. These capabilities measure both the frequency and severity of risks in AI outputs, enabling teams to systematically address quality, safety, and security concerns throughout the entire AI development journey—from selecting the right model to monitoring production performance, quality, and safety.

[!INCLUDE [evaluation-preview](../includes/evaluation-preview.md)]

## What is observability?

AI observability refers to the ability to monitor, understand, and troubleshoot AI systems throughout their lifecycle. It involves collecting and analyzing signals such as evaluation metrics, logs, traces, and model and agent outputs to gain visibility into performance, quality, safety, and operational health.

## What are evaluators?

Evaluators are specialized tools that measure the quality, safety, and reliability of AI responses. By implementing systematic evaluations throughout the AI development lifecycle, teams can identify and address potential issues before they impact users. The following supported evaluators provide comprehensive assessment capabilities across different AI application types and concerns:

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

By using these evaluators strategically throughout the development lifecycle, teams can build more reliable, safe, and effective AI applications that meet user needs while minimizing potential risks.

:::image type="content" source="../media/evaluations/lifecycle.png" alt-text="Diagram of enterprise GenAIOps lifecycle, showing model selection, building an AI application, and operationalizing." lightbox="../media/evaluations/lifecycle.png":::

## The three stages of GenAIOps evaluation

GenAIOps uses the following three stages.

### Base model selection

Before building your application, you need to select the right foundation. This initial evaluation helps you compare different models based on:

- Quality and accuracy: How relevant and coherent are the model's responses?
- Task performance: Does the model handle your specific use cases efficiently?
- Ethical considerations: Is the model free from harmful biases?
- Safety profile: What is the risk of generating unsafe content?

**Tools available**: [Microsoft Foundry benchmark](model-benchmarks.md) for comparing models on public datasets or your own data, and the Azure AI Evaluation SDK for [testing specific model endpoints](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

### Preproduction evaluation

After you select a base model, the next step is to develop an AI agent or application. Before you deploy to a production environment, thorough testing is essential to ensure that the AI agent or application is ready for real-world use.

Preproduction evaluation involves:

- Testing with evaluation datasets: These datasets simulate realistic user interactions to ensure the AI agent performs as expected.
- Identifying edge cases: Finding scenarios where the AI agent's response quality might degrade or produce undesirable outputs.
- Assessing robustness: Ensuring that the AI agent can handle a range of input variations without significant drops in quality or safety.
- Measuring key metrics: Metrics such as task adherence, response groundedness, relevance, and safety are evaluated to confirm readiness for production.

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of preproduction evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

The preproduction stage acts as a final quality check, reducing the risk of deploying an AI agent or application that doesn't meet the desired performance or safety standards.

Evaluation Tools and Approaches:

::: moniker range="foundry-classic"

- **Bring your own data**: You can evaluate your AI agents and applications in preproduction using your own evaluation data with supported evaluators, including quality, safety, or custom evaluators, and view results via the Foundry portal. Use Foundry's evaluation wizard or [Azure AI Evaluation SDK's](../how-to/develop/evaluate-sdk.md) supported evaluators, including generation quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md). [View results by using the Foundry portal](../how-to/evaluate-results.md).
- **Simulators and AI red teaming agent**: If you don't have evaluation data (test data), [Azure AI Evaluation SDK's simulators](..//how-to/develop/simulator-interaction-data.md) can help by generating topic-related or adversarial queries. These simulators test the model's response to situation-appropriate or attack-like queries (edge cases).

  - [AI red teaming agent](../how-to/develop/run-scans-ai-red-teaming-agent.md) simulates complex adversarial attacks against your AI system using a broad range of safety and security attacks using Microsoft's open framework for Python Risk Identification Tool or PyRIT.
  - [Adversarial simulators](../how-to/develop/simulator-interaction-data.md#generate-adversarial-simulations-for-safety-evaluation) injects static queries that mimic potential safety risks or security attacks such as attempted jailbreaks, helping identify limitations and preparing the model for unexpected conditions.
  - [Context-appropriate simulators](../how-to/develop/simulator-interaction-data.md#generate-synthetic-data-and-simulate-non-adversarial-tasks) generate typical, relevant conversations you'd expect from users to test quality of responses. With context-appropriate simulators you can assess metrics such as groundedness, relevance, coherence, and fluency of generated responses.

   Automated scans using the AI red teaming agent enhance preproduction risk assessment by systematically testing AI applications for risks. This process involves simulated attack scenarios to identify weaknesses in model responses before real-world deployment. By running AI red teaming scans, you can detect and mitigate potential safety issues before deployment. This tool is recommended to be used with human-in-the-loop processes such as conventional AI red teaming probing to help accelerate risk identification and aid in the assessment by a human expert.

Alternatively, you can also use [the Foundry portal](../how-to/evaluate-generative-ai-app.md) for testing your generative AI applications.

::: moniker-end

::: moniker range="foundry"

- Bring your own data: You can evaluate your AI applications in preproduction using your own evaluation data with supported evaluators, including generation quality, safety, or custom evaluators, and view results via the Foundry portal. Use Foundry's evaluation wizard or [Foundry SDK's](../how-to/develop/evaluate-sdk.md) supported evaluators, including generation quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md), and [view results via the Foundry portal](../how-to/evaluate-results.md).

- Simulators and AI red teaming agent: If you don't have evaluation data (test data), simulators can help by generating topic-related or adversarial queries. These simulators test the model's response to situation-appropriate or attack-like queries (edge cases).

  [AI red teaming agent](../how-to/develop/run-scans-ai-red-teaming-agent.md) simulates complex adversarial attacks against your AI system using a broad range of safety and security attacks using Microsoft's open framework for Python Risk Identification Tool or PyRIT.
  
  Automated scans using the AI red teaming agent enhances preproduction risk assessment by systematically testing AI applications for risks. This process involves simulated attack scenarios to identify weaknesses in model responses before real-world deployment. By running AI red teaming scans, you can detect and mitigate potential safety issues before deployment. This tool is recommended to be used with human-in-the-loop processes such as conventional AI red teaming probing to help accelerate risk identification and aid in the assessment by a human expert.

Alternatively, you can also use [the Foundry portal](../how-to/evaluate-generative-ai-app.md) for testing your generative AI applications.

::: moniker-end

After you get satisfactory results, you can deploy the AI application to production.

### Post-production monitoring

::: moniker range="foundry-classic"
After deployment, continuous monitoring ensures your AI application maintains quality in real-world conditions.
::: moniker-end
::: moniker range="foundry"
After deployment, [continuous monitoring](../default/agents/how-to/how-to-monitor-agents-dashboard.md) ensures your AI application maintains quality in real-world conditions.
::: moniker-end

- **Operational metrics**: Regular measurement of key AI agent operational metrics.
- **Continuous evaluation**: Enables quality and safety evaluation of production traffic at a sampled rate.
- **Scheduled evaluation**: Enables scheduled quality and safety evaluation using a test dataset to detect drift in the underlying systems.
- **Scheduled red teaming**: Provides scheduled adversarial testing capabilities to probe for safety and security vulnerabilities.
- **Azure Monitor alerts**: Swift action when harmful or inappropriate outputs occur. Set up alerts for continuous evaluation to be notified when evaluation results drop below the pass rate threshold in production.

Effective monitoring helps maintain user trust and allows for rapid issue resolution.

Observability provides comprehensive monitoring capabilities essential for today's complex and rapidly evolving AI landscape. Seamlessly integrated with Azure Monitor Application Insights, this solution enables continuous monitoring of deployed AI applications to ensure optimal performance, safety, and quality in production environments.

The Foundry Observability dashboard delivers real-time insights into critical metrics. It allows teams to quickly identify and address performance issues, safety concerns, or quality degradation. 

For Agent-based applications, Foundry offers enhanced continuous evaluation capabilities. These capabilities can provide deeper visibility into quality and safety metrics. They can create a robust monitoring ecosystem that adapts to the dynamic nature of AI applications while maintaining high standards of performance and reliability.  

By continuously monitoring the AI application's behavior in production, you can maintain high-quality user experiences and swiftly address any issues that surface.

## Building trust through systematic evaluation

GenAIOps establishes a reliable process for managing AI applications throughout their lifecycle. By implementing thorough evaluation at each stage—from model selection through deployment and beyond—teams can create AI solutions that aren't just powerful but trustworthy and safe.

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
