---
title: Connect OpenAPI tools to Microsoft Foundry agents
titleSuffix: Microsoft Foundry
description: Connect OpenAPI 3.0 tools to Microsoft Foundry agents using API key, managed identity, or anonymous authentication. Integrate external APIs with your AI agents today.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/12/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-openapi-function-new
---

# Connect agents to OpenAPI tools

Connect your Microsoft Foundry agents to external APIs using OpenAPI 3.0 specifications. Agents that connect to OpenAPI tools can call external services, retrieve real-time data, and extend their capabilities beyond built-in functions.

[OpenAPI specifications](https://spec.openapis.org/oas/latest.html) define a standard way to describe HTTP APIs so you can integrate existing services with your agents. Microsoft Foundry supports three authentication methods: `anonymous`, `API key`, and `managed identity`. For help choosing an authentication method, see [Choose an authentication method](#choose-an-authentication-method).

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription with the right permissions.
- Azure RBAC role: Contributor or Owner on the Foundry project.
- A Foundry project created with an endpoint configured.
- An AI model deployed in your project.
- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- SDK installed for your preferred language:
  - Python: `azure-ai-projects` (latest prerelease version)
  - C#: `Azure.AI.Projects.OpenAI`
  - TypeScript/JavaScript: `@azure/ai-projects`

### Environment variables

| Variable | Description |
| --- | --- |
| `AZURE_AI_PROJECT_ENDPOINT` | Your Foundry project endpoint URL (not the external OpenAPI service endpoint). |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Your deployed model name. |
| `OPENAPI_PROJECT_CONNECTION_NAME` | (For API key auth) Your project connection name for the OpenAPI service. |

- OpenAPI 3.0 specification file that meets these requirements:
  - Each function must have an `operationId` (required for the OpenAPI tool).
  - `operationId` should only contain letters, `-`, and `_`.
  - Use descriptive names to help models efficiently decide which function to use.
  - Supported content type: "application/json", "application/json-patch+json"
- For managed identity authentication: Reader role or higher on target service resources.
- For API key/token authentication: a project connection configured with your API key or token. See [Add a new connection to your project](../../../../how-to/connections-add.md).

> [!NOTE]
> The `AZURE_AI_PROJECT_ENDPOINT` value refers to your Microsoft Foundry project endpoint, not the external OpenAPI service endpoint. You can find this endpoint in the Microsoft Foundry portal under your project’s Overview page. This endpoint is required to authenticate the agent service and is separate from any OpenAPI endpoints defined in your specification file.

## Understand limitations

- Your OpenAPI spec must include `operationId` for each operation, and `operationId` can include only letters, `-`, and `_`.
- Supported content types: `application/json`, `application/json-patch+json`.
- For API key authentication, use one API key security scheme per OpenAPI tool. If you need multiple security schemes, create multiple OpenAPI tools.

## Code example

> [!NOTE]
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for details.
> - If you use API key for authentication, your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

> [!IMPORTANT]
> **For API key authentication to work**, your OpenAPI specification file must include:
> 1. A `securitySchemes` section with your API key configuration, such as the header name and parameter name.
> 1. A `security` section that references the security scheme.
> 1. A project connection configured with the matching key name and value.
> 
> Without these configurations, the API key isn't included in requests. For detailed setup instructions, see the [Authenticate with API key](#authenticate-with-api-key) section.
>
> You can also use token-based authentication (for example, a Bearer token) by storing the token in a project connection. For Bearer token auth, create a **Custom keys** connection with key set to `Authorization` and value set to `Bearer <token>` (replace `<token>` with your actual token). The word `Bearer` followed by a space must be included in the value. For details, see [Set up a Bearer token connection](#set-up-a-bearer-token-connection).

:::zone pivot="python"
### Quick verification

First, verify your environment is configured correctly:

```python
# Verify authentication and project connection
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with DefaultAzureCredential() as credential, \
     AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
    print(f"Successfully connected to project")
```

If this command runs without errors, you're ready to create an agent with OpenAPI tools.

### Complete example

```python
# Import required libraries
import os
import jsonref
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

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
    # IMPORTANT: Your OpenAPI spec must include securitySchemes and security sections
    # Example spec structure for API key auth:
    # {
    #   "components": {
    #     "securitySchemes": {
    #       "apiKeyHeader": {
    #         "type": "apiKey",
    #         "name": "x-api-key",  # This must match the key name in your project connection
    #         "in": "header"
    #       }
    #     }
    #   },
    #   "security": [{"apiKeyHeader": []}]
    # }
    #
    # For Bearer token authentication, use this securitySchemes structure instead:
    # {
    #   "components": {
    #     "securitySchemes": {
    #       "bearerAuth": {
    #         "type": "apiKey",
    #         "name": "Authorization",
    #         "in": "header"
    #       }
    #     }
    #   },
    #   "security": [{"bearerAuth": []}]
    # }
    # Then set connection key = "Authorization" and value = "Bearer <token>"
    # The word "Bearer" followed by a space MUST be included in the value.
    
    openapi_connection = project_client.connections.get(os.environ["OPENAPI_PROJECT_CONNECTION_NAME"])
    connection_id = openapi_connection.id
    print(f"OpenAPI connection ID: {connection_id}")

    openapi_key_auth_tool={
        "type": "openapi",
        "openapi":{
            "name": "TOOL_NAME",
            "spec": SPEC_NAME,  # Must include securitySchemes and security sections
            "auth": {
                  "type": "project_connection",
                  "security_scheme": {
                      "project_connection_id": connection_id              
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

### What this code does

This example creates an agent with an OpenAPI tool that calls the wttr.in weather API using anonymous authentication. When you run the code:

1. It loads the weather OpenAPI specification from a local JSON file.
1. Creates an agent with the weather tool configured for anonymous access.
1. Sends a query asking about Seattle's weather.
1. The agent uses the OpenAPI tool to call the weather API and returns formatted results.
1. Cleans up by deleting the agent version.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- Local file: `weather_openapi.json` (OpenAPI specification)

### Expected output

```console
Agent created (id: asst_abc123, name: MyAgent23, version: 1)
Response created: The weather in Seattle is currently cloudy with a temperature of 52°F (11°C)...

Cleaning up...
Agent deleted
```

### Common errors

- `FileNotFoundError`: OpenAPI specification file not found at specified path
- `KeyError`: Missing required environment variables
- `AuthenticationError`: Invalid credentials or insufficient permissions, or missing `securitySchemes` in OpenAPI spec for API key authentication
- Invalid `operationId` format in OpenAPI spec causes tool registration failure
- **API key not injected**: Verify your OpenAPI spec includes both `securitySchemes` and `security` sections, and that the key name matches your project connection

:::zone-end

:::zone pivot="csharp"
## Sample of using Agents with OpenAPI tool

This example demonstrates how to use services described by an [OpenAPI specification](https://spec.openapis.org/oas/latest.html) by using an agent. It uses the [wttr.in](https://wttr.in/:help) service to get weather and its specification file [weather_openapi.json](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/weather_openapi.json). This example uses synchronous methods of the Azure AI Projects client library. For an example that uses asynchronous methods, see the [sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample21_OpenAPI.md) in the Azure SDK for .NET repository on GitHub.

```csharp
class OpenAPIDemo
{
    // Utility method to get the OpenAPI specification file from the Assets folder.
    private static string GetFile([CallerFilePath] string pth = "")
    {
        var dirName = Path.GetDirectoryName(pth) ?? "";
        return Path.Combine(dirName, "Assets", "weather_openapi.json");
    }

    public static void Main()
    {
        // First, create an agent client and read the environment variables, which will be used in the next steps.
        var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
        var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
        AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

        // Create an Agent with `OpenAPIAgentTool` and anonymous authentication.
        string filePath = GetFile();
        OpenAPIFunctionDefinition toolDefinition = new(
            name: "get_weather",
            spec: BinaryData.FromBytes(BinaryData.FromBytes(File.ReadAllBytes(filePath))),
            auth: new OpenAPIAnonymousAuthenticationDetails()
        );
        toolDefinition.Description = "Retrieve weather information for a location.";
        OpenAPITool openapiTool = new(toolDefinition);

        // Create the agent definition and the agent version.
        PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
        {
            Instructions = "You are a helpful assistant.",
            Tools = { openapiTool }
        };
        AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition));

        // Create a response object and ask the question about the weather in Seattle, WA.
        ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
        ResponseResult response = responseClient.CreateResponse(
                userInputText: "Use the OpenAPI tool to print out, what is the weather in Seattle, WA today."
            );
        Console.WriteLine(response.GetOutputText());

        // Finally, delete all the resources created in this sample.
        projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
    }
}
```

### What this code does

This C# example creates an agent with an OpenAPI tool that retrieves weather information from wttr.in by using anonymous authentication. When you run the code:

1. It reads the weather OpenAPI specification from a local JSON file.
1. Creates an agent with the weather tool configured.
1. Sends a request asking about Seattle's weather using the OpenAPI tool.
1. The agent calls the weather API and returns the results.
1. Cleans up by deleting the agent.

### Required inputs

- Environment variables: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
- Local file: `Assets/weather_openapi.json` (OpenAPI specification)

### Expected output

```console
The weather in Seattle, WA today is cloudy with temperatures around 52°F...
```

### Common errors

- `FileNotFoundException`: OpenAPI specification file not found in Assets folder
- `ArgumentNullException`: Missing required environment variables
- `UnauthorizedAccessException`: Invalid credentials or insufficient RBAC permissions
- **API key not injected**: Verify your OpenAPI spec includes both `securitySchemes` (in `components`) and `security` sections with matching scheme names

## Sample of using Agents with OpenAPI tool on Web service, requiring authentication

In this example, you use services with an OpenAPI specification by using the agent in a scenario that requires authentication. You use the TripAdvisor specification.

The TripAdvisor service requires key-based authentication. To create a connection in the Azure portal, open Microsoft Foundry and, at the left panel select **Management center** and then select **Connected resources**. Finally, create new connection of **Custom keys** type. Name it `tripadvisor` and add a key value pair. Add key named `key` and enter a value with your TripAdvisor key.

```csharp
class OpenAPIConnectedDemo
{
    // Utility method to get the OpenAPI specification file from the Assets folder.
    private static string GetFile([CallerFilePath] string pth = "")
    {
        var dirName = Path.GetDirectoryName(pth) ?? "";
        return Path.Combine(dirName, "Assets", "tripadvisor_openapi.json");
    }

