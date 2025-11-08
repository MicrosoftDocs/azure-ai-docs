---
title: Observability in Generative AI
titleSuffix: Azure AI Foundry
description: Learn how Azure AI Foundry enables safe, high-quality generative AI through systematic evaluation and observability tools.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: mithigpe
ms.date: 10/09/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - build-aifnd
  - build-2025
---

# Observability in generative AI

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In today's AI-driven world, Generative AI Operations (GenAIOps) is revolutionizing how organizations build and deploy intelligent systems. As companies increasingly use AI to transform decision making, enhance customer experiences, and fuel innovation, one element stands paramount: robust evaluation frameworks. Evaluation isn't just a checkpoint. It's the foundation of trust in AI applications. Without rigorous assessment, AI systems can produce content that's:

- Fabricated or ungrounded in reality
- Irrelevant or incoherent to user needs
- Harmful in perpetuating content risks and stereotypes
- Dangerous in spreading misinformation
- Vulnerable to security exploits

This assessment is where evaluators become essential. Specialized tools measure both the frequency and severity of risks in AI outputs. These tools enable teams to systematically address quality, safety, and security concerns. Use these tools throughout the AI development journey, from selecting the right model to monitoring production performance, quality, and safety.

## What are evaluators?

Evaluators are specialized tools that measure the quality, safety, and reliability of AI responses. When teams implement systematic evaluations throughout the AI development lifecycle, they can identify and address potential issues before those issues affect users. The following supported evaluators provide comprehensive assessment capabilities across different AI application types and concerns.

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
| Document Retrieval | Measures accuracy in retrieval results given ground truth. | Ground truth, retrieved documents |
| Groundedness | Measures how consistent the response is with respect to the retrieved context. | Query (optional), context, response |
| Groundedness Pro | Measures whether the response is consistent with respect to the retrieved context. | Query, context, response |
| Relevance | Measures how relevant the response is with respect to the query. | Query, response|
| Response Completeness | Measures to what extent the response is complete (not missing critical information) with respect to the ground truth. | Response, ground truth |

To learn more, see [Retrieval-augmented Generation (RAG) evaluators](./evaluation-evaluators/rag-evaluators.md).

### Safety and security (preview)

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

### Agents (preview)

| Evaluator | Purpose | Inputs |
|--|--|--|
| Intent Resolution | Measures how accurately the agent identifies and addresses user intentions. | Query, response |
| Task Adherence | Measures how well the agent follows through on identified tasks. | Query, response, tool definitions (optional) |
| Tool Call Accuracy | Measures how well the agent selects and calls the correct tools to. | Query, either response or tool calls, tool definitions |

To learn more, see [Agent evaluators](./evaluation-evaluators/agent-evaluators.md).

### Azure OpenAI graders (preview)

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

Before you build your application, select the right foundation. This initial evaluation helps you compare different models based on:

- Quality and accuracy: How relevant and coherent are the model's responses?
- Task performance: Does the model handle your specific use cases efficiently?
- Ethical considerations: Is the model free from harmful biases?
- Safety profile: What is the risk of generating unsafe content?

