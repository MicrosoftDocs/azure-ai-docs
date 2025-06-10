---
title: How to use the AI agent catalog
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use the AI agent catalog to use code samples to quickly deploy agents.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 05/18/2025
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
---

# Get started with the Agent Catalog

Accelerate your agent development using code samples and best practices for creating agents. Each agent sample below links to a GitHub Repository, where you can browse the agent's configuration files, setup instructions and source code to start integrating them into your own project in code.
With agents you create using these code samples, be sure to assess safety and legal implications, and to comply with all applicable laws and safety standards. See the [transparency note](/legal/cognitive-services/agents/transparency-note) for more information.

[!INCLUDE [feature-preview](../../../ai-foundry/includes/feature-preview.md)]

## Prerequisites

- [Azure subscription](https://azure.microsoft.com/free)
- An [Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Find the Agent Catalog in the Azure AI Foundry portal

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).
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

A full list of agent samples in the catalog can be found on the Azure AI Foundry portal and the list below. There are several templates available that are authored by Microsoft and partners across different domains such as: travel, finance, insurance, business intelligence, healthcare, and more. 

**Azure AI Foundry Agent Service agent catalog**

| Code sample | Description | Author | Type | SDK | Difficulty level | Tools |
|-------------|-------------|--------|--------------|------------------|------|--------|
| [Browser Automation Agent](https://aka.ms/browser-automation) | Kickstart browser automation scenarios with this Azure Playwright powered template | Microsoft | Single-agent | Foundry Agent Service | Beginner | Playwright |
| [AI Red Teaming Agent](https://github.com/microsoft/agent-catalog/tree/main/semantic-kernel-blueprints/ai-red-teaming-agent) | Facilitates the development of a copilot to accelerate your AI red teaming process: through multi-agent system that automates the generation, transformation, and execution of harmful prompts against target generative AI models or applications for AI red teaming purposes. Useful for streamlining safety testing workflows, surfacing guardrail bypasses, and guiding risk mitigation planning. | Microsoft | Multi-agent | Semantic Kernel | Advanced | N/A |
| [Saifr Communication Compliance Agent](https://aka.ms/saifr-communication-agent) | The Saifr Communication Compliance Agent identifies potentially noncompliant text and generates a more compliant, fair, and balanced version, helping end users better adhere to relevant regulatory guidelines | Saifr from Fidelity Labs | Single-agent | Foundry Agent Service | Intermediate | OpenAPI Specified Tool |
| [Auquan Due Diligence Risk Analyst](https://aka.ms/due-diligence-risk-analyst-agent) | Helps create agents that assess risks across financial, operational, regulatory, and ESG domains | Auquan | Single-agent | Foundry Agent Service | Intermediate | OpenAPI Specified Tool |
| [Healthcare Agent Orchestrator](https://aka.ms/healthcare-multi-agent) | Facilitates the development and testing of  modular specialized agents that coordinate across diverse data types and tools like M365 and Teams to assist multi-disciplinary healthcare workflows—such as cancer care. | Microsoft | Multi-agent | Semantic Kernel | Advanced |  |
| [ResearchFlow Agent](https://aka.ms/research-flow) | Helps create agents that execute complex, multi-step research workflows and solve open-ended tasks | Microsoft | Multi-agent | Foundry Agent Service | Advanced |  |
| [Magentic-One Agent](https://aka.ms/magnetic-one) | A generalist, autonomous multi-agent system that performs deep research and problem-solving by orchestrating web search, code generation, and code execution agents. Helpful for tackling open-ended analytical or technical tasks. | Microsoft | Multi-agent | Foundry Agent Service | Advanced |  |
| [SightMachine Filler Optimization Agent](https://aka.ms/sight-machine-filler-optimization-agent) | The SightMachine Filler Optimization Agent supports building agents that analyze manufacturing data to reduce bottlenecks and improve throughput via predictive insights | SightMachine | Single-agent | Foundry Agent Service | Intermediate | Azure Functions |
| [Marquee Insights AI News Agent](https://aka.ms/ai-news-agent) | Enables creating an agent that retrieves and summarize news focused on Microsoft, healthcare, and legal sectors | Marquee Insights | Single-agent | Foundry Agent Service | Intermediate |  |
| [MiHCM HR Assist Agent](https://aka.ms/hr-agent) | Supports agent development for HR scenarios by enabling employees to navigate HR-related records like leave balances, HR requests and work activities using MiHCM's HR APIs | MiHCM | Single-agent | Foundry Agent Service | Intermediate | OpenAPI Specified Tool |
| [Portfolio Navigator](https://aka.ms/trusty-link) | Supports agent creation for exploring financial topics from Morningstar data and Grounding with Bing | Microsoft | Single-agent | Foundry Agent Service | Beginner | Morningstar, Grounding with Bing |
| [Travel Planner](https://aka.ms/travel-planner) | Enables agent creation for travel scenarios | Microsoft | Single-agent | Foundry Agent Service | Beginner | File Search, Code Interpreter, Tripadvisor, OpenAPI Specified Tool |
| [Home Loan Guide](https://aka.ms/home-loan-guide) | Enables agent creation to provide users with helpful information about mortgage applications at a fictitious company, Contoso Bank. | Microsoft | Single-agent | Foundry Agent Service | Beginner | Connected Agents, File Search, Code Interpreter, Grounding with Bing |
| [Sales Analyst Agent](https://aka.ms/sales-analyst) | Supports building agents that analyze sales data | Microsoft | Single-agent | Foundry Agent Service | Beginner | File Search, Code Interpreter |
| [Customer Service Agent](https://aka.ms/customer-service) | Helps create a multi-agent system that manages full-cycle support resolution —from authentication to escalation to resolution | Microsoft | Multi-agent | Foundry Agent Service | Advanced |  |
| [Warranty Claim Processing Agent](https://aka.ms/warranty-claim-processing) | Facilitates the development of agents for processing warranty claims | Microsoft | Single-agent | Semantic Kernel | Intermediate | OpenAPI Specified Tool |
| [Voice Live Agent](https://aka.ms/voice-live-agent) | Enables agent development for real-time, voice-based interactions using Azure AI Voice Live API. | Microsoft | Single-agent | Foundry Agent Service  | Intermediate |  |
| [Text Translation Agent](https://aka.ms/translation-agent) | Helps create agents that handle multilingual text processing, including dynamic language detection and bidirectional translation using Azure AI Translator service | Microsoft | Single-agent | Foundry Agent Service | Beginner | OpenAPI Specified Tool |
| [Video Translation Agent](https://aka.ms/video-translation-agent) | Supports building agents for multilingual video localization with translation, subtitles, and speech generation | Microsoft | Single-agent | Semantic Kernel | Beginner | N/A |
| [Intent Routing Agent](https://aka.ms/intent-routing) | Helps create agents that detect user intent and provide exact answering. Perfect for deterministically intent routing and exact question answering with human controls. | Microsoft | Single-agent | Foundry Agent Service | Beginner | OpenAPI Specified Tool |
| [Exact Question Answering Agent](https://aka.ms/exact-question-answering) | Supports building agents that answer predefined, high-value questions to ensure consistent and accurate responses. | Microsoft | Single-agent | Foundry Agent Service | Beginner | OpenAPI Specified Tool |
| [Contract Analysis Agent](https://aka.ms/contract-analysis-agent) | Enables creating agents that compare contract versions, extract key clauses, highlight differences, and generate review-ready reports. | Microsoft | Single-agent | Semantic Kernel | Intermediate | File Search, OpenAPI Specified Tool |
| [SOP Forge Agent](https://aka.ms/sop-forge-agent) | Helps create an agent that converts instructional videos into a fully formatted Standard Operating Procedure (SOP). | Microsoft | Single-agent | Semantic Kernel | Intermediate | File Search, OpenAPI Specified Tool |