    public static void Main()
    {
        // First, we need to create agent client and read the environment variables, which will be used in the next steps.
        var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
        var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
        AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

        // Create an Agent with `OpenAPIAgentTool` and authentication by project connection security scheme.
        string filePath = GetFile();
        AIProjectConnection tripadvisorConnection = projectClient.Connections.GetConnection("tripadvisor");
        OpenAPIFunctionDefinition toolDefinition = new(
            name: "tripadvisor",
            spec: BinaryData.FromBytes(BinaryData.FromBytes(File.ReadAllBytes(filePath))),
            auth: new OpenAPIProjectConnectionAuthenticationDetails(new OpenAPIProjectConnectionSecurityScheme(
                projectConnectionId: tripadvisorConnection.Id
            ))
        );
        toolDefinition.Description = "Trip Advisor API to get travel information.";
        OpenAPITool openapiTool = new(toolDefinition);

        // Create the agent definition and the agent version.
        PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
        {
            Instructions = "You are a helpful assistant.",
            Tools = { openapiTool }
        };
        AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition));

        // Create a response object and ask the question about the hotels in France.
        // Test the Web service access before you run production scenarios.
        // It can be done by setting:
        // ToolChoice = ResponseToolChoice.CreateRequiredChoice()`
        // in the ResponseCreationOptions. This setting will
        // force Agent to use tool and will trigger the error if it is not accessible.
        ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
        CreateResponseOptions responseOptions = new()
        {
            ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
            InputItems =
            {
                ResponseItem.CreateUserMessageItem("Recommend me 5 top hotels in paris, France."),
            }
        };
        ResponseResult response = responseClient.CreateResponse(
            options: responseOptions
        );
        Console.WriteLine(response.GetOutputText());

        // Finally, delete all the resources we have created in this sample.
        projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
    }
}
```

### What this code does

This C# example demonstrates using an OpenAPI tool with API key authentication through a project connection. When you run the code:

1. It loads the TripAdvisor OpenAPI specification from a local file.
1. Retrieves the `tripadvisor` project connection containing your API key.
1. Creates an agent with the TripAdvisor tool configured to use the connection for authentication.
1. Sends a request for hotel recommendations in Paris.
1. The agent calls the TripAdvisor API using your stored API key and returns results.
1. Cleans up by deleting the agent.

### Required inputs

- Environment variables: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
- Local file: `Assets/tripadvisor_openapi.json`
- Project connection: `tripadvisor` with valid API key configured

### Expected output

```console
Here are 5 top hotels in Paris, France:
1. Hotel Name - Rating: 4.5/5, Location: ...
2. Hotel Name - Rating: 4.4/5, Location: ...
...
```

### Common errors

- `ConnectionNotFoundException`: No project connection named `tripadvisor` found.
- `AuthenticationException`: Invalid API key in project connection, or missing/incorrect `securitySchemes` configuration in OpenAPI spec.
- Tool not used: Verify `ToolChoice = ResponseToolChoice.CreateRequiredChoice()` forces tool usage.
- **API key not passed to API**: Ensure the OpenAPI spec has proper `securitySchemes` and `security` sections configured.

:::zone-end

:::zone pivot="rest"
The following examples show how to call an OpenAPI tool by using the REST API.

### Anonymous authentication

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --header "Authorization: Bearer $AGENT_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
    "input": "Use the OpenAPI tool to get the weather in Seattle, WA today.",
    "tools": [
      {
        "type": "openapi",
        "openapi": {
          "name": "weather",
          "description": "Tool to get weather data",
          "auth": { "type": "anonymous" },
          "spec": {
            "openapi": "3.1.0",
            "info": {
              "title": "get weather data",
              "description": "Retrieves current weather data for a location.",
              "version": "v1.0.0"
            },
            "servers": [{ "url": "https://wttr.in" }],
            "paths": {
              "/{location}": {
                "get": {
                  "description": "Get weather information for a specific location",
                  "operationId": "GetCurrentWeather",
                  "parameters": [
                    {
                      "name": "location",
                      "in": "path",
                      "description": "City or location to retrieve the weather for",
                      "required": true,
                      "schema": { "type": "string" }
                    },
                    {
                      "name": "format",
                      "in": "query",
                      "description": "Format in which to return data. Always use 3.",
                      "required": true,
                      "schema": { "type": "integer", "default": 3 }
                    }
                  ],
                  "responses": {
                    "200": {
                      "description": "Successful response",
                      "content": {
                        "text/plain": {
                          "schema": { "type": "string" }
                        }
                      }
                    },
                    "404": { "description": "Location not found" }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }'
```

