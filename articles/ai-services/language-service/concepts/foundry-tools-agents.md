---
title: Azure Language in Foundry Tools - tools and agents
titleSuffix: Foundry Tools
description: Learn how Azure Language in Foundry Tools integrates with Microsoft Foundry, including Model Context Protocol (MCP) server endpoints, intent routing agents, and exact question answering agents.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 02/06/2026
ms.author: lajanuar
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Azure Language tools and agents

Azure Language in Foundry Tools provides agents and endpoints for building conversational applications. These tools combine Azure Language natural language processing capabilities with Microsoft Foundry agent experiences.

This article introduces the Azure Language integrations that are available in Foundry Tools:

* An Azure Language Model Context Protocol (MCP) server endpoint.
* An intent routing agent that combines Conversational Language Understanding (CLU) and Custom Question Answering (CQA).
* An exact question answering agent that uses CQA to return curated, deterministic responses.

> [!IMPORTANT]
> The Azure Language tools and agents described in this article are currently in preview. See the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) for legal terms that apply.

The following table summarizes each integration to help you choose the right one for your scenario:

| Feature | Best for | Key technology | Setup complexity |
|---------|----------|---------------|------------------|
| **MCP server** | Adding Azure Language NLP capabilities to any MCP-compatible agent | Model Context Protocol | Low — configure a connection and endpoint |
| **Intent routing agent** | Multi-intent conversations that need deterministic routing with fallback | CLU + CQA | Medium — deploy CLU and CQA projects |
| **Exact question answering agent** | FAQ-style scenarios that require consistent, verbatim answers | CQA | Low — deploy a CQA project, no code required |

## Key concepts

* **Agent**: An AI experience that can interpret user input and choose actions or tools to complete tasks.
* **Tool**: A capability an agent can call to retrieve information or perform actions.
* **Model Context Protocol (MCP)**: An open protocol for exposing tools and contextual data to agents and large language models.
* **Connected resources and connections**: Configuration in Microsoft Foundry that lets an agent access external services (including credentials).

## Azure Language MCP server (preview)

