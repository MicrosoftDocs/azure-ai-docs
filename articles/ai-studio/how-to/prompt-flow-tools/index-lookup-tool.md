---
title: Index Lookup tool for flows in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces you to the Index Lookup tool for flows in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 5/21/2024
ms.reviewer: estraight
ms.author: lagayhar
author: lgayhardt
---

# Index Lookup tool for Azure AI Foundry

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The prompt flow Index Lookup tool enables the use of common vector indices (such as Azure AI Search, Faiss, and Pinecone) for retrieval augmented generation in prompt flow. The tool automatically detects the indices in the workspace and allows the selection of the index to be used in the flow.

## Build with the Index Lookup tool

1. Create or open a flow in [Azure AI Foundry](https://ai.azure.com). For more information, see [Create a flow](../flow-develop.md).
1. Select **+ More tools** > **Index Lookup** to add the Index Lookup tool to your flow.

    :::image type="content" source="../../media/prompt-flow/configure-index-lookup-tool.png" alt-text="Screenshot that shows the Index Lookup tool added to a flow in Azure AI Foundry portal." lightbox="../../media/prompt-flow/configure-index-lookup-tool.png":::

1. Enter values for the Index Lookup tool [input parameters](#inputs). The large language model [(LLM) tool](llm-tool.md) can generate the vector input.
1. Add more tools to your flow, as needed. Or select **Run** to run the flow.
1. To learn more about the returned output, see the [Outputs table](#outputs).

## Inputs

The following input parameters are available.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| mlindex_content | string | The type of index to be used. Input depends on the index type. An example of an Azure AI Search index JSON can be seen underneath the table. | Yes |
| queries | string, `Union[string, List[String]]` | The text to be queried.| Yes |
|query_type | string | The type of query to be performed. Options include Keyword, Semantic, Hybrid, and others.  | Yes |
| top_k | integer | The count of top-scored entities to return. Default value is 3. | No |

Here's an example of an Azure AI Search index input:

```json
embeddings:
  api_base: <api_base>
  api_type: azure
  api_version: 2023-07-01-preview
  batch_size: '1'
  connection:
    id: /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.MachineLearningServices/workspaces/<workspace> /connections/<AOAI_connection>
  connection_type: workspace_connection
  deployment: <embedding_deployment>
  dimension: <embedding_model_dimension>
  kind: open_ai
  model: <embedding_model>
  schema_version: <version>
index:
  api_version: 2023-07-01-Preview
  connection:
    id: /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.MachineLearningServices/workspaces/<workspace> /connections/<cogsearch_connection>
  connection_type: workspace_connection
  endpoint: <cogsearch_endpoint>
  engine: azure-sdk
  field_mapping:
    content: id
    embedding: content_vector_open_ai
    metadata: id
  index: <index_name>
  kind: acs
  semantic_configuration_name: azureml-default
```

## Outputs

The following JSON format response is an example returned by the tool that includes the top-k scored entities. The entity follows a generic schema of vector search results provided by the `promptflow-vectordb` SDK. For the Vector Index Search, the following fields are populated:

| Field name | Type | Description |
| ---- | ---- | ----------- |
| metadata | dict | The customized key-value pairs provided by the user when creating the index. |
| page_content | string | The content of the vector chunk being used in the lookup. |
| score | float | Depends on the index type defined in the Vector Index. If the index type is Faiss, the score is L2 distance. If the index type is Azure AI Search, the score is cosine similarity. |

```json
[
  {
    "metadata":{
      "answers":{},
      "captions":{
        "highlights":"sample_highlight1",
        "text":"sample_text1"
      },
      "page_number":44,
      "source":{
        "filename":"sample_file1.pdf",
        "mtime":1686329994,
        "stats":{
          "chars":4385,
          "lines":41,
          "tiktokens":891
        },
        "url":"sample_url1.pdf"
      },
      "stats":{
        "chars":4385,"lines":41,"tiktokens":891
      }
    },
    "page_content":"vector chunk",
    "score":0.021349556744098663
  },

  {
    "metadata":{
      "answers":{},
      "captions":{
        "highlights":"sample_highlight2",
        "text":"sample_text2"
      },
      "page_number":44,
      "source":{
        "filename":"sample_file2.pdf",
        "mtime":1686329994,
        "stats":{
          "chars":4385,
          "lines":41,
          "tiktokens":891
        },
        "url":"sample_url2.pdf"
      },
      "stats":{
        "chars":4385,"lines":41,"tiktokens":891
      }
    },
    "page_content":"vector chunk",
    "score":0.021349556744098663
  },
    
]

```

## Related content

- [Learn more about how to create a flow](../flow-develop.md)