### API key authentication (project connection)

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --header "Authorization: Bearer $AGENT_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
    "input": "Use the OpenAPI tool to get the weather in Seattle, WA today.",
    "tools": [
      {
        "type": "openapi",
        "openapi": {
          "name": "weather",
          "description": "Tool to get weather data",
          "auth": {
            "type": "project_connection",
            "security_scheme": {
              "project_connection_id": "'$WEATHER_APP_PROJECT_CONNECTION_ID'"
            }
          },
          "spec": {
            "openapi": "3.1.0",
            "info": {
              "title": "get weather data",
              "description": "Retrieves current weather data for a location.",
              "version": "v1.0.0"
            },
            "servers": [{ "url": "https://wttr.in" }],
            "paths": {
              "/{location}": {
                "get": {
                  "description": "Get weather information for a specific location",
                  "operationId": "GetCurrentWeather",
                  "parameters": [
                    {
                      "name": "location",
                      "in": "path",
                      "description": "City or location to retrieve the weather for",
                      "required": true,
                      "schema": { "type": "string" }
                    },
                    {
                      "name": "format",
                      "in": "query",
                      "description": "Format in which to return data. Always use 3.",
                      "required": true,
                      "schema": { "type": "integer", "default": 3 }
                    }
                  ],
                  "responses": {
                    "200": {
                      "description": "Successful response",
                      "content": {
                        "text/plain": {
                          "schema": { "type": "string" }
                        }
                      }
                    },
                    "404": { "description": "Location not found" }
                  }
                }
              }
            },
            "components": {
              "securitySchemes": {
                "apiKeyHeader": {
                  "type": "apiKey",
                  "name": "x-api-key",
                  "in": "header"
                }
              }
            },
            "security": [
              { "apiKeyHeader": [] }
            ]
          }
        }
      }
    ]
  }'
