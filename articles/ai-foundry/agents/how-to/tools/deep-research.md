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

The Deep Research tool in the Azure AI Foundry Agent Service enables you to integrate a web-based research capability into your systems. The Deep Research capability is a specialized AI capability designed to perform in-depth, multi-step research using data from the public web.  

> [!IMPORTANT]
> * The Deep Research tool uses **Grounding with Bing Search**. Be sure to read and understand all stipulations of its use, including potential [costs](https://www.microsoft.com/bing/apis/grounding-pricing) that can be incurred, the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), and [use and display requirements](./bing-grounding.md#how-to-display-grounding-with-bing-search-results). See the [Grounding with Bing Search](./bing-grounding.md) documentation for more information.
> * The Agents service and SDK use the Azure OpenAI `o3-deep-research` model. This model is not accessible from Azure OpenAI Chat Completions and Responses APIs.
> * When you use Grounding with Bing Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is not subject to the same data processing terms (including location of processing) and does not have the same compliance standards and certifications as the Azure AI Foundry Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal). It is your responsibility to assess whether use of Grounding with Bing Search in your agent meets your needs and requirements.

> [!NOTE]
> * When using Grounding with Bing Search, only the Bing search query, tool parameters, and your resource key are sent to Bing, and no end user-specific information is included. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

## Usage support
The deep research tool is a **code-only release** and available for use using the Agents Python SDK once you complete the Azure AI Foundry project setup described in the following sections.

|Azure AI foundry portal  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  |  |  | ✔️  | ✔️ |

> [!NOTE]
> Once the agent is running, some elements of the agent and thread runs can show up in the Azure AI Foundry user interface.

## Knowledge source support
The deep research tool is tightly integrated with Grounding with Bing Search and only supports web-based research.

## How Deep Research works

At its core, the Deep Research tool orchestrates a multi-step research pipeline uses the Azure OpenAI's `o3-deep-research` model together with Grounding with Bing Search to autonomously search for and read information from multiple online sources appropriate to the user prompt. This enables the Deep Research tool to generate thorough, documented, and cited reports on complex topics. 

### Deep research model deployment

The Deep Research tool uses the Azure OpenAI `o3-deep-research` model for its research tasks. The model was fine-tuned on the Azure OpenAI `o3` reasoning model.

**Key features**:
- Handles data as part of its research tasks.
- 200-K context length, 100-K completion tokens, and May 31, 2024 knowledge cutoff.
- Outputs its thinking as reasoning summary as it analyzes information.
- Delivers a synthesized report at the end of the research task.

**Deployment information**:
- Deployment type: Global Standard
- Available regions: West US, Norway East
- Quotas and limits: Enterprise: `30K RPS / 30M TPM`, Default: `3K RPS / 3M TPM`

### GPT model deployment for clarifying intent

The Deep Research tool uses a second model deployment to clarify the question contained in the user prompt, gather additional context if needed, and precisely scope the research task. This helps make the output of an agent using the Deep Research tool more relevant and actionable, and can help optimize the search for your business scenario.

This second model is selected by the customer during configuration of the Deep Research tool and can be any of the GPT-series models including GPT-4o and GPT-4.1.

### Grounding with Bing Search

Once the task is scoped, the agent using the Deep Research tool invokes the [Grounding with Bing Search](./bing-grounding.md) tool to gather a curated set of recent web data designed to provide the research model with a foundation of authoritative, high quality, up-to-date sources. 

### Task execution

The Deep Research model then executes the research task. This involves reasoning, analyzing, and synthesizing information across all discovered sources. Unlike simple summarization, it reasons step-by-step, pivots as it encounters new insights, and composes a comprehensive answer that's sensitive to nuance, ambiguity, and emerging patterns in the data. 

### Transparency, safety, and compliance

The output is a structured report that documents not only the comprehensive answer, but also provides source citations and describes the model's reasoning path, including any clarifications requested during the session. This makes every answer fully auditable. See the [Transparency note for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/transparency-note) for more information.

## Prerequisites
- If you already have access to the Azure OpenAI `o3` model, no request is required to access the `o3-deep-research`  model. Otherwise, fill out the [request form](https://aka.ms/OAI/deepresearchaccess). 
- An Azure subscription with the ability to create resources [Set up your environment](../../environment-setup.md)
- [Grounding with Bing Search tool](./bing-grounding.md) resource for connecting to your Azure AI Foundry project.
- [Model deployments](../../../model-inference/how-to/create-model-deployments.md) for the following models
    - `o3-deep-research` version `2025-06-26`. This model is available in `West US` and `Norway East`.
    - Any Azure OpenAI GPT model like `gpt-4o` for intent clarification.

## Setup 

To use the Deep Research tool, you need to create the Azure AI Foundry type project, add your Grounding with Bing Search resource as a new connection, deploy the `o3-deep-research-model`, and deploy the selected Azure OpenAI GPT model. 

:::image type="content" source="../../media/tools/deep-research/setup-deep-research-tool.png" alt-text="A diagram of the steps to set up the deep research tool." lightbox="../../media/tools/deep-research/setup-deep-research-tool.png":::

1. Navigate to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and create a new project.
   
   :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-1.png" alt-text="A screenshot of the project creation button." lightbox="../../media/tools/deep-research/deep-research-tool-step-1.png":::

1. Select the Azure AI Foundry project type.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-2.png" alt-text="A screenshot of the Azure AI Foundry project type." lightbox="../../media/tools/deep-research/deep-research-tool-step-2.PNG":::

1. Update the project name and description.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-3.png" alt-text="A screenshot of an example project name." lightbox="../../media/tools/deep-research/deep-research-tool-step-3.png":::

1. Connect a Grounding with Bing Search account.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-4.png" alt-text="A screenshot showing a connection to a Grounding with Bing search account." lightbox="../../media/tools/deep-research/deep-research-tool-step-4.png":::

1. Navigate to the **Models + Endpoints** tab.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-5.png" alt-text="A screenshot of the models and endpoints page." lightbox="../../media/tools/deep-research/deep-research-tool-step-5.png":::

1. Deploy the `o3-deep-research-model` model.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-6.png" alt-text="A screenshot of a deep research model deployment." lightbox="../../media/tools/deep-research/deep-research-tool-step-6.png":::

1. Deploy an Azure OpenAI GPT model. For example `gpt-4o`.

    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-7.png" alt-text="A screenshot of an Azure OpenAI GPT 4o model deployment." lightbox="../../media/tools/deep-research/deep-research-tool-step-7.png":::

## Next steps

Learn [how to use the Deep Research tool](./deep-research-samples.md). 
