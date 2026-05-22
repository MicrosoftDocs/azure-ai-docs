---
title: "Determine PTU sizing for a workload"
description: "Find per-model throughput parameters and estimate how many PTUs your provisioned deployment needs using formulas or the Foundry capacity calculator."
ai-usage: ai-assisted
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: how-to
ms.date: 05/22/2026
manager: nitinme
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
recommendations: false
#customerIntent: As a developer planning a provisioned throughput deployment in Microsoft Foundry, I want to find per-model throughput parameters and estimate PTU requirements for my workload so that I can size my deployment correctly before I create it.
---

# Determine PTU sizing for a workload

Before creating a provisioned deployment, estimate how many provisioned throughput units (PTUs) your workload needs. This article provides the per-model throughput parameters you need and shows how to calculate PTU requirements using sizing formulas or the Foundry capacity calculator.

If you're new to provisioned throughput, start with [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md). When you're ready to create your deployment, see [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md).

## Prerequisites

- Familiarity with the concepts in [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md).
- An estimate of your workload characteristics: expected peak requests per minute (RPM), average prompt size in tokens, and average response size in tokens.

## Estimate PTUs required

Two approaches are available for estimating the number of PTUs required for a workload:

- Use the [sizing formulas](#estimate-manually) for full control over the calculation
- Use the [Foundry capacity calculator](#use-the-capacity-calculator) for a guided estimate. 

Both approaches use per-model values from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model) to generate estimates. For the most accurate results, benchmark a deployment against representative traffic rather than relying solely on estimated inputs.

> [!NOTE]
> For older models (before GPT-4o), the [request/call shape distribution](../concepts/provisioned-throughput.md#ptu-sizing) affects capacity consumption: a small number of large calls can consume significantly more capacity than many small calls with the same average token count. For GPT-4o and later models, TPM per PTU is set for input and output tokens separately, so this tiering effect doesn't apply.


### Estimate manually

You can estimate the PTUs your workload requires using the model-specific values from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model) and information about your expected traffic as follows:


| Input | Description |
|---|---|
| **Model** | The model you plan to deploy, for example, `gpt-5.2`. Determines which *Input TPM per PTU* and *output-to-input ratio* values to use from the [deployment parameters tables](#deployment-parameters-and-throughput-values-by-model). |
| **Deployment type** | The provisioned deployment type: Global Provisioned, Data Zone Provisioned, or Regional Provisioned. |
| **Peak RPM** | The expected peak number of calls per minute sent to the model. |
| **Average prompt size** | The average number of input tokens per request. |
| **Average response size** | The average number of output tokens per request. |
| **Cache rate** | The percentage of input tokens served from the prompt cache. Use `0` if caching isn't used. Cached tokens are deducted 100% from the utilization calculation and don't consume PTU capacity. |

#### Normalized TPM

The manual calculation of PTUs converts your expected token volume into a single number called the *normalized TPM*. The number of PTUs required is then determined by dividing the *normalized TPM* by the model's **Input TPM per PTU** value.

**Formulas:**

- Input TPM = Peak RPM × average prompt size (tokens)
- Output TPM = Peak RPM × average response size (tokens)
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

Use the [capacity calculator](https://ai.azure.com/resource/calculator) in the Foundry portal to size specific workload shapes. Find the calculator under **Operate** > **Quota** > **Provisioned throughput unit**, and enter the following parameters based on your workload:

| Input | Description |
|---|---|
| **Model** | The model you plan to use. |
| **Version** | The version of the model you plan to use. |
| **Peak calls per min** | The number of calls per minute expected to be sent to the model. |
| **Tokens in prompt call** | The number of tokens in the prompt for each call to the model. Calls with larger prompts consume more PTU capacity. The calculator assumes a single prompt value—for workloads with wide variance in prompt size, benchmark a deployment against your actual traffic for a more accurate estimate. |
| **Tokens in model response** | The number of tokens generated per call, also called generation size. Calls with larger generation sizes consume more PTU capacity. As with prompt tokens, the calculator assumes a single value. |
| **Cache rate** | Percentage of input tokens served from the prompt cache. |

After you fill in the required details, select **Calculate**. The output shows:

- The estimated PTU count required for the workload. This value is rounded up to the nearest PTU scale increment for the selected deployment type, or to the deployment type's minimum PTU count, depending on which one is larger.
- The raw (unrounded) estimated PTU count.


## How input and output tokens affect throughput

The throughput (measured as tokens per minute, or TPM) that a deployment gets per PTU depends on the model and the mix of input and output tokens in a given minute. Generating output tokens requires more processing capacity than consuming input tokens.

For GPT-4.1 models and later, the system determines an *output-to-input ratio* to match the global standard price ratio between input and output tokens, [with exceptions for some models](#models-with-a-non-standard-output-to-input-ratio). For example,

- For gpt-5, one output token counts as eight input tokens toward your utilization limit, matching the model's [global standard price](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) ratio.
- For gpt-4.1, one output token counts as four input tokens.
- Older models use different ratios.

For all deployments, cached tokens are deducted 100% from the utilization calculation, meaning repeated prompt tokens don't consume PTU capacity. See [Prompt caching](prompt-caching.md) for more information.

### Models with a non-standard output-to-input ratio

Some models use an output-to-input ratio that differs from their global standard price ratio. For example, with Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit, which differs from that model's standard price ratio. See [pricing for Llama models](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/) for the full input and output pricing breakdown.

## Deployment parameters and throughput values by model

The tables in this section list the throughput and deployment parameters for each supported model. To understand what the parameters in each row mean, see the [Appendix](#appendix).

### Latest Azure OpenAI models

> [!NOTE]
> gpt-5.4, gpt-4.1, gpt-4.1-mini, and gpt-4.1-nano don't support long context (requests estimated at larger than 128k prompt tokens).

| Topic | **gpt-5.5** | **gpt-5.4** | **gpt-5.3-codex** | **gpt-5.2** | **gpt-5.2-codex** | **gpt-5.1** | **gpt-5.1-codex** | **gpt-5** | **gpt-5-mini** | **gpt-4.1** | **gpt-4.1-mini** | **gpt-4.1-nano** | **o3** | **o4-mini** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Regional provisioned scale increment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Input TPM per PTU | 1,200 | 2,400 | 3,400 | 3,400 | 3,400 | 4,750 | 4,750 | 4,750 | 23,750 | 3,000 | 14,900 | 59,400 | 3,000 | 5,400 |
| Output-to-input ratio | 6 | 6 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 4 | 4 | 4 | 4 | 4 |
| Latency target value<sup>1</sup> | 99% > 100 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 80 TPS | 99% > 80 TPS | 99% > 90 TPS | 99% > 100 TPS | 99% > 80 TPS | 99% > 90 TPS |

<sup>1</sup> Calculated as p50 request latency on a per 5-minute basis. TPS = tokens per second.

### Previous Azure OpenAI models

| Topic | **gpt-4o** | **gpt-4o-mini** | **o3-mini** | **o1** |
|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 25 | 25 | 25 |
| Regional provisioned scale increment | 50 | 25 | 25 | 50 |
| Input TPM per PTU | 2,500 | 37,000 | 2,500 | 230 |
| Output-to-input ratio | 4 | 4 | 4 | 4 |
| Latency target value<sup>1</sup> | 99% > 25 TPS | 99% > 33 TPS | 99% > 66 TPS | 99% > 25 TPS |

<sup>1</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Foundry Models sold by Azure

This section lists other Foundry Models sold by Azure, not including the Azure OpenAI in Foundry Models listed in the previous tables.

| Topic | **Llama-3.3-70B-Instruct** | **DeepSeek-R1** | **DeepSeek-V3-0324** |
|---|---|---|---|
| Global & data zone provisioned minimum deployment | 100 | 100 | 100 |
| Global & data zone provisioned scale increment | 100 | 100 | 100 |
| Regional provisioned minimum deployment | NA | NA | NA |
| Regional provisioned scale increment | NA | NA | NA |
| Input TPM per PTU | 8,450 | 4,000 | 4,000 |
| Output-to-input ratio | 4<sup>1</sup> | 4 | 4 |
| Latency target value<sup>2</sup> | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS |

<sup>1</sup> For Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit. This ratio differs from the global standard price ratio between input and output tokens. See [Models with a non-standard output-to-input ratio](#models-with-a-non-standard-output-to-input-ratio) and [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/).

<sup>2</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Fireworks on Microsoft Foundry models (Preview)

The following Fireworks on Microsoft Foundry models currently support provisioned throughput.

|Topic|**gpt-oss-120b**|**Kimi K2 Instruct 0905**|**Kimi K2 Thinking**|**Kimi K2.5**|**Kimi K2.6**|**DeepSeek v3.1**|**DeepSeek v3.2**|**Qwen3 14B**|**MiniMax 2.5**|**GLM-5**|**GLM-4.7**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Global provisioned minimum deployment|80|500|500|800|800|800|1200|80|400|700|800|
|Global provisioned scale increment|40|275|275|400|400|400|600|40|200|350|400|
|Input TPM per PTU|13,500|1,250|700|530|2,000|1,050|1,500|4,800|3,000|3,500|3,000|
|Latency Target Value<sup>1</sup>|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|99% > 50 TPS|

<sup>1</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Appendix

Each row in the tables corresponds to one of the following parameters:

| Parameter | Description |
|---|---|
| **Global & data zone provisioned minimum deployment** | The smallest number of PTUs you can deploy for Global Provisioned or Data Zone Provisioned deployment types. For example, gpt-5.2 requires a minimum deployment of 15 PTUs. |
| **Global & data zone provisioned scale increment** | The PTU increment in which you can increase or decrease a Global Provisioned or Data Zone Provisioned deployment. Continuing with the gpt-5.2 example, an increment of 5 means deployments can be sized at 15, 20, 25, and so on. |
| **Regional provisioned minimum deployment** | The smallest number of PTUs you can deploy for a Regional Provisioned deployment. For example, gpt-5.2 requires a minimum regional provisioned deployment of 50 PTUs. |
| **Regional provisioned scale increment** | The PTU increment for Regional Provisioned deployments. Continuing with the gpt-5.2 example, an increment of 50 means deployments can be sized at 50, 100, 150, and so on. |
| **Input TPM per PTU** | The maximum input tokens per minute (TPM) that one PTU supports. Use this value when [estimating PTUs](#estimate-ptus-required). |
| **Output-to-input ratio** | The weight applied to output tokens when estimating PTU requirements. This value reflects the model's global standard price ratio between output and input tokens, with [exceptions for some models](#models-with-a-non-standard-output-to-input-ratio). For example, a ratio of 8 means one output token counts as eight input tokens toward the model's TPM limit. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/), [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/), and [DeepSeek model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/deepseek/) for current pricing. |
| **Latency target value** | The expected request latency at the stated PTU utilization level. Expressed as a percentile threshold—for example, "99% > 50 TPS" means 99% of requests are processed at more than 50 tokens per second. |


## Related content

- [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md)
- [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md)
- [Provisioned throughput billing and cost management](../concepts/provisioned-throughput-billing.md)
- [Operate provisioned deployments in production](./provisioned-get-started.md)
