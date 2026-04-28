---
title: "Agent manifests for Foundry Agent Service"
description: "Explore pre-built agent manifests for the Foundry Agent Service. Browse manifests across industries with tools, prompt patterns, and one-click deployment."
author: nicholasdbrady
ms.author: nbrady
ms.date: 04/03/2026
ms.topic: overview
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Agent manifests for Foundry Agent Service

> [!NOTE]
> Agent Manifests are for educational and experimentation purposes. Resulting agents are not production ready. Review all provided resources and carefully test agent behavior in the context of your use case. Agents you create may be subject to legal and regulatory requirements, may require licenses, or may not be suitable for all industries, scenarios, or use cases. By using any template, you are acknowledging that resulting agents and other output are solely your responsibility, and that you will comply with all applicable laws, regulations, and relevant safety standards, terms of service, and codes of conduct. See the [Transparency note for Azure Agent Service](../../responsible-ai/agents/transparency-note.md) for more information.

Microsoft Foundry Agent Service provides a collection of pre-built agent manifests that help you easily jumpstart building and deploying agents with just a few clicks. Each manifest bundles a Foundry model configuration, prompt instructions, and tool definitions into a ready-to-use agent template. Browse manifests to find one that matches your scenario, select **Create Agent**, and start running it in minutes.

Manifests serve two purposes:

- **Deploy immediately** — Each manifest helps you create a simple, experimental working agent that you can run without writing prompt instructions from scratch.
- **Learn prompt patterns** — Each manifest demonstrates a specific prompt engineering technique, such as XML-structured instructions or autonomous decision logic, that you can study and adapt for your own agents.

## Prerequisites

- An Azure subscription.
- A [Foundry project](../../how-to/create-projects.md).
- A [model deployment](../../foundry-models/how-to/create-model-deployments.md) (for example, `gpt-5-mini`).

## Browse the manifests

To browse the agent manifests:

