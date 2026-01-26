---
title: 'Tools governance'
titleSuffix: Microsoft Foundry
description: Learn how to use AI Gateway and Azure API Management policies to govern MCP tools for agents in Microsoft Foundry.
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

# Tools governance with AI Gateway (preview)

AI Gateway in Microsoft Foundry provides a single, governed entry point for tools added to Microsoft Foundry projects. After a gateway is connected, all new MCP tools route through a secure gateway endpoint where authentication, policies, and usage limits are consistently enforced.

> [!NOTE]
> Only new MCP tools created in the Microsoft Foundry portal that don't use managed OAuth are routed through AI Gateway.

## Prerequisites

To enable governance for tools using AI Gateway in Microsoft Foundry:

- AI Gateway must be connected to the Microsoft Foundry resource
   - Governance is activated at the Microsoft Foundry resource level. All governance functionality depends on this connection.
- The MCP server must support one of the following authentication methods:
   - Managed identity (Microsoft Entra)
   - Key-based (API key or token)
   - Custom OAuth identity passthrough
   - Unauthenticated (if applicable)

## Key benefits

- Secure routing for all new MCP tools using a gateway endpoint
- Consistent access control and authentication enforcement
- Centralized observability for gateway traffic (such as logs and metrics)
- Unified policies for throttling, IP restrictions, and routing
- Seamless reuse of tools through public and private catalogs

## Enable AI Gateway for your Foundry resource

If AI Gateway isn't already connected to your Foundry resource, enable it first.

1. Follow the steps in [Configure AI Gateway in the Foundry portal](../../../configuration/enable-ai-api-management-gateway-portal.md).
1. Return to this article after AI Gateway is connected to your Foundry resource.

## Govern a tool

### Add a tool

To add a tool to be governed, use the Foundry portal. You can add a tool using the tool catalog by selecting **Tools** > **Catalog**, then choosing an MCP server to add.

You can also add a custom tool by selecting **Build** > **Tools** > **Custom** > **Model Context Protocol**. Then paste your MCP server endpoint and select an authentication type.

For more information about MCP tools, see [Connect to Model Context Protocol servers](model-context-protocol.md).

### Confirm routing

Ensure the following information is correct for your MCP server:
- Remote MCP server endpoint (AI gateway endpoint)
- Redirect URL (if using custom OAuth identity passthrough)
- Authentication method (key-based auth, OAuth identity passthrough)
- Which agents are using this tool

### Apply policies

Navigate to the [Azure portal](https://portal.azure.com/) page for your resource. Select **API Management** to apply needed policies for governance. [Policies](/azure/api-management/api-management-howto-policies) must be applied through API Management. Common policies include:

- Rate limiting - limit how many calls a project or user can make a minute.
    
    ```xml
    <inbound>
      <base />
      <rate-limit-by-key calls="60" renewal-period="60" counter-key="@(context.Request.IpAddress)" />
    </inbound>
    ```
- IP filtering - allow requests only from trusted networks.

    ```xml
    <inbound>
      <base />
      <ip-filter action="allow">
        <address>10.0.0.0/24</address> <!-- internal network -->
        <address>20.50.123.45</address> <!-- trusted app -->
      </ip-filter>
    </inbound> 
    ```
    
- Correlation ID - add a unique request ID so you can trace requests later in logs.
    
    ```xml
    <inbound>
      <base />
        <set-header name="X-Correlation-Id" exists-action="override"> 
        <value>@(context.RequestId)</value>
      </set-header>
    </inbound>
    ```
    
- Remove sensitive headers - clean up incoming requests to protect credentials or session data.
    
    ```xml
    <inbound>
      <base />
      <set-header name="Cookie" exists-action="delete" />
      <set-header name="Referer" exists-action="delete" />
    </inbound>
    ```

    > [!IMPORTANT]
    > Avoid deleting authentication headers (such as `Authorization`) unless you're sure the MCP server doesn't require them.

- Simple routing control - if you have different backends (like ones for different geographies), you can route requests based on a header.
    
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

After you configure your MCP server, you can test it in the Microsoft Foundry portal.

## Verify governance is working

Use these checks to confirm traffic is routed through AI Gateway and policies are applied.

1. In Foundry Tools, open your MCP tool configuration.
1. Confirm the configured tool endpoint points to the AI Gateway (not directly to your MCP server).
1. In the Azure portal, open the API Management instance connected to your Foundry resource.
1. Review metrics and logs to confirm requests appear when your agent calls the tool.

## Security considerations

- Treat API keys, tokens, and OAuth client secrets as secrets. Store shared credentials in a project connection when possible, and limit who can access the project.
- Apply the least-privilege principle for managed identity and Microsoft Entra access.
- Review which headers you forward to backends. Remove only headers you don't need, and avoid stripping required authentication headers.

For MCP authentication options, see [Authentication support for the Model Context Protocol (MCP) tool (preview)](../mcp-authentication.md).

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| The tool still calls the MCP server directly. | The tool was created before AI Gateway was connected, or the tool isn't eligible for gateway routing (for example, it uses managed OAuth). | Recreate the tool after AI Gateway is connected, and confirm the tool is an MCP tool that doesn't use managed OAuth. |
| Tool calls fail after you add API Management policies. | A policy blocks traffic (rate limits, IP filtering) or modifies headers required by the MCP server. | Temporarily disable policies to isolate the cause, then refine the policy conditions. Avoid deleting required authentication headers. |
| OAuth sign-in fails for custom OAuth identity passthrough. | Redirect URL or OAuth app configuration is incorrect. | Re-check the redirect URL in your OAuth app registration and confirm required OAuth settings. For options and terminology, see [MCP server authentication](../mcp-authentication.md). |
| You don't see request traces in AI Gateway. | AI Gateway doesn't log tool traces. | Use API Management logging/metrics for gateway traffic, and use your MCP server logs for tool-level details. |

## Limitations

- Only MCP tools are supported today. Foundry-based tools such as SharePoint, code-first MCP tools, tools with managed OAuth, or OpenAPI tools are not supported.
- Tool traces are not logged by AI Gateway.
- Gateway routing is only applied at tool creation. Existing tools aren't automatically mediated with AI Gateway.
- Application of API management policies is only supported in the Azure portal, not the Microsoft Foundry portal.

For a broader list of Agent Service tool support when working with gateways, see [Bring your own AI gateway to Azure AI Agent Service (preview)](../ai-gateway.md).

## Next steps

> [!div class="nextstepaction"]
> [Connect to Model Context Protocol servers](model-context-protocol.md)

> [!div class="nextstepaction"]
> [Authentication support for the Model Context Protocol (MCP) tool (preview)](../mcp-authentication.md)

> [!div class="nextstepaction"]
> [Discover and manage tools in the Foundry tool catalog (preview)](../../concepts/tool-catalog.md)