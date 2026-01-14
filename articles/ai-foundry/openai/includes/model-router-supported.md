---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 12/12/2025
---


## Supported underlying models
With the `2025-11-18` version, Model Router adds nine new models including Anthropic's Claude, DeepSeek, Llama, Grok models to support a total of 18 models available for routing your prompts.

> [!NOTE]
> You don't need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments will get invoked by Model router if they're selected for routing.

|Model router version|Underlying models| Underlying model version
|:---:|:---|:----:|
|`2025-11-18`| `gpt-4.1` </br> `gpt-4.1-mini` </br> `gpt-4.1-nano` </br> `o4-mini` <br> `gpt-5-nano` <br> `gpt-5-mini` <br> `gpt-5`<sup>1</sup> <br> `gpt-5-chat` <br> `Deepseek-v3.1`<sup>2</sup> <br> `gpt-oss-120b`<sup>2</sup> <br> `llama4-maverick-instruct`<sup>2</sup> <br> `grok-4`<sup>2</sup> <br> `grok-4-fast`<sup>2</sup> <br> `claude-haiku-4-5`<sup>3</sup> <br> `claude-opus-4-1`<sup>3</sup> <br> `claude-sonnet-4-5`<sup>3</sup> | `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> N/A <br> N/A <br> N/A <br> N/A <br> N/A <br> `2024-11-20` <br> `2024-07-18` <br> `2025-10-01` <br> `2025-08-05` <br> `2025-09-29` |
|`2025-08-07`| `gpt-4.1` </br> `gpt-4.1-mini` </br> `gpt-4.1-nano` </br> `o4-mini` </br> `gpt-5`<sup>1</sup> <br> `gpt-5-mini` <br> `gpt-5-nano` <br> `gpt-5-chat` | `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` |
|`2025-05-19`| `gpt-4.1` </br>`gpt-4.1-mini` </br>`gpt-4.1-nano` </br>`o4-mini`  |  `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` |

- <sup>1</sup>Requires registration.
- <sup>2</sup>Model router support is in preview.
- <sup>3</sup>Model router support is in preview. Requires deployment of model for use with Model router.