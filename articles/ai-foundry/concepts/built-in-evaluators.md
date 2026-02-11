---
title: Built-in Evaluators Reference
titleSuffix: Microsoft Foundry
description: Comprehensive reference for all built-in evaluators in Microsoft Foundry
monikerRange: 'foundry-classic || foundry'
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 01/16/2026
ms.service: azure-ai-foundry
ms.topic: article
---

# Built-in evaluators reference

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Microsoft Foundry provides a comprehensive set of built-in evaluators to assess the quality, safety, and reliability of AI responses throughout the development lifecycle. This reference details all available evaluators, their purposes, required inputs, and guidance on selecting the right evaluator for your use case. You can also create [custom evaluators](./evaluation-evaluators/custom-evaluators.md) tailored to your specific evaluation criteria.

[!INCLUDE [evaluation-preview](../includes/evaluation-preview.md)]

## General purpose evaluators

| Evaluator | Purpose | Inputs |
|--|--|--|
| Coherence | Measures logical consistency and flow of responses.| Query, response |
| Fluency | Measures natural language quality and readability. | Response  |

To learn more, see [General purpose evaluators](./evaluation-evaluators/general-purpose-evaluators.md).

## Textual similarity evaluators

| Evaluator | Purpose | Inputs |
|--|--|--|
| Similarity | AI-assisted textual similarity measurement. | Query, context, ground truth |
| F1 Score | Harmonic mean of precision and recall in token overlaps between response and ground truth. | Response, ground truth |
| BLEU | Bilingual Evaluation Understudy score for translation quality measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| GLEU | Google-BLEU variant for sentence-level assessment measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation measures overlaps in n-grams between response and ground truth. | Response, ground truth |
| METEOR | Metric for Evaluation of Translation with Explicit Ordering measures overlaps in n-grams between response and ground truth. | Response, ground truth |

To learn more, see [Textual similarity evaluators](./evaluation-evaluators/textual-similarity-evaluators.md).

## RAG evaluators

| Evaluator | Purpose | Inputs |
|--|--|--|
| Retrieval | Measures how effectively the system retrieves relevant information. | Query, context |
| Document Retrieval| Measures accuracy in retrieval results given ground truth. | Ground truth, retrieved documents |
| Groundedness | Measures how consistent the response is with respect to the retrieved context. |  Query (optional), context, response |
| Groundedness Pro (preview) | Measures whether the response is consistent with respect to the retrieved context. | Query, context, response |
| Relevance | Measures how relevant the response is with respect to the query. | Query, response| 
| Response Completeness | Measures to what extent the response is complete (not missing critical information) with respect to the ground truth. | Response, ground truth |

To learn more, see [Retrieval-augmented Generation (RAG) evaluators](./evaluation-evaluators/rag-evaluators.md).

## Risk and safety evaluators

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

## Agent evaluators

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

## Azure OpenAI graders

| Evaluator | Purpose |  Inputs |
|--|--|--|
| Model Labeler | Classifies content using custom guidelines and labels. | Query, response, ground truth |
| String Checker | Performs flexible text validations and pattern matching. | Response |
| Text Similarity | Evaluates the quality of text or determine semantic closeness. | Response, ground truth |
| Model Scorer| Generates numerical scores (customized range) for content based on custom guidelines. | Query, response, ground truth |

To learn more, see [Azure OpenAI Graders](./evaluation-evaluators/azure-openai-graders.md).

## Custom evaluators

In addition to built-in evaluators, you can create custom evaluators tailored to your specific evaluation criteria. Custom evaluators allow you to define unique scoring logic, validation rules, and quality metrics that align with your business requirements and application-specific needs.

To learn more, see [Custom evaluators](./evaluation-evaluators/custom-evaluators.md).

## Selecting the right evaluator

Choosing the appropriate evaluator depends on your AI application type and evaluation goals. Use this guide to select evaluators that best match your use case:

