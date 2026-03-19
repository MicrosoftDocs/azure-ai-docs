---
title: include file
description: include file
author: scottpolly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include
---

In this quickstart, you transcribe speech to text using the [Azure OpenAI Whisper model](../../../ai-services/speech-service/whisper-overview.md). The Whisper model can transcribe human speech in numerous languages and translate other languages into English.

> [!TIP]
> This quickstart takes approximately 10-15 minutes to complete.

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](whisper-rest.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](whisper-python.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET SDK quickstart](whisper-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](whisper-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](whisper-typescript.md)]

::: zone-end

::: zone pivot="programming-language-powershell"

[!INCLUDE [PowerShell quickstart](whisper-powershell.md)]

::: zone-end

> [!NOTE]
> For information about other audio models that you can use with Azure OpenAI, see [Audio models](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio).

> [!TIP]
> The file size limit for the Whisper model is 25 MB. If you need to transcribe a file larger than 25 MB, you can use the Azure Speech in Foundry Tools [batch transcription](../../../ai-services/speech-service/batch-transcription-create.md#use-a-whisper-model) API.

## Troubleshooting

### Authentication errors

If you receive 401 Unauthorized errors, verify:
- Your API key is correctly set in environment variables
- Your Azure OpenAI resource is active
- Your account has the Cognitive Services Contributor role

### File format errors

The Whisper model supports mp3, mp4, mpeg, mpga, m4a, wav, and webm formats. Other formats return an error.

### File size limit

Audio files must be 25 MB or smaller. For larger files, use the [Azure Speech batch transcription API](../../../ai-services/speech-service/batch-transcription-create.md#use-a-whisper-model).

### Deployment not found

Verify your deployment name matches exactly what you created in Azure OpenAI Studio. Deployment names are case-sensitive.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* To learn how to convert audio data to text in batches, see [Create a batch transcription](../../../ai-services/speech-service/batch-transcription-create.md).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
