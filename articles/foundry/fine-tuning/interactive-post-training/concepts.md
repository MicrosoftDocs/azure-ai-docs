---
title: Key concepts for interactive training (preview) in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Understand how training sessions, adapters, rewards, model updates, and checkpoints fit together in interactive training.
author: chillatom
ms.author: coreyhill
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 10/07/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Key concepts for interactive training (preview) in Microsoft Foundry

<a id="key-concepts-for-interactive-post-training-preview-sessions-checkpoints-and-how-training-runs"></a>

[!INCLUDE [Feature preview](../../includes/feature-preview.md)]

[!INCLUDE [Interactive training preview access](../../includes/interactive-training-preview-access.md)]

Interactive training lets your program control how a model learns while Microsoft Foundry runs the model. Your program, also called a **training driver**, chooses the examples, evaluates responses, and decides when to update the model.

The concepts below explain how the parts of a training loop fit together. For code and implementation details, see the [SDK cheatsheet](sdk-cheatsheet.md).

## Training sessions

A **training session** holds the model and its current training progress while your experiment runs. Your driver requests individual operations, such as generating responses or applying an update.

A session serves a different purpose from a managed job or deployment:

| Resource | Purpose |
| --- | --- |
| **Interactive training session** | Your program controls the training loop one operation at a time. |
| **Managed fine-tuning job** | The service runs a predefined training workflow from the data and settings you provide. |
| **Serving deployment** | A trained model answers requests from an application. |

Your driver keeps the session active while the experiment runs. Progress held only in the session isn't a durable record; a completed training checkpoint preserves it.

## LoRA adapters

<a id="lora-configuration"></a>

A **base model** is the model you start with. Its **weights** are the learned values that shape its behavior.

A **low-rank adaptation (LoRA) adapter** is a small set of trainable weights added to the base model. Training changes the adapter rather than retraining all the model's original weights.

The adapter contains what your experiment learns. It remains tied to a compatible base model; it isn't a standalone replacement for that model.

