---
title: Upgrade or switch models with Ask AI
titleSuffix: Microsoft Foundry
description: Learn how to use Ask AI in the Microsoft Foundry portal to detect deprecated models, evaluate alternatives, upgrade deployments, and update agents to newer model versions.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/13/2026
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
#CustomerIntent: As a developer or AI engineer, I want to identify deprecated or outdated models and upgrade them so that my agents use the best available model version.
---

# Upgrade or switch models with Ask AI (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Use Ask AI — the built-in chat assistant in the Microsoft Foundry portal — to detect deprecated or outdated models, compare alternatives, and upgrade deployed models or agents to newer versions. Review upgrade recommendations, evaluate the new model, compare performance, and update your agent — all from the Ask AI chat panel.

> [!NOTE]
> Ask AI model upgrade recommendations are available for models deployed through Foundry Models. For information about Ask AI capabilities and availability, see [What is Ask AI?](../../../concepts/ask-ai.md)

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with one or more deployed models or [agents](../../../agents/overview.md).
- Access to **Ask AI** (the chat assistant) in the Foundry portal.
- At least one [evaluation dataset](../../../how-to/develop/cloud-evaluation.md) in CSV or JSONL format. The dataset should include columns for the input query and the expected (ground truth) response for your scenario. For dataset preparation guidance, see [Evaluate your generative AI app](../../../how-to/evaluate-generative-ai-app.md?view=foundry&preserve-view=true).
- **Contributor** role (or higher) on the Foundry resource to deploy models, and **Azure AI User** role (or higher) on the Foundry project to build and run evaluations. For more information, see [Role-based access control for Microsoft Foundry](../../../concepts/rbac-foundry.md).

## Open a chat session in Ask AI

You can start a chat with Ask AI from any page in the Foundry portal.

1. Select the **Ask AI** icon at the top of the page.
1. Select a predefined prompt, such as **Should I upgrade my model?**, from the **Ask AI** banner. These prompts appear on model detail, agent, and monitoring pages.
    :::image type="content" source="../../media/observability/model-upgrade-predefined-prompts.png" alt-text="Screenshot of the Ask AI panel showing predefined prompts for model upgrade, including Should I upgrade my model and Is any model I'm using deprecated." lightbox="../../media/observability/model-upgrade-predefined-prompts.png":::

   The Ask AI chat panel opens on the right side of the page. You can type questions or select a predefined prompt to begin.

## Review model upgrade recommendations

Use Ask AI to check whether any of your deployed models are deprecated or have newer versions available.

1. In the Ask AI chat panel, type a question about your deployed models. For example, try "Should I upgrade my model?" or "Is any model I'm using deprecated?"

    :::image type="content" source="../../media/observability/model-upgrade-ask-ai.png" alt-text="Screenshot of Ask AI displaying a list of recommended model upgrades with version comparison details." lightbox="../../media/observability/model-upgrade-ask-ai.png":::

1. Review the list of recommended models that Ask AI displays. Key differences between your current model and the recommended alternatives are highlighted.
1. Select a model name to view its details in the model catalog, or select **Deploy** to go to the model deployment page. To learn how to deploy a model, see [Add and configure models to Foundry Models](../../../foundry-models/how-to/create-model-deployments.md).

    :::image type="content" source="../../media/observability/model-upgrade-selected-model.png" alt-text="Screenshot of a model detail page showing model capabilities, with Ask AI suggesting related model pages to review." lightbox="../../media/observability/model-upgrade-selected-model.png":::

1. After you deploy the recommended model, go to the **Deployments** page and confirm the deployment status shows **Succeeded** before proceeding to evaluation.

## Evaluate and compare model performance

After deploying the new model, evaluate it against your current model using the same agent instructions and configurations.

1. In Ask AI, ask to evaluate the newly deployed model. Either follow the link that Ask AI provides or let Ask AI set up the evaluation run for you. For details on manual setup, see [Evaluate your generative AI app](../../../how-to/evaluate-generative-ai-app.md?view=foundry&preserve-view=true).

    :::image type="content" source="../../media/observability/model-upgrade-evaluations.png" alt-text="Screenshot of the evaluation creation page with Ask AI guiding model evaluation setup through a step-by-step workflow." lightbox="../../media/observability/model-upgrade-evaluations.png":::

1. After the evaluation completes, open the evaluation detail page to review metric scores for both models side by side.
1. Use [compare](../../../how-to/evaluate-results.md?view=foundry&preserve-view=true#compare-the-evaluation-results) or [cluster analysis](cluster-analysis.md) to analyze differences in relevance, groundedness, and coherence.

If the new model isn't satisfactory, test other models and repeat these steps. Each new run appears alongside previous runs in the same evaluation, so you can compare results across multiple models.

## Update your agent to use the new model

After you confirm the new model meets your requirements, update your agent to use it:

1. In Ask AI, type a request like "Update my agent to use the new model."
1. Ask AI identifies the agent and current model, then displays the proposed change. Review the summary.
1. Select **Apply** to confirm the model switch. Ask AI creates a new agent version that uses the updated model.
1. Verify the update by checking the agent version history on the **Agent Playground** page. The page shows the new version with the updated model in the version history.

To update manually, go to the **Agent Playground** page, select your agent, and change the model in the agent configuration. To find other agents in your project that use the same model, type "Find other agents using this model" in Ask AI.

> [!NOTE]
> When you update the agent model, the change applies to new conversations. In-progress conversations continue to use the previous model until they complete.

## Roll back to a previous model

If the new model doesn't meet your requirements after the update, revert to the previous version:

1. Go to the **Agent Playground** page and select your agent.
1. Open the version history and select the previous version.
1. Select **Restore** to revert the agent to the earlier model configuration.
1. Verify the rollback by testing the agent in the playground.

> [!NOTE]
> Rolling back restores the agent configuration only. Evaluation runs and deployment records for the new model remain in your project history.

## Troubleshoot common issues

| Issue | Resolution |
|-------|------------|
| Ask AI doesn't suggest any model upgrades | Verify that your deployed model has a newer version available in the [model catalog](../../../foundry-models/how-to/create-model-deployments.md). Ask AI only recommends upgrades when newer versions exist. |
| Evaluation run fails to start | Confirm that your evaluation dataset is in CSV or JSONL format, and that you have the **Azure AI User** role (or higher) on the project. |
| New model performs worse than the current model | Use [compare](../../../how-to/evaluate-results.md?view=foundry&preserve-view=true#compare-the-evaluation-results) to review per-metric scores. Consider testing with a different model or adjusting agent instructions before switching. |
| Agent update doesn't take effect | Check the agent version history in **Agent Playground** to confirm the new version was created. To revert, see [Roll back to a previous model](#roll-back-to-a-previous-model). |

## Related content

After you upgrade your model and verify agent performance, consider monitoring ongoing model performance or exploring cost optimization options.

- [What is Ask AI?](../../../concepts/ask-ai.md)
- [Optimize cost and performance with Ask AI](../../control-plane/how-to-optimize-cost-performance.md)
- [Model versions in Foundry Models](../../../foundry-models/concepts/model-versions.md?view=foundry&preserve-view=true)
- [Evaluate your generative AI app](../../../how-to/evaluate-generative-ai-app.md?view=foundry&preserve-view=true)
- [Compare evaluation results](../../../how-to/evaluate-results.md?view=foundry&preserve-view=true)
