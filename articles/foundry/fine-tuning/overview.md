---
title: Fine-tuning in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn when to fine-tune, compare managed fine-tuning and interactive training, and choose models, methods, training tiers, and deployment options.
author: chillatom
ms.author: coreyhill
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: overview
ms.date: 10/06/2026
ms.custom: doc-kit-assisted, references_regions
ai-usage: ai-assisted
---

# Fine-tuning in Microsoft Foundry

<a id="when-to-use-fine-tuning"></a>

Fine-tuning adapts a pretrained model to your task through additional training on task-specific data. It adjusts the model's weights rather than adding examples to each prompt. You build on the model's existing capabilities without training a model from scratch.

Fine-tuning can help when you have high-quality, task-specific training data and want to:

- **Improve accuracy and relevance.** Training on more examples than fit in a prompt can teach task-specific patterns.
- **Reduce prompt overhead.** Fewer prompt examples can lower token costs and latency.
- **Align style and structure.** Responses can follow a consistent tone, format, or schema.
- **Improve tool use.** Training examples can improve tool selection and argument accuracy.
- **Use retrieved context effectively.** Models can learn to prioritize relevant context and ignore irrelevant information.
- **Specialize a smaller model.** Teacher-generated examples can help a smaller model meet task requirements at lower cost and latency.

Benefits aren't guaranteed; held-out evaluation helps you compare the fine-tuned model with your baseline. Fine-tuning adds [training and hosting costs](cost-management.md) and doesn't replace retrieval for current information or application-level safety controls.

## Choose your training approach

Microsoft Foundry provides two training approaches. **[Managed fine-tuning](../openai/how-to/fine-tuning.md)** runs a training job from your data and settings. **[Interactive training (preview)](interactive-post-training/overview.md)** lets you control training steps in Python.

Both use Foundry-managed training infrastructure; you don't provision training GPUs.

