---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 5/08/2025
ms.author: lagayhar
ms.custom: include file
---

## Features

- **Automated Evaluation**: Integrate offline evaluation into your CI/CD workflows to automate the pre-production assessment of AI models.

- **Built-in Evaluators**: Leverage existing evaluators provided by the [Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md).

    The following evaluators are supported:

    | Category | Evaluator class/Metrics | AI Agent evaluations | GenAI evaluations |
    |--|--|--|--|
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `GroundednessEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `GroundednessProEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `RetrievalEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `RelevanceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `CoherenceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `FluencyEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `SimilarityEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `IntentResolutionEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `TaskAdherenceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `ToolCallAccuracyEvaluator` | Not Supported | Not Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `ResponseCompletenessEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md) | `DocumentRetrievalEvaluator` | Not Supported | Not Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md) | `F1ScoreEvaluator` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md) | `RougeScoreEvaluator` | Not Supported | Not Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md) | `GleuScoreEvaluator` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md) | `BleuScoreEvaluator ` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md) | `MeteorScoreEvaluator` | Not Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `ViolenceEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `SexualEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `SelfHarmEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `HateUnfairnessEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `IndirectAttackEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `ProtectedMaterialEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `CodeVulnerabilityEvaluator` | Supported | Supported |
    | [Risk and safety (AI-assisted)](../how-to/develop/evaluate-sdk.md#risk-and-safety-evaluators-preview) | `UngroundedAttributesEvaluator` | Not Supported | Supported |
    | [Composite](../how-to/develop/evaluate-sdk.md#composite-evaluators) | `QAEvaluator` | Not Supported | Supported |
    | [Composite](../how-to/develop/evaluate-sdk.md#composite-evaluators) | `ContentSafetyEvaluator` | Supported | Supported |
    | [Composite](../how-to/develop/evaluate-sdk.md#composite-evaluators) | `AgentOverallEvaluator` | Not Supported | Not Supported |
    | Operational metrics | Client run duration | Supported | Not Supported |
    | Operational metrics | Server run duration | Supported | Not Supported |
    | Operational metrics | Completion tokens | Supported | Not Supported |
    | Operational metrics | Prompt tokens | Supported | Not Supported |
    | [Custom evaluators](../how-to/develop/evaluate-sdk.md#custom-evaluators) |  | Not Supported | Not Supported |
