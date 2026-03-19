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

## Prerequisites

- An Azue OpenAI model deployed
- One of the following authentication methods:
	- Microsoft Entra ID (recommended).
	- An API key.

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

- If you get a `401` or `403` error, confirm you authenticated with the intended identity or key, and that it has access to the Azure OpenAI resource.
- If you get a `404` error, confirm the endpoint uses the `...openai.azure.com/openai/v1/` path and that you used a valid model deployment name.
- If requests fail unexpectedly, check for proxy and firewall restrictions, and retry with a smaller prompt to rule out payload-size issues.
