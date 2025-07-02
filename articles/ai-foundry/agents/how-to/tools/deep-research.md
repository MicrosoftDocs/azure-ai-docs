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

The Deep Research model in the Azure AI Foundry Agent Service enables you to use an advanced agentic research capability, and integrate it with your data and systems.

> [!IMPORTANT]
> * The Deep Research tool uses **Grounding with Bing Search**. Be sure to read and understand all stipulations of its use, including potential [costs](https://www.microsoft.com/bing/apis/grounding-pricing) that can be incurred, the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), and [use and display requirements](./bing-grounding.md#how-to-display-grounding-with-bing-search-results). See the [Grounding with Bing Search](./bing-grounding.md) documentation for more information.
> * The Deep Research tool uses the Azure OpenAI `o3-deep-research` model. This model is not available in Azure OpenAi service.

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  |  |  | ✔️  | ✔️ |

## How Deep Research works

At its core, the Deep Research tool orchestrates a multi-step research pipeline that’s tightly integrated with Grounding with Bing Search and the Azure OpenAI deep research model.

### Deep research model deployment

The Deep research tool uses the `o3-deep-research` model for its research tasks. It is a fine-tuned version of the `o3` model designed to perform automated detailed analysis of knowledge sources and create detailed research reports.

**Key features**:
- Handles text, images and PDFs as part of its research tasks
- 200K context length, 100K completion tokens, and May 31, 2024 knowledge cutoff
- Outputs its thinking as reasoning summary as it analyzes information
- Delivers a synthesized report at the end of the research task

**Deployment information**:
- Deployment type: Global Standard
- Regions: West US, Norway East
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
- A basic or standard agent [environment setup](../../environment-setup.md)
- Access to the Deep Research model is gated. Fill out the [request form](https://aka.ms/OAI/deepresearchaccess) for access. If you have already have access to the o3 model no request is required.

## Setup 

To use the Deep Research model, you need to create a new project and add your Grounding with Bing Search resource as a new connection. In the [AI Foundry portal](https://ai.azure.com/?cid=learnDocs):

1. :::image type="content" source="../../media/tools/deep-research/project-creation.png" alt-text="A screenshot of  project creation in Azure AI Foundry." lightbox="../../media/tools/deep-research/project-creation.png":::

1. Navigate to the project you created in the agent setup. Click on **Open in management center**.
    :::image type="content" source="../../media/tools/ai-search/project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../../media/tools/ai-search/project-studio.png":::

1. Select **Create connection**.

    :::image type="content" source="../../media/create-connection.png" alt-text="A screenshot showing the connection creation screen in the Azure AI Foundry portal" lightbox="../../media/create-connection.png":::

1. In the screen that appears, select **Grounding with Bing Search**. Then enter your connection details.

    :::image type="content" source="../../media/tools/deep-research/bing-connection.png" alt-text="A screenshot of the screen to select Grounding with Bing Search." lightbox="../../media/tools/deep-research/bing-connection.png":::

    :::image type="content" source="../../media/tools/bing/add-connection.png" alt-text="A screenshot of the screen to add a Grounding with Bing Search connection." lightbox="../../media/tools/bing/add-connection.png":::

1. Deploy the Deep Research model. Select **Models + Endpoints**. Then select **Deploy model**. 

    :::image type="content" source="../../media/deploy-model.png" alt-text="A screenshot of the screen to deploy a model." lightbox="../../media/deploy-model.png":::

1. Search for the `o3-deep-research` model, and confirm the model deployment.

    > [!NOTE]
    > You also need to deploy a GPT chat model in your project, for example GPT-4o.

    :::image type="content" source="../../media/tools/deep-research/deep-research-model.png" alt-text="A screenshot of the model deployment." lightbox="../../media/tools/deep-research/deep-research-model.png":::

## Next steps

Learn [how to use the Deep Research tool](./deep-research-samples.md). 
