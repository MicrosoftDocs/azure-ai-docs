---
title: Upload Foundry Tools custom translation model language pair datasets 
titleSuffix: Foundry Tools
description: How to upload Microsoft Foundry custom translation datasets
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to
---

# How to upload a Foundry Tools custom translation model datasets

Document types are associated with the language pair selected when you create a project.

1. Follow [Create a language pair](create-language-pair.md), then continue here. 

1. Select the language pair **Name** you want to manage.

   :::image type="content" source="../media/fine-tune-edit-language-pair-1.png" alt-text="Screenshot illustrating edit language pair fields.":::

1. Select **Manage data** and then select **Add data**. 

1. Select dataset type and select your data document format.

   :::image type="content" source="../media/fine-tune-upload-data.png" alt-text="Screenshot illustrating the upload data page.":::

    - For **Parallel documents**, fill in the `Document set name` and select **Upload file** to browse local director to select source and target Files.
    - For **Translation memory (TM)** or **ZIP with multiple sets**, select **Upload file** to browse local directory to select the file.

1. Select **Add**.


## Upload history

You can view history of all document uploads details like document type, upload status, etc.

1. The upload history tab shows history for the selected language pair.

1. This page shows the status of all of your past uploads. It displays
    uploads from most recent to least recent. Each upload shows name, status, type, and created on.

   :::image type="content" source="../media/fine-tune-upload-history.png" alt-text="Screenshot showing the upload history page.":::

## Next steps

> [!div class="nextstepaction"]
> [Learn how to train model](train-model.md)
