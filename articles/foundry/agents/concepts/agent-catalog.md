---
title: "Agent catalog for Foundry Agent Service"
description: "Explore pre-built agent templates in the Foundry agent catalog. Browse templates across industries with tools, prompt patterns, and one-click deployment."
author: nicholasdbrady
ms.author: nbrady
ms.date: 04/03/2026
ms.topic: overview
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Agent catalog for Foundry Agent Service

The agent catalog in Microsoft Foundry Agent Service is a collection of pre-built agent templates that you can deploy with one click. Each template is a working business automation agent and a prompt engineering learning resource. Browse the catalog to find a template that matches your scenario, select **Create Agent**, and start running it in minutes.

Templates serve two purposes:

- **Deploy immediately** — Each template creates a working agent that you can run against your own data without writing prompt instructions from scratch.
- **Learn prompt patterns** — Each template demonstrates a specific prompt engineering technique, such as XML-structured instructions or autonomous decision logic, that you can study and adapt for your own agents.

> [!NOTE]
> Agent templates are educational resources you build from. They don't perform actions directly on your behalf. You configure each agent with your own data sources, tools, and business context before running it.

## Prerequisites

- An Azure subscription.
- A [Foundry project](../../how-to/create-projects.md).
- A [model deployment](../../foundry-models/how-to/create-model-deployments.md) (for example, `gpt-5-mini`).

## Browse the catalog

To browse the agent catalog:

