---
title: "Get started using Foundry MCP Server with Visual Studio Code"
description: "Connect to Foundry MCP Server from Visual Studio Code, authenticate with Entra ID, and run your first prompts against Foundry services."
keywords: mcp, model context protocol, foundry mcp server, visual studio code
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 03/12/2026
ms.topic: get-started
ms.service: azure-ai-foundry
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Get started with Microsoft Foundry MCP Server (preview) using Visual Studio Code

Foundry MCP Server (preview) is a cloud-hosted implementation of the Model Context Protocol (MCP). It exposes curated tools that let your agents perform read and write operations against Foundry services without calling backend APIs directly. You don't need to deploy infrastructure — the server provides a secure, scalable endpoint with built-in authentication through Microsoft Entra ID.

Use an MCP-compliant client such as Visual Studio Code to connect to the public endpoint, authenticate with Entra ID, and let LLMs access the tools. After you connect, you can build agents that invoke these tools with natural language prompts.

In this article, you learn how to:

- Connect to Foundry MCP Server with GitHub Copilot in Visual Studio Code
- Run prompts to test Foundry MCP Server tools and interact with Azure resources

This guide takes about 5 minutes to complete.

[!INCLUDE [preview-feature](../openai/includes/preview-feature.md)]

## Prerequisites

- Azure account with an active subscription. If you don't have one, [create a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you don't have a project, create one with the [Microsoft Foundry SDK Quickstart](/azure/ai-foundry/quickstarts/get-started-code?tabs=python#first-run-experience).
- [Visual Studio Code](https://code.visualstudio.com/download) (version 1.99 or later).
- A [GitHub Copilot](https://github.com/features/copilot) subscription (Individual, Business, or Enterprise).
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) Visual Studio Code extension.
- Contributor or higher role on the Foundry project you want to access.

## Install and start Foundry MCP Server

Select an option to install Foundry MCP Server in Visual Studio Code.

## [User profile](#tab/user)

Install Foundry MCP Server in your user profile so it's available to all workspaces in Visual Studio Code.

1. Open the **Command Palette** (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).
1. Search for **MCP: Add Server**.
1. Select the **HTTP (HTTP or Server-Sent Events)** option.
1. Enter `https://mcp.ai.azure.com` as the URL.
1. Enter a friendly name such as *foundry-mcp-remote*, then press <kbd>Enter</kbd>. Visual Studio Code adds the following server entry under your user profile:

    ```json
    { 
      "servers": { 
        "foundry-mcp-remote": { 
          "type": "http", 
          "url": "https://mcp.ai.azure.com" 
        } 
      } 
    }
    ```

1. Open the **Command Palette** (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).
1. Search for and select **MCP: List Servers**.
1. Select Foundry MCP Server you added and choose **Start Server**.
1. A green indicator appears next to the server name in **MCP: List Servers**, confirming the connection is active.
1. When prompted, sign in to Azure so the MCP server can interact with services in your subscription.
1. Open GitHub Copilot and select **Agent Mode**.
1. Select the tools icon, search for *Foundry* to filter the list, and confirm the server appears.

    :::image type="content" source="../media/mcp/foundry-mcp-server-tools.png" alt-text="Screenshot of GitHub Copilot Agent Mode tools list showing Foundry MCP Server tool.":::

    Learn more about Agent Mode in the [Visual Studio Code documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

## [Workspace install](#tab/workspace)

Install Foundry MCP Server for a specific workspace to scope it to that folder:

1. Open an empty folder or an existing project folder in Visual Studio Code.
1. In the folder root, create a `.vscode` folder if it doesn't exist.
1. Inside the `.vscode` folder, create a file named `mcp.json`, and add the following JSON.

    ```json
    { 
      "servers": { 
        "foundry-mcp-remote": { 
          "type": "http", 
          "url": "https://mcp.ai.azure.com" 
        } 
      } 
    }
    ```

1. Save your changes to `mcp.json`.
1. Select the **Start** button above the new server entry.
1. A green indicator appears next to the server name, confirming the connection is active.
1. When prompted, sign in so the MCP server can interact with services in your subscription.
1. Open GitHub Copilot and select Agent Mode.
1. Select the tools icon, search for *Foundry* to filter the results, and confirm the server appears.

    :::image type="content" source="../media/mcp/foundry-mcp-server-tools.png" alt-text="A screenshot showing Foundry MCP Server as GitHub Copilot tool.":::

    To learn more about Agent Mode, visit the [Visual Studio Code documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

---

## Use prompts to test Foundry MCP Server

1. Open the GitHub Copilot chat panel and confirm **Agent Mode** is selected.
1. Enter a prompt that uses Foundry MCP Server tools—for example *Tell me about the latest models on Foundry*.
1. Copilot requests permission to run the required Foundry MCP Server operation. Select **Continue** or use the arrow to choose a more specific behavior:

    - **Current session** always runs the operation in the current GitHub Copilot Agent Mode session.
    - **Current workspace** always runs the command for the current Visual Studio Code workspace.
    - **Always allow** sets the operation to always run for any GitHub Copilot Agent Mode session or any Visual Studio Code workspace.

    :::image type="content" source="../media/mcp/foundry-mcp-server-run-tool.png" alt-text="Screenshot of options to run Foundry MCP Server operations.":::

    The response resembles the following shortened output. Your actual results vary based on current model availability.

    ```text
    Latest / Notable Foundry Models (Preview Snapshot)
    
    1. Frontier & Reasoning Models
    gpt-4o (2024-11-20) – Flagship multimodal model; strong multi-turn coherence.
    o3 (2025-04-16) – Balanced reasoning with good accuracy/quality trade-off.
    o4-mini (2025-04-16) – Strong quality with better latency than o3.
    Phi-4 – Microsoft small frontier open model; competitive quality at lower cost.

    // Further output omitted
    ```

1. Explore and test Foundry MCP Server operations with other prompts, such as:

    ```text
    What tools can I use from Foundry MCP Server (preview)?
    Tell me about the latest models on Foundry
    Show me details about the GPT-4o model on Foundry
    ```

## Troubleshooting

| Issue | Resolution |
| ----- | ---------- |
| Server doesn't start | Verify you entered the URL `https://mcp.ai.azure.com` correctly. Open the **Command Palette** and run **MCP: List Servers** to check server status. |
| Authentication prompt doesn't appear | Make sure the GitHub Copilot extension is installed and you're signed in to Visual Studio Code with a Microsoft account that has access to your Azure subscription. |
| Foundry tools don't appear in Agent Mode | Confirm the server is running (green indicator in **MCP: List Servers**). Check that you selected **Agent Mode** in the Copilot chat panel, then select the tools icon and search for *Foundry*. |
| "Access denied" or permission errors | Verify you have Contributor or higher role on the Foundry project. The server uses On-Behalf-Of flow with your Entra ID credentials. |

## Clean up resources

To remove the server configuration:

- **User profile**: Open the **Command Palette**, run **MCP: List Servers**, select the Foundry server, and choose **Remove Server**.
- **Workspace**: Delete the server entry from the `.vscode/mcp.json` file in your project folder.

## Related content

> [!div class="nextstepaction"]
> [Foundry MCP Server tools and example prompts](available-tools.md)

* [Foundry MCP Server security and best practices](security-best-practices.md)
* [Foundry MCP Server tools and example prompts](available-tools.md)
