---
title: Migrate from Azure AI Inference SDK to OpenAI v1 SDK
titleSuffix: Azure AI Foundry
description: Learn about migrating from the Azure AI Inference SDK to OpenAI v1 SDK for Azure AI Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 10/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: 
ms.custom: migration
zone_pivot_groups: openai-supported-languages
ai-usage: ai-assisted
---

# Migrate from Azure AI Inference SDK to OpenAI v1 SDK

This article provides guidance on migrating your applications from the Azure AI Inference SDK to the OpenAI v1 SDK. The OpenAI v1 SDK offers broader compatibility, access to the latest OpenAI features, and simplified code with unified patterns across Azure OpenAI and Foundry Models.

::: zone pivot="programming-language-python"

[!INCLUDE [Python](../includes/model-inference-migration/python.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [C#](../includes/model-inference-migration/csharp.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript](../includes/model-inference-migration/javascript.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java](../includes/model-inference-migration/java.md)]

::: zone-end

::: zone pivot="programming-language-go"

[!INCLUDE [Go](../includes/model-inference-migration/go.md)]

::: zone-end

## Related content

- [How to generate chat completions with Azure AI Foundry Models](../foundry-models/how-to/use-chat-completions.md)
- [Azure OpenAI supported programming languages](../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [API evolution and version lifecycle](../openai/api-version-lifecycle.md)
