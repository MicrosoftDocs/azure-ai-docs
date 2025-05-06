---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 4/30/2025
ms.author: lagayhar
ms.custom: include file
---

## Features

- **Automated Evaluation**: Integrate offline evaluation into your CI/CD workflows to automate the pre-production assessment of AI models.

- **Built-in Evaluators**: Leverage existing evaluators provided by the [Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md).

    The following evaluators are supported:

    | Category | Evaluator class/Metrics | AI Agent evals | GenAI evals |
    |--|--|--|--|
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `GroundednessEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `GroundednessProEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `RetrievalEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `RelevanceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `CoherenceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `FluencyEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `SimilarityEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `IntentResolutionEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `TaskAdherenceEvaluator` | Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `ToolCallAccuracyEvaluator` | Supported | Not Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `ResponseCompletenessEvaluator` | Not Supported | Supported |
    | [Performance and quality (AI-assisted)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `DocumentRetrievalEvaluator` | Not Supported | Not Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `F1ScoreEvaluator` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `RougeScoreEvaluator` | Not Supported | Not Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `GleuScoreEvaluator` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `BleuScoreEvaluator ` | Not Supported | Supported |
    | [Performance and quality (NLP)](../how-to/develop/evaluate-sdk.md#performance-and-quality-evaluators) | `MeteorScoreEvaluator` | Not Supported | Supported |
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
