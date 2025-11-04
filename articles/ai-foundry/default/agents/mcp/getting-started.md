---
title: Get started using the Azure AI Foundry MCP Server with Visual Studio Code
description: Learn how to connect to and consume Azure AI Foundry MCP Server operations with Visual Studio Code
keywords: azure developer cli, azd
author: alexwolfmsft
ms.author: alexwolf
ms.date: 11/04/2025
ms.topic: get-started
ms.custom: build-2025
ai-usage: ai-assisted
---

# Get started with the Azure AI Foundry MCP Server using Visual Studio Code

Azure AI Foundry MCP Server is a cloud-hosted server implementation of the Model Context Protocol (MCP), managed by Microsoft. It provides tools through the MCP protocol that let developers and agents interact with Azure AI Foundry services.

Use an MCP-compliant client such as Visual Studio Code to connect to the public endpoint, authenticate with Entra ID, and let LLMs access the tools. Create agents that use the MCP tools.

In this article, you learn how to:

- Connect to the Azure AI Foundry MCP Server with GitHub Copilot in Visual Studio Code
- Run prompts to test Azure AI Foundry MCP Server tools and interact with Azure resources

## Prerequisites

- Azure account with an active subscription. If you don't have an account, [create a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) with a free trial subscription.
- Azure AI Foundry project. If you don't have a project, create one with the [Azure AI Foundry SDK Quickstart](/azure/ai-foundry/quickstarts/get-started-code?tabs=python#first-run-experience).
- [Visual Studio Code](https://code.visualstudio.com/download) 
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) Visual Studio Code extension.

## Benefits of Azure AI Foundry MCP Server

- **Cloud-hosted, unified interface for AI tool orchestration**: Azure AI Foundry MCP Server (preview) provides a secure, scalable endpoint for MCP-compliant clients. Customers don't need to deploy infrastructure. This enables seamless integration for AI developers and supports multi-agent scenarios.
- **Identity and access control**: The server enforces authentication and authorization with Microsoft Entra ID. It performs all operations within the authenticated user's permissions (On-Behalf-Of flow).
- **Scenario-focused, extensible tool collections**: The MCP Server exposes a growing set of tools for read and write operations on models, deployments, evaluations, and agents in Azure AI Foundry. The tools are extensible, letting developers and agents interact with Foundry services without knowing backend APIs or data schemas.
- **Accelerated agent and developer productivity**: Natural language workflows (via MCP clients and large language models) enable rapid tool discovery and invocation, streamlining development and multi-agent orchestration.

## Install and start Azure AI Foundry MCP Server

Select an option to install Azure AI Foundry MCP Server in Visual Studio Code.

## [User profile](#tab/user)

Install the Azure AI Foundry MCP Server in your user profile to make it available to all workspaces in Visual Studio Code.

1. Open the **Command Palette** in Visual Studio Code by selecting <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>.
1. Search for **MCP:Add Server**.
1. Select the **HTTP (Http or Server-Sent Events)** option.
1. Enter `https://mcp.ai.azure.com` as the URL.
1. Enter a friendly name, such as *azure-ai-foundry-mcp-preview*, then press <kbd>Enter</kbd>. Visual Studio Code adds the following server entry under your user profile:

    ```json
    { 
      "servers": { 
        "azure-ai-foundry-mcp-preview": { 
          "type": "http", 
          "url": "https://mcp.ai.azure.com" 
        } 
      } 
    }
    ```

