---
title: What's new in Azure OpenAI in Azure AI Foundry Models?
titleSuffix: Azure AI services
description: Learn about the latest news and features updates for Azure OpenAI.
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin #
ms.service: azure-ai-openai
ms.custom:
  - ignite-2023
  - references_regions
  - ignite-2024
ms.topic: whats-new
ms.date: 04/16/2025
recommendations: false
---

# What's new in Azure OpenAI in Azure AI Foundry Models

This article provides a summary of the latest releases and major documentation updates for Azure OpenAI.

## April 2025

### Realtime API (preview) support for WebRTC

The Realtime API (preview) now supports WebRTC, enabling real-time audio streaming and low-latency interactions. This feature is ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants. For more information, see the [Realtime API (preview) documentation](./how-to/realtime-audio-webrtc.md).

### GPT-image-1 released (preview, limited access)

GPT-image-1 (2025-04-15) is the latest image generation model from Azure OpenAI. It features major improvements over DALL-E, including:
- Better at responding to precise instructions.
- Reliably renders text.
- Accepts images as input, which enables the new capabilities of image editing and inpainting.

Request access: [Limited access model application](https://aka.ms/oai/gptimage1access)

Follow the [image generation how-to guide](/en-us/azure/ai-services/openai/how-to/dall-e) to get started with the new model.

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

For more information on model capabilities, and region availability see the [models documentation](./concepts/models.md#gpt-45-preview).

### Stored completions API

[Stored completions](./how-to/stored-completions.md#stored-completions-api) allow you to capture the conversation history from chat completions sessions to use as datasets for evaluations and fine-tuning.

### o3-mini datazone standard deployments

`o3-mini` is now available for global standard, and data zone standard deployments for registered limited access customers.

For more information, see our [reasoning model guide](./how-to/reasoning.md). 

### gpt-4o mini audio released

The `gpt-4o-mini-audio-preview` (2024-12-17) model is the latest audio completions model. For more information, see the [audio generation quickstart](./audio-completions-quickstart.md).

The `gpt-4o-mini-realtime-preview` (2024-12-17) model is the latest real-time audio model. The real-time models use the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions. For more information, see the [real-time audio quickstart](./realtime-audio-quickstart.md).

For more information about available models, see the [models and versions documentation](./concepts/models.md#audio-models).

## January 2025

### o3-mini released

`o3-mini` (2025-01-31) is the latest reasoning model, offering enhanced reasoning abilities. For more information, see our [reasoning model guide](./how-to/reasoning.md).

### GPT-4o audio completions

The `gpt-4o-audio-preview` model is now available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability). Use the `gpt-4o-audio-preview` model for audio generation.

The `gpt-4o-audio-preview` model introduces the audio modality into the existing `/chat/completions` API. The audio model expands the potential for AI applications in text and voice-based interactions and audio analysis. Modalities supported in `gpt-4o-audio-preview` model include:  text, audio, and text + audio. For more information, see the [audio generation quickstart](./audio-completions-quickstart.md).

> [!NOTE]
> The [Realtime API](./realtime-audio-quickstart.md) uses the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions.

### GPT-4o Realtime API 2024-12-17

The `gpt-4o-realtime-preview` model version 2024-12-17 is available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability). Use the `gpt-4o-realtime-preview` version 2024-12-17 model instead of the `gpt-4o-realtime-preview` version 2024-10-01-preview model for real-time audio interactions.

- Added support for [prompt caching](./how-to/prompt-caching.md) with the `gpt-4o-realtime-preview` model.
- Added support for new voices. The `gpt-4o-realtime-preview` models now support the following voices: "alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse".
- Rate limits are no longer based on connections per minute. Rate limiting is now based on RPM (requests per minute) and TPM (tokens per minute) for the `gpt-4o-realtime-preview` model. The rate limits for each `gpt-4o-realtime-preview` model deployment are 100K TPM and 1K RPM. During the preview, [Azure AI Foundry portal](https://ai.azure.com/) and APIs might inaccurately show different rate limits. Even if you try to set a different rate limit, the actual rate limit will be 100K TPM and 1K RPM.

For more information, see the [GPT-4o real-time audio quickstart](realtime-audio-quickstart.md) and the [how-to guide](./how-to/realtime-audio.md).

## December 2024

### o1 reasoning model released for limited access

The latest `o1` model is now available for API access and model deployment. **Registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who previously applied and received access to `o1-preview`, don't need to reapply as they are automatically on the wait-list for the latest model.

Request access: [limited access model application](https://aka.ms/OAI/o1access)

To learn more about the advanced `o1` series models see, [getting started with o1 series reasoning models](./how-to/reasoning.md).

### Region availability

| Model | Region |
|---|---|
|`o1` <br>(Version: 2024-12-17)| East US2 (Global Standard) <br> Sweden Central (Global Standard) |

### Preference fine-tuning (preview)

[Direct preference optimization (DPO)](./how-to/fine-tuning-direct-preference-optimization.md) is a new alignment technique for large language models, designed to adjust model weights based on human preferences. Unlike reinforcement learning from human feedback (RLHF), DPO does not require fitting a reward model and uses simpler data (binary preferences) for training. This method is computationally lighter and faster, making it equally effective at alignment while being more efficient. DPO is especially useful in scenarios where subjective elements like tone, style, or specific content preferences are important. We’re excited to announce the public preview of DPO in Azure OpenAI, starting with the `gpt-4o-2024-08-06` model.

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

## November 2024

### Vision Fine-tuning GA

Vision fine-tuning with GPT-4o (2024-08-06) in now Generally Available (GA).

[Vision fine-tuning](./how-to/fine-tuning.md) allows you to add images to your JSONL training data. Just as you can send one or many image inputs to chat completions, you can include those same message types within your training data. Images can be provided either as URLs or as base64 encoded images.

For fine-tuning model region availability, see the [models page](./concepts/models.md#fine-tuning-models).

### NEW AI abuse monitoring

We are introducing new forms of abuse monitoring that leverage LLMs to improve efficiency of detection of potentially abusive use of the Azure OpenAI service and to enable abuse monitoring without the need for human review of prompts and completions. Learn more, see [Abuse monitoring](/azure/ai-services/openai/concepts/abuse-monitoring).

Prompts and completions that are flagged through content classification and/or identified to be part of a potentially abusive pattern of use are subjected to an additional review process to help confirm the system's analysis and inform actioning decisions. Our abuse monitoring systems have been expanded to enable review by LLM by default and by humans when necessary and appropriate. 

## October 2024

### NEW data zone standard deployment type

Data zone standard deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone standard provides higher default quotas than our Azure geography-based deployment types.  Data zone standard deployments are supported on `gpt-4o-2024-08-06`, `gpt-4o-2024-05-13`, and `gpt-4o-mini-2024-07-18` models.

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

### Global Batch GA

Azure OpenAI global batch is now generally available.

The Azure OpenAI Batch API is designed to handle large-scale and high-volume processing tasks efficiently. Process asynchronous groups of requests with separate quota, with 24-hour target turnaround, at [50% less cost than global standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than send one request at a time you send a large number of requests in a single file. Global batch requests have a separate enqueued token quota avoiding any disruption of your online workloads.  

Key use cases include:

* **Large-Scale Data Processing:** Quickly analyze extensive datasets in parallel.

* **Content Generation:** Create large volumes of text, such as product descriptions or articles.

* **Document Review and Summarization:** Automate the review and summarization of lengthy documents.

* **Customer Support Automation:** Handle numerous queries simultaneously for faster responses.

* **Data Extraction and Analysis:** Extract and analyze information from vast amounts of unstructured data.

* **Natural Language Processing (NLP) Tasks:** Perform tasks like sentiment analysis or translation on large datasets.

* **Marketing and Personalization:** Generate personalized content and recommendations at scale.

For more information on [getting started with global batch deployments](./how-to/batch.md).

### o1-preview and o1-mini models limited access

The `o1-preview` and `o1-mini` models are now available for API access and model deployment. **Registration is required, and access will be granted based on Microsoft's eligibility criteria**.

Request access: [limited access model application](https://aka.ms/oai/modelaccess)

Customers who were already approved and have access to the model through the early access playground don't need to apply again, you'll automatically be granted API access. Once access has been granted, you'll need to create a deployment for each model.

**API support:**

Support for the **o1 series** models was added in API version `2024-09-01-preview`.

The `max_tokens` parameter has been deprecated and replaced with the new `max_completion_tokens` parameter. **o1 series** models will only work with the `max_completion_tokens` parameter.

**Region availability**:

Models are available for standard and global standard deployment in East US2 and Sweden Central for approved customers.

### New GPT-4o Realtime API for speech and audio public preview

Azure OpenAI GPT-4o audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o audio `realtime` API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

The `gpt-4o-realtime-preview` model is available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability).

For more information, see the [GPT-4o real-time audio quickstart](realtime-audio-quickstart.md).

### Global batch support updates

Global batch now supports GPT-4o (2024-08-06). See the [global batch getting started guide](./how-to/batch.md) for more information.

## September 2024

### Azure OpenAI Studio UX updates

As of September 19, 2024, when you go to the [Azure OpenAI Studio](https://oai.azure.com/) you no longer see the legacy Azure OpenAI Studio by default. If needed you'll still be able to go back to the previous experience by using the **Switch to the old look** toggle in the top bar of the UI for the next couple of weeks. If you switch back to legacy [Azure AI Foundry portal](https://ai.azure.com/), it helps if you fill out the feedback form to let us know why. We're actively monitoring this feedback to improve the new experience.


### GPT-4o 2024-08-06 provisioned deployments
GPT-4o 2024-08-06 is now available for provisioned deployments in East US, East US 2, North Central US, and Sweden Central. It's also available for global provisioned deployments.

For the latest information on model availability, see the [models page](/azure/ai-services/openai/concepts/models#provisioned-deployment-model-availability).

### NEW Global provisioned deployment type
Global deployments are available in the same Azure OpenAI resources as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure. Global provisioned deployments are supported on `gpt-4o-2024-08-06` and `gpt-4o-mini-2024-07-18` models.

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

### NEW o1-preview and o1-mini models available for limited access

The Azure OpenAI `o1-preview` and `o1-mini` models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

### Key capabilities of the o1 series

- Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
- Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
- Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
- Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.

### Model variants

- `o1-preview`: `o1-preview` is the more capable of the `o1` series models.  
- `o1-mini`: `o1-mini` is the faster and cheaper of the `o1` series models.

Model version: `2024-09-12`

Request access: [limited access model application](https://aka.ms/oai/modelaccess)

### Limitations

The `o1` series models are currently in preview and don't include some features available in other models, such as image understanding and structured outputs which are available in the latest GPT-4o model. For many tasks, the generally available GPT-4o models might still be more suitable.

### Safety

OpenAI has incorporated additional safety measures into the `o1` models, including new techniques to help the models refuse unsafe requests. These advancements make the `o1` series some of the most robust models available.

### Availability

The `o1-preview` and `o1-mini` are available in the East US2 region for limited access through the [Azure AI Foundry portal](https://ai.azure.com) early access playground. Data processing for the `o1` models might occur in a different region than where they are available for use.

To try the `o1-preview` and `o1-mini` models in the early access playground **registration is required, and access will be granted based on Microsoft’s eligibility criteria.**

Request access: [limited access model application](https://aka.ms/oai/modelaccess)

Once access has been granted, you will need to:

1. Navigate to https://ai.azure.com/resources and select a resource in the `eastus2` region. If you don't have an Azure OpenAI resource in this region you'll need to [create one](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI).  
2. Once the `eastus2` Azure OpenAI resource is selected, in the upper left-hand panel under **Playgrounds** select **Early access playground (preview)**.
 
## August 2024

### GPT-4o 2024-08-06 structured outputs

- Available for standard and global deployments in [all US regions and Sweden Central](./concepts/models.md#global-standard-model-availability).
- This model adds support for [structured outputs](https://aka.ms/oai/docs/structured-outputs).

### GPT-4o mini provisioned deployments

GPT-4o mini is now available for provisioned deployments in Canada East, East US, East US2, North Central US, and Sweden Central.

For the latest information on model availability, see the [models page](/azure/ai-services/openai/concepts/models#provisioned-deployment-model-availability).

### GPT-4o fine-tuning (Public Preview)

GPT-4o fine-tuning is now available for Azure OpenAI in public preview in North Central US and Sweden Central.

For more information, see our [blog post](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/fine-tune-gpt-4o-on-azure-openai-service/ba-p/4228693).

### New preview API release

API version `2024-07-01-preview` is the latest dataplane authoring & inference API release. It replaces API version `2024-05-01-preview` and adds support for:

- [Batch API support added](./how-to/batch.md)
- [Vector store chunking strategy parameters](/azure/ai-services/openai/reference-preview?#request-body-17)
- `max_num_results` that the file search tool should output.

For more information see our [reference documentation](./reference-preview.md)

### GPT-4o mini regional availability

- GPT-4o mini is available for standard and global standard deployment in the East US and Sweden Central regions.
- GPT-4o mini is available for global batch deployment in East US, Sweden Central, and West US regions.

### Evaluations guide

- New blog post on [getting started with model evaluations](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880). We recommend using this guide as part of the [model upgrade and retirement process](./concepts/model-retirements.md).

### Latest GPT-4o model available in the early access playground (preview)

On August 6, 2024, OpenAI [announced](https://openai.com/index/introducing-structured-outputs-in-the-api/) the latest version of their flagship GPT-4o model version `2024-08-06`. GPT-4o `2024-08-06` has all the capabilities of the previous version as well as:

* An enhanced ability to support complex structured outputs.
* Max output tokens have been increased from 4,096 to 16,384.

Azure customers can test out GPT-4o `2024-08-06` today in the new Azure AI Foundry early access playground (preview).

Unlike the previous early access playground, the [Azure AI Foundry portal](https://ai.azure.com/) early access playground (preview) doesn't require you to have a resource in a specific region.

> [!NOTE]
> Prompts and completions made through the early access playground (preview) might be processed in any Azure OpenAI region, and are currently subject to a 10 request per minute per Azure subscription limit. This limit might change in the future.
>
> Azure OpenAI abuse monitoring is enabled for all early access playground users even if approved for modification; default content filters are enabled and cannot be modified.

To test out GPT-4o `2024-08-06`, sign-in to the Azure AI early access playground (preview) using this [link](https://aka.ms/oai/docs/earlyaccessplayground).

### Global batch deployments are now available

The Azure OpenAI Batch API is designed to handle large-scale and high-volume processing tasks efficiently. Process asynchronous groups of requests with separate quota, with 24-hour target turnaround, at [50% less cost than global standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than send one request at a time you send a large number of requests in a single file. Global batch requests have a separate enqueued token quota avoiding any disruption of your online workloads.  

Key use cases include:

* **Large-Scale Data Processing:** Quickly analyze extensive datasets in parallel.

* **Content Generation:** Create large volumes of text, such as product descriptions or articles.

* **Document Review and Summarization:** Automate the review and summarization of lengthy documents.

* **Customer Support Automation:** Handle numerous queries simultaneously for faster responses.

* **Data Extraction and Analysis:** Extract and analyze information from vast amounts of unstructured data.

* **Natural Language Processing (NLP) Tasks:** Perform tasks like sentiment analysis or translation on large datasets.

* **Marketing and Personalization:** Generate personalized content and recommendations at scale.

For more information on [getting started with global batch deployments](./how-to/batch.md).

## July 2024

### GPT-4o mini is now available for fine-tuning

GPT-4o mini fine-tuning is [now available in public preview](./concepts/models.md#fine-tuning-models) in Sweden Central and in North Central US.

### Assistants File Search tool is now billed

The [file search](./how-to/file-search.md) tool for Assistants now has additional charges for usage. See the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for more information.

### GPT-4o mini model available for deployment

GPT-4o mini is the latest Azure OpenAI model first [announced on July 18, 2024](https://azure.microsoft.com/blog/openais-fastest-model-gpt-4o-mini-is-now-available-on-azure-ai/):

*"GPT-4o mini allows customers to deliver stunning applications at a lower cost with blazing speed. GPT-4o mini is significantly smarter than GPT-3.5 Turbo—scoring 82% on Measuring Massive Multitask Language Understanding (MMLU) compared to 70%—and is more than 60% cheaper.1 The model delivers an expanded 128K context window and integrates the improved multilingual capabilities of GPT-4o, bringing greater quality to languages from around the world."*

The model is currently available for both [standard and global standard deployment](./how-to/deployment-types.md) in the East US region.

For information on model quota, consult the [quota and limits page](./quotas-limits.md) and for the latest info on model availability refer to the [models page](./concepts/models.md).

### New Responsible AI default content filtering policy 

The new default content filtering policy `DefaultV2` delivers the latest safety and security mitigations for the GPT model series (text), including:
- Prompt Shields for jailbreak attacks on user prompts (filter), 
- Protected material detection for text (filter) on model completions 
- Protected material detection for code (annotate) on model completions

While there are no changes to content filters for existing resources and deployments (default or custom content filtering configurations remain unchanged), new resources and GPT deployments will automatically inherit the new content filtering policy `DefaultV2`. Customers have the option to switch between safety defaults and create custom content filtering configurations. 

Refer to our [Default safety policy documentation](./concepts/default-safety-policies.md) for more information.

### New GA API release

API version `2024-06-01` is the latest GA data plane inference API release. It replaces API version `2024-02-01` and adds support for:

- embeddings `encoding_format` & `dimensions` parameters.
- chat completions `logprobs` & `top_logprobs` parameters.

Refer to our [data plane inference reference documentation](./reference.md) for more information.

### Expansion of regions available for global standard deployments of gpt-4o

 GPT-4o is now available for [global standard deployments](./how-to/deployment-types.md) in:

- australiaeast     
- brazilsouth       
- canadaeast        
- eastus            
- eastus2           
- francecentral     git
- germanywestcentral
- japaneast         
- koreacentral      
- northcentralus    
- norwayeast        
- polandcentral     
- southafricanorth  
- southcentralus    
- southindia        
- swedencentral     
- switzerlandnorth  
- uksouth           
- westeurope        
- westus            
- westus3           

For information on global standard quota, consult the [quota and limits page](./quotas-limits.md).


## June 2024

### Retirement date updates

* Updated `gpt-35-turbo` 0301 retirement date to no earlier than October 1, 2024.
* Updated `gpt-35-turbo` & `gpt-35-turbo-16k`0613 retirement date to October 1, 2024.
* Updated `gpt-4` & `gpt-4-32k` 0314 deprecation date to October 1, 2024, and retirement date to June 6, 2025.  

Refer to our [model retirement guide](./concepts/model-retirements.md) for the latest information on model deprecation and retirement.

### Token based billing for fine-tuning

* Azure OpenAI fine-tuning billing is now based on the number of tokens in your training file – instead of the total elapsed training time. This can result in a significant cost reduction for some training runs, and makes estimating fine-tuning costs much easier. To learn more, you can consult the [official announcement](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/pricing-update-token-based-billing-for-fine-tuning-training/ba-p/4164465).

### GPT-4o released in new regions

* GPT-4o is now also available in:
    -  Sweden Central for standard regional deployment.
    -  Australia East, Canada East, Japan East, Korea Central, Sweden Central, Switzerland North, & West US 3 for provisioned deployment.

For the latest information on model availability, see the [models page](./concepts/models.md).

### Customer-managed key (CMK) support for Assistants

Threads and Files in Assistants now supports CMK in the following region:
* West US 3

## May 2024

### GPT-4o provisioned deployments

`gpt-4o` Version: `2024-05-13` is available for both standard and provisioned deployments. Provisioned and standard model deployments accept both text and image/vision inference requests.
For information on model regional availability, consult the model matrix for [provisioned deployments](./concepts/models.md#provisioned-deployment-model-availability).

### Assistants v2 (preview)

A refresh of the Assistants API is now publicly available. It contains the following updates:

* [File search tool and vector storage](https://go.microsoft.com/fwlink/?linkid=2272425)
* [Max completion and max prompt token support](./concepts/assistants.md) for managing token usage.
* `tool_choice` [parameter](./assistants-reference-runs.md#run-object) for forcing the Assistant to use a specified tool. 
You can now create messages with the [assistant](.//assistants-reference-messages.md#create-message) role to create custom conversation histories in Threads.
* Support for `temperature`, `top_p`, `response_format` [parameters](./assistants-reference.md#create-an-assistant).
* Streaming and polling support. You can use the helper functions in our Python SDK to create runs and stream responses. We have also added polling SDK helpers to share object status updates without the need for polling. 
* Experiment with [Logic Apps and Function Calling using Azure OpenAI Studio](./how-to/assistants-logic-apps.md). Import your REST APIs implemented in Logic Apps as functions and the studio invokes the function (as a Logic Apps workflow) automatically based on the user prompt.
* AutoGen by Microsoft Research provides a multi-agent conversation framework to enable convenient building of Large Language Model (LLM) workflows across a wide range of applications. Azure OpenAI assistants are now integrated into AutoGen via `GPTAssistantAgent`, a new experimental agent that lets you seamlessly add Assistants into AutoGen-based multi-agent workflows. This enables multiple Azure OpenAI assistants that could be task or domain specialized to collaborate and tackle complex tasks.
* Support for fine-tuned `gpt-3.5-turbo-0125` [models](./concepts/models.md#assistants-preview) in the following regions:
    * East US 2
    * Sweden Central
* Expanded [regional support](./concepts/models.md#assistants-preview) for:
    * Japan East
    * UK South
    * West US
    * West US 3
    * Norway east

For more information, see the [blog post](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/announcing-azure-openai-service-assistants-preview-refresh/ba-p/4143217) about assistants.

### GPT-4o model general availability (GA)

GPT-4o ("o is for "omni") is the latest model from OpenAI launched on May 13, 2024.

- GPT-4o integrates text, and images in a single model, enabling it to handle multiple data types simultaneously. This multimodal approach enhances accuracy and responsiveness in human-computer interactions.
- GPT-4o matches GPT-4 Turbo in English text and coding tasks while offering superior performance in non-English languages and in vision tasks, setting new benchmarks for AI capabilities.

For information on model regional availability, see the [models page](./concepts/models.md).

### Global standard deployment type (preview)

Global deployments are available in the same Azure OpenAI resources as non-global offers but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global standard provides the highest default quota for new models and eliminates the need to load balance across multiple resources.

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

### Fine-tuning updates

- GPT-4 fine-tuning is [now available in public preview](./concepts/models.md#fine-tuning-models).
- Added support for [seed](/azure/ai-services/openai/tutorials/fine-tune?tabs=python-new%2Ccommand-line#begin-fine-tuning), [events](/azure/ai-services/openai/tutorials/fine-tune?tabs=python-new%2Ccommand-line#list-fine-tuning-events), [full validation statistics](/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-python#analyze-your-customized-model), and [checkpoints](/azure/ai-services/openai/tutorials/fine-tune?tabs=python-new%2Ccommand-line#list-checkpoints) as part of the `2024-05-01-preview` API release.

### DALL-E and GPT-4 Turbo Vision GA configurable content filters

Create custom content filters for your DALL-E 2 and 3, GPT-4 Turbo with Vision GA (`turbo-2024-04-09`), and GPT-4o deployments. [Content filtering](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cpython-new#configurability-preview)

### Asynchronous Filter available for all Azure OpenAI customers

Running filters asynchronously for improved latency in streaming scenarios is now available for all Azure OpenAI customers. [Content filtering](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cpython-new#content-streaming)

### Prompt Shields

Prompt Shields protect applications powered by Azure OpenAI models from two types of attacks: direct (jailbreak) and indirect attacks. Indirect Attacks (also known as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks) are a type of attack on systems powered by Generative AI models that might occur when an application processes information that wasn’t directly authored by either the developer of the application or the user. [Content filtering](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cpython-new#prompt-shields)

### 2024-05-01-preview API release

- For more information, see the [API version lifecycle](./api-version-deprecation.md).

### GPT-4 Turbo model general availability (GA)

[!INCLUDE [GPT-4 Turbo](./includes/gpt-4-turbo.md)]

## April 2024

### Fine-tuning is now supported in two new regions East US 2 and Switzerland West

Fine-tuning is now available with support for:

### East US 2

- `gpt-35-turbo` (0613)
- `gpt-35-turbo` (1106)
- `gpt-35-turbo` (0125)

### Switzerland West

- `babbage-002`
- `davinci-002`
- `gpt-35-turbo` (0613)
- `gpt-35-turbo` (1106)
- `gpt-35-turbo` (0125)

Check the [models page](concepts/models.md#fine-tuning-models), for the latest information on model availability and fine-tuning support in each region.  

### Multi-turn chat training examples

Fine-tuning now supports [multi-turn chat training examples](./how-to/fine-tuning.md#multi-turn-chat-file-format).

### GPT-4 (0125) is available for Azure OpenAI On Your Data

You can now use the GPT-4 (0125) model in [available regions](./concepts/models.md#chat-completions-1) with Azure OpenAI On Your Data.

## March 2024

### Risks & Safety monitoring in Azure OpenAI Studio

Azure OpenAI Studio now provides a Risks & Safety dashboard for each of your deployments that uses a content filter configuration. Use it to check the results of the filtering activity. Then you can adjust your filter configuration to better serve your business needs and meet Responsible AI principles.

[Use Risks & Safety monitoring](./how-to/risks-safety-monitor.md)

### Azure OpenAI On Your Data updates

- You can now connect to an Elasticsearch vector database to be used with [Azure OpenAI On Your Data](./concepts/use-your-data.md?tabs=elasticsearch#supported-data-sources).
- You can use the [chunk size parameter](./concepts/use-your-data.md#chunk-size-preview) during data ingestion to set the maximum number of tokens of any given chunk of data in your index.

### 2024-02-01 general availability (GA) API released

This is the latest GA API release and is the replacement for the previous `2023-05-15` GA release. This release adds support for the latest Azure OpenAI GA features like Whisper, DALLE-3, fine-tuning, on your data, and more.

Features that are in preview such as Assistants, text to speech (TTS), and some of the "on your data" datasources, require a preview API version. For more information, check out our [API version lifecycle guide](./api-version-deprecation.md).

### Whisper general availability (GA)

The Whisper speech to text model is now GA for both REST and Python. Client library SDKs are currently still in public preview.

Try out Whisper by following a [quickstart](./whisper-quickstart.md).

### DALL-E 3 general availability (GA)

DALL-E 3 image generation model is now GA for both REST and Python. Client library SDKs are currently still in public preview.

Try out DALL-E 3 by following a [quickstart](./dall-e-quickstart.md).

### New regional support for DALL-E 3

You can now access DALL-E 3 with an Azure OpenAI resource in the `East US` or `AustraliaEast` Azure region, in addition to `SwedenCentral`.

### Model deprecations and retirements

We have added a page to track [model deprecations and retirements](./concepts/model-retirements.md) in Azure OpenAI. This page provides information about the models that are currently available, deprecated, and retired.

### 2024-03-01-preview API released

`2024-03-01-preview` has all the same functionality as `2024-02-15-preview` and adds two new parameters for embeddings:

- `encoding_format` allows you to specify the format to generate embeddings in `float`, or `base64`. The default is `float`.
- `dimensions` allows you set the number of output embeddings. This parameter is only supported with the new third generation embeddings models: `text-embedding-3-large`, `text-embedding-3-small`. Typically larger embeddings are more expensive from a compute, memory, and storage perspective. Being able to adjust the number of dimensions allows more control over overall cost and performance. The `dimensions` parameter isn't supported in all versions of the OpenAI 1.x Python library, to take advantage of this parameter  we recommend upgrading to the latest version: `pip install openai --upgrade`.

If you're currently using a preview API version to take advantage of the latest features, we recommend consulting the [API version lifecycle](./api-version-deprecation.md) article to track how long your current API version will be supported.

### Update to GPT-4-1106-Preview upgrade plans

The deployment upgrade of `gpt-4` 1106-Preview to `gpt-4` 0125-Preview scheduled for March 8, 2024 is no longer taking place. Deployments of `gpt-4` versions 1106-Preview and 0125-Preview set to "Auto-update to default" and "Upgrade when expired" will start to be upgraded after a stable version of the model is released.  

For more information on the upgrade process refer to the [models page](./concepts/models.md).

## February 2024

### GPT-3.5-turbo-0125 model available

This model has various improvements, including higher accuracy at responding in requested formats and a fix for a bug which caused a text encoding issue for non-English language function calls.

For information on model regional availability and upgrades refer to the [models page](./concepts/models.md).

### Third generation embeddings models available

- `text-embedding-3-large`
- `text-embedding-3-small`

In testing, OpenAI reports both the large and small third generation embeddings models offer better average multi-language retrieval performance with the [MIRACL](https://github.com/project-miracl/miracl) benchmark while still maintaining better performance for English tasks with the [MTEB](https://github.com/embeddings-benchmark/mteb) benchmark than the second generation text-embedding-ada-002 model.

For information on model regional availability and upgrades refer to the [models page](./concepts/models.md).

### GPT-3.5 Turbo quota consolidation

To simplify migration between different versions of the GPT-3.5-Turbo models (including 16k), we'll be consolidating all GPT-3.5-Turbo quota into a single quota value.

- Any customers who have increased quota approved will have combined total quota that reflects the previous increases.

- Any customer whose current total usage across model versions is less than the default will get a new combined total quota by default.

### GPT-4-0125-preview model available

The `gpt-4` model version `0125-preview` is now available on Azure OpenAI in the East US, North Central US, and South Central US regions.  Customers with deployments of `gpt-4` version `1106-preview` will be automatically upgraded to `0125-preview` in the coming weeks.  

For information on model regional availability and upgrades refer to the [models page](./concepts/models.md).

### Assistants API public preview

Azure OpenAI now supports the API that powers OpenAI's GPTs. Azure OpenAI Assistants (Preview) allows you to create AI assistants tailored to your needs through custom instructions and advanced tools like code interpreter, and custom functions. To learn more, see:

- [Quickstart](./assistants-quickstart.md)
- [Concepts](./concepts/assistants.md)
- [In-depth Python how-to](./how-to/assistant.md)
- [Code Interpreter](./how-to/code-interpreter.md)
- [Function calling](./how-to/assistant-functions.md)
- [Assistants model & region availability](./concepts/models.md#assistants-preview)
- [Assistants Python & REST reference](./assistants-reference.md)
- [Assistants Samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)

### OpenAI text to speech voices public preview

Azure OpenAI now supports text to speech APIs with OpenAI's voices. Get AI-generated speech from the text you provide. To learn more, see the [overview guide](../speech-service/openai-voices.md) and try the [quickstart](./text-to-speech-quickstart.md).

> [!NOTE]
> Azure AI Speech also supports OpenAI text to speech voices. To learn more, see [OpenAI text to speech voices via Azure OpenAI or via Azure AI Speech](../speech-service/openai-voices.md#openai-text-to-speech-voices-via-azure-openai-service-or-via-azure-ai-speech) guide.

### New Fine-tuning capabilities and model support

- [Continuous fine-tuning](https://aka.ms/oai/fine-tuning-continuous)
- [Fine-tuning & function calling](./how-to/fine-tuning-functions.md)
- [`gpt-35-turbo 1106` support](./concepts/models.md#fine-tuning-models)

### New regional support for Azure OpenAI On Your Data

You can now use Azure OpenAI On Your Data in the following Azure region:
* South Africa North

### Azure OpenAI On Your Data general availability

- [Azure OpenAI On Your Data](./concepts/use-your-data.md) is now generally available.

## December 2023

### Azure OpenAI On Your Data

- Full VPN and private endpoint support for Azure OpenAI On Your Data, including security support for: storage accounts, Azure OpenAI resources, and Azure AI Search service resources.   
- New article for using [Azure OpenAI On Your Data configuration](./how-to/on-your-data-configuration.md) by protecting data with virtual networks and private endpoints.

### GPT-4 Turbo with Vision now available

GPT-4 Turbo with Vision on Azure OpenAI service is now in public preview. GPT-4 Turbo with Vision is a large multimodal model (LMM) developed by OpenAI that can analyze images and provide textual responses to questions about them. It incorporates both natural language processing and visual understanding. With enhanced mode, you can use the [Azure AI Vision](/azure/ai-services/computer-vision/overview) features to generate additional insights from the images.

- Explore the capabilities of GPT-4 Turbo with Vision in a no-code experience using the [Azure OpenAI Playground](https://oai.azure.com/). Learn more in the [Quickstart guide](./gpt-v-quickstart.md).
- Vision enhancement using GPT-4 Turbo with Vision is now available in the [Azure OpenAI Playground](https://oai.azure.com/) and includes support for Optical Character Recognition, object grounding, image support for "add your data," and support for video prompt.
- Make calls to the chat API directly using the [REST API](https://aka.ms/gpt-v-api-ref).
- Region availability is currently limited to `SwitzerlandNorth`, `SwedenCentral`, `WestUS`, and `AustraliaEast`  
- Learn more about the known limitations of GPT-4 Turbo with Vision and other [frequently asked questions](/azure/ai-services/openai/faq#gpt-4-with-vision).

## November 2023

### New data source support in Azure OpenAI On Your Data

- You can now use [Azure Cosmos DB for MongoDB vCore](./concepts/use-your-data.md#supported-data-sources) and URLs/web addresses as data sources to ingest your data and chat with a supported Azure OpenAI model.

### GPT-4 Turbo Preview & GPT-3.5-Turbo-1106 released

Both models are the latest release from OpenAI with improved instruction following, [JSON mode](./how-to/json-mode.md), [reproducible output](./how-to/reproducible-output.md), and parallel function calling.

- **GPT-4 Turbo Preview** has a max context window of 128,000 tokens and can generate 4,096 output tokens. It has the latest training data with knowledge up to April 2023. This model is in preview and isn't recommended for production use. All deployments of this preview model will be automatically updated in place once the stable release becomes available.

- **GPT-3.5-Turbo-1106** has a max context window of 16,385 tokens and can generate 4,096 output tokens.

For information on model regional availability consult the [models page](./concepts/models.md).

The models have their own unique per region [quota allocations](./quotas-limits.md).

### DALL-E 3 public preview

DALL-E 3 is the latest image generation model from OpenAI. It features enhanced image quality, more complex scenes, and improved performance when rendering text in images. It also comes with more aspect ratio options. DALL-E 3 is available through OpenAI Studio and through the REST API. Your OpenAI resource must be in the `SwedenCentral` Azure region.

DALL-E 3 includes built-in prompt rewriting to enhance images, reduce bias, and increase natural variation.

Try out DALL-E 3 by following a [quickstart](./dall-e-quickstart.md).

### Responsible AI

- **Expanded customer configurability**: All Azure OpenAI customers can now configure all severity levels (low, medium, high) for the categories hate, violence, sexual and self-harm, including filtering only high severity content. [Configure content filters](./how-to/content-filters.md)

- **Content Credentials in all DALL-E models**: AI-generated images from all DALL-E models now include a digital credential that discloses the content as AI-generated. Applications that display image assets can leverage the open source [Content Authenticity Initiative SDK](https://opensource.contentauthenticity.org/docs/js-sdk/getting-started/quick-start/) to display credentials in their AI generated images. [Content Credentials in Azure OpenAI](/azure/ai-services/openai/concepts/content-credentials)

- **New RAI models**
    
    - **Jailbreak risk detection**: Jailbreak attacks are user prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or to break the rules set in the System Message. The jailbreak risk detection model is optional (default off), and available in annotate and filter model. It runs on user prompts.
    - **Protected material text**: Protected material text describes known text content (for example, song lyrics, articles, recipes, and selected web content) that can be outputted by large language models. The protected material text model is optional (default off), and available in annotate and filter model. It runs on LLM completions.
    - **Protected material code**: Protected material code describes source code that matches a set of source code from public repositories, which can be outputted by large language models without proper citation of source repositories. The protected material code model is optional (default off), and available in annotate and filter model. It runs on LLM completions.

    [Configure content filters](./how-to/content-filters.md)

- **Blocklists**: Customers can now quickly customize content filter behavior for prompts and completions further by creating a custom blocklist in their filters. The custom blocklist allows the filter to take action on a customized list of patterns, such as specific terms or regex patterns. In addition to custom blocklists, we provide a Microsoft profanity blocklist (English). [Use blocklists](./how-to/use-blocklists.md)
## October 2023

### New fine-tuning models (preview)

- `gpt-35-turbo-0613` is [now available for fine-tuning](./how-to/fine-tuning.md).

- `babbage-002` and `davinci-002` are [now available for fine-tuning](./how-to/fine-tuning.md). These models replace the legacy ada, babbage, curie, and davinci base models that were previously available for fine-tuning.

- Fine-tuning availability is limited to certain regions. Check the [models page](concepts/models.md#fine-tuning-models), for the latest information on model availability in each region.

- Fine-tuned models have different [quota limits](quotas-limits.md) than regular models.

- [Tutorial: fine-tuning GPT-3.5-Turbo](./tutorials/fine-tune.md)

### Azure OpenAI On Your Data

- New [custom parameters](./concepts/use-your-data.md#runtime-parameters) for determining the number of retrieved documents and strictness.
    - The strictness setting sets the threshold to categorize documents as relevant to your queries.
    - The retrieved documents setting specifies the number of top-scoring documents from your data index used to generate responses.
- You can see data ingestion/upload status in the Azure OpenAI Studio.
- Support for private endpoints & VPNs for blob containers.

## September 2023

### GPT-4
GPT-4 and GPT-4-32k are now available to all Azure OpenAI customers. Customers no longer need to apply for the waitlist to use GPT-4 and GPT-4-32k (the Limited Access registration requirements continue to apply for all Azure OpenAI models). Availability might vary by region. Check the [models page](concepts/models.md), for the latest information on model availability in each region.

### GPT-3.5 Turbo Instruct

Azure OpenAI now supports the GPT-3.5 Turbo Instruct model. This model has performance comparable to `text-davinci-003` and is available to use with the Completions API. Check the [models page](concepts/models.md), for the latest information on model availability in each region.

### Whisper public preview

Azure OpenAI now supports speech to text APIs powered by OpenAI's Whisper model. Get AI-generated text based on the speech audio you provide. To learn more, check out the [quickstart](./whisper-quickstart.md).

> [!NOTE]
> Azure AI Speech also supports OpenAI's Whisper model via the batch transcription API. To learn more, check out the [Create a batch transcription](../speech-service/batch-transcription-create.md#use-a-whisper-model) guide. Check out [What is the Whisper model?](../speech-service/whisper-overview.md) to learn more about when to use Azure AI Speech vs. Azure OpenAI.

### New Regions

- Azure OpenAI is now also available in the Sweden Central, and Switzerland North regions. Check the [models page](concepts/models.md), for the latest information on model availability in each region.

### Regional quota limits increases

- Increases to the max default quota limits for certain models and regions. Migrating workloads to [these models and regions](./quotas-limits.md) will allow you to take advantage of higher Tokens per minute (TPM).  

## August 2023

### Azure OpenAI on your own data (preview) updates

- You can now deploy Azure OpenAI On Your Data to [Power Virtual Agents](/azure/ai-services/openai/concepts/use-your-data#deploying-the-model).
- Azure OpenAI On Your Data now supports private endpoints.
- Ability to [filter access to sensitive documents](./concepts/use-your-data.md#document-level-access-control).
- [Automatically refresh your index on a schedule](./concepts/use-your-data.md#schedule-automatic-index-refreshes).
- [Vector search and semantic search options](./concepts/use-your-data.md#search-types). 
- [View your chat history in the deployed web app](./how-to/use-web-app.md#enabling-chat-history-using-cosmos-db)

## July 2023

### Support for function calling

- [Azure OpenAI now supports function calling](./how-to/function-calling.md) to enable you to work with functions in the chat completions API.

### Embedding input array increase

- Azure OpenAI now [supports arrays with up to 16 inputs](./how-to/switching-endpoints.yml#azure-openai-embeddings-multiple-input-support) per API request with text-embedding-ada-002 Version 2.

### New Regions

- Azure OpenAI is now also available in the Canada East, East US 2, Japan East, and North Central US regions. Check the [models page](concepts/models.md), for the latest information on model availability in each region.  

## June 2023

### Use Azure OpenAI on your own data (preview)

- [Azure OpenAI On Your Data](./concepts/use-your-data.md) is now available in preview, enabling you to chat with OpenAI models such as GPT-35-Turbo and GPT-4 and receive responses based on your data. 

### New versions of gpt-35-turbo and gpt-4 models

- gpt-35-turbo (version 0613)
- gpt-35-turbo-16k (version 0613)
- gpt-4 (version 0613)
- gpt-4-32k (version 0613)

### UK South

- Azure OpenAI is now available in the UK South region. Check the [models page](concepts/models.md), for the latest information on model availability in each region.  

### Content filtering & annotations (Preview)

- How to [configure content filters](how-to/content-filters.md) with Azure OpenAI.
- [Enable annotations](concepts/content-filter.md) to view content filtering category and severity information as part of your GPT based Completion and Chat Completion calls.

### Quota

- Quota provides the flexibility to actively [manage the allocation of rate limits across the deployments](how-to/quota.md) within your subscription.

## May 2023

### Java & JavaScript SDK support

- NEW Azure OpenAI preview SDKs offering support for [JavaScript](quickstart.md?tabs=command-line&pivots=programming-language-javascript) and [Java](quickstart.md?tabs=command-line&pivots=programming-language-java).

### Azure OpenAI Chat Completion General Availability (GA)

- General availability support for:
  - Chat Completion API version `2023-05-15`.
  - GPT-35-Turbo models.
  - GPT-4 model series. 
  
If you're currently using the `2023-03-15-preview` API, we recommend migrating to the GA `2023-05-15` API. If you're currently using API version `2022-12-01` this API remains GA, but doesn't include the latest Chat Completion capabilities.

> [!IMPORTANT]
> Using the current versions of the GPT-35-Turbo models with the completion endpoint remains in preview.
  
### France Central

- Azure OpenAI is now available in the France Central region. Check the [models page](concepts/models.md), for the latest information on model availability in each region.  

## April 2023

- **DALL-E 2 public preview**. Azure OpenAI now supports image generation APIs powered by OpenAI's DALL-E 2 model. Get AI-generated images based on the descriptive text you provide. To learn more, check out the [quickstart](./dall-e-quickstart.md).

- **Inactive deployments of customized models will now be deleted after 15 days; models will remain available for redeployment.** If a customized (fine-tuned) model is deployed for more than fifteen (15) days during which no completions or chat completions calls are made to it, the deployment will automatically be deleted (and no further hosting charges will be incurred for that deployment). The underlying customized model will remain available and can be redeployed at any time. To learn more check out the [how-to-article](/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-studio#deploy-a-custom-model).


## March 2023

- **GPT-4 series models are now available in preview on Azure OpenAI**. To request access, existing Azure OpenAI customers can [apply by filling out this form](https://aka.ms/oai/get-gpt4). These models are currently available in the East US and South Central US regions.

- **New Chat Completion API for GPT-35-Turbo and GPT-4 models released in preview on 3/21**. To learn more, check out the [updated quickstarts](./quickstart.md) and [how-to article](./how-to/chatgpt.md).

- **GPT-35-Turbo preview**. To learn more, check out the [how-to article](./how-to/chatgpt.md).

- Increased training limits for fine-tuning: The max training job size (tokens in training file) x (# of epochs) is 2 Billion tokens for all models. We have also increased the max training job from 120 to 720 hours. 
- Adding additional use cases to your existing access.  Previously, the process for adding new use cases required customers to reapply to the service. Now, we're releasing a new process that allows you to quickly add new use cases to your use of the service. This process follows the established Limited Access process within Azure AI services. [Existing customers can attest to any and all new use cases here](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUM003VEJPRjRSOTZBRVZBV1E5N1lWMk1XUyQlQCN0PWcu). Please note that this is required anytime you would like to use the service for a new use case you didn't originally apply for.

## February 2023

### New Features

- .NET SDK(inference) [preview release](https://www.nuget.org/packages/Azure.AI.OpenAI/1.0.0-beta.3) | [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)
- [Terraform SDK update](https://registry.terraform.io/providers/hashicorp/azurerm/3.37.0/docs/resources/cognitive_deployment) to support Azure OpenAI management operations.
- Inserting text at the end of a completion is now supported with the `suffix` parameter.

### Updates

- Content filtering is on by default.

New articles on:

- [Monitoring an Azure OpenAI](./how-to/monitoring.md)
- [Plan and manage costs for Azure OpenAI](./how-to/manage-costs.md)

New training course:

- [Intro to Azure OpenAI](/training/modules/explore-azure-openai/)


## January 2023

### New Features

* **Service GA**. Azure OpenAI is now generally available.​

* **New models**: Addition of the latest text model, text-davinci-003 (East US, West Europe), text-ada-embeddings-002 (East US, South Central US, West Europe)


## December 2022

### New features

* **The latest models from OpenAI.** Azure OpenAI provides access to all the latest models including the GPT-3.5 series​.

* **New API version (2022-12-01).** This update includes several requested enhancements including token usage information in the API response, improved error messages for files, alignment with OpenAI on fine-tuning creation data structure, and support for the suffix parameter to allow custom naming of fine-tuned jobs.  ​

* **Higher request per second limits.** 50 for non-Davinci models. 20 for Davinci models.​

* **Faster fine-tune deployments.** Deploy an Ada and Curie fine-tuned models in under 10 minutes.​

* **Higher training limits:** 40M training tokens for Ada, Babbage, and Curie. 10M for Davinci.​

* **Process for requesting modifications to the abuse & miss-use data logging & human review.** Today, the service logs request/response data for the purposes of abuse and misuse detection to ensure that these powerful models aren't abused. However, many customers have strict data privacy and security requirements that require greater control over their data. To support these use cases, we're releasing a new process for customers to modify the content filtering policies or turn off the abuse logging for low-risk use cases. This process follows the established Limited Access process within Azure AI services and [existing OpenAI customers can apply here](https://aka.ms/oai/modifiedaccess).​

* **Customer managed key (CMK) encryption.** CMK provides customers greater control over managing their data in Azure OpenAI by providing their own encryption keys used for storing training data and customized models. Customer-managed keys (CMK), also known as bring your own key (BYOK), offer greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data. [Learn more from our encryption at rest documentation](encrypt-data-at-rest.md).

* **Lockbox support**​

* **SOC-2 compliance**​

* **Logging and diagnostics** through Azure Resource Health, Cost Analysis, and Metrics & Diagnostic settings​.

* **Studio improvements.** Numerous usability improvements to the Studio workflow including Azure AD role support to control who in the team has access to create fine-tuned models and deploy.

### Changes (breaking)

**Fine-tuning** create API request has been updated to match OpenAI’s schema.

**Preview API versions:**

```json
{​
    "training_file": "file-XGinujblHPwGLSztz8cPS8XY",​
    "hyperparams": { ​
        "batch_size": 4,​
        "learning_rate_multiplier": 0.1,​
        "n_epochs": 4,​
        "prompt_loss_weight": 0.1,​
    }​
}
```

**API version 2022-12-01:**

```json
{​
    "training_file": "file-XGinujblHPwGLSztz8cPS8XY",​
    "batch_size": 4,​
    "learning_rate_multiplier": 0.1,​
    "n_epochs": 4,​
    "prompt_loss_weight": 0.1,​
}
```

**Content filtering is temporarily off** by default. Azure content moderation works differently than Azure OpenAI. Azure OpenAI runs content filters during the generation call to detect harmful or abusive content and filters them from the response. [Learn More​](./concepts/content-filter.md)

​These models will be re-enabled in Q1 2023 and be on by default. ​

​**Customer actions**​

* [Contact Azure Support](https://portal.azure.com/#view/Microsoft_Azure_Support/HelpAndSupportBlade/~/overview) if you would like these turned on for your subscription​.
* [Apply for filtering modifications](https://aka.ms/oai/modifiedaccess), if you would like to have them remain off. (This option will be for low-risk use cases only.)​

## Next steps

Learn more about the [underlying models that power Azure OpenAI](./concepts/models.md).
