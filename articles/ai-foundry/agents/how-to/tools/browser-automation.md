---
title: 'How to use browser automation in Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to automate browser tasks using AI agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 07/28/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

## Browser automation (preview)

> [!CUATION]
> We strongly recommend using the Browser Automation Tool on a low privilege virtual machine with no access to sensitive data.

Browser Automation tool enables users to perform real-world browser tasks through natural language prompts. Powered by [Microsoft Playwright Workspaces (preview)](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing), it facilitates multi-turn conversations to automate browser-based workflows such as searching, navigating, filling forms, and booking.

## How it works

The interaction begins when the user sends a user query to an agent connected to the browser automation tool. For example, *"Show me all available yoga classes this week from the following url <url>".* Upon receiving the request, Azure AI Foundry Agent Service creates an isolated browser session using your own provisioned Playwright workspace. Each session is sandboxed for privacy and security. The browser session mimics a real user browsing experience, enabling interaction with complex web UIs (for example, class schedules, filters, or booking pages). The browser performs Playwright-driven actions, such as navigating to relevent pages, and applying filters or parameters based on user preferences (such as time, location, instructor).  Combining the model with Playwright allows the model to see the browser screen by parsing the HTML or XML pages into DOM documents, make decisions, and perform actions like clicking, typing, and navigating websites. You should exercise caution when using this tool.

An example flow would be:

1. A user sends a request to the model that includes a call to the browser automation tool with the URL you want to go to.

1. The tool receives a response from the model. If the response has actions for it to take, those steps contain suggested actions to make progress toward the specified goal. For example an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.

1. The tool executes the action in a sandboxed environment.

1. After executing the action, the tool captures the updated state of the environment as a screenshot.

1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

The browser automation tool supports multi-turn conversations, allowing the user to refine their request and complete a task, such as booking a flight.

## Example scenarios:

- Booking & Reservations: Automate form-filling and schedule confirmation across booking portals.

- Product Discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Setup

## Playwright workspace resource setup:

1. Create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.

    1. [Generate an access token](https://aka.ms/pww/docs/manage-access-tokens) for the Playwright Workspace resource. 
    
    1. Access the workspace region endpoint in the **Workspace Details** page.
    1. Give the project identity a "Contributor" role on the Playwright Workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access). 
    
1. Create a serverless connection in the Azure AI Foundry project with the Playwright workspace region endpoint and the Playwright workspace Access Token.

    1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and select your project. Go to the **Management center** and select **connected resources**.

    1. Create a new **Serverless Model** connection, and enter the following information.

        * **Target URI**: The Playwright workspace region endpoint, for example `wss://{region}.api.playwright.microsoft.com/playwrightworkspaces/{workspaceId}/browsers`.

        For more information on getting this value, see the [PlayWright documentation](https://aka.ms/pww/docs/configure-service-endpoint)

    1. * **Key**: [Get the Playwright access token](https://aka.ms/pww/docs/generate-access-token)

    For more information on creating a connection, see [Create a connection](../../../how-to/connections-add.md?pivots=fdp-project).

1. Create a browser automation tool with your connection ID

## Transparency note

Review the [transparency note](/azure/ai-foundry/responsible-ai/agents/transparency-note#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The browser automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](/azure/ai-foundry/responsible-ai/agents/transparency-note#considerations-when-choosing-a-use-case) when using this tool.

The browser automation tool carries substantial security risks and user responsibility: Errors in AI judgment or malicious and misleading instructions on web pages can lead the AI to execute unintended commands, potentially compromising the security of your browser, computer, or any linked accounts, including personal, financial, or enterprise systems. By using the browser automation tool, you accept full responsibility and liability for its use and for any agents you create with it, including any impact on other users who gain access to the tool's functionality through your agents.