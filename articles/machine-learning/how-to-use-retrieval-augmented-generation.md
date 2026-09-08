---
title: Get started with RAG using a prompt flow sample (preview)
titleSuffix: Azure Machine Learning
description: Set up a prompt flow using the samples gallery.
services: machine-learning
ms.author: scottpolly
author: s-polly
ms.reviewer: balapv
ms.service: azure-machine-learning
ms.subservice: core
ms.date: 08/31/2026
ms.topic: how-to
ms.custom: prompt
ms.collection: ce-skilling-ai-copilot 
ai-usage: ai-assisted
---

# Get started with RAG using a prompt flow sample

[!INCLUDE [prompt-flow-retirement](includes/prompt-flow-retirement.md)]

In this article, you learn how to use retrieval-augmented generation (RAG) by creating a prompt flow. [Prompt flow](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/harness-the-power-of-large-language-models-with-azure-machine-learning-prompt-fl/3828459) is the interactive editor in Azure Machine Learning for prompt engineering. To get started, create a prompt flow sample that uses RAG from the samples gallery, and use it to learn how Vector Index works in a prompt flow.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]


## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* An Azure Machine Learning workspace. If you don't have one, [create a workspace](quickstart-create-resources.md) before you begin.

* Access to Azure OpenAI in Microsoft Foundry Models.

* Prompt flow enabled in your Azure Machine Learning workspace.

> [!NOTE]
> To enable prompt flow, turn on **Build AI solutions with Prompt flow** in the **Manage preview features** pane of your Azure Machine Learning workspace.


## Create a prompt flow using the samples gallery

1. Select **Prompt flow** on the left menu.

2. Select **Create**.

3. In the **Explore gallery** menu, select **View Detail** on the _Q&A on Your Data_ sample.

:::image type="content" source="./media/how-to-use-retrieval-augmented-generation/view-detail.png" alt-text="Screenshot showing view details button on the prompt flow sample.":::

4. Read the instructions and select **Clone** to create a prompt flow in your workspace.

:::image type="content" source="./media/how-to-use-retrieval-augmented-generation/clone.png" alt-text="Screenshot showing instructions and clone button on the prompt flow sample.":::

5. The cloned prompt flow opens, which you can run in your workspace and explore.

:::image type="content" source="./media/how-to-use-retrieval-augmented-generation/flow.png" alt-text="Screenshot showing the prompt flow sample.":::


## Related content

[Use Azure Machine Learning pipelines with no code to construct RAG pipelines (preview)](how-to-use-pipelines-prompt-flow.md)

[How to create vector index in Azure Machine Learning prompt flow (preview)](how-to-create-vector-index.md)

[Use Vector Stores with Azure Machine Learning (preview)](concept-vector-stores.md)
