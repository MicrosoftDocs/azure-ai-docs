---
title: 'How to use Microsoft SharePoint content with Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Microsoft SharePoint content.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 05/01/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---
# Use the Microsoft SharePoint tool

Integrate your Azure AI Agent with the **Microsoft Sharepoint** to chat with your private documents securely. You can connect to your SharePoint site, such as `contoso.sharepoint.com/sites/policies` to ground your Agents with that data. When a user sends a query, the agent will determine if SharePoint should be leveraged or not. If so, it will send a query using the SharePoint tool, which checks if the user has a Microsoft 365 copilot license and use managed identity to retrieve relevant documents they have access to. The scope of retrieval includes all supported documents in this SharePoint site. Lastly, the agent will generate responses based on retrieved information. With identity passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in SharePoint while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Prerequisites
1. Developers and end users have Microsoft 365 copilot license

1. Developers and end users have at least `AI Developer` RBAC role. 

1. Developers and end users have at least `READ` access to the SharePoint site.

## Setup  

> [!NOTE]
> 1. Supported document types: text data in the following format: `.pdf`, `.docx`, `.ppt`, `.txt`, `.aspx` 
> 2. We recommend you start with SharePoint sites that have: a simple folder structure and a small number of short documents. 

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. You can add the SharePoint tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal, in either the **Create and debug** or **Agent playground** screen for your agent, scroll down the setup pane on the right to knowledge. Then select **Add**.

   :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **SharePoint** and follow the prompts to add the tool. You can only add one per agent.

1. Click to add a new connection. Once you have added a connection, you can directly select from existing list.
   1. To create a new connection, you need to find `site_url` in your SharePoint site. You can add either a SharePoint site or a SharePoint folder. For a SharePoint site, it will look like `https://microsoft.sharepoint.com/teams/<site_name>`. For a SharePoint folder, it will look like `https://microsoft.sharepoint.com/teams/<site_name>/Shared%20documents/<folder_name>`

   1. Then, you can add it to your connection. Make sure you have selected the **is secret** option.

## Next steps

[See the full sample for SharePoint.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_sharepoint.py)