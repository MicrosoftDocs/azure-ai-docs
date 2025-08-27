---
title: What's new in Azure OpenAI in Azure AI Foundry Models?
description: Learn about the latest news and features updates for Azure OpenAI.
author: mrbullwinkle
ms.author: mbullwin #
manager: nitinme
ms.date: 08/14/2025
ms.service: azure-ai-openai
ms.topic: whats-new
ms.custom:
  - ignite-2023
  - references_regions
  - ignite-2024
  - build-2025
---

# What's new in Azure OpenAI in Azure AI Foundry Models

This article provides a summary of the latest releases and major documentation updates for Azure OpenAI.

## August 2025

### Sora image-to-video support

TBD You can specify the frame index (starting frame in video), and regions of the image to use.

Sora is now available in the Sweden Central region as well as East US 2.

TBD To create a video generation job with inpainting, user should send a POST request to : POST `/video/generations/jobs?api-version=preview`     api-version is v1 if not otherwise specified

### Provisioned spillover General Availability (GA)

Spillover is now Generally Available. Spillover manages traffic fluctuations on provisioned deployments by routing overages to a designated standard deployment. To learn more about how to maximize utilization for your provisioned deployments with spillover, see [Manage traffic with spillover for provisioned deployments](./how-to/spillover-traffic-management.md).

### GPT-5 models available

- `gpt-5`, `gpt-5-mini`, `gpt-5-nano` To learn more, see the [getting started with reasoning models page](./how-to/reasoning.md).
- `gpt-5-chat` is now available. To learn more, see the [models page](./concepts/models.md)

- `gpt-5` is now available for [Provisioned Throughput Units (PTU)](./how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).

- **[Registration is required for access to the gpt-5 model](https://aka.ms/oai/gpt5access).**

- `gpt-5-mini`, `gpt-5-nano`, and `gpt-5-chat` do not require registration.


### New version of model-router

- Model router now supports GPT-5 series models.

- The latest version of model router is currently limited access only. You can request access using the `gpt-5 access` form: [gpt-5 limited access model application](https://aka.ms/oai/gpt5access). If you already have `o3 access` no request is required.

- Model router for Azure AI Foundry is a deployable AI chat model that automatically selects the best underlying chat model to respond to a given prompt. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](./concepts/model-router.md). To use model router with the Completions API, follow the [How-to guide](./concepts/model-router.md).


## July 2025 

### GPT-image-1 update (preview)

- Input fidelity parameter: The `input_fidelity` parameter in the image edits API lets you control how closely the model conveys the style and features of the subjects in the original (input) image. This is useful for:
    - Editing photos while preserving facial features; creating avatars that look like original person across different styles; combining faces from multiple people into one image.
    - Maintaining brand identity in generated images for marketing assets, mockups, product photography.
    - E-commerce and fashion, where you need to edit images of outfits or product details without compromising realism.

- Partial image streaming: The image generation and image edits APIs support partial image streaming, where they return images with partially rendered content throughout the image generation process. Display these images to the user to provide earlier visual feedback and show the progress of the image generation operation. 

## June 2025


### codex-mini & o3-pro models released

- `codex-mini` and `o3-pro` are now available. To learn more, see the [getting started with reasoning models page](./how-to/reasoning.md)

## May 2025

### Sora video generation released (preview)

Sora (2025-05-02) is a video generation model from OpenAI that can create realistic and imaginative video scenes from text instructions.

Follow the [Video generation quickstart](/azure/ai-foundry/openai/video-generation-quickstart) to get started. For more information, see the [Video generation concepts](./concepts/video-generation.md) guide.

### Spotlighting for prompt shields

Spotlighting is a sub-feature of prompt shields that enhances protection against indirect (embedded document) attacks by tagging input documents with special formatting to indicate lower trust to the model. For more information, see the [Prompt shields filter](./concepts/content-filter-prompt-shields.md) documentation.


### Model router (preview)

Model router for Azure AI Foundry is a deployable AI chat model that automatically selects the best underlying chat model to respond to a given prompt. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](./concepts/model-router.md). To use model router with the Completions API, follow the [How-to guide](./concepts/model-router.md).

## April 2025

