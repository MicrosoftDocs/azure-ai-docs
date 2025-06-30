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
> * Deep Research uses **Grounding with Bing Search**. Be sure to read and understand all stipulations of its use, including potential [costs](https://www.microsoft.com/bing/apis/grounding-pricing) that can be incurred, the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), and [use and display requirements](./bing-grounding.md#how-to-display-grounding-with-bing-search-results). See the [Grounding with Bing Search](./bing-grounding.md) documentation for more information.
> * Deep Research is not available in Azure OpenAI. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  |  |  | ✔️  | ✔️ |

## How Deep Research works

At its core, the Deep Research tool orchestrates a multi-step research pipeline that’s tightly integrated with Grounding with Bing Search and Azure OpenAI models

### Clarifying intent and scoping the task

When a user or downstream app submits a research query, the agent uses GPT-series models including GPT-4o and GPT-4.1 to clarify the question, gather additional context if needed, and precisely scope the research task. This ensures the agent’s output is both relevant and actionable, and that every search is optimized for your business scenario.

### Grounding with Bing Search

Once the task is scoped, the agent invokes the [Grounding with Bing Search](./bing-grounding.md) tool to gather a curated set of high-quality, recent web data. This ensures the research model is working from a foundation of authoritative, up-to-date sources. 

### Task execution

The Deep Research model then starts the research task execution. This involves thinking reasoning, analyzing, and synthesizing information across all discovered sources. Unlike simple summarization, it reasons step-by-step, pivots as it encounters new insights, and composes a comprehensive answer that's sensitive to nuance, ambiguity, and emerging patterns in the data. 

### Transparency, safety, and compliance

Every stage of the process is safeguarded by input/output classifiers and chain-of-thought (CoT) summarizers. The final output is a structured report that documents not only the answer, but also the model's reasoning path, source citations, and any clarifications requested during the session. This makes every answer fully auditable.

## Prerequisites
- A basic or standard agent [environment setup](../../environment-setup.md)
- Access to the Deep Research model is gated. Fill out the [request form](https://aka.ms/OAI/deepresearchaccess) for access. If you have already have access to the o3 model no request is required.

To use Deep Research, you will create the following in this article:

- The [Grounding with Bing Search tool](./bing-grounding.md)
- A [deployed models](../../../model-inference/how-to/create-model-deployments.md) and the following model
    - `o3-deep-research` version `2025-06-26`. This model is available in `West US` and `Norway East`.

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