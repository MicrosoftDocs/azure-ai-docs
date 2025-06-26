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

# Deep Research tool

The [Deep Research](https://openai.com/index/introducing-deep-research/) model in the Azure AI Foundry Agent Service enables you to use OpenAI's advanced agentic research capability, and integrate it with your data and systems.

> [!IMPORTANT]
> Deep Research uses **Grounding with Bing Search**. Be sure to read and understand all stipulations of its use, including potential [costs](https://www.microsoft.com/bing/apis/grounding-pricing) that can be incurred, the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), and [use and display requirements](./bing-grounding.md#how-to-display-grounding-with-bing-search-results). See the [Grounding with Bing Search](./bing-grounding.md) documentation for more information.

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  |  |  | ✔️  | ✔️ |

## How Deep Research works

At its core, the Deep Research tool orchestrates a multi-step research pipeline that’s tightly integrated with Grounding with Bing Search and Azure OpenAI models

### Clarifying intent and scoping the task

When a user or downstream app submits a research query, the agent uses GPT-4o to clarify the question, gather additional context if needed, and precisely scope the research task. This ensures the agent’s output is both relevant and actionable, and that every search is optimized for your business scenario.

### Grounding with Bing Search

Once the task is scoped, the agent invokes the [Grounding with Bing Search](./bing-grounding.md) tool to gather a curated set of high-quality, recent web data. This ensures the research model is working from a foundation of authoritative, up-to-date sources. 

### Task execution

The Deep Research model then starts the research task execution. This involves thinking reasoning, analyzing, and synthesizing information across all discovered sources. Unlike simple summarization, it reasons step-by-step, pivots as it encounters new insights, and composes a comprehensive answer that's sensitive to nuance, ambiguity, and emerging patterns in the data. 

### Transparency, safety, and compliance

Every stage of the process is safeguarded by input/output classifiers and chain-of-thought (CoT) summarizers. The final output is a structured report that documents not only the answer, but also the model's reasoning path, source citations, and any clarifications requested during the session. This makes every answer fully auditable.

## Prerequisites
- A basic or standard agent [environment setup](../../environment-setup.md)
- The [Grounding with Bing Search tool](./bing-grounding.md)
- The following [deployed models](../../../model-inference/how-to/create-model-deployments.md)
    - **GPT-4o**
    - **o3-deep-research** 
- A [deployed agent](../quickstart.md)

## Setup 

To use the Deep Research model, you need to add your Grounding with Bing Search as a new connection. In the [AI Foundry portal](https://ai.azure.com/?cid=learnDocs):

1. In Azure AI Foundry, navigate to the project you created in the agent setup. Click on **Open in management center**.
    :::image type="content" source="../../media\tools\ai-search\project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../../media\tools\ai-search\project-studio.png":::

1. Select **Create connection**.

    :::image type="content" source="../../media/create-connection.png" alt-text="A screenshot showing the connection creation screen in the Azure AI Foundry portal" lightbox="../../media/create-connection.png":::

1. In the screen that appears, select **Grounding with Bing Search**. 

    :::image type="content" source="../../media\tools\bing\add-connection.png" alt-text="A screenshot of the screen to add a Grounding with Bing Search connection." lightbox="../../media\tools\bing\add-connection.png":::
