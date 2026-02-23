---
title: Built-in Evaluators Reference
titleSuffix: Microsoft Foundry
description: Comprehensive reference for all built-in evaluators in Microsoft Foundry
monikerRange: 'foundry-classic || foundry'
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 02/12/2026
ms.service: azure-ai-foundry
ms.topic: article
---

# Built-in evaluators reference

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Microsoft Foundry provides a comprehensive set of built-in evaluators to assess the quality, safety, and reliability of AI responses throughout the development lifecycle. This reference details all available evaluators, their purposes, required inputs, and guidance on selecting the right evaluator for your use case. You can also create [custom evaluators](./evaluation-evaluators/custom-evaluators.md) tailored to your specific evaluation criteria.

[!INCLUDE [evaluation-preview](../includes/evaluation-preview.md)]

## General purpose evaluators

| Evaluator | Purpose |
|--|--|--|
| Coherence | Measures logical consistency and flow of responses.|
| Fluency | Measures natural language quality and readability. |

To learn more, see [General purpose evaluators](./evaluation-evaluators/general-purpose-evaluators.md).

## Textual similarity evaluators

| Evaluator | Purpose |
|--|--|--|
| Similarity | AI-assisted textual similarity measurement. |
| F1 Score | Harmonic mean of precision and recall in token overlaps between response and ground truth. |
| BLEU | Bilingual Evaluation Understudy score for translation quality measures overlaps in n-grams between response and ground truth. |
| GLEU | Google-BLEU variant for sentence-level assessment measures overlaps in n-grams between response and ground truth. |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation measures overlaps in n-grams between response and ground truth. |
| METEOR | Metric for Evaluation of Translation with Explicit Ordering measures overlaps in n-grams between response and ground truth. |

To learn more, see [Textual similarity evaluators](./evaluation-evaluators/textual-similarity-evaluators.md).

## RAG evaluators

| Evaluator | Purpose |
|--|--|--|
| Retrieval | Measures how effectively the system retrieves relevant information. |
| Document Retrieval| Measures accuracy in retrieval results given ground truth. |
| Groundedness | Measures how consistent the response is with respect to the retrieved context. |
| Groundedness Pro (preview) | Measures whether the response is consistent with respect to the retrieved context. |
| Relevance | Measures how relevant the response is with respect to the query. |
| Response Completeness | Measures to what extent the response is complete (not missing critical information) with respect to the ground truth. |

To learn more, see [Retrieval-augmented Generation (RAG) evaluators](./evaluation-evaluators/rag-evaluators.md).

## Risk and safety evaluators

| Evaluator | Purpose |
|--|--|--|
| Hate and Unfairness | Identifies biased, discriminatory, or hateful content. |
| Sexual | Identifies inappropriate sexual content. |
| Violence | Detects violent content or incitement. |
| Self-Harm | Detects content promoting or describing self-harm.|
| Content Safety | Comprehensive assessment of various safety concerns. |
| Protected Materials | Detects unauthorized use of copyrighted or protected content. |
| Code Vulnerability | Identifies security issues in generated code. |
| Ungrounded Attributes | Detects fabricated or hallucinated information inferred from user interactions. |

To learn more, see [Risk and safety evaluators](./evaluation-evaluators/risk-safety-evaluators.md).

## Agent evaluators

::: moniker range="foundry-classic"

| Evaluator | Purpose |
|--|--|--|
| Intent Resolution (preview) | Measures how accurately the agent identifies and addresses user intentions. |
| Task Adherence (preview)| Measures how well the agent follows through on identified tasks. |
| Tool Call Accuracy (preview) | Measures how well the agent selects and calls the correct tools to. |

::: moniker-end

::: moniker range="foundry"

| Evaluator | Purpose |
|--|--|--|
| Task Adherence (preview)  | Measures whether the agent follows through on identified tasks according to system instructions. |
| Task Completion (preview)| Measures whether the agent successfully completed the requested task end-to-end. |
| Intent Resolution (preview) | Measures how accurately the agent identifies and addresses user intentions. |
| Task Navigation Efficiency (preview) | Determines whether the agent's sequence of steps matches an optimal or expected path to measure efficiency. |
| Tool Call Accuracy (preview) | Measures the overall quality of tool calls including selection, parameter correctness, and efficiency. |
| Tool Selection (preview) | Measures whether the agent selected the most appropriate and efficient tools for a task. |
| Tool Input Accuracy (preview)| Validates that all tool call parameters are correct with strict criteria including grounding, type, format, completeness, and appropriateness. |
| Tool Output Utilization (preview)| Measures whether the agent correctly interprets and uses tool outputs contextually in responses and subsequent calls. |
| Tool Call Success (preview) | Evaluates whether all tool calls executed successfully without technical failures. |

::: moniker-end

To learn more, see [Agent evaluators](./evaluation-evaluators/agent-evaluators.md).

## Azure OpenAI graders

| Evaluator | Purpose |
|--|--|--|
| Model Labeler | Classifies content using custom guidelines and labels. |
| String Checker | Performs flexible text validations and pattern matching. |
| Text Similarity | Evaluates the quality of text or determine semantic closeness. |
| Model Scorer| Generates numerical scores (customized range) for content based on custom guidelines. |

To learn more, see [Azure OpenAI Graders](./evaluation-evaluators/azure-openai-graders.md).

## Custom evaluators

In addition to built-in evaluators, you can create custom evaluators tailored to your specific evaluation criteria. Custom evaluators allow you to define unique scoring logic, validation rules, and quality metrics that align with your business requirements and application-specific needs.

To learn more, see [Custom evaluators](./evaluation-evaluators/custom-evaluators.md).

## Combining evaluators

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
