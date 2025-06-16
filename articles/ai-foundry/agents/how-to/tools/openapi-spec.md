---
title: 'How to use Azure AI Foundry Agent Service with OpenAPI Specified Tools'
titleSuffix: Azure AI Foundry
description: Learn how to use Azure AI Agents with OpenAPI Specified Tools.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 03/12/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---
# How to use Azure AI Foundry Agent Service with OpenAPI Specified Tools

You can now connect your Azure AI Agent to an external API using an OpenAPI 3.0 specified tool, 
allowing for scalable interoperability with various applications. Enable your custom tools 
to authenticate access and connections with managed identities (Microsoft Entra ID) for 
added security, making it ideal for integrating with existing infrastructure or web services.

OpenAPI Specified tool improves your function calling experience by providing standardized, 
automated, and scalable API integrations that enhance the capabilities and efficiency of your agent. 
[OpenAPI specifications](https://spec.openapis.org/oas/latest.html) provide a formal standard for 
describing HTTP APIs. This allows people to understand how an API works, how a sequence of APIs works together, generate client code, create tests, apply design standards, and more. Currently, we support three authentication types with the OpenAPI 3.0 specified tools: `anonymous`, `API key`, `managed identity`.

### Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|
|   ✔️   | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites
1. Ensure you've completed the prerequisites and setup steps in the [quickstart](../../quickstart.md).

1. Check the OpenAPI spec for the following requirements:
    1. Although not required by the OpenAPI spec, `operationId` is required for each function to be used with the OpenAPI tool.
    1. `operationId` should only contain letters, `-` and `_`. You can modify it to meet the requirement. We recommend using descriptive name to help models efficiently decide which function to use.

## Authenticating with API Key

With API key authentication, you can authenticate your OpenAPI spec using various methods such as an API key or Bearer token. Only one API key security schema is supported per OpenAPI spec. If you need multiple security schemas, create multiple OpenAPI spec tools.

1. Update your OpenAPI spec security schemas. it has a `securitySchemes` section and one scheme of type `apiKey`. For example:

   ```json
    "securitySchemes": {
        "apiKeyHeader": {
                "type": "apiKey",
                "name": "x-api-key",
                "in": "header"
            }
    }
   ```

   You usually only need to update the `name` field, which corresponds to the name of `key` in the connection. If the security schemes include multiple schemes, we recommend keeping only one of them.

1. Update your OpenAPI spec to include a `security` section:
   ```json
   "security": [
        {  
        "apiKeyHeader": []  
        }  
    ]
   ```

1. Remove any parameter in the OpenAPI spec that needs API key, because API key will be stored and passed through a connection, as described later in this article.

1. Create a `custom keys` connection to store your API key.

    1. Go to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and select the AI Project. Click **connected resources**.
    :::image type="content" source="../../media\tools\bing\project-settings-button.png" alt-text="A screenshot of the settings button for an AI project." lightbox="../../media\tools\bing\project-settings-button.png":::

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
      - Connection name: YOUR_CONNECTION_NAME (You will use this connection name in the sample code below.)
      - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.

1. Once you have created a connection, you can use it through the SDK or REST API. Use the tabs at the top of this article to see code examples.

## Authenticating with managed identity (Microsoft Entra ID)

[Microsoft Entra ID](/entra/fundamentals/whatis) is a cloud-based identity and access management service that your employees can use to access external resources. Microsoft Entra ID allows you to authenticate your APIs with additional security without the need to pass in API keys. Once you have set up managed identity authentication, it will authenticate through the Azure AI Service your agent is using. 

To set up authenticating with Managed Identity:

1. Enable the Azure AI Service of your agent has `system assigned managed identity` enabled.

    :::image type="content" source="../../media\tools\managed-identity-portal.png" alt-text="A screenshot showing the managed identity selector in the Azure portal." lightbox="../../media\tools\managed-identity-portal.png":::

1. Create a resource of the service you want to connect to through OpenAPI spec.

1. Assign proper access to the resource.
    1. Click **Access Control** for your resource
       
    1. Click **Add** and then **add role assignment** at the top of the screen.

        :::image type="content" source="../../media\tools\role-assignment-portal.png" alt-text="A screenshot showing the role assignment selector in the Azure portal." lightbox="../../media\tools\role-assignment-portal.png":::
        
    1. Select the proper role assignment needed, usually it will require at least *READER* role. Then click **Next**.

    1. Select **Managed identity** and then click **select members**.

    1. In the managed identity dropdown menu, search for **Azure AI services** and then select the AI Service of your agent.

    1. Click **Finish**.

1. Once the setup is done, you can continue by using the tool through the Foundry Portal, SDK, or REST API. Use the tabs at the top of this article to see code samples.
