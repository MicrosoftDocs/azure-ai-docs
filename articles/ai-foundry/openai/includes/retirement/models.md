---
title: Model Retirement Table 
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Model retirement table for Azure OpenAI in Microsoft Foundry Models.
manager: nitinme
ms.date: 12/16/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom: references_regions, build-2025
---


# [Text generation](#tab/text)

### Text generation

| Model Name | Model Version<sup>1</sup> | Lifecycle Status | Deprecation Date (No New Customers) | Retirement Date | Replacement Model |
|:--|:--|:--|:--|:--|:--|
| `gpt-5-chat` | 2025-08-07 | `Preview` | n/a | 2026-03-01 | `gpt-5.2-chat` |
| `gpt-5-chat` | 2025-10-03 | `Preview` | n/a | 2026-03-01 | `gpt-5.2-chat` |
| `gpt-4o` | 2024-05-13 | `Generally Available` | 2025-05-13 | Standard deployment type retires on **2026-03-31**, with auto-upgrades scheduled to start on **2026-03-09**. For other deployment types, including ALL Provisioned, Global Standard, and Data Zone Standard, the retirement date has been moved to **2026-10-01**. | `gpt-5.1` |
| `gpt-4o` | 2024-08-06 | `Generally Available` | 2025-08-06 | Standard deployment type retires on **2026-03-31**, with auto-upgrades scheduled to start on **2026-03-09**. For other deployment types, including ALL Provisioned, Global Standard, and Data Zone Standard, the retirement date has been moved to **2026-10-01**. | `gpt-5.1` |
| `gpt-4o` | 2024-11-20 | `Generally Available` | 2025-11-20 | 2026-10-01 | `gpt-5.1` |
| `gpt-4o-mini` | 2024-07-18 | `Generally Available` | 2025-07-18 | Standard deployment type retires on **2026-03-31**, with auto-upgrades scheduled to start on **2026-03-09**. For other deployment types, including ALL Provisioned, Global Standard, and Data Zone Standard, the retirement date has been moved to **2026-10-01**. | `gpt-4.1-mini` |
| `gpt-4.1` | 2025-04-14 | `Generally Available` | 2026-04-14 | 2026-10-14 | `gpt-5` |
| `gpt-4.1-mini` | 2025-04-14 | `Generally Available` | 2026-04-14 | 2026-10-14 | `gpt-5-mini` |
| `gpt-4.1-nano` | 2025-04-14 | `Generally Available` | 2026-04-14 | 2026-10-14 | `gpt-5-nano` |
| `computer-use-preview` | 2025-03-11 | `Preview` | n/a | No earlier than 2026-04-14 |  |
| `o1` | 2024-12-17 | `Generally Available` | 2025-12-17 | 2026-07-15 | `o3` |
| `o1-pro` | 2025-03-19 | `Generally Available` | 2026-03-19 | 2026-09-18 | `o3-pro` |
| `o3-mini` | 2025-01-31 | `Generally Available` | 2026-01-31 | 2026-08-02 | `o4-mini` |
| `o3` | 2025-04-16 | `Generally Available` | 2026-04-16 | 2026-10-16 |  |
| `o3-pro` | 2025-06-10 | `Generally Available` | 2026-06-10 | 2026-12-10 |  |
| `o3-deep-research` | 2025-06-26 | `Generally Available` | 2026-06-26 | 2026-12-26 |  |
| `o4-mini` | 2025-04-16 | `Generally Available` | 2026-04-16 | 2026-10-16 |  |
| `codex-mini` | 2025-05-16 | `Generally Available` | 2026-05-16 | 2026-11-15 |  |
| `model-router` | 2025-11-18 | `Generally Available` | 2026-11-18 | 2027-05-20 |  |
| `gpt-5-mini` | 2025-08-07 | `Generally Available` | 2026-08-07 | 2027-02-06 |  |
| `gpt-5-nano` | 2025-08-07 | `Generally Available` | 2026-08-07 | 2027-02-06 |  |
| `gpt-5-codex` | 2025-09-15 | `Generally Available` | 2026-09-15 | 2027-03-17 |  |
| `gpt-5-pro` | 2025-10-06 | `Generally Available` | 2026-10-06 | 2027-04-07 |  |
| `gpt-5.1` | 2025-11-13 | `Generally Available` | 2026-11-13 | 2027-05-15 |  |
| `gpt-5.1-codex` | 2025-11-13 | `Generally Available` | 2026-11-13 | 2027-05-15 |  |
| `gpt-5.1-codex-mini` | 2025-11-13 | `Generally Available` | 2026-11-13 | 2027-05-15 |  |
| `gpt-5.1-chat` | 2025-11-13 | `Preview` | n/a | No earlier than 2026-03-31 |  |
| `gpt-5.2` | 2025-12-11 | `Generally Available` | No earlier than 2026-12-12 | No earlier than 2027-05-12 | |
| `gpt-5.2-chat` | 2025-12-11 | `Preview` | n/a | No earlier than 2026-04-01 | |


# [Audio](#tab/audio)

### Audio

