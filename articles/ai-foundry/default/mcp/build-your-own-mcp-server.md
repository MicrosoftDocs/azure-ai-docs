---
title: Build and register a Model Context Protocol (MCP) server
ms.reviewer: samuelzhang
description: Learn how to build a custom MCP server using Azure Functions, register it in your organizational tool catalog, and connect it to Foundry Agent Service.
keywords: Model Context Protocol, MCP server, Azure Functions, Azure API Center, tool catalog, Foundry Agent Service
#customer intent: As a developer, I want to build a custom MCP server using Azure Functions so that I can integrate internal APIs with Foundry Agent Service.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/05/2026
ai-usage: ai-assisted
ms.custom: ai-assisted
---

# Build and register a Model Context Protocol (MCP) server

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) provides a standard interface for AI agents to interact with APIs and external services. When you need to integrate private or internal enterprise systems that don't have existing MCP server implementations, you can build your own custom server. This article shows you how to create a remote MCP server using Azure Functions, register it in a private organizational tool catalog using Azure API Center, and connect it to Foundry Agent Service.

This approach enables you to securely integrate internal APIs and services into the Microsoft Foundry ecosystem, allowing agents to call your enterprise-specific tools through a standardized MCP interface.

## Prerequisites

- A Foundry project with Agent Service enabled. For setup instructions, see [Quickstart: Get started with Agent Service](../../agents/quickstart.md).
- An Azure subscription and permissions to create resources. At minimum, you typically need the Contributor role on the target resource group.
- [Python](https://www.python.org/downloads/) version 3.11 or higher installed on your local development machine.
- [Azure Functions Core Tools](/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools) version 4.0.7030 or higher.
- [Azure Developer CLI](https://aka.ms/azd) installed for deployment automation.
- For local development and debugging:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for Visual Studio Code
- An [Azure API Center resource](/azure/api-center/overview) (optional, required only for organizational tool catalog registration).

> [!NOTE]
> Agent Service connects only to publicly accessible MCP server endpoints.

## Understand the request flow

The high-level flow looks like this:

1. You deploy an MCP server (this article uses Azure Functions) that exposes one or more MCP tools.
1. You optionally register the server in Azure API Center so it shows up in an organizational tool catalog.
1. In Foundry portal, you connect the MCP server to Agent Service.
1. When an agent needs a tool, Agent Service calls your MCP server endpoint.
1. Your MCP server validates the request, calls your internal API, and returns the tool result.

## Build an MCP server by using Azure Functions

Azure Functions is a serverless compute service that provides scale-to-zero capability, burst scaling, and enterprise features including identity-based access and virtual networking. The lightweight programming model makes it straightforward to build MCP servers so you can focus on implementing your business logic rather than infrastructure management.

1. Open a terminal or command prompt and navigate to the folder where you want to create your project.

1. Run the `azd init` command to initialize the project from [this sample MCP server template](https://github.com/Azure-Samples/remote-mcp-functions-python):

   ```bash
   azd init --template remote-mcp-functions-python -e mcpserver-python
   ```

1. Review the sample code structure. The template includes:

   - Function definitions for MCP endpoints.
   - Configuration for authentication and authorization.
   - Deployment scripts for Azure.

1. Customize the MCP server functions to expose your specific APIs and services. Modify the function code to implement the tools and capabilities your agents need.

1. Test your MCP server locally by using the Azure Functions Core Tools:

   ```bash
   func start
   ```

   After the function host starts, verify the MCP endpoint is accessible:

   ```bash
   curl http://localhost:7071/runtime/webhooks/mcp
   ```

   You should receive an MCP server response. If you see errors, check the function app logs in the terminal output.

1. Deploy your MCP server to Azure by using the Azure Developer CLI:

   ```bash
   azd up
   ```

   Follow the prompts to select your Azure subscription and resource group.

1. After deployment completes, save the following information for later steps:

   - Remote MCP server endpoint: `https://{function_app_name}.azurewebsites.net/runtime/webhooks/mcp`
   - Authentication information: For access key authentication, note the `mcp_extension` system key in the Azure portal.

   If you prefer a CLI workflow to retrieve function access keys, see [Work with access keys in Azure Functions](/azure/azure-functions/function-keys-how-to?tabs=azure-cli#get-your-function-access-keys).

For additional implementation details including advanced authentication patterns and troubleshooting, refer to the tutorial [Host an MCP server on Azure Functions](/azure/azure-functions/functions-mcp-tutorial?tabs=mcp-extension&pivots=programming-language-python).

## Secure your MCP server endpoint

Before you share your MCP server with others, define and apply a security baseline:

- Require authentication. Avoid anonymous access unless your scenario explicitly needs it.
- Treat credentials as secrets. Don't hard-code keys in code or check them into source control. Store secrets in a secure store such as [Azure Key Vault](/azure/key-vault/general/overview).
- Implement least privilege for downstream calls. If your MCP server calls internal APIs, scope permissions to only what the exposed tools need.
- Log and monitor tool calls. Use Azure Functions logging to trace requests and troubleshoot failures.

For Agent Service authentication patterns (for example, key-based authentication, Microsoft Entra identities, and OAuth identity passthrough), see [MCP server authentication](../agents/how-to/mcp-authentication.md).

For governance and operational guidance when you run MCP tools, see [Foundry MCP Server best practices and security guidance](security-best-practices.md).

## Register your MCP server in the organizational tool catalog

When you register your MCP server in Azure API Center, you create a private organizational tool catalog. This step is optional but recommended for sharing MCP servers across your organization with consistent governance and discoverability.

To register your MCP server:

1. Sign in to the [Azure portal](https://portal.azure.com) and go to your Azure API Center resource.

   > [!TIP]
   > The API Center name becomes your private tool catalog name in the registry filter. Choose an informative name that helps users identify your organization's tool catalog.

1. In the left navigation pane, expand **Inventory** and select **Assets**.

1. Select **Register an asset** and choose **MCP server**.

1. Provide the required information about your MCP server.

1. Configure environments and deployments following the tutorial: [Add environments and deployments for APIs in Azure API Center](/azure/api-center/configure-environments-deployments).

1. Configure authentication for your MCP server (optional):

   In the left navigation pane of your API Center resource, select **Governance** > **Authorization**.

   :::image type="content" source="../media/build-your-own-mcp-server/azure-api-center-authorization-page.png" alt-text="Screenshot showing the Azure API Center authorization configuration page with Governance menu expanded." lightbox="../media/build-your-own-mcp-server/azure-api-center-authorization-page.png":::

1. Select **Add configuration**.

1. Choose the security scheme that matches your MCP server requirements:

   - **API Key**: Developers provide the API key during tool configuration in Foundry
   - **OAuth**: Configure OAuth 2.0 authentication parameters
   - **HTTP**: Configure bearer token authorization

1. Provide the required authentication details for your selected scheme.

   > [!NOTE]
   > If you choose API Key authentication, the key you store in Azure Key Vault isn't automatically used in Foundry. Developers must provide the API key when configuring the MCP server connection.

1. Configure access management (optional):

   a. Go to your registered MCP server in API Center.
   
   b. Select **Details** > **Versions** > **Manage Access (preview)**.
   
   c. Configure which users or groups can access this MCP server through the organizational catalog.

After registration, your MCP server appears in the Foundry tool catalog with the governance and authentication settings you configured.

## Connect the MCP server to Agent Service

You can connect your MCP server to Agent Service through the organizational tool catalog (if you registered it) or as a custom MCP tool.

### Connect using the organizational tool catalog

If you registered your MCP server in Azure API Center, users with appropriate access can discover and configure it:

1. In [Foundry portal](https://ai.azure.com), go to your project.

1. Go to **Build** > **Tools** or open Agent Builder.

1. Browse the organizational tool catalog to find your registered MCP server.

1. Follow the configuration guidance displayed in the tool catalog to add the server to your agent.

### Connect using a custom MCP tool

If you don't register your MCP server in the organizational catalog, add it directly as a custom tool:

1. In [Foundry portal](https://ai.azure.com), go to your project.

1. Go to **Build** > **Tools** or open Agent Builder.

1. Select **Add tool** > **Custom** > **Model Context Protocol**.

1. Enter your MCP server details:

   - **Name**: Unique name for your remote MCP server
   - **Remote MCP Server endpoint**: Enter your remote MCP server endpoint URL (for example, `https://{function_app_name}.azurewebsites.net/runtime/webhooks/mcp`)
   - **Authentication**: Select the authentication method. For **Key-based** authentication, provide the following credential:
       - **Credential**: `"x-functions-key": "{mcp_extension_system_key}"`

1. Select **Connect** to register the custom MCP tool.

For detailed configuration steps (including project connections and approval workflows), see [Connect to Model Context Protocol servers (preview)](../agents/how-to/tools/model-context-protocol.md).

After connecting your MCP server, agents in your Foundry project can call the tools and functions exposed by your custom server.

## Verify the MCP server works end to end

After you deploy and connect the server, verify that the server is discoverable and that an agent can successfully invoke a tool.

1. In Foundry portal, confirm the MCP server appears in your project tool list.
1. Create an agent (or open an existing agent) and add the MCP server tool.
1. Run a prompt that should require one of your MCP tools.
1. If approval is enabled, review the tool name and arguments, then approve the call.
1. Confirm the tool call succeeds.

   If the tool call fails, open the Function App logs in Azure portal to confirm the MCP endpoint was invoked and to diagnose errors.

## Troubleshooting

Here are some common issues you might encounter when building and connecting your MCP server:

- **MCP server connection fails**: Confirm the server URL is publicly reachable and uses the MCP webhook path (`/runtime/webhooks/mcp`). Check the Function App logs in Azure portal for errors.
- **Authentication errors (401/403)**: Verify you're using the correct key or token for the authentication method you selected. Rotate keys that might have been exposed, and update any saved credentials.
- **Tool discovery problems**: If you registered the server in Azure API Center, confirm the API is published and you have access to it. If you added a custom tool, confirm the endpoint URL is correct.
- **Tool call succeeds but an internal API fails**: Review your MCP server logs to confirm what request was sent to the downstream API. Verify the MCP server identity or API credentials have the required permissions.

## Clean up resources

When you're done, delete Azure resources created by the template to avoid ongoing charges.

1. In your MCP server project folder, run:

   ```bash
   azd down --purge
   ```

1. If you registered the server in Azure API Center, remove the API entry if you no longer need it.

## Related content

- [MCP server authentication](../agents/how-to/mcp-authentication.md)
- [Get started with Foundry MCP Server (preview) using Visual Studio Code](get-started.md)
- [Foundry MCP Server best practices and security guidance](security-best-practices.md)
- [Explore available tools and example prompts for Foundry MCP Server (preview)](available-tools.md)
- [Add environments and deployments in Azure API Center](/azure/api-center/configure-environments-deployments)
- [Azure Functions Python developer guide](/azure/azure-functions/functions-reference-python)
