---
title: Copy a Foundry Tools custom translation model to another project.
titleSuffix: Foundry Tools
description: This article explains how to copy a Microsoft Foundry custom translation model to another custom translation project.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to
---

# Copy a Foundry Tools custom translation model

Copying a Microsoft Foundry custom translation model to other project enables model lifecycle management (for example, development → test → production) and increases usage scalability while reducing the training cost.

## Copy custom translation model to another project

   > [!NOTE]
   >
   > To copy model from one project to another, you must be a user with an **Owner** role in both projects.
   >
   > The copied model can't be recopied. You can only rename, delete, or publish a copied model.

1. After successful model training, select the **Train model** from the left menu.

1. Select the model **Name** to copy.

1. Select **Copy to project**.

   :::image type="content" source="../media/fine-tune-copy-model-1.png" alt-text="Screenshot illustrating the copy-model dialog window.":::

1. Fill out the target details.

   :::image type="content" source="../media/fine-tune-copy-model-2.png" alt-text="Screenshot illustrating the copy model dialog window.":::

   > [!NOTE]
      >
      > A dropdown list displays the list of projects available to use. Otherwise, select **Create a new project**.
      >
      > If selected project contains a language pair for the same source to target, it can be selected from the language pairs dropdown list, otherwise, select **Create a new language pair** to create one.

1. Select **Copy model**. The process should complete fairly quickly.

1. A notification panel shows the copy progress. :

1. In the target project and language pair, After **Copy model** completion, a copied model is available in the target project > language pair and ready to publish. A **Copied model** watermark is appended to the model name.

   :::image type="content" source="../media/fine-tune-copy-model-3.png" alt-text="Screenshot illustrating the copy complete dialog window.":::

## Next steps

> [!div class="nextstepaction"]
> [Learn how to deploy a custom translation model](deploy-model.md).
