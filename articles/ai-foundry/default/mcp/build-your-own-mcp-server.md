---
title: Build and register a Model Context Protocol (MCP) server
ms.reviewer: samuelzhang
description: Learn how to build a custom MCP server using Azure Functions, register it in your organizational tool catalog, and connect it to Foundry Agent Service.
#customer intent: As a developer, I want to build a custom MCP server using Azure Functions so that I can integrate internal APIs with Foundry Agent Service.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/07/2025
ms.custom: ai-assisted
---

# Build and register a Model Context Protocol (MCP) server

Model Context Protocol (MCP) provides a standard interface for AI agents to interact with APIs and external services. When you need to integrate private or internal enterprise systems that don't have existing MCP server implementations, you can build your own custom server. This article shows you how to create a remote MCP server using Azure Functions, register it in a private organizational tool catalog using Azure API Center, and connect it to Foundry Agent Service.

This approach enables you to securely integrate internal APIs and services into the Microsoft Foundry ecosystem, allowing agents to call your enterprise-specific tools through a standardized MCP interface.

## Prerequisites

- A Foundry project with Agent Service enabled. For setup instructions, see [Quickstart: Get started with Agent Service](../../agents/quickstart.md).
- [Python](https://www.python.org/downloads/) version 3.11 or higher installed on your local development machine.
- [Azure Functions Core Tools](/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools) version 4.0.7030 or higher.
- [Azure Developer CLI](https://aka.ms/azd) installed for deployment automation.
- For local development and debugging:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for Visual Studio Code
- An [Azure API Center resource](/azure/api-center/overview) (optional, required only for organizational tool catalog registration).

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

1. Deploy your MCP server to Azure by using the Azure Developer CLI:

   ```bash
   azd up
   ```

   Follow the prompts to select your Azure subscription and resource group.

1. After deployment completes, save the following information for later steps:

   | Item | Example or value |
   |------|------------------|
   | Remote MCP server endpoint | `https://{function_app_name}.azurewebsites.net/runtime/webhooks/mcp` |
   | Authentication information | For access key authentication, note the `mcp_extension` system key from the Azure portal |

For detailed implementation guidance, see [Quickstart: Build a custom remote MCP server using Azure Functions](/azure/azure-functions/scenario-custom-remote-mcp-server?pivots=programming-language-python).

## Register your MCP server in the organizational tool catalog

When you register your MCP server in Azure API Center, you create a private organizational tool catalog. This step is optional but recommended for sharing MCP servers across your organization with consistent governance and discoverability.

To register your MCP server:

1. Sign in to the [Azure portal](https://portal.azure.com) and go to your Azure API Center resource.

   > [!TIP]
   > The API Center name becomes your private tool catalog name in the registry filter. Choose an informative name that helps users identify your organization's tool catalog.

1. Register your remote MCP server by adding it as an API:

   a. In the left navigation pane, select **APIs**.
   
   b. Select **+ Add API** and provide the required information about your MCP server.
   
   c. Configure environments and deployments following the tutorial: [Add environments and deployments for APIs in Azure API Center](/azure/api-center/configure-environments-deployments).

1. Configure authentication for your MCP server (optional):

   a. In the left navigation pane of your API Center resource, select **Governance** > **Authorization**.

   :::image type="content" source="../media/build-your-own-mcp-server/azure-api-center-authorization-page.png" alt-text="Screenshot showing the Azure API Center authorization configuration page with Governance menu expanded." lightbox="../media/build-your-own-mcp-server/azure-api-center-authorization-page.png":::

   b. Select **Add configuration**.
   
   c. Choose the security scheme that matches your MCP server requirements:
      - **API Key**: Developers provide the API key during tool configuration in Foundry
      - **OAuth**: Configure OAuth 2.0 authentication parameters
      - **HTTP**: Configure bearer token authorization
   
   d. Provide the required authentication details for your selected scheme.

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

For detailed configuration steps, see [Connect to a Model Context Protocol server endpoint in Agent Service](../../agents/how-to/tools/model-context-protocol.md).

After connecting your MCP server, agents in your Foundry project can call the tools and functions exposed by your custom server. Test the connection by creating an agent and verifying it can successfully invoke your MCP server's capabilities.

## Troubleshooting

Here are some common issues you might encounter when building and connecting your MCP server:

- **MCP server connection fails**: Ensure that your Azure Function is running and accessible. Check the function logs in the Azure portal for any errors.
- **Authentication errors**: Verify that you're using the correct system key or API key. If using API Key authentication, ensure the key is correctly configured in the Foundry connection settings.
- **Tool not found**: If you registered your MCP server in the organizational catalog, make sure you've added it to your agent. If using a custom tool, verify the endpoint URL and tool name.

## Related content

- [Get started with Agent Service](../../agents/quickstart.md)
- [Connect to Model Context Protocol servers](../../agents/how-to/tools/model-context-protocol.md)
- [Add environments and deployments in Azure API Center](/azure/api-center/configure-environments-deployments)
- [Azure Functions Python developer guide](/azure/azure-functions/functions-reference-python)
