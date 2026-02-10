---
title: Embedding tool for flows in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: This article introduces you to the Embedding tool for flows in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
  - hub-only
ms.topic: article
ms.date: 01/27/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Embedding tool for flows in Microsoft Foundry portal

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The prompt flow Embedding tool converts text into dense vector representations for various natural language processing tasks.

> [!TIP]
> For chat and completion tools, see the large language model [(LLM) tool](llm-tool.md).

## Prerequisites

[!INCLUDE [hub-only-prereq](../../includes/hub-only-prereq.md)]

## Build with the Embedding tool

1. Create or open a flow in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). For more information, see [Create a flow](../flow-develop.md).
1. Select **+ More tools** > **Embedding** to add the Embedding tool to your flow.

    :::image type="content" source="../../media/prompt-flow/embedding-tool.png" alt-text="Screenshot that shows the Embedding tool added to a flow in Foundry portal." lightbox="../../media/prompt-flow/embedding-tool.png":::

1. Select the connection to one of your provisioned resources. For example, select **Default_AzureOpenAI**.
1. Enter values for the Embedding tool input parameters described in the [Inputs table](#inputs).
1. Add more tools to your flow, as needed. Or select **Run** to run the flow.
1. The outputs are described in the [Outputs table](#outputs).

## Inputs

The following input parameters are available.

| Name                   | Type        | Description                                                                             | Required |
|------------------------|-------------|-----------------------------------------------------------------------------------------|----------|
| input                  | string      | The input text to embed.                                                                 | Yes      |
| model, deployment_name | string      | The instance of the text-embedding engine to use.                                            | Yes      |

## Outputs

The output is a list of vector representations for the input text. For example:

```
[
  0.123,
  0.456,
  0.789
]
```

## Next steps

- [Learn more about how to create a flow](../flow-develop.md)
