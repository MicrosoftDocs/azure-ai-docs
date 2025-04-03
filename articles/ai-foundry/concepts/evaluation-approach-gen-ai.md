---
title: Evaluation of generative AI applications with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Explore the broader domain of monitoring and evaluating large language models through the establishment of precise metrics, the development of test sets for measurement, and the implementation of iterative testing.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 04/04/2025
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
---

# Evaluation of generative AI applications

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In the rapidly evolving landscape of artificial intelligence, the integration of Generative AI Operations (GenAIOps) is transforming how organizations develop and deploy AI applications. As businesses increasingly rely on AI to enhance decision-making, improve customer experiences, and drive innovation, the importance of a robust evaluation framework can't be overstated. Evaluation is an essential component of the generative AI lifecycle to build confidence and trust in AI-centric applications. If not designed carefully, these applications can produce outputs that are fabricated and ungrounded in context, irrelevant or incoherent, resulting in poor customer experiences, or worse, perpetuate societal stereotypes, promote misinformation, expose organizations to malicious attacks, or a wide range of other negative impacts. 

Evaluators are helpful tools to assess the frequency and severity of content risks or undesirable behavior in AI responses. Performing iterative, systematic evaluations with the right evaluators can help teams measure and address potential response quality, safety, or security concerns throughout the AI development lifecycle, from initial model selection through post-production monitoring. Evaluation within the GenAI Ops Lifecycle production.

:::image type="content" source="../media/evaluations/lifecycle.png" alt-text="Diagram of enterprise GenAIOps lifecycle, showing model selection, building an AI application, and operationalizing." lightbox="../media/evaluations/lifecycle.png":::

 By understanding and implementing effective evaluation strategies at each stage, organizations can ensure their AI solutions not only meet initial expectations but also adapt and thrive in real-world environments. Let's dive into how evaluation fits into the three critical stages of the AI lifecycle

## Base model selection

The first stage of the AI lifecycle involves selecting an appropriate base model. Generative AI models vary widely in terms of capabilities, strengths, and limitations, so it's essential to identify which model best suits your specific use case. During base model evaluation, you "shop around" to compare different models by testing their outputs against a set of criteria relevant to your application.

Key considerations at this stage might include:

- **Accuracy/quality**: How well does the model generate relevant and coherent responses?
- **Performance on specific tasks**: Can the model handle the type of prompts and content required for your use case? How is its latency and cost?
- **Bias and ethical considerations**: Does the model produce any outputs that might perpetuate or promote harmful stereotypes?
- **Risk and safety**: Are there any risks of the model generating unsafe or malicious content?

You can explore [Azure AI Foundry benchmarks](./model-benchmarks.md)to evaluate and compare models on publicly available datasets, while also regenerating benchmark results on your own data. Alternatively, you can evaluate one of many base generative AI models via Azure AI Evaluation SDK as demonstrated, see [Evaluate model endpoints sample](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb).

## Pre-production evaluation

After selecting a base model, the next step is to develop an AI application—such as an AI-powered chatbot, a retrieval-augmented generation (RAG) application, an agentic AI application, or any other generative AI tool. Following development, pre-production evaluation begins. Before deploying the application in a production environment, rigorous testing is essential to ensure the model is truly ready for real-world use.

:::image type="content" source="../media/evaluations/evaluation-models-diagram.png" alt-text="Diagram of pre-production evaluation for models and applications with the six steps." lightbox="../media/evaluations/evaluation-models-diagram.png ":::

Pre-production evaluation involves:

- **Testing with evaluation datasets**: These datasets simulate realistic user interactions to ensure the AI application performs as expected.
- **Identifying edge cases**: Finding scenarios where the AI application’s response quality might degrade or produce undesirable outputs.
- **Assessing robustness**: Ensuring that the model can handle a range of input variations without significant drops in quality or safety.
- **Measuring key metrics**: Metrics such as response groundedness, relevance, and safety are evaluated to confirm readiness for production.

The pre-production stage acts as a final quality check, reducing the risk of deploying an AI application that doesn't meet the desired performance or safety standards.

