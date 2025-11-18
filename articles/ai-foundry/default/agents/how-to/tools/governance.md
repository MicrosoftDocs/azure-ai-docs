---
title: 'Tools governance'
titleSuffix: Microsoft Foundry
description: Learn how to use AI Gateway to provide a governed entrypoint for authentication policies.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/14/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Tools governance with AI Gateway (preview)

AI Gateway in Microsoft Foundry provides a single, governed entry point for tools added to Azure AI Foundry projects. After a gateway is connected, all new MCP tools route through a secure gateway endpoint where authentication, policies, and usage limits are consistently enforced.

> [!NOTE]
> Only new MCP tools created in the Microsoft Foundry portal that don't use managed OAuth are routed through AI Gateway.

## Key benefits

- Secure routing for all new tools using a gateway endpoint
- Consistent access control and authentication enforcement
- Unified policies for throttling, IP restrictions, and routing
- Centralized observability for tool calls (such as logs and metrics)
- Seamless reuse of tools through public and private catalogs

## Prerequisites

To enable governance for tools using AI Gateway in Microsoft Foundry:

- AI Gateway must be connected to the Microsoft Foundry resource
   - Governance is activated at the Microsoft Foundry resource level. All governance functionality depends on this connection.
- The MCP server must support one of the following authentication methods:
   - Managed identity (Microsoft Entra)
   - Key-based (API key or token)
   - Custom OAuth identity passthrough
   - Unauthenticated (if applicable)

## Govern a tool

### Add a tool

To add a tool to be governed, use the Microsoft Foundry portal. You can add a tool using the tool catalog by selecting **Tools** > **Catalog**, then choosing an MCP server to add: 

You can also add a custom tool in the Microsoft Foundry by selecting **Build** > **Tools** > **Custom** > **Model Context Protocol**. Then paste your MCP server endpoint, and select an authentication type:

### Confirm routing

Ensure the following information is correct for your MCP server:
- Remote MCP server endpoint (AI gateway endpoint)
- Redirect URL (if using custom OAuth identity passthrough)
- Authentication method (key-based auth, OAuth identity passthrough)
- Which agents are using this tool

### Apply Policies

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
      <set-header name="Authorization" exists-action="delete" />
    </inbound>
    ```

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

## Limitations

- Only MCP tools are supported today. Foundry-based tools such as SharePoint, code-first MCP tools, tools with managed OAuth, or OpenAPI tools are not supported.
- Tool traces are not logged by AI Gateway.
- Gateway routing is only applied at tool creation. Existing tools aren't automatically mediated with AI Gateway.
- Application of API management policies is only supported in the Azure portal, not the Microsoft Foundry portal.