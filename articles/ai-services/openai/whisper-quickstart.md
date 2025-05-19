---
title: Convert speech to text with Azure OpenAI in Azure AI Foundry Models
titleSuffix: Azure OpenAI
description: Learn how to use the Azure OpenAI Whisper model for speech to text conversion.
manager: nitinme
ms.service: azure-ai-openai
ms.custom: devx-track-python
ms.topic: quickstart
ms.date: 3/10/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
recommendations: false
zone_pivot_groups: programming-languages-rest-ps-py-js-cs
---

# Quickstart: Speech to text with the Azure OpenAI Whisper model

This quickstart explains how to use the [Azure OpenAI Whisper model](../speech-service/whisper-overview.md) for speech to text conversion. The Whisper model can transcribe human speech in numerous languages, and it can also translate other languages into English.

> [!NOTE]
> For information about other audio models that you can use with Azure OpenAI, see [Audio models](./concepts/models.md?tabs=standard-audio#standard-deployment-regional-models-by-endpoint).

The file size limit for the Whisper model is 25 MB. If you need to transcribe a file larger than 25 MB, you can use the Azure AI Speech [batch transcription](../speech-service/batch-transcription-create.md#use-a-whisper-model) API.

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/whisper-rest.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/whisper-python.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET SDK quickstart](includes/whisper-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/whisper-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [JavaScript quickstart](includes/whisper-typescript.md)]

::: zone-end

::: zone pivot="programming-language-powershell"

[!INCLUDE [PowerShell quickstart](includes/whisper-powershell.md)]

::: zone-end

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* To learn how to convert audio data to text in batches, see [Create a batch transcription](../speech-service/batch-transcription-create.md).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
