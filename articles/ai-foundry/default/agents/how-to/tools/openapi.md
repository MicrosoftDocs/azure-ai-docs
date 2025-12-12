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

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

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
## Sample of using Agents with OpenAPI tool

This example demonstrates the ability to use services with an [OpenAPI Specification](https://en.wikipedia.org/wiki/OpenAPI_Specification) with the Agent. It uses the [wttr.in](https://wttr.in/:help) service to get weather and its specification file [weather_openapi.json](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/weather_openapi.json). This example uses synchronous methods of the Azure AI Projects client library. FOr an example that uses asynchronous methods, see the [sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample21_OpenAPI.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Utility method to get the OpenAPI specification file from the Assets folder.
private static string GetFile([CallerFilePath] string pth = "")
{
    var dirName = Path.GetDirectoryName(pth) ?? "";
    return Path.Combine(dirName, "Assets", "weather_openapi.json");
}

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
OpenAPIAgentTool openapiTool = new(toolDefinition);

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
OpenAIResponse response = responseClient.CreateResponse(
        userInputText: "Use the OpenAPI tool to print out, what is the weather in Seattle, WA today."
    );
Console.WriteLine(response.GetOutputText());

// Finally, delete all the resources created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

## Sample of using Agents with OpenAPI tool on Web service, requiring authentication

In this example we will demonstrate the possibility to use services with [OpenAPI Specification](https://en.wikipedia.org/wiki/OpenAPI_Specification) with the Agent in the scenario, requiring authentication. We will use the TripAdvisor specification.

Note that the TripAdvisor service requires key-based authentication. To create a connection in the Azure portal, open Microsoft Foundry and, at the left panel select **Management center** and then select **Connected resources**, and, finally, create new connection of **Custom keys** type; name it `tripadvisor` and add a key value pair. Add key named `key` and enter a value with your TripAdvisor key.

```csharp
// Utility method to get the OpenAPI specification file from the Assets folder.
private static string GetFile([CallerFilePath] string pth = "")
{
    var dirName = Path.GetDirectoryName(pth) ?? "";
    return Path.Combine(dirName, "Assets", "tripadvisor_openapi.json");
}

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
OpenAPIAgentTool openapiTool = new(toolDefinition);

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
ResponseCreationOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice()
};
OpenAIResponse response = responseClient.CreateResponse(
    userInputText: "Recommend me 5 top hotels in paris, France.",
    options: responseOptions
);
Console.WriteLine(response.GetOutputText());

// Finally, delete all the resources we have created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

:::zone-end

:::zone pivot="rest"
The following is an example of using the REST API to call an OpenAPI specified tool with different authentication methods.

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --H "User-Agent: insomnia/11.6.1" \
  --d '{
"model": "$AZURE_AI_MODEL_DEPLOYMENT_NAME",
"input": "Use the OpenAPI tool to print out, what is the weather in Seattle, WA today.",
"tools": [{
        "type": "openapi",
        "openapi": {
          "name": "weatherapp",
          "description": "Tool to get weather data",
          "auth": {
            "type": "anonymous"
          },
        // "auth": {
              "type": "project_connection",
              "security_scheme": {
                  "project_connection_id": "$WEATHER_APP_PROJECT_CONNECTION_ID"              
              }              
            },
         // "auth": {
              "type": "managed_identity",
              "security_scheme": {
                  "audience": ""              
              }              
            },                                        
          "spec": {
            "openapi": "3.1.0",
            "info": {
                "title": "get weather data",
                "description": "Retrieves current weather data for a location.",
                "version": "v1.0.0"
            },
            "servers": [{
                "url": "https://wttr.in"
            }],
            "auth": [],
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
                            "schema": {
                            "type": "string"
                            }
                        },
                        {
                            "name": "format",
                            "in": "query",
                            "description": "Format in which to return data. Always use 3.",
                            "required": true,
                            "schema": {
                            "type": "integer",
                            "default": 3
                            }
                        }
                        ],
                        "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                            "text/plain": {
                                "schema": {
                                "type": "string"
                                }
                            }
                            }
                        },
                        "404": {
                            "description": "Location not found"
                        }
                        },
                        "deprecated": false
                    }
                }
            },
            "components": {
                "schemes": { }
            }
            }
        }
    }]
    }''
```
:::zone-end

:::zone pivot="typescript"

## Create an agent with OpenAPI tool capabilities

The following TypeScript code example demonstrates how to create an AI agent with OpenAPI tool capabilities using the `OpenApiAgentTool` and synchronous Azure AI Projects client. The agent can call external APIs defined by OpenAPI specifications. For a JavaScript version of this example, see the [sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentOpenApi.js) in the Azure SDK for JavaScript repository on GitHub.

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

## Create an agent that uses OpenAPI tools authenticated with a project connection

The following TypeScript code example demonstrates how to create an AI agent that uses OpenAPI tools authenticated via a project connection. The agent loads the TripAdvisor OpenAPI specification from local assets and can invoke the API through the configured project connection. For a JavaScript version of this example, see the [sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentOpenApiConnectionAuth.js) in the Azure SDK for JavaScript repository on GitHub.

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
