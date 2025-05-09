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
    | General purpose| [QAEvaluator](../concepts/evaluation-evaluators/general-purpose-evaluators.md##question-answering-composite-evaluator)| Not Supported | Supported |
    | General purpose (AI-assisted) | [CoherenceEvaluator](../concepts/evaluation-evaluators/general-purpose-evaluators.md#coherence) | Supported | Supported |
    | General purpose (AI-assisted)| [FluencyEvaluator](../concepts/evaluation-evaluators/general-purpose-evaluators.md#fluency) | Supported | Supported |
    | Textual similarity | [SimilarityEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators.md#similarity) | Not Supported | Supported |
    | Textual similarity | [F1ScoreEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators#f1-score) | Not Supported | Supported |
    | Textual similarity | [RougeScoreEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators) | Not Supported | Not Supported |
    | Textual similarity | [GleuScoreEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators#gleu-score) | Not Supported | Supported |
    | Textual similarity | [BleuScoreEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators#bleu-score) | Not Supported | Supported |
    | Textual similarity | [MeteorScoreEvaluator](../concepts/evaluation-evaluators/textual-similarity-evaluators#meteor-score) | Not Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted)| [GroundednessEvaluator](../concepts/evaluation-evaluators/rag-evaluators.md#groundedness) | Not Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted) | [GroundednessProEvaluator](../concepts/evaluation-evaluators/rag-evaluators.md#groundedness-pro) | Not Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted)  | [RetrievalEvaluator](../concepts/evaluation-evaluators/rag-evaluators.md#relevance) | Not Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted)  | [RelevanceEvaluator](../concepts/evaluation-evaluators/rag-evaluators.md#retrieval) | Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted) | [ResponseCompletenessEvaluator`](../concepts/evaluation-evaluators/rag-evaluators.md#response-completeness)| Not Supported | Supported |
    | Retrieval-augmented Generation (RAG) (AI-assisted) | [DocumentRetrievalEvaluator](../concepts/evaluation-evaluators/rag-evaluators.md#document-retrieval) | Not Supported | Not Supported |
    | Risk and safety (AI-assisted)| [ViolenceEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#violent-content)| Supported | Supported |
    | Risk and safety (AI-assisted) | [SexualEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#sexual-content) | Supported | Supported |
    | Risk and safety (AI-assisted) | [SelfHarmEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#self-harm-related-content) | Supported | Supported |
    | Risk and safety (AI-assisted)| [HateUnfairnessEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#hateful-and-unfair-content)| Supported | Supported |
    | Risk and safety (AI-assisted)| [IndirectAttackEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#indirect-attack-jailbreak-xpia)| Supported | Supported |
    | Risk and safety (AI-assisted)| [ProtectedMaterialEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#protected-material-content) | Supported | Supported |
    | Risk and safety (AI-assisted)| [CodeVulnerabilityEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#code-vulnerability) | Supported | Supported |
    | Risk and safety (AI-assisted)| [UngroundedAttributesEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md##ungrounded-attributes) | Not Supported | Supported |
    | Risk and safety (AI-assisted) | [ContentSafetyEvaluator](../concepts/evaluation-evaluators/risk-safety-evaluators.md#content-safety-composite-evaluator) | Supported | Supported |
    | Agent (AI-assisted) | [IntentResolutionEvaluator](../concepts/evaluation-evaluators/agent-evaluators.md#intent-resolution)| Supported | Supported |
    | Agent (AI-assisted)| [TaskAdherenceEvaluator](../concepts/evaluation-evaluators/agent-evaluators.md#task-adherence) | Supported | Supported |
    | Agent (AI-assisted) | [ToolCallAccuracyEvaluator](/concepts/evaluation-evaluators/agent-evaluators.md#tool-call-accuracy) | Not Supported | Not Supported |
    | Composite | `AgentOverallEvaluator` | Not Supported | Not Supported |
    | Operational metrics | Client run duration | Supported | Not Supported |
    | Operational metrics | Server run duration | Supported | Not Supported |
    | Operational metrics | Completion tokens | Supported | Not Supported |
    | Operational metrics | Prompt tokens | Supported | Not Supported |
    | [Custom evaluators](../concepts/evaluation-evaluators/custom-evaluators.md) |  | Not Supported | Not Supported |