```

### Managed identity authentication

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --header "Authorization: Bearer $AGENT_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
    "input": "Use the OpenAPI tool to get the weather in Seattle, WA today.",
    "tools": [
      {
        "type": "openapi",
        "openapi": {
          "name": "weather",
          "description": "Tool to get weather data",
          "auth": {
            "type": "managed_identity",
            "security_scheme": {
              "audience": "'$MANAGED_IDENTITY_AUDIENCE'"
            }
          },
          "spec": {
            "openapi": "3.1.0",
            "info": {
              "title": "get weather data",
              "description": "Retrieves current weather data for a location.",
              "version": "v1.0.0"
            },
            "servers": [{ "url": "https://wttr.in" }],
            "paths": {
              "/{location}": {
                "get": {
                  "description": "Get weather information for a specific location",
                  "operationId": "GetCurrentWeather",
                  "parameters": [
                    {
                      "name": "location",
                      "in": "path",
                      "description": "City or location to retrieve the weather for",
                      "required": true,
                      "schema": { "type": "string" }
                    },
                    {
                      "name": "format",
                      "in": "query",
                      "description": "Format in which to return data. Always use 3.",
                      "required": true,
                      "schema": { "type": "integer", "default": 3 }
                    }
                  ],
                  "responses": {
                    "200": {
                      "description": "Successful response",
                      "content": {
                        "text/plain": {
                          "schema": { "type": "string" }
                        }
                      }
                    },
                    "404": { "description": "Location not found" }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }'
```

