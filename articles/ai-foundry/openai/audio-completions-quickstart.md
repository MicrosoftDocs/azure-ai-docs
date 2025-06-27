---
title: Quickstart - Getting started with Azure OpenAI audio generation
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with audio generation using Azure OpenAI.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 5/23/2025
author: eric-urban
ms.author: eur
ms.custom: references_regions
zone_pivot_groups: audio-completions-quickstart
recommendations: false
---

# Quickstart: Get started using Azure OpenAI audio generation

::: zone pivot="ai-foundry-portal"

[!INCLUDE [AI Foundry](includes/audio-completions-ai-foundry.md)]

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

## Clean-up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Troubleshooting

> [!NOTE]
> When using `gpt-4o-audio-preview` for chat completions with the audio modality and `stream` is set to true the only supported audio format is pcm16.

## Related content

* Learn more about Azure OpenAI [deployment types](./how-to/deployment-types.md).
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md).
