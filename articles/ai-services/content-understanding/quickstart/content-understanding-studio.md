---
title: Quickstart Try out Content Understanding Studio
titleSuffix: Foundry Tools
description: Try out the new features of the Content Understanding Studio
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/30/2025
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Quickstart: Try out Content Understanding Studio

[Content Understanding Studio](https://aka.ms/cu-studio) is designed to help you quickly try out prebuilt analyzers, build and test your custom analyzers, and improve analyzer performance over time quickly and easily. This quickstart guide will walk you through the basic steps to get started so you can begin exploring all of the ways Content Understanding can improve your data-heavy workflows.

## Prerequisites
To get started, make sure you have the following resources and permissions:
*	An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
*	A Microsoft Foundry resource created in a [supported region](../language-region-support.md#region-support).
* A Foundry Model deployment of GPT-4.1 completion model and a text-embedding-3-large embedding model in your Foundry resource. For directions on how to deploy models, see [Create model deployments in Foundry portal](/articles/ai-foundry/foundry-models/how-to/create-model-deployments.md?pivots=ai-foundry-portal).

## Explore Content Understanding Studio
If you are familiar with the Document Intelligence service, you may recognize the classic features of Document Intelligence, now coupled with the new features that Content Understanding brings to analyze data of all modalities. When you arrive in [Content Understanding Studio](https://aka.ms/cu-studio), you have the option to select between the classic Document Intelligence Studio, and the new features of Content Understanding, shown below. Select “Content Understanding” to get started.

## Try out Content Understanding prebuilt analyzers

Get started by trying out the prebuilt analyzers offered through the Content Understanding. Start by opening [Content Understanding Studio](https://aka.ms/cu-studio).

1.	**Browse prebuilt analyzers**: Select the option to view all prebuilt analyzers from the home page of [Content Understanding Studio](https://aka.ms/cu-studio).

2.	**Select a prebuilt to try**: Content Understanding offers an extensive list of prebuilt analyzers that support scenarios across all modalities. Select an option based on your data needs to explore what features it offers.
 
3.	**Test on sample data**: Explore how the analyzer performs on provided sample data.

:::image type="content" source="../media/quickstarts/cu-studio-tryout.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="../media/quickstarts/cu-studio-tryout.png" :::

4. **Try out-on your own data**: To try out Content Understanding on your data, you will need to select a deployment of both a chat completion model and an embeddings model. Learn more about bringing your own deployment in [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md). 

<!---[Include screenshot of deployment selection]--->

5.	**Need to make changes to the schema to best fit your scenario?** Content Understanding offers customization on all prebuilt analyzers. Learn more about customizing in [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).

6.	**Don’t see an analyzer that suits your needs?** Learn more about building custom analyzers from scratch using AI-assisted suggestions in [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).

7.	**Have data to classify?** Learn more about classification in [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md).


## Next Steps
Once you’ve completed these steps, you’re ready to dive deeper into the advanced features offered by Content Understanding Studio, including custom analyzer building & improvement, and creating custom classifiers.

1.	Build and improve a custom analyzer using [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md)
2.	Learn more about classification in [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md)

