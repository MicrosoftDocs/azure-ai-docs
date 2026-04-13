---
title: Include file
description: Include file
author: mrbullwinkle
ms.reviewer: sgilley
ms.author: mbullwin
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

JSON mode allows you to set the model's response format to return a valid JSON object as part of a chat completion. While generating valid JSON was possible previously, there could be issues with response consistency that would lead to invalid JSON objects being generated.

JSON mode guarantees valid JSON output, but it doesn't guarantee the output matches a specific schema. If you need schema guarantees, use Structured Outputs.

> [!NOTE]
> While JSON mode is still supported, when possible we recommend using [structured outputs](../how-to/structured-outputs.md). Like JSON mode structured outputs generate valid JSON, but with the added benefit that you can constrain the model to use a specific JSON schema.

>[!NOTE]
> Currently Structured outputs are not supported on [bring your own data](../../../foundry-classic/openai/concepts/use-your-data.md) scenario.

## JSON mode support

JSON mode is only currently supported with the following models:

### API support

Support for JSON mode was first added in API version [`2023-12-01-preview`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2023-12-01-preview/inference.json)
