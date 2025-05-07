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

# Get started with the agent catalog

Streamline your agentic system development with prebuilt, task-specific agent code samples. Benefit from a quick deployment for a variety of tasks. For example, translation, sales prep, computer use, and more.

[!INCLUDE [feature-preview](../../../ai-foundry/includes/feature-preview.md)]

## Prerequisites

- [Azure subscription](https://azure.microsoft.com/free)
- An [Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Find the agent catalog in the Azure AI Foundry portal

1. Go to [Azure AI Foundry portal](https://ai.azure.com).
1. Open your project.
1. On the left pane, select **Agents**.
1. Near the top of the screen, select **Catalog**. Find the code sample you want to use.

    :::image type="content" source="../media/agent-catalog.png" alt-text="A screenshot of the model catalog." lightbox="../media/agent-catalog.png":::

1. Select **Open in Github** to view the entire sample application.

## Explore the code samples

Once you're looking at the GitHub repository for your sample, refer to the README for more instructions and information on how to deploy your own version of the application.

Instructions vary by sample, but most include information on:
* Setup instructions
* Using the code sample
* Tools used

The README also includes information about the application, such as the use case, architecture, and other tips.

## View all available code samples

A full list of agent samples in the catalog can be found on the Azure AI Foundry. There are several templates available that are authored by Microsoft and partners across different domains such as: travel, finance, insurance, business intelligence, healthcare, and more. 


**Azure AI Agent Service Agent Catalog**

| Code sample | Description | Author | Capabilities | Difficulty Level | Structure | Domain | Risk considerations |
|-----------------|-------------|--------|--------------|------------------|-----------|--------|---------------------|
| [Browser Automation Agent](#) | Helps users complete simple and complex web browser tasks such as online class booking using simple natural languge prompts and Azure Playwright Service | Microsoft | Web Browser Automation, Playwright Actions | Beginner-friendly | Single-Agent | Education, General | TBD |
| [Deep Research Agent](#) | Conducts multi-step research tasks using OpenAI models, real-time web data, files, and third-party sources to generate comprehensive, cited reports for complex queries in science, finance, policy, and more. | Microsoft | Web Search, File Analysis, Image Reasoning, Task Scheduling | Advanced | Single-Agent | Research | TBD |
| [Claim Concierge](#) | Helps patients navigate claims in their preferred language by auto-detecting user language, translating interactions and guiding them through submissions, appeals, and coverage questions. | Microsoft | File Search, Code Interpreter, Translator, Connected Agents | Beginner-friendly | Multi-Agent | Insurance | TBD |
| [Trusty Link](#) | Helps users explore financial topics and investment products using Morningstar data and Bing Search. Designed for education, not advice. | Microsoft | Morningstar API, Bing Grounding, File Search | Beginner-friendly | Single-Agent | Finance | TBD |
| [Travel Planner](https://github.com/microsoft/agent-blueprints/tree/main/azure-ai-agent-service-blueprints/travel-agent) | Create travel itinerary using latest travel related info powered by Bing grounding tool. | Microsoft | Tripadvisor API, Code Interpreter, OpenAPi tool (Flights) | Beginner-friendly | Single-Agent | Travel | TBD |
| [Home Loan Guide](https://github.com/microsoft/agent-blueprints/tree/main/azure-ai-agent-service-blueprints/home-loan-guide) | Guides users through the mortgage application process, explains loan options, and helps with document readiness | Microsoft | Document QA, Enterprise Data Grounding, Code Interpreter | Beginner-friendly | Single-Agent | Finance | TBD |
| [Sales Analyst Agent](#) | Analyzes sales data using File Search and built-in tools to generate insights like regional revenue metrics for a company. | Microsoft | File Search, Data Analysis, Insight Generation | Beginner-friendly | Single-Agent | Sales, Business Intelligence | TBD |
| [AI News Agent](#) | Retrieves and summarizes news using SerpAPI and Azure AI Agent Service, with a focus on Microsoft, Healthcare, and Legal sector developments. | Marquee Insights | Real-Time Search, Summarization, Sector Prioritization | Intermediate | Single-Agent | General, Healthcare, Legal | TBD |
| [Saifr Communication Agent](#) | Converts potentially noncompliant text to a more compliant, fair, and balanced version to help users better align with regulatory guidelines. Not intended to replace legal, compliance, or business functions; end users remain responsible for regulatory obligations | Fidelity Saifr | AI Text Review, OpenAPI tool | Intermediate | Single-Agent | Finance, Compliance | TBD |
| [Due Diligence Risk Analyst](#) | Provides comprehensive risk analysis and timeline tracking across operational, financial, regulatory, and sustainability dimensions. Processes structured risk data to generate detailed timelines, actionable insights, and visual risk indicators. | Auquan | Code Interpreter, Grounding with Bing Search, Auquan OpenAPI tool | Intermediate | Single Agent | Finance, Legal, ESG | TBD |
| [SightMachine Filler Optimization Agent](#) | Helps manufacturing engineers improve bottling line efficiency by analyzing historical data, performing root cause analysis, and offering predictive insights to optimize throughput and reduce bottlenecks. Accessible via natural language queries for ease of use without data science expertise. | SightMachine | Root Cause Analysis, Azure Functions | Intermediate | Single-Agent | Manufacturing, Industrial Operations | TBD |
| [Voice Live Agent](https://github.com/yulin-li/voice-agent-sample/tree/master/samples/react) | Enables real-time speech interaction using Azure AI Voice Live API for seamless voice-based conversations | Microsoft | Real-Time Speech | Intermediate | Single-Agent | General | TBD |
| [Meeting Prep Agent](#) | Prepares you for external meetings by scanning your calendar, researching attendees, and sending a concise Teams summary with bios and context. | Microsoft | Bing Grounding, Outlook Calendar, Teams Messaging via Azure Logic Apps | Intermediate | Single-Agent | General | TBD |
| [CommsPilot](#) | Drafts accurate support replies and personalized outbound sales emails by combining internal documents with real-time public profile grounding. Supports inbox automation and outreach logging via Logic Apps. | Microsoft | File Search, Bing Grounding, Outlook Connector (Logic Apps) | Intermediate | Single-Agent | Customer Support, Sales | TBD |
| [Supply Sense](#) | Tracks shipments, forecasts inventory needs, and analyzes logistics performance to help supply chain teams act on real-time insights. | Microsoft | Azure Maps, Azure Table Storage, Code Interpreter | Intermediate | Single-Agent | Supply Chain | TBD |
| [Store Ops Guide](#) | Helps store managers optimize layout, staffing, and promotions by analyzing store photos, foot traffic data, and customer feedback | Microsoft | GPT-4o (Vision), File Search, Code Interpreter, Bing Grounding | Intermediate | Single-Agent | Retail | TBD |
| [Translation Agent](#) | Handles multilingual translation with dynamic language detection, bidirectional translation, and interactive clarification of missing parameters using Translator Service | Microsoft | Azure AI Services Language Detection, Translation | Beginner-friendly | Single-Agent | General | TBD |
| [Intent Routing Agent](#) | Detects user intent and routes queries deterministically to the appropriate tool (CLU or CQA) for accurate handling of high-value requests with human controls | Microsoft | Azure AI Services Intent Recognition, FAQ Answering | Beginner-friendly | Single-Agent | Customer Support | TBD |
| [Exact Question Answering Agent](#) | Answers high-value predefined questions deterministically using a CQA tool to ensure consistent and accurate responses with no rewriting | Microsoft | Azure AI Services FAQ Answering, Deterministic Responses | Beginner-friendly | Single-Agent | Customer Support | TBD |
| [Personal Shopper Agent](#) | Uses multi-agent orchestration to triage customer intent and route to refund or sales agents, supporting live streaming responses and human-in-the-loop for retail support scenarios. | Microsoft | Intent Routing, Human-in-the-Loop | Intermediate | Multi-Agent | Retail, Customer Support | TBD |
| [Magentic One Agent](#) | A generalist, autonomous multi-agent system that performs deep research and problem-solving by orchestrating web search, code generation, and code execution agents. Ideal for tackling open-ended analytical or technical tasks. | Microsoft | Multi-Agent Workflow, Web Search, Code Generation, Code Execution | Advanced | Multi-Agent | Research | TBD |
| [Customer Service Agent](#) | Orchestrates customer authentication, triage, billing, and sales support using a dynamic multi-agent workflow. Includes human-in-the-loop escalation, real-time streaming, and full-cycle support resolution. | Microsoft | Authentication, Human-in-the-Loop | Advanced | Multi-Agent | Customer Support, Telecom | TBD |
| [ResearchFlow Agent](#) | Executes complex, multi-agent research workflows by gathering facts, planning actions, and coordinating dynamic sub-agents to solve open-ended tasks. Supports adaptive planning, user prompting, and final summarization. | Microsoft | Planning, Fact Management, Dynamic Agent Routing, User Prompting | Advanced | Multi-Agent | Research | TBD |



**Semantic Kernel Agent Catalog**

| Code sample | Description | Author | Capabilities | Difficulty Level | Structure | Domain | Risk considerations |
|-----------------|-------------|--------|--------------|------------------|-----------|--------|---------------------|
| [AI Red Teaming Agent](https://github.com/microsoft/agent-blueprints/tree/main/semantic-kernel-blueprints/ai_red_team) | Automates the generation, transformation, and execution of harmful prompts against target generative AI models or applications. Useful for streamlining safety testing workflows, surfacing filter bypasses, and recording every step for later analysis. | Microsoft | Multi-agent, Custom tool, RAI Testing | Advanced | Multi-Agent | Security | TBD |
| [Healthcare Multi-Agent Orchestrator](https://github.com/Azure-Samples/healthcare-multi-agent) | Demonstrates the integration of AI models and general reasoners within a group chat environment, facilitating seamless deployment for evaluations in the healthcare industry. | Microsoft | Multi-agent, Azure Bots, MS Teams | Advanced | Multi-Agent | Healthcare, General | TBD |
| [Warranty Claim Processing Agent](#) | Processes warranty claims by extracting structured data, redacting PII, and determining eligibility, resolution type, and urgency using strict rules and a JSON schema. | Microsoft | Document Intelligence, PII Redaction, JSON Output Generation | Intermediate | Single-Agent | Retail | TBD |
| [Contract Analysis](#) | Compares two versions of a contract to extract key fields and clauses, highlights differences, and generates a report for review and follow-up | Microsoft | File Search, Content Understanding | Intermediate | Single-Agent | Legal, Compliance, Operations | TBD |
| [SOP Forge](#) | Converts instructional video into a fully formatted Standard Operating Procedure (SOP). Transcribes, identifies steps, adjusts tone, swaps visuals, and delivers a Markdown-ready file. Supports fast editing and visual generation for updated documentation. | Microsoft | Content Understanding, File Search, Image Gen | Intermediate | Single-Agent | Operations | TBD |
| [Video Translation Agent](https://github.com/microsoft/agent-blueprints/tree/main/semantic-kernel-blueprints/video-translation-agent) | Translates videos between languages with customizable speech and subtitle output. Leverages Azure AI Foundry, Speech Services, and Blob Storage to support multilingual video localization for internal communications, education, and marketing. | Microsoft | Audio transcription, Speech synthesis, Subtitle generation | Beginner-friendly | Single-Agent | Media & Communications | TBD |

