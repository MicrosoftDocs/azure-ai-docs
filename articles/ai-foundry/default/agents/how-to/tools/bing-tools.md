---
title: 'Grounding with Bing Search overview for the agents API'
titleSuffix: Microsoft Foundry
description: Learn about the options available to let agents search the web using standard and custom Bing Search grounding tools.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: article
ms.date: 12/11/2025
author: alvinashcraft
ms.author: aashcraft
ai-usage: ai-assisted
zone_pivot_groups: selection-bing-grounding-new
---

# Grounding with Bing Search tools for agents

Traditional language models operate with a knowledge cutoff. They can't access new information beyond a fixed point in time. By using Grounding with Bing Search and Grounding with Bing Custom Search (preview), your agents can incorporate real-time public web data when generating responses. By using these tools, you can ask questions such as "what is the top AI news today".

The grounding process involves several key steps:

1. **Query formulation**: The agent identifies information gaps and constructs search queries.
1. **Search execution**: The grounding tool submits queries to search engines and retrieves results.
1. **Information synthesis**: The agent processes search results and integrates findings into responses.
1. **Source attribution**: The agent provides transparency by citing search sources.

>[!IMPORTANT]
> - Grounding with Bing Search and/or Grounding with Bing Custom Search is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:~:text=First-Party%20Consumption%20Services) with [terms for online services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS), governed by the [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409). 
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and/or Grounding with Bing Custom Search. When you use Grounding with Bing Search and/or Grounding with Bing Custom Search, your data flows outside the Azure compliance and Geo boundary. This also means use of Grounding with Bing Search and/or Grounding with Bing Custom Search waives all elevated Government Community Cloud security and compliance commitments, to include data sovereignty and screened/citizenship-based support, as applicable.  
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See pricing for [details](https://www.microsoft.com/en-us/bing/apis/grounding-pricing). 
> - See the [manage section](#manage-grounding-with-bing-search-and-grounding-with-bing-custom-search) for information about how Azure admins can manage access to use of Grounding with Bing Search and/or Grounding with Bing Custom Search.

## Available tools

|Tool  |Description  |Use-case  |
|---------|---------|---------|
|Grounding with Bing Search     | Gives agents standard access to Bing's search capabilities.        | Scenarios requiring broad knowledge access.        |
|Grounding with Bing Custom Search (preview)  | Allows agents to search within a configurable set of public web domains. You define the parts of the web you want to draw from so users only see relevant results from the domains and subdomains of your choosing.        | Scenarios requiring information management.        |

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

## Code examples

> [!NOTE]
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"
The following examples demonstrate how to create an agent with Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools, and how to use the agent to respond to user queries.

# [Grounding with Bing Search](#tab/grounding-with-bing)

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BingGroundingAgentTool,
    BingGroundingSearchToolParameters,
    BingGroundingSearchConfiguration,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[
                BingGroundingAgentTool(
                    bing_grounding=BingGroundingSearchToolParameters(
                        search_configurations=[
                            BingGroundingSearchConfiguration(
                                project_connection_id=os.environ["BING_PROJECT_CONNECTION_ID"]
                            )
                        ]
                    )
                )
            ],
        ),
        description="You are a helpful agent.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="What is today's date and whether in Seattle?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(f"URL Citation: {annotation.url}")
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```

# [Grounding with Bing Custom Search (preview)](#tab/grounding-with-bing-custom)

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BingCustomSearchAgentTool,
    BingCustomSearchToolParameters,
    BingCustomSearchConfiguration,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Get the OpenAI client for responses and conversations
openai_client = project_client.get_openai_client()

bing_custom_search_tool = BingCustomSearchAgentTool(
    bing_custom_search_preview=BingCustomSearchToolParameters(
        search_configurations=[
            BingCustomSearchConfiguration(
                project_connection_id=os.environ["BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID"],
                instance_name=os.environ["BING_CUSTOM_SEARCH_INSTANCE_NAME"],
            )
        ]
    )
)

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="""You are a helpful agent that can use Bing Custom Search tools to assist users. 
            Use the available Bing Custom Search tools to answer questions and perform tasks.""",
            tools=[bing_custom_search_tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input(
        "Enter your question for the Bing Custom Search agent " "(e.g., 'Tell me more about foundry agent service'): \n"
    )

    # Send initial request that will trigger the Bing Custom Search tool
    stream_response = openai_client.responses.create(
        stream=True,
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(
                                f"URL Citation: {annotation.url}, "
                                f"Start index: {annotation.start_index}, "
                                f"End index: {annotation.end_index}"
                            )
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```

---
:::zone-end

:::zone pivot="csharp"
The following C# examples demonstrate how to create an agent with Grounding with Bing Search tool, and how to use the agent to respond to user queries. These examples use synchronous calls for simplicity. For asynchronous examples, see the [agent tools C# samples](https://github.com/Azure/azure-sdk-for-net/tree/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples).

To enable your Agent to use Bing search API, use `BingGroundingAgentTool`.

# [Grounding with Bing Search](#tab/grounding-with-bing)

```csharp
// Read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var connectionName = System.Environment.GetEnvironmentVariable("BING_CONNECTION_NAME");

// Create an instance of AIProjectClient.
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get the Bing connection and create the agent version with Bing grounding tool
AIProjectConnection bingConnectionName = projectClient.Connections.GetConnection(connectionName: connectionName);
BingGroundingAgentTool bingGroundingAgentTool = new(new BingGroundingSearchToolOptions(
    searchConfigurations: [new BingGroundingSearchConfiguration(projectConnectionId: bingConnectionName.Id)]
    )
);
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { bingGroundingAgentTool, }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Output the agent version info
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

OpenAIResponse response = responseClient.CreateResponse("How does wikipedia explain Euler's Identity?");

// Helper method to extract and format URL citation annotations
private static string GetFormattedAnnotation(OpenAIResponse response)
{
    foreach (ResponseItem item in response.OutputItems)
    {
        if (item is MessageResponseItem messageItem)
        {
            foreach (ResponseContentPart content in messageItem.Content)
            {
                foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
                {
                    if (annotation is UriCitationMessageAnnotation uriAnnotation)
                    {
                        return $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                    }
                }
            }
        }
    }
    return "";
}

// Validate and print the response
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine($"{response.GetOutputText()}{GetFormattedAnnotation(response)}");

// Clean up resources by deleting the agent version
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

# [Grounding with Bing in streaming scenarios](#tab/grounding-with-bing-streaming)

```csharp
// Read the environment variables, which will be used in the next steps
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var connectionName = System.Environment.GetEnvironmentVariable("BING_CONNECTION_NAME");

// Create an instance of AIProjectClient
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get the Bing connection and create the agent version with Bing grounding tool
AIProjectConnection bingConnectionName = projectClient.Connections.GetConnection(connectionName: connectionName);
BingGroundingAgentTool bingGroundingAgentTool = new(new BingGroundingSearchToolOptions(
    searchConfigurations: [new BingGroundingSearchConfiguration(projectConnectionId: bingConnectionName.Id)]
    )
);
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { bingGroundingAgentTool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Helper method to extract and format URL citation annotations
private static string GetFormattedAnnotation(ResponseItem item)
{
    if (item is MessageResponseItem messageItem)
    {
        foreach (ResponseContentPart content in messageItem.Content)
        {
            foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
            {
                if (annotation is UriCitationMessageAnnotation uriAnnotation)
                {
                    return $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                }
            }
        }
    }
    return "";
}

// Stream the response from the agent version
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

string annotation = "";
string text = "";

// Parse the streaming response and output the results
foreach (StreamingResponseUpdate streamResponse in responseClient.CreateResponseStreaming("How does wikipedia explain Euler's Identity?"))
{
    if (streamResponse is StreamingResponseCreatedUpdate createUpdate)
    {
        Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
    }
    else if (streamResponse is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.WriteLine($"Delta: {textDelta.Delta}");
    }
    else if (streamResponse is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
    {
        text = textDoneUpdate.Text;
    }
    else if (streamResponse is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
    {
        if (annotation.Length == 0)
        {
            annotation = GetFormattedAnnotation(itemDoneUpdate.Item);
        }
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed: {errorUpdate.Message}");
    }
}
Console.WriteLine($"{text}{annotation}");

// Clean up resources by deleting the agent version
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

---

:::zone-end

:::zone pivot="rest"
The following REST API examples demonstrate how to use Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools to respond to user queries.

# [Grounding with Bing Search](#tab/grounding-with-bing)

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --H "User-Agent: insomnia/11.6.1" \
  --d '{
"model": "$AZURE_AI_MODEL_DEPLOYMENT_NAME",
"input": "How does wikipedia explain Euler's Identity?",
"tools": [
  {
   "type": "bing_grounding",
   "bing_grounding": {
    "search_configurations": [
            {
                "project_connection_id": "$BING__SEARCH_PROJECT_CONNECTION_ID",
                "count": 7, 
                "market": "en-US", 
                "set_lang": "en", 
                "freshness": "7d",
            }
        ]
    }
    ]
}'
```


# [Grounding with Bing Custom Search (preview)](#tab/grounding-with-bing-custom)

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --H "User-Agent: insomnia/11.6.1" \
  --d '{
"model": "$AZURE_AI_MODEL_DEPLOYMENT_NAME",
"input": "How does wikipedia explain Euler's Identity?",
"tools": [
  {
   "type": "bing_custom_search_preview",
   "bing_custom_search_preview": {
        "search_configurations": [
            {
                "project_connection_id": "$BING__SEARCH_PROJECT_CONNECTION_ID",
                "instance_name": "$BING_CUSTOM_SEARCH_INSTANCE_NAME",                         
                "count": 7, 
                "market": "en-US", 
                "set_lang": "en", 
                "freshness": "7d",
            }
        ]
    }
    ]
}'
```


---

:::zone-end

:::zone pivot="typescript"
The following TypeScript examples demonstrate how to create an agent with Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools, and how to use the agent to respond to user queries. For JavaScript examples, see the [agent tools JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools) in the Azure SDK for JavaScript repository on GitHub.

# [Grounding with Bing Search](#tab/grounding-with-bing)

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const bingProjectConnectionId =
  process.env["BING_PROJECT_CONNECTION_ID"] || "<bing project connection id>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with Bing grounding tool...");

  const agent = await project.agents.createVersion("MyBingGroundingAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant.",
    tools: [
      {
        type: "bing_grounding",
        bing_grounding: {
          search_configurations: [
            {
              project_connection_id: bingProjectConnectionId,
            },
          ],
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Send request that requires current information from the web
  console.log("\nSending request to Bing grounding agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: "What is today's date and weather in Seattle?",
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
      if (event.item.type === "message") {
        const item = event.item;
        if (item.content && item.content.length > 0) {
          const lastContent = item.content[item.content.length - 1];
          if (lastContent.type === "output_text" && lastContent.annotations) {
            for (const annotation of lastContent.annotations) {
              if (annotation.type === "url_citation") {
                console.log(
                  `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
                );
              }
            }
          }
        }
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

  console.log("\nBing grounding agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

# [Grounding with Bing Custom Search (preview)](#tab/grounding-with-bing-custom)

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const bingCustomSearchProjectConnectionId =
  process.env["BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID"] ||
  "<bing custom search project connection id>";
const bingCustomSearchInstanceName =
  process.env["BING_CUSTOM_SEARCH_INSTANCE_NAME"] || "<bing custom search instance name>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with Bing Custom Search tool...");

  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a helpful agent that can use Bing Custom Search tools to assist users. Use the available Bing Custom Search tools to answer questions and perform tasks.",
    tools: [
      {
        type: "bing_custom_search_preview",
        bing_custom_search_preview: {
          search_configurations: [
            {
              project_connection_id: bingCustomSearchProjectConnectionId,
              instance_name: bingCustomSearchInstanceName,
            },
          ],
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Prompt user for input
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const userInput = await new Promise<string>((resolve) => {
    rl.question(
      "Enter your question for the Bing Custom Search agent (e.g., 'Tell me more about foundry agent service'): \n",
      (answer) => {
        rl.close();
        resolve(answer);
      },
    );
  });

  // Send initial request that will trigger the Bing Custom Search tool
  console.log("\nSending request to Bing Custom Search agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: userInput,
      stream: true,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
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
      if (event.item.type === "message") {
        const item = event.item;
        if (item.content && item.content.length > 0) {
          const lastContent = item.content[item.content.length - 1];
          if (lastContent.type === "output_text" && lastContent.annotations) {
            for (const annotation of lastContent.annotations) {
              if (annotation.type === "url_citation") {
                console.log(
                  `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
                );
              }
            }
          }
        }
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

  console.log("\nBing Custom Search agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

---

:::zone-end

## How it works

The user query is the message that an end user sends to an agent, such as *"should I take an umbrella with me today? I'm in Seattle."* Instructions are the system message a developer can provide to share context and provide instructions to the AI model on how to use various tools or behave. 

When a user sends a query, the customer's AI model deployment first processes it (using the provided instructions) to later perform a Bing search query (which is [visible to developers](#how-to-display-search-results)). 
Grounding with Bing returns relevant search results to the customer's model deployment, which then generates the final output. 

> [!NOTE]
> When you use Grounding with Bing Search or Grounding with Bing Custom Search, the only information sent to Bing is the Bing search query, tool parameters, and your resource key. The service doesn't send any end user-specific information. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

Authorization happens between the Grounding with Bing Search or Grounding with Bing Custom Search service and Foundry Agent Service. Any Bing search query that the service generates and sends to Bing for the purposes of grounding is transferred, along with the resource key, outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is subject to Bing's terms and doesn't have the same compliance standards and certifications as the Agent Service, as described in the [Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise). It's your responsibility to assess whether the use of Grounding with Bing Search or Grounding with Bing Custom Search in your agent meets your needs and requirements.

Transactions with your Grounding with Bing resource are counted by the number of tool calls per run. You can see how many tool calls are made from the run step.

Developers and end users don't have access to raw content returned from Grounding with Bing Search. The model response, however, includes citations with links to the websites used to generate the response, and a link to the Bing query used for the search. You can retrieve the **model response** by accessing the data in the conversation that was created. These two *references* must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Search's [Use and Display Requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise#use-and-display-requirements). See the [how to display Grounding with Bing Search results](#how-to-display-search-results) section for details.

## How to display search results

According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise#use-and-display-requirements#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. You can find this information in the API response, in the `arguments` parameter. To render the webpage, replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like `https://www.bing.com/search?q={search query}`.

:::image type="content" source="../../../../agents/media/tools/bing/website-citations.png" alt-text="A screenshot showing citations for Bing search results." lightbox="../../../../agents/media/tools/bing/website-citations.png":::

## Grounding with Bing Custom Search configuration

Grounding with Bing Custom Search is a powerful tool that you can use to select a subspace of the web to limit your Agent’s grounding knowledge. Here are a few tips to help you take full advantage of this capability: 

- If you own a public site that you want to include in the search but Bing hasn't indexed, see the [Bing webmaster documentation](https://www.bing.com/webmaster/help/webmaster-guidelines-30fba23d) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date. 
- You need at least the contributor role for the Bing Custom Search resource to create a configuration.
- You can only block certain domains and perform a search against the rest of the web (a competitor's site, for example). 
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing. 
  - Domain (for example, `https://www.microsoft.com`) 
  - Domain and path (for example, `https://www.microsoft.com/surface`) 
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`) 

## Supported capabilities and known issues

- The Grounding with Bing Search tool is designed to retrieve real-time information from the web, not specific web domains. For retrieving information from specific domains, use the Grounding with Bing Custom Search tool.
- Don't **summarize** an entire web page.
- Within one run, the AI model evaluates the tool outputs and might decide to invoke the tool again for more information and context. The AI model might also decide which pieces of tool outputs are used to generate the response.
- Azure AI Agent service returns **AI model generated response** as output so end-to-end latency is impacted by pre-/post-processing of LLMs.
- The Grounding with Bing Search and Grounding with Bing Custom Search tools don't return the tool output to developers and end users.
- Grounding with Bing Search and Grounding with Bing Custom Search only works with agents that aren't using VPN or Private Endpoints. The agent must have normal network access.

## Manage Grounding with Bing Search and Grounding with Bing Custom Search

Admins can use RBAC role assignments to enable or disable the use of Grounding with Bing and Grounding with Bing Custom Search within the subscription or resource group. 

1. The admin registers `Microsoft.Bing` in the Azure subscription. The admin needs permissions to perform the `/register/action` operation for the resource provider. The Contributor and Owner roles include this permission. For more information about how to register, see the [Azure Resource Manager](/azure/azure-resource-manager/management/resource-providers-and-types) documentation.
1. After the admin registers `Microsoft.Bing`, users with permissions can create, delete, or retrieve the resource key for a Grounding with Bing and/or Grounding with Bing Custom Search resource. These users need the **Contributor** or **Owner** role at the subscription or resource group level. 
1. After creating a Grounding with Bing and/or Grounding with Bing Custom Search resource, users with permissions can create a Microsoft Foundry connection to connect to the resource and use it as a tool in Foundry Agent Service. These users need at least the **Azure AI Project Manager** role. 

### Disable use of Grounding with Bing Search and Grounding with Bing Custom Search

1. The admin needs to have the **Owner** or **Contributor** role in your subscription.
1. The admin can then delete all Grounding with Bing Search and Grounding with Bing Custom Search resources in the subscription.
1. The admin should then unregister the `Microsoft.Bing` resource provider in your subscription (you can't unregister before deleting all resources). For more information, see the [Azure Resource Manager documentation](/azure/azure-resource-manager/management/resource-providers-and-types). 
1. Next, the admin should create an Azure Policy to disallow creation of Grounding with Bing Search and Grounding with Bing Custom Search resources in their subscription, following the sample [here](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/05-custom-policy-definitions/deny-disallowed-connections.json).
