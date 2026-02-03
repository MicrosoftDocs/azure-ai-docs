---
title: Quickstart - Get started with Azure OpenAI audio generation
titleSuffix: Azure OpenAI
description: Get started with audio generation using Azure OpenAI.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/30/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions
zone_pivot_groups: audio-completions-quickstart
recommendations: false
monikerRange: 'foundry-classic || foundry'

---

# Quickstart: Get started with Azure OpenAI audio generation

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Foundry](includes/audio-completions-foundry.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/audio-completions-javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/audio-completions-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/audio-completions-rest.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](includes/audio-completions-typescript.md)]

::: zone-end

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Troubleshooting

> [!NOTE]
> When using `gpt-4o-audio-preview` for chat completions with the audio modality and `stream` is set to true the only supported audio format is pcm16.

## Related content

* Learn more about Azure OpenAI [deployment types](../foundry-models/concepts/deployment-types.md).
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md).
