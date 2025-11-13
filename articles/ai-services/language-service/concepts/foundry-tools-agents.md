---
title: Azure Language tools and agents
titleSuffix: Foundry Tools
description: Learn about Azure Language integration with Foundry Tools, including Model Context Protocol (MCP) server endpoints, intent routing agents, and exact question answering agents for AI-powered conversational applications.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 11/05/2025
ms.author: lajanuar
---

# Azure Language tools and agents

Azure Language integrates with Foundry Tools to provide agents and endpoints for building conversational applications. These tools combine Azure Language's natural language processing capabilities with AI agent frameworks.

## Azure Language MCP server 🆕

The Azure Language MCP server in [**Foundry**](https://ai.azure.com/) connects AI agents to Azure Language services through the Model Context Protocol. This integration enables developers to build conversational applications with natural language processing while maintaining compliance and transparency.

The server transforms Azure Language services into agent-friendly endpoints that support real-time workflows. Implementing standard MCP protocols ensures consistent communication between AI agents and language services.

### Core capabilities

* **Language processing**: Access to Azure Language's comprehensive natural language processing (NLP) services, including [**Named Entity Recognition**](../named-entity-recognition/overview.md), [**Text Analytics for health**](../text-analytics-for-health/overview.md), [**Conversational Language Understanding**](../conversational-language-understanding/overview.md), [**Custom Question Answering**](../question-answering/overview.md), [**Language Detection**](../language-detection/overview.md), [**Sentiment Analysis**](../sentiment-opinion-mining/overview.md), [**Summarization**](../summarization/overview.md), [**Key Phrase Extraction**](../key-phrase-extraction/overview.md), and [**PII redaction**](../personally-identifiable-information/overview.md). These services process text with accuracy and support multiple languages.

* **Local deployment**: Azure Language also provides local MCP server where developers can host the server in their own environment. You can find the local MCP server and setup instructions in the [Quickstart for Language MCP Server](https://github.com/Azure-Samples/ai-language-samples) sample in our GitHub repository.

* ***Remote MCP Server Endpoint***

    ```bash
    https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview
    ```

## Azure Language Intent Routing agent 🆕

The Intent Routing agent in [**Foundry**](https://ai.azure.com/) manages conversation flows by combining intent classification with answer delivery. This agent creates a framework that ensures users receive accurate responses while maintaining operational control.

The agent, which is built on Azure Language's natural language understanding capabilities, processes user input through layers. The system analyzes messages to understand intentions, then users can implement logic to route requests through appropriate channels based on confidence levels.

The agent prioritizes deterministic behavior, making it suitable for enterprise applications where consistency is important.

### Prerequisites

Before setting up the Intent Routing agent, ensure you have the following resources and configurations in place:

* **Foundry resource**: You need an active Foundry resource to host your agent.

* **Project resources**: Create your CLU and CQA projects using one of the following resource types:
  * Foundry resource.
  * AI hub resource.
  * Azure Language in Foundry Tools resource.

* **Project deployments**: Deploy the following required projects:

  * Custom Question Answering (CQA) deployment - see [CQA Overview](../question-answering/overview.md).
  * Conversational Language Understanding (CLU) deployment - see [CLU Overview](../conversational-language-understanding/overview.md).

* **Custom connection setup**: Configure a custom connection between your agent project and the Language resources:
  * In your agent project management center, use "Custom keys" connection when adding the custom connection in the connected resources page.
  * Add a key-value pair with `Ocp-Apim-Subscription-Key` as the key name and your resource key as the value.
  * For Foundry and AI hub resources, find the resource key in the resource overview page in the Foundry portal management center.
  * For any resource type, you can also find the key in the Azure portal.
  * For detailed connection instructions, see [Create a connection](/azure/ai-foundry/how-to/connections-add).

### Key capabilities

* **Intent classification**: [**Conversational Language Understanding (CLU)**](../conversational-language-understanding/overview.md) analyzes user utterances to identify intents and extract entities. The system recognizes conversation patterns and understands context.

* **Response delivery**: [**Custom Question Answering (CQA)**](../question-answering/overview.md) provides responses drawn from curated knowledge sources. This capability ensures users receive consistent information that aligns with organizational standards.

* **Knowledge management**: Users can manage their intent definitions in CLU projects and manage pairs of question-answers in CQA projects. This capability provides oversight for the agent's knowledge base and response capabilities.

* **Fallback processing**: Users can easily add retrieval-augmented generation (RAG) to the agent to handle edge cases and uncommon questions by using approved knowledge sources.

* ***Download intent routing template code with Azure Developer CLI (azd)***

    ```azurecli
        azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/intent_routing_agent/versions/1
    ```

## Azure Language Exact Question Answering agent 🆕

The Exact Question Answering agent in [**Foundry**](https://ai.azure.com/) delivers responses to frequently asked business questions through a fully managed, no-code solution. This agent provides consistent answers to queries while maintaining governance and quality control.

The agent combines Azure AI Agent Service capabilities with [**Custom Question Answering**](../question-answering/overview.md) technology. This integration creates a solution with minimal setup while delivering performance and oversight.

The agent works well for scenarios where answer accuracy is important, such as customer service, help desk operations, or compliance information delivery.

In addition to creating the agent from the Exact Question Answering Agent template in Agent Catalog, users can also create the agent directly from their CQA project in the Foundry portal. More details can be found in [Create and deploy a CQA agent](../question-answering/how-to/deploy-agent.md).

### Prerequisites

Before setting up the Exact Question Answering agent, ensure you have the following resources and configurations in place:

* **Foundry resource**: You need an active Foundry resource to host your agent.

* **Project resources**: Create your CQA project using one of the following resource types:
  * Foundry resource.
  * AI hub resource.
  * Language resource.

* **Project deployment**: Deploy the following required project:

  * Custom Question Answering (CQA) deployment - see [CQA Overview](../question-answering/overview.md).


* **Custom connection setup**: Configure a custom connection between your agent project and the Language resources:
  * In your agent project management center, use "Custom keys" connection when adding the custom connection in the connected resources page.
  * Add a key-value pair with `Ocp-Apim-Subscription-Key` as the key name and your resource key as the value.
  * For Foundry and AI hub resources, find the resource key in the resource overview page in the Foundry portal management center.
  * For any resource type, you can also find the key in the Azure portal.
  * For detailed connection instructions, see [Create a connection](/azure/ai-foundry/how-to/connections-add).

* ***Download exact question answering template code with Azure Developer CLI (azd)***

    ```azurecli
        azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/exact_question_answering_agent/versions/1
    ```

### Key capabilities

* **Azure integration**: The agent integrates Azure AI Agent Service with [**Custom Question Answering**](../question-answering/overview.md) capabilities within Azure Language services. This integration eliminates complex configuration requirements and provides access to enterprise security and monitoring features.

* **No-code deployment**: Organizations can deploy and configure the agent through Foundry's visual interface without writing custom code. This approach enables business stakeholders to participate in knowledge base creation and maintenance.

* **Knowledge management**: Users can manage question-answer pairs in CQA projects, providing control over the agent's knowledge base and ensuring response accuracy.

* **Deterministic answering**: The agent returns exact verbatim responses as defined in the CQA project answers, ensuring consistent and controllable responses to questions.

* **Fallback processing**: Users can easily add retrieval-augmented generation (RAG) to handle queries outside the predefined knowledge base by using approved organizational content sources.

## Related content

[Configure Azure resources for Foundry](configure-azure-resources.md)