1. Open the [Foundry portal](https://ai.azure.com).
1. Navigate to your project.
1. Select **Discover** > **Agents**.
    
    :::image type="content" source="../../media/agent-catalog/agents-catalog-browse.png" alt-text="Screenshot of the Foundry agent manifests showing 30 agent manifests with search, sort, and tool icons for each manifest." lightbox="../../media/agent-catalog/agents-catalog-browse.png":::
    
You can search for manifests by name or sort by **Featured** to find the right starting point for your scenario. Each manifest card shows the agent name, publisher, and the tools it uses.

## Manifest components

Every agent manifest includes these components:

| Component | Description |
|---|---|
| **Tools** | The [tools](../concepts/tool-catalog.md) the agent uses, such as web search, code interpreter, or SharePoint. Most manifests use one or two tools. |
| **Industry** | Whether the manifest is cross-industry (generic) or vertical-specific, such as marketing or manufacturing. |
| **Tone** | The communication style: formal, technical, coaching, conversational, or concise. |
| **Output format** | What the agent produces: reports, dashboards, code, emails, narratives, presentations, or tables. |
| **Interaction style** | How the agent engages: autonomous (no mid-flow input), single-shot (one request, one response), or multi-turn (ongoing conversation). |
| **Complexity** | The decision-making depth: simple (linear steps), multi-step (phased execution), or decision-tree (branching logic). |
| **Prompt structure** | The instruction format: XML tags, Markdown headers, natural language, or numbered rules. |
| **Memory** | Whether the agent retains context across conversations (on) or treats each conversation independently (off). |

## Tools used by manifests

Manifests use the most common enterprise tools available in Agent Service. The following table lists each tool and its purpose.

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

Most manifests use two tools. A few single-tool manifests show that well-crafted instructions can handle complex workflows without additional tools.

For more information about configuring tools, see [Agent tools overview](tool-catalog.md).

## Industries and use cases

The manifests cover both cross-industry and vertical-specific scenarios:

| Category | Coverage | Examples |
|---|---|---|
| **Generic** | Cross-industry manifests for common business workflows | Competitive research, status reporting, incident analysis, meeting prep |
| **Marketing** | Campaign analysis, brand monitoring, content planning | A/B test analysis, social campaign performance, content calendars |
| **Manufacturing** | Supply chain and operations | Supplier qualification, procurement automation |
| **Retail** | Customer insights and store operations | Review synthesis, handbook assistants |
| **Travel and hospitality** | Planning and booking | Trip itinerary design |
| **Non-profit** | Donor management and engagement | Donor engagement strategy |
| **E-commerce** | Product optimization | SEO optimization for product listings |

> [!TIP]
> Cross-industry manifests work in any vertical. A manifest like the "Competitive Landscape Researcher" applies equally to technology, retail, or manufacturing.

## Available manifests

The following tables list all agent manifests currently available, grouped by industry.

### Generic

| Manifest | Tools | Interaction | Complexity |
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

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Content Calendar Planner | Web search, SharePoint | Multi-turn | Decision-tree |
| Brand Mention Monitor | Grounding with Bing Search, Code Interpreter | Autonomous | Decision-tree |
| Campaign A/B Test Analyzer | Azure AI Search, Code Interpreter | Multi-turn | Multi-step |
| Social Campaign Performance Analyzer | Code Interpreter | Autonomous | Multi-step |

### Manufacturing

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Supplier Qualification Checker | Web search, File Search | Multi-turn | Decision-tree |
| Internal Procurement Portal | Browser Automation, Microsoft Fabric, OpenAPI tool | Autonomous | Decision-tree |

### Retail

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Customer Review Synthesizer | Code Interpreter | Autonomous | Multi-step |
| Store Operations Handbook Assistant | SharePoint, Azure AI Search | Multi-turn | Decision-tree |

### Travel and hospitality

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Trip Itinerary Designer | Web search, File Search | Multi-turn | Decision-tree |

### Non-profit

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Donor Engagement Strategist | Azure AI Search, Grounding with Bing Search, OpenAPI tool | Multi-turn | Multi-step |

### E-commerce

| Manifest | Tools | Interaction | Complexity |
|---|---|---|---|
| Product Listing SEO Optimizer | Web search, Browser Automation | Multi-turn | Multi-step |

## Prompt engineering patterns

Each manifest uses one of four prompt structure styles. You can study these patterns to improve your own agent instructions:

| Pattern | Best for | Example |
|---|---|---|
| **XML tags** | Complex agents with clear separation of concerns. Sections like `<role>`, `<scope>`, and `<tool_strategy>` make instructions easy to parse. | Meeting Prep Briefing |
| **Markdown headers** | Technical workflows with hierarchical organization. Uses `# Role`, `## Step 1` structure for clear step ordering. | Codebase Documentation Generator |
| **Natural language** | Coaching personas and conversational agents. Reads like a paragraph-style briefing with implicit structure. | Trip Itinerary Designer |
| **Numbered rules** | Strict execution contracts and autonomous decision logic. Each rule is a discrete, enforceable instruction. | Brand Mention Monitor |

No single pattern is universally best. Choose a structure based on how your agent needs to process its instructions: strict compliance favors numbered rules, complex multi-phase workflows benefit from XML tags, and conversational agents work well with natural language.

## Create an agent from a manifest

To create an agent from a manifest:

1. Open the agent manifests in the Foundry portal.
1. Select a manifest that matches your use case.
1. Select **Create Agent**.
1. Configure your agent:
   - Select a model deployment (for example, `gpt-5-mini`).
   - Connect the required tools (for example, add a SharePoint connection or configure web search).
   - Optionally customize the instructions to match your specific requirements.

    After creation, you can continue to modify the instructions, swap tools, or change the model deployment at any time. 
    > [!NOTE]
    > Agent manifests are for [educational and experimentation purposes only](#agent-manifests-for-foundry-agent-service). Resulting agents are not production ready. 
1. Test your agent in the [agents playground](../../concepts/concept-playgrounds.md).
1. When you're satisfied with the results, [publish your agent](../how-to/agent-applications.md).

> [!TIP]
> Start by running a manifest with its default instructions before customizing. This helps you understand the agent's workflow and identify which parts to adjust for your scenario.

## Related content

- [Quickstart: Create an agent from a manifest](../quickstarts/quickstart-agent-catalog.md)
- [Agent tools overview](tool-catalog.md)
- [Tool best practices](tool-best-practice.md)
- [What is Foundry Agent Service?](../overview.md)
- [Agent development lifecycle](development-lifecycle.md)
- [Create a private tool catalog](../how-to/private-tool-catalog.md)
- [Transparency note for Azure Agent Service](../../responsible-ai/agents/transparency-note.md)