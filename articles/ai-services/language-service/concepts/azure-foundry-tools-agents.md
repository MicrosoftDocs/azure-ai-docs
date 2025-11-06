---
title: Azure Language tools and agents
titleSuffix: Azure AI Foundry Tools
description: Learn about Azure Language integration with Foundry Tools, including MCP server endpoints, intent routing agents, and exact question answering agents for AI-powered conversational applications.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 11/05/2025
ms.author: lajanuar
---

# Azure Language tools and agents

Azure Language integrates with Azure AI Foundry Tools to provide agents and endpoints for building conversational applications. These tools combine Azure Language's natural language processing capabilities with AI agent frameworks.

## Azure Language MCP server 🆕

The Azure Language MCP server connects AI agents to Azure Language services through the Model Context Protocol. This integration enables developers to build conversational applications with natural language processing while maintaining compliance and transparency.

The server transforms Azure Language services into agent-friendly endpoints that support real-time workflows. By implementing standard MCP protocols, it ensures consistent communication between AI agents and language services.

### Core capabilities

* **Language processing**: Access to Azure Language's NLP services, including sentiment analysis, entity recognition, key phrase extraction, and language detection. These services process text with accuracy and support multiple languages.

* **Compliance and privacy**: Built-in PII detection and redaction help organizations meet regulatory requirements by identifying and protecting sensitive information. The server maintains audit trails and supports privacy policies.

* **Question answering**: Custom Question Answering integration enables domain-specific knowledge retrieval. Organizations can deploy their own knowledge bases and provide agents with access to information sources.

* **Extensible architecture**: The modular design supports expansion with additional Azure Language services and custom processing modules.

> ***MCP Server Endpoint***

```bash
https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp
```

## Azure Language Intent Routing agent 🆕

The Intent Routing agent manages conversation flows by combining intent classification with answer delivery. This agent creates a framework that ensures users receive accurate responses while maintaining operational control.

Built on Azure Language's natural language understanding capabilities, the agent processes user input through layers. The system analyzes messages to understand intentions, then routes requests through appropriate channels based on confidence levels and business rules.

The agent prioritizes deterministic behavior, making it suitable for enterprise applications where consistency is important.

### Key capabilities

* **Intent classification**: Conversational Language Understanding (CLU) analyzes user utterances to identify intents and extract entities. The system recognizes conversation patterns and understands context.

* **Response delivery**: Custom Question Answering (CQA) provides responses drawn from curated knowledge sources. This ensures users receive consistent information that aligns with organizational standards.

* **Routing logic**: The agent implements decision trees that route conversations based on confidence scores, intent types, and business policies. High-confidence requests receive immediate responses, while uncertain queries trigger human review processes.

* **Governance**: Built-in oversight mechanisms enable human review, approval workflows, and audit logging for routing decisions. Organizations can monitor agent performance and maintain compliance.

* **Fallback processing**: Retrieval-augmented generation (RAG) handles edge cases and uncommon questions by leveraging approved knowledge sources.

> ***Download template code with Azure Developer CLI (azd)***

```bash
azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/intent_routing_agent/versions/1
```

## Azure Language Exact Question Answering agent 🆕

The Exact Question Answering agent delivers responses to frequently asked business questions through a fully managed, no-code solution. This agent provides consistent answers to queries while maintaining governance and quality control.

The agent combines Azure AI Agent Service capabilities with Custom Question Answering technology. This integration creates a solution with minimal setup while delivering performance and oversight.

The agent works well for scenarios where answer accuracy is important, such as customer service, helpdesk operations, or compliance information delivery.

### Key capabilities

* **Azure integration**: The agent integrates Azure AI Agent Service with Custom Question Answering capabilities within Azure Language services. This integration eliminates complex configuration requirements and provides access to enterprise security and monitoring features.

* **No-code deployment**: Organizations can deploy and configure the agent through Azure AI Foundry's visual interface without writing custom code. This approach enables business stakeholders to participate in knowledge base creation and maintenance.

* **Governance framework**: Oversight capabilities include human review workflows, policy-based response controls, and escalation procedures for complex queries. Organizations can implement approval processes and audit trails.

* **Automation**: The agent handles routine business questions through deterministic logic that ensures consistent responses regardless of query variations or timing.

* **Fallback processing**: For queries outside the predefined knowledge base, retrieval-augmented generation (RAG) provides responses by leveraging approved organizational content sources.

> ***Download template code with Azure Developer CLI (azd)***

```bash
azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/exact_question_answering_agent/versions/1
```

## Related content

[Configure Azure resources for Azure AI Foundry](configure-azure-resources.md)