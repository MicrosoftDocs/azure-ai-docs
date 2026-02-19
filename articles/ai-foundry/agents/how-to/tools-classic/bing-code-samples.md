---
title: 'Grounding with Bing Search code samples'
titleSuffix: Microsoft Foundry
description: Find code samples to ground Azure AI Agents using Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/18/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-bing-grounding-code
ms.custom: azure-ai-agents-code
---

# How to use Grounding with Bing Search

> [!NOTE]
> - This document refers to the classic version of the agents API. 
> - We recommend customers to start with new [Web Search tool (preview)](../../../default/agents/how-to/tools/web-search.md) with the agents API. If you want to understand the difference between Web Search tool vs Grounding with Bing Search tool, you can learn more [here](../../../default/agents/how-to/tools/web-overview.md)
> 
> 🔍 [View the new Grounding with Bing Search documentation](../../../default/agents/how-to/tools/bing-tools.md).

Use this article to find step-by-step instructions and code samples for Grounding with Bing search.

## Prerequisites

* A [connected Grounding with Bing Search resource](./bing-grounding.md#setup).
* Your connection ID needs to be in this format: `/subscriptions/<subscription_id>/resourceGroups/<resource_group_name>/providers/Microsoft.CognitiveServices/accounts/<ai_service_name>/projects/<project_name>/connections/<connection_name>`

> [!IMPORTANT]
> There are requirements for displaying Grounding with Bing Search results. See the [overview article](./bing-grounding.md#how-to-display-grounding-with-bing-search-results) for details. 

::: zone pivot="portal"

1. In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) navigate to the **Agents** screen for your agent. Scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media\tools\knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Foundry portal." lightbox="../../media\tools\knowledge-tools.png":::

1. Select **Grounding with Bing Search** and follow the prompts to add the tool. Note you can add only one per agent.

    :::image type="content" source="../../media\tools\knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Foundry portal." lightbox="../../media\tools\knowledge-tools-list.png":::

1. Select **Add** to add new connections. Once you add a connection, you can directly select from existing list.
   
   :::image type="content" source="../../media\tools\bing\choose-bing-connection.png" alt-text="A screenshot showing the button for creating a new connection." lightbox="../../media\tools\bing\choose-bing-connection.png":::

1. Select the Grounding with Bing Search resource you want to use and select **Add connection**. 

   :::image type="content" source="../../media\tools\bing\create-bing-connection.png" alt-text="A screenshot showing available Grounding with Bing Search connections." lightbox="../../media\tools\bing\create-bing-connection.png":::

::: zone-end

::: zone pivot="python"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingGroundingTool

# Create an Azure AI Client from an endpoint, copied from your Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()  # Use Azure Default Credential for authentication
)
```


## Create an agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

```python
conn_id = os.environ["BING_CONNECTION_NAME"]  # Ensure the BING_CONNECTION_NAME environment variable is set

# Initialize the Bing Grounding tool
bing = BingGroundingTool(connection_id=conn_id)

with project_client:
    # Create an agent with the Bing Grounding tool
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=bing.definitions,  # Attach the Bing Grounding tool
    )
    print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Add a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="What is the weather in Seattle today?",  # Message content
)
print(f"Created message, ID: {message['id']}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```python
# Create and process an agent run
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
    # tool_choice={"type": "bing_grounding"}  # optional, you can force the model to use Grounding with Bing Search tool
)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message.role}, Content: {message.content}")
```

## Optionally output the run steps used by the agent
```python
run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
for step in run_steps:
    print(f"Step {step['id']} status: {step['status']}")

    # Check if there are tool calls in the step details
    step_details = step.get("step_details", {})
    tool_calls = step_details.get("tool_calls", [])

    if tool_calls:
        print("  Tool calls:")
        for call in tool_calls:
            print(f"    Tool Call ID: {call.get('id')}")
            print(f"    Type: {call.get('type')}")

            function_details = call.get("function", {})
            if function_details:
                print(f"    Function name: {function_details.get('name')}")
    print()  # add an extra newline between steps
```

## Delete the agent when done
```python
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```


::: zone-end
 
::: zone pivot="csharp"

## Create a project client

Create a client object that contains the project endpoint for connecting to your AI project and other resources.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("ProjectEndpoint");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("ModelDeploymentName");
var bingConnectionId = System.Environment.GetEnvironmentVariable("BingConnectionId");

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Create an agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

```csharp

BingGroundingToolDefinition bingGroundingTool = new(
    new BingGroundingSearchToolParameters(
        [new BingGroundingSearchConfiguration(bingConnectionId)]
    )
);

