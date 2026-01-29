---
title: Quickstart Try out Content Understanding Studio
titleSuffix: Foundry Tools
description: Try out the new features of the Content Understanding Studio
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Quickstart: Try out Content Understanding Studio

[Content Understanding Studio](https://aka.ms/cu-studio) helps you try prebuilt analyzers, build and test custom analyzers, and improve analyzer performance over time. This quickstart walks you through the basic steps to get started.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A Microsoft Foundry resource created in a [supported region](../language-region-support.md#region-support).
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Explore Content Understanding Studio

If you're familiar with Document Intelligence, you might recognize the classic features. Content Understanding Studio includes those features and adds multimodal analysis.

When you arrive in [Content Understanding Studio](https://aka.ms/cu-studio), select between the classic Document Intelligence Studio and the new Content Understanding experience. Select "Content Understanding" to get started.

## Try out Content Understanding prebuilt analyzers

Get started by trying out the prebuilt analyzers offered through the Content Understanding. Start by opening [Content Understanding Studio](https://aka.ms/cu-studio).

1.	**Browse prebuilt analyzers**: Select the option to view all prebuilt analyzers from the home page of [Content Understanding Studio](https://aka.ms/cu-studio).

2.	**Select a prebuilt to try**: Content Understanding offers an extensive list of prebuilt analyzers that support scenarios across all modalities. Select an option based on your data needs to explore what features it offers.
 
3.	**Test on sample data**: Explore how the analyzer performs on provided sample data.

:::image type="content" source="../media/quickstarts/cu-studio-tryout.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="../media/quickstarts/cu-studio-tryout.png" :::

4. **Try out on your own data**: To try out Content Understanding on your data, you need to select a deployment of both a chat completion model and an embeddings model. Learn more in [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md).

<!---[Include screenshot of deployment selection]--->

5.	**Need to make changes to the schema to fit your scenario?** Content Understanding supports customization for all prebuilt analyzers. Learn more in [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).

6.	**Don't see an analyzer that suits your needs?** Learn more about building custom analyzers from scratch using AI-assisted suggestions in [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).

7.	**Have data to classify?** Learn more about classification in [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md).


## Next steps

After you complete these steps, you're ready to explore more features in Content Understanding Studio, including custom analyzer improvement and custom classifiers.

1.	Build and improve a custom analyzer using [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).
2.	Learn more about classification in [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md).

