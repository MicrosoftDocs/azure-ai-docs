---
title: Azure OpenAI in Azure AI Foundry Models
titleSuffix: Azure OpenAI
description: Learn about the different model capabilities that are available with Azure OpenAI.
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder#
manager: nitinme
ms.date: 06/16/2025
ms.service: azure-ai-openai
ms.topic: conceptual
ms.custom:
  - references_regions
  - build-2023
  - build-2023-dataai
  - refefences_regions
  - build-2025
---

# Azure OpenAI in Azure AI Foundry Models

Azure OpenAI is powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. For Azure Government model availability, please refer to [Azure Government OpenAI Service](../azure-government.md).

| Models | Description |
|--|--|
| [codex-mini](#o-series-models) | Fine-tuned version of o4-mini. |  
| [GPT-4.1 series](#gpt-41-series) | Latest model release from Azure OpenAI |
| [model-router](#model-router) | A model that intelligently selects from a set of underlying chat models to respond to a given prompt. |
| [computer-use-preview](#computer-use-preview) | An experimental model trained for use with the Responses API computer use tool. |
| [GPT-4.5 Preview](#gpt-45-preview) |The latest GPT model that excels at diverse text and image tasks.  |
| [o-series models](#o-series-models) |[Reasoning models](../how-to/reasoning.md) with advanced problem-solving and increased focus and capability.  |
| [GPT-4o & GPT-4o mini & GPT-4 Turbo](#gpt-4o-and-gpt-4-turbo) | The latest most capable Azure OpenAI models with multimodal versions, which can accept both text and images as input. |
| [GPT-4](#gpt-4) | A set of models that improve on GPT-3.5 and can understand and generate natural language and code. |
| [GPT-3.5](#gpt-35) | A set of models that improve on GPT-3 and can understand and generate natural language and code. |
| [Embeddings](#embeddings-models) | A set of models that can convert text into numerical vector form to facilitate text similarity. |
| [Image generation](#image-generation-models) | A series of models that can generate original images from natural language. |
| [Audio](#audio-models) | A series of models for speech to text, translation, and text to speech. GPT-4o audio models support either low-latency, "speech in, speech out" conversational interactions or audio generation. |

## GPT 4.1 series

### Region availability

| Model | Region |
|---|---|
| `gpt-4.1` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability). |
| `gpt-4.1-nano` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-4.1-mini` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability).|

### Capabilities

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-4.1` (2025-04-14)   | - Text & image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> Structured outputs (chat completions)   | - 1,047,576 <br> - 128,000 (provisioned managed deployments) | 32,768 | May 31, 2024 |
| `gpt-4.1-nano` (2025-04-14) | - Text & image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> Structured outputs (chat completions)   | - 1,047,576  <br> - 128,000 (provisioned managed deployments)  | 32,768 | May 31, 2024 |
| `gpt-4.1-mini` (2025-04-14) | - Text & image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> Structured outputs (chat completions)   | - 1,047,576  <br> - 128,000 (provisioned managed deployments)  | 32,768 | May 31, 2024 |

## model-router

A model that intelligently selects from a set of underlying chat models to respond to a given prompt.

### Region availability

| Model | Region |
|---|---|
| `model-router` (2025-05-19) | East US 2 (Global Standard), Sweden Central (Global Standard)|

### Capabilities 

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `model-router` (2025-05-19) | A model that intelligently selects from a set of underlying chat models to respond to a given prompt. | 200,000* | 32768 (GPT 4.1 series)</br> 100 K (o4-mini) | May 31, 2024 |

*Larger context windows are compatible with _some_ of the underlying models, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model, otherwise the call will fail.

## computer-use-preview

An experimental model trained for use with the [Responses API](../how-to/responses.md) computer use tool. It can be used in conjunction with 3rd-party libraries to allow the model to control mouse & keyboard input while getting context from screenshots of the current environment.

> [!CAUTION]
> We don't recommend using preview models in production. We will upgrade all deployments of preview models to either future preview versions or to the latest stable GA version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

### Availability

**For access to `computer-use-preview` registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who have access to other limited access models will still need to request access for this model.

Request access: [`computer-use-preview` limited access model application](https://aka.ms/oai/cuaaccess)

Once access has been granted, you will need to create a deployment for the model.

### Region availability

| Model | Region |
|---|---|
| `computer-use-preview` |  See the [models table](#model-summary-table-and-region-availability). |

### Capabilities

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `computer-use-preview` (2025-03-11)  | Specialized model for use with the [Responses API](../how-to/responses.md) computer use tool <br> <br>-Tools <br>-Streaming<br>-Text(input/output)<br>- Image(input)   | 8,192 | 1,024 | Oct 2023 |


## GPT-4.5 Preview

### Region availability

| Model | Region |
|---|---|
| `gpt-4.5-preview` |  See the [models table](#model-summary-table-and-region-availability).|

### Capabilities

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-4.5-preview` (2025-02-27) <br> **GPT-4.5 Preview**  | [GPT 4.1](#gpt-41-series) is the recommended replacement for this model. Excels at diverse text and image tasks. <br>- Structured outputs <br>- Prompt caching <br>- Tools <br>- Streaming<br>- Text(input/output)<br>- Image(input)   | 128,000 | 16,384 | Oct 2023 |

> [!NOTE]
> It is expected behavior that the model cannot answer questions about itself. If you want to know when the knowledge cutoff for the model's training data is, or other details about the model you should refer to the model documentation above.

## o-series models

The Azure OpenAI o<sup>&#42;</sup> series models are specifically designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|  --- |  :--- |:--- |:---: |
| `codex-mini` (2025-05-16) | Fine-tuned version of o4-mini. <br> - [Responses API](../how-to/responses.md) <br>- Structured outputs<br> - Text, image processing <br> - Functions/Tools<br> [Full summary of capabilities](../how-to/reasoning.md) | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o3-pro` (2025-06-10) | - [Responses API](../how-to/responses.md) <br>- Structured outputs<br> - Text, image processing <br> - Functions/Tools<br> [Full summary of capabilities](../how-to/reasoning.md) | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o4-mini` (2025-04-16) | - **NEW** reasoning model, offering [enhanced reasoning abilities](../how-to/reasoning.md). <br><br> - Chat Completions API <br> - [Responses API](../how-to/responses.md) <br>- Structured outputs<br> - Text, image processing <br> - Functions/Tools<br> [Full summary of capabilities](../how-to/reasoning.md) | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |   
| `o3` (2025-04-16) | - **NEW** reasoning model, offering [enhanced reasoning abilities](../how-to/reasoning.md). <br>  <br> - Chat Completions API <br> - [Responses API](../how-to/responses.md) <br> - Structured outputs<br> - Text, image processing <br> - Functions/Tools/Parallel tool calling <br> [Full summary of capabilities](../how-to/reasoning.md) | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |    
| `o3-mini` (2025-01-31) | - [Enhanced reasoning abilities](../how-to/reasoning.md). <br> - Structured outputs<br> - Text-only processing <br> - Functions/Tools | Input: 200,000 <br> Output: 100,000 | Oct 2023 |  
| `o1` (2024-12-17) | - [Enhanced reasoning abilities](../how-to/reasoning.md). <br> - Structured outputs<br> - Text, image processing <br> - Functions/Tools | Input: 200,000 <br> Output: 100,000 | Oct 2023 |  
|`o1-preview` (2024-09-12) | Older preview version | Input: 128,000  <br> Output: 32,768 | Oct 2023 |
| `o1-mini` (2024-09-12) | A faster and more cost-efficient option in the o1 series, ideal for coding tasks requiring speed and lower resource consumption. <br><br> Global standard deployment available by default. <br> <br> Standard (regional) deployments are currently only available for select customers who received access as part of the `o1-preview` limited access release.  | Input: 128,000  <br> Output: 65,536 | Oct 2023 |

### Availability

To learn more about the advanced `o-series` models see, [getting started with reasoning models](../how-to/reasoning.md).

### Region availability

| Model | Region |
|---|---|
|`codex-mini` | East US2 & Sweden Central (Global Standard)   |
|`o3-pro`   | East US2 & Sweden Central (Global Standard)    |
|`o4-mini`|   See the [models table](#model-summary-table-and-region-availability).  |
| `o3` |   See the [models table](#model-summary-table-and-region-availability).  |
|`o3-mini` | See the [models table](#model-summary-table-and-region-availability). |
|`o1` | See the [models table](#model-summary-table-and-region-availability). |
| `o1-preview` | See the [models table](#model-summary-table-and-region-availability). This model is only available for customers who were granted access as part of the original limited access |
| `o1-mini` | See the [models table](#model-summary-table-and-region-availability). |

## GPT-4o and GPT-4 Turbo

GPT-4o integrates text and images in a single model, enabling it to handle multiple data types simultaneously. This multimodal approach enhances accuracy and responsiveness in human-computer interactions. GPT-4o matches GPT-4 Turbo in English text and coding tasks while offering superior performance in non-English languages and vision tasks, setting new benchmarks for AI capabilities.

### How do I access the GPT-4o and GPT-4o mini models?

GPT-4o and GPT-4o mini are available for **standard** and **global-standard** model deployment.

You need to [create](../how-to/create-resource.md) or use an existing resource in a [supported standard](#gpt-4-and-gpt-4-turbo-model-availability) or [global standard](#global-standard-model-availability) region where the model is available.

When your resource is created, you can [deploy](../how-to/create-resource.md#deploy-a-model) the GPT-4o models. If you are performing a programmatic deployment, the **model** names are:

- `gpt-4o` **Version** `2024-11-20`
- `gpt-4o` **Version** `2024-08-06`
- `gpt-4o` **Version** `2024-05-13`
- `gpt-4o-mini` **Version** `2024-07-18`

### GPT-4 Turbo

GPT-4 Turbo is a large multimodal model (accepting text or image inputs and generating text) that can solve difficult problems with greater accuracy than any of OpenAI's previous models. Like GPT-3.5 Turbo, and older GPT-4 models GPT-4 Turbo is optimized for chat and works well for traditional completions tasks.

## GPT-4

GPT-4 is the predecessor to GPT-4 Turbo. Both the GPT-4 and GPT-4 Turbo models have a base model name of `gpt-4`. You can distinguish between the GPT-4 and Turbo models by examining the model version.

- `gpt-4` **Version** `0314`
- `gpt-4` **Version** `0613`
- `gpt-4-32k` **Version** `0613`

You can see the token context length supported by each model in the [model summary table](#model-summary-table-and-region-availability).

## GPT-4 and GPT-4 Turbo models

- These models can only be used with the Chat Completion API.

See [model versions](../concepts/model-versions.md) to learn about how Azure OpenAI handles model version upgrades, and [working with models](../how-to/working-with-models.md) to learn how to view and configure the model version settings of your GPT-4 deployments.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|  --- |  :--- |:--- |:---: |
| `gpt-4o` (2024-11-20) <br> **GPT-4o (Omni)**  | **Latest large GA model** <br> - Structured outputs<br> - Text, image processing <br> - JSON Mode <br> - parallel function calling <br> - Enhanced accuracy and responsiveness <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision <br> - Superior performance in non-English languages and in vision tasks. <br> - **Enhanced creative writing ability** | Input: 128,000  <br> Output: 16,384 | Oct 2023 |
|`gpt-4o` (2024-08-06) <br> **GPT-4o (Omni)** | - Structured outputs<br> - Text, image processing <br> - JSON Mode <br> - parallel function calling <br> - Enhanced accuracy and responsiveness <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision <br> - Superior performance in non-English languages and in vision tasks |Input: 128,000  <br> Output: 16,384 | Oct 2023 |
|`gpt-4o-mini` (2024-07-18) <br> **GPT-4o mini** | **Latest small GA model** <br> - Fast, inexpensive, capable model ideal for replacing GPT-3.5 Turbo series models. <br> - Text, image processing <br>- JSON Mode <br> - parallel function calling | Input: 128,000 <br> Output: 16,384  | Oct 2023 |
|`gpt-4o` (2024-05-13) <br> **GPT-4o (Omni)** | Text, image processing <br> - JSON Mode <br> - parallel function calling <br> - Enhanced accuracy and responsiveness <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision <br> - Superior performance in non-English languages and in vision tasks |Input: 128,000  <br> Output: 4,096| Oct 2023 |
| `gpt-4` (turbo-2024-04-09) <br>**GPT-4 Turbo with Vision** | **New GA model** <br> - Replacement for all previous GPT-4 preview models (`vision-preview`, `1106-Preview`, `0125-Preview`). <br> - [**Feature availability**](#gpt-4o-and-gpt-4-turbo) is currently different depending on method of input, and deployment type. | Input: 128,000  <br> Output: 4,096  | Dec 2023 |
| `gpt-4-32k` (0613) | **Older GA model** <br> - Basic function calling with tools  | 32,768               | Sep 2021         |
| `gpt-4` (0613)     | **Older GA model** <br> - Basic function calling with tools | 8,192                | Sep 2021         |
| `gpt-4-32k`(0314)  | **Older GA model** <br> - [Retirement information](./model-retirements.md#current-models) | 32,768               | Sep 2021         |
| `gpt-4` (0314) | **Older GA model** <br> - [Retirement information](./model-retirements.md#current-models)  | 8,192 | Sep 2021         |

> [!CAUTION]
> We don't recommend using preview models in production. We will upgrade all deployments of preview models to either future preview versions or to the latest stable GA version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

## GPT-3.5

GPT-3.5 models can understand and generate natural language or code. The most capable and cost effective model in the GPT-3.5 family is GPT-3.5 Turbo, which has been optimized for chat and works well for traditional completions tasks as well. GPT-3.5 Turbo is available for use with the Chat Completions API. GPT-3.5 Turbo Instruct has similar capabilities to `text-davinci-003` using the Completions API instead of the Chat Completions API.  We recommend using GPT-3.5 Turbo and GPT-3.5 Turbo Instruct over [legacy GPT-3.5 and GPT-3 models](./legacy-models.md).


|  Model ID   | Description | Max Request (tokens) | Training Data (up to) |
|  --------- |:---|:------:|:----:|
| `gpt-35-turbo` (0125) **NEW** | **Latest GA Model** <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) <br> - Higher accuracy at responding in requested formats. <br> - Fix for a bug which caused a text encoding issue for non-English language function calls.  | Input: 16,385<br> Output: 4,096  | Sep 2021 |
| `gpt-35-turbo` (1106) | **Older GA Model** <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) | Input: 16,385<br> Output: 4,096 |  Sep 2021|
| `gpt-35-turbo-instruct` (0914) | **Completions endpoint only** <br> - Replacement for [legacy completions models](./legacy-models.md) | 4,097 |Sep 2021 |

To learn more about how to interact with GPT-3.5 Turbo and the Chat Completions API check out our [in-depth how-to](../how-to/chatgpt.md).

**<sup>1</sup>** This model will accept requests > 4,096 tokens. It is not recommended to exceed the 4,096 input token limit as the newer version of the model are capped at 4,096 tokens. If you encounter issues when exceeding 4,096 input tokens with this model this configuration is not officially supported.

## Embeddings

 `text-embedding-3-large` is the latest and most capable embedding model. Upgrading between embeddings models is not possible. In order to move from using `text-embedding-ada-002` to `text-embedding-3-large` you would need to generate new embeddings. 

- `text-embedding-3-large`
- `text-embedding-3-small`
- `text-embedding-ada-002`

In testing, OpenAI reports both the large and small third generation embeddings models offer better average multi-language retrieval performance with the [MIRACL](https://github.com/project-miracl/miracl) benchmark while still maintaining performance for English tasks with the [MTEB](https://github.com/embeddings-benchmark/mteb) benchmark.

|Evaluation Benchmark| `text-embedding-ada-002` | `text-embedding-3-small` |`text-embedding-3-large` |
|---|---|---|---|
| MIRACL average | 31.4 | 44.0 | 54.9 |
| MTEB average | 61.0 | 62.3 | 64.6 |

The third generation embeddings models support reducing the size of the embedding via a new `dimensions` parameter. Typically larger embeddings are more expensive from a compute, memory, and storage perspective. Being able to adjust the number of dimensions allows more control over overall cost and performance. The `dimensions` parameter is not supported in all versions of the OpenAI 1.x Python library, to take advantage of this parameter  we recommend upgrading to the latest version: `pip install openai --upgrade`.

OpenAI's MTEB benchmark testing found that even when the third generation model's dimensions are reduced to less than `text-embeddings-ada-002` 1,536 dimensions performance remains slightly better.

## Image generation models

The image generation models generate images from text prompts that the user provides. GPT-image-1 is in limited access public preview. DALL-E 3 is generally available for use with the REST APIs. DALL-E 2 and DALL-E 3 with client SDKs are in preview.

### Availability

**For access to `gpt-image-1` registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who have access to other limited access models will still need to request access for this model.

Request access: [`gpt-image-1` limited access model application](https://aka.ms/oai/gptimage1access)

Once access has been granted, you will need to create a deployment for the model.

### Region availability

| Model | Region |
|---|---|
|`dall-e-3` | East US<br>Australia East<br>Sweden Central|
|`gpt-image-1` | West US 3 (Global Standard) <br> UAE North (Global Standard) |


## Video generation models

Sora is an AI model from OpenAI that can create realistic and imaginative video scenes from text instructions. Sora is in public preview.



### Region availability

| Model | Region |
|---|---|
|`sora` | East US 2|

## Audio models

Audio models in Azure OpenAI are available via the `realtime`, `completions`, and `audio` APIs.

### GPT-4o audio models

The GPT 4o audio models are part of the GPT-4o model family and support either low-latency, "speech in, speech out" conversational interactions or audio generation. 

> [!CAUTION]
> We don't recommend using preview models in production. We will upgrade all deployments of preview models to either future preview versions or to the latest stable GA version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

Details about maximum request tokens and training data are available in the following table.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|---|---|---|---|
|`gpt-4o-mini-audio-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for audio and text generation. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-mini-realtime-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-audio-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for audio and text generation. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-realtime-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-mini-realtime-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |

To compare the availability of GPT-4o audio models across all regions, see the [models table](#global-standard-model-availability).

### Audio API

The audio models via the `/audio` API can be used for speech to text, translation, and text to speech. 

#### Speech to text models

|  Model ID  | Description | Max Request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |
| `gpt-4o-transcribe` | Speech to text powered by GPT-4o. | 25 MB|
| `gpt-4o-mini-transcribe` | Speech to text powered by GPT-4o mini. | 25 MB|

#### Speech translation models

|  Model ID  | Description | Max Request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |

#### Text to speech models (Preview)

|  Model ID  | Description |
|  --- | :--- |
| `tts` | Text to speech optimized for speed. |
| `tts-hd` | Text to speech optimized for quality.|
| `gpt-4o-mini-tts` | Text to speech model powered by GPT-4o mini.<br/><br/>You can guide the voice to speak in a style or tone. |

For more information see [Audio models region availability](?tabs=standard-audio#standard-deployment-regional-models-by-endpoint) in this article.

## Model summary table and region availability

### Models by deployment type

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment: 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see our [deployment types guide](../how-to/deployment-types.md).

# [Global Standard](#tab/global-standard)

### Global standard model availability

[!INCLUDE [Standard Global](../includes/model-matrix/standard-global.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for global standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time access to `o1-mini` standard (regional) deployments is not being expanded.

# [Global Provisioned Managed](#tab/global-ptum)

### Global provisioned managed model availability

[!INCLUDE [Provisioned Managed Global](../includes/model-matrix/provisioned-global.md)]

# [Global Batch](#tab/global-batch)

### Global batch model availability

[!INCLUDE [Global batch](../includes/model-matrix/global-batch.md)]

# [Data Zone Standard](#tab/datazone-standard)

### Data zone standard model availability

[!INCLUDE [Data zone standard](../includes/model-matrix/datazone-standard.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for global standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time access to `o1-mini` standard (regional) deployments is not being expanded.

# [Data Zone Provisioned Managed](#tab/datazone-provisioned-managed)

### Data zone provisioned managed model availability

[!INCLUDE [Global data zone provisioned managed](../includes/model-matrix/datazone-provisioned-managed.md)]

# [Data Zone Batch](#tab/datazone-batch)

### Data zone batch model availability

[!INCLUDE [Data zone batch](../includes/model-matrix/global-batch-datazone.md)]

# [Standard](#tab/standard)

### Standard deployment model availability

[!INCLUDE [Standard Models](../includes/model-matrix/standard-models.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for global standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time access to `o1-mini` standard (regional) deployments is not being expanded.


# [Provisioned Managed](#tab/provisioned)

### Provisioned deployment model availability

[!INCLUDE [Provisioned](../includes/model-matrix/provisioned-models.md)]

> [!NOTE]
> The provisioned version of `gpt-4` **Version:** `turbo-2024-04-09` is currently limited to text only.

For more information on Provisioned deployments, see our [Provisioned guidance](./provisioned-throughput.md).

---

This table doesn't include fine-tuning regional availability information.  Consult the [fine-tuning section](#fine-tuning-models) for this information.

### Standard deployment (regional) models by endpoint

# [Chat Completions](#tab/standard-chat-completions)

### Chat completions

[!INCLUDE [Chat Completions](../includes/model-matrix/standard-chat-completions.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for global standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time access to `o1-mini` standard (regional) deployments is not being expanded.

### GPT-4 and GPT-4 Turbo model availability

#### Select customer access

In addition to the regions above which are available to all Azure OpenAI customers, some select preexisting customers have been granted access to versions of GPT-4 in additional regions:

| Model | Region |  
|---|:---|  
| `gpt-4` (0314) <br> `gpt-4-32k` (0314) | East US <br> France Central <br> South Central US <br> UK South |  
| `gpt-4` (0613) <br> `gpt-4-32k` (0613) | East US <br> East US 2 <br> Japan East <br> UK South |  

### GPT-3.5 models

See [model versions](../concepts/model-versions.md) to learn about how Azure OpenAI handles model version upgrades, and [working with models](../how-to/working-with-models.md) to learn how to view and configure the model version settings of your GPT-3.5 Turbo deployments.

# [Embeddings](#tab/standard-embeddings)

### Embeddings models

[!INCLUDE [Embeddings](../includes/model-matrix/standard-embeddings.md)]

These models can only be used with Embedding API requests.

> [!NOTE]
> `text-embedding-3-large` is the latest and most capable embedding model. Upgrading between embedding models is not possible. In order to migrate from using `text-embedding-ada-002` to `text-embedding-3-large` you would need to generate new embeddings.  

|  Model ID | Max Request (tokens) | Output Dimensions |Training Data (up-to)
|---|---| :---:|:---:|:---:|
| `text-embedding-ada-002` (version 2) |8,192 | 1,536 | Sep 2021 |
| `text-embedding-ada-002` (version 1) |2,046 | 1,536 | Sep 2021 |
| `text-embedding-3-large` | 8,192 | 3,072 |Sep 2021 |
| `text-embedding-3-small` | 8,192|  1,536 | Sep 2021 |

> [!NOTE]
> When sending an array of inputs for embedding, the max number of input items in the array per call to the embedding endpoint is 2048.

# [Image Generation](#tab/standard-image-generations)

### Image generation models

[!INCLUDE [Image Generation](../includes/model-matrix/standard-image-generation.md)]

|  Model ID  | Max Request (characters) |
|  --- | :---: |
| gpt-image-1 | 4,000 |
| dall-e-3  | 4,000 |

# [Video Generation](#tab/standard-video-generations)

### Video generation models

| **Region**   | **sora**   |
|:-----------------|:---------------------:|
| eastus2    | ✅                  |

|  Model ID  | Max Request (characters) |
|  --- | :---: |
| sora | 4,000 |



# [Audio](#tab/standard-audio)

### Audio models

[!INCLUDE [Audio](../includes/model-matrix/standard-audio.md)]

# [Completions (Legacy)](#tab/standard-completions)

### Completions models

[!INCLUDE [Completions](../includes/model-matrix/standard-completions.md)]

---

## Fine-tuning models

[!INCLUDE [Fine-tune models](../includes/fine-tune-models.md)]

## Assistants (Preview)

For Assistants you need a combination of a supported model, and a supported region. Certain tools and capabilities require the latest models. The following models are available in the Assistants API, SDK, and Azure AI Foundry. The following table is for standard deployment. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](./provisioned-throughput.md). The listed models and regions can be used with both Assistants v1 and v2. You can use [global standard models](#global-standard-model-availability) if they are supported in the regions listed below. 


| **Region**   |  **gpt-4o**, **2024-05-13**   | **gpt-4o**, **2024-08-06**   | **gpt-4o-mini**, **2024-07-18**   | **gpt-4**, **0613**   | **gpt-4**, **1106-Preview**   | **gpt-4**, **0125-Preview**    | **gpt-4**, **turbo-2024-04-09**   | **gpt-4-32k**, **0613**  | **gpt-35-turbo**, **0613**   | **gpt-35-turbo**, **1106**   | **gpt-35-turbo**, **0125**   | **gpt-35-turbo-16k**, **0613**   |
|:-----------------|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:---------------------------:|:---------------------------:|:-------------------------------:|:-----------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:------------------------------:|
| australiaeast    | -                      | -                      | -                           | ✅                | ✅                        | -                       | -                           | ✅                    | ✅                       | ✅                       | ✅                       | ✅                           |
| eastus           | ✅                       | ✅                       | ✅                            | -               | -                       | ✅                        |  ✅                            | -                   | ✅                       | -                      | ✅                       | ✅                           |
| eastus2          | ✅                       | ✅                       | ✅                            | -               | ✅                        | -                       | ✅                            | -                   | ✅                       | -                      | ✅                       | ✅                           |
| francecentral    | -                      | -                      | -                           | ✅                | ✅                        | -                       | -                           | ✅                    | ✅                       | ✅                       | -                      | ✅                           |
| japaneast        | -                      | -                      | -                           | -               | -                       | -                       | -                           | -                   | ✅                       | -                      | ✅                       | ✅                           |
| norwayeast       | -                      | -                      | -                           | -               | ✅                        | -                       |  -                           | -                   | -                      | -                      | -                      | -                          |
| southindia       | -                      | -                      | -                           | -               | ✅                        | -                       | -                           | -                   | -                      | ✅                       | ✅                       | -                          |
| swedencentral    | ✅                       | ✅                       | ✅                            | ✅                | ✅                        | -                       | ✅                            | ✅                    | ✅                       | ✅                       | -                      | ✅                           |
| uksouth          | -                      | -                      | -                           | -               | ✅                        | ✅                        | -                           | -                   | ✅                       | ✅                       | ✅                       | ✅                           |
| westus           | ✅                       | ✅                       | ✅                            | -               | ✅                        | -                       |✅                            | -                   | -                      | ✅                       | ✅                       | -                          |
| westus3          | ✅                       | ✅                       | ✅                            | -               | ✅                        | -                       | ✅                            | -                   | -                      | -                      | ✅                       | -                          |

## Model retirement

For the latest information on model retirements, refer to the [model retirement guide](./model-retirements.md).

## Next steps

- [Model retirement and deprecation](./model-retirements.md)
- [Learn more about working with Azure OpenAI models](../how-to/working-with-models.md)
- [Learn more about Azure OpenAI](../overview.md)
- [Learn more about fine-tuning Azure OpenAI models](../how-to/fine-tuning.md)
