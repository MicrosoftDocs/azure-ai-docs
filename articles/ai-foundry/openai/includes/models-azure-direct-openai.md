---
title: Azure OpenAI in Microsoft Foundry Models
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder#
manager: nitinme
ms.date: 01/14/2026
ms.service: azure-ai-foundry
ms.topic: include
---

> [!NOTE]
> Foundry Models sold directly by Azure also include select models from top model providers, such as:
>
> - Black Forest Labs: `FLUX.2-pro`, `FLUX.1-Kontext-pro`, `FLUX-1.1-pro`
> - Cohere: `Cohere-command-a`, `embed-v-4-0`, `Cohere-rerank-v4.0-pro`, `Cohere-rerank-v4.0-fast`
> - DeepSeek: `DeepSeek-V3.2`, `DeepSeek-V3.2-Speciale`, `DeepSeek-V3.1`, `DeepSeek-V3-0324`, `DeepSeek-R1-0528`, `DeepSeek-R1`
> - Moonshot AI: `Kimi-K2.5`, `Kimi-K2-Thinking`
> - Meta: `Llama-4-Maverick-17B-128E-Instruct-FP8`, `Llama-3.3-70B-Instruct` 
> - Microsoft: `MAI-DS-R1`, `model-router`
> - Mistral: `mistral-document-ai-2505`, `Mistral-Large-3`
> - xAI: `grok-code-fast-1`, `grok-3`, `grok-3-mini`, `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning`, `grok-4`
> 
> To learn about these models, switch to [Other model collections](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-direct-others) at the top of this article. 


## Azure OpenAI in Microsoft Foundry models

[!INCLUDE [azure-open-ai-models-list](../includes/azure-openai-models-list.md)]

## GPT-5.2

### Region availability

| Model | Region |
|---|---|
| `gpt-5.2` |  See the [models table](#model-summary-table-and-region-availability).   |
| `gpt-5.2-chat` |  See the [models table](#model-summary-table-and-region-availability).  |
| `gpt-5.2-codex` | East US2 & Sweden Central (Global Standard) |

- **[Registration is required for access to gpt-5.2 and gpt-5.2-codex](https://aka.ms/oai/gpt5access).**

Access will be granted based on Microsoft's eligibility criteria. Customers who previously applied and received access to a limited access model, don't need to reapply as their approved subscriptions will automatically be granted access upon model release.

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-5.2-codex` (2026-01-14) |  - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md). <br> - Optimized for [Codex CLI & Codex VS Code extension](../how-to/codex.md)  | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | |
| `gpt-5.2` (2025-12-11) |  - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md).  | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | August 2025 |
| `gpt-5.2-chat` (2025-12-11)<br>**Preview** |  - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs <br> - Functions, tools, and parallel tool calling. |128,000 <br><br>Input: 111,616 <br> Output: 16,384  | 16,384 | August 2025 |


> [!CAUTION]
> We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.


<!-- > [!IMPORTANT]
> - `gpt-5.1` `reasoning_effort` defaults to `none`. When upgrading from previous reasoning models to `gpt-5.1`, keep in mind that you may need to update your code to explicitly pass a `reasoning_effort` level if you want reasoning to occur.
>
> - `gpt-5.1-chat` adds built-in reasoning capabilities. Like other [reasoning models](../how-to/reasoning.md) it does not support parameters like `temperature`. If you upgrade from using `gpt-5-chat` (which is not a reasoning model) to `gpt-5.1-chat` make sure you remove any custom parameters like `temperature` from your code which are not supported by reasoning models.
>
> - `gpt-5.1-codex-max` adds support for setting `reasoning_effort` to `xhigh`. Reasoning effort `none` is not supported with `gpt-5.1-codex-max`.  -->


## GPT-5.1

### Region availability

| Model | Region |
|---|---|
| `gpt-5.1` |  See the [models table](#model-summary-table-and-region-availability).   |
| `gpt-5.1-chat` |  See the [models table](#model-summary-table-and-region-availability).  |
| `gpt-5.1-codex` |  See the [models table](#model-summary-table-and-region-availability).  |
| `gpt-5.1-codex-mini` |  See the [models table](#model-summary-table-and-region-availability).  |
| `gpt-5.1-codex-max` |  See the [models table](#model-summary-table-and-region-availability).  | 


- **[Registration is required for access to gpt-5.1, gpt-5.1-codex, and gpt-5.1-codex-max](https://aka.ms/oai/gpt5access).**

Access will be granted based on Microsoft's eligibility criteria. Customers who previously applied and received access to a limited access model, don't need to reapply as their approved subscriptions will automatically be granted access upon model release.

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-5.1` (2025-11-13) |  - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md).  | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | September 30, 2024  |
| `gpt-5.1-chat` (2025-11-13) <br>**Preview** |  - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs <br> - Functions, tools, and parallel tool calling. |128,000 <br><br>Input: 111,616 <br> Output: 16,384  | 16,384 | September 30, 2024 |
| `gpt-5.1-codex` (2025-11-13) |  - [Responses API](../how-to/responses.md) only. <br> - Text and image processing  <br> - Structured outputs.  <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md)<br> - Optimized for [Codex CLI & Codex VS Code extension](../how-to/codex.md)  | 400,000<br><br>Input: 272,000<br>Output: 128,000 | 128,000 | September 30, 2024 |
| `gpt-5.1-codex-mini` (2025-11-13) |  - [Responses API](../how-to/responses.md) only. <br> - Text and image processing  <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md)<br> - Optimized for [Codex CLI & Codex VS Code extension](../how-to/codex.md)  | 400,000<br><br>Input: 272,000<br>Output: 128,000 | 128,000 | September 30, 2024 |
| `gpt-5.1-codex-max` (2025-12-04) |  - [Responses API](../how-to/responses.md) only. <br> - Text and image processing  <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md)<br> - Optimized for [Codex CLI & Codex VS Code extension](../how-to/codex.md)  | 400,000<br><br>Input: 272,000<br>Output: 128,000 | 128,000 | September 30, 2024 |