### Realtime API (preview) support for WebRTC

The Realtime API (preview) now supports WebRTC, enabling real-time audio streaming and low-latency interactions. This feature is ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants. For more information, see the [Realtime API (preview) documentation](./how-to/realtime-audio-webrtc.md).

### GPT-image-1 released (preview, limited access)

GPT-image-1 (`2025-04-15`) is the latest image generation model from Azure OpenAI. It features major improvements over DALL-E, including:
- Better at responding to precise instructions.
- Reliably renders text.
- Accepts images as input, which enables the new capabilities of image editing and inpainting.

Request access: [Limited access model application](https://aka.ms/oai/gptimage1access)

Follow the [image generation how-to guide](/en-us/azure/ai-foundry/openai/how-to/dall-e) to get started with the new model.

### o4-mini and o3 models released

`o4-mini` and `o3` models are now available. These are the latest reasoning models from Azure OpenAI offering significantly enhanced reasoning, quality, and performance. For more information, see the [getting started with reasoning models page](./how-to/reasoning.md).

### GPT-4.1 released

GPT 4.1 and GPT 4.1-nano are now available. These are the latest models from Azure OpenAI. GPT 4.1 has a 1 million token context limit. For more information, see the [models page](./concepts/models.md#gpt-41-series).

### gpt-4o audio models released

New audio models powered by GPT-4o are now available.  

- The `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` speech to text models are released. Use these models via the `/audio` and `/realtime` APIs.  

- The `gpt-4o-mini-tts` text to speech model is released. Use the `gpt-4o-mini-tts` model for text to speech generation via the `/audio` API.

For more information about available models, see the [models and versions documentation](./concepts/models.md#audio-models).

## March 2025

### Responses API & computer-use-preview model

The [Responses API](./how-to/responses.md) is a new stateful API from Azure OpenAI. It brings together the best capabilities from the chat completions and assistants API in one unified experience. The Responses API also adds support for the new `computer-use-preview` model which powers the [Computer use](./how-to/computer-use.md) capability.

**For access to `computer-use-preview` registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who have access to other limited access models will still need to request access for this model.

Request access: [`computer-use-preview` limited access model application](https://aka.ms/oai/cuaaccess)

For more information on model capabilities, and region availability see the [models documentation](./concepts/models.md#computer-use-preview).

:::image type="content" source="./media/computer-use-preview.gif" alt-text="Animated gif of computer-use-preview model integrated with playwright." lightbox="./media/computer-use-preview.gif":::

[Playwright integration demo code](./how-to/responses.md#computer-use).

### Provisioned spillover (preview)

Spillover manages traffic fluctuations on provisioned deployments by routing overages to a designated standard deployment. To learn more about how to maximize utilization for your provisioned deployments with spillover, see [Manage traffic with spillover for provisioned deployments (preview)](./how-to/spillover-traffic-management.md).

### Specify content filtering configurations 

In addition to the deployment-level content filtering configuration, we now also provide a request header that allows you specify your custom configuration at request time for every API call. For more information, see [Use content filters (preview)](./how-to/content-filters.md#specify-a-content-filtering-configuration-at-request-time-preview).

## February 2025

### GPT-4.5 Preview

The latest GPT model that excels at diverse text and image tasks is now available on Azure OpenAI.

For more information on model capabilities, and region availability see the [models documentation](./concepts/models.md).

### Stored completions API

[Stored completions](./how-to/stored-completions.md#stored-completions-api) allow you to capture the conversation history from chat completions sessions to use as datasets for evaluations and fine-tuning.

### o3-mini data zone standard deployments

`o3-mini` is now available for global standard, and data zone standard deployments for registered limited access customers.

For more information, see our [reasoning model guide](./how-to/reasoning.md). 

### gpt-4o mini audio released

The `gpt-4o-mini-audio-preview` (`2024-12-17`) model is the latest audio completions model. For more information, see the [audio generation quickstart](./audio-completions-quickstart.md).

The `gpt-4o-mini-realtime-preview` (`2024-12-17`) model is the latest real-time audio model. The real-time models use the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions. For more information, see the [real-time audio quickstart](./realtime-audio-quickstart.md).

For more information about available models, see the [models and versions documentation](./concepts/models.md#audio-models).

## January 2025

### o3-mini released

`o3-mini` (`2025-01-31`) is the latest reasoning model, offering enhanced reasoning abilities. For more information, see our [reasoning model guide](./how-to/reasoning.md).

### GPT-4o audio completions

The `gpt-4o-audio-preview` model is now available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability). Use the `gpt-4o-audio-preview` model for audio generation.

The `gpt-4o-audio-preview` model introduces the audio modality into the existing `/chat/completions` API. The audio model expands the potential for AI applications in text and voice-based interactions and audio analysis. Modalities supported in `gpt-4o-audio-preview` model include:  text, audio, and text + audio. For more information, see the [audio generation quickstart](./audio-completions-quickstart.md).

> [!NOTE]
> The [Realtime API](./realtime-audio-quickstart.md) uses the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions.

### GPT-4o Realtime API 2024-12-17

The `gpt-4o-realtime-preview` model version 2024-12-17 is available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability). Use the `gpt-4o-realtime-preview` version 2024-12-17 model instead of the `gpt-4o-realtime-preview` version 2024-10-01-preview model for real-time audio interactions.

- Added support for [prompt caching](./how-to/prompt-caching.md) with the `gpt-4o-realtime-preview` model.
- Added support for new voices. The `gpt-4o-realtime-preview` models now support the following voices: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`.
- Rate limits are no longer based on connections per minute. Rate limiting is now based on RPM (requests per minute) and TPM (tokens per minute) for the `gpt-4o-realtime-preview` model. The rate limits for each `gpt-4o-realtime-preview` model deployment are 100K TPM and 1K RPM. During the preview, [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and APIs might inaccurately show different rate limits. Even if you try to set a different rate limit, the actual rate limit will be 100K TPM and 1K RPM.

For more information, see the [GPT-4o real-time audio quickstart](realtime-audio-quickstart.md) and the [how-to guide](./how-to/realtime-audio.md).

## December 2024

### o1 reasoning model released for limited access

The latest `o1` model is now available for API access and model deployment. **Registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who previously applied and received access to `o1-preview`, don't need to reapply as they're automatically on the wait-list for the latest model.

Request access: [limited access model application](https://aka.ms/OAI/o1access)

To learn more about the advanced `o1` series models see, [getting started with o1 series reasoning models](./how-to/reasoning.md).

### Region availability

| Model | Region |
|---|---|
|`o1` <br>(Version: 2024-12-17)| East US2 (Global Standard) <br> Sweden Central (Global Standard) |

### Preference fine-tuning (preview)

[Direct preference optimization (DPO)](./how-to/fine-tuning-direct-preference-optimization.md) is a new alignment technique for large language models, designed to adjust model weights based on human preferences. Unlike reinforcement learning from human feedback (RLHF), DPO doesn't require fitting a reward model and uses simpler data (binary preferences) for training. This method is computationally lighter and faster, making it equally effective at alignment while being more efficient. DPO is especially useful in scenarios where subjective elements like tone, style, or specific content preferences are important. We’re excited to announce the public preview of DPO in Azure OpenAI, starting with the `gpt-4o-2024-08-06` model.

For fine-tuning model region availability, see the [models page](./concepts/models.md#fine-tuning-models).

### Stored completions & distillation

[Stored completions](./how-to/stored-completions.md) allow you to capture the conversation history from chat completions sessions to use as datasets for [evaluations](./how-to/evaluations.md) and [fine-tuning](./how-to/fine-tuning.md).

### GPT-4o 2024-11-20

`gpt-4o-2024-11-20` is now available for [global standard deployment](./how-to/deployment-types.md) in:

- East US
- East US 2
- North Central US
- South Central US
- West US
- West US 3
- Sweden Central

### NEW data zone provisioned deployment type

Data zone provisioned deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure infrastructure within Microsoft specified data zones. Data zone provisioned deployments are supported on `gpt-4o-2024-08-06`, `gpt-4o-2024-05-13`, and `gpt-4o-mini-2024-07-18` models.

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

## Next steps

Learn more about the [underlying models that power Azure OpenAI](./concepts/models.md).
