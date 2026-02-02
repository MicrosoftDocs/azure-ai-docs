---
title: Govern Tools by Using an AI Gateway
titleSuffix: Microsoft Foundry
description: Learn how to use an AI gateway and Azure API Management policies to govern MCP tools for agents in Microsoft Foundry.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/20/2026
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents,  pilot-ai-workflow-jan-2026
ai-usage: ai-assisted  
---

# Govern tools by using an AI gateway (preview)

An AI gateway in Microsoft Foundry provides a single, governed entry point for tools that you add to Foundry projects. After a gateway is connected, all new Model Context Protocol (MCP) tools are routed through a secure gateway endpoint that consistently enforces authentication, policies, and usage limits.

This feature is in preview. Only new MCP tools created in the Foundry portal that don't use managed OAuth are routed through an AI gateway.

## Prerequisites

- The AI gateway must be connected to the Microsoft Foundry resource. Follow the steps in [Configure an AI gateway in your Foundry resources](../../../configuration/enable-ai-api-management-gateway-portal.md).
  
  Governance is activated at the Microsoft Foundry resource level. All governance functionality depends on this connection.

- The MCP server must support one of the following authentication methods:

  - Managed identity (Microsoft Entra)
  - Key-based (API key or token)
  - Custom OAuth identity passthrough
  - Unauthenticated (if applicable)

## Key benefits

- Secure routing for all new MCP tools through a gateway endpoint
- Consistent access control and authentication enforcement
- Centralized observability for gateway traffic (such as logs and metrics)
- Unified policies for throttling, IP restrictions, and routing
- Seamless reuse of tools through public and private catalogs

## Govern a tool

The following sections walk you through setting up an AI gateway as a governed entry point.

### Add a tool

To add a tool to be governed, use either of these methods in the Foundry portal:

- Use the tool catalog by selecting **Tools** > **Catalog**. Then choose an MCP server to add.
- Add a custom tool by selecting **Build** > **Tools** > **Custom** > **Model Context Protocol**. Then paste your MCP server endpoint and select an authentication type.

For more information about MCP tools, see [Connect to Model Context Protocol servers](model-context-protocol.md).

### Confirm routing

Ensure that the following information is correct for your MCP server:

- Remote MCP server endpoint (AI gateway endpoint)
- Redirect URL, if you're using custom OAuth identity passthrough
- Authentication method, if you're using key-based authentication or OAuth identity passthrough
- Which agents are using this tool

### Apply policies

In the [Azure portal](https://portal.azure.com/), go to your resource. Select **API Management** to apply [policies](/azure/api-management/api-management-howto-policies) for governance.

You must apply policies through Azure API Management. Common policies include:

- **Rate limiting**: Limit how many calls a project or user can make in one minute.

    ```xml
    <inbound>
      <base />
      <rate-limit-by-key calls="60" renewal-period="60" counter-key="@(context.Request.IpAddress)" />
    </inbound>
    ```

- **IP filtering**: Allow requests from only trusted networks.

    ```xml
    <inbound>
      <base />
      <ip-filter action="allow">
        <address>10.0.0.0/24</address> <!-- internal network -->
        <address>20.50.123.45</address> <!-- trusted app -->
      </ip-filter>
    </inbound> 
    ```

- **Correlation ID**: Add a unique request ID so that you can trace requests later in logs.

    ```xml
    <inbound>
      <base />
        <set-header name="X-Correlation-Id" exists-action="override"> 
        <value>@(context.RequestId)</value>
      </set-header>
    </inbound>
    ```

- **Removal of sensitive headers**: Clean up incoming requests to help protect credentials or session data.

    ```xml
    <inbound>
      <base />
      <set-header name="Cookie" exists-action="delete" />
      <set-header name="Referer" exists-action="delete" />
    </inbound>
    ```

    > [!IMPORTANT]
    > Avoid deleting authentication headers (such as `Authorization`) unless you're sure that the MCP server doesn't require them.

- **Simple routing control**: If you have different backends (like ones for different geographies), you can route requests based on a header.

    ```xml
    <inbound>
      <base />
      <choose>
        <when condition="@(context.Request.Headers.GetValueOrDefault('X-Region','us') == 'eu')">
          <set-backend-service base-url="https://europe-api.contoso-mcp.net" />
        </when>
        <otherwise>
          <set-backend-service base-url="https://us-api.contoso-mcp.net" />
        </otherwise>
      </choose>
    </inbound>
    ```

For more policy XML examples, see the [API Management policy snippets](https://github.com/Azure/api-management-policy-snippets) repository on GitHub.

### Test with an agent

After you configure your MCP server, you can test it in the Foundry portal.

## Verify that governance is working

Use these steps to confirm that traffic is routed through the AI gateway and policies are applied:

1. In Foundry Tools, open your MCP tool configuration. Confirm that the configured tool endpoint points to the AI gateway (not directly to your MCP server).

1. In the Azure portal, open the API Management instance connected to your Foundry resource. Review metrics and logs to confirm that requests appear when your agent calls the tool.

## Security considerations

- Treat API keys, tokens, and OAuth client secrets as secrets. Store shared credentials in a project connection when possible, and limit who can access the project.
- Apply the least-privilege principle for managed identity and Microsoft Entra access.
- Review which headers you forward to backends. Remove only headers that you don't need, and avoid stripping required authentication headers.

For MCP authentication options, see [Set up authentication for Model Context Protocol (MCP) tools (preview)](../mcp-authentication.md).

## Troubleshooting

| Problem | Cause | Resolution |
| --- | --- | --- |
| The tool still calls the MCP server directly. | The tool was created before the AI gateway was connected, or the tool isn't eligible for gateway routing (for example, it uses managed OAuth). | Re-create the tool after the AI gateway is connected. Confirm that the tool is an MCP tool that doesn't use managed OAuth. |
| Tool calls fail after you add API Management policies. | A policy blocks traffic (rate limits, IP filtering) or modifies headers that the MCP server requires. | Temporarily disable policies to isolate the cause, and then refine the policy conditions. Avoid deleting required authentication headers. |
| OAuth sign-in fails for custom OAuth identity passthrough. | Redirect URL or OAuth app configuration is incorrect. | Re-check the redirect URL in your OAuth app registration and confirm required OAuth settings. For options and terminology, see [Set up authentication for Model Context Protocol (MCP) tools (preview)](../mcp-authentication.md). |
| You don't see request traces in the AI gateway. | The AI gateway doesn't log tool traces. | Use API Management logging and metrics for gateway traffic. Use your MCP server logs for tool-level details. |

## Limitations

- AI gateways support only MCP tools. Foundry-based tools such as SharePoint, code-first MCP tools, tools with managed OAuth, or OpenAPI tools aren't supported.
- AI gateways don't log tool traces.
- Gateway routing is applied only at tool creation. Existing tools aren't automatically mediated with AI gateways.
- API gateways support the application of API Management policies only in the Azure portal, not the Foundry portal.

For a broader list of Foundry Agent Service tool support when you're working with gateways, see [Bring your own AI gateway to Azure AI Agent Service (preview)](../ai-gateway.md).

## Related content

- [Connect to Model Context Protocol servers (preview)](model-context-protocol.md)
- [Set up authentication for Model Context Protocol (MCP) tools (preview)](../mcp-authentication.md)
- [Discover and manage tools in the Foundry tool catalog (preview)](../../concepts/tool-catalog.md)
