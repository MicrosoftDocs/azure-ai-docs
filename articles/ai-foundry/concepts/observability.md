---
title: Observability in Generative AI with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how Azure AI Foundry enables safe, high-quality generative AI through systematic evaluation and observability tools.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: conceptual
ms.date: 05/19/2025
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
---

# Observability in generative AI  

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In today's AI-driven world, Generative AI Operations (GenAIOps) is revolutionizing how organizations build and deploy intelligent systems. As companies increasingly use AI to transform decision-making, enhance customer experiences, and fuel innovation, one element stands paramount: robust evaluation frameworks. Evaluation isn't just a checkpoint. It's the foundation of trust in AI applications. Without rigorous assessment, AI systems can produce content that's:

- Fabricated or ungrounded in reality
- Irrelevant or incoherent to user needs
- Harmful in perpetuating content risks and stereotypes
- Dangerous in spreading misinformation
- Vulnerable to security exploits

This is where evaluators become essential. These specialized tools measure both the frequency and severity of risks in AI outputs, enabling teams to systematically address quality, safety, and security concerns throughout the entire AI development journey—from selecting the right model to monitoring production performance, quality, and safety.

## What are evaluators?

Evaluators are specialized tools that measure the quality, safety, and reliability of AI responses. By implementing systematic evaluations throughout the AI development lifecycle, teams can identify and address potential issues before they impact users. The following supported evaluators provide comprehensive assessment capabilities across different AI application types and concerns:


[**RAG (Retrieval Augmented Generation)**:](./evaluation-evaluators/rag-evaluators.md)

| Evaluator | Purpose |
|--|--|
| Retrieval | Measures how effectively the system retrieves relevant information. |
| Document Retrieval | Measures accuracy in retrieval results given ground truth. |
| Groundedness | Measures how consistent the response is with respect to the retrieved context. |
| Groundedness Pro | Measures whether the response is consistent with respect to the retrieved context. |
| Relevance | Measures how relevant the response is with respect to the query. |
| Response Completeness | Measures to what extent the response is complete (not missing critical information) with respect to the ground truth. |


[**Agents:**](./evaluation-evaluators/agent-evaluators.md)

| Evaluator | Purpose |
|--|--|
| Intent Resolution | Measures how accurately the agent identifies and addresses user intentions.|
| Task Adherence | Measures how well the agent follows through on identified tasks. |
| Tool Call Accuracy | Measures how well the agent selects and calls the correct tools to.|


[**General Purpose:**](./evaluation-evaluators/general-purpose-evaluators.md)

| Evaluator | Purpose |
|--|--|
| Fluency | Measures natural language quality and readability. |
| Coherence | Measures logical consistency and flow of responses.|
| QA | Measures comprehensively various quality aspects in question-answering.|


[**Safety and Security:**](./evaluation-evaluators/risk-safety-evaluators.md)

| Evaluator | Purpose |
|--|--|
| Violence | Detects violent content or incitement. |
| Sexual | Identifies inappropriate sexual content. |
| Self-Harm | Detects content promoting or describing self-harm.|
| Hate and Unfairness | Identifies biased, discriminatory, or hateful content. |
| Ungrounded Attributes | Detects fabricated or hallucinated information inferred from user interactions. |
| Code Vulnerability | Identifies security issues in generated code. |
| Protected Materials | Detects unauthorized use of copyrighted or protected content. |
| Content Safety | Comprehensive assessment of various safety concerns. |


[**Textual Similarity:**](./evaluation-evaluators/textual-similarity-evaluators.md)

| Evaluator | Purpose |
|--|--|
| Similarity | AI-assisted textual similarity measurement. |
| F1 Score | Harmonic mean of precision and recall in token overlaps between response and ground truth. |
| BLEU | Bilingual Evaluation Understudy score for translation quality measures overlaps in n-grams between response and ground truth. |
| GLEU | Google-BLEU variant for sentence-level assessment measures overlaps in n-grams between response and ground truth. |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation measures overlaps in n-grams between response and ground truth. |
| METEOR | Metric for Evaluation of Translation with Explicit Ordering measures overlaps in n-grams between response and ground truth. |


