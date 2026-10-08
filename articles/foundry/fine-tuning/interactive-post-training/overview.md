---
title: What is interactive training (preview) in Microsoft Foundry?
titleSuffix: Microsoft Foundry
description: Build your own post-training loop with sampling, rewards, gradient updates, and checkpoints while Microsoft Foundry runs open-weight models on serverless GPUs.
author: chillatom
ms.author: coreyhill
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: overview
ms.date: 10/06/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# What is interactive training (preview) in Microsoft Foundry?

<a id="what-is-interactive-post-training-preview-in-microsoft-foundry"></a>

[!INCLUDE [Feature preview](../../includes/feature-preview.md)]

[!INCLUDE [Interactive training preview access](../../includes/interactive-training-preview-access.md)]

Interactive training (preview) is an API for building your own post-training loop over open-weight models in Microsoft Foundry. You control the experiment in Python. Foundry runs model sampling and low-rank adaptation (LoRA) updates on serverless GPUs.

For reinforcement learning (RL), your code controls rollout collection, rewards, advantages, and update scheduling. The same primitives support supervised learning, preference learning, distillation, and custom-loss workflows.

## When to use it

Use interactive training when the training loop itself is part of your research:

- **You need a custom learning signal.** Supply demonstrations, compute rewards and advantages, or compose a local loss for preference learning or other objectives.
- **Your model interacts with an environment.** Coordinate model responses, tool calls, observations, and rewards in your driver.
- **You need control over individual updates.** Select batches, token masks, loss settings, and optimizer parameters. Decide when to accumulate gradients and apply an update.
- **You want to inspect and adapt an experiment.** Sample from the current adapter, evaluate on held-out prompts, and choose the next prompts based on observed results.
- **You need to preserve and continue progress.** Save adapter and optimizer state, then resume in a compatible session. Keep dataset position and other experiment state in your driver.

Managed fine-tuning also supports graders for reinforcement fine-tuning. Choose interactive training when you need control over the loop, not just the grader or job settings. See [Choose your training approach](../overview.md#choose-your-training-approach).

## Who does what

Your Python program is the training driver. It prepares inputs and coordinates the experiment. Foundry maintains the model and adapter state and executes the requested operations.

[![Diagram separating your Python driver from Foundry model execution. The driver owns tokenization, rewards, advantages, objectives, and experiment scheduling. It sends tokens and operation requests to Foundry and receives samples, log probabilities, metrics, and checkpoint IDs. Foundry executes sampling, forward and backward passes, and optimizer updates and manages checkpoint operations.](../../media/interactive-training/driver-service-boundary.svg)](../../media/interactive-training/driver-service-boundary.svg)

Your driver can run on a CPU, including your own machine or a compute environment. A reward model or environment you add can have its own compute requirements. Keep the driver running while it manages the loop.

## Core concepts and primitives

A session is stateful: gradient computation, optimizer updates, and sampling are separate operations on a selected model and adapter. This separation lets you choose when to collect data, accumulate gradients, update, and evaluate.

| Building block | What it does |
| --- | --- |
| Training session and LoRA adapter | `FineTuningSession.create` initializes a supported base model with your adapter configuration. The session holds the state used by subsequent operations. |
| Tokenized batch and masks | `Datum` carries model inputs and loss inputs. Masks select which tokens contribute to learning, such as assistant tokens rather than prompts or tool observations. |
| Sampling | `sample` generates responses from a selected sampler checkpoint. RL inputs pair sampled tokens with their rollout log probabilities and reward-derived advantages. |
| Forward and backward passes | `forward` returns per-example loss-function outputs without accumulating gradients. `forward_backward` computes the selected objective and accumulates gradients. It doesn't apply an optimizer update. |
| Optimizer update | `optim_step` applies accumulated gradients with your Adam parameters. You choose when to update and which learning rate to use. |
| Sampler checkpoint | `save_weights_for_sampler` prepares adapter weights for generation. Refresh these weights after an update before sampling from the updated adapter. |
| Training checkpoint | `save_weights` persists adapter weights and optimizer state. `FineTuningSession.create_from_checkpoint` resumes training in a compatible session. |

The SDK includes `cross_entropy` for supervised updates and RL losses such as `importance_sampling` and `ppo`. These losses are loss primitives, not predefined end-to-end algorithms. For input contracts and custom-loss composition, see [Key concepts](concepts.md#loss-functions-and-token-weights).

## How an RL loop works

Consider a math-reasoning experiment: your model generates several answers to each problem, and your program grades their correctness. For a worked example, follow [Get started](quickstart.md).

[![Diagram of one RL iteration. Foundry refreshes sampler weights and samples rollouts. Your driver computes rewards, advantages, and token masks. Foundry computes gradients and applies the optimizer update. The loop returns to refresh sampler weights before collecting new rollouts.](../../media/interactive-training/reinforcement-learning-iteration-overview.svg)](../../media/interactive-training/reinforcement-learning-iteration-overview.svg)

Establish a held-out baseline and test your reward function before the first update. Then repeat:

1. **Prepare the current policy for sampling.** Save sampler weights from the training adapter, then collect several responses, or *rollouts*, for each prompt.
1. **Score and compare responses.** Your reward function assigns a score to each rollout. Subtract the prompt group's mean reward to produce each rollout's *advantage*.
1. **Prepare the learning signal.** Align sampled assistant tokens with their rollout log probabilities and advantages. Exclude prompts and environment observations from the learning signal.
1. **Compute gradients.** Submit the batch to `forward_backward` with `importance_sampling`. Complete the gradient computation before the update that consumes it.
1. **Update the adapter.** Call `optim_step`, then refresh sampler weights before collecting responses from the updated policy.
1. **Evaluate and preserve progress.** Compare held-out correctness with the baseline and save training checkpoints at your chosen cadence.

## Get started

Choose the starting point that fits your task:

- **Quickstart:** Follow the [quickstart sample](quickstart.md) to clone the repository and run a short reinforcement-learning recipe.
- **Try other recipes:** Explore the [fine-tuning samples repository](https://github.com/microsoft-foundry/fine-tuning) for more training examples.
- **Look up an operation:** Use the [SDK cheatsheet (preview)](sdk-cheatsheet.md) for functions and key parameters.
- **Understand the training loop:** Read [Key concepts](concepts.md) for rewards, advantages, token masks, and checkpoints.

## Supported models and regions

<a id="supported-models"></a>
<a id="access-and-supported-regions"></a>
<a id="access-regions-quotas-pricing-and-roles"></a>

See the fine-tuning overview for [supported models](../overview.md#supported-models) and [supported regions](../overview.md#supported-regions).

## Related content

- [Fine-tuning overview](../overview.md).
- [Get started with interactive training](quickstart.md).
- [SDK cheatsheet (preview)](sdk-cheatsheet.md).
- [Interactive training costs](../cost-management.md#estimate-interactive-training-costs-preview).
- [Fine-tuning samples on GitHub](https://github.com/microsoft-foundry/fine-tuning).