1. Open the [Foundry portal](https://ai.azure.com).
1. Navigate to your project.
1. Select **Discover** > **Agents**.

:::image type="content" source="../../media/agent-catalog/agents-catalog-browse.png" alt-text="Screenshot of the Foundry agent catalog showing 30 agent templates with search, sort, and tool icons for each template." lightbox="../../media/agent-catalog/agents-catalog-browse.png":::

You can search for templates by name or sort by **Featured** to find the right starting point for your scenario. Each template card shows the agent name, publisher, and the tools it uses.

## Template components

Every agent template in the catalog includes these components:

| Component | Description |
|---|---|
| **Tools** | The Foundry tools the agent uses, such as web search, code interpreter, or SharePoint. Most templates use one or two tools. |
| **Industry** | Whether the template is cross-industry (generic) or vertical-specific, such as marketing or manufacturing. |
| **Tone** | The communication style: formal, technical, coaching, conversational, or concise. |
| **Output format** | What the agent produces: reports, dashboards, code, emails, narratives, presentations, or tables. |
| **Interaction style** | How the agent engages: autonomous (no mid-flow input), single-shot (one request, one response), or multi-turn (ongoing conversation). |
| **Complexity** | The decision-making depth: simple (linear steps), multi-step (phased execution), or decision-tree (branching logic). |
| **Prompt structure** | The instruction format: XML tags, Markdown headers, natural language, or numbered rules. |
| **Memory** | Whether the agent retains context across conversations (on) or treats each conversation independently (off). |

## Tools used by catalog templates

Templates use the most common enterprise tools available in Agent Service. The following table lists each tool and its purpose.

| Tool | Type | Description |
|---|---|---|
| **[Web search](../how-to/tools/web-search.md)** | Built-in | Retrieves real-time information from the public web. Most versatile tool with the lowest setup friction. |
| **[Code Interpreter](../how-to/tools/code-interpreter.md)** | Built-in | Writes and runs Python code for data analysis, calculations, and chart generation. |
| **[SharePoint](../how-to/tools/sharepoint.md) (preview)** | Built-in | Searches and retrieves documents from your SharePoint sites. |
| **[GitHub](../how-to/tools/model-context-protocol.md) (via MCP)** | Custom | Accesses repositories, pull requests, issues, and code for developer workflows. Connected through an MCP server. |
| **[Grounding with Bing Search](../how-to/tools/bing-tools.md)** | Built-in | Retrieves cited, verifiable facts from the web with source attribution. |
| **[Azure AI Search](../how-to/tools/ai-search.md)** | Built-in | Queries knowledge indexes for grounded, domain-specific answers. |
| **[Microsoft Fabric](../how-to/tools/fabric.md) (preview)** | Built-in | Connects to your enterprise data warehouse for analytics. |
| **[File Search](../how-to/tools/file-search.md)** | Built-in | Analyzes uploaded documents using vector search. |
| **[Browser Automation](../how-to/tools/browser-automation.md) (preview)** | Built-in | Interacts with web UIs through natural language prompts. |
| **[OpenAPI tool](../how-to/tools/openapi.md)** | Custom | Calls external APIs using an OpenAPI specification. |

Most templates use two tools. A few single-tool templates show that well-crafted instructions can handle complex workflows without additional tools.

For more information about configuring tools, see [Agent tools overview](tool-catalog.md).

## Industries and use cases

The catalog covers both cross-industry and vertical-specific scenarios:

| Category | Coverage | Examples |
|---|---|---|
| **Generic** | Cross-industry templates for common business workflows | Competitive research, status reporting, incident analysis, meeting prep |
| **Marketing** | Campaign analysis, brand monitoring, content planning | A/B test analysis, social campaign performance, content calendars |
| **Manufacturing** | Supply chain and operations | Supplier qualification, procurement automation |
| **Retail** | Customer insights and store operations | Review synthesis, handbook assistants |
| **Travel and hospitality** | Planning and booking | Trip itinerary design |
| **Non-profit** | Donor management and engagement | Donor engagement strategy |
| **E-commerce** | Product optimization | SEO optimization for product listings |

> [!TIP]
> Cross-industry templates work in any vertical. A template like the "Competitive Landscape Researcher" applies equally to technology, retail, or manufacturing.

## Available templates

The following tables list all agent templates currently available in the catalog, grouped by industry.

### Generic

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Competitive Landscape Researcher | Web search, Code Interpreter | Autonomous | Multi-step |
| Weekly Team Status Reporter | GitHub, SharePoint | Autonomous | Simple |
| Release Notes Generator | GitHub, Code Interpreter | Single-shot | Multi-step |
| Meeting Prep Briefing | Web search, SharePoint, Grounding with Bing Search | Multi-turn | Multi-step |
| Data Quality Auditor | Microsoft Fabric, Code Interpreter | Autonomous | Multi-step |
| Internal Policy Q&A | SharePoint | Single-shot | Simple |
| Sales Metrics Dashboard Builder | Microsoft Fabric, Code Interpreter | Multi-turn | Multi-step |
| Blog Post Drafter | Web search, File Search | Multi-turn | Multi-step |
| Incident Postmortem Writer | GitHub, SharePoint | Single-shot | Multi-step |
| Internal App Test Runner | Browser Automation, GitHub | Multi-turn | Multi-step |
| Executive Weekly Digest | Microsoft Fabric, SharePoint, Grounding with Bing Search | Single-shot | Multi-step |
| API Integration Troubleshooter | OpenAPI tool, Code Interpreter | Multi-turn | Decision-tree |
| Document Standards Reviewer | File Search, SharePoint | Multi-turn | Decision-tree |
| PR Review & Merge Assistant | GitHub, File Search | Single-shot | Decision-tree |
| RFP Response Drafter | Azure AI Search, SharePoint | Single-shot | Decision-tree |
| Event Venue Research & Booking | Web search, Browser Automation | Multi-turn | Multi-step |
| Codebase Documentation Generator | GitHub, Code Interpreter | Autonomous | Multi-step |
| Workspace Utilization Reporter | Microsoft Fabric, SharePoint | Multi-turn | Multi-step |
| Industry News & Trend Scanner | Grounding with Bing Search | Autonomous | Simple |

### Marketing

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Content Calendar Planner | Web search, SharePoint | Multi-turn | Decision-tree |
| Brand Mention Monitor | Grounding with Bing Search, Code Interpreter | Autonomous | Decision-tree |
| Campaign A/B Test Analyzer | Azure AI Search, Code Interpreter | Multi-turn | Multi-step |
| Social Campaign Performance Analyzer | Code Interpreter | Autonomous | Multi-step |

### Manufacturing

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Supplier Qualification Checker | Web search, File Search | Multi-turn | Decision-tree |
| Internal Procurement Portal | Browser Automation, Microsoft Fabric, OpenAPI tool | Autonomous | Decision-tree |

### Retail

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Customer Review Synthesizer | Code Interpreter | Autonomous | Multi-step |
| Store Operations Handbook Assistant | SharePoint, Azure AI Search | Multi-turn | Decision-tree |

### Travel and hospitality

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Trip Itinerary Designer | Web search, File Search | Multi-turn | Decision-tree |

### Non-profit

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Donor Engagement Strategist | Azure AI Search, Grounding with Bing Search, OpenAPI tool | Multi-turn | Multi-step |

### E-commerce

| Template | Tools | Interaction | Complexity |
|---|---|---|---|
| Product Listing SEO Optimizer | Web search, Browser Automation | Multi-turn | Multi-step |

## Prompt engineering patterns

Each template uses one of four prompt structure styles. You can study these patterns to improve your own agent instructions:

| Pattern | Best for | Example |
|---|---|---|
| **XML tags** | Complex agents with clear separation of concerns. Sections like `<role>`, `<scope>`, and `<tool_strategy>` make instructions easy to parse. | Meeting Prep Briefing |
| **Markdown headers** | Technical workflows with hierarchical organization. Uses `# Role`, `## Step 1` structure for clear step ordering. | Codebase Documentation Generator |
| **Natural language** | Coaching personas and conversational agents. Reads like a paragraph-style briefing with implicit structure. | Trip Itinerary Designer |
| **Numbered rules** | Strict execution contracts and autonomous decision logic. Each rule is a discrete, enforceable instruction. | Brand Mention Monitor |

No single pattern is universally best. Choose a structure based on how your agent needs to process its instructions: strict compliance favors numbered rules, complex multi-phase workflows benefit from XML tags, and conversational agents work well with natural language.

## Create an agent from a template

To create an agent from a catalog template:

1. Open the agent catalog in the Foundry portal.
1. Select a template that matches your use case.
1. Select **Create Agent**.
1. Configure your agent:
   - Select a model deployment (for example, `gpt-5-mini`).
   - Connect the required tools (for example, add a SharePoint connection or configure web search).
   - Optionally customize the instructions to match your specific requirements.

   After creation, you can continue to modify the instructions, swap tools, or change the model deployment at any time.
1. Test your agent in the [agents playground](../../concepts/concept-playgrounds.md).
1. When you're satisfied with the results, [publish your agent](../how-to/publish-agent.md).

> [!TIP]
> Start by running a template with its default instructions before customizing. This helps you understand the agent's workflow and identify which parts to adjust for your scenario.

## Related content

- [Agent tools overview](tool-catalog.md)
- [Tool best practices](tool-best-practice.md)
- [What is Foundry Agent Service?](../overview.md)
- [Agent development lifecycle](development-lifecycle.md)
- [Create a private tool catalog](../how-to/private-tool-catalog.md)
