---
title: Deploy model - Custom Translation
titleSuffix: Azure AI services
description: This article explains how to deploy a Custom Translation model.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 01/28/2025
ms.author: lajanuar
ms.topic: how-to
---
# Deploy a Custom Translation model

Deploying your Custom Translation model makes it available for use with the Azure AI Translator API. A language pair might have one or many successfully trained models. You can only deploy one model per language pair; however, you can deploy  a model to one or multiple regions depending on your needs. For more information, see [Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/#pricing).

## Deploy your trained model

You can deploy one model per language pair to one or multiple regions.

1. Select the **Deploy model** from the menu on the left.

1. Select the model name under **Name** and check the button then select **Deploy model**.

   :::image type="content" source="../media/new-fine-tune-translation-deploy-model.png" alt-text="Screenshot illustrating the deploy-model function.":::

1. Check the desired regions. Later, you can add or remove regions by selecting **Update regions**.

1. Select **Deploy model**. The status should transition from _Updating_deployment_ to _Deployed_region_names_.

   :::image type="content" source="../media/new-fine-tune-translation-deployed.png" alt-text="Screenshot illustrating the deploy-model function.":::

## Replace a deployed model

To replace a deployed model, you can exchange the deployed model with a different model in the same region:

1. Select the model name under **Name** then select **Deploy model**.

   :::image type="content" source="../media/new-fine-tune-translation-swap-model1.png" alt-text="Screenshot illustrating the swap-model function.":::

1. Select **Swap model**.

The redeployment takes several minutes to complete. In the meantime, deployed model will continue to be available for use with the Translator API until this process is complete.

   :::image type="content" source="../media/new-fine-tune-translation-swap-model2.png" alt-text="Screenshot illustrating the swap-model function.":::

## Next steps

> [!div class="nextstepaction"]
> [Learn how to Translate using your deployed model](../azure-ai-foundry/how-to-custom-translation-translate-from-model.md)