### RAG (Retrieval-Augmented Generation) applications

For applications that retrieve information from knowledge bases or documents:

- **Retrieval**: Assess how effectively your system retrieves relevant information from the knowledge base
- **Groundedness**: Verify that responses are consistent with and supported by the retrieved context
- **Groundedness Pro**: Enhanced validation for response consistency with stricter criteria (preview)
- **Relevance**: Ensure responses directly address the user's query
- **Document Retrieval**: Validate retrieval accuracy against known ground truth documents

### Agent applications

For AI agents that use tools and follow multi-step workflows:

- **Tool Call Accuracy**: Measure overall quality of tool selection, parameter correctness, and efficiency
- **Tool Selection**: Validate that agents choose the most appropriate tools for each task
- **Tool Input Accuracy**: Ensure tool parameters are correct, properly formatted, and well-grounded
- **Tool Output Utilization**: Verify agents correctly interpret and use tool results
- **Task Adherence**: Confirm agents follow system instructions and complete identified tasks
- **Task Completion**: Measure end-to-end task success
- **Intent Resolution**: Assess how accurately agents identify and address user intentions
- **Task Navigation Efficiency**: Evaluate whether agents follow optimal paths to task completion

### Safety and security validation

For all AI applications requiring content safety and security checks:

- **Content Safety**: Comprehensive assessment covering hate, sexual, violence, and self-harm content
- **Hate and Unfairness**: Detect biased, discriminatory, or hateful content
- **Sexual**: Identify inappropriate sexual content
- **Violence**: Detect violent content or incitement to violence
- **Self-Harm**: Identify content promoting or describing self-harm
- **Protected Materials**: Detect unauthorized use of copyrighted or protected content
- **Code Vulnerability**: Identify security issues in AI-generated code
- **Ungrounded Attributes**: Detect fabricated or hallucinated information

### Translation and localization quality

For applications that translate or localize content:

- **BLEU**: Measure n-gram overlap for translation quality assessment
- **METEOR**: Evaluate translation with explicit word ordering and synonym matching
- **ROUGE**: Assess recall-oriented quality for gisting and summarization
- **GLEU**: Perform sentence-level translation quality measurement
- **F1 Score**: Calculate harmonic mean of precision and recall in token overlaps

### General content quality

For assessing overall response quality across any application type:

- **Coherence**: Evaluate logical consistency and flow of responses
- **Fluency**: Measure natural language quality and readability
- **Similarity**: Compare semantic similarity between responses and expected outputs
- **Response Completeness**: Verify responses contain all critical information from ground truth

### Combining evaluators

For comprehensive quality assessment, combine multiple evaluators:

- **RAG applications**: Retrieval + Groundedness + Relevance + Content Safety
- **Agent applications**: Tool Call Accuracy + Task Adherence + Intent Resolution + Content Safety
- **Translation applications**: BLEU + METEOR + Fluency + Coherence
- **All applications**: Add risk and safety evaluators (Hate and Unfairness, Sexual, Violence, Self-Harm) for responsible AI practices

## Related content

- [Observability in generative AI](./observability.md)
- [General purpose evaluators](./evaluation-evaluators/general-purpose-evaluators.md)
- [Textual similarity evaluators](./evaluation-evaluators/textual-similarity-evaluators.md)
- [Retrieval-augmented Generation (RAG) evaluators](./evaluation-evaluators/rag-evaluators.md)
- [Risk and safety evaluators](./evaluation-evaluators/risk-safety-evaluators.md)
- [Agent evaluators](./evaluation-evaluators/agent-evaluators.md)
- [Azure OpenAI Graders](./evaluation-evaluators/azure-openai-graders.md)
- [Custom evaluators](./evaluation-evaluators/custom-evaluators.md)
- [Evaluate with the Foundry SDK](../how-to/develop/evaluate-sdk.md)
- [Evaluate generative AI apps in Foundry](../how-to/evaluate-generative-ai-app.md)