The Azure Language MCP server in the [Foundry portal](https://ai.azure.com/) connects agents to Azure Language services through the Model Context Protocol (MCP). This integration helps you build conversational applications that can call Azure Language capabilities as tools.

The MCP server exposes Azure Language features through an agent-friendly endpoint that supports real-time workflows.

### Core capabilities

* **Language processing**: Access to Azure Language natural language processing (NLP) capabilities, including [Named Entity Recognition](../named-entity-recognition/overview.md), [Text Analytics for health](../text-analytics-for-health/overview.md), [Conversational Language Understanding](../conversational-language-understanding/overview.md), [Custom Question Answering](../question-answering/overview.md), [Language Detection](../language-detection/overview.md), [Sentiment Analysis](../sentiment-opinion-mining/overview.md), [Summarization](../summarization/overview.md), [Key Phrase Extraction](../key-phrase-extraction/overview.md), and [PII redaction](../personally-identifiable-information/overview.md).

* **Local deployment**: Azure Language also provides a local MCP server that you can host in your own environment. For setup guidance, see the Azure Language MCP Server quickstart in the [Azure Language samples repository](https://github.com/Azure-Samples/ai-language-samples).

* **Remote MCP server endpoint**

    ```bash
    https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview
    ```

### Prerequisites

To use the Azure Language MCP server with agents:

* An Azure subscription. [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* A Foundry resource and project. You need Contributor or Owner role on the resource group.
* An Azure Language resource.
* A configured connection in your Foundry project so the agent can authenticate to the Azure Language endpoint.

For connection setup details, see [Create a connection](../../../ai-foundry/how-to/connections-add.md?view=foundry&preserve-view=true).

### Security considerations

If you authenticate with API keys, treat keys as secrets:

* Store keys in a secure secret store and rotate them regularly.
* Avoid embedding keys directly in source code, scripts, or documentation.

### Limitations

Some Foundry configurations restrict which MCP servers you can use. For example, network-secured Foundry projects can require publicly accessible MCP servers. For details, see [Connect to Model Context Protocol servers (preview)](../../../ai-foundry/default/agents/how-to/tools/model-context-protocol.md).

## Azure Language intent routing agent (preview)

The intent routing agent in the [Foundry portal](https://ai.azure.com/) manages conversation flows by combining intent classification with answer delivery. It helps you route user questions to curated answers when possible, and fall back to other approaches when needed.

The agent, which is built on Azure Language natural language understanding capabilities, processes user input through layers. The system analyzes messages to understand intentions, then you can implement logic to route requests through appropriate channels based on confidence levels.

The agent prioritizes deterministic behavior, making it suitable for enterprise applications where consistency is important.

### Prerequisites

Before you set up the intent routing agent, make sure you have the following resources and configurations in place:

* **Azure subscription**: [Create one for free](https://azure.microsoft.com/free/cognitive-services). You need Contributor or Owner role on the resource group.

* **Foundry resource**: You need an active Foundry resource to host your agent.

* **Project resources**: Create your CLU and CQA projects using one of the following resource types:
  * Foundry resource.
  * AI hub resource.
  * Azure Language resource.

* **Project deployments**: Deploy the following required projects:

  * Custom Question Answering (CQA) deployment. See [CQA Overview](../question-answering/overview.md).
  * Conversational Language Understanding (CLU) deployment. See [CLU Overview](../conversational-language-understanding/overview.md).

* **Custom connection setup**: Configure a custom connection between your agent project and the Azure Language resources. For the full connection setup steps, see [Set up a custom connection](#set-up-a-custom-connection).

### Key capabilities

* **Intent classification**: [**Conversational Language Understanding (CLU)**](../conversational-language-understanding/overview.md) analyzes user utterances to identify intents and extract entities. The system recognizes conversation patterns and understands context.

* **Response delivery**: [**Custom Question Answering (CQA)**](../question-answering/overview.md) provides responses drawn from curated knowledge sources. This capability ensures users receive consistent information that aligns with organizational standards.

* **Knowledge management**: You can manage your intent definitions in CLU projects and manage pairs of question-answers in CQA projects. This capability provides oversight for the agent's knowledge base and response capabilities.

* **Fallback processing**: You can add retrieval-augmented generation (RAG) to the agent to handle edge cases and uncommon questions by using approved knowledge sources.

### Get the template

Download the intent routing template code with Azure Developer CLI (`azd`):

```bash
azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/intent_routing_agent/versions/1
```

After the command completes, the template scaffolds a project directory with configuration files and sample code.

## Azure Language Exact Question Answering agent (preview)

The **Exact Question Answering** agent in the [Foundry portal](https://ai.azure.com/) delivers responses to frequently asked business questions through a fully managed, no-code solution. This agent provides consistent answers to queries while maintaining governance and quality control.

The agent combines Foundry Agent Service capabilities with [**Custom Question Answering**](../question-answering/overview.md) technology. This integration creates a solution with minimal setup while delivering performance and oversight.

The agent works well for scenarios where answer accuracy is important, such as customer service, help desk operations, or compliance information delivery.

In addition to creating the agent from the exact question answering agent template in Agent Catalog, you can also create the agent directly from your CQA project in the Foundry portal. For more information, see [Create and deploy a CQA agent](../question-answering/how-to/deploy-agent.md).

### Prerequisites

Before you set up the exact question answering agent, make sure you have the following resources and configurations in place:

* **Azure subscription**: [Create one for free](https://azure.microsoft.com/free/cognitive-services). You need Contributor or Owner role on the resource group.

* **Foundry resource**: You need an active Foundry resource to host your agent.

* **Project resources**: Create your CQA project using one of the following resource types:
  * Foundry resource.
  * AI hub resource.
  * Azure Language resource.

* **Project deployment**: Deploy the following required project:

  * Custom Question Answering (CQA) deployment. See [CQA Overview](../question-answering/overview.md).

* **Custom connection setup**: Configure a custom connection between your agent project and the Azure Language resources. For the full connection setup steps, see [Set up a custom connection](#set-up-a-custom-connection).

### Get the template

Download the exact question answering template code with Azure Developer CLI (`azd`):

```bash
azd ai agent init -m azureml://registries/azureml-staging/agentmanifests/exact_question_answering_agent/versions/1
```

After the command completes, the template scaffolds a project directory with configuration files and sample code.

### Key capabilities

* **Agent Service integration**: The agent integrates Agent Service with [**Custom Question Answering**](../question-answering/overview.md) capabilities within Azure Language services. This integration eliminates complex configuration requirements and provides access to enterprise security and monitoring features.

* **No-code deployment**: Organizations can deploy and configure the agent through the Foundry visual interface without writing custom code. This approach enables business stakeholders to participate in knowledge base creation and maintenance.

* **Knowledge management**: You can manage question-answer pairs in CQA projects, providing control over the agent's knowledge base and ensuring response accuracy.

* **Deterministic answering**: The agent returns exact verbatim responses as defined in the CQA project answers, ensuring consistent and controllable responses to questions.

* **Fallback processing**: You can add retrieval-augmented generation (RAG) to handle queries outside the predefined knowledge base by using approved organizational content sources.

## Set up a custom connection

Both the intent routing agent and the exact question answering agent require a custom connection between your agent project and Azure Language resources. Follow these steps to configure the connection:

1. In your agent project management center, select **Connected resources**.
1. Select **Custom keys** when you add the custom connection.
1. Add a key-value pair with `Ocp-Apim-Subscription-Key` as the key name and your resource key as the value.
1. For Foundry and AI hub resources, find the resource key on the resource overview page in the Foundry portal management center.
1. For any resource type, you can also find the key in the Azure portal.

For detailed connection instructions, see [Create a connection](../../../ai-foundry/how-to/connections-add.md?view=foundry&preserve-view=true).

To verify the connection is working, send a test message to the agent. If the agent returns a response from your CQA knowledge base, the connection is configured correctly.

## Troubleshooting

* **The agent returns authentication errors**: Confirm the connection uses the `Ocp-Apim-Subscription-Key` header name and that the value matches your Azure Language resource key.
* **The agent doesn't use CLU or CQA as expected**: Confirm your CLU and CQA projects are deployed and that the agent is connected to the correct resources.
* **Responses are low confidence or irrelevant**: Review CLU intent training data and CQA question-answer pairs, then redeploy your projects.
* **The MCP server returns a 404 or connection error**: Verify the endpoint URL uses the correct Foundry resource name and API version. Confirm the Azure Language resource is in a supported region.
* **The `azd ai agent init` command fails**: Make sure you have the latest version of the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) installed and that you're signed in with `azd auth login`.

## Related content

* [Configure Azure resources for Foundry](configure-azure-resources.md)
* [Create and deploy a CQA agent](../question-answering/how-to/deploy-agent.md)
* [Connect to Model Context Protocol servers (preview)](../../../ai-foundry/default/agents/how-to/tools/model-context-protocol.md)

