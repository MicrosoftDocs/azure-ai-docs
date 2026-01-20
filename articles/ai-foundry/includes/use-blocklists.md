---
title: include file
description: include file
author: PatrickFarley
ms.reviewer: pafarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 12/30/2025
ms.custom: include
monikerRange: 'foundry-classic || foundry'

---

[!INCLUDE [version-banner](./version-banner.md)]

## Create a blocklist

::: moniker range="foundry-classic"

1. Go to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) and navigate to your project. Then select the **Guardrails + controls** page in the left navigation and select the **Blocklists** tab.

    :::image type="content" source="../media/content-safety/content-filter/select-blocklists.png" lightbox="../media/content-safety/content-filter/select-blocklists.png" alt-text="Screenshot of the Blocklists page tab.":::

1. Select **Create a blocklist**. Enter a name for your blocklist, add a description, and select an Azure OpenAI resource to connect it to. Then select **Create Blocklist**.

1. Select your new blocklist. On the blocklist's page, select **Add new term**.

1. Enter the term that you want to filter and select **Add term**. You can also use a regex. You can delete each term in your blocklist.

## Attach a blocklist to a content filter configuration

1. After you create the blocklist, return to the **Guardrails + controls** page and select the **Content filters** tab. Create a new content filter configuration. A wizard opens with several AI content safety components.

    :::image type="content" source="../media/content-safety/content-filter/create-content-filter.png" lightbox="../media/content-safety/content-filter/create-content-filter.png" alt-text="Screenshot of the Create content filter button.":::

1. On the **Input filter** and **Output filter** screens, turn on the **Blocklist** toggle. You can then select a blocklist from the list. 
    There are two types of blocklists: the custom blocklists you created, and prebuilt blocklists that Microsoft provides&mdash;in this case a Profanity blocklist (English).

1. Decide which of the available blocklists you want to include in your content filtering configuration. Review and finish the content filtering configuration by selecting **Next**. You can always go back and edit your configuration. When it's ready, select **Create content filter**. You can now apply the new configuration that includes your blocklists to a deployment.

::: moniker-end

::: moniker range="foundry"
Go to [Foundry](https://ai.azure.com/) and navigate to your project. Then select the **Guardrails + controls** page in the left navigation. Select the **Create a custom blocklist** link, and follow the instructions.

::: moniker-end