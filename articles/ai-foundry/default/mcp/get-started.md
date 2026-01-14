---
title: Get started using Foundry MCP Server with Visual Studio Code
description: Learn how to connect to and consume Foundry MCP Server operations with Visual Studio Code
keywords: azure developer cli, azd
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 11/04/2025
ms.topic: get-started
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Get started with Foundry MCP Server (preview) using Visual Studio Code

Foundry MCP Server (preview) is a Microsoft-managed, cloud-hosted implementation of the Model Context Protocol (MCP). It exposes curated tools that let your agents perform read and write operations against Foundry services without calling backend APIs directly.

Use an MCP-compliant client such as Visual Studio Code to connect to the public endpoint, authenticate with Entra ID, and let LLMs access the tools. After you connect, you can build agents that invoke these tools with natural language prompts.

In this article, you learn how to:

- Connect to Foundry MCP Server with GitHub Copilot in Visual Studio Code
- Run prompts to test Foundry MCP Server tools and interact with Azure resources

[!INCLUDE [preview-feature](../../openai/includes/preview-feature.md)]

## Prerequisites

- Azure account with an active subscription. If you don't have one, [create a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Foundry project. If you don't have a project, create one with the [Microsoft Foundry SDK Quickstart](/azure/ai-foundry/quickstarts/get-started-code?tabs=python#first-run-experience).
- [Visual Studio Code](https://code.visualstudio.com/download).
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) Visual Studio Code extension.

## Benefits of Foundry MCP Server

- **Cloud-hosted interface for AI tool orchestration**: Foundry MCP Server (preview) provides a secure, scalable endpoint for MCP-compliant clients. You don't need to deploy infrastructure, enabling seamless integration and multi-agent scenarios.
- **Identity and access control**: The server enforces authentication and authorization with Microsoft Entra ID. It performs all operations within the authenticated user's permissions (On-Behalf-Of flow).
- **Scenario-focused, extensible tools**: The MCP Server exposes a growing set of tools for read and write operations on models, deployments, evaluations, and agents in Foundry. The tools are extensible, letting developers and agents interact with services without knowing backend APIs or data schemas.
- **Accelerated agent and developer productivity**: Natural language workflows (via MCP clients and large language models) enable rapid tool discovery and invocation, streamlining development and multi-agent orchestration.

## Install and start Foundry MCP Server

Select an option to install Foundry MCP Server in Visual Studio Code.

## [User profile](#tab/user)

Install Foundry MCP Server in your user profile so it's available to all workspaces in Visual Studio Code.

1. Open the **Command Palette** (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).
1. Search for **MCP:Add Server**.
1. Select the **HTTP (Http or Server-Sent Events)** option.
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
1. Search for and select **MCP:List Servers**.
1. Select Foundry MCP Server you added and choose **Start Server**.
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
        "azure-ai-foundry-mcp-preview": { 
          "type": "http", 
          "url": "https://mcp.ai.azure.com" 
        } 
      } 
    }
    ```

1. Save your changes to `mcp.json`.
1. Select the **Start** button above the new server entry. 
1. When prompted, sign in so the MCP server can interact with services in your subscription.
1. Open GitHub Copilot and select Agent Mode.
1. Select the tools icon, search for *Foundry* to filter the results, and confirm the server appears.

    :::image type="content" source="../media/mcp/foundry-mcp-server-tools.png" alt-text="A screenshot showing Foundry MCP Server as GitHub Copilot tool.":::

    To learn more about Agent Mode, visit the [Visual Studio Code Documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

---

## Use prompts to test Foundry MCP Server

1. Open the GitHub Copilot chat panel and confirm **Agent Mode** is selected.
1. Enter a prompt that uses Foundry MCP Server tools—for example *Tell me about the latest models on Foundry*.
1. Copilot requests permission to run the required Foundry MCP Server operation. Select **Continue** or use the arrow to choose a more specific behavior:

    - **Current session** always runs the operation in the current GitHub Copilot Agent Mode session.
    - **Current workspace** always runs the command for the current Visual Studio Code workspace.
    - **Always allow** sets the operation to always run for any GitHub Copilot Agent Mode session or any Visual Studio Code workspace.

    :::image type="content" source="../media/mcp/foundry-mcp-server-run-tool.png" alt-text="Screenshot of options to run Foundry MCP Server operations.":::

    The response resembles the following shortened output:

    ```text
    Latest / Notable Foundry Models (Preview Snapshot)
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

1. Explore and test Foundry MCP Server operations with other prompts, such as:

    ```text
    What tools can I use from Foundry MCP Server (preview)?
    Tell me about the latest models on Foundry
    Show me details about the GPT-5-mini model on Foundry
    ```

## Related content

* [Foundry MCP Server security and best practices](security-best-practices.md)
* [Foundry MCP Server tools and example prompts](available-tools.md)
