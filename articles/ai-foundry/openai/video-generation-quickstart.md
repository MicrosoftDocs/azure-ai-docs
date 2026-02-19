---
title: 'Quickstart: Generate video with Sora'
titleSuffix: Azure OpenAI
description: Learn how to get started generating video clips with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 01/29/2026
ms.custom: dev-focus
zone_pivot_groups: openai-video-generation
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Quickstart: Generate a video with Sora (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [Video generation introduction](./includes/video-generation-intro.md)]


::: zone pivot="rest-api"


[!INCLUDE [REST API quickstart](includes/video-generation-rest.md)]

::: zone-end

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Portal quickstart](includes/video-generation-studio.md)]

::: zone-end


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../ai-services/multi-service-resource.md?pivots=azportal)
- [Azure CLI](../../ai-services/multi-service-resource.md?pivots=azcli)

## Related content

* Learn more about Azure OpenAI [deployment types](../foundry-models/concepts/deployment-types.md).
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md).