- Bring your own data: You can evaluate your AI applications in pre-production using your own evaluation data with Azure AI Foundry or [Azure AI Evaluation SDK’s](../how-to/develop/evaluate-sdk.md) supported evaluators, including [generation quality, safety,](./evaluation-metrics-built-in.md) or [custom evaluators](../how-to/develop/evaluate-sdk.md#custom-evaluators), and [view results via the Azure AI Foundry portal](../how-to/evaluate-results.md).
- Simulators and AI red teaming agent (preview): If you don’t have evaluation data (test data), Azure AI [Evaluation SDK’s simulators](..//how-to/develop/simulator-interaction-data.md) can help by generating topic-related or adversarial queries. These simulators test the model’s response to situation-appropriate or attack-like queries (edge cases).
    - [Adversarial simulators](../how-to/develop/simulator-interaction-data.md#generate-adversarial-simulations-for-safety-evaluation) injects static queries that mimic potential safety risks or security attacks such as or attempt jailbreaks, helping identify limitations and preparing the model for unexpected conditions.  
    - [Context-appropriate simulators](../how-to/develop/simulator-interaction-data.md#generate-synthetic-data-and-simulate-non-adversarial-tasks) generate typical, relevant conversations you’d expect from users to test quality of responses. With context-appropriate simulators you can assess metrics such as groundedness, relevance, coherence, and fluency of generated responses.
    - [AI red teaming agent](../how-to/develop/run-scans-ai-red-teaming-agent.md) (preview) simulates complex adversarial attacks against your AI system using a broad range of safety and security attacks using Microsoft’s open framework for Python Risk Identification Tool or [PyRIT](https://github.com/Azure/PyRIT). Automated scans using the AI red teaming agent enhances pre-production risk assessment by systematically testing AI applications for risks. This process involves simulated attack scenarios to identify weaknesses in model responses before real-world deployment. By running AI red teaming scans, you can detect and mitigate potential safety issues before deployment. This tool is recommended to be used in conjunction with human-in-the-loop processes such as conventional AI red teaming probing to help accelerate risk identification and aid in the assessment by a human expert.

Alternatively, you can also use [Azure AI Foundry portal's evaluation widget](../how-to/evaluate-generative-ai-app.md) for testing your generative AI applications.  

Once satisfactory results are achieved, the AI application can be deployed to production.

## Post-production monitoring

After deployment, the AI application enters the post-production evaluation phase, also known as online evaluation or monitoring. At this stage, the model is embedded within a real-world product and responds to actual user queries in production. Monitoring ensures that the model continues to behave as expected and adapts to any changes in user behavior or content.

- **Ongoing performance tracking**: Regularly measuring AI application’s response using key metrics to ensure consistent output quality.
- **Incident response**: Quickly responding to any harmful, unfair, or inappropriate outputs that might arise during real-world use.

By [continuously monitoring the AI application’s behavior in production](https://aka.ms/AzureAIMonitoring), you can maintain high-quality user experiences and swiftly address any issues that surface.

## Conclusion

GenAIOps is all about establishing a reliable and repeatable process for managing generative AI applications across their lifecycle. Evaluation plays a vital role at each stage, from base model selection, through pre-production testing, to ongoing post-production monitoring. By systematically measuring and addressing risks and refining AI systems at every step, teams can build generative AI solutions that aren't only powerful but also trustworthy and safe for real-world use.  

Cheat sheet:

| Purpose |  Process | Parameters |
| -----| -----| ----|
| What are you evaluating for? | Identify or build relevant evaluators | - [Quality and performance](./evaluation-metrics-built-in.md?tabs=warning#generation-quality-metrics) ( [Quality and performance sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py))<br> </br> - [Safety and Security](./evaluation-metrics-built-in.md?#risk-and-safety-evaluators) ([Safety and Security sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluatesafetyrisks.py)) <br> </br> - [Custom](../how-to/develop/evaluate-sdk.md#custom-evaluators) ([Custom sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/evaluate.py)) |
| What data should you use?  | Upload or generate relevant dataset | [Generic simulator for measuring Quality and Performance](./concept-synthetic-data.md) ([Generic simulator sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/finetune/Llama-notebooks/datagen/synthetic-data-generation.ipynb)) <br></br> - [Adversarial simulator for measuring Safety and Security](../how-to/develop/simulator-interaction-data.md) ([Adversarial simulator sample notebook](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/src/evaluation/simulate_and_evaluate_online_endpoint.ipynb)) <br></br> AI red teaming agent for running automated scans to assess safety and security vulnerabilities ([AI red teaming agent sample notebook](https://aka.ms/airedteamingagent-sample))|
| What resources should conduct the evaluation? | Run evaluation | - Local run <br> </br>  - Remote cloud run |
| How did my model/app perform? | Analyze results  | [View aggregate scores, view details, score details, compare evaluation runs](..//how-to/evaluate-results.md) |
| How can I improve? | Make changes to model, app, or evaluators | - If evaluation results didn't align to human feedback, adjust your evaluator. <br></br> - If evaluation results aligned to human feedback but didn't meet quality/safety thresholds, apply targeted mitigations. |

## Related content

- [Evaluate your generative AI apps via the playground](../how-to/evaluate-prompts-playground.md)
- [Run automated scans with the AI red teaming agent to assess safety and security risks](../how-to/develop/run-scans-ai-red-teaming-agent.md)
- [Evaluate your generative AI apps with the Azure AI Foundry SDK or portal](../how-to/evaluate-generative-ai-app.md)
- [Evaluation and monitoring metrics for generative AI](evaluation-metrics-built-in.md)
- [Transparency Note for Azure AI Foundry safety evaluations](safety-evaluations-transparency-note.md)
