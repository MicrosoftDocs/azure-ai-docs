---
title: "Deep research tool"
titleSuffix: Azure AI Foundry
description: Learn how to use the deep research tool with agents.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 06/25/2025
ms.service: azure-ai-agent-service
ms.topic: how-to
---

# Deep Research tool (preview)

The Deep Research model in the Azure AI Foundry Agent Service enables you to use web-based research capability, and integrate it with your systems.

> [!IMPORTANT]
> * The Deep Research tool uses **Grounding with Bing Search**. Be sure to read and understand all stipulations of its use, including potential [costs](https://www.microsoft.com/bing/apis/grounding-pricing) that can be incurred, the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), and [use and display requirements](./bing-grounding.md#how-to-display-grounding-with-bing-search-results). See the [Grounding with Bing Search](./bing-grounding.md) documentation for more information.
> * The Deep Research tool uses the Azure OpenAI `o3-deep-research` model. This model is not available in the Azure OpenAI service.

> [!NOTE]
> When using Grounding with Bing Search, only the Bing search query, tool parameters, and your resource key are sent to Bing, and no end user-specific information is included. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

## Usage support
The deep research tool is a **code-only release** and available for use using the Agents Python SDK once you complete the AI Foundry project setup described in the following sections.

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  |  |  | ✔️  | ✔️ |

> [!NOTE]
> Once the agent is running, some elements of the agent and thread runs can show up in the Foundry user interface.

## Knowledge source support
The deep research tool is tightly integrated with Grounding with Bing Search and only supports web-based research.

## How Deep Research works

At its core, the Deep Research tool orchestrates a multi-step research pipeline that’s tightly integrated with Grounding with Bing Search and the Azure OpenAI deep research model.

### Deep research model deployment

The Deep research tool uses the `o3-deep-research` model for its research tasks. It is a fine-tuned version of the `o3` model designed to perform automated detailed analysis of knowledge sources and create detailed research reports.

**Key features**:
- Handles text, images, and PDFs as part of its research tasks
- 200-K context length, 100K completion tokens, and May 31, 2024 knowledge cutoff
- Outputs its thinking as reasoning summary as it analyzes information
- Delivers a synthesized report at the end of the research task

**Deployment information**:
- Deployment type: Global Standard
- Available regions: West US, Norway East
- Quotas and limits: Enterprise: 30 K RPS/ 30 M TPM, Default: 3 K RPS/ 3 M TPM

### GPT model deployment for clarifying intent

The deep research tool uses a second model deployment to clarify the question, gather additional context if needed, and precisely scope the research task. This ensures the agent’s output is both relevant and actionable, and that every search is optimized for your business scenario.

This second model can be any of the GPT-series models including GPT-4o and GPT-4.1.

### Grounding with Bing Search

Once the task is scoped, the agent invokes the [Grounding with Bing Search](./bing-grounding.md) tool to gather a curated set of high-quality, recent web data. This ensures the research model is working from a foundation of authoritative, up-to-date sources. 

### Task execution

The Deep Research model then starts the research task execution. This involves thinking reasoning, analyzing, and synthesizing information across all discovered sources. Unlike simple summarization, it reasons step-by-step, pivots as it encounters new insights, and composes a comprehensive answer that's sensitive to nuance, ambiguity, and emerging patterns in the data. 

### Transparency, safety, and compliance

The output is a structured report that documents not only the answer, but also the model's reasoning path, source citations, and any clarifications requested during the session. This makes every answer fully auditable.

## Prerequisites
- If you already have access to the `o3` model no request is required for the deep research model. Otherwise, fill out the [request form](https://aka.ms/OAI/deepresearchaccess). 
- An Azure subscription with the ability to create resources [Set up your environment](../../environment-setup.md)
- [Grounding with Bing Search tool](./bing-grounding.md) resource for connecting to your AI Foundry project.
- [Model deployments](../../../model-inference/how-to/create-model-deployments.md) for the following models
    - `o3-deep-research` version `2025-06-26`. This model is available in `West US` and `Norway East`.
    - Any GPT model like the `gpt-4o` for intent clarification.

## Setup 

To use the Deep Research tool, you need to create the AI Foundry type project, add your Grounding with Bing Search resource as a new connection, deploy the deep research model, and deploy the GPT model. 

:::image type="content" source="../../media/tools/deep-research/setup-deep-research-tool.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/setup-deep-research-tool.png":::

1. Navigate to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and create a new project.
   
   :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-1.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-1.png":::

1. Select the Azure AI Foundry project type.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-2.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-2.PNG":::

1. Update the project name and description
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-3.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-3.png":::

1. Connect a Grounding with Bing Search account
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-4.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-4.png":::

1. Navigate to the **Models + Endpoints** tab.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-5.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-5.png":::

1. Deploy the deep research model.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-6.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-6.png":::

1. Deploy a GPT model. For example gpt-4o

    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-7.png" alt-text="Steps to set up the deep research tool." lightbox="../../media/tools/deep-research/deep-research-tool-step-7.png":::

## Next steps

Learn [how to use the Deep Research tool](./deep-research-samples.md). 