| Model Name | Model Version<sup>1</sup>  | Lifecycle Status | Deprecation Date (No New Customers) | Retirement Date | Replacement Model |
|:--|:--|:--|:--|:--|:--|
| `gpt-4o-audio-preview` | 2024-12-17 | `Preview` | n/a | 2026-02-02 | `gpt-audio` |
| `gpt-4o-realtime-preview` | 2024-12-17 | `Preview` | n/a | 2026-02-02 | `gpt-realtime` |
| `gpt-4o-mini-audio-preview` | 2024-12-17 | `Preview` | n/a | No earlier than February 28, 2026 |  |
| `gpt-4o-mini-realtime-preview` | 2024-12-17 | `Preview` | n/a | No earlier than February 28, 2026 |  |
| `gpt-4o-transcribe` | 2025-03-20 | `Preview` | n/a | No earlier than February 28, 2026 |  |
| `gpt-4o-mini-tts` | 2025-03-20 | `Preview` | n/a | No earlier than February 28, 2026 |  |
| `gpt-4o-mini-transcribe` | 2025-03-20 | `Preview` | n/a | No earlier than February 28, 2026 |  |
| `gpt-4o-transcribe-diarize` | 2025-10-15 | `Generally Available` | 2026-10-15 | 2027-04-16 |  |
| `gpt-audio` | 2025-08-28 | `Generally Available` | 2026-08-28 | 2027-02-28 |  |
| `gpt-realtime` | 2025-08-28 | `Generally Available` | 2026-08-28 | 2027-02-28 |  |
| `gpt-audio-mini` | 2025-10-06 | `Generally Available` | 2026-10-06 | 2027-04-07 |  |
| `tts` | 001 | `Generally Available` | No earlier than February 28, 2026 |  |  |
| `tts-hd` | 001 | `Generally Available` | No earlier than February 28, 2026 |  |  |
| `whisper` | 001 | `Generally Available` | No earlier than June 18, 2026 |  |  |
| `gpt-realtime-mini` | 2025-12-15   | `Generally Available` | n/a | No earlier than December 15, 2026    |       |
| `gpt-4o-mini-transcribe` | 2025-12-15   | `Generally Available` | n/a | No earlier than December 15, 2026    |       |
| `gpt-4o-mini-tts` | 2025-12-15   | `Generally Available` | n/a | No earlier than December 15, 2026    |       |

# [Image and video](#tab/image)

### Image and video

| Model Name | Model Version<sup>1</sup>  | Lifecycle Status | Deprecation Date (No New Customers) | Retirement Date | Replacement Model |
|:--|:--|:--|:--|:--|:--|
| `dall-e-3` | 3 | `Generally Available` | n/a | 2026-03-04 | `gpt-image-1-mini` |
| `gpt-image-1` | 2025-04-15 | `Preview` | n/a | No earlier than 2026-03-31 | `gpt-image-1-mini` |
| `gpt-image-1-mini` | 2025-10-06 | `Generally Available` | 2026-10-06 | 2027-04-07 |  |
| `sora` | 2025-05-02 | `Preview` | n/a | No earlier than 2026-02-28 | `sora-2` |
| `gpt-image-1.5`    | 2025-12-16   | `Preview`    | n/a | No earlier than 2026-12-16 |  |
| `sora-2` | 2025-10-15 | `Preview` | n/a | No earlier than 2026-04-30 |  |


# [Embedding](#tab/embedding)

### Embedding

| Model Name | Model Version<sup>1</sup>  | Lifecycle Status | Deprecation Date (No New Customers) | Retirement Date | Replacement Model |
|:--|:--|:--|:--|:--|:--|
| `text-embedding-3-large` | 1 | `Generally Available` | n/a | No retirement scheduled. Will not retire before April 15, 2027 | n/a |
| `text-embedding-3-small` | 1 | `Generally Available` | n/a | No retirement scheduled. Will not retire before April 15, 2027 | n/a |
| `text-embedding-ada-002` | 2 | `Generally Available` | n/a | No retirement scheduled. Will not retire before April 15, 2027 | n/a |
| `text-embedding-ada-002` | 1 | `Generally Available` | n/a | No retirement scheduled. Will not retire before April 15, 2027 | n/a |

---

<sup>1</sup> For some models, the launch date is used as the value of the model version.

We notify all customers with these preview deployments at least 30 days before the start of the upgrades. We publish an upgrade schedule that details the order of regions and model versions that we follow during the upgrades, and link to that schedule from here.

> [!TIP]
> Will a model upgrade happen if the new model version isn't yet available in that region?
>
> Yes, even in cases where the latest model version isn't yet available in a region, we automatically upgrade deployments during the scheduled upgrade window. For more information, see [Azure OpenAI model versions](/azure/ai-foundry/openai/concepts/model-versions#will-a-model-upgrade-happen-if-the-new-model-version-is-not-yet-available-in-that-region).

## Fine-tuned models

Fine-tuned models retire in two phases: *training* and *deployment*.

Unless explicitly stated, training retires no earlier than the base model retirement date. After a model is retired for training, it's no longer available for fine-tuning but any models you've trained remain available for deployment.

At deployment retirement, inference and deployment return error responses.

| Model            | Version     | Training retirement date   | Deployment retirement date        |
| -----------------|-------------|----------------------------|-----------------------------------|
| `gpt-4o`         | 2024-08-06  | No earlier than 2026-09-31<sup>1</sup> | 2027-03-31 |
| `gpt-4o-mini`    | 2024-07-18  | No earlier than 2026-09-31<sup>1</sup> | 2027-03-31 |
| `gpt-4.1`        | 2025-04-14  | Base model retirement  | One year after training retirement |
| `gpt-4.1-mini`   | 2025-04-14  | Base model retirement  | One year after training retirement |
| `gpt-4.1-nano`   | 2025-04-14  | Base model retirement  | One year after training retirement |
| `o4-mini`        | 2025-04-16  | Base model retirement  | One year after training retirement |

<sup>1</sup> For existing customers only. Otherwise, training retirement occurs at base model retirement.

## Default model versions

| Model | Current default version | New default version | Default upgrade date |
|---|---|---|---|
|  `gpt-4o` | 2024-08-06 | - | - |
