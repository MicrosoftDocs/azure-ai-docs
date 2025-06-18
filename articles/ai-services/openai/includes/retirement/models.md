---
title: Model retirement table 
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Model retirement table for  Azure OpenAI in Azure AI Foundry Models
manager: nitinme
ms.date: 06/18/2025
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions, build-2025
---


# [Text generation](#tab/text)

### Text generation

| Model                     | Version         | Retirement date                    | Replacement model                    |
| --------------------------|-----------------|------------------------------------|--------------------------------------|
| `gpt-4.5-preview`         | 2025-02-27      | No Auto-upgrades <br>July 14, 2025 | `gpt-4.1` version: `2025-04-14`      |
| `gpt-3.5-turbo-instruct`  | 0914            | No earlier than July 16, 2025      |                                      |
| `o1-preview`              | 2024-09-12      | No earlier than July 28, 2025      | `o1`                                 |
| `computer-use-preview`    | 2025-03-11      | No earlier than September 1, 2025  |                                      |
| `gpt-35-turbo`            | 1106            | No earlier than September 1, 2025  | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-35-turbo`            | 0125            | No earlier than September 1, 2025  | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-4`                   | turbo-2024-04-09| No earlier than September 1, 2025  | `gpt-4o` version: `2024-11-20`       |
| `model router`            | 2025-05-19      | No earlier than September 1, 2025  |                                      |
| `gpt-4o`                  | 2024-05-13      | No earlier than September 15, 2025 | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4o-mini`             | 2024-07-18      | No earlier than September 15, 2025 | `gpt-4.1-mini` version: `2025-04-14` |
| `o1-mini`                 | 2024-09-12      | No earlier than September 26, 2025 |                                      |
| `gpt-4o`                  | 2024-08-06      | No earlier than October 15, 2025   | `gpt-4.1` version: `2025-04-14`      |
| `o1`                      | 2024-12-17      | No earlier than December 17, 2025  |                                      |
| `o3-mini`                 | 2025-01-31      | No earlier than February 1, 2026   |                                      |
| `gpt-4o`                  | 2024-11-20      | No earlier than March 1, 2026      | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4.1`                 | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `gpt-4.1-mini`            | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `gpt-4.1-nano`            | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `o4-mini`                 | 2025-04-16      | No earlier than April 11, 2026     |                                      |
| `o3`                      | 2025-04-16      | No earlier than April 11, 2026     |                                      |

# [Audio](#tab/audio)

### Audio

| Model                          | Version         | Retirement date                    | Replacement model                    |
| -------------------------------|-----------------|------------------------------------|--------------------------------------|
| `gpt-4o-mini-realtime-preview` | 2024-12-17      | No earlier than July 2, 2025       |                                      |
| `gpt-4o-realtime-preview`      | 2024-12-17      | No earlier than July 2, 2025       |                                      |
| `gpt-4o-audio-preview`         | 2024-12-17      | No earlier than July 2, 2025       |                                      |
| `gpt-4o-audio-preview`         | 2024-12-17      | No earlier than July 2, 2025       |                                      |
| `gpt-4o-transcribe`            | 2025-03-20      | No earlier than August 11, 2025    |                                      |
| `gpt-4o-mini-tts`              | 2025-03-20      | No earlier than August 11, 2025    |                                      |
| `gpt-4o-mini-transcribe`       | 2025-03-20      | No earlier than August 11, 2025    |                                      |
| `tts`                          | 001             | No earlier than February 1, 2026   |                                      |

# [Image & Video](#tab/image)

### Image & video

| Model                          | Version         | Retirement date                    | Replacement model                    |
| -------------------------------|-----------------|------------------------------------|--------------------------------------|
| `dalle-3`                      | 3               | No earlier than September 15, 2025 |                                      |
| `gpt-image-1`                  | 2025-04-15      | No earlier than August 1, 2025     |                                      |

# [Embedding](#tab/embedding)

### Embedding

| Model                          | Version         | Retirement date                    | Replacement model                                    |
| -------------------------------|-----------------|------------------------------------|------------------------------------------------------|
| `text-embedding-ada-002`       | 2               | No earlier than April 30, 2026     | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-ada-002`       | 1               | No earlier than April 30, 2026     | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-3-small`       |                 | No earlier than April 30, 2026     |                                                      |
| `text-embedding-3-large`       |                 | No earlier than April 30, 2026     |                                                      |