**Tools available**: [Azure AI Foundry benchmark](model-benchmarks.md) for comparing models on public datasets or your own data, and the Azure AI Evaluation SDK for [testing specific model endpoints](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

### Pre-production evaluation

After you select a base model, the next step is to develop an AI application, such as an AI-powered chatbot, a retrieval-augmented generation (RAG) application, an agentic AI application, or any other generative AI tool. When development is complete, *pre-production evaluation* begins. Before you deploy to a production environment, thorough testing is essential to ensure that the model is ready for real-world use.

Pre-production evaluation involves:

- Testing with evaluation datasets: These datasets simulate realistic user interactions to ensure that the AI application performs as expected.
- Identifying edge cases: Find scenarios where the AI application's response quality might degrade or produce undesirable outputs.
- Assessing robustness: Ensure that the model can handle a range of input variations without significant drops in quality or safety.
- Measuring key metrics: Evaluate metrics such as response groundedness, relevance, and safety to confirm readiness for production.

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of pre-production evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

The pre-production stage acts as a final quality check, reducing the risk of deploying an AI application that doesn't meet the desired performance or safety standards.

Evaluation Tools and Approaches:

- **Bring your own data**: You can evaluate your AI applications in pre-production using your own evaluation data with supported evaluators, including generation quality, safety, or custom evaluators. View results by using the Azure AI Foundry portal.

  Use Azure AI Foundry’s evaluation wizard or [Azure AI Evaluation SDK’s](../how-to/develop/evaluate-sdk.md) supported evaluators, including generation quality, safety, or [custom evaluators](./evaluation-evaluators/custom-evaluators.md). [View results by using the Azure AI Foundry portal](../how-to/evaluate-results.md).

- **Simulators and AI red teaming agent (preview)**: If you don’t have evaluation data or test data, [Azure AI Evaluation SDK’s simulators](..//how-to/develop/simulator-interaction-data.md) can help by generating topic-related or adversarial queries. These simulators test the model’s response to situation-appropriate or attack-like queries (edge cases).

  - [Adversarial simulators](../how-to/develop/simulator-interaction-data.md#generate-adversarial-simulations-for-safety-evaluation) inject static queries that mimic potential safety risks or security attacks or attempted jailbreaks. The simulators help identify limitations to prepare the model for unexpected conditions.
  - [Context-appropriate simulators](../how-to/develop/simulator-interaction-data.md#generate-synthetic-data-and-simulate-non-adversarial-tasks) generate typical, relevant conversations you might expect from users to test quality of responses. With context-appropriate simulators, you can assess metrics such as groundedness, relevance, coherence, and fluency of generated responses.
  - [AI red teaming agent (preview)](../how-to/develop/run-scans-ai-red-teaming-agent.md) simulates complex adversarial attacks against your AI system using a broad range of safety and security attacks. It uses Microsoft’s open framework for Python Risk Identification Tool (PyRIT).
    
    Automated scans using the AI red teaming agent enhance pre-production risk assessment by systematically testing AI applications for risks. This process involves simulated attack scenarios to identify weaknesses in model responses before real-world deployment.

    By running AI red teaming scans, you can detect and mitigate potential safety issues before deployment. We recommend that you use this tool along with human-in-the-loop processes, such as conventional AI red teaming probing, to help accelerate risk identification and aid in the assessment by a human expert.

Alternatively, you can also use [evaluation functionality](../how-to/evaluate-generative-ai-app.md) in the Azure AI Foundry portal for testing your generative AI applications.

After you get satisfactory results, you can deploy the AI application to production.

### Post-production monitoring

After deployment, continuous monitoring ensures your AI application maintains quality in real-world conditions.

- **Performance tracking**: Regular measurement of key metrics.
- **Incident response**: Swift action when harmful or inappropriate outputs occur.

Effective monitoring helps maintain user trust and allows for rapid issue resolution.  

Azure AI Foundry Observability provides comprehensive monitoring capabilities essential for today's complex and rapidly evolving AI landscape. Seamlessly integrated with Azure Monitor Application Insights, this solution enables continuous monitoring of deployed AI applications to ensure optimal performance, safety, and quality in production environments.

The Foundry Observability dashboard delivers real-time insights into critical metrics. It allows teams to quickly identify and address performance issues, safety concerns, or quality degradation. 

For Agent-based applications, Foundry offers enhanced continuous evaluation capabilities. These capabilities can provide deeper visibility into quality and safety metrics. They can create a robust monitoring ecosystem that adapts to the dynamic nature of AI applications while maintaining high standards of performance and reliability.  

By continuously monitoring the AI application's behavior in production, you can maintain high-quality user experiences and swiftly address any issues that surface.

## Building trust through systematic evaluation

GenAIOps establishes a reliable process for managing AI applications throughout their lifecycle. By implementing thorough evaluation at each stage—from model selection through deployment and beyond—teams can create AI solutions that aren't just powerful but trustworthy and safe.

### Evaluation cheat sheet

| Purpose |  Process | Parameters |
| -----| -----| ----|
| What are you evaluating for? | Identify or build relevant evaluators | - [Quality and performance sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py) <br> </br> - [Agents Response Quality](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/evaluate/Supported_Evaluation_Metrics/Agent_Evaluation) <br> </br> - [Safety and Security](./evaluation-evaluators/risk-safety-evaluators.md) ([Safety and Security sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluatesafetyrisks.py)) <br> </br> - [Custom](./evaluation-evaluators/custom-evaluators.md) ([Custom sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py)) |
| What data should you use?  | Upload or generate relevant dataset | - [Generic simulator for measuring Quality and Performance](./concept-synthetic-data.md) ([Generic simulator sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/finetune/Llama-notebooks/datagen/synthetic-data-generation.ipynb)) <br></br> - [Adversarial simulator for measuring Safety and Security](../how-to/develop/simulator-interaction-data.md) ([Adversarial simulator sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/simulate_and_evaluate_online_endpoint.ipynb)) <br></br> - AI red teaming agent for running automated scans to assess safety and security vulnerabilities ([AI red teaming agent sample notebook](https://aka.ms/airedteamingagent-sample))|
| What resources should conduct the evaluation? | Run evaluation | - [Local run](../how-to/develop/evaluate-sdk.md) <br> </br>  - [Remote cloud run](../how-to/develop/cloud-evaluation.md) |
| How did my model/app perform? | Analyze results  | - [View aggregate scores, view details, score details, compare evaluation runs](..//how-to/evaluate-results.md) |
| How can I improve? | Make changes to model, app, or evaluators | - If evaluation results didn't align to human feedback, adjust your evaluator. <br></br> - If evaluation results aligned to human feedback but didn't meet quality/safety thresholds, apply targeted mitigations. Example of mitigations to apply: [Azure AI Content Safety](../ai-services/content-safety-overview.md) |

## Region support

Currently certain AI-assisted evaluators are available only in the following regions:

| Region | Hate and unfairness, Sexual, Violent, Self-harm, Indirect attack, Code vulnerabilities, Ungrounded attributes | Groundedness Pro | Protected material |
|--|--|--|--|
| East US 2 | Supported | Supported | Supported |
| Sweden Central | Supported | Supported | N/A |
| US North Central | Supported | N/A | N/A |
| France Central | Supported | N/A | N/A |
| Switzerland West | Supported | N/A | N/A |

## Pricing

Observability features such as Risk and Safety Evaluations and Continuous Evaluations are billed based on consumption as listed in [our Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

## Related content

- [Evaluate with the Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md)
- [Evaluate generative AI apps by using Azure AI Foundry](../how-to/evaluate-generative-ai-app.md)
- [See evaluation results in the Azure AI Foundry portal](../how-to/evaluate-results.md)
- [Azure AI Foundry Transparency Note](safety-evaluations-transparency-note.md)
