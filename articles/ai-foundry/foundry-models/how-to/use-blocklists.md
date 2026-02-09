---
title: Use blocklists in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: Learn how to create custom blocklists in Microsoft Foundry portal as part of your content filtering configurations.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 12/30/2025
ms.author: pafarley
author: PatrickFarley
monikerRange: 'foundry-classic || foundry'
---

# Use blocklists with Foundry Models in Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

The configurable content filters are sufficient for most content moderation needs. However, you might need to create custom blocklists in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) as part of your content filtering configurations to filter terms specific to your use case. This article shows how to create custom blocklists as part of your content filters in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

## Prerequisites

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. For more information, see [Upgrade from GitHub Models to Foundry Models](./quickstart-github-models.md).
* A Foundry services resource. For more information, see [Create a Foundry Services resource](../../../ai-services/multi-service-resource.md?context=/azure/ai-services/model-inference/context/context).
* A Foundry project [connected to your Foundry services resource](./configure-project-connection.md).
* A model deployment. For more information, see [Add and configure models to Foundry services](./create-model-deployments.md).

    > [!NOTE]
    > Blocklist (preview) support is limited to Azure OpenAI models.

[!INCLUDE [use-blocklists](../../includes/use-blocklists.md)]

## Next step

* [Configure content filtering](./configure-content-filters.md)
