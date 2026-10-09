---
title: Troubleshoot interactive training (preview) in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Diagnose access, capacity, training, checkpoint, and evaluation errors without replaying ambiguous optimizer updates.
author: chillatom
ms.author: coreyhill
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: troubleshooting
ms.date: 10/06/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Troubleshoot interactive training (preview) in Microsoft Foundry

<a id="troubleshoot-interactive-post-training-preview"></a>

[!INCLUDE [Feature preview](../../includes/feature-preview.md)]

[!INCLUDE [Interactive training preview access](../../includes/interactive-training-preview-access.md)]

Use this article to troubleshoot interactive training in Microsoft Foundry.

## Common symptoms

Use typed SDK errors and their attributes rather than matching message text.

| Symptom or error | What to check |
| --- | --- |
| Access or authorization rejected | Verify the project endpoint, credential identity, permissions, and [explicit preview approval](overview.md#access-and-supported-regions). Installing the SDK doesn't enable access. |
| `NoCapacityError` | Confirm model eligibility and project capacity. Honor a supplied retry hint rather than repeatedly creating sessions. |
| `BatchTooLargeError` | Inspect reported limits. Reduce examples or sequence length, or accumulate supported batches before an optimizer step. |
| Rank or training tier rejected | Check [low-rank adaptation (LoRA) configuration](concepts.md#lora-configuration) and [training-tier selection](concepts.md#training-tier-selection). SDK fields don't establish model availability. |
| Training input rejected | Verify next-token alignment, tensor lengths, explicit weights, and the selected model's input support. |
| `TrainingEngineError` | Stop using the failed session. Recover from a completed training checkpoint and retain available diagnostic references. |
| `OperationResultUnavailableError` | Inspect `operation_completed`. Don't repeat an update that might already have completed. |
| Mixed-loss accumulation rejected | Complete the optimizer step before switching incompatible [loss-reduction groups](concepts.md#keep-loss-reduction-consistent). |
| Sampling uses old weights | Refresh sampler weights after the update and use the completed sampler checkpoint identifier for the correct session. |
| Resume uses the wrong data position | Restore driver state separately. A service checkpoint doesn't restore the notebook's dataset cursor or schedule. |
| Imports don't resolve | Check the installed `azure-ai-finetuningsessions` version and `azure.ai.finetuningsessions` namespace against [Get started](quickstart.md#install-and-configure). |

For exception types and attributes, see the [Python SDK documentation](/python/api/overview/azure/ai-finetuningsessions-readme?view=azure-python-preview&preserve-view=true).

## Reinforcement learning doesn't improve

Inspect complete rollouts and held-out results before increasing the run size.

| Symptom | What to check |
| --- | --- |
| Reward remains zero | Look for truncated or unparseable answers. Test the grader on known correct and incorrect responses, including malformed outputs. |
| Advantages are zero | Inspect rewards within each prompt group. Equal rewards produce zero centered advantages even if rewards vary across groups. |
| Training reward rises, but held-out performance doesn't | Separate task correctness from formatting rewards. Check for shortcuts, data leakage, and changes to the evaluation budget. |
| Tool-use rollouts fail | Check your driver-side tools, environment, data access, and formatting. Session operations don't automatically provision these dependencies. |
| Results change after recovery | Confirm checkpoint identity, restored driver state, sampling settings, and grader version before continuing updates. |

For worked training and evaluation examples, explore the [fine-tuning samples repository](https://github.com/microsoft-foundry/fine-tuning).

## Don't replay ambiguous updates

A client timeout doesn't prove that a remote operation failed or stopped. An optimizer update can complete even when its result isn't available.

Inspect the existing operation rather than submitting it again. Preserve the last confirmed checkpoint, update index, and driver state. If state is uncertain, [recover from a completed checkpoint](sdk-cheatsheet.md#save-and-resume-training).

Never interpret a missing loss or result as a successful zero-valued outcome. A session's lifecycle status doesn't establish completion of an individual request.

## Check cleanup and deployment separately

If normal cleanup fails, stop the owning driver and [inspect and unload the correct session](concepts.md#inspect-and-unload-sessions). Save required state first. Unloading and closing local clients aren't checkpoint deletion.

A training or sampler checkpoint isn't a serving endpoint. Confirm artifact compatibility, provider access, and serving capacity through the [deployment guide](../deploy-fine-tuned-models.md). Changing training parameters doesn't resolve missing deployment features or quota.

## Gather support details

Record the project and region, installed SDK version, selected model and training tier, session ID, and checkpoint reference. Include the request or operation ID, error type, and diagnostic reference when available.

Provide a sanitized, timestamped account of the last confirmed step and relevant experiment settings. Keep session status separate from operation completion.

Don't include credentials, private datasets, full customer prompts, or unrestricted HTTP body logs. Review notebook outputs and rollout traces before sharing them.

## Related content

- [Key concepts](concepts.md).
- [SDK cheatsheet](sdk-cheatsheet.md).
- [Azure support](https://azure.microsoft.com/support/create-ticket/).
