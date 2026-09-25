---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/23/2026
ms.custom: include
ai-usage: ai-assisted
---

Before creating a provisioned deployment, estimate how many provisioned throughput units (PTUs) your workload needs. This article provides the per-model throughput parameters you need and shows how to calculate PTU requirements using sizing formulas or the Foundry capacity calculator.

If you're new to provisioned throughput, start with [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md) When you're ready to create your deployment, see [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md).

## Prerequisites

- Familiarity with the concepts in [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md)
- An estimate of your workload characteristics: expected peak requests per minute (RPM), average prompt size in tokens, and average response size in tokens.

## Estimate PTUs for text-only model

For a text model, the workload always includes *text output tokens.* Input can consist of *text input tokens*, *image input tokens*, or a combination of both. This section covers how to estimate the number of PTUs required for a workload when you use a text model. For how to estimate the number of PTUs for an image model, see [Estimate PTUs for image model](#estimate-ptus-for-image-model).

Two approaches are available for estimating the PTUs required for a workload:

- Use the [sizing formulas](#estimate-manually) for full control over the calculation
- Use the [Foundry capacity calculator](#use-the-capacity-calculator) for a guided estimate. 

Both approaches use per-model values from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model) to generate estimates. For the most accurate results, benchmark a deployment against representative traffic rather than relying solely on estimated inputs.

> [!NOTE]
> For older models (before GPT-4o), the [request/call shape distribution](../concepts/provisioned-throughput.md#ptu-sizing) affects capacity consumption: a small number of large calls can consume significantly more capacity than many small calls with the same average token count. For GPT-4o and later models, TPM per PTU is set for input and output tokens separately, so this tiering effect doesn't apply.


### Estimate manually

You can estimate the PTUs your workload requires by using the model-specific values from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model) and information about your expected traffic as follows:


| Input | Description |
|---|---|
| **Model** | The model you plan to deploy, such as `gpt-5.2`. This value determines which *Input TPM per PTU* and *output-to-input ratio* values to use from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model). |
| **Deployment type** | The provisioned deployment type: Global Provisioned, Data Zone Provisioned, or Regional Provisioned. |
| **Peak RPM** | The expected peak number of calls per minute sent to the model. |
| **Average prompt size** | The average number of input tokens per request. |
| **Average response size** | The average number of output tokens per request. |
| **Cache rate** | The percentage of input tokens served from the prompt cache. Use `0` if caching isn't used. Cached tokens are deducted 100% from the utilization calculation and don't consume PTU capacity. |

#### Normalized TPM

The manual calculation of PTUs converts your expected token volume into a single number called the *normalized TPM*. The number of PTUs required is then determined by dividing the *normalized TPM* by the model's **Input TPM per PTU** value.

**Formulas:**

- Input TPM = Peak RPM × average prompt size
- Output TPM = Peak RPM × average response size
- Normalized TPM = (input TPM × (1 − cache rate)) + (output-to-input ratio × output TPM)
- PTUs required = normalized TPM ÷ Input TPM per PTU

**Worked example:**

Suppose your application sends requests at a peak rate of 1,000 RPM, with an average prompt size of 200 tokens and an average response size of 20 tokens, using the gpt-5.2 model with Data Zone provisioned throughput deployment. From the [table](#latest-azure-openai-models), gpt-5.2 has an Input TPM per PTU of 3,400 and an output-to-input ratio of 8.

- Input TPM = 1,000 × 200 = 200,000
- Output TPM = 1,000 × 20 = 20,000
- Normalized TPM (no cache) = 200,000 + (8 × 20,000) = 360,000
- PTUs required = 360,000 ÷ 3,400 = 105.88 (**110 PTUs** rounded up to the nearest 5 PTUs, matching the Data Zone Provisioned scale increment for gpt-5.2.)

If 50% of input tokens are served from the prompt cache:

- Effective input TPM = 200,000 × (1 − 0.50) = 100,000
- Normalized TPM = 100,000 + (8 × 20,000) = 260,000
- PTUs required = 260,000 ÷ 3,400 = 76.47 (**80 PTUs** rounded up to the nearest 5 PTUs, matching the Data Zone Provisioned scale increment for gpt-5.2.)

In summary, the PTUs needed for this example call shape with and without caching are as follows:

| Peak calls per minute (RPM) | Prompt size (tokens) | Response size (tokens) | Cache rate | Input TPM | Output TPM | Normalized TPM | Estimated PTUs | PTUs (rounded up)<sup>1</sup> |
|---|---|---|---|---|---|---|---|---|
| 1,000 | 200 | 20 | 0% | 200,000 | 20,000 | 360,000 | 105.88 | 110 |
| 1,000 | 200 | 20 | 50% | 100,000 | 20,000 | 260,000 | 76.47 | 80 |

<sup>1</sup> Rounded up to the nearest 5 PTUs, matching the Data Zone Provisioned scale increment for gpt-5.2.

### Use the capacity calculator

Use the [capacity calculator](https://ai.azure.com/nextgen/goto/build/models/ptu-calculator) in the Foundry portal to size specific workload shapes. Find the calculator on the **Quota** page and enter the following parameters based on your workload:

| Input | Description |
|---|---|
| **Model** | The model you plan to use. |
| **Version** | The version of the model you plan to use. |
| **Peak calls per min** | The number of calls per minute you expect to send to the model. |
| **Tokens in prompt call** | The number of tokens in the prompt for each call to the model. Calls with larger prompts consume more PTU capacity. The calculator assumes a single prompt value. For workloads with wide variance in prompt size, benchmark a deployment against your actual traffic for a more accurate estimate. |
| **Tokens in model response** | The number of tokens generated per call, also called generation size. Calls with larger generation sizes consume more PTU capacity. As with prompt tokens, the calculator assumes a single value. |
| **Cache rate** | Percentage of input tokens served from the prompt cache. |

After you fill in the required details, select **Calculate**. The output shows:

- The estimated PTU count required for the workload. This value is rounded up to the nearest PTU scale increment for the selected deployment type, or to the deployment type's minimum PTU count, depending on which one is larger.
- The raw (unrounded) estimated PTU count.


## How input and output tokens affect throughput

The throughput that a deployment gets per PTU depends on the model and the mix of input and output tokens in a given minute. Throughput is measured as tokens per minute, or TPM. Generating output tokens requires more processing capacity than consuming input tokens.

For GPT-4.1 models and later, the system determines an *output-to-input ratio* to match the global standard price ratio between input and output tokens, [with exceptions for some models](#models-with-a-non-standard-output-to-input-ratio). For example,

- For gpt-5, one output token counts as eight input tokens toward your utilization limit, matching the model's [global standard price](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) ratio.
- For gpt-4.1, one output token counts as four input tokens.
- Older models use different ratios.

For all deployments, cached tokens are deducted 100% from the utilization calculation, so repeated prompt tokens don't consume PTU capacity. See [Prompt caching](../how-to/prompt-caching.md) for more information.

### Models with a non-standard output-to-input ratio

Some models use an output-to-input ratio that differs from their global standard price ratio. For example, with Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit, which differs from that model's standard price ratio. See [pricing for Llama models](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/) for the full input and output pricing breakdown.

## Deployment parameters and throughput values by model

The tables in this section list the throughput and deployment parameters for each supported model. To understand what the parameters in each row mean, see [Understand deployment parameters](#understand-deployment-parameters).

### Latest Azure OpenAI models

> [!NOTE]
>
> Long-context requests that exceed 128K prompt tokens aren't supported for `gpt-5.4`, `gpt-4.1`, `gpt-4.1-mini`, and `gpt-4.1-nano`. The system routes these requests to [spillover deployments](../how-to/spillover-traffic-management.md), if available. Otherwise, the requests return an error.

| Topic | **gpt-6-sol**,<br>**2026-09-22** | **gpt-6-astra**,<br>**2026-09-03** | **gpt-5.6-luna**,<br>**2026-07-09** | **gpt-5.6-terra**,<br>**2026-07-09** | **gpt-5.6-sol**,<br>**2026-07-09** | **gpt-5.5**,<br>**2026-04-24** | **gpt-image-2**,<br>**2026-04-21** | **gpt-5.4**,<br>**2026-03-05** | **gpt-5.4-mini**,<br>**2026-03-17** | **gpt-5.3-codex**,<br>**2026-02-24** | **gpt-5.2**,<br>**2025-12-11** | **gpt-5.2-codex**,<br>**2026-01-14** | **gpt-5.1**,<br>**2025-11-13** | **gpt-5.1-codex**,<br>**2025-11-13** | **gpt-5**,<br>**2025-08-07** | **gpt-5-mini**,<br>**2025-08-07** | **gpt-4.1**,<br>**2025-04-14** | **gpt-4.1-mini**,<br>**2025-04-14** | **gpt-4.1-nano**,<br>**2025-04-14** | **o3**,<br>**2025-04-16** | **o4-mini**,<br>**2025-04-16** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 | 15 | 15 | 100 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 | 5 | 5 | 100 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 50 | 50 | 50 | 50 | 50 | 100  | 50 | 25 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Regional provisioned scale increment | 50 | 50 | 50 | 50 | 50 | 50 | 100 | 50 | 25 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Input TPM per PTU | 3,000 | 600 | 30,000 | 3,000 | 1,200 | 1,200 | 1,200 | 2,400 | 7,900 | 3,400 | 3,400 | 3,400 | 4,750 | 4,750 | 4,750 | 23,750 | 3,000 | 14,900 | 59,400 | 3,000 | 5,400 |
| Output-to-input ratio | See [GPT-6 sizing guidance](#normalized-token-pricing-for-gpt-6-astra) | See [GPT-6 sizing guidance](#normalized-token-pricing-for-gpt-6-astra) | 6 | 6 | 6 | 6 | See [GPT-image-2 sizing guidance](#estimate-ptus-for-image-model) | 6 | 6 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 4 | 4 | 4 | 4 | 4 |
| Latency target value<sup>1</sup> | 99% > 80 TPS | 99% > 40 TPS | 99% > 100 TPS | 99% > 70 TPS | 99% > 80 TPS | 99% > 50 TPS | N/A<sup>2</sup> | 99% > 50 TPS | 99% > 100 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 80 TPS | 99% > 80 TPS | 99% > 90 TPS | 99% > 100 TPS | 99% > 80 TPS | 99% > 90 TPS |

<sup>1</sup> Calculated as p50 request latency on a per 5-minute basis. TPS = tokens per second.

<sup>2</sup> Latency SLA not defined.

<a id="normalized-token-pricing-for-gpt-6-astra"></a>
<a id="normalized-token-pricing"></a>

#### Normalized token pricing for GPT-6 Astra and newer models

GPT-6 Astra, GPT-6 Sol, and newer Azure OpenAI models use normalized tokens to align PTU capacity consumption with Global Standard pay-as-you-go token pricing. This method accounts for input, cached input, cache writes, and output, including different weights for short- and long-context requests.

GPT-6 Astra and GPT-6 Sol support [prompt cache breakpoints](../how-to/prompt-caching.md#configure-prompt-cache-breakpoints) for explicit control over prompt caching. Cache reads and writes are included in normalized-token accounting.

> [!NOTE]
> One short-context input token is one normalized token. Calculate every other token weight by dividing its price by the same model's short-context input price. For newer models, apply this method using that model's own prices; don't assume its weights are unchanged.
>
> Cached input and cache writes consume PTU capacity at their respective weights. The older sizing rule that deducts cached input entirely doesn't apply to models using this accounting method.

##### Pay-as-you-go prices and token weights

The following prices give GPT-6 Astra and GPT-6 Sol the same normalized token weights. For either model, a short-context output token consumes 5 normalized tokens, and a long-context output token consumes 7.5 normalized tokens. Prices are in USD per 1 million tokens.

| Token type | GPT-6 Astra Global Standard price | GPT-6 Sol Global Standard price | Price relative to the model's short-context input | Normalized token cost |
|---|---:|---:|---:|---:|
| Short-context input | $10.00 | $2.00 | 1.0× | 1.0 |
| Short-context cached input | $1.00 | $0.20 | 0.1× | 0.1 |
| Short-context cache write | $12.50 | $2.50 | 1.25× | 1.25 |
| Short-context output | $50.00 | $10.00 | 5.0× | 5.0 |
| Long-context input | $20.00 | $4.00 | 2.0× | 2.0 |
| Long-context cached input | $2.00 | $0.40 | 0.2× | 0.2 |
| Long-context cache write | $25.00 | $5.00 | 2.5× | 2.5 |
| Long-context output | $75.00 | $15.00 | 7.5× | 7.5 |

`Normalized token cost = token-type price ÷ the model's short-context input price`

For GPT-6 Astra, divide by $10.00. For GPT-6 Sol, divide by $2.00. Use the same pricing unit in the numerator and denominator. For example, GPT-6 Sol long-context output has a weight of `$15.00 ÷ $2.00 = 7.5`.

##### Convert normalized tokens to PTUs

Each PTU supplies a model-specific normalized-token budget per minute. Because short-context input has a weight of 1, that budget equals the model's Input TPM per PTU value.

| Model | Version | Short-context input TPM per PTU | Normalized TPM per PTU |
|---|---|---:|---:|
| gpt-6-astra | 2026-09-03 | 600 | 600 |
| gpt-6-sol | 2026-09-22 | 3,000 | 3,000 |

- Normalized TPM = Sum of (tokens per minute in each token category × that category's normalized token cost).
- Raw PTUs required = Normalized TPM ÷ the model's normalized TPM per PTU.

Assign each token to its applicable category once; don't count a cached or cache-write token again as ordinary input. Round the raw PTU requirement up to a supported deployment size, using the minimum and scale increment in the [deployment table](#latest-azure-openai-models).

##### PTU and pay-as-you-go comparison

This illustration uses **one PTU at $260.00 per month**, retaining the existing article's example cost and applying it to both models. It assumes 100% sustained utilization for 30 days, no discounts, and the token prices above. It's a capacity comparison, not a quote for a deployable configuration; deployment minimums still apply.

| Metric | GPT-6 Astra PTU | GPT-6 Astra pay-as-you-go | GPT-6 Sol PTU | GPT-6 Sol pay-as-you-go |
|---|---:|---:|---:|---:|
| Monthly normalized-token volume | **25.92M** (`600 × 60 × 24 × 30`) | **25.92M** | **129.60M** (`3,000 × 60 × 24 × 30`) | **129.60M** |
| Monthly cost for that volume | **$260.00** (example assumption) | **$259.20** (`25.92M × $10.00/M`) | **$260.00** (example assumption) | **$259.20** (`129.60M × $2.00/M`) |
| Effective cost per 1M normalized tokens | **~$10.03** (`$260.00 ÷ 25.92`) | **$10.00** (`$259.20 ÷ 25.92`) | **~$2.01** (`$260.00 ÷ 129.60`) | **$2.00** (`$259.20 ÷ 129.60`) |

Under these assumptions, PTU and pay-as-you-go costs are approximately equal at full utilization. Using the same token weights makes this a token-mix-independent comparison of normalized-token capacity, not a guarantee of realized workload throughput or cost. Lower utilization increases the effective PTU cost per token.

For current Azure prices and purchase terms, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/azure-openai/).

### Previous Azure OpenAI models

| Topic | **gpt-4o** | **gpt-4o-mini** | **o3-mini** | **o1** |
|---|---|---|---|---|
| Global and data zone provisioned minimum deployment | 15 | 15 | 15 | 15 |
| Global and data zone provisioned scale increment | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 25 | 25 | 25 |
| Regional provisioned scale increment | 50 | 25 | 25 | 50 |
| Input TPM per PTU | 2,500 | 37,000 | 2,500 | 230 |
| Output-to-input ratio | 4 | 4 | 4 | 4 |
| Latency target value<sup>1</sup> | 99% > 25 TPS | 99% > 33 TPS | 99% > 66 TPS | 99% > 25 TPS |

<sup>1</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Foundry Models sold by Azure

This section lists other Foundry models sold by Azure, not including the Azure OpenAI in Foundry Models listed in the previous tables.

| Topic | **Llama-3.3-70B-Instruct** |
|---|---|
| Global and data zone provisioned minimum deployment | 100 |
| Global and data zone provisioned scale increment | 100 |
| Regional provisioned minimum deployment | NA |
| Regional provisioned scale increment | NA |
| Input TPM per PTU | 8,450 |
| Output-to-input ratio | 4<sup>1</sup> |
| Latency target value<sup>2</sup> | 99% > 50 TPS |

<sup>1</sup> For Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit. This ratio differs from the global standard price ratio between input and output tokens. See [Models with a non-standard output-to-input ratio](#models-with-a-non-standard-output-to-input-ratio) and [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/).

<sup>2</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Fireworks on Microsoft Foundry models

The following Fireworks on Microsoft Foundry models support both Global and US Data Zone provisioned throughput.

|Topic|**DeepSeek v3.1**|**DeepSeek v3.2**|**DeepSeek V4 Flash 0731**|**DeepSeek V4 Pro**|**Gemma 4 26B A4B IT**|**Gemma 4 31B IT**|**GLM-4.7**|**GLM 5**|**GLM-5.1**|**GLM 5.2**|**gpt-oss-20b**|**gpt-oss-120b**|**Inkling**|**Kimi K2 Instruct 0905**|**Kimi K2 Thinking**|**Kimi K2.5**|**Kimi K2.6**|**Kimi K2.7 Code**|**MiniMax M2.5**|**MiniMax M3**|**Ministral 3 3B Instruct 2512**|**Nemotron 3.5 Lightning**|**Nemotron Super 120B**|**Nemotron 3 Ultra NVFP4**|**PaddleOCR VL 1.6**|**Qwen 3 14B**|**Qwen 3 32B**|**Qwen 3.5 4B**|**Qwen 3.5 9B**|**Qwen 3.5 27B**|**Qwen 3.5 35B A3B**|**Qwen 3.5 112B A10B**|**Qwen 3.5 397B**|**Qwen 3.6 27B**|**Qwen 3.6 35B A3B**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Minimum deployment|200|300|100|400|200|200|200|300|400|400|80|40|400|200|200|200|200|200|400|400|40|50|100|200|40|80|80|80|40|550|40|100|100|40|40|
|Scale increment|100|150|50|200|100|100|100|150|200|200|40|20|200|100|100|100|100|100|200|200|20|25|50|100|20|40|40|40|20|275|20|50|50|20|20|
|Input TPM per PTU|2,100|3,000|2,800|200|5,400|2,200|6,000|600|900|300|25,000|13,500|3,850|2,500|1,400|1,060|4,000|2,000|5,300|5,300|25,400|60,350|4,850|1,100|341,500|4,800|5,000|35,500|10,700|2,730|17,800|5,600|4,250|7,700|31,000|
|Latency Target Value<sup>1</sup>|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|

<sup>1</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

## Understand deployment parameters

Each row in the tables corresponds to one of the following parameters:

| Parameter | Description |
|---|---|
| **Global & data zone provisioned minimum deployment** | The smallest number of PTUs you can deploy for Global Provisioned or Data Zone Provisioned deployment types. For example, gpt-5.2 requires a minimum deployment of 15 PTUs. |
| **Global & data zone provisioned scale increment** | The PTU increment in which you can increase or decrease a Global Provisioned or Data Zone Provisioned deployment. Continuing with the gpt-5.2 example, an increment of 5 means deployments can be sized at 15, 20, 25, and so on. |
| **Regional provisioned minimum deployment** | The smallest number of PTUs you can deploy for a Regional Provisioned deployment. For example, gpt-5.2 requires a minimum regional provisioned deployment of 50 PTUs. |
| **Regional provisioned scale increment** | The PTU increment for Regional Provisioned deployments. Continuing with the gpt-5.2 example, an increment of 50 means deployments can be sized at 50, 100, 150, and so on. |
| **Input TPM per PTU** | The maximum input tokens per minute (TPM) that one PTU supports. Use this value when [estimating PTUs](#estimate-ptus-for-text-only-model). |
| **Output-to-input ratio** | The weight applied to output tokens when estimating PTU requirements. This value reflects the model's global standard price ratio between output and input tokens, with [exceptions for some models](#models-with-a-non-standard-output-to-input-ratio). For example, a ratio of 8 means one output token counts as eight input tokens toward the model's TPM limit. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/), [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/), and [DeepSeek model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/deepseek/) for current pricing. |
| **Latency target value** | The expected request latency at the stated PTU utilization level. Expressed as a percentile threshold—for example, "99% > 50 TPS" means 99% of requests are processed at more than 50 tokens per second. |

## Estimate PTUs for image model

Image models extend the PTU sizing methodology used with text-only models because a workload for an image model contains *image output tokens* in addition to *text input tokens* and *image input tokens*. Each of these token types consumes PTU capacity differently. 

To size a deployment, you must first convert all token types into a common unit called **normalized tokens**, which represent the equivalent number of text input tokens before estimating PTU requirements.

> [!NOTE]
> Before using Azure Monitor to monitor a deployed image model, review [Limitations and known issues for image model metrics](../how-to/provisioned-get-started.md#limitations-and-known-issues-for-image-model-metrics).

### Estimate PTUs manually

Estimate the PTUs your workload requires by using the throughput values for your image model and information about your expected traffic as follows:

#### Traffic information

| Input | Description |
| --- | --- |
| **Peak RPM** | The expected peak number of requests per minute sent to the model. |
| **Text input tokens** | The average number of text input tokens per request. |
| **Image input tokens**<sup>1</sup> | The average number of image input tokens per request. |
| **Image output tokens**<sup>2</sup> | The average number of image output tokens per request. |

<sup>1</sup> To estimate **image input tokens** per request, refer to the OpenAI documentation: [Image input cost calculator](https://developers.openai.com/api/docs/guides/images-vision?api-mode=responses#image-input-cost-calculator). 

<sup>2</sup> To estimate **image output tokens** per request, refer to the OpenAI documentation: [Image output token calculator](https://developers.openai.com/api/docs/guides/image-generation#gpt-image-25-and-gpt-image-2-output-tokens).

#### Throughput values for image model

GPT-image-2 uses the following throughput values:

| Parameter | Value |
| --- | --- |
| Text input tokens per minute per PTU | 1,200 |
| Image input tokens per minute per PTU | 750 |
| Image-to-text conversion factor<sup>1</sup> | 1.6 |
| Image output-to-image-input token cost ratio<sup>2</sup> | 3.75 |

<sup>1</sup> The image-to-text conversion factor is `Text input tokens per minute per PTU` ÷ `Image input tokens per minute per PTU`. This factor means that one image token uses the same PTU capacity as about `1.6` text input tokens.

<sup>2</sup> Image output tokens have a higher weight than image input tokens because image generation needs extra processing. The image output weighting happens before converting to text-token equivalents.

#### Normalized TPM

The manual calculation converts image input and output tokens to equivalent text input tokens. The resulting *normalized TPM* determines the number of PTUs required.

- Normalized tokens per request = Text input tokens + (image input tokens × 1.6) + (image output tokens × 3.75 × 1.6)
- Normalized TPM = Normalized tokens per request × Peak RPM
- PTUs required = Normalized TPM ÷ 1,200

Round the raw PTU requirement up to the nearest deployment increment or to the minimum deployment size, whichever is larger.

**Worked example:**

Suppose your application sends 10 requests per minute, with 2,000 text input tokens, 1,229 image input tokens, and 7,024 image output tokens per request. GPT-image-2 has an image-to-text conversion factor of 1.6, an image output-to-input ratio of 3.75, and 1,200 normalized TPM per PTU.

- Normalized tokens per request = 2,000 + (1,229 × 1.6) + (7,024 × 3.75 × 1.6) = 46,110.4
- Normalized TPM = 46,110.4 × 10 = 461,104
- PTUs required = 461,104 ÷ 1,200 = 384.25 (**400 PTUs** rounded up to the nearest 100 PTUs, matching the scale increment for GPT-image-2.)

In summary, the PTUs needed for this example workload are as follows:

| Peak RPM | Text input tokens | Image input tokens | Image output tokens | Normalized TPM | Estimated PTUs | Deployment PTUs<sup>1</sup> |
|----------|-------------------|--------------------|---------------------|----------------|----------------|-----------------------------|
| 10       | 2,000             | 1,229              | 7,024               | 461,104        | 384.25         | 400                         |

<sup>1</sup> Rounded up to the 100-PTU scale increment for GPT-image-2.

## Related content

- [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md)
- [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md)
- [Provisioned throughput billing and cost management](../concepts/provisioned-throughput-billing.md)
- [Operate provisioned deployments in production](../how-to/provisioned-get-started.md)