1. Open the **Command Palette** by selecting <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>.
1. Search for and select **MCP:List Servers**.
1. Select the Azure AI Foundry MCP Server you added, then choose **Start Server**.
1. Visual Studio Code prompts you to sign in to Azure. Sign in so the MCP server can interact with services in your account. 
1. Open GitHub Copilot and select **Agent Mode**.
1. Select the tools icon to view the available tools. Search for *Foundry* to filter the list. You see the server you installed.

    :::image type="content" source="../media/mcp/foundry-mcp-server-tools.png" alt-text="Screenshot of GitHub Copilot Agent Mode tools list showing Azure AI Foundry MCP Server tool.":::

    Learn more about Agent Mode in the [Visual Studio Code documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

## [Workspace install](#tab/workspace)

Install Azure AI Foundry MCP Server for a specific workspace:

1. Open an empty folder or an existing project folder in Visual Studio Code.
1. In the folder root, create a `.vscode` folder if it doesn't exist.
1. Inside the `.vscode` folder, create a file named `mcp.json`, and add the following JSON.

    ```json
    { 
      "servers": { 
        "azure-ai-foundry-mcp-preview": { 
          "type": "http", 
          "url": "https://mcp.ai.azure.com" 
        } 
      } 
    }
    ```

1. Save your changes to `mcp.json`.
1. Select the **Start** button above the new server entry. 
1. VS Code prompts you to authenticate to Azure. Sign in with your account to let MCP server interact with services on your account. 
1. Open GitHub Copilot and select Agent Mode.
1. Select the tools icon to view the available tools. Search for *Foundry* to filter the results. You should see the server listed that you installed previously.

    :::image type="content" source="../media/mcp/foundry-mcp-server-tools.png" alt-text="A screenshot showing Azure AI Foundry MCP Server as GitHub Copilot tool.":::

    To learn more about Agent Mode, visit the [Visual Studio Code Documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

---

## Use prompts to test the Azure AI Foundry MCP Server

1. Open GitHub Copilot and select Agent Mode.
1. Enter a prompt that uses Azure AI Foundry MCP Server tools, such as *Tell me about the latest models on Azure AI Foundry*.
1. Copilot requests permission to run the necessary Azure AI Foundry MCP Server operation for your prompt. Select **Continue** or use the arrow to select a more specific behavior:

    - **Current session** always runs the operation in the current GitHub Copilot Agent Mode session.
    - **Current workspace** always runs the command for the current Visual Studio Code workspace.
    - **Always allow** sets the operation to always run for any GitHub Copilot Agent Mode session or any Visual Studio Code workspace.

    :::image type="content" source="../media/mcp/foundry-mcp-server-run-tool.png" alt-text="Screenshot of options to run Azure AI Foundry MCP Server operations.":::

    The previous prompt output resembles the following partial example:

    ```text
    Latest / Notable Azure AI Foundry Models (Preview Snapshot)
    Curated from the model catalog and benchmark data you requested. I've grouped by category and highlighted truly recent arrivals (2025 releases or late 2024 previews), plus why you'd pick them. Where available, I note cost, performance, or capability signals (e.g., throughput_gtps, reasoning focus, modality).
    
    1. Frontier & Reasoning Models
    gpt-5-pro (2025-10-06) – Latest flagship conversational / reasoning model from OpenAI; expect top-tier multi-turn coherence and complex tool orchestration.
    gpt-5 (2025-08-07), gpt-5-mini, gpt-5-nano – New performance tiers; mini/nano are cost-optimized for high-volume requests.
    o3-pro (2025-06-10) – High reasoning accuracy (multiple >0.95 accuracy slices) but very high latency (p50 ~102s) indicating chain-of-thought style deliberation. Use only for tasks requiring deep reasoning (complex math, logic).
    o3 (2025-04-16) – Balanced reasoning; much faster than o3-pro; good accuracy/quality trade-off.
    o4-mini (2025-04-16) – Successor in "o" line; strong quality with better latency than o3-pro.
    Phi-4 (versions through 7) – Microsoft small frontier open model; competitive quality at radically lower token cost (input $0.125 / 1M tokens). Strong for cost-sensitive general tasks.

    // Further output omitted
    ```

1. Explore and test Azure AI Foundry MCP Server operations with other relevant prompts, such as:

        ```text
    What tools can I use from Azure AI Foundry MCP Server (preview)?
    Tell me about the latest models on Azure AI Foundry
    Show me details about the GPT-5-mini model on Azure AI Foundry
    ```

## Next steps

> [!div class="nextstepaction"]
> [Explore Azure AI Foundry MCP Server tools](../../tools/index.md)
