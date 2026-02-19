---
title: 'Fine-tuning cost management'
titleSuffix: Azure OpenAI
description: Learn about the training and hosting costs associated with fine-tuning
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
show_latex: true
ms.custom: ignite2025
monikerRange: 'foundry-classic || foundry'
---

# Cost management for fine-tuning

Fine-tuning involves two cost components: a one-time training cost and ongoing hosting and inference costs. This guide explains how to estimate and manage both.

> [!IMPORTANT]
> The numbers in this article are for example purposes only. You should always refer to the official [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service) for pricing details to use in the formulas provided in this article.

## Upfront investment - training your model

This is the one-time, fixed cost associated with teaching a base model your specific requirements using your training data. The following sections explain how training costs are calculated.

For all training jobs, you have the option to use **global standard** (10-30% discount from regional standard training) or **developer** (50% discount from global). Neither Global nor Developer training guarantee data residency; developer training will run on pre-emptible spot capacity so may take longer to complete. Developer tier jobs may be paused by the system but automatically resume; you don't incur charges for jobs in paused states.

### The calculation formula

**Supervised Fine-Tuning (SFT) & Preference Fine-Tuning (DPO)**

It's straightforward to estimate the costs for SFT & DPO. You're charged based on the number of tokens in your training file, and the number of epochs for your training job.

