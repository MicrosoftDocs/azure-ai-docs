---
title: Azure OpenAI in Microsoft Foundry Models supported programming languages
description: Programming language support for Azure OpenAI.
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
ms.topic: concept-article
ms.date: 11/26/2025
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
zone_pivot_groups: openai-supported-languages
---

# Azure OpenAI supported programming languages

[!INCLUDE [version-banner](../includes/version-banner.md)]

## Prerequisites

- An Azue OpenAI model deployed
- One of the following authentication methods:
	- Microsoft Entra ID (recommended).
	- An API key.

::: zone pivot="programming-language-dotnet"

[!INCLUDE [C#](./includes/language-overview/dotnet.md)]

::: zone-end

::: zone pivot="programming-language-go"

[!INCLUDE [Go](./includes/language-overview/go.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java](./includes/language-overview/java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript](./includes/language-overview/javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python](./includes/language-overview/python.md)]

::: zone-end

## Troubleshooting

- If you get a `401` or `403` error, confirm you authenticated with the intended identity or key, and that it has access to the Azure OpenAI resource.
- If you get a `404` error, confirm the endpoint uses the `...openai.azure.com/openai/v1/` path and that you used a valid model deployment name.
- If requests fail unexpectedly, check for proxy and firewall restrictions, and retry with a smaller prompt to rule out payload-size issues.


