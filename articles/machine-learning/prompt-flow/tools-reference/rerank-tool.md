---
title: Rerank tool  in Azure Machine Learning prompt flow
titleSuffix: Azure Machine Learning
description: The prompt flow rerank tool enables you to rerank documents based on the relevancy to a given query. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: reference
ms.date: 08/29/2024
ms.reviewer: sooryar
ms.author: lagayhar
author: lgayhardt
ms.update-cycle: 365-days
---

# Rerank tool (preview)

The prompt flow Rerank tool improves search quality of relevant documents given a query for retrieval-augment generation (RAG) in prompt flow. This tool works best with [Index Look up tool](index-lookup-tool.md) as a ranker after the initial retrieval.

> [!IMPORTANT]
> Rerank tool is currently in public preview. This preview is provided without a service-level agreement, and is not recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Use the Rerank tool

1. Create or open a flow in Microsoft Foundry portal. For more information, see [Create a flow](../how-to-develop-flow.md#create-and-develop-your-prompt-flow).
1. Select **+More tools** > **Rerank tool** to add the Rerank tool to your flow.

     :::image type="content" source="../media/rerank-tool/rerank-tool.png" alt-text="Screenshot that shows the rerank tool added to a flow in Azure Machine Learning" lightbox="../media/rerank-tool/rerank-tool.png":::

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
