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
    | Performance and quality (AI-assisted) | `GroundednessEvaluator` | Not Supported | Supported |
    | Performance and quality (AI-assisted) | [`GroundednessProEvaluator`](../concepts/evaluation-evaluators/rag-evaluators#groundedness-pro) | Not Supported | Supported |
    | Performance and quality (AI-assisted) | `RetrievalEvaluator` | Not Supported | Supported |
    | Performance and quality (AI-assisted)| `RelevanceEvaluator` | Supported | Supported |
    | Performance and quality (AI-assisted) | `CoherenceEvaluator` | Supported | Supported |
    | Performance and quality (AI-assisted) | `FluencyEvaluator` | Supported | Supported |
    | Performance and quality (AI-assisted)| `SimilarityEvaluator` | Not Supported | Supported |
    | Performance and quality (AI-assisted) | `IntentResolutionEvaluator` | Supported | Supported |
    | Performance and quality (AI-assisted)| `TaskAdherenceEvaluator` | Supported | Supported |
    | Performance and quality (AI-assisted) | `ToolCallAccuracyEvaluator` | Not Supported | Not Supported |
    | Performance and quality (AI-assisted) | `ResponseCompletenessEvaluator` | Not Supported | Supported |
    | Performance and quality (AI-assisted) | `DocumentRetrievalEvaluator` | Not Supported | Not Supported |
    | Performance and quality (NLP) | `F1ScoreEvaluator` | Not Supported | Supported |
    | Performance and quality (NLP) | `RougeScoreEvaluator` | Not Supported | Not Supported |
    | Performance and quality (NLP) | `GleuScoreEvaluator` | Not Supported | Supported |
    | Performance and quality (NLP) | `BleuScoreEvaluator ` | Not Supported | Supported |
    | Performance and quality (NLP) | `MeteorScoreEvaluator` | Not Supported | Supported |
    | Risk and safety (AI-assisted)| `ViolenceEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted) | `SexualEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted) | `SelfHarmEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted)| `HateUnfairnessEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted)| `IndirectAttackEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted)| `ProtectedMaterialEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted)| `CodeVulnerabilityEvaluator` | Supported | Supported |
    | Risk and safety (AI-assisted)| `UngroundedAttributesEvaluator` | Not Supported | Supported |
    | Composite| `QAEvaluator` | Not Supported | Supported |
    | Composite | `ContentSafetyEvaluator` | Supported | Supported |
    | Composite| `AgentOverallEvaluator` | Not Supported | Not Supported |
    | Operational metrics | Client run duration | Supported | Not Supported |
    | Operational metrics | Server run duration | Supported | Not Supported |
    | Operational metrics | Completion tokens | Supported | Not Supported |
    | Operational metrics | Prompt tokens | Supported | Not Supported |
    | [Custom evaluators](../concepts/evaluation-evaluators/custom-evaluators.md) |  | Not Supported | Not Supported |
