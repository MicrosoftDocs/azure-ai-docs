---
title: Include file
description: Include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD044 -->

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/) if you don't have one.
- An Azure OpenAI resource with a `gpt-5-mini` model deployment.
- Your Azure OpenAI resource endpoint, such as `https://YOUR-RESOURCE-NAME.openai.azure.com`.
- For Microsoft Entra ID authentication, an identity that has permission to run inference. For role options, see [Configure Microsoft Entra ID authentication](../../foundry-models/how-to/configure-entra-id.md).
- For API key authentication, an Azure OpenAI resource key. Microsoft Entra ID is recommended for production applications.
- A supported language runtime and package manager for the language you select.

The `model` value in every request is your Azure model deployment name. The examples use `gpt-5-mini`; replace it if your deployment has a different name.

::: zone pivot="programming-language-dotnet"

[!INCLUDE [C#](language-overview/dotnet.md)]

::: zone-end

::: zone pivot="programming-language-go"

[!INCLUDE [Go](language-overview/go.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java](language-overview/java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript](language-overview/javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python](language-overview/python.md)]

::: zone-end

## Troubleshooting

- For a `401` or `403` response, confirm that the intended identity or API key can access the Azure OpenAI resource.
- For a `404` response, confirm that the base URL ends in `/openai/v1/` and that `model` contains a valid deployment name.
- For a package or type error, update the SDK and compare the installed version with the version tested on this page.
- For a model parameter error, check whether the deployed model supports the parameter. Parameter support can differ between model families.

## Related content

- [The Azure OpenAI Starter Kit](https://aka.ms/openai/start)
- [Azure OpenAI To Responses](https://aka.ms/azure-openai-to-responses)
- [Use the Azure OpenAI Responses API](../how-to/responses.md)
- [Azure OpenAI v1 API](../api-version-lifecycle.md)
