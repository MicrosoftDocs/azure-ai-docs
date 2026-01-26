---
title: Use Browser Automation in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to automate browser tasks using AI agents in Microsoft Foundry Agent Service. Configure Browser Automation with Playwright Workspaces to perform real-world tasks through natural language.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/09/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# Browser Automation (preview)

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Browser Automation documentation](../../../default/agents/how-to/tools/browser-automation.md?view=foundry&preserve-view=true).

> [!WARNING]
> The Browser Automation tool comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users' browsers, computers, and any accounts to which the browser or AI has access, including personal, financial, or enterprise systems. By using the Browser Automation tool, you are acknowledging that you bear responsibility and liability for any use of it and of any resulting agents you create with it, including with respect to any other users to whom you make Browser Automation tool functionality available, including through resulting agents. We strongly recommend using the Browser Automation tool on low-privilege virtual machines with no access to sensitive data or critical resources.

The Browser Automation tool enables users to perform real-world browser tasks through natural language prompts. Powered by [Microsoft Playwright Workspaces](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing), it facilitates multi-turn conversations to automate browser-based workflows such as searching, navigating, filling forms, and booking.

## How it works

The interaction begins when the user sends a user query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following url \<url\>."* Upon receiving the request, Foundry Agent Service creates an isolated browser session by using your own provisioned Playwright workspace. Each session is sandboxed for privacy and security. The browser session mimics a real user browsing experience, enabling interaction with complex web UIs (for example, class schedules, filters, or booking pages). The browser performs Playwright-driven actions, such as navigating to relevant pages, and applying filters or parameters based on user preferences (such as time, location, instructor). By combining the model with Playwright, the model can see the browser screen by parsing the HTML or XML pages into DOM documents. The model makes decisions and performs actions like clicking, typing, and navigating websites. You should exercise caution when using this tool.

An example flow is:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.
1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be a screenshot so the model can assess the current state with an updated screenshot or a click with X/Y coordinates indicating where the mouse should be moved.
1. The Browser Automation tool executes the action in a sandboxed environment.
1. After executing the action, The Browser Automation tool captures the updated state of the environment as a screenshot.
1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

   The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete a booking.

## Example scenarios

- Booking and reservations: Automate form filling and schedule confirmation across booking portals.
- Product discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Setup

1. Create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.
   1. [Generate an access token](https://aka.ms/pww/docs/manage-access-tokens) for the Playwright Workspace resource. 
   1. Access the workspace region endpoint in the **Workspace Details** page.
   1. Give the project identity a **Contributor** role on the Playwright Workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access).
1. Create a serverless connection in the Microsoft Foundry project with the Playwright workspace region endpoint and the Playwright workspace Access Token.
   1. Go to the [Foundry portal](https://ai.azure.com/) and select your project. Go to the **Management center** and select **connected resources**.
   1. Create a new **Serverless Model** connection, and enter the following information.

      - **Target URI**: The Playwright workspace region endpoint, for example `wss://{region}.api.playwright.microsoft.com/playwrightworkspaces/{workspaceId}/browsers`. The URI should start with `wss://` instead of `https://` if presented.

      For more information on getting this value, see the [PlayWright documentation](https://aka.ms/pww/docs/configure-service-endpoint).

      - **Key**: [Get the Playwright access token](https://aka.ms/pww/docs/generate-access-token).

   For more information on creating a connection, see [Create a connection](../../../how-to/connections-add.md).

1. Configure your client by adding a Browser Automation tool using the Azure Playwright connection ID.

## Transparency note

Review the [transparency note](/azure/ai-foundry/responsible-ai/agents/transparency-note#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](/azure/ai-foundry/responsible-ai/agents/transparency-note#considerations-when-choosing-a-use-case) when using this tool.
