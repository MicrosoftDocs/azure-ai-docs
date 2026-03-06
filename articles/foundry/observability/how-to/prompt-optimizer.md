---
title: Optimize agent prompts with Prompt Optimizer (preview)
description: Learn how to use Prompt Optimizer in Microsoft Foundry to automatically improve your agent's system instructions using AI-driven prompt engineering best practices.
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
ms.date: 03/13/2026
ms.topic: how-to
ms.service: azure-ai-foundry
---

# Optimize agent prompts by using Prompt Optimizer (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use Prompt Optimizer in Microsoft Foundry to automatically improve your agent's system instructions. Prompt Optimizer applies [prompt-engineering best practices](../../openai/concepts/prompt-engineering.md) to restructure, clarify, and enhance your instructions. It provides transparent, paragraph-level reasoning for every change. You can iteratively refine results by adding suggestions and reoptimizing until satisfied, then apply the final output with a single click.

This article covers how to use Prompt Optimizer in the Foundry portal playground.

## Prerequisites

- A [Foundry project](../how-to/create-projects.md) with at least one [prompt agent or workflow agent](../../agents/overview.md).
- A model deployment in a [supported region](#supported-regions).
- Access to the [agents playground](../../concepts/concept-playgrounds.md#agents-playground) or [model playground](../../concepts/concept-playgrounds.md#model-playground) in the Foundry portal.

## How Prompt Optimizer works

Prompt Optimizer uses a multistep process that combines your input with LLM-driven optimization:

1. **Input collection**: You provide an initial description of what your agent should do (for new agents) or open the optimizer with existing instructions already in place. Optionally, you can provide additional suggestions to guide the optimization (for example, "Have a professional tone" or "Make it kid-friendly").

2. **LLM-based optimization**: An LLM receives your instructions and any suggestions. It applies prompt-engineering best practices to restructure, clarify, and enhance the instructions.

3. **Reasoning generation**: For each modified paragraph, the LLM generates an explanation of *why* the change was made. This reasoning is displayed alongside the optimized text for full transparency.

4. **Iterative refinement**: After the initial optimization, you can provide additional suggestions and reoptimize. Each subsequent optimization uses the latest optimized text as the new baseline, combined with your new suggestion. Repeat this loop until you're satisfied with the result.

## Open Prompt Optimizer

To open Prompt Optimizer in the Foundry portal:

1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Make sure the **New Foundry** toggle is on. These steps refer to Foundry (new).
2. Navigate to the **Build** page and select your agent.
3. In the agent configuration panel, find the **Instructions** section.
4. Select the pencil-with-sparkle icon (✏️✨) next to the *Instructions* header. This action opens the Prompt Optimizer dialog.

> [!TIP]
> You can use Prompt Optimizer inside both the agents playground and the model playground wherever a system instructions field is present.

## Optimize a new agent's instructions

If your agent doesn't have instructions yet:

1. Open Prompt Optimizer. The dialog displays an empty state prompting you to describe what you want your agent to do.
2. In the text area, enter a description of your agent's purpose and behavior. For example: *"A travel planning assistant that helps users plan multi-day trips with budget recommendations."*
3. Select **Optimize**. The optimizer generates a full set of structured system instructions based on your description.
4. Review the optimized instructions. Changed paragraphs are highlighted in purple with a left purple border.
5. Select **Use prompt** to apply the optimized instructions to your agent.

## Optimize existing instructions

If your agent already has instructions, follow these steps:

1. Open Prompt Optimizer. The dialog shows your original instructions in a bordered card.
2. Optionally, enter a suggestion in the suggestion bar to guide the optimization. For example: *"Add guardrails for off-topic questions"* or *"Make the tone more conversational."*
3. Select **Optimize**. The optimizer analyzes your current instructions and generates an improved version.
4. Review the optimized instructions.
5. Select **Use prompt** to replace your current instructions with the optimized version.

> [!NOTE]
> You can leave the suggestion field empty. In some cases, optimization without additional direction produces strong results, since the optimizer focuses purely on structural and clarity improvements.

## Review optimization reasoning

Prompt Optimizer provides transparent, paragraph-level reasoning for every change:

- **Individual reasoning**: Select the chat bubble icon (💬) next to any changed paragraph to view why that specific change was made. The reasoning appears in a purple-highlighted box below the paragraph.
- **Show all reasoning**: Select the **Show all reasoning** toggle to display reasoning for every changed paragraph at once.

Reasoning explanations describe what prompt-engineering principle was applied and why it improves the instructions. This information helps you understand and validate each suggestion before accepting it.

## Iterate on optimizations

You can refine the optimized result as many times as needed:

1. After reviewing the optimized instructions, enter a new suggestion in the suggestion bar. For example: *"Shorten the response format section"* or *"Add a fallback behavior when the user asks something out of scope."*
2. Select **Optimize** again. The optimizer uses your latest optimized text as the new baseline and applies your new suggestion.
3. Repeat until you're satisfied.
4. Select **Use prompt** to apply the final result.

> [!IMPORTANT]
> Optimization results aren't stored permanently. To apply results, select **Use prompt** before closing the dialog, or you lose the results.

## Supported regions

You can use Prompt Optimizer in projects hosted in the following regions. 

- Central US
- East US 2
- France Central
- Germany West Central
- Italy North
- Japan West
- North Central US
- Poland Central
- Spain Central
- Sweden Central
- Switzerland West
- UAE North
- West US
- West US 2
- West US 3

In unsupported regions, the **Optimize** button doesn't appear.

## Limitations

- **Text-based instructions only**: The optimizer works with text-based agent instructions only. It doesn't support optimization of non-text configuration elements such as tool definitions or knowledge sources.
- **Ephemeral results**: Optimization results aren't persisted across sessions. Select **Use prompt** to apply results before closing the dialog.
- **No version history**: The optimizer doesn't automatically save previous versions of your instructions. Consider copying your original instructions before optimizing if you want to preserve them.

## Best practices

- **Start simple, then refine**: Begin with a short description of your agent's purpose and let the optimizer create the initial structure. Then iterate with targeted suggestions.
- **Use specific suggestions**: Vague suggestions like "make it better" produce less useful results than specific ones like "add error handling for invalid dates" or "restrict responses to English only."
- **Review reasoning before accepting**: The per-paragraph reasoning helps you catch changes that might not align with your use case, even if they follow prompt-engineering best practices.
- **Test after optimizing**: After applying optimized instructions, test your agent in the playground to verify the changes produce the expected behavior before deploying.
- **Preserve your original prompt**: If you want to revert after applying an optimized prompt, simply reload the page. The optimized result isn't saved until you explicitly save your agent, so reloading restores your previous instructions.
- **Run a full evaluation**: After optimizing, run an evaluation with your own dataset to measure whether the changes actually improve your agent's performance. Prompt Optimizer applies general best practices, but your evaluation data validates whether those changes work for your specific use case.

## Troubleshooting

| Issue | Possible cause | Resolution |
|-------|---------------|------------|
| Optimize icon doesn't appear | Project is in an unsupported region | Move your project to a [supported region](#supported-regions) or create a new project in one of the listed regions. |
| Optimization produces unexpected results | Suggestion was too vague or conflicting | Provide more specific guidance in the suggestion bar. Try optimizing without a suggestion first, then add targeted refinements. |
| Optimization takes too long | Large or complex instructions | Break your instructions into focused sections and optimize them individually, then combine. |
| Changes don't appear in the agent | "Use prompt" wasn't selected | Open the optimizer again and rerun the optimization. Make sure to select **Use prompt** before closing the dialog. |

## Related content

- [Evaluate your AI agents](evaluate-agent.md)
