---
title: Translate text with Foundry Tools custom translation model
titleSuffix: Foundry Tools
description: How to make translation requests using deployed Microsoft Foundry custom translation model
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to
---

# Translate text with a Foundry Tools custom translation model

After you deploy your custom translation model, you can access it with the Azure Translator API by using the **Category ID** parameter.

## How to translate

1. Use the **Category ID** when making a custom translation request via Microsoft Translator [Text API V3](../../../text-translation/reference/v3/translate.md?tabs=curl). 

1. To find the model **Category ID**, select **Train model** from the left menu then select the model name.

1. Select **Edit** and copy the  **Category ID**.

   :::image type="content" source="../media/fine-tune-translate-category-id.png" alt-text="Screenshot illustrating translate-model function.":::

   ```http

     curl.exe -X POST "https://<resource-name>.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&from=en&to=de&category=<category-id>" \
     -H "Ocp-Apim-Subscription-Key:<resource- key>" \
     -H "Ocp-Apim-Subscription-Region:<your-region>" \
     -H "Content-Type: application/json" -d "[{'Text':'Hello, what is your name?'}]"

   ```

   More information about the Translator Text API can be found on the [Translator API Reference](../../../text-translation/reference/v3/translate.md) page.

1. You can also use **Microsoft Foundry** > **AI Services** > **Language + Translator** > **Translation** > **Text translation**

   :::image type="content" source="../media/fine-tune-translate-foundry.png" alt-text="Screenshot illustrating the translate-model function.":::

> [!NOTE]
>
> Use Category ID for Custom translator model ID.

## Next steps

> [!div class="nextstepaction"]
> [Learn more about building and publishing custom translation models](../beginners-guide.md)
