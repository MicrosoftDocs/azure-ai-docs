---
title: How to migrate from Azure AI Inference SDK to OpenAI SDK
titleSuffix: Microsoft Foundry
description: Learn how to migrate to OpenAI SDK from Azure AI Inference SDK for enhanced compatibility and unified APIs when working with Microsoft Foundry Models.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 11/05/2025
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom: migration
zone_pivot_groups: openai-supported-languages
ai-usage: ai-assisted
#CustomerIntent: As a developer using Azure AI Inference SDK, I want to migrate my applications to the OpenAI SDK so that I can access broader model support, unified APIs, the latest OpenAI features, simplified authentication, and eliminate the need to frequently update API version parameters.
---

# Migrate from Azure AI Inference SDK to OpenAI SDK

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

This article provides guidance on migrating your applications from the Azure AI Inference SDK to the OpenAI SDK. The OpenAI SDK offers broader compatibility, access to the latest OpenAI features, and simplified code with unified patterns across Azure OpenAI and Foundry Models.

> [!NOTE]
> The OpenAI SDK refers to the client libraries (such as the Python `openai` package or JavaScript `openai` npm package) that connect to [OpenAI v1 API endpoints](../openai/api-version-lifecycle.md#api-evolution). These SDKs have their own versioning separate from the API version - for example, the Go OpenAI SDK is currently at v3, but it still connects to the OpenAI v1 API endpoints with `/openai/v1/` in the URL path.

## Benefits of migrating

Migrating to the OpenAI SDK provides several advantages:

- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok
- **Unified API**: Uses the same SDK libraries and clients for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **Implicit API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters

## Key differences

The following table shows the main differences between the two SDKs:

| Aspect | Azure AI Inference SDK | OpenAI SDK |
|--------|------------------------|-------------|
| Client class | `ChatCompletionsClient` | `OpenAI` |
| Endpoint format | `https://<resource>.services.ai.azure.com/models` | `https://<resource>.openai.azure.com/openai/v1/` |
| API version | Required in URL or parameter | Not required (uses v1 API) |
| Model parameter | Optional (for multi-model endpoints) | Required (deployment name) |
| Authentication | Azure credentials only | API key or Azure credentials |


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


## Common migration patterns

### Model parameter handling

- **Azure AI Inference SDK**: The `model` parameter is optional for single-model endpoints but required for multimodel endpoints.
- **OpenAI SDK**: The `model` parameter is always required and should be set to your deployment name.

### Endpoint URL format

- **Azure AI Inference SDK**: Uses `https://<resource>.services.ai.azure.com/models`.
- **OpenAI SDK**: Uses `https://<resource>.openai.azure.com/openai/v1` (connects to the OpenAI v1 API).

### Response structure

The response structure is similar but has some differences:

- **Azure AI Inference SDK**: Returns `ChatCompletions` object with `choices[].message.content`.
- **OpenAI SDK**: Returns `ChatCompletion` object with `choices[].message.content`.

Both SDKs provide similar access patterns to response data, including:
- Message content
- Token usage
- Model information
- Finish reason

## Migration checklist

Use this checklist to ensure a smooth migration:

> [!div class="checklist"]
> * Install the OpenAI SDK for your programming language
> * Update authentication code (API key or Microsoft Entra ID)
> * Change endpoint URLs from `.services.ai.azure.com/models` to `.openai.azure.com/openai/v1/`
> * Update client initialization code
> * Always specify the `model` parameter with your deployment name
> * Update request method calls (`complete` → `chat.completions.create`)
> * Update streaming code if applicable
> * Update error handling to use OpenAI SDK exceptions
> * Test all functionality thoroughly
> * Update documentation and code comments

## Troubleshooting

### Authentication failures

If you experience authentication failures:

- Verify your API key is correct and isn't expired
- For Microsoft Entra ID, ensure your application has the correct permissions
- Check that the credential scope is set to `https://cognitiveservices.azure.com/.default`

### Endpoint errors

If you receive endpoint errors:

- Verify the endpoint URL format includes `/openai/v1/` at the end.
- Ensure your resource name is correct.
- Check that the model deployment exists and is active.

### Model not found errors

If you receive "model not found" errors:

- Verify you're using your deployment name, not the model name.
- Check that the deployment is active in your Microsoft Foundry resource.
- Ensure the deployment name matches exactly (case-sensitive).

## Related content

- [Azure OpenAI supported programming languages](../openai/supported-languages.md)
- [How to generate chat completions with Foundry Models](../openai/api-version-lifecycle.md)
- [API evolution and version lifecycle](../openai/api-version-lifecycle.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)

