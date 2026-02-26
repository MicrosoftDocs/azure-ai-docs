---
title: "Deep research tool"
titleSuffix: Microsoft Foundry
description: Learn how to use the deep research tool with agents.
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 11/19/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom: references_regions
---

# Deep Research tool (preview)

> [!NOTE]
> * The **parent** Foundry project resource and the contained  `o3-deep-research` model and GPT models **must exist** in the same Azure subscription and region. Supported regions are **West US** and **Norway East**.
> * This tool is only available in `2025-05-15-preview` API. We highly recommend that you migrate to use the `2025-11-15-preview` API. This enables you to use the `o3-deep-research` model with [web search](../../../default/agents/how-to/tools/web-search.md) or MCP tool.

The Deep Research tool in the Foundry Agent Service enables you to integrate a web-based research capability into your systems. The Deep Research capability is a specialized AI capability designed to perform in-depth, multi-step research using data from the public web.  

## Usage support
The deep research tool is a **code-only release** and available for use using the Agents Python SDK once you complete the Microsoft Foundry project setup described in the following sections.

|Azure AI foundry portal  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ | ✔️ | ✔️ |  | ✔️  | ✔️ |

> [!NOTE]
> Once the agent is running, some elements of the agent and thread runs can show up in the Foundry user interface.

## Integrated with Grounding with Bing Search
The deep research tool is tightly integrated with Grounding with Bing Search and only supports web-based research. Once the task is scoped, the agent using the Deep Research tool invokes the [Grounding with Bing Search](./bing-grounding.md) tool to gather a curated set of recent web data designed to provide the research model with a foundation of authoritative, high quality, up-to-date sources. 

> [!IMPORTANT]
> 1. Your usage of Grounding with Bing Search can incur costs. See the [pricing page](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> 1. By creating and using a Grounding with Bing Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the terms available at https://www.microsoft.com/en-us/bing/apis/grounding-legal, which may be updated from time to time.
> 1. When you use Grounding with Bing Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is not subject to the same data processing terms (including location of processing) and does not have the same compliance standards and certifications as the Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal). It is your responsibility to assess whether use of Grounding with Bing Search in your agent meets your needs and requirements.

> [!NOTE]
> When using Grounding with Bing Search, only the Bing search query, tool parameters, and your resource key are sent to Bing, and no end user-specific information is included. Your resource key is sent to Bing solely for billing and rate limiting purposes.

## Regions supported
The Deep Research tool is supported in the following regions where the deep research model is available for deployment.

|West US  | Norway East |
|---------|---------|
| ✔️ | ✔️ | 

## GPT-4o model for clarifying research scope

The Deep Research tool uses the `gpt-4o` model to clarify the question contained in the user prompt, gather additional context if needed, and precisely scope the research task. This model is deployed during configuration of the Deep Research tool. 

> [!NOTE]
> Other GPT-series models including GPT-4o-mini and the GPT-4.1 series are not supported for scope clarification.

## Deep research model for analysis

- **Model name**: `o3-deep-research`
- **Deployment type**: Global Standard
- **Available regions**: West US, Norway East
- **Quotas and limits**: Enterprise: `30K RPS / 30M TPM`, Default: `3K RPS / 3M TPM`
  
## Research tool prerequisites
- If you already have access to the Azure OpenAI `o3` model, no request is required to access the `o3-deep-research`  model. Otherwise, fill out the [request form](https://aka.ms/OAI/deepresearchaccess). 
- An Azure subscription with the ability to create Foundry project, Grounding with Bing Search, deep research model and GPT model resources [Set up your environment](../../environment-setup.md) in the **West US** and **Norway East** regions.
- [Grounding with Bing Search tool](./bing-grounding.md) resource for connecting to your Foundry project.
- [Model deployments](../../../foundry-models/how-to/create-model-deployments.md) for the following models
    - `o3-deep-research` version `2025-06-26`. This model is available in `West US` and `Norway East`.
    - The `gpt-4o` model for intent clarification. Deploy this model in the same region.

## Research tool setup 

To use the Deep Research tool, you need to create the Foundry type project, add your Grounding with Bing Search resource as a new connection, deploy the `o3-deep-research-model`, and deploy the selected Azure OpenAI GPT model. 

:::image type="content" source="../../media/tools/deep-research/setup-deep-research-tool.png" alt-text="A diagram of the steps to set up the deep research tool." lightbox="../../media/tools/deep-research/setup-deep-research-tool.png":::

1. Navigate to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and create a new project.
   
   :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-1.png" alt-text="A screenshot of the project creation button." lightbox="../../media/tools/deep-research/deep-research-tool-step-1.png":::

1. Select the Foundry project type.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-2.png" alt-text="A screenshot of the Foundry project type." lightbox="../../media/tools/deep-research/deep-research-tool-step-2.PNG":::

1. Update the project name and description.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-3.png" alt-text="A screenshot of an example project name." lightbox="../../media/tools/deep-research/deep-research-tool-step-3.png":::

1. Navigate to the **Models + Endpoints** tab.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-5.png" alt-text="A screenshot of the models and endpoints page." lightbox="../../media/tools/deep-research/deep-research-tool-step-5.png":::

1. Deploy the `o3-deep-research-model` model.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-6.png" alt-text="A screenshot of a deep research model deployment." lightbox="../../media/tools/deep-research/deep-research-tool-step-6.png":::

1. Deploy an Azure OpenAI GPT model. For example `gpt-4o`.

    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-7.png" alt-text="A screenshot of an Azure OpenAI GPT 4o model deployment." lightbox="../../media/tools/deep-research/deep-research-tool-step-7.png":::

1. Connect a Grounding with Bing Search account.
   
    :::image type="content" source="../../media/tools/deep-research/deep-research-tool-step-4.png" alt-text="A screenshot showing a connection to a Grounding with Bing search account." lightbox="../../media/tools/deep-research/deep-research-tool-step-4.png":::

## Transparency, safety, and compliance

The output is a structured report that documents not only the comprehensive answer, but also provides source citations and describes the model's reasoning path, including any clarifications requested during the session. This makes every answer fully auditable. See the [Transparency note for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/transparency-note) for more information.

## Next steps

Learn [how to use the Deep Research tool](./deep-research-samples.md). 
