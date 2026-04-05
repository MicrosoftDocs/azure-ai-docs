---
title: "Quickstart: Create an agent from the catalog"
description: "Create and test an AI agent from the Foundry agent catalog. Pick a pre-built template, configure a model, and chat with your agent in the playground."
author: nicholasdbrady
ms.author: nbrady
ms.date: 04/03/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: quickstart
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to create an agent from a pre-built template so that I can quickly start building AI-powered automation without writing instructions from scratch.
---

# Quickstart: Create an agent from the catalog

In this quickstart, you create an agent from a pre-built template in the Foundry agent catalog and test it in the playground. The agent catalog provides ready-to-use agent templates that combine tested prompts, tool configurations, and interaction patterns so you can skip writing instructions from scratch.

**In this quickstart, you:**

> [!div class="checklist"]
> * Browse the agent catalog and select a template
> * Create an agent from the template
> * Test the agent in the playground

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project with a model deployed (for example, `gpt-4o`). If you don't have a project, first complete [Quickstart: Set up Microsoft Foundry resources](../../tutorials/quickstart-create-foundry-resources.md).

## Browse the agent catalog

1. Open the [Foundry portal](https://ai.azure.com).
1. Navigate to your project.
1. Select **Discover** (1), then select **Agents** (2).

   :::image type="content" source="../../media/agent-catalog/agents-catalog-browse.png" alt-text="Screenshot of the Foundry portal showing the Discover tab highlighted in the top navigation and the Agents link highlighted in the left sidebar, with the agent catalog displaying 30 available templates." lightbox="../../media/agent-catalog/agents-catalog-browse.png":::

   The catalog displays available agent templates. Each card shows the agent name, publisher, and the tools the agent uses.

1. Select the **Industry News & Trend Scanner** template.

   The template detail page shows what the agent does, the tools it uses, and the prompt engineering pattern it demonstrates.

   :::image type="content" source="../../media/agent-catalog/agent-catalog-template-detail.png" alt-text="Screenshot of the Industry News and Trend Scanner template detail page showing the agent description, tools, and the Create agent button highlighted in the top-right corner." lightbox="../../media/agent-catalog/agent-catalog-template-detail.png":::

## Create the agent

1. Select **Create agent**.
1. In the **Create an agent from manifest** dialog, enter a name for your agent (1). The name must start and end with alphanumeric characters and can contain hyphens in the middle.
1. Select **Create** (2).

   :::image type="content" source="../../media/agent-catalog/agent-catalog-create-dialog.png" alt-text="Screenshot of the Create an agent from manifest dialog with the agent name field highlighted and the Create button highlighted." lightbox="../../media/agent-catalog/agent-catalog-create-dialog.png":::

   The portal creates the agent and opens the agent builder playground.

## Configure the tool connection

After the agent is created, the playground opens with the template's instructions and tools pre-configured. Before you can test the agent, you need to connect the **Grounding with Bing Search** tool to a Bing Search resource.

1. Under **Tools**, find **Grounding with Bing Search**.
1. Select a connection from the **Connections** dropdown.

   :::image type="content" source="../../media/agent-catalog/agent-catalog-connection.png" alt-text="Screenshot of the agent builder playground showing the Grounding with Bing Search tool with the Select a connection dropdown highlighted." lightbox="../../media/agent-catalog/agent-catalog-connection.png":::

> [!NOTE]
> If you don't have a Bing Search connection, you need to create a Grounding with Bing Search resource first. For step-by-step instructions, see [Manage Grounding with Bing Search connections](../how-to/manage-grounding-with-bing.md).

## Test the agent in the playground

With the tool connection configured, you can now test the agent:

1. In the **Chat** panel on the right, type a prompt like `Scan the AI industry for the latest news and trends`.
1. Select **Send** (or press **Enter**).

   The agent runs multiple Bing-grounded searches, deduplicates results, and returns a formatted industry briefing.

   :::image type="content" source="../../media/agent-catalog/agent-catalog-response.png" alt-text="Screenshot of the agent playground chat showing the user prompt and the beginning of the agent response with an industry briefing header, period, and top stories with source citations." lightbox="../../media/agent-catalog/agent-catalog-response.png":::

1. Scroll down to see the full briefing. The response includes **Top Stories** with source citations, **Trend Watch** for emerging patterns across stories, and **Quick Hits** for notable one-line items.

   :::image type="content" source="../../media/agent-catalog/agent-catalog-response-full.png" alt-text="Screenshot of the bottom of the agent response showing the Trend Watch section, Quick Hits section, Bing Search grounding citations, and quality metrics showing AI Quality 100 percent and Safety 100 percent." lightbox="../../media/agent-catalog/agent-catalog-response-full.png":::

> [!TIP]
> Start by running the agent with its default instructions before customizing. This helps you understand the agent's workflow and identify which parts to adjust for your scenario.

## Clean up resources

If you no longer need the agent:

1. Select **Build** > **Agents** to view your agents.
1. Select the agent you created.
1. Select **More** (**...**) > **Delete**.

## Related content

- [Agent catalog overview](../concepts/agent-catalog.md)
- [Agent tools overview](../concepts/tool-catalog.md)
- [Quickstart: Create a prompt agent](prompt-agent.md)
- [Agent development lifecycle](../concepts/development-lifecycle.md)