For implementation details, see [Create a session](sdk-cheatsheet.md#create-a-session).

## Training tiers

<a id="training-tier-selection"></a>

A **training tier** describes the service option used to run training. Tiers can differ in where training runs, how capacity is provided, and the service guarantees that apply.

The options available to you depend on the model, region, and project. Training tiers are separate from deployment options used to serve a trained model. See [Training types](../overview.md#training-types).

## Message formatting

<a id="format-model-inputs"></a>

Your messages need to be converted into a form the selected model understands. That format also distinguishes user prompts, assistant responses, and information returned by tools.

- **Tokens** are small units of text, such as words or word parts, that the model reads and generates.
- **A tokenizer** converts text into tokens and tokens back into text.
- **A chat template** organizes messages so the model can distinguish speakers and recognize where a response begins.
- **A renderer** prepares messages in the model's format and converts generated responses back into readable content.

Different models can use different message formats. Consistent formatting helps the training program identify which parts of an interaction should contribute to learning.

Image-based training also requires a compatible vision-language model and image-training support for your project. A message formatter that understands images doesn't establish that training is available for them.

## The training loop

<a id="primitives"></a>

Interactive training separates generating responses, calculating learning signals, and applying updates. Your driver combines these operations into a workflow.

| Operation | What it means |
| --- | --- |
| **Sampling** | The model generates responses from a selected snapshot of the adapter. |
| **Forward pass** | The model processes examples so you can measure loss or inspect learning signals without accumulating changes for an update. |
| **Gradient computation** | Training calculates how the adapter's weights could change to improve the learning objective. |
| **Optimizer update** | The optimizer applies the accumulated gradients to change the adapter. |
| **Evaluation** | Your driver measures performance on examples kept separate from training. |

**Gradients** describe potential changes to the adapter. An **optimizer** turns those gradients into an update. Calculating gradients doesn't change the adapter by itself.

Several sets of examples can contribute gradients to one update. After an update, sampling needs a refreshed snapshot to use the adapter's latest learned state.

Evaluation uses **held-out examples**, which aren't used for training, to check performance on the task you care about. A lower training loss or higher training reward alone doesn't establish better performance.

For the corresponding operations in code, see the [SDK cheatsheet](sdk-cheatsheet.md).

## Loss functions and token weights

A **loss function** expresses the objective that training tries to improve. It turns examples and learning signals into a measure that guides changes to the adapter.

| Learning approach | What guides the update |
| --- | --- |
| **Supervised learning** | Desired responses show the model what to produce. |
| **Reinforcement learning** | Scores and comparisons between generated responses guide which behavior to strengthen. |

A loss function is one part of a workflow. It doesn't choose your examples, grade responses, or decide when training stops.

**Token weights** control how strongly parts of an example contribute to learning. **Masks** exclude parts that shouldn't contribute.

For example, a supervised-learning workflow can learn from the assistant's response without learning to reproduce the user's prompt.

For reinforcement learning, the learning signal also distinguishes model-generated responses from information supplied by the user or environment. It uses information from the model that generated each response, even if the model changes later.

Custom objectives can combine model outputs with calculations in your driver. The driver still coordinates the learning signals and model updates.

For data structures and examples, see [Prepare supervised data](sdk-cheatsheet.md#prepare-supervised-data) and [Prepare RL data](sdk-cheatsheet.md#prepare-rl-data).

### How learning signals are combined

<a id="keep-loss-reduction-consistent"></a>

Different objectives can combine learning signals differently, such as adding them together or averaging them. Combining incompatible approaches in one update can change its scale or cause the service to reject it.

Contributions to the same update need a consistent way of combining learning signals. An update completes before the workflow switches to an incompatible approach.

## Rewards, rollouts, and advantages

In reinforcement learning, your driver evaluates what the model does and turns that evaluation into a learning signal.

| Concept | Meaning |
| --- | --- |
| **Rollout** | A generated response or a longer interaction that can include tool calls and observations. |
| **Reward** | A score that describes how well a rollout meets the task's goal. Your program assigns this score. |
| **Advantage** | A comparison that indicates whether a response performs better or worse than a reference, such as other responses to the same prompt. |

One approach generates several responses to the same prompt and compares each reward with the group's average reward:

- **Above average:** The response has a positive advantage.
- **Below average:** The response has a negative advantage.
- **Equal rewards:** All responses have zero advantage, so this comparison supplies no learning signal.

For a math task, the reward can reflect whether the final answer is correct. A high formatting score alone doesn't establish that the answer is correct.

Your driver defines the grading rules and comparison method. For complete examples, explore the [fine-tuning samples repository](https://github.com/microsoft-foundry/fine-tuning).

## Operation completion

Each operation takes time to run. The service accepting a request is different from finishing the requested work.

| Status | What it tells you |
| --- | --- |
| **Accepted** | The service receives the request. The work might still be waiting or running. |
| **Completed** | The operation finishes, and its result can be used by a dependent operation. |
| **Timed out** | Your driver stops waiting. This doesn't prove that the operation fails or stops on the service. |

The order matters: an update depends on completed gradient computation, and sampling from new weights depends on a completed refresh. A missing result isn't a successful result or a zero-valued measurement.

For implementation details, see [Use asynchronous operations](sdk-cheatsheet.md#use-asynchronous-operations).

## Checkpoints

A **checkpoint** records model state at a particular point. Training checkpoints and sampler checkpoints preserve different information.

| Type | What it preserves | What you use it for |
| --- | --- | --- |
| **Training checkpoint** | The adapter's learned weights and the optimizer's record of earlier updates. | Recovering progress or continuing training in a compatible session. |
| **Sampler checkpoint** | A snapshot of adapter weights for generating responses. | Sampling from a selected version of the adapter, without the information needed to resume training. |

A sampler refresh prepares the latest adapter state for generation. It isn't a substitute for a saved training checkpoint, and it doesn't necessarily create a persistent artifact.

Your driver has its own progress to preserve, such as which examples it has already used and when evaluation occurs. A model checkpoint doesn't restore that progress automatically.

Neither checkpoint type is an application endpoint. Using the trained model in an application is a separate deployment task.

For code examples, see [Save and resume training](sdk-cheatsheet.md#save-and-resume-training).

## Session lifecycle

<a id="inspect-and-unload-sessions"></a>

Unloading releases a session's active training resources. It serves a different purpose from deleting the session and its saved artifacts.

| Action | Meaning |
| --- | --- |
| **Inspect** | Check the session's status and identify its saved checkpoints. |
| **Unload** | Release the active session's compute resources. This isn't checkpoint deletion. |
| **Delete** | Remove the session. This can also remove its checkpoints and sampling resources. |

Submitting an unload request doesn't confirm that cleanup completes. Closing your driver's network connection also isn't the same as unloading the session.

A completed training checkpoint preserves progress before a session ends. Deleting the session can remove that saved state, so deletion isn't interchangeable with releasing compute.

For implementation details, see [Close resources](sdk-cheatsheet.md#close-resources).

## Related content

Explore these resources when you're ready to use the concepts:

- [Get started with interactive training](quickstart.md) to run a short training recipe.
- [SDK cheatsheet](sdk-cheatsheet.md) for code examples and implementation details.
- [Fine-tuning samples on GitHub](https://github.com/microsoft-foundry/fine-tuning) for complete training workflows.
