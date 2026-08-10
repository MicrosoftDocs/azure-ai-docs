---
title: "Quickstart: Optimize a prompt agent (preview)"
titleSuffix: Microsoft Foundry
description: "Optimize a prompt agent's instructions, function-calling tool descriptions, and model selection in the Foundry portal."
author: aahill
ms.author: aahi
ms.date: 08/04/2026
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to optimize a prompt agent so that I can improve its quality against representative tasks and evaluation criteria.
---

# Quickstart: Optimize a prompt agent (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

In this quickstart, use the optimization wizard in the Foundry portal to
improve a prompt agent's instructions, function-calling tool descriptions, and
model selection. Select an agent version, dataset, and evaluators, run the
optimizer, and compare the generated candidates with the baseline.

If you don't have an Azure subscription, create a
[free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Prerequisites

Before you begin, you need:

- A Microsoft Foundry project with a deployed prompt agent. To create one, see
  [Quickstart: Create a prompt agent](prompt-agent.md).
- An evaluation model and a supported optimization model deployed in the
  project. For supported models, see
  [Models](../concepts/agent-optimizer-overview.md#models).
- A dataset source: agent traces, an evaluation dataset registered in the
  project, or a JSONL dataset to upload. The dataset must use the column names
  required by the selected evaluators because the wizard doesn't support column
  mapping.

## Open the optimization wizard

:::image type="content" source="../media/quickstart/optimize-prompt-entry.png" alt-text="Screenshot of the Optimize tab for a prompt agent, with the Create optimization run button highlighted." lightbox="../media/quickstart/optimize-prompt-entry.png":::

1. Go to the [Foundry portal](https://ai.azure.com) and open your project.
1. Select **Agents**, and then select the prompt agent you want to optimize.
1. Select the **Optimize** tab.
1. Select **Create optimization run**.

## Select the optimization target

The target defines the prompt-agent version and candidate models to evaluate.

:::image type="content" source="../media/quickstart/optimize-prompt-target.png" alt-text="Screenshot of the Target step with controls for the agent version, optimization model, maximum candidates, evaluation model, and model comparison." lightbox="../media/quickstart/optimize-prompt-target.png":::

1. In the **Target** step, select the agent version to use as the baseline.
   The latest version is selected by default.
1. Select the optimization model, maximum number of candidates, and evaluation
   model.
1. To evaluate candidates across multiple model deployments, turn on
   **Compare across models**, and then select the models to include.
1. Continue to the **Dataset** step.

The optimizer can generate candidates that improve the agent's instructions,
function-calling tool descriptions, or model selection. Other tool types aren't
supported for tool-description optimization.

> [!IMPORTANT]
> A prompt agent's function-calling tools execute on the client side. The
> optimizer can improve the tool and parameter descriptions that guide function
> calls, but it can't execute or evaluate the tools during tool-description
> optimization.

## Select an evaluation dataset

The optimizer uses the same dataset to score the baseline and each generated
candidate.

1. In the **Dataset** step, choose one of these options:

   - Generate a dataset from agent traces.
   - Select an existing dataset registered in the project.
   - Upload a new dataset from your device.

1. Preview the dataset and confirm that it contains the columns required by
   your evaluators.
1. Continue to the **Criteria** step.

Use representative tasks, including common requests, edge cases, and behaviors
you want the optimizer to preserve or improve.

## Select evaluation criteria

Evaluators define how the optimizer scores each response.

1. In the **Criteria** step, select one or more evaluators:

   - Select built-in evaluators and configure any required parameters.
   - Select an existing custom evaluator.
   - Create a custom rubric evaluator, and then select it.

1. Confirm that each evaluator is compatible with the dataset schema.
1. Continue to the **Review** step.

## Review and submit the run

:::image type="content" source="../media/quickstart/optimize-prompt-submit.png" alt-text="Screenshot of the Review step summarizing the optimization target, dataset, criteria, and Submit button." lightbox="../media/quickstart/optimize-prompt-submit.png":::

1. On the **Review** step, verify the agent and version, dataset, evaluators,
   evaluator configurations, and candidate models.
1. Select **Submit**.
1. Wait for the optimization run to finish. The run appears in the
   **Optimization runs** list with its current status.

Run time depends on the dataset size, number of candidates, and selected
models.

## Compare the results

1. When the run succeeds, select it under **Optimization runs**.
1. Compare each candidate's score with the baseline score.
1. Review the before-and-after instruction changes.
1. Inspect the per-evaluator scores and, if you selected multiple models,
   compare the results for each model.
1. Select the candidate that provides a meaningful quality improvement without
   an unacceptable increase in token usage or cost.

If every candidate scores lower than the baseline, keep the current agent.
Revise the dataset, evaluators, or optimization settings before you run the
optimizer again.

## Promote a candidate

Promote the selected candidate to create a new version of the prompt agent.

1. On the completed run page, select **Promote candidate**.
1. In **Promote candidate as new agent version**, select the candidate to
   promote.
1. Review the current active version and the selected candidate's score
   improvement over the baseline.
1. Select **Promote to agent version**.

The promotion creates a new agent version with the candidate's optimized
configuration. If the agent is pinned to a specific version, the new version
doesn't receive traffic until you set it as the active version in the agent's
details.

## What you learned

In this quickstart, you:

- Started a prompt-agent optimization run in the Foundry portal.
- Selected a dataset, evaluators, and candidate models.
- Compared optimized candidates with the prompt-agent baseline.
- Promoted the selected candidate to a new prompt-agent version.

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Quickstart: Optimize a hosted agent](quickstart-optimize-hosted-agent.md)
- [Convert agent traces into evaluation datasets](../../observability/how-to/traces-to-dataset.md)
