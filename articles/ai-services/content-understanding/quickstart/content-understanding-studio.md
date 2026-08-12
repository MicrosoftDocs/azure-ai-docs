---
title: "Quickstart: Try Content Understanding Studio or Microsoft Foundry"
titleSuffix: Foundry Tools
description: Use Content Understanding Studio to try analyzers and create custom analyzers, or use Microsoft Foundry to run its available analyzers.
author: PatrickFarley 
ms.author: pafarley
manager: mcleans
ms.date: 07/16/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: quickstart
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
  - dev-focus
---

# Quickstart: Try Content Understanding Studio or Microsoft Foundry

[Content Understanding Studio](https://contentunderstanding.ai.azure.com/) is the primary experience for trying prebuilt and search analyzers and creating custom analyzers. In this quickstart, use Studio or [Microsoft Foundry (new)](https://ai.azure.com/) to discover and run available analyzers.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A Microsoft Foundry resource, created in a [supported region](../language-region-support.md#region-support).

#### [Content Understanding Studio](#tab/cu-studio-prereq)

[!INCLUDE [Studio model deployment setup](../includes/foundry-model-deployment-setup-studio.md)]

#### [Microsoft Foundry (new)](#tab/foundry-new-prereq)

1. Go to [Microsoft Foundry](https://ai.azure.com/).

1. Navigate to the Content Understanding playground.

1. Select the gear icon to open the **Configure** panel. Select existing model deployments or deploy new models from the playground. Alternatively, go to the [model catalog](https://ai.azure.com/explore/models), deploy the [models supported by Content Understanding](../service-limits.md#supported-generative-models), and then return to the playground to select them.

#### [REST API](#tab/rest-api-prereq)

[!INCLUDE [REST model deployment setup](../includes/foundry-model-deployment-setup-rest.md)]

---

#### [Content Understanding Studio](#tab/cu-studio)

## Explore Content Understanding Studio

Open [Content Understanding Studio](https://contentunderstanding.ai.azure.com/) and sign in with your Azure account.

## Try out prebuilt analyzers

Get started by trying a prebuilt analyzer in Content Understanding Studio.

1. **Browse prebuilt analyzers**: Select the option to view all prebuilt analyzers from the Studio home page.
1. **Select a prebuilt analyzer**: Select an analyzer based on your data type and scenario.
1. **Test on sample data**: Explore how the analyzer performs on provided sample data.
    :::image type="content" source="../media/quickstarts/cu-studio-tryout.png" alt-text="Screenshot of Content Understanding Studio showing the prebuilt analyzer selection and results interface." lightbox="../media/quickstarts/cu-studio-tryout.png" :::
1. **Try out on your own data**: To try out Content Understanding on your data, you need to select a deployment of both a chat completion model and an embeddings model. Learn more in [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md).
1. **Verify the results**: After running the analyzer, review the output in the results pane. You should see extracted fields, key-value pairs, or other structured data depending on the analyzer you selected. If the output matches your expectations, you've successfully tested the prebuilt analyzer.

## Create a custom analyzer (optional)

After you try a prebuilt analyzer, you can create an analyzer for your specific needs:

- **Create a custom analyzer**: Define a schema with the fields you want to extract. See [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md).
- **Classify data**: Route documents to different processing paths. See [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md).

#### [Microsoft Foundry (new)](#tab/foundry-new)


## Available analyzers

Foundry supports the Read and Layout content extraction analyzers and a subset of prebuilt analyzers. The analyzer dropdown shows the analyzers currently available in Foundry. For a full comparison, see [Content Understanding Studio and Microsoft Foundry](../foundry-vs-content-understanding-studio.md).

## Try an analyzer

1. Go to [Microsoft Foundry](https://ai.azure.com/) and select your project or create a new one.
1. Select **Build** in the upper right menu, then select **Models** on the left pane. This lets you access your own deployed models and any prebuilt models provided by Foundry Tools.
1. Select the **AI Services** tab, and then select the **Content Understanding Playground**.
1. Run the analyzer on the sample data provided, or upload your own content to see how the model performs. Examine the results, either formatted or as raw JSON data.
    :::image type="content" source="../media/quickstarts/foundry-playground.png" alt-text="Screenshot of the Content Understanding playground in Microsoft Foundry showing a document and Layout analyzer results." lightbox="../media/quickstarts/foundry-playground.png" :::

---

## Related content

- [Content Understanding Studio and Microsoft Foundry](../foundry-vs-content-understanding-studio.md)
- [How to build a custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md)
- [How to classify and route with custom categories in Content Understanding Studio](../how-to/classification-content-understanding-studio.md)
- [Connect your Content Understanding analyzer to Foundry model deployments](../concepts/models-deployments.md)