> [!CAUTION]
> We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

> [!IMPORTANT]
> - `gpt-5.1` `reasoning_effort` defaults to `none`. When upgrading from previous reasoning models to `gpt-5.1`, keep in mind that you may need to update your code to explicitly pass a `reasoning_effort` level if you want reasoning to occur.
>
> - `gpt-5.1-chat` adds built-in reasoning capabilities. Like other [reasoning models](../how-to/reasoning.md) it does not support parameters like `temperature`. If you upgrade from using `gpt-5-chat` (which is not a reasoning model) to `gpt-5.1-chat` make sure you remove any custom parameters like `temperature` from your code which are not supported by reasoning models.
>
> - `gpt-5.1-codex-max` adds support for setting `reasoning_effort` to `xhigh`. Reasoning effort `none` is not supported with `gpt-5.1-codex-max`. 

## GPT-5

### Region availability


| Model | Region |
|---|---|
| `gpt-5` (2025-08-07) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-5-mini` (2025-08-07) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-5-nano` (2025-08-07) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-5-chat` (2025-08-07) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-5-chat` (2025-10-03) |  See the [models table](#model-summary-table-and-region-availability). |
| `gpt-5-codex` (2025-09-11) |  See the [models table](#model-summary-table-and-region-availability). |
| `gpt-5-pro` (2025-10-06) |  See the [models table](#model-summary-table-and-region-availability).  |

- **[Registration is required for access to the gpt-5-pro, gpt-5, & gpt-5-codex models](https://aka.ms/oai/gpt5access).**

- `gpt-5-mini`, `gpt-5-nano`, and `gpt-5-chat` do not require registration.

 Access will be granted based on Microsoft's eligibility criteria. Customers who previously applied and received access to `o3`, don't need to reapply as their approved subscriptions will automatically be granted access upon model release.

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-5` (2025-08-07) |  - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md).  | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | September 30, 2024  |
| `gpt-5-mini` (2025-08-07) | - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md).     | 400,000<br><br>Input: 272,000<br>Output: 128,000   | 128,000  | May 31, 2024 |
| `gpt-5-nano` (2025-08-07) | - [Reasoning](../how-to/reasoning.md) <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md).     | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | May 31, 2024 |
| `gpt-5-chat` (2025-08-07)<br>**Preview** | - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - **Input**: Text/Image <br> - **Output**: Text only  | 128,000 | 16,384 | September 30, 2024 |
| `gpt-5-chat` (2025-10-03)<br>**Preview**<sup>1<sup/> | - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - **Input**: Text/Image <br> - **Output**: Text only  | 128,000 | 16,384 | September 30, 2024 |
| `gpt-5-codex` (2025-09-11) | - [Responses API](../how-to/responses.md) only. <br> - **Input**: Text/Image <br> - **Output**: Text only  <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> - [Full summary of capabilities](../how-to/reasoning.md)<br> - Optimized for [Codex CLI & Codex VS Code extension](../how-to/codex.md)  | 400,000<br><br>Input: 272,000<br>Output: 128,000 | 128,000 | - |
| `gpt-5-pro` (2025-10-06) | - [Reasoning](../how-to/reasoning.md) <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions and tools <br> - [Full summary of capabilities](../how-to/reasoning.md).  | 400,000<br><br>Input: 272,000<br>Output: 128,000  | 128,000 | September 30, 2024 |

> [!NOTE]
> <sup>1</sup> `gpt-5-chat` version `2025-10-03` introduces a significant enhancement focused on emotional intelligence and mental health capabilities. This upgrade integrates specialized datasets and refined response strategies to improve the model's ability to:
> - **Understand and interpret emotional context** more accurately, enabling nuanced and empathetic interactions.
> - **Provide supportive, responsible responses** in conversations related to mental health, ensuring sensitivity and adherence to best practices.
>
> These improvements aim to make GPT-5-chat more context-aware, human-centric, and reliable in scenarios where emotional tone and well-being considerations are critical.

> [!CAUTION]
> We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

## gpt-oss

### Region availability

| Model | Region |
|---|---|
| `gpt-oss-120b`  | All Azure OpenAI regions |

### Capabilities

|  Model ID  | Description | Context Window | Max Output Tokens | Training Data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-oss-120b` (Preview)   | - Text in/text out only <br> - Chat Completions API <br> - Streaming <br> - Function calling <br> - Structured outputs <br> - Reasoning <br> - Available for deployment<sup>1</sup> and via [managed compute](../../how-to/deploy-models-managed.md)  | 131,072 | 131,072 | May 31, 2024 |
| `gpt-oss-20b` (Preview) | - Text in/text out only <br> - Chat Completions API <br> - Streaming <br> - Function calling <br> - Structured outputs <br> - Reasoning <br> - Available via [managed compute](../../how-to/deploy-models-managed.md) and [Foundry Local](../../foundry-local/get-started.md#optional-run-the-latest-gpt-oss-20b-model) | 131,072 | 131,072 | May 31, 2024 |

<sup>1</sup> Unlike other Azure OpenAI models `gpt-oss-120b` requires a [Foundry project](/azure/ai-foundry/quickstarts/get-started-code?tabs=azure-ai-foundry) to deploy the model.

### Deploy with code

```cli
az cognitiveservices account deployment create \
  --name "Foundry-project-resource" \
  --resource-group "test-rg" \
  --deployment-name "gpt-oss-120b" \
  --model-name "gpt-oss-120b" \
  --model-version "1" \
  --model-format "OpenAI-OSS" \
  --sku-capacity 10 \
  --sku-name "GlobalStandard"
```


## GPT-4.1 series

### Region availability

| Model | Region |
|---|---|
| `gpt-4.1` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability). |
| `gpt-4.1-nano` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability).|
| `gpt-4.1-mini` (2025-04-14) |  See the [models table](#model-summary-table-and-region-availability).|

### Capabilities

> [!IMPORTANT]
> A known issue is affecting all GPT 4.1 series models. Large tool or function call definitions that exceed 300,000 tokens will result in failures, even though the 1 million token context limit of the models wasn't reached.
>
> The errors can vary based on API call and underlying payload characteristics.
>
> Here are the error messages for the Chat Completions API:
>
> - `Error code: 400 - {'error': {'message': "This model's maximum context length is 300000 tokens. However, your messages resulted in 350564 tokens (100 in the messages, 350464 in the functions). Please reduce the length of the messages or functions.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}`
>
> - `Error code: 400 - {'error': {'message': "Invalid 'tools[0].function.description': string too long. Expected a string with maximum length 1048576, but got a string with length 2778531 instead.", 'type': 'invalid_request_error', 'param': 'tools[0].function.description', 'code': 'string_above_max_length'}}`
>
> Here's the error message for the Responses API:
>
> - `Error code: 500 - {'error': {'message': 'The server had an error processing your request. Sorry about that! You can retry your request, or contact us through an Azure support request at: https://go.microsoft.com/fwlink/?linkid=2213926 if you keep seeing this error. (Please include the request ID d2008353-291d-428f-adc1-defb5d9fb109 in your email.)', 'type': 'server_error', 'param': None, 'code': None}}`

|  Model ID  | Description | Context window | Max output tokens | Training data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `gpt-4.1` (2025-04-14)   | - Text and image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> - Structured outputs (chat completions)   | - 1,047,576 <br> - 128,000 (standard & provisioned managed deployments) <br> - 300,000 (batch deployments) | 32,768 | May 31, 2024 |
| `gpt-4.1-nano` (2025-04-14) | - Text and image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> - Structured outputs (chat completions)   | - 1,047,576  <br> - 128,000 (standard & provisioned managed deployments) <br> - 300,000 (batch deployments)  | 32,768 | May 31, 2024 |
| `gpt-4.1-mini` (2025-04-14) | - Text and image input <br> - Text output <br> - Chat completions API <br>- Responses API <br> - Streaming <br> - Function calling <br> - Structured outputs (chat completions)   | - 1,047,576  <br> - 128,000 (standard & provisioned managed deployments) <br> - 300,000 (batch deployments)  | 32,768 | May 31, 2024 |

## computer-use-preview


An experimental model trained for use with the [Responses API](../how-to/responses.md) computer use tool.

It can be used with third-party libraries to allow the model to control mouse and keyboard input, while getting context from screenshots of the current environment.

> [!CAUTION]
> We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

Registration is required to access `computer-use-preview`. Access is granted based on Microsoft's eligibility criteria. Customers who have access to other limited access models still need to request access for this model.

To request access, go to [`computer-use-preview` limited access model application](https://aka.ms/oai/cuaaccess). When access is granted, you need to create a deployment for the model.

### Region availability

| Model | Region |
|---|---|
| `computer-use-preview` |  See the [models table](#model-summary-table-and-region-availability). |

### Capabilities

|  Model ID  | Description | Context window | Max output tokens | Training data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `computer-use-preview` (2025-03-11)  | Specialized model for use with the [Responses API](../how-to/responses.md) computer use tool <br> <br>- Tools <br>- Streaming<br>- Text (input/output)<br>- Image (input)   | 8,192 | 1,024 | October 2023 |

## o-series models

The Azure OpenAI o-series models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math, compared to previous iterations.

|  Model ID  | Description | Max request (tokens) | Training data (up to)  |
|  --- |  :--- |:--- |:---: |
| `codex-mini` (2025-05-16) | Fine-tuned version of `o4-mini`. <br> - [Responses API](../how-to/responses.md). <br>- Structured outputs.<br> - Text and image processing. <br> - Functions and tools.<br> [Full summary of capabilities](../how-to/reasoning.md). | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o3-pro` (2025-06-10) | - [Responses API](../how-to/responses.md). <br>- Structured outputs.<br> - Text and image processing. <br> - Functions and tools.<br> [Full summary of capabilities](../how-to/reasoning.md). | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o4-mini` (2025-04-16) | - *New* reasoning model, offering [enhanced reasoning abilities](../how-to/reasoning.md). <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br>- Structured outputs.<br> - Text and image processing. <br> - Functions and tools.<br> [Full summary of capabilities](../how-to/reasoning.md). | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o3` (2025-04-16) | - *New* reasoning model, offering [enhanced reasoning abilities](../how-to/reasoning.md). <br> - Chat Completions API. <br> - [Responses API](../how-to/responses.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions, tools, and parallel tool calling. <br> [Full summary of capabilities](../how-to/reasoning.md). | Input: 200,000 <br> Output: 100,000 | May 31, 2024 |
| `o3-mini` (2025-01-31) | - [Enhanced reasoning abilities](../how-to/reasoning.md). <br> - Structured outputs.<br> - Text-only processing. <br> - Functions and tools. | Input: 200,000 <br> Output: 100,000 | October 2023 |  
| `o1` (2024-12-17) | - [Enhanced reasoning abilities](../how-to/reasoning.md). <br> - Structured outputs.<br> - Text and image processing. <br> - Functions and tools. | Input: 200,000 <br> Output: 100,000 | October 2023 |  
|`o1-preview` (2024-09-12) | Older preview version. | Input: 128,000  <br> Output: 32,768 | October 2023 |
| `o1-mini` (2024-09-12) | A faster and more cost-efficient option in the o1 series, ideal for coding tasks that require speed and lower resource consumption. <br> - Global Standard deployment available by default. <br> - Standard (regional) deployments are currently only available for select customers who received access as part of the `o1-preview` limited access release.  | Input: 128,000  <br> Output: 65,536 | October 2023 |

To learn more about advanced o-series models, see [Getting started with reasoning models](../how-to/reasoning.md).

### Region availability

| Model | Region |
|---|---|
|`codex-mini` | East US2 & Sweden Central (Global Standard).   |
|`o3-pro`   | East US2 & Sweden Central (Global Standard).    |
|`o4-mini`|   See the [models table](#model-summary-table-and-region-availability).  |
| `o3` |   See the [models table](#model-summary-table-and-region-availability).  |
|`o3-mini` | See the [models table](#model-summary-table-and-region-availability). |
|`o1` | See the [models table](#model-summary-table-and-region-availability). |
| `o1-preview` | See the [models table](#model-summary-table-and-region-availability). This model is available only for customers who were granted access as part of the original limited access. |
| `o1-mini` | See the [models table](#model-summary-table-and-region-availability). |

## GPT-4o and GPT-4 Turbo

GPT-4o integrates text and images in a single model, which enables it to handle multiple data types simultaneously. This multimodal approach enhances accuracy and responsiveness in human-computer interactions. GPT-4o matches GPT-4 Turbo in English text and coding tasks while offering superior performance in non-English language tasks and vision tasks, setting new benchmarks for AI capabilities.

## GPT-4 and GPT-4 Turbo models

These models can be used only with the Chat Completions API.

See [Model versions](../concepts/model-versions.md) to learn about how Azure OpenAI handles model version upgrades. See [Working with models](../how-to/working-with-models.md) to learn how to view and configure the model version settings of your GPT-4 deployments.

|  Model ID  | Description | Max request (tokens) | Training data (up to)  |
|  --- |  :--- |:--- |:---: |
| `gpt-4o` (2024-11-20) <br> GPT-4o (Omni)  | - Structured outputs.<br> - Text and image processing. <br> - JSON Mode. <br> - Parallel function calling. <br> - Enhanced accuracy and responsiveness. <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision. <br> - Superior performance in non-English languages and in vision tasks. <br> - Enhanced creative writing ability. | Input: 128,000  <br> Output: 16,384 | October 2023 |
|`gpt-4o` (2024-08-06) <br> GPT-4o (Omni) | - Structured outputs.<br> - Text and image processing. <br> - JSON Mode. <br> - Parallel function calling. <br> - Enhanced accuracy and responsiveness. <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision. <br> - Superior performance in non-English languages and in vision tasks. |Input: 128,000  <br> Output: 16,384 | October 2023 |
|`gpt-4o-mini` (2024-07-18) <br> GPT-4o mini | - Fast, inexpensive, capable model ideal for replacing GPT-3.5 Turbo series models. <br> - Text and image processing. <br>- JSON Mode. <br> - Parallel function calling. | Input: 128,000 <br> Output: 16,384  | October 2023 |
|`gpt-4o` (2024-05-13) <br> GPT-4o (Omni) | - Text and image processing. <br> - JSON Mode. <br> - Parallel function calling. <br> - Enhanced accuracy and responsiveness. <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision. <br> - Superior performance in non-English languages and in vision tasks. |Input: 128,000  <br> Output: 4,096| October 2023 |
| `gpt-4` (turbo-2024-04-09) <br>GPT-4 Turbo with Vision | New generally available model. <br> - Replacement for all previous GPT-4 preview models (`vision-preview`, `1106-Preview`, `0125-Preview`). <br> - [Feature availability](#gpt-4o-and-gpt-4-turbo) is currently different, depending on the method of input and the deployment type. | Input: 128,000  <br> Output: 4,096  | December 2023 |

> [!CAUTION]
> We don't recommend that you use preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

## Embeddings

 `text-embedding-3-large` is the latest and most capable embedding model. You can't upgrade between embeddings models. To move from using `text-embedding-ada-002` to `text-embedding-3-large`, you need to generate new embeddings.

- `text-embedding-3-large`
- `text-embedding-3-small`
- `text-embedding-ada-002`

OpenAI reports that testing shows that both the large and small third generation embeddings models offer better average multi-language retrieval performance with the [MIRACL](https://github.com/project-miracl/miracl) benchmark. They still maintain performance for English tasks with the [MTEB](https://github.com/embeddings-benchmark/mteb) benchmark.

|Evaluation benchmark| `text-embedding-ada-002` | `text-embedding-3-small` |`text-embedding-3-large` |
|---|---|---|---|
| MIRACL average | 31.4 | 44.0 | 54.9 |
| MTEB average | 61.0 | 62.3 | 64.6 |

The third generation embeddings models support reducing the size of the embedding via a new `dimensions` parameter. Typically, larger embeddings are more expensive from a compute, memory, and storage perspective. When you can adjust the number of dimensions, you gain more control over overall cost and performance. The `dimensions` parameter isn't supported in all versions of the OpenAI 1.x Python library. To take advantage of this parameter, we recommend that you upgrade to the latest version: `pip install openai --upgrade`.

OpenAI's MTEB benchmark testing found that even when the third generation model's dimensions are reduced to less than the 1,536 dimensions of `text-embeddings-ada-002`, performance remains slightly better.

## Image generation models

The image generation models generate images from text prompts that the user provides. GPT-image-1 series models are in limited access preview. DALL-E 3 is generally available for use with the REST APIs. DALL-E 2 and DALL-E 3 with client SDKs are in preview.

Registration is required to access `gpt-image-1`, `gpt-image-1-mini`, or `gpt-image-1.5`. Access is granted based on Microsoft's eligibility criteria. Customers who have access to other limited access models still need to request access for this model.

To request access, fill out an application form: [Apply for GPT-image-1 access](https://aka.ms/oai/gptimage1access); [Apply for GPT-image-1.5 access](https://aka.ms/oai/gptimage1.5access). When access is granted, you need to create a deployment for the model.

### Region availability

| Model | Region |
|---|---|
|`dall-e-3` | East US<br>Australia East<br>Sweden Central|
|`gpt-image-1` | West US 3 (Global Standard) <br> East US 2 (Global Standard) <br> UAE North (Global Standard) <br> Poland Central (Global Standard)<br>Sweden Central (Global Standard)|
|`gpt-image-1-mini` | West US 3 (Global Standard) <br> East US 2 (Global Standard) <br> UAE North (Global Standard) <br> Poland Central (Global Standard)<br>Sweden Central (Global Standard) |
|`gpt-image-1.5` | West US 3 (Global Standard) <br> East US 2 (Global Standard) <br> UAE North (Global Standard) <br> Poland Central (Global Standard)<br>Sweden Central (Global Standard)|



## Video generation models

Sora is an AI model from OpenAI that can create realistic and imaginative video scenes from text instructions. Sora is in preview.

### Region availability

| Model | Region |
|---|---|
|`sora` | East US 2 (Global Standard)<br>Sweden Central (Global Standard)  |
| `sora-2` | East US 2 (Global Standard)<br>Sweden Central (Global Standard) |


## Audio models

Audio models in Azure OpenAI are available via the `realtime`, `completions`, and `audio` APIs.

### GPT-4o audio models

The GPT-4o audio models are part of the GPT-4o model family and support either low-latency, *speech in, speech out* conversational interactions or audio generation.

> [!CAUTION]
> We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

Details about maximum request tokens and training data are available in the following table:

|  Model ID  | Description | Max request (tokens) | Training data (up to)  |
|---|---|---|---|
|`gpt-4o-mini-audio-preview` (2024-12-17) <br> GPT-4o audio | Audio model for audio and text generation. |Input: 128,000  <br> Output: 16,384 | September 2023 |
|`gpt-4o-audio-preview` (2024-12-17) <br> GPT-4o audio | Audio model for audio and text generation. |Input: 128,000  <br> Output: 16,384 | September 2023 |
|`gpt-4o-realtime-preview` (2025-06-03) <br> GPT-4o audio | Audio model for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | October 2023 |
|`gpt-4o-realtime-preview` (2024-12-17) <br> GPT-4o audio | Audio model for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | October 2023 |
|`gpt-4o-mini-realtime-preview` (2024-12-17) <br> GPT-4o audio | Audio model for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | October 2023 |
|`gpt-realtime` (2025-08-28) (GA)<br>`gpt-realtime-mini` (2025-10-06)<br> `gpt-realtime-mini-2025-12-15` (2025-12-15) <br> `gpt-audio`(2025-08-28)<br>`gpt-audio-mini`(2025-10-06) | Audio model for real-time audio processing. |Input: 28,672  <br> Output: 4,096 | October 2023 |

To compare the availability of GPT-4o audio models across all regions, refer to the [models table](#global-standard-model-availability).

### Audio API

The audio models via the `/audio` API can be used for speech to text, translation, and text to speech.

#### Speech-to-text models


|  Model ID  | Description | Max request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |
| `gpt-4o-transcribe` | Speech-to-text model powered by GPT-4o. | 25 MB|
| `gpt-4o-mini-transcribe` | Speech-to-text model powered by GPT-4o mini. | 25 MB|
| `gpt-4o-transcribe-diarize` | Speech-to-text model with automatic speech recognition. | 25 MB|
| `gpt-4o-mini-transcribe-2025-12-15` | Speech-to-text model with automatic speech recognition. Improved transcription accuracy and robustness. | 25 MB|



#### Speech translation models

|  Model ID  | Description | Max request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |

#### Text-to-speech models (preview)

|  Model ID  | Description |
|  --- | :--- |
| `tts` | Text-to-speech model optimized for speed. |
| `tts-hd` | Text-to-speech model optimized for quality.|
| `gpt-4o-mini-tts` | Text-to-speech model powered by GPT-4o mini.<br/><br/>You can guide the voice to speak in a specific style or tone. |
| `gpt-4o-mini-tts-2025-12-15` | Text-to-speech model powered by GPT-4o mini.<br/><br/>You can guide the voice to speak in a specific style or tone. |

## Model summary table and region availability

### Models by deployment type

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment:

- **Standard**: Has a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned**: Also has a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, but the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types, see our [Deployment types guide](../../foundry-models/concepts/deployment-types.md).

# [Global Standard](#tab/global-standard-aoai)


### Global Standard model availability

[!INCLUDE [Standard Global](../includes/model-matrix/standard-global.md)]

> [!NOTE]
> `o3-deep-research` is currently only available with Foundry Agent Service. To learn more, see the [Deep Research tool guidance](/azure/ai-foundry/agents/how-to/tools/deep-research).

# [Global Provisioned managed](#tab/global-ptum-aoai)

### Global Provisioned managed model availability

[!INCLUDE [Provisioned Managed Global](../includes/model-matrix/provisioned-global.md)]

# [Global Batch](#tab/global-batch)

### Global Batch model availability

[!INCLUDE [Global batch](../includes/model-matrix/global-batch.md)]

# [Data Zone Standard](#tab/datazone-standard)

### Data Zone Standard model availability

[!INCLUDE [Data zone standard](../includes/model-matrix/datazone-standard.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for Global Standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time, access to `o1-mini` standard (regional) deployments isn't being expanded.

# [Data Zone Provisioned managed](#tab/datazone-provisioned-managed)

### Data Zone Provisioned managed model availability

[!INCLUDE [Global data zone provisioned managed](../includes/model-matrix/datazone-provisioned-managed.md)]

# [Data Zone Batch](#tab/datazone-batch)

### Data Zone Batch model availability

[!INCLUDE [Data zone batch](../includes/model-matrix/global-batch-datazone.md)]

# [Standard](#tab/standard)

### Standard deployment model availability

[!INCLUDE [Standard Models](../includes/model-matrix/standard-models.md)]

> [!NOTE]
> `o1-mini` is currently available to all customers for Global Standard deployment.
>
> Select customers were granted standard (regional) deployment access to `o1-mini` as part of the `o1-preview` limited access release. At this time, access to `o1-mini` standard (regional) deployments isn't being expanded.

# [Provisioned managed](#tab/provisioned)

### Provisioned deployment model availability

[!INCLUDE [Provisioned](../includes/model-matrix/provisioned-models.md)]

> [!NOTE]
> The provisioned version of `gpt-4` version `turbo-2024-04-09` is currently limited to text only.

For more information on provisioned deployments, see [Provisioned guidance](../concepts/provisioned-throughput.md).

---

This table doesn't include fine-tuning regional availability information. Consult the [fine-tuning section](#fine-tuning-models) for this information.

### Embeddings models

These models can be used only with Embedding API requests.

> [!NOTE]
> `text-embedding-3-large` is the latest and most capable embedding model. You can't upgrade between embedding models. To migrate from using `text-embedding-ada-002` to `text-embedding-3-large`, you need to generate new embeddings.  

|  Model ID | Max request (tokens) | Output dimensions |Training data (up to)
|---|---| :---:|:---:|:---:|
| `text-embedding-ada-002` (version 2) |8,192 | 1,536 | Sep 2021 |
| `text-embedding-ada-002` (version 1) |2,046 | 1,536 | Sep 2021 |
| `text-embedding-3-large` | 8,192 | 3,072 |Sep 2021 |
| `text-embedding-3-small` | 8,192|  1,536 | Sep 2021 |

> [!NOTE]
> When you send an array of inputs for embedding, the maximum number of input items in the array per call to the embedding endpoint is 2,048.

### Image generation models

|  Model ID  | Max request (characters) |
|  --- | :---: |
| `gpt-image-1` | 4,000 |
| `gpt-image-1-mini` | 4,000 |
| `gpt-image-1.5` | 4,000 |
| `dall-e-3`  | 4,000 |

### Video generation models

|  Model ID  | Max Request (characters) |
|  --- | :---: |
| sora | 4,000 |

## Fine-tuning models

[!INCLUDE [Fine-tune models](../includes/fine-tune-models.md)]

## Assistants (preview)

For Assistants, you need a combination of a supported model and a supported region. Certain tools and capabilities require the latest models. The following models are available in the Assistants API, SDK, and Foundry. The following table is for standard deployment. For information on provisioned throughput unit availability, see [Provisioned throughput](../concepts/provisioned-throughput.md). The listed models and regions can be used with both Assistants v1 and v2. You can use [Global Standard models](#global-standard-model-availability) if they're supported in the following regions.

| Region   |  gpt-4o, 2024-05-13   | gpt-4o, 2024-08-06   | gpt-4o-mini, 2024-07-18   | gpt-4, 0613   | gpt-4, 1106-Preview   | gpt-4, 0125-Preview    | gpt-4, turbo-2024-04-09   | gpt-4-32k, 0613  | gpt-35-turbo, 0613   | gpt-35-turbo, 1106   | gpt-35-turbo, 0125   | gpt-35-turbo-16k, 0613   |
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

For the latest information on model retirements, refer to the [model retirement guide](../concepts/model-retirements.md).

## Related content

- [Foundry Models from partners and community](../../foundry-models/concepts/models-from-partners.md)
- [Model retirement and deprecation](../concepts/model-retirements.md)
- [Learn more about working with Azure OpenAI models](../how-to/working-with-models.md)
- [Learn more about Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Learn more about fine-tuning Azure OpenAI models](../how-to/fine-tuning.md)
