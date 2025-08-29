---
title: GPT-4 Turbo general availability
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Information on GPT-4 Turbo model behavior and limitations
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 04/29/2024
---

The latest GA release of GPT-4 Turbo is:

- `gpt-4` **Version:** `turbo-2024-04-09`

This is the replacement for the following preview models:

- `gpt-4` **Version:** `1106-Preview`
- `gpt-4` **Version:** `0125-Preview`
- `gpt-4` **Version:** `vision-preview`

### Differences between OpenAI and Azure OpenAI GPT-4 Turbo GA Models

- OpenAI's version of the latest `0409` turbo model supports JSON mode and function calling for all inference requests.
- Azure OpenAI's version of the latest `turbo-2024-04-09` currently doesn't support the use of JSON mode and function calling when making inference requests with image (vision) input. Text based input requests (requests without `image_url` and inline images) do support JSON mode and function calling.

### Differences from gpt-4 vision-preview

- Azure AI specific Vision enhancements integration with GPT-4 Turbo with Vision isn't supported for `gpt-4` **Version:** `turbo-2024-04-09`. This includes Optical Character Recognition (OCR), object grounding, video prompts, and improved handling of your data with images.

> [!IMPORTANT]
> Vision enhancements preview features including Optical Character Recognition (OCR), object grounding, video prompts will be retired and no longer available once `gpt-4` Version: `vision-preview` is upgraded to `turbo-2024-04-09`. If you are currently relying on any of these preview features, this automatic model upgrade will be a breaking change.

### GPT-4 Turbo provisioned managed availability

- `gpt-4` **Version:** `turbo-2024-04-09` is available for both standard and provisioned deployments. Currently the provisioned version of this model **doesn't support image/vision inference requests**. Provisioned deployments of this model only accept text input. Standard model deployments accept both text and image/vision inference requests.

### Deploying GPT-4 Turbo with Vision GA

To deploy the GA model from the Azure AI Foundry portal, select `GPT-4` and then choose the `turbo-2024-04-09` version from the dropdown menu. The default quota for the `gpt-4-turbo-2024-04-09` model will be the same as current quota for GPT-4-Turbo. See the [regional quota limits.](../quotas-limits.md)