// Create the Agent
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "Use the bing grounding tool to answer questions.",
    tools: [bingGroundingTool]
);
```

## Create a thread and run

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
PersistentThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");
ThreadRun run = agentClient.Runs.CreateRun(thread, agent);

```

## Wait for the agent to complete and print the output

First, wait for the agent to complete the run by polling its status. The model uses the Grounding with Bing Search tool to provide a response to the user's question.

```csharp
// Wait for the agent to finish running
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = agentClient.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

// Confirm that the run completed successfully
if (run.Status != RunStatus.Completed)
{
    throw new Exception("Run did not complete successfully, error: " + run.LastError?.Message);
}
```

Then, retrieve and process the messages from the completed run.

```csharp
// Retrieve all messages from the agent client
Pageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Process messages in order
foreach (PersistentThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            string response = textItem.Text;

            // If we have Text URL citation annotations, reformat the response to show title & URL for citations
            if (textItem.Annotations != null)
            {
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUriCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UriCitation.Title}]({urlAnnotation.UriCitation.Uri})");
                    }
                }
            }
            Console.Write($"Agent response: {response}");
        }
        else if (contentItem is MessageImageFileContent imageFileItem)
        {
            Console.Write($"<image from ID: {imageFileItem.FileId}");
        }
        Console.WriteLine();
    }
}

```

## Optionally output the run steps used by the agent

```csharp
// Retrieve the run steps used by the agent and print those to the console
Console.WriteLine("Run Steps used by Agent:");
Pageable<RunStep> runSteps = agentClient.Runs.GetRunSteps(run);

foreach (var step in runSteps)
{
    Console.WriteLine($"Step ID: {step.Id}, Total Tokens: {step.Usage.TotalTokens}, Status: {step.Status}, Type: {step.Type}");

    if (step.StepDetails is RunStepMessageCreationDetails messageCreationDetails)
    {
        Console.WriteLine($"   Message Creation Id: {messageCreationDetails.MessageCreation.MessageId}");
    }
    else if (step.StepDetails is RunStepToolCallDetails toolCallDetails)
    {
        // We know this agent only has the Bing Grounding tool, so we can cast it directly
        foreach (RunStepBingGroundingToolCall toolCall in toolCallDetails.ToolCalls)
        {
            Console.WriteLine($"   Tool Call Details: {toolCall.GetType()}");

            foreach (var result in toolCall.BingGrounding)
            {
                Console.WriteLine($"      {result.Key}: {result.Value}");
            }
        }
    }
}

```

## Clean up resources

Clean up the resources from this sample.

```csharp
// Delete thread and agent
agentClient.Threads.DeleteThread(threadId: thread.Id);
agentClient.Administration.DeleteAgent(agentId: agent.Id);
```
::: zone-end

::: zone pivot="javascript"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```javascript
const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"];

// Create an Azure AI Client
const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```


## Create an agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

```javascript

const connectionId = process.env["AZURE_BING_CONNECTION_ID"] || "<connection-name>";
// Initialize agent bing tool with the connection id
const bingTool = ToolUtility.createBingGroundingTool([{ connectionId: connectionId }]);

// Create agent with the bing tool and process assistant run
const agent = await client.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [bingTool.definition],
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Create a thread

```javascript
// Create thread for communication
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create message to thread
const message = await client.messages.create(
  thread.id,
  "user",
  "How does wikipedia explain Euler's Identity?",
);
console.log(`Created message, message ID : ${message.id}`);
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```javascript

// Create and process agent run in thread with tools
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
  console.log(`Run failed: ${run.lastError?.message}`);
}
console.log(`Run finished with status: ${run.status}`);

// Delete the assistant when done
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);

// Fetch and log all messages
const messagesIterator = client.messages.list(thread.id);
console.log(`Messages:`);

// Get the first message
const firstMessage = await messagesIterator.next();
if (!firstMessage.done && firstMessage.value) {
  const agentMessage = firstMessage.value.content[0];
  if (isOutputOfType(agentMessage, "text")) {
    const textContent = agentMessage;
    console.log(`Text Message Content - ${textContent.text.value}`);
  }
}

```

::: zone-end


::: zone pivot="rest"

>[!IMPORTANT]
> 1. This REST API enables developers to invoke the Grounding with Bing Search tool through the Foundry Agent Service. It doesn't send calls to the Grounding with Bing Search API directly. 

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.