### What this code does

This REST API example shows how to call an OpenAPI tool with different authentication methods. The request:

1. Sends a query to the agent asking about Seattle's weather.
1. Includes the OpenAPI tool definition inline with the weather API specification.
1. Shows three authentication options (anonymous, API key via project connection, managed identity) as commented alternatives.
1. The agent uses the tool to call the weather API and returns formatted results.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `API_VERSION`, `AGENT_TOKEN`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
- For API key auth: `WEATHER_APP_PROJECT_CONNECTION_ID`.
- For managed identity auth: `MANAGED_IDENTITY_AUDIENCE`.
- Inline OpenAPI specification in request body.

### Expected output

```json
{
  "id": "resp_abc123",
  "object": "response",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "text",
          "text": "The weather in Seattle, WA today is cloudy with a temperature of 52°F (11°C)..."
        }
      ]
    }
  ]
}
```

### Common errors

- `401 Unauthorized`: Invalid or missing `AGENT_TOKEN`, or API key not injected because `securitySchemes` and `security` are missing in your OpenAPI spec
- `404 Not Found`: Incorrect endpoint or model deployment name
- `400 Bad Request`: Malformed OpenAPI specification or invalid auth configuration
- **API key not sent with request**: Verify the `components.securitySchemes` section in your OpenAPI spec is properly configured (not empty) and matches your project connection key name
:::zone-end

:::zone pivot="typescript"

## Create an agent with OpenAPI tool capabilities

