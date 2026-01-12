---
title: Use Foundry Agent Service with OpenAPI Tools
titleSuffix: Microsoft Foundry
description: Learn how to configure Azure AI Agents with OpenAPI tools for API integration. Connect external APIs with authentication options including managed identity and API keys.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/22/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# How to use Foundry Agent Service with OpenAPI Specified Tools

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new OpenAPI tool documentation](../../../default/agents/how-to/tools/openapi.md?view=foundry&preserve-view=true).

You can now connect your Azure AI Agent to an external API by using an OpenAPI 3.0 specified tool, enabling scalable interoperability with various applications. By using managed identities (Microsoft Entra ID) for authentication, you can securely enable your custom tools to authenticate access and connections. This approach is ideal for integrating with existing infrastructure or web services.

OpenAPI Specified tool improves your function calling experience by providing standardized, automated, and scalable API integrations that enhance the capabilities and efficiency of your agent. [OpenAPI specifications](https://spec.openapis.org/oas/latest.html) provide a formal standard for describing HTTP APIs. This standard helps people understand how an API works, how a sequence of APIs works together, and it supports generating client code, creating tests, applying design standards, and more. Currently, the OpenAPI 3.0 specified tools support three authentication types: `anonymous`, `API key`, and `managed identity`.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|   ✔️   | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

1. Ensure you complete the prerequisites and setup steps in the [quickstart](../../quickstart.md).
1. Check the OpenAPI spec for the following requirements:
    1. Although not required by the OpenAPI spec, each function must have an `operationId` to work with the OpenAPI tool.
    1. The `operationId` should only contain letters, `-`, and `_`. You can modify it to meet this requirement. Use a descriptive name to help models efficiently decide which function to use.

## Authenticate with API key

By using API key authentication, you can authenticate your OpenAPI spec through different methods, such as an API key or Bearer token. Each OpenAPI spec supports only one API key security schema. If you need multiple security schemas, create multiple OpenAPI spec tools.

1. Update your OpenAPI spec security schemas. It has a `securitySchemes` section and one scheme of type `apiKey`. For example:

   ```json
    "securitySchemes": {
        "apiKeyHeader": {
                "type": "apiKey",
                "name": "x-api-key",
                "in": "header"
            }
    }
   ```

   You usually only need to update the `name` field, which corresponds to the name of `key` in the connection. If the security schemes include multiple schemes, keep only one of them.

1. Update your OpenAPI spec to include a `security` section:

   ```json
   "security": [
        {  
        "apiKeyHeader": []  
        }  
    ]
   ```

1. Remove any parameter in the OpenAPI spec that needs API key, because the API key is stored and passed through a connection, as described later in this article.
1. Create a `custom keys` connection to store your API key.

    1. Go to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) and select **Management center** from the left navigation pane.

       :::image type="content" source="../../media\tools\bing\project-settings-button.png" alt-text="A screenshot of the settings button for an AI project." lightbox="../../media\tools\bing\project-settings-button.png":::

    1. Select **Connected resources** under the AI project in the left navigation pane.
    1. Select **+ new connection** in the settings page.

       >[!NOTE]
       > If you regenerate the API key at a later date, you need to update the connection with the new key.
        
       :::image type="content" source="../../media\tools\bing\project-connections.png" alt-text="A screenshot of the connections screen for the AI project." lightbox="../../media\tools\bing\project-connections.png":::

   1. Select **custom keys** in **other resource types**.
    
      :::image type="content" source="../../media\tools\bing\api-key-connection.png" alt-text="A screenshot of the custom keys selection for the AI project." lightbox="../../media\tools\bing\api-key-connection.png":::
    
   1. Enter the following information
      - key: `name` field of your security scheme. In this example, it should be `x-api-key`

        ```json
        "securitySchemes": {
            "apiKeyHeader": {
                    "type": "apiKey",
                    "name": "x-api-key",
                    "in": "header"
                }
        }
        ```

      - value: YOUR_API_KEY
      - Connection name: YOUR_CONNECTION_NAME (You use this connection name in the sample code below.)
      - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.

1. After you create a connection, use it through the SDK or REST API. Use the tabs at the top of this article to see code examples.

## Authenticate with managed identity (Microsoft Entra ID)

[Microsoft Entra ID](/entra/fundamentals/whatis) is a cloud-based identity and access management service that your employees can use to access external resources. By using Microsoft Entra ID, you can add extra security when you authenticate your APIs without needing to use API keys. After you set up managed identity authentication, the Foundry Tool your agent uses handles the authentication.

When configuring managed identity authentication, you need to provide an **Audience** value. The audience is the OAuth2 resource identifier (also called scope or application ID URI) that identifies which API or service the managed identity can access.

**Common audience values:**

- Foundry Tools (formerly Azure AI services or Cognitive Services): `https://cognitiveservices.azure.com/`
- Azure Resource Manager APIs: `https://management.azure.com/`
- Microsoft Graph: `https://graph.microsoft.com/`
- Custom APIs registered in Microsoft Entra ID: Use the **Application ID URI** found in the API's app registration

To set up authentication by using Managed Identity:

1. Make sure your Foundry resource has a system assigned managed identity enabled.

    :::image type="content" source="../../media\tools\managed-identity-portal.png" alt-text="A screenshot showing the managed identity selector in the Azure portal." lightbox="../../media\tools\managed-identity-portal.png":::

1. Create a resource for the service you want to connect to through OpenAPI spec.
1. Assign the proper access to the resource.
    1. Select **Access Control** for your resource.
    1. Select **Add** and then **add role assignment** at the top of the screen.

        :::image type="content" source="../../media\tools\role-assignment-portal.png" alt-text="A screenshot showing the role assignment selector in the Azure portal." lightbox="../../media\tools\role-assignment-portal.png":::
        
    1. Select the proper role assignment needed. Usually, it requires at least the *READER* role. Then select **Next**.
    1. Select **Managed identity** and then select **select members**.
    1. In the managed identity dropdown menu, search for **Foundry Tools** and then select the Foundry Tool of your agent.
    1. Select **Finish**.

1. After you complete the setup, you can use the tool through the Foundry portal, SDK, or REST API. Use the tabs at the top of this article to see code samples.
