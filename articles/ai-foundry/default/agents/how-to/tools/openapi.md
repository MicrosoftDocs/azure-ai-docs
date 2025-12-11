---
title: How to use Microsoft Foundry Agent Service with OpenAPI Specified Tools
titleSuffix: Microsoft Foundry
description: Learn how to connect OpenAPI tools to Microsoft Foundry agents using authentication methods like API keys and managed identities. Integrate your APIs with AI agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/05/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-openapi-function-new
---

# Connect to OpenAPI Specification

You can now connect your Microsoft Foundry Agent Service to an external API by using an OpenAPI 3.0 specified tool. This connection enables scalable interoperability with various applications. You can enable your custom tools to authenticate access and connections with managed identities (Microsoft Entra ID) for added security. This feature is ideal for integrating with existing infrastructure or web services.

OpenAPI Specified tool improves your function calling experience by providing standardized, automated, and scalable API integrations that enhance the capabilities and efficiency of your agent. [OpenAPI specifications](https://spec.openapis.org/oas/latest.html) provide a formal standard for describing HTTP APIs. This standard allows people to understand how an API works, how a sequence of APIs works together, generate client code, create tests, apply design standards, and more. Currently, we support three authentication types with the OpenAPI 3.0 specified tools: `anonymous`, `API key`, `managed identity`.

### Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | 	Java SDK |REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|   ✔️   | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

1. Check the OpenAPI spec for the following requirements:
   1. Although the OpenAPI spec doesn't require it, you need an `operationId` for each function to use with the OpenAPI tool.
   1. `operationId` should only contain letters, `-`, and `_`. You can modify it to meet the requirement. Use a descriptive name to help models efficiently decide which function to use.

## Code example

:::zone pivot="python"
> [!NOTE]
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
> - If you use API key for authentication, your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`

```python
import os
import jsonref
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
)

load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    weather_asset_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/weather_openapi.json"))

    with open(weather_asset_file_path, "r") as f:
        openapi_weather = jsonref.loads(f.read())


    # Initialize agent OpenApi tool using the read in OpenAPI spec
    weather_tool = {
        "type": "openapi",
        "openapi":{
            "name": "weather",
            "spec": openapi_weather,
            "auth": {
                "type": "anonymous"
            },
        }
    }

    # If you want to use key-based authentication
    openapi_key_auth_tool={
        "type": "openapi",
        "openapi":{
            "name": "TOOL_NAME",
            "spec": SPEC_NAME,
            "auth": {
                  "type": "project_connection",
                  "security_scheme": {
                      "project_connection_id": "/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}"              
                  }              
            },
        }
    }

    # If you want to use Managed Identity authentication
    openapi_mi_auth_tool={
      "type": "openapi",
      "openapi":{
          "name": "TOOL_NAME",
          "description": "",
          "spec": SPEC_NAME,
          "auth": {
              "type": "managed_identity",
              "security_scheme": {
                  "audience": ""  #audience to the service, such as https://ai.azure.com     
              }              
              },
      }
  }

    agent = project_client.agents.create_version(
        agent_name="MyAgent23",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[weather_tool],
        ),
        description="You are a helpful assistant.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    response = openai_client.responses.create(
        input="What's the weather in Seattle?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response created: {response.output_text}")

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"

For C# usage, see the [Sample of using Agents with OpenAPI tool in Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample20_OpenAPI.md) and [Sample of using Agents with OpenAPI tool in Azure.AI.Projects.OpenAI on Web service, requiring authentication](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample21_OpenAPI_Connection.md) examples in the Azure SDK for .NET repository on GitHub.

:::zone-end

## Authenticating with API key

With API key authentication, you can authenticate your OpenAPI spec by using various methods such as an API key or Bearer token. You can only use one API key security schema per OpenAPI spec. If you need multiple security schemas, create multiple OpenAPI spec tools.

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

1. Remove any parameter in the OpenAPI spec that needs API key, because API key is stored and passed through a connection, as described later in this article.
1. Create a connection to store your API key.
   1. Go to the [Microsoft Foundry portal](https://ai.azure.com/nextgen?cid=learnDocs) and select the AI Project. Go to build -> agents. 
   1. Select **OpenAPI** in tools -> custom. 

        >[!NOTE]
        > If you regenerate the API key at a later date, you need to update the connection with the new key.
    
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
1. Once you create a connection, you can use it through the SDK or REST API. Use the tabs at the top of this article to see code examples.

## Authenticating with managed identity (Microsoft Entra ID)

[Microsoft Entra ID](/entra/fundamentals/whatis) is a cloud-based identity and access management service that your employees can use to access external resources. Microsoft Entra ID allows you to authenticate your APIs with extra security without the need to pass in API keys. When you set up managed identity authentication, it authenticates through the Foundry Tool your agent uses. 

To set up authentication with Managed Identity:

1. Make sure your Foundry resource has system assigned managed identity enabled.

   :::image type="content" source="../../../../agents/media/tools/managed-identity-portal.png" alt-text="A screenshot showing the managed identity selector in the Azure portal." lightbox="../../../../agents/media/tools/managed-identity-portal.png":::

1. Create a resource for the service you want to connect to through OpenAPI spec.
1. Assign proper access to the resource.
   1. Select **Access Control** for your resource.
   1. Select **Add** and then **add role assignment** at the top of the screen.

      :::image type="content" source="../../../../agents/media/tools/role-assignment-portal.png" alt-text="A screenshot showing the role assignment selector in the Azure portal." lightbox="../../../../agents/media/tools/role-assignment-portal.png":::
        
   1. Select the proper role assignment needed, usually it requires at least the *READER* role. Then select **Next**.
   1. Select **Managed identity** and then select **select members**.
   1. In the managed identity dropdown menu, search for **Foundry Account** and then select the Foundry account of your agent.
   1. Select **Finish**.
1. When you finish the setup, you can continue by using the tool through the Foundry portal, SDK, or REST API. Use the tabs at the top of this article to see code samples.