> [!NOTE]
> Interactive training is in preview and requires explicit access approval. Request access through the [preview sign-up form](https://aka.ms/foundry-interactive-training-signup) and wait for approval before creating training sessions.

| | Managed fine-tuning | Interactive training (preview) |
| --- | --- | --- |
| **How it works** | Submit data and settings; Foundry runs the training job. | Write a Python loop; Foundry executes training and sampling operations. |
| **Best for** | Beginners and AI engineers who prefer predefined workflows over lower-level training operations. | Experienced ML practitioners building custom training workflows. |
| **Your control** | Data, supported hyperparameters, and RFT graders. | Losses, rewards, rollouts, gradient accumulation, updates, and checkpoints. |
| **Training methods** | Model-specific SFT, DPO, and RFT; distillation through teacher-generated SFT data. | Recipes for SFT, reinforcement learning, preference learning, distillation, and custom losses. |
| **Example use cases** | Distill a larger model, learn from support conversations, or improve responses with a grader. | Collect tool-use rollouts, apply custom rewards, or change training-loop update and evaluation behavior. |

> [!TIP]
> Start with managed fine-tuning if you're new to model customization. It provides predefined workflows without requiring you to implement individual training operations.

Model requirements can constrain this choice. A model supported for one approach, method, or modality isn't automatically supported for another. Cookbook recipe support also doesn't establish service availability. Check the [supported models table](#supported-models) below for available combinations.

## Customization methods

Customization methods determine how a model learns from training data or feedback, such as desired responses, preferences, or rewards.

| Method | Training signal | When it fits |
| --- | --- | --- |
| [Supervised fine-tuning (SFT)](../openai/how-to/fine-tuning.md) | Prompts and desired responses. | You can demonstrate the behavior the model should learn. |
| [Preference fine-tuning, using direct preference optimization (DPO)](../openai/how-to/fine-tuning-direct-preference-optimization.md) | Preferred and rejected responses to the same input. | Quality depends on preferences such as tone or completeness, rather than one correct answer. |
| [Reinforcement fine-tuning (RFT)](../openai/how-to/reinforcement-fine-tuning.md) | Prompts and a grader that scores generated responses. | Multiple solutions are possible, and you can reliably score their quality. |

The predefined methods in this table apply only to managed fine-tuning. Interactive training exposes training primitives for building custom training workflows.

## Training types

Training types define where training runs and how capacity, pricing, and service guarantees apply. They're separate from deployment types, which determine how you serve a trained model.

| Training type | Description |
| --- | --- |
| Standard | Training occurs in the current Foundry resource's region and provides guarantees for data residency. Ideal for workloads where data must remain in a specific region. |
| Data zone | Training occurs within a supported data zone rather than a single region. Ideal for workloads where data must remain within that zone. ***Only the US data zone is currently supported.*** |
| Global | Provides more affordable pricing compared to Standard by using capacity beyond your current region. Data and weights are copied to the region where training occurs. Ideal if data residency is not a restriction and you want faster queue times. |
| Developer | Provides significant cost savings by using idle capacity for training. There are no latency or SLA guarantees, so jobs in this tier might be automatically preempted and resumed later. There are no guarantees for data residency either. Ideal for experimentation and price-sensitive workloads. |

<a id="deployment-types"></a>

## Deployment options

Foundry offers three deployment options with different serving infrastructure and billing models.

- **Serverless**: Foundry hosts the fine-tuned model and manages the serving infrastructure.
- **Managed compute (preview)**: Dedicated GPU capacity runs a matching base model with one or more compatible LoRA adapters.
- **Fireworks on Foundry (preview)**: The Fireworks runtime serves one adapter merged into a full-weight copy of the base model.

Serverless and Fireworks offer different deployment types, which determine the processing geography, capacity, and billing model. Availability depends on the model, deployment option, and artifact.

| Deployment type | Description |
| --- | --- |
| Standard | Runs inference in the deployment's region with per-token billing and applicable fine-tuned-model hosting charges. |
| Data Zone Standard | Runs inference within a supported data zone with per-token billing. ***Only the US data zone is supported.*** |
| Global Standard | Uses global capacity with per-token billing. Custom model weights might temporarily be stored outside the resource's geography. |
| Developer | Runs inference globally with per-token billing and no hourly hosting fee or data-residency guarantee. For evaluation only; lasts 24 hours and has no availability SLA. |
| Provisioned Throughput | Provides regional capacity billed in provisioned throughput units (PTUs) for predictable throughput. |
| Global Provisioned | Uses global capacity with PTU-based billing for imported custom models. |

## Supported models

Your requirements might call for a specific model or training approach. Use the table to check which combinations support your customization method, training type, and deployment option.

[!INCLUDE [Fine-tuning model support](../includes/fine-tune-supported-models.md)]

<a id="supported-regions"></a>

## Supported global training regions

[!INCLUDE [Fine-tuning region support](../openai/includes/fine-tune-global-training-regions.md)]

## Supported Standard deployment regions

[!INCLUDE [Standard deployment region support](../includes/fine-tune-standard-deployment-regions.md)]

## Supported Provisioned Throughput deployment regions

[!INCLUDE [Provisioned Throughput deployment region support](../includes/fine-tune-provisioned-throughput-deployment-regions.md)]

## Challenges and limitations

Fine-tuning is an iterative engineering process, not a guaranteed improvement.

| Challenge | How to address it |
| --- | --- |
| Data quality and coverage | Use accurate, consistent, representative examples. Inspect missing scenarios, duplicates, bias, and sensitive information before uploading data. |
| Overfitting and evaluation leakage | Separate training, validation, and final test data. Compare checkpoints on held-out tasks, not just training loss. |
| Misleading reward signals | Test RFT graders against correct, incorrect, and adversarial responses. Rising reward doesn't establish better task performance if the model exploits the grader. |
| Experimentation and cost | Budget for repeated runs, grading, evaluation, hosting, and inference. Stop experiments that don't improve the target metric. |
| Model and serving compatibility | Confirm method, tier, version, and deployment eligibility before training. An adapter isn't interchangeable across similarly named base models. |
| Maintenance | Reassess quality as task data changes or a base model approaches retirement. Retraining and redeployment can be necessary. |
| Safety and governance | Review data handling and managed safety evaluation. Keep application-level safety controls and evaluate the final serving runtime. |
| Interactive runtime responsibilities | Maintain your driver, environments, tokenization, checkpoints, and recovery logic. In-session sampling isn't proof of production serving behavior. |

## Next steps

<a id="get-started"></a>

Start with the guide for your training approach, then deploy and evaluate your fine-tuned model.

- [Customize a model with supervised fine-tuning](../openai/how-to/fine-tuning.md).
- [Customize a model with direct preference optimization](../openai/how-to/fine-tuning-direct-preference-optimization.md).
- [Customize a model with reinforcement fine-tuning](../openai/how-to/reinforcement-fine-tuning.md).
- [Get started with interactive training](interactive-post-training/quickstart.md).
- [Customize a premium healthcare AI model](../how-to/healthcare-ai/fine-tune-premium-healthcare-models.md).
- [Deploy fine-tuned models](deploy-fine-tuned-models.md).
- [Run evaluations from the Foundry portal](../how-to/evaluate-generative-ai-app.md).
- [Explore fine-tuning samples on GitHub](https://github.com/microsoft-foundry/fine-tuning).