$$
\text{price} = \text{\# training tokens} \times \text{\# epochs} \times \text{training price per token}
$$

In general, smaller models and more recent models have lower prices per token than larger, older models. To estimate the number of tokens in your file, you can use the [tiktoken library](https://github.com/openai/tiktoken) – or, for a less precise estimate, one word is roughly equivalent to four tokens.

Both regional and global training are available for SFT. If you don't need data residency, global training allows you to train at a discounted rate.

> [!IMPORTANT]
> You aren't charged for time spent in queue, failed jobs, jobs canceled prior to training beginning, or data safety checks. Training token price is different from inferencing input/output token price. For pricing details, see the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service).

#### Example: Supervised fine-tuning (SFT)

Projecting the hypothetical costs to fine-tune a model that takes natural language and outputs code.

1. Prepare the training data file: 500 prompt / response pairs, with a total of 1 million tokens, and a validation file with 20 examples and 40,000 tokens.
2. Configure training run:
      - Select base model (GPT-4.1)
      - Specify global training
      - Set hyperparameters to **default**. Algorithmically, training is set to 2 epochs.

Training runs for 2 hours, 15 minutes

**Total cost**:
  
$$
\$2 \div 1\text{M tokens} \times 1\text{M training tokens} \times 2\text{ epochs} = \$4
$$

### Reinforcement fine-tuning (RFT)

The cost is determined by the time spent on training the model for the reinforcement fine-tuning technique.

**The formula is:**

$$
\text{price} = \text{Time taken for training} \times \text{Hourly training cost} + \text{Grader inferencing per token (if model grader is used)}
$$

- **Time**: Total time in hours rounded to two decimal places (for example, 1.25 hours).
- **Hourly Training cost**: $100 per hour of core training time for `o4-mini-2025-04-16`. Refer to the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service) for actual pricing details.
- **Model grading**: Tokens used to grade outputs during training are billed separately at data zone rates once training is complete.

#### Example: Training model with graders (without model grader – Score_model)

This example projects the cost to train a customer service chatbot.

| Step | Time | Billable |
|------|------|----------|
| Submit fine-tuning job | 02:00 | No |
| Data preprocessing (includes safety checks) | 02:00–02:30 | No |
| Training | 02:30–06:30 | Yes (4 hours) |
| Model creation (includes safety steps) | After 06:30 | No |

**Final Calculation**:  

$$
\text{Total time taken for training} \times \text{Hourly training cost} = 4 \times 100 = \$200
$$

Your one-time investment to create this `o4-mini` custom fine-tuned model would be **$400.00**.

#### Example: Training a model with model 'Score_model' grader (o3-mini being used as grader)

This example projects the cost to train a customer service chatbot.

| Step | Time | Billable |
|------|------|----------|
| Submit fine-tuning job | 02:00 | No |
| Data preprocessing (includes safety checks) | 02:00–02:30 | No |
| Training | 02:30–06:30 | Yes (4 hours) |
| Model grader (5M input tokens, 4.9M output tokens) | During training | Yes (billed separately) |
| Model creation (includes safety steps) | After 06:30 | No |

**Final Calculation**:  

$$
\text{Total time taken for training} \times \text{Hourly training cost} = 4 \times 100 = \$400
$$

$$
\text{Grading costs} = \text{\# Input tokens} \times \text{Price per input token} + \text{Output tokens} \times \text{Price per output token}
$$

$$
= (5 \times 1.1) + (4.9 \times 4.4) = 5.5 + 21.56 = \$27.06
$$

$$
\text{Total training costs} = \$427.06
$$

Your one-time investment to create this o4-mini custom fine-tuned model would be **$427.06**.

### Managing costs and spending limits when using RFT

To control your spending, consider the following strategies:

| Strategy | Description |
|----------|-------------|
| Start small | Use shorter runs with `reasoning_effort` set to Low and smaller validation datasets to understand how your configuration affects time. |
| Limit validation | Use a reasonable number of validation examples and `eval_samples`. Avoid validating more often than you need. |
| Choose smallest grader | Select the smallest grader model that meets your quality requirements. |
| Adjust compute | Tune `compute_multiplier` to balance convergence speed and cost. |
| Monitor and cancel | Monitor your run in the Foundry portal or via the API. You can pause or cancel at any time. |

RFT jobs can lead to high training costs, so per-job billing is capped at **$5,000**. When a job reaches this limit, training pauses and a deployable checkpoint is created. You can validate the training job, metrics, and logs, then decide whether to resume. If you resume, billing continues with no further price limits.

### Job failures and cancellations

You aren't billed for work lost due to a service error. However, if you cancel a run, you'll be charged for the work completed up to that point.
  
**Example**: the run trains for 2 hours, writes a checkpoint, trains for 1 more hour, but then fails. Only the 2 hours of training up to the checkpoint are billable.

## Ongoing operational costs – using your model

After your model is trained, you can deploy it using one of the following hosting options:

- **Standard**: pay per-token at the same rate as base model Standard deployments with an additional $1.70/hour hosting fee. Offers regional data residency guarantees.
- **Global Standard**: pay per-token at the same rate as base model Global Standard deployments with an additional hosting fee. Doesn't offer data residency guarantees. Offers higher throughput than Standard deployments.
- **Regional Provisioned Throughput**: offers latency guarantees, designed for latency-sensitive workloads. Instead of paying per-token or an hourly hosting fee, deployments accrue PTU-hours based on the number of provisioned throughput units (PTU) assigned to the deployment, and billed at a rate determined by your agreements or reservations with Microsoft Azure.
- **Developer Tier**: pay per-token and without an hourly hosting fee but offers neither data residency nor availability guarantees. Developer Tier is designed for model candidate evaluation and proof of concepts, deployments are removed automatically after 24 hours regardless of usage but may be redeployed as needed.

The right deployment type for your use case depends on weighing your AI requirements and where you are on your fine-tuning journey.

| Deployment Type             | Availability | Latency | Token Rate         | Hourly Rate     |
|----------------------------|------------------|-------------|--------------------|-----------------|
| Standard                   | [SLA](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services)            | Best effort        | Same as base model | $1.70/hour      |
| Global Standard            | [SLA](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services)            | Best effort       | Same as base model | $1.70/hour      |
| Regional Provisioned Throughput | [SLA](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services)       | [PTU](/azure/ai-foundry/openai/concepts/provisioned-throughput?tabs=global-ptum#when-to-use-provisioned-throughput) | None         | PTU/hour        |
| Developer Tier             | None             | Best effort        | Same as Global Standard | None      |

Full pricing information for all models is available on the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service).

### Example for o4-mini

- Hosting charges: $1.70 per hour
- Input Cost: $1.10 per 1M tokens
- Output Cost: $4.40 per 1M tokens

#### Example: Monthly usage of a fine-tuned chatbot

Let's assume your chatbot handles 10,000 customer conversations in its first month:

- Hosting charges: $1.70 per hour
- Total Input: The user queries sent to the model total 20 million tokens.
- Total Output: The model's responses to users total 40 million tokens.
- Input Cost Calculation: 20× $1.10 = $22.00
- Output Cost Calculation: 40 × $4.40 = $176.00

Your total operational cost for the month would be:

Total Cost = Hosting charges + Token usage cost

$$
\text{Total Cost} = (1.70 \times 30 \times 24) + (22 + 176) = \$1422.00
$$

Always refer to the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service) for pricing information. The numbers in this article are for example purposes only.


## Next steps

- Get started with the [Foundry Models fine-tuning tutorial](../tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).
- Learn more about [Foundry Models quotas and limits](../quotas-limits.md).
