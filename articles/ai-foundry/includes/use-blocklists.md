---
title: include file
description: include file
author: PatrickFarley
ms.reviewer: pafarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/01/2025
ms.custom: include
---


## Create a blocklist

1. Go to [Azure AI Foundry](https://ai.azure.com/) and navigate to your project. Then select the **Guardrails + controls** page on the left nav and select the **Blocklists** tab.

    :::image type="content" source="../media/content-safety/content-filter/select-blocklists.png" lightbox="../media/content-safety/content-filter/select-blocklists.png" alt-text="Screenshot of the Blocklists page tab.":::

1. Select **Create a blocklist**. Enter a name for your blocklist, add a description, and select an Azure OpenAI resource to connect it to. Then select **Create Blocklist**.

1. Select your new blocklist once it's created. On the blocklist's page, select **Add new term**.

1. Enter the term that should be filtered and select **Add term**. You can also use a regex. You can delete each term in your blocklist.

## Attach a blocklist to a content filter configuration

1. Once the blocklist is ready, go back to the **Guardrails + controls** page and select the **Content filters** tab. Create a new content filter configuration. This opens a wizard with several AI content safety components.

    :::image type="content" source="../media/content-safety/content-filter/create-content-filter.png" lightbox="../media/content-safety/content-filter/create-content-filter.png" alt-text="Screenshot of the Create content filter button.":::

1. On the **Input filter** and **Output filter** screens, toggle the **Blocklist** button on. You can then select a blocklist from the list. 
    There are two types of blocklists: the custom blocklists you created, and prebuilt blocklists that Microsoft provides&mdash;in this case a Profanity blocklist (English).

1. You can now decide which of the available blocklists you want to include in your content filtering configuration. The last step is to review and finish the content filtering configuration by selecting **Next**. You can always go back and edit your configuration. Once it’s ready, select a **Create content filter**. The new configuration that includes your blocklists can now be applied to a deployment.