The following TypeScript code example demonstrates how to create an AI agent with OpenAPI tool capabilities by using the `OpenApiAgentTool` and synchronous Azure AI Projects client. The agent can call external APIs defined by OpenAPI specifications. For a JavaScript version of this example, see the [sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentOpenApi.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import {
  AIProjectClient,
  OpenApiAgentTool,
  OpenApiFunctionDefinition,
  OpenApiAnonymousAuthDetails,
} from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const weatherSpecPath = path.resolve(__dirname, "../assets", "weather_openapi.json");

function loadOpenApiSpec(specPath: string): unknown {
  if (!fs.existsSync(specPath)) {
    throw new Error(`OpenAPI specification not found at: ${specPath}`);
  }

  try {
    const data = fs.readFileSync(specPath, "utf-8");
    return JSON.parse(data);
  } catch (error) {
    throw new Error(`Failed to read or parse OpenAPI specification at ${specPath}: ${error}`);
  }
}

function createWeatherTool(spec: unknown): OpenApiAgentTool {
  const auth: OpenApiAnonymousAuthDetails = { type: "anonymous" };
  const definition: OpenApiFunctionDefinition = {
    name: "get_weather",
    description: "Retrieve weather information for a location using wttr.in",
    spec,
    auth,
  };

  return {
    type: "openapi",
    openapi: definition,
  };
}

export async function main(): Promise<void> {
  console.log("Loading OpenAPI specifications from assets directory...");
  const weatherSpec = loadOpenApiSpec(weatherSpecPath);

  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with OpenAPI tool...");

  const agent = await project.agents.createVersion("MyOpenApiAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a helpful assistant that can call external APIs defined by OpenAPI specs to answer user questions.",
    tools: [createWeatherTool(weatherSpec)],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  console.log("\nSending request to OpenAPI-enabled agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input:
        "What's the weather in Seattle and how should I plan my outfit for the day based on the forecast?",
      stream: true,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
        tool_choice: "required",
      },
    },
  );

  // Process the streaming response
  for await (const event of streamResponse) {
    if (event.type === "response.created") {
      console.log(`Follow-up response created with ID: ${event.response.id}`);
    } else if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    } else if (event.type === "response.output_text.done") {
      console.log("\n\nFollow-up response done!");
    } else if (event.type === "response.output_item.done") {
      const item = event.item as any;
      if (item.type === "message") {
        const content = item.content?.[item.content.length - 1];
        if (content?.type === "output_text" && content.annotations) {
          for (const annotation of content.annotations) {
            if (annotation.type === "url_citation") {
              console.log(
                `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
              );
            }
          }
        }
      } else if (item.type === "tool_call") {
        console.log(`Tool call completed: ${item.name ?? "unknown"}`);
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nOpenAPI agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### What this code does

This TypeScript example creates an agent with an OpenAPI tool for weather data by using anonymous authentication. When you run the code:

1. It loads the weather OpenAPI specification from a local JSON file.
1. Creates an agent with the weather tool configured.
1. Sends a streaming request asking about Seattle's weather and outfit planning.
1. Processes the streaming response and displays deltas as they arrive.
1. It forces tool usage by using `tool_choice: "required"` to ensure the API is called.
1. Cleans up by deleting the agent.

## Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
- Local file: `../assets/weather_openapi.json` (OpenAPI specification)

### Expected output

```console
Loading OpenAPI specifications from assets directory...
Creating agent with OpenAPI tool...
Agent created (id: asst_abc123, name: MyOpenApiAgent, version: 1)

Sending request to OpenAPI-enabled agent with streaming...
Follow-up response created with ID: resp_xyz789
The weather in Seattle is currently...
Tool call completed: get_weather

Follow-up completed!

Cleaning up resources...
Agent deleted

OpenAPI agent sample completed!
```

### Common errors

- `Error: OpenAPI specification not found`: File path incorrect or file missing
- Missing environment variables causes initialization failure
- `AuthenticationError`: Invalid Azure credentials
- **API key not working**: If switching from anonymous to API key auth, ensure your OpenAPI spec has `securitySchemes` and `security` properly configured

## Create an agent that uses OpenAPI tools authenticated with a project connection

The following TypeScript code example demonstrates how to create an AI agent that uses OpenAPI tools authenticated through a project connection. The agent loads the TripAdvisor OpenAPI specification from local assets and can invoke the API through the configured project connection. For a JavaScript version of this example, see the [sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentOpenApiConnectionAuth.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import {
  AIProjectClient,
  OpenApiAgentTool,
  OpenApiFunctionDefinition,
  OpenApiProjectConnectionAuthDetails,
} from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const tripAdvisorProjectConnectionId =
  process.env["TRIPADVISOR_PROJECT_CONNECTION_ID"] || "<tripadvisor project connection id>";
const tripAdvisorSpecPath = path.resolve(__dirname, "../assets", "tripadvisor_openapi.json");

function loadOpenApiSpec(specPath: string): unknown {
  if (!fs.existsSync(specPath)) {
    throw new Error(`OpenAPI specification not found at: ${specPath}`);
  }

  try {
    const data = fs.readFileSync(specPath, "utf-8");
    return JSON.parse(data);
  } catch (error) {
    throw new Error(`Failed to read or parse OpenAPI specification at ${specPath}: ${error}`);
  }
}

function createTripAdvisorTool(spec: unknown): OpenApiAgentTool {
  const auth: OpenApiProjectConnectionAuthDetails = {
    type: "project_connection",
    security_scheme: {
      project_connection_id: tripAdvisorProjectConnectionId,
    },
  };

  const definition: OpenApiFunctionDefinition = {
    name: "get_tripadvisor_location_details",
    description:
      "Fetch TripAdvisor location details, reviews, or photos using the Content API via project connection auth.",
    spec,
    auth,
  };

  return {
    type: "openapi",
    openapi: definition,
  };
}

export async function main(): Promise<void> {
  console.log("Loading TripAdvisor OpenAPI specification from assets directory...");
  const tripAdvisorSpec = loadOpenApiSpec(tripAdvisorSpecPath);

  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with OpenAPI project-connection tool...");

  const agent = await project.agents.createVersion("MyOpenApiConnectionAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a travel assistant that consults the TripAdvisor Content API via project connection to answer user questions about locations.",
    tools: [createTripAdvisorTool(tripAdvisorSpec)],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  console.log("\nSending request to TripAdvisor OpenAPI agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input:
        "Provide a quick overview of the TripAdvisor location 293919 including its name, rating, and review count.",
      stream: true,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
        tool_choice: "required",
      },
    },
  );

  // Process the streaming response
  for await (const event of streamResponse) {
    if (event.type === "response.created") {
      console.log(`Follow-up response created with ID: ${event.response.id}`);
    } else if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    } else if (event.type === "response.output_text.done") {
      console.log("\n\nFollow-up response done!");
    } else if (event.type === "response.output_item.done") {
      const item = event.item as any;
      if (item.type === "message") {
        const content = item.content?.[item.content.length - 1];
        if (content?.type === "output_text" && content.annotations) {
          for (const annotation of content.annotations) {
            if (annotation.type === "url_citation") {
              console.log(
                `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
              );
            }
          }
        }
      } else if (item.type === "tool_call") {
        console.log(`Tool call completed: ${item.name ?? "unknown"}`);
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nTripAdvisor OpenAPI agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### What this code does

This TypeScript example demonstrates using an OpenAPI tool with API key authentication through a project connection. When you run the code:

1. It loads the TripAdvisor OpenAPI specification from a local file.
1. It configures authentication by using the `TRIPADVISOR_PROJECT_CONNECTION_ID` environment variable.
1. It creates an agent with the TripAdvisor tool that uses the project connection for API key authentication.
1. It sends a streaming request for TripAdvisor location details.
1. It forces tool usage by using `tool_choice: "required"` to ensure the API is called.
1. It processes and displays the streaming response.
1. It cleans up by deleting the agent.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `TRIPADVISOR_PROJECT_CONNECTION_ID`
- Local file: `../assets/tripadvisor_openapi.json`
- Project connection configured with TripAdvisor API key

### Expected output

```console
Loading TripAdvisor OpenAPI specification from assets directory...
Creating agent with OpenAPI project-connection tool...
Agent created (id: asst_abc123, name: MyOpenApiConnectionAgent, version: 1)

Sending request to TripAdvisor OpenAPI agent with streaming...
Follow-up response created with ID: resp_xyz789
Location 293919 is the Eiffel Tower in Paris, France. It has a rating of 4.5 stars with over 140,000 reviews...
Tool call completed: get_tripadvisor_location_details

Follow-up completed!

Cleaning up resources...
Agent deleted

TripAdvisor OpenAPI agent sample completed!
```

### Common errors

- `Error: OpenAPI specification not found`: Check the file path.
- Connection not found: Verify `TRIPADVISOR_PROJECT_CONNECTION_ID` is correct and connection exists.
- `AuthenticationException`: Invalid API key in project connection.
- **API key not injected in requests**: Your OpenAPI spec must include proper `securitySchemes` (under `components`) and `security` sections. The key name in `securitySchemes` must match the key in your project connection.
- `Content type is not supported`: Currently, only these two content types are supported: `application/json` and `application/json-patch+json`.
:::zone-end

## Security and data considerations

When you connect an agent to an OpenAPI tool, the agent can send request parameters derived from user input to the target API.

- Use project connections for secrets (API keys and tokens). Avoid putting secrets in an OpenAPI spec file or source code.
- Review what data the API receives and what it returns before you use the tool in production.
- Use least-privilege access. For managed identity, assign only the roles the target service requires.

## Authenticate with API key

By using API key authentication, you can authenticate your OpenAPI spec by using various methods such as an API key or Bearer token. You can use only one API key security schema per OpenAPI spec. If you need multiple security schemas, create multiple OpenAPI spec tools.

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
  1. Go to the [Foundry portal](https://ai.azure.com/nextgen?cid=learnDocs) and open your project.
  1. Create or select a connection that stores the secret. See [Add a new connection to your project](../../../../how-to/connections-add.md).

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
1. After you create a connection, you can use it through the SDK or REST API. Use the tabs at the top of this article to see code examples.

## Set up a Bearer token connection

You can use token-based authentication (for example, a Bearer token) with the same `project_connection` auth type used for API keys. The key difference is how you configure both the OpenAPI spec and the project connection.

1. Update your OpenAPI spec `securitySchemes` to use `Authorization` as the header name:

   ```json
   "securitySchemes": {
       "bearerAuth": {
           "type": "apiKey",
           "name": "Authorization",
           "in": "header"
       }
   }
   ```

1. Add a `security` section that references the scheme:

   ```json
   "security": [
       {
           "bearerAuth": []
       }
   ]
   ```

1. Create a **Custom keys** connection in your Foundry project:
   1. Go to the [Foundry portal](https://ai.azure.com/nextgen?cid=learnDocs) and open your project.
   1. Create or select a connection that stores the secret. See [Add a new connection to your project](../../../../how-to/connections-add.md).
   1. Enter the following values:
      - **key**: `Authorization` (must match the `name` field in your `securitySchemes`)
      - **value**: `Bearer <token>` (replace `<token>` with your actual token)

   > [!IMPORTANT]
   > The value must include the word `Bearer` followed by a space before the token. For example: `Bearer eyJhbGciOiJSUzI1NiIs...`. If you omit `Bearer `, the API receives a raw token without the required authorization scheme prefix, and the request fails.

1. After you create the connection, use it with the `project_connection` auth type in your code, the same way you would for API key authentication. The connection ID uses the same format: `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

## Authenticate by using managed identity (Microsoft Entra ID)

[Microsoft Entra ID](/entra/fundamentals/what-is-entra) is a cloud-based identity and access management service that your employees can use to access external resources. By using Microsoft Entra ID, you can add extra security to your APIs without needing to use API keys. When you set up managed identity authentication, the agent authenticates through the Foundry tool it uses.

To set up authentication by using Managed Identity:

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

## Troubleshoot common errors

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| API key isn't included in requests. | OpenAPI spec missing `securitySchemes` or `security` sections. | Verify your OpenAPI spec includes both `components.securitySchemes` and a top-level `security` section. Ensure the scheme `name` matches the key name in your project connection. |
| Agent doesn't call the OpenAPI tool. | Tool choice not set or `operationId` not descriptive. | Use `tool_choice="required"` to force tool invocation. Ensure `operationId` values are descriptive so the model can choose the right operation. |
| Authentication fails for managed identity. | Managed identity not enabled or missing role assignment. | Enable system-assigned managed identity on your Foundry resource. Assign the required role (Reader or higher) on the target service. |
| Request fails with 400 Bad Request. | OpenAPI spec doesn't match actual API. | Validate your OpenAPI spec against the actual API. Check parameter names, types, and required fields. |
| Request fails with 401 Unauthorized. | API key or token invalid or expired. | Regenerate the API key/token and update your project connection. Verify the connection ID is correct. |
| Tool returns unexpected response format. | Response schema not defined in OpenAPI spec. | Add response schemas to your OpenAPI spec for better model understanding. |
| `operationId` validation error. | Invalid characters in `operationId`. | Use only letters, `-`, and `_` in `operationId` values. Remove numbers and special characters. |
| Connection not found error. | Connection name or ID mismatch. | Verify `OPENAPI_PROJECT_CONNECTION_NAME` matches the connection name in your Foundry project. |
| Bearer token not sent correctly. | Connection value missing `Bearer ` prefix. | Set the connection value to `Bearer <token>` (with the word `Bearer` and a space before the token). Verify the OpenAPI spec `securitySchemes` uses `"name": "Authorization"`. |

## Choose an authentication method

The following table helps you choose the right authentication method for your OpenAPI tool:

| Authentication method | Best for | Setup complexity |
| --- | --- | --- |
| Anonymous | Public APIs with no authentication | Low |
| API key | Third-party APIs with key-based access | Medium |
| Managed identity | Azure services and Microsoft Entra ID-protected APIs | Medium-High |

## Related content

- [Add a new connection to your project](../../../../how-to/connections-add.md)
- [Set up your environment for Foundry Agent Service](../../../../agents/environment-setup.md)
- [Agents REST API (preview)](../../../../reference/foundry-project-rest-preview.md)