---


We'll notify all customers with these preview deployments at least 30 days before the start of the upgrades. We'll publish an upgrade schedule detailing the order of regions and model versions that we'll follow during the upgrades, and link to that schedule from here.

> [!TIP]
> **Will a model upgrade happen if the new model version is not yet available in that region?**
>
> Yes, even in cases where the latest model version is not yet available in a region, we'll automatically upgrade deployments during the scheduled upgrade window. For more information, see [Azure OpenAI model versions](/azure/ai-services/openai/concepts/model-versions#will-a-model-upgrade-happen-if-the-new-model-version-is-not-yet-available-in-that-region).

> [!IMPORTANT]
> Vision enhancements preview features including Optical Character Recognition (OCR), object grounding, video prompts will be retired and no longer available once `gpt-4` Version: `vision-preview` is upgraded to `turbo-2024-04-09`. If you're currently relying on any of these preview features, this automatic model upgrade will be a breaking change.

## Fine-tuned models

Fine-tuned models retire in two phases: training and deployment.

All fine-tuned models follow their equivalent base model for **training** retirement. Once retired, a given model is no longer available for fine tuning.

For fine-tuned models made generally available since `gpt-4o-2024-08-06`, **deployment** retirement occurs 1 year after **training** retirement. At deployment retirement, inference and deployment returns error responses.

| Model            | Version     | Training retirement date  | Deployment retirement date       |
| -----------------|-------------|---------------------------|----------------------------------|
| `gpt-35-turbo`   | 1106        | At base model retirement  | At training retirement           |
| `gpt-35-turbo`   | 0125        | At base model retirement  | At training retirement           |
| `gpt-4o`         | 2024-08-06  | At base model retirement  | One year after training retirement |
| `gpt-4o-mini`    | 2024-07-18  | At base model retirement  | One year after training retirement |
| `gpt-4.1`        | 2025-04-14  | At base model retirement  | One year after training retirement |
| `gpt-4.1-mini`   | 2025-04-14  | At base model retirement  | One year after training retirement |
| `gpt-4.1-nano`   | 2025-04-14  | At base model retirement  | One year after training retirement |
| `o4-mini`        | 2025-04-16  | At base model retirement  | One year after training retirement |

## Default model versions

| Model | Current default version | New default version | Default upgrade date |
|---|---|---|---|
| `gpt-35-turbo` | 0301 | 0125 | Deployments of versions `0301`, `0613`, and `1106` set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 21, 2025.|
|  `gpt-4o` | 2024-08-06 | - | - |

## Deprecated models

 These models are no longer available for new deployments.

If you're an existing customer looking for information about these models, see [Legacy models](./legacy-models.md).

| Model | Deprecation date | Retirement date | Suggested replacement |
| --------- | --------------------- | ------------------- | -------------------- |
| `gpt-4o-realtime-preview` - 2024-10-01 | February 25, 2025 | March 26, 2025 | `gpt-4o-realtime-preview` (version 2024-12-17) or `gpt-4o-mini-realtime-preview` (version 2024-12-17) |
| `gpt-35-turbo` - 0301 | | February 13, 2025   | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-35-turbo` - 0613 | | February 13, 2025 | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-4`<br>`gpt-4-32k` - 0314 |         | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`<br>`gpt-4-32k` - 0613 |         | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-35-turbo-16k`     - 0613 |         | April  30, 2025                    | `gpt-4.1-mini` version: `2025-04-14` |

| babbage-002 | | January 27, 2025 |  |
| davinci-002 | | January 27, 2025 | |
| dall-e-2|  | January 27, 2025 | dalle-3 |
| ada | July 6, 2023 | June 14, 2024 |  |
| babbage | July 6, 2023 | June 14, 2024 |  |
| curie | July 6, 2023 | June 14, 2024 | |
| davinci | July 6, 2023 | June 14, 2024 |  |
| text-ada-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-babbage-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-curie-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-davinci-002 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-davinci-003 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| code-cushman-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| code-davinci-002 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-similarity-ada-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-babbage-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-curie-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-davinci-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-ada-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-ada-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-babbage-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-babbage-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-curie-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-curie-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-davinci-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-davinci-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-ada-code-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-ada-text-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-babbage-code-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-babbage-text-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |

