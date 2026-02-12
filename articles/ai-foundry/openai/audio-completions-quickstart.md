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

### Authentication errors

If you receive a 401 or 403 error:
- **Keyless auth:** Verify you've run `az login` and have the `Cognitive Services User` role assigned to your account.
- **API key:** Check that `AZURE_OPENAI_API_KEY` is set correctly and the key hasn't been regenerated.

### Model not found

If the `gpt-4o-mini-audio-preview` model isn't available:
- Verify the model is deployed in your Azure OpenAI resource.
- Check that you're using a [supported region](../foundry-models/concepts/models-sold-directly-by-azure.md).

### Audio file issues

If the generated audio file doesn't play:
- Ensure the file was written completely (check file size is greater than 0 bytes).
- Verify the format matches what your player supports (wav is widely compatible).
- For streaming responses, remember that only pcm16 format is supported.

### Rate limiting

If you receive a 429 error, you've exceeded the rate limit. Wait and retry, or request a quota increase. For more information about rate limits, see [Azure OpenAI quotas and limits](quotas-limits.md).

## Related content

* Learn more about Azure OpenAI [deployment types](../foundry-models/concepts/deployment-types.md).
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md).
