---
title: Quickstart Try out Content Understanding Studio or Foundry portal
titleSuffix: Foundry Tools
description: Try out the new features of the Content Understanding Studio, or access the prebuilt analyzers through the Foundry portal.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 02/12/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
  - dev-focus
---

# Quickstart: Try out Content Understanding via web portal

[Content Understanding Studio](https://aka.ms/cu-studio) helps you try prebuilt analyzers, build and test custom analyzers, and improve analyzer performance over time. This quickstart walks you through the basic steps to get started.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A Microsoft Foundry resource, created in a [supported region](../language-region-support.md#region-support).
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

#### [Content Understanding Studio](#tab/cu-studio)

## Explore Content Understanding Studio

If you're familiar with Document Intelligence, you might recognize the classic features. Content Understanding Studio includes those features and adds multimodal analysis.

When you arrive in [Content Understanding Studio](https://aka.ms/cu-studio), select between the classic Document Intelligence Studio and the new Content Understanding experience. Select "Content Understanding" to get started.

## Try out prebuilt analyzers

Get started by trying out the prebuilt analyzers offered through Content Understanding. Start by opening [Content Understanding Studio](https://aka.ms/cu-studio).

1. **Browse prebuilt analyzers**: Select the option to view all prebuilt analyzers from the home page of [Content Understanding Studio](https://aka.ms/cu-studio).
1. **Select a prebuilt to try**: Content Understanding offers an extensive list of prebuilt analyzers that support scenarios across all modalities. Select an option based on your data needs to explore what features it offers.
1. **Test on sample data**: Explore how the analyzer performs on provided sample data.
    :::image type="content" source="../media/quickstarts/cu-studio-tryout.png" alt-text="Screenshot of Content Understanding Studio showing the prebuilt analyzer selection and results interface." lightbox="../media/quickstarts/cu-studio-tryout.png" :::
1. **Try out on your own data**: To try out Content Understanding on your data, you need to select a deployment of both a chat completion model and an embeddings model. Learn more in [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md).
1. **Verify the results**: After running the analyzer, review the output in the results pane. You should see extracted fields, key-value pairs, or other structured data depending on the analyzer you selected. If the output matches your expectations, you've successfully tested the prebuilt analyzer.

## Customize your analyzer (optional)

After you try the prebuilt analyzers, you can customize them to fit your specific needs:

- **Modify the schema**: Content Understanding supports customization for all prebuilt analyzers. See [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).
- **Build from scratch**: Create custom analyzers using AI-assisted suggestions. See [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).
- **Classify data**: Route documents to different processing paths. See [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md).

#### [Microsoft Foundry (new)](#tab/foundry-new)

With Microsoft Foundry (new), you can quickly test prebuilt analyzer models. You don't need to deploy any models yourself. Just select these options to explore their capabilities and see how they extract and organize information from your documents.

## Available analyzers

- **Read** (`prebuilt-read`) extracts text elements such as words, paragraphs, formulas, and barcodes. It provides OCR without layout analysis.
- **Layout** (`prebuilt-layout`) extracts text and layout elements such as words, figures, paragraphs, and tables. It also extracts document structure (sections and formatting), hyperlinks, and (for digital PDFs) annotations such as highlights, underlines, and strikethroughs.

These prebuilt analyzers don't require a language model or embedding model. For more information, see [Content extraction analyzers](../concepts/prebuilt-analyzers.md#content-extraction-analyzers).

## Try out prebuilt analyzers

1. Go to [!INCLUDE [foundry-link](../../../ai-foundry/default/includes/foundry-link.md)] and select your project or create a new one.
1. Select **Build** in the upper right menu, then select **Models** on the left pane. This lets you access your own deployed models and any prebuilt models provided by Foundry Tools.
1. Select the **AI Services** tab, and find 
**Azure Content Understanding - Read** or 
**Azure Content Understanding - Layout**. Selecting either one brings you to that model's respective playground page.
1. Run the analyzer on the sample data provided, or connect your own data to see how the model performs. Examine the results, either formatted or as raw JSON data.

---

## Related content

- [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md)
- [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md)
- [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md)

