---
title: How to use the AI agent catalog
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use the AI agent catalog to use code samples to quickly deploy agents.
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/29/2025
ms.author: aahi
author: aahill
---

# Get started with the Agent Catalog

Accelerate your agent development using code samples and best practices for creating agents. Each agent sample below links to a GitHub Repository, where you can browse the agent's configuration files, setup instructions and source code to start integrating them into your own project in code.
With agents you create using these code samples, be sure to assess safety and legal implications, and to comply with all applicable laws and safety standards.[Learn More](https://learn.microsoft.com/en-us/legal/cognitive-services/agents/transparency-note)

[!INCLUDE [feature-preview](../../../ai-foundry/includes/feature-preview.md)]

## Prerequisites

- [Azure subscription](https://azure.microsoft.com/free)
- An [Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Find the Agent Catalog in the Azure AI Foundry portal

1. Go to [Azure AI Foundry portal](https://ai.azure.com).
1. Open your project.
1. On the left pane, select **Agents**.
1. Near the top of the screen, select **Catalog**. Find the code sample you want to use.

    :::image type="content" source="../media/agent-catalog.png" alt-text="A screenshot of the model catalog." lightbox="../media/agent-catalog.png":::

1. Select **Open in Github** to view the entire sample application.

## Explore the code samples

Once you're looking at the GitHub repository for your sample, refer to the README for more instructions and information on how to deploy your own version of the application.

Instructions vary by sample, but most include information on:
* Pre-requisites
* Setup instructions
* Configuration files
* Sample dataset
* Example prompts and agent interactions
* Tools used

The README also includes information about the application, such as the use case, architecture, and other tips.

## View all available code samples

A full list of agent samples in the catalog can be found on the Azure AI Foundry. There are several templates available that are authored by Microsoft and partners across different domains such as: travel, finance, insurance, business intelligence, healthcare, and more. 

**Azure AI Agent Service Agent Catalog**

| Code sample | Description | Author | Type | SDK | Difficulty level | Tools |
|-------------|-------------|--------|--------------|------------------|------|--------|
| [Browser Automation Agent](#) | Kickstart browser automation scenarios with this Azure Playwright powered template | Microsoft | Single-agent | Agent AI Agent Service | Beginner | Playwright |
| [AI Red Teaming Agent](#) | Facilitates the development of a copilot to accelerate your AI red teaming process: through multi-agent system that automates the generation, transformation, and execution of harmful prompts against target generative AI models or applications for AI red teaming purposes. Useful for streamlining safety testing workflows, surfacing guardrail bypasses, and guiding risk mitigation planning. | Microsoft | Multi-agent | Semantic Kernel | Advanced | NA |
| [Saifr Communication Compliance Agent](#) | The Saifr Communication Compliance Agent identifies potentially noncompliant text and generates a more compliant, fair, and balanced version, helping end users better adhere to relevant regulatory guidelines | Saifr from Fidelity Labs | Single-agent | Agent AI Agent Service | Intermediate | OpenAPI Specified Tool |
| [Auquan Due Diligence Risk Analyst](#) | Helps create agents that assess risks across financial, operational, regulatory, and ESG domains | Auquan | Single-agent | Agent AI Agent Service | Intermediate | OpenAPI Specified Tool |
| [Healthcare Multi-agent Orchestrator](#) | Facilitates the development and testing of  modular specialized agents that coordinate across diverse data types and tools like M365 and Teams to assist multi-disciplinary healthcare workflows—such as cancer care. | Microsoft | Multi-agent | Semantic Kernel | Advanced | TBD |
| [ResearchFlow Agent](#) | Helps create agents that execute complex, multi-step research workflows and solve open-ended tasks | Microsoft | Multi-agent | Agent AI Agent Service | Advanced | TBD |
| [Magentic-One Agent](#) | A generalist, autonomous multi-agent system that performs deep research and problem-solving by orchestrating web search, code generation, and code execution agents. Helpful for tackling open-ended analytical or technical tasks. | Microsoft | Multi-agent | Agent AI Agent Service | Advanced | TBD |
| [SightMachine Filler Optimization Agent](#) | The SightMachine Filler Optimization Agent supports building agents that analyze manufacturing data to reduce bottlenecks and improve throughput via predictive insights | SightMachine | Single-agent | Agent AI Agent Service | Intermediate | Azure Functions |
| [Marquee Insights AI News Agent](#) | Enables creating an agent that retrieves and summarize news focused on Microsoft, healthcare, and legal sectors | Marquee Insights | Single-agent | Agent AI Agent Service | Intermediate | TBD |
| [MiHCM HR Assist Agent](#) | Supports agent development for HR scenarios by enabling employees to navigate HR-related records like leave balances, HR requests and work activities using MiHCM's HR APIs | MiHCM | Single-agent | Agent AI Agent Service | Intermediate | OpenAPI Specified Tool |
| [Claim Concierge](#) | Helps create agents for multi-lingual claim navigation | Microsoft | Multi-agent | Agent AI Agent Service | Beginner | Connected Agents, File Search, Grounding with Bing, Code Interpreter |
| [Portfolio Navigator](#) | Supports agent creation for exploring financial topics from Morningstar data and Grounding with Bing | Microsoft | Single-agent | Agent AI Agent Service | Beginner | Morningstar, Grounding with Bing |
| [Travel Planner](#) | Enables agent creation for travel scenarios | Microsoft | Single-agent | Agent AI Agent Service | Beginner | File Search, Code Interpreter, Tripadvisor, OpenAPI Specified Tool |
| [Home Loan Guide](#) | Enables agent creation to provide users with helpful information about mortgage applications at a fictitious company, Contoso Bank. | Microsoft | Single-agent | Agent AI Agent Service | Beginner | Connected Agents, File Search, Code Interpreter, Grounding with Bing |
| [Sales Analyst Agent](#) | Supports building agents that analyze sales data | Microsoft | Single-agent | Agent AI Agent Service | Beginner | File Search, Code Interpreter |
| [Customer Service Agent](#) | Helps create a multi-agent system that manages full-cycle support resolution —from authentication to escalation to resolution | Microsoft | Multi-agent | Agent AI Agent Service | Advanced | TBD |
| [Warranty Claim Processing Agent](#) | Facilitates the development of agents for processing warranty claims | Microsoft | Single-agent | Semantic Kernel | Intermediate | OpenAPI Specified Tool |
| [Voice Live Agent](#) | Enables agent development for real-time, voice-based interactions using Azure AI Voice Live API. | Microsoft | Single-agent | Agent AI Agent Service  | Intermediate | TBD |
| [Meeting Prep Agent](#) | Helps build an agent that helps with meetings by researching attendees and generating contextual summaries | Microsoft | Single-agent | Agent AI Agent Service | Intermediate | Grounding with Bing, Azure Logic Apps |
| [CommsPilot](#) | Enables agent creation for personalized outbound sales emails and outreach logging | Microsoft | Single-agent | Agent AI Agent Service | Intermediate | File Search, Grounding with Bing, Azure Logic Apps |
| [Text Translation Agent](#) | Helps create agents that handle multilingual text processing, including dynamic language detection and bidirectional translation using Azure AI Translator service | Microsoft | Single-agent | Agent AI Agent Service | Beginner | OpenAPI Specified Tool |
| [Video Translation Agent](#) | Supports building agents for multilingual video localization with translation, subtitles, and speech generation | Microsoft | Single-agent | Semantic Kernel |  | Beginner | NA |
| [Intent Routing Agent](#) | Helps create agents that detect user intent and provide exact answering. Perfect for deterministically intent routing and exact question answering with human controls. | Microsoft | Single-agent | Agent AI Agent Service | Beginner | OpenAPI Specified Tool |
| [Exact Question Answering Agent](#) | Supports building agents that answer predefined, high-value questions to ensure consistent and accurate responses. | Microsoft | Single-agent | Agent AI Agent Service | Beginner | OpenAPI Specified Tool |
| [Contract Analysis Agent](#) | Enables creating agents that compare contract versions, extract key clauses, highlight differences, and generate review-ready reports. | Microsoft | Single-agent | Semantic Kernel | Intermediate | File Search, OpenAPI Specified Tool |
| [SOP Forge Agent](#) | Helps create an agent that converts instructional videos into a fully formatted Standard Operating Procedure (SOP). | Microsoft | Single-agent | Semantic Kernel | Intermediate | File Search, OpenAPI Specified Tool |
