---
title: Publish an Azure AI Custom Translator model
titleSuffix: Azure AI services
description: This article explains how to publish an Azure AI Custom Translator model.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 01/28/2025
ms.author: lajanuar
ms.topic: how-to
---
# Publish an Azure AI Custom Translator model

Publishing your Custom Translator model makes it available for use with the Azure AI Translator API. A project might have one or many successfully trained models. You can only publish one model per project; however, you can publish  a model to one or multiple regions depending on your needs. For more information, see [Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/#pricing).

## Publish your trained model

You can publish one model per project to one or multiple regions.

1. Select the `Publish model` blade.

1. Select *en-de with sample data* and select `Publish`.

1. Check the desired regions.

1. Select `Publish`. The status should transition from _Deploying_ to _Deployed_.

   :::image type="content" source="../media/quickstart/publish-model.png" alt-text="Screenshot illustrating the publish-model blade.":::

## Replace a published model

To replace a published model, you can exchange the published model with a different model in the same region:

1. Select the replacement model.

1. Select `Publish`.

1. Select `publish` once more in the `Publish model` dialog window.

## Next steps

> [!div class="nextstepaction"]
> [Learn how to translate with Azure AI Custom Translator models](../quickstart.md)