[**Azure OpenAI Graders:**](./evaluation-evaluators/azure-openai-graders.md)

| Evaluator | Purpose |
|--|--|
| Model Labeler | Classifies content using custom guidelines and labels. |
| Model Scorer | Generates numerical scores (customized range) for content based on custom guidelines. |
| String Checker | Performs flexible text validations and pattern matching. |
| Textual Similarity | Evaluates the quality of text or determine semantic closeness. |

By using these evaluators strategically throughout the development lifecycle, teams can build more reliable, safe, and effective AI applications that meet user needs while minimizing potential risks.

:::image type="content" source="../media/evaluations/lifecycle.png" alt-text="Diagram of enterprise GenAIOps lifecycle, showing model selection, building an AI application, and operationalizing." lightbox="../media/evaluations/lifecycle.png":::

## The three stages of GenAIOps evaluation

### Base model selection

Before building your application, you need to select the right foundation. This initial evaluation helps you compare different models based on:

- Quality and accuracy: How relevant and coherent are the model's responses?
- Task performance: Does the model handle your specific use cases efficiently?
- Ethical considerations: Is the model free from harmful biases?
- Safety profile: What is the risk of generating unsafe content?

**Tools available**: [Azure AI Foundry benchmark](model-benchmarks.md) for comparing models on public datasets or your own data, and the Azure AI Evaluation SDK for [testing specific model endpoints](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

### Pre-production evaluation

After you select a base model, the next step is to develop an AI application—such as an AI-powered chatbot, a retrieval-augmented generation (RAG) application, an agentic AI application, or any other generative AI tool. Once development is complete, pre-production evaluation begins. Before deploying to a production environment, thorough testing is essential to ensure the model is ready for real-world use.

Pre-production evaluation involves:

- Testing with evaluation datasets: These datasets simulate realistic user interactions to ensure the AI application performs as expected.
- Identifying edge cases: Finding scenarios where the AI application's response quality might degrade or produce undesirable outputs.
- Assessing robustness: Ensuring that the model can handle a range of input variations without significant drops in quality or safety.
- Measuring key metrics: Metrics such as response groundedness, relevance, and safety are evaluated to confirm readiness for production.

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of pre-production evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

The pre-production stage acts as a final quality check, reducing the risk of deploying an AI application that doesn't meet the desired performance or safety standards.

Evaluation Tools and Approaches:

- Bring your own data: You can evaluate your AI applications in pre-production using your own evaluation data with supported evaluators, including generation quality, safety, or custom evaluators, and view results via the Azure AI Foundry portal. Use Azure AI Foundry’s evaluation wizard or [Azure AI Evaluation SDK’s](../how-to/develop/evaluate-sdk.md) supported evaluators, including generation quality, safety, or [custom evaluators](../how-to/develop/evaluate-sdk.md#custom-evaluators), and [view results via the Azure AI Foundry portal](../how-to/evaluate-results.md).
- Simulators and AI red teaming agent (preview): If you don’t have evaluation data (test data), [Azure AI Evaluation SDK’s simulators](..//how-to/develop/simulator-interaction-data.md) can help by generating topic-related or adversarial queries. These simulators test the model’s response to situation-appropriate or attack-like queries (edge cases).
    - [Adversarial simulators](../how-to/develop/simulator-interaction-data.md#generate-adversarial-simulations-for-safety-evaluation) injects static queries that mimic potential safety risks or security attacks such as or attempt jailbreaks, helping identify limitations and preparing the model for unexpected conditions.
    - [Context-appropriate simulators](../how-to/develop/simulator-interaction-data.md#generate-synthetic-data-and-simulate-non-adversarial-tasks) generate typical, relevant conversations you’d expect from users to test quality of responses. With context-appropriate simulators you can assess metrics such as groundedness, relevance, coherence, and fluency of generated responses.
    - [AI red teaming agent (preview)](../how-to/develop/run-scans-ai-red-teaming-agent.md) simulates complex adversarial attacks against your AI system using a broad range of safety and security attacks using Microsoft’s open framework for Python Risk Identification Tool or PyRIT. Automated scans using the AI red teaming agent enhances pre-production risk assessment by systematically testing AI applications for risks. This process involves simulated attack scenarios to identify weaknesses in model responses before real-world deployment. By running AI red teaming scans, you can detect and mitigate potential safety issues before deployment. This tool is recommended to be used with human-in-the-loop processes such as conventional AI red teaming probing to help accelerate risk identification and aid in the assessment by a human expert.

Alternatively, you can also use [Azure AI Foundry portal's evaluation widget](../how-to/evaluate-generative-ai-app.md) for testing your generative AI applications.

Once satisfactory results are achieved, the AI application can be deployed to production.

### Post-production monitoring

After deployment, continuous monitoring ensures your AI application maintains quality in real-world conditions:

- Performance tracking: Regular measurement of key metrics.
- Incident response: Swift action when harmful or inappropriate outputs occur.

Effective monitoring helps maintain user trust and allows for rapid issue resolution.  

Azure AI Foundry Observability provides comprehensive monitoring capabilities essential for today's complex and rapidly evolving AI landscape. Seamlessly integrated with Azure Monitor Application Insights, this solution enables continuous monitoring of deployed AI applications to ensure optimal performance, safety, and quality in production environments. The Foundry Observability dashboard delivers real-time insights into critical metrics, allowing teams to quickly identify and address performance issues, safety concerns, or quality degradation. For Agent-based applications, Foundry offers enhanced continuous evaluation capabilities that can be enabled to provide deeper visibility into quality and safety metrics, creating a robust monitoring ecosystem that adapts to the dynamic nature of AI applications while maintaining high standards of performance and reliability.  

By continuously monitoring the AI application's behavior in production, you can maintain high-quality user experiences and swiftly address any issues that surface.

## Building trust through systematic evaluation

GenAIOps establishes a reliable process for managing AI applications throughout their lifecycle. By implementing thorough evaluation at each stage—from model selection through deployment and beyond—teams can create AI solutions that aren't just powerful but trustworthy and safe.

### Evaluation cheat sheet

| Purpose |  Process | Parameters |
| -----| -----| ----|
| What are you evaluating for? | Identify or build relevant evaluators | - [Quality and performance sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py) <br> </br> - [Agents Response Quality](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/evaluate/Supported_Evaluation_Metrics/Agent_Evaluation) <br> </br> - [Safety and Security](./evaluation-evaluators/risk-safety-evaluators.md) ([Safety and Security sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluatesafetyrisks.py)) <br> </br> - [Custom](../how-to/develop/evaluate-sdk.md#custom-evaluators) ([Custom sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py)) |
| What data should you use?  | Upload or generate relevant dataset | [Generic simulator for measuring Quality and Performance](./concept-synthetic-data.md) ([Generic simulator sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/finetune/Llama-notebooks/datagen/synthetic-data-generation.ipynb)) <br></br> - [Adversarial simulator for measuring Safety and Security](../how-to/develop/simulator-interaction-data.md) ([Adversarial simulator sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/simulate_and_evaluate_online_endpoint.ipynb)) <br></br> AI red teaming agent for running automated scans to assess safety and security vulnerabilities ([AI red teaming agent sample notebook](https://aka.ms/airedteamingagent-sample))|
| What resources should conduct the evaluation? | Run evaluation | - [Local run](../how-to/develop/evaluate-sdk.md) <br> </br>  - [Remote cloud run](../how-to/develop/cloud-evaluation.md) |
| How did my model/app perform? | Analyze results  | [View aggregate scores, view details, score details, compare evaluation runs](..//how-to/evaluate-results.md) |
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

Observability features such as Risk and Safety Evaluations and Continuous Evaluations are billed based on consumption as listed in [our Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/). Select the tab labeled **Complete AI Toolchain** to view the pricing details for evaluations.

## Related content

- [Evaluate your generative AI apps via the playground](../how-to/evaluate-prompts-playground.md)
- [Evaluate with the Azure AI evaluate SDK](../how-to/develop/evaluate-sdk.md)
- [Evaluate your generative AI apps with the Azure AI Foundry portal](../how-to/evaluate-generative-ai-app.md)
- [View the evaluation results](../how-to/evaluate-results.md)
- [Transparency Note for Azure AI Foundry safety evaluations](safety-evaluations-transparency-note.md)