## Create an agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "instructions": "You are a helpful agent.",
        "name": "my-agent",
        "model": "gpt-4o",
        "tools": [
          {
            "type": "bing_grounding",
            "bing_grounding": {
                "search_configurations": [
                    {
                        "connection_id": "<your_connection_id>",
                        "count": 7, 
                        "market": "en-US", 
                        "set_lang": "en", 
                        "freshness": "Week",
                    }
                ]
            }
          }
        ]
      }'
```

## Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

::: zone-end

::: zone pivot="java"

## Code example

```java
package com.example.agents;

import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.models.BingGroundingSearchConfiguration;
import com.azure.ai.agents.persistent.models.BingGroundingSearchToolParameters;
import com.azure.ai.agents.persistent.models.BingGroundingToolDefinition;
import com.azure.ai.agents.persistent.models.CreateAgentOptions;
import com.azure.ai.agents.persistent.models.CreateRunOptions;
import com.azure.ai.agents.persistent.models.MessageImageFileContent;
import com.azure.ai.agents.persistent.models.MessageRole;
import com.azure.ai.agents.persistent.models.MessageTextContent;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.PersistentAgentThread;
import com.azure.ai.agents.persistent.models.RunStatus;
import com.azure.ai.agents.persistent.models.ThreadMessage;
import com.azure.ai.agents.persistent.models.ThreadRun;
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.core.http.rest.PagedIterable;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.util.Arrays;

public class AgentExample {

    public static void main(String[] args) {

        // variables for authenticating requests to the agent service 
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");
        String bingConnectionId = System.getenv("BING_CONNECTION_ID");

        PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder().endpoint(projectEndpoint)
            .credential(new DefaultAzureCredentialBuilder().build());
        PersistentAgentsClient agentsClient = clientBuilder.buildClient();
        PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
        ThreadsClient threadsClient = agentsClient.getThreadsClient();
        MessagesClient messagesClient = agentsClient.getMessagesClient();
        RunsClient runsClient = agentsClient.getRunsClient();

        BingGroundingSearchConfiguration searchConfiguration = new BingGroundingSearchConfiguration(bingConnectionId);
        BingGroundingSearchToolParameters searchToolParameters
            = new BingGroundingSearchToolParameters(Arrays.asList(searchConfiguration));

        BingGroundingToolDefinition bingGroundingTool = new BingGroundingToolDefinition(searchToolParameters);

        String agentName = "bing_grounding_example";
        CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName)
            .setName(agentName)
            .setInstructions("You are a helpful agent")
            .setTools(Arrays.asList(bingGroundingTool));
        PersistentAgent agent = administrationClient.createAgent(createAgentOptions);

        PersistentAgentThread thread = threadsClient.createThread();
        ThreadMessage createdMessage = messagesClient.createMessage(
            thread.getId(),
            MessageRole.USER,
            "How does wikipedia explain Euler's Identity?");

        try {
            //run agent
            CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
                .setAdditionalInstructions("");
            ThreadRun threadRun = runsClient.createRun(createRunOptions);

            waitForRunCompletion(thread.getId(), threadRun, runsClient);
            printRunMessages(messagesClient, thread.getId());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            //cleanup
            threadsClient.deleteThread(thread.getId());
            administrationClient.deleteAgent(agent.getId());
        }
    }
    
    // A helper function to print messages from the agent
    public static void printRunMessages(MessagesClient messagesClient, String threadId) {

        PagedIterable<ThreadMessage> runMessages = messagesClient.listMessages(threadId);
        for (ThreadMessage message : runMessages) {
            System.out.print(String.format("%1$s - %2$s : ", message.getCreatedAt(), message.getRole()));
            for (MessageContent contentItem : message.getContent()) {
                if (contentItem instanceof MessageTextContent) {
                    System.out.print((((MessageTextContent) contentItem).getText().getValue()));
                } else if (contentItem instanceof MessageImageFileContent) {
                    String imageFileId = (((MessageImageFileContent) contentItem).getImageFile().getFileId());
                    System.out.print("Image from ID: " + imageFileId);
                }
                System.out.println();
            }
        }
    }

    // a helper function to wait until a run has completed running
    public static void waitForRunCompletion(String threadId, ThreadRun threadRun, RunsClient runsClient)
        throws InterruptedException {

        do {
            Thread.sleep(500);
            threadRun = runsClient.getRun(threadId, threadRun.getId());
        }
        while (
            threadRun.getStatus() == RunStatus.QUEUED
                || threadRun.getStatus() == RunStatus.IN_PROGRESS
                || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

        if (threadRun.getStatus() == RunStatus.FAILED) {
            System.out.println(threadRun.getLastError().getMessage());
        }
    }
}
```
::: zone-end
