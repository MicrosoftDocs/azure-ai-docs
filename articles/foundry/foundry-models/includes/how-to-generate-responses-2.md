---
title: Include file
description: Include file
author: msakande
ms.reviewer: achand
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Troubleshoot common errors

| Error | Cause | Resolution |
| --- | --- | --- |
| 401 Unauthorized | Invalid or expired credential | Verify your `DefaultAzureCredential` has the **Cognitive Services OpenAI User** role assigned on the resource. |
| 404 Not Found | Wrong endpoint or deployment name | Confirm your endpoint URL includes `/api/projects/YOUR_PROJECT_NAME` and the deployment name matches your Foundry portal. |
| 400 Model not supported | Model doesn't support Responses API | Check the [supported models list](#supported-foundry-models) and verify your deployment uses a compatible model. |

## Related content

- [Migrate from Azure AI Inference SDK to OpenAI SDK](../../how-to/model-inference-to-openai-migration.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Model support for v1 Azure OpenAI API](../../openai/api-version-lifecycle.md#model-support)
