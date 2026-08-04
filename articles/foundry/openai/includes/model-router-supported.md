---
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 03/18/2026
---


## Supported models

> [!NOTE]
> You don't need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments will get invoked by Model router if they're selected for routing.

### Model router version `2025-11-18` (latest)

| Format | Model | Version |
|:---|:---|:---:|
| OpenAI | `gpt-4.0` | `2024-11-20` |
| OpenAI | `gpt-4.0-mini` | `2024-07-18` |
| OpenAI | `gpt-4.1` | `2025-04-14` |
| OpenAI | `gpt-4.1-mini` | `2025-04-14` |
| OpenAI | `gpt-4.1-nano` | `2025-04-14` |
| OpenAI | `o4-mini` | `2025-04-16` |
| OpenAI | `gpt-5-nano` | `2025-08-07` |
| OpenAI | `gpt-5-mini` | `2025-08-07` |
| OpenAI | `gpt-5` | `2025-08-07` |
| OpenAI | `gpt-5-chat` | `2025-08-07` |
| OpenAI | `gpt-5.2` | `2025-12-11` |
| OpenAI | `gpt-5.2-chat` | `2025-12-11` |
| OpenAI | `gpt-5.3-chat` | `2026-03-03` |
| OpenAI | `gpt-5.4-nano` | `2026-03-17` |
| OpenAI | `gpt-5.4-mini` | `2026-03-17` |
| OpenAI | `gpt-5.4` | `2026-03-05` |
| OpenAI | `gpt-5.5` | `2026-04-24` |
| DeepSeek | `Deepseek-V3.1`<sup>2</sup> | `1` |
| DeepSeek | `Deepseek-V3.2`<sup>2</sup> | `1` |
| OpenAI | `gpt-oss-120b`<sup>2</sup> | `1` |
| Meta | `Llama-4-Maverick-17B-128E-Instruct-FP8`<sup>2</sup> | `1` |
| xAI | `grok-4`<sup>2</sup> | `1` |
| xAI | `grok-4-fast-reasoning`<sup>2</sup> | `1` |
| Anthropic | `claude-haiku-4-5`<sup>3</sup> | `20251001` |
| Anthropic | `claude-sonnet-4-5`<sup>3</sup> | `20250929` |
| Anthropic | `claude-opus-4-1`<sup>3</sup> | `20250805` |
| Anthropic | `claude-opus-4-6`<sup>3</sup> | `1` |
| Anthropic | `claude-opus-4-7`<sup>3</sup> | `1` |

- <sup>1</sup>Requires registration.
- <sup>2</sup>Model router support is in preview.
- <sup>3</sup>Model router support is in preview. Requires deployment of model for use with Model router.

<!--
### Model router version `2025-08-07`

| Format | Model | Version |
|:---|:---|:---:|
| OpenAI | `gpt-4.1` | `2025-04-14` |
| OpenAI | `gpt-4.1-mini` | `2025-04-14` |
| OpenAI | `gpt-4.1-nano` | `2025-04-14` |
| OpenAI | `o4-mini` | `2025-04-16` |
| OpenAI | `gpt-5`<sup>1</sup> | `2025-08-07` |
| OpenAI | `gpt-5-mini` | `2025-08-07` |
| OpenAI | `gpt-5-nano` | `2025-08-07` |
| OpenAI | `gpt-5-chat` | `2025-08-07` |

- <sup>1</sup>Requires registration.


### Model router version `2025-05-19`

| Format | Model | Version |
|:---|:---|:---:|
| OpenAI | `gpt-4.1` | `2025-04-14` |
| OpenAI | `gpt-4.1-mini` | `2025-04-14` |
| OpenAI | `gpt-4.1-nano` | `2025-04-14` |
| OpenAI | `o4-mini` | `2025-04-16` |
-->
