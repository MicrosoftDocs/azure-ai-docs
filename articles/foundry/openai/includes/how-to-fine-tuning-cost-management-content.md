---
title: include file
description: include file
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ai-usage: ai-assisted
ms.date: 10/05/2026
ms.custom: include, classic-and-new
---

Fine-tuning in Microsoft Foundry involves training costs and ongoing hosting and inference costs. Use this guide to estimate costs for managed fine-tuning jobs or interactive training sessions.

Training billing differs between the two approaches. Hosting and inference pricing works the same way for models trained with either approach, for the same model and deployment configuration.

## Prerequisites

- A model and training approach selected from the [fine-tuning overview](../../fine-tuning/overview.md#supported-models).
- Current rates for your model, training type, and deployment option from [fine-tuning pricing](https://aka.ms/oai/pricing).
- An approved budget for training, evaluation, and serving.

> [!IMPORTANT]
> Get current rates from [fine-tuning pricing](https://aka.ms/oai/pricing). The examples use symbolic rates with sample usage quantities. Substitute the rates for your model and configuration to calculate your costs.

<a id="upfront-investment---training-your-model"></a>

## Estimate managed fine-tuning costs

Each managed fine-tuning job incurs a training cost. Supervised fine-tuning (SFT) and preference fine-tuning (DPO) use token-based billing. Reinforcement fine-tuning (RFT) uses training-time billing, with separate model-grading costs when applicable.

Training rates differ between regional Standard, Global Standard, and Developer training. Compare the current rates for your supported model in [fine-tuning pricing](https://aka.ms/oai/pricing).

Neither global nor Developer training guarantees regional data residency. Developer training uses preemptible capacity, so a job might take longer to complete. Paused Developer jobs resume automatically, and you don't incur charges while they're paused.

<a id="the-calculation-formula"></a>

### Supervised fine-tuning and preference fine-tuning

You're charged based on the number of tokens in your training file and the number of epochs for your job.

$$
\text{price} = \text{\# training tokens} \times \text{\# epochs} \times \text{training price per token}
$$

Estimate the number of tokens with the tokenizer for your selected model.

Both regional and global training are available for SFT. If you don't need data residency, global training allows you to train at a discounted rate.

> [!IMPORTANT]
> You aren't charged for time spent in queue, failed jobs, jobs canceled prior to training beginning, or data safety checks. Training token price is different from inferencing input/output token price. For pricing details, see [fine-tuning pricing](https://aka.ms/oai/pricing).

#### Example: Supervised fine-tuning (SFT)

This example estimates the cost of a GPT-4.1 model that takes natural language and outputs code. Let `T` be its training rate per million tokens from [fine-tuning pricing](https://aka.ms/oai/pricing).

1. Prepare a training file with 500 prompt-response pairs totaling 1 million tokens, and a validation file with 20 examples totaling 40,000 tokens.
1. Select GPT-4.1 and global training.
1. Configure the run for two epochs.

The run takes 2 hours and 15 minutes. Its elapsed time doesn't determine the SFT training charge.

**Total cost**:
  
$$
\text{Training cost} = \frac{1{,}000{,}000 \times 2}{1{,}000{,}000} \times T = 2T
$$

### Reinforcement fine-tuning (RFT)

Managed RFT billing depends on the time spent training. If you use a model grader, its inference tokens are billed separately.

**The formula is:**

$$
\text{price} = \text{Time taken for training} \times \text{Hourly training cost} + \text{Grader inferencing per token (if model grader is used)}
$$

- **Time**: Total time in hours rounded to two decimal places (for example, 1.25 hours).
- **Hourly training cost**: The rate for your model and training type from [fine-tuning pricing](https://aka.ms/oai/pricing).
- **Model grading**: Tokens used to grade outputs during training are billed separately at data zone rates once training is complete.

#### Example: Training without a model grader

This example estimates the cost to train a customer service chatbot without a model grader. Let `H` be the hourly training rate for your model from [fine-tuning pricing](https://aka.ms/oai/pricing).

| Step | Time | Billable |
| --- | --- | --- |
| Submit fine-tuning job | 02:00 | No |
| Data preprocessing (includes safety checks) | 02:00–02:30 | No |
| Training | 02:30–06:30 | Yes (4 hours) |
| Model creation (includes safety steps) | After 06:30 | No |

**Final calculation**:

$$
\text{Training cost} = 4 \times H = 4H
$$

The job incurs four hours of training charges.

#### Example: Training with a model grader

This example uses `o3-mini` as a `score_model` grader. Get the following rates from [fine-tuning pricing](https://aka.ms/oai/pricing):

- `H`: Hourly training rate.
- `I`: Grader input rate per million tokens.
- `O`: Grader output rate per million tokens.

| Step | Time | Billable |
| --- | --- | --- |
| Submit fine-tuning job | 02:00 | No |
| Data preprocessing (includes safety checks) | 02:00–02:30 | No |
| Training | 02:30–06:30 | Yes (4 hours) |
| Model grader (5M input tokens, 4.9M output tokens) | During training | Yes (billed separately) |
| Model creation (includes safety steps) | After 06:30 | No |

**Final calculation**:

$$
\text{Training cost} = 4 \times H = 4H
$$

$$
\text{Grading costs} = \text{\# Input tokens} \times \text{Price per input token} + \text{Output tokens} \times \text{Price per output token}
$$

$$
\text{Grading cost} = (5 \times I) + (4.9 \times O) = 5I + 4.9O
$$

$$
\text{Total training cost} = 4H + 5I + 4.9O
$$

Add the training charge and both grading-token charges to estimate the job's total cost.

<a id="managing-costs-and-spending-limits-when-using-rft"></a>

### Manage RFT costs and spending limits

To control your spending, consider the following strategies:

| Strategy | Description |
| --- | --- |
| Start small | Use shorter runs with `reasoning_effort` set to Low and smaller validation datasets to understand how your configuration affects time. |
| Limit validation | Use a reasonable number of validation examples and `eval_samples`. Avoid validating more often than you need. |
| Choose smallest grader | Select the smallest grader model that meets your quality requirements. |
| Adjust compute | Tune `compute_multiplier` to balance convergence speed and cost. |
| Monitor and cancel | Monitor your run in the Foundry portal or via the API. You can pause or cancel at any time. |

Managed RFT jobs initially pause when combined training and grading costs reach the service's per-job spending limit. For current billing details, see [fine-tuning pricing](https://aka.ms/oai/pricing).

When a job reaches this limit, training pauses and a deployable checkpoint is created. Review the job, metrics, and logs before deciding whether to resume. If you resume, billing continues without another cost-based limit.

### Job failures and cancellations

For managed RFT, you aren't billed for work lost due to a service error. If you cancel a run, you're charged for work completed up to that point.
  
**Example**: the run trains for 2 hours, writes a checkpoint, trains for 1 more hour, but then fails. Only the 2 hours of training up to the checkpoint are billable.

## Estimate interactive training costs (preview)

Interactive training bills the tokens used by your training and sampling operations. It doesn't use the managed RFT hourly training formula.

Use [fine-tuning pricing](https://aka.ms/oai/pricing) for applicable rates, and confirm your training budget during [preview onboarding](../../fine-tuning/interactive-post-training/overview.md#access-and-supported-regions). Managed-job discounts and RFT spending limits don't define interactive-session pricing or limits.

### Billable token categories

Estimate each category separately, using its own token count and rate.

| Category | Usage |
| --- | --- |
| Prefill tokens | Input tokens processed for sampling that aren't served from the prompt cache. |
| Cached prefill tokens | Input tokens served from the prompt cache during sampling. |
| Sampling tokens | Output tokens generated by sampling operations. |
| Training tokens | Tokens processed by training operations. |

When rates are quoted per million tokens, calculate each charge as token count divided by 1,000,000, multiplied by the category's rate. Add the four charges:

$$
\begin{aligned}
\text{Interactive training cost} ={}&
\frac{\text{Prefill tokens}}{1{,}000{,}000} \times \text{Prefill rate} \\
&+ \frac{\text{Cached prefill tokens}}{1{,}000{,}000} \times \text{Cached prefill rate} \\
&+ \frac{\text{Sampling tokens}}{1{,}000{,}000} \times \text{Sampling rate} \\
&+ \frac{\text{Training tokens}}{1{,}000{,}000} \times \text{Training rate}
\end{aligned}
$$

Use cumulative usage across the run, not just the number of tokens in your original dataset. Separate cached and uncached prefill counts so you don't count the same input token under both prefill categories.

### Example: Interactive training run

Suppose an interactive run generates rollouts and performs training updates. The following table shows its cumulative usage.

Use the corresponding rates per million tokens from [fine-tuning pricing](https://aka.ms/oai/pricing). In this example, `P`, `C`, `S`, and `T` represent the prefill, cached prefill, sampling, and training rates.

| Category | Tokens | Rate per million tokens | Charge calculation |
| --- | --- | --- | --- |
| Prefill | 1,000,000 | `P` | `1 × P` |
| Cached prefill | 3,000,000 | `C` | `3 × C` |
| Sampling | 2,000,000 | `S` | `2 × S` |
| Training | 4,000,000 | `T` | `4 × T` |
| **Total** | | | `P + 3C + 2S + 4T` |

This total covers the interactive run only. Add any separate model-grading or evaluation inference costs and the cost of deploying the trained model.

<a id="ongoing-operational-costs--using-your-model"></a>

## Estimate hosting and inference costs

After training, select a deployment option for your model. The following billing models apply to models from both managed fine-tuning and interactive training. Model and artifact compatibility still determines which options you can use.

| Option | Billing model | Main cost drivers |
| --- | --- | --- |
| Serverless | Input and output tokens plus applicable hosting fees, or provisioned throughput units (PTUs). | Model, deployment type, token usage, and hosting time or provisioned capacity. |
| Fireworks on Foundry | Token-based offers for supported catalog models; provisioned throughput for imported custom models. | Model, supported offer, and token usage or PTU-hours. |
| Managed compute (preview) | GPU-hours at the rate for the selected accelerator family. | GPUs per instance, instance count, and deployment time. |

For compatibility and deployment instructions, see [Deploy fine-tuned models](../../fine-tuning/deploy-fine-tuned-models.md).

### Serverless

Serverless deployment pricing depends on the deployment type supported by your fine-tuned model.

| Deployment type | Inference charge | Hosting or capacity charge |
| --- | --- | --- |
| Standard | Input and output tokens at the applicable base-model Standard rates. | Fine-tuned-model hourly hosting fee. |
| Global Standard | Input and output tokens at the applicable base-model Global Standard rates. | Fine-tuned-model hourly hosting fee. |
| Regional Provisioned Throughput | No separate per-token charge. | PTU-hours, at the rate determined by your agreement or reservation. |
| Developer | Input and output tokens at the applicable Global Standard rates. | No hourly hosting fee. |

Developer deployments are for evaluation. They have no availability or data-residency guarantees and are removed after 24 hours, regardless of usage. You can redeploy them as needed.

For a token-based deployment, add the input and output token charges to any hourly hosting charge. For Provisioned Throughput, multiply allocated PTUs by deployment hours and the applicable PTU-hour rate.

<a id="example-for-o4-mini"></a>

#### Example: Monthly usage of a fine-tuned chatbot

Suppose a fine-tuned `o4-mini` chatbot handles 10,000 conversations and remains deployed for a 30-day month. Get these rates from [fine-tuning pricing](https://aka.ms/oai/pricing):

- `H`: Hourly hosting rate.
- `I`: Input rate per million tokens.
- `O`: Output rate per million tokens.

| Component | Usage | Rate | Charge calculation |
| --- | --- | --- | --- |
| Hosting | 720 hours | `H` per hour | `720 × H` |
| Input tokens | 20 million tokens | `I` per million tokens | `20 × I` |
| Output tokens | 40 million tokens | `O` per million tokens | `40 × O` |
| **Total** | | | `720H + 20I + 40O` |

The total is:

$$
\text{Total cost} = (H \times 30 \times 24) + (20 \times I) + (40 \times O) = 720H + 20I + 40O
$$

Substitute your model's rates to calculate the monthly hosting and inference cost.

### Fireworks on Foundry

Fireworks supports pay-per-token and provisioned throughput offers for supported catalog models. Imported custom models use provisioned throughput. Don't assume a catalog model's pay-per-token offer is available for its fine-tuned custom model.

For a token-based offer, calculate input and output token charges at the selected model's rates. For a custom-model provisioned deployment, calculate:

$$
\text{Serving cost} = \text{Allocated PTUs} \times \text{Deployment hours} \times \text{Rate per PTU-hour}
$$

PTU charges depend on allocated capacity and deployment time, rather than the number of requests you send. Review the pricing terms for your custom deployment.

#### Example: Provisioned custom-model deployment

Suppose you allocate 80 PTUs to a custom model for 10 hours. Let `U` be the rate per PTU-hour from [fine-tuning pricing](https://aka.ms/oai/pricing).

$$
\text{Serving cost} = 80 \times 10 \times U = 800U
$$

This example doesn't specify a minimum PTU allocation. Review the [custom-model deployment guide](../../how-to/fireworks/import-custom-models.md#deploy-the-imported-model) for deployment requirements.

### Managed compute (preview)

Managed compute bills GPU-hours, not inference tokens. Total GPUs equal the number of model instances multiplied by the GPUs per instance in the selected deployment template.

Hourly rates vary by accelerator family and deployment scope. Calculate the serving cost as:

$$
\text{Serving cost} = \text{GPUs per instance} \times \text{Instance count} \times \text{Deployment hours} \times \text{Rate per GPU-hour}
$$

Allocated GPU capacity incurs charges while the deployment runs, even when you aren't sending inference requests. Delete an unused deployment to release its accelerators and stop billing.

#### Example: GPU-backed deployment

Suppose a deployment uses two GPUs per instance and one instance for 10 hours. It consumes 20 GPU-hours. Let `G` be the rate per GPU-hour from [fine-tuning pricing](https://aka.ms/oai/pricing).

$$
\text{Serving cost} = 2 \times 1 \times 10 \times G = 20G
$$

If you change capacity during the billing period, calculate each interval separately and add the charges. See [managed compute billing](../../concepts/managed-compute-overview.md#billing-quota-and-deployment-scopes) for billing mechanics.

## Manage your spending

Budget for experimentation and serving separately. Repeat training runs, sampling, grading, and evaluation can add to the cost of the final model.

1. Select a compatible model and training approach, then confirm the applicable rates before starting a run.
1. Run a small experiment and measure training usage, sampling usage, and model quality before increasing the run size.
1. For interactive training, budget each of the four token categories. More rollouts or longer responses increase sampling usage.
1. Monitor deployed-model costs with [Cost Management](../../concepts/manage-costs.md), and set budget alerts for unexpected spending.
1. Remove deployments you no longer need, especially those with hourly hosting, PTU, or GPU charges.

## Related content

- [Choose a fine-tuning approach and model](../../fine-tuning/overview.md).
- [Deploy fine-tuned models](../../fine-tuning/deploy-fine-tuned-models.md).
- [Plan and manage Foundry costs](../../concepts/manage-costs.md).
