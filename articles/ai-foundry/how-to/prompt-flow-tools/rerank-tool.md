---
title: Rerank tool for flows in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces you to the Rerank tool for flows in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: reference
ms.date: 01/29/2025
ms.reviewer: jingyizhu
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---


# Rerank tool for flows in Azure AI Foundry portal

The prompt flow Rerank tool improves search quality of relevant documents given a query for retrieval-augment generation (RAG) in prompt flow. This tool works best with [Index Look up tool](index-lookup-tool.md) as a ranker after the initial retrieval.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Use the Rerank tool

1. Create or open a flow in Azure AI Foundry portal. For more information, see [Create a flow](../flow-develop.md).
1. Select **+More tools** > **Rerank tool** to add the Rerank tool to your flow.

     :::image type="content" source="../../media/prompt-flow/rerank-tool.png" alt-text="Screenshot that shows the rerank tool added to a flow in Azure AI Foundry portal." lightbox="../../media/prompt-flow/rerank-tool.png":::

1. Enter values for the Rerank tool input parameters.
1. Add more tools to your flow as needed, or select **Run** to run the flow.
1. To learn more about the returned output, see [outputs](#outputs).

## Inputs

The following are available input parameters:

| Name                | Type    | Description                                                     |
|---------------------|---------|-----------------------------------------------------------------|
| `queries`           | string  | The question relevant to your input documents.                  |
| `ranker_parameters` | string  | The type of ranking methods to use.                             |
| `result_groups`     | object  | The list of document chunks to rerank.                          |
| `top_k`             | integer | The count of top-scored entities to return. Default value is 3. |


## Outputs

The following JSON format response is an example returned by the tool that includes the relevancy score returned by the type of ranking method you chose.

| Field Name          | Description                      |
|---------------------|----------------------------------|
| `text`              | Content of the document chunk.   |
| `Metadata`          | Metadata like file path and url. |
| `additional_fields` | Metadata and rerank score.       |

```json

 [ 
    { 
        "text": "sample text", 
        "metadata": 

        { 
            "filepath": "sample_file_path", 
            "metadata_json_string": "meta_json_string" 
            "title": "", 
            "url": "" 
        }, 

        "additional_fields": 

        { 
            "filepath": "sample_file_path", 
            "metadata_json_string": "meta_json_string" 
            "title": "", 
            "url": "", 
            "@promptflow_vectordb.reranker_score": 0.013795365 
        } 
    } 
  ] 

```
