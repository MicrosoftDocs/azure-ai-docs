---
title: "How to use Azure AI Search in Foundry Agent Service (classic)"
description: "Learn how to ground classic Foundry agents with content from an existing Azure AI Search index by using supported SDK and REST API samples."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/05/2026
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.custom:
    - azure-ai-agents
    - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-azure-ai-search
---

# How to use an existing index with the Azure AI Search tool (classic)

> [!NOTE]
> This document refers to the Microsoft Foundry (classic) agents.
>
> 🔍 [View the new Azure AI Search tool documentation](../../../../foundry/agents/how-to/tools/ai-search.md).
> Agents (classic) are deprecated and retire on March 31, 2027. Use the new agents in the generally available [Foundry Agent Service](../../../../foundry/agents/overview.md). Follow the [migration guide](../../../../foundry/agents/how-to/migrate.md) to update your workloads.

This article explains how to use an existing search index with the [Azure AI Search](/azure/search/search-what-is-azure-search) tool.

## Prerequisites

+ Completion of the [Azure AI Search tool setup](./azure-ai-search.md?pivot=overview-azure-ai-search).
+ Sign in locally by using `az login` so `DefaultAzureCredential` can authenticate.
+ Install the classic-compatible packages for your language:

    - Python 3.9 or later: `pip install "azure-ai-projects==1.0.0" "azure-ai-agents==1.1.0" azure-identity`.
    - .NET 8 or later: `dotnet add package Azure.AI.Agents.Persistent --version 1.1.0` and `dotnet add package Azure.Identity`.
    - Node.js 20 or later: `npm install @azure/ai-agents@1.1.0 @azure/identity`.
    - Java: `com.azure:azure-ai-agents-persistent:1.0.0-beta.2` and `com.azure:azure-identity:1.18.4`.

:::zone pivot="portal"

## Add the Azure AI Search tool to an agent

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) and select your project.

1. From the left pane, select **Agents**.

1. Select your agent from the list, and then select **Knowledge** > **Add**.

1. Select **Azure AI Search**. 

1. Follow the prompts to add the Azure AI Search tool.

:::zone-end

:::zone pivot="python"

## Set environment variables

Set the project endpoint, model deployment name, and existing search index name:

```bash
export PROJECT_ENDPOINT="<your-project-endpoint>"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
export AZURE_AI_SEARCH_INDEX_NAME="<your-index-name>"
```

## Create a project client

Create a project client by using the endpoint of your Foundry project.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_endpoint = os.environ["PROJECT_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)
)
```

## Configure the Azure AI Search tool

Using the connection ID of your Azure AI Search service, configure the Azure AI Search tool to use your search index.

```python
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
from azure.ai.projects.models import ConnectionType

# Define the Azure AI Search connection ID and index name
azure_ai_conn_id = project_client.connections.get_default(ConnectionType.AZURE_AI_SEARCH).id
print(f"Search connection ID: {azure_ai_conn_id}")

index_name = os.environ["AZURE_AI_SEARCH_INDEX_NAME"]

# Initialize the Azure AI Search tool
ai_search = AzureAISearchTool(
    index_connection_id=azure_ai_conn_id,
    index_name=index_name,
    query_type=AzureAISearchQueryType.SIMPLE,  # Use SIMPLE query type
    top_k=3,  # Retrieve the top 3 results
    filter="",  # Optional filter for search results
)
```

## Create an agent with the Azure AI Search tool enabled

Change the model to the one deployed in your project. You can find the model name on the **Models** tab of the Foundry portal. You can also change the agent's name and instructions to suit your needs.

```python
# Define the model deployment name
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

# Create an agent with the Azure AI Search tool
agent = project_client.agents.create_agent(
    model=model_deployment_name,
    name="my-agent",
    instructions="You are a helpful agent",
    tools=ai_search.definitions,
    tool_resources=ai_search.resources,
)
print(f"Created agent, ID: {agent.id}")
```

## Ask the agent questions about data in the index

Now that the agent is created, you can ask it questions about the data in your search index.

```python
from azure.ai.agents.models import MessageRole, ListSortOrder

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Send a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="What is the temperature rating of the cozynights sleeping bag?",
)
print(f"Created message, ID: {message.id}")

# Create and process a run with the specified thread and agent
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages in the thread
messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages.data:
    print(f"Role: {message.role}, Content: {message.content}")
```

### Expected output

The answer depends on your index. A successful run produces output similar to:

```output
Search connection ID: <connection-id>
Created agent, ID: <agent-id>
Created thread, ID: <thread-id>
Created message, ID: <message-id>
Run finished with status: RunStatus.COMPLETED
Role: MessageRole.AGENT, Content: <answer grounded in the search index>
```

## Clean up resources

After you verify the response, delete the thread and agent, and then close the project client.

```python
project_client.agents.threads.delete(thread.id)
project_client.agents.delete_agent(agent.id)
project_client.close()
print("Deleted thread and agent, and closed the project client")
```

:::zone-end

:::zone pivot="csharp"

## Set environment variables

Set the values that the sample reads at runtime.

```powershell
$env:PROJECT_ENDPOINT = "<your-project-endpoint>"
$env:MODEL_DEPLOYMENT_NAME = "<your-model-deployment-name>"
$env:AZURE_AI_SEARCH_CONNECTION_ID = "<your-search-connection-id>"
$env:AZURE_AI_SEARCH_INDEX_NAME = "<your-index-name>"
```

## Create a project client

Create a client object that contains the endpoint of your Foundry project, which enables connections to your project and other resources.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using System;
using System.Threading;

var projectEndpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var azureAiSearchConnectionId = Environment.GetEnvironmentVariable(
    "AZURE_AI_SEARCH_CONNECTION_ID");
var indexName = Environment.GetEnvironmentVariable("AZURE_AI_SEARCH_INDEX_NAME");

// Create the agent client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Configure the Azure AI Search tool

Using the connection ID of your Azure AI Search service, configure the Azure AI Search tool to use your search index.

```csharp
AzureAISearchToolResource searchResource = new(
    indexConnectionId: azureAiSearchConnectionId,
    indexName: indexName,
    topK: 5,
    filter: "category eq 'sleeping bag'",
    queryType: AzureAISearchQueryType.Simple
);

ToolResources toolResource = new() { AzureAISearch = searchResource };

```

## Create an agent with the Azure AI Search tool enabled

Change the model to the one deployed in your project. You can find the model name on the **Models** tab of the Foundry portal. You can also change the agent's name and instructions to suit your needs.

```csharp
// Create an agent with Tools and Tool Resources
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "Use the index provided to answer questions.",
    tools: [new AzureAISearchToolDefinition()],
    toolResources: toolResource
);
Console.WriteLine($"Created agent, ID: {agent.Id}");

```

## Ask the agent questions about data in the index

Now that the agent is created, you can ask it questions about the data in your search index.

```csharp
// Create thread for communication
PersistentAgentThread thread = agentClient.Threads.CreateThread();
Console.WriteLine($"Created thread, ID: {thread.Id}");

// Create message and run the agent
PersistentThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the temperature rating of the cozynights sleeping bag?");
ThreadRun run = agentClient.Runs.CreateRun(thread, agent);
Console.WriteLine($"Created run, ID: {run.Id}");

```

## Wait for the agent to complete and print the output

Wait for the agent to finish running and print the output to the console.

```csharp
// Wait for the agent to finish running
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = agentClient.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

Console.WriteLine($"Run finished with status: {run.Status}");

// Confirm that the run completed successfully
if (run.Status != RunStatus.Completed)
{
    throw new Exception("Run did not complete successfully, error: " + run.LastError?.Message);
}

// Retrieve the messages from the agent client
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
            // Annotate only agent messages
            if (threadMessage.Role == MessageRole.Agent && textItem.Annotations.Count > 0)
            {
                string annotatedText = textItem.Text;

                // If there are text URL citation annotations, reformat the response to show the title and URL for citations
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUriCitationAnnotation urlAnnotation)
                    {
                        annotatedText = annotatedText.Replace(
                            urlAnnotation.Text,
                            $" [see {urlAnnotation.UriCitation.Title}] ({urlAnnotation.UriCitation.Uri})");
                    }
                }
                Console.Write(annotatedText);
            }
            else
            {
                Console.Write(textItem.Text);
            }
        }
        else if (contentItem is MessageImageFileContent imageFileItem)
        {
            Console.Write($"<image from ID: {imageFileItem.FileId}");
        }
        Console.WriteLine();
    }
}
```

### Expected output

The answer and citations depend on your index. A successful run produces output similar to:

```output
Created agent, ID: <agent-id>
Created thread, ID: <thread-id>
Created run, ID: <run-id>
Run finished with status: Completed
<timestamp> - Agent: <answer grounded in the search index> [see <source title>] (<source URL>)
```

## Optionally output the run steps used by the agent

```csharp
// Retrieve the run steps used by the agent and print them to the console
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
        // This agent only has the Azure AI Search tool, so cast it directly
        foreach (RunStepAzureAISearchToolCall toolCall in toolCallDetails.ToolCalls)
        {
            Console.WriteLine($"   Tool Call Details: {toolCall.GetType()}");

            foreach (var result in toolCall.AzureAISearch)
            { 
                Console.WriteLine($"      {result.Key}: {result.Value}");
            }
        }
    }
}

```
## Clean up resources

Delete the resources from this sample.

```csharp
// Clean up resources
agentClient.Threads.DeleteThread(thread.Id);
agentClient.Administration.DeleteAgent(agent.Id);
Console.WriteLine("Deleted thread and agent");
```

:::zone-end

:::zone pivot="javascript"

## Set environment variables

Set the values that the sample reads at runtime.

```bash
export PROJECT_ENDPOINT="<your-project-endpoint>"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
export AZURE_AI_CONNECTION_ID="<your-search-connection-id>"
export AZURE_AI_SEARCH_INDEX_NAME="<your-index-name>"
```

## Create a client

Create an agents client by using the endpoint of your Foundry project.

```javascript
const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { DefaultAzureCredential } = require("@azure/identity");
const { delay } = require("@azure/core-util");

const projectEndpoint = process.env["PROJECT_ENDPOINT"];
const modelDeploymentName = process.env["MODEL_DEPLOYMENT_NAME"];
const connectionId = process.env["AZURE_AI_CONNECTION_ID"];
const indexName = process.env["AZURE_AI_SEARCH_INDEX_NAME"];

if (!projectEndpoint || !modelDeploymentName || !connectionId || !indexName) {
    throw new Error("Set all environment variables listed in this section");
}

const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```

## Configure the Azure AI Search tool

Using the connection ID of your Azure AI Search service, configure the Azure AI Search tool to use your search index.

```javascript
const azureAISearchTool = ToolUtility.createAzureAISearchTool(connectionId, indexName, {
    queryType: "simple",
    topK: 3,
    filter: "",
});

```

## Create an agent with the Azure AI Search tool enabled

Change the model to the one deployed in your project. You can find the model name on the **Models** tab of the Foundry portal. You can also change the agent's name and instructions to suit your needs.

```javascript

const agent = await client.createAgent(modelDeploymentName, {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [azureAISearchTool.definition],
  toolResources: azureAISearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Ask the agent questions about data in the index

Now that the agent is created, you can ask it questions about the data in your search index.

```javascript
// Create thread for communication
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create message to thread
const message = await client.messages.create(
  thread.id,
  "user",
  "What is the temperature rating of the cozynights sleeping bag?",
);
console.log(`Created message, message ID : ${message.id}`);

// Create and process the agent run in thread with tools
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
  console.log(`Run failed:`, JSON.stringify(run, null, 2));
}
console.log(`Run finished with status: ${run.status}`);

// Fetch run steps to get the details of agent run
const runSteps = await client.runSteps.list(thread.id, run.id);

for await (const step of runSteps) {
  console.log(`Step ID: ${step.id}, Status: ${step.status}`);
  const stepDetails = step.stepDetails;
  if (isOutputOfType(stepDetails, "tool_calls")) {
    const toolCalls = stepDetails.toolCalls;
    for (const toolCall of toolCalls) {
      console.log(`Tool Call ID: ${toolCall.id}, Tool type: ${toolCall.type}`);
      if (isOutputOfType(toolCall, "azure_ai_search")) {
        {
          const azureAISearch = toolCall.azureAISearch;
          if (azureAISearch) {
            console.log(`Azure AI Search Tool Call input: ${azureAISearch.input}`);
            console.log(`Azure AI Search Tool Call output: ${azureAISearch.output}`);
          }
        }
      }
    }
  }
}

// Fetch and log all messages
const messagesIterator = client.messages.list(thread.id);
console.log(`Messages:`);

// Get the first message
for await (const m of messagesIterator) {
  if (m.content.length > 0) {
    const agentMessage = m.content[0];
    if (isOutputOfType(agentMessage, "text")) {
      const textContent = agentMessage;
      console.log(`Text Message Content - ${textContent.text.value}`);
    }
  }
  break; // Just process the first message
}
```

### Expected output

The answer depends on your index. A successful run produces output similar to:

```output
Created agent, agent ID: <agent-id>
Created thread, thread ID: <thread-id>
Created message, message ID: <message-id>
Run finished with status: completed
Text Message Content - <answer grounded in the search index>
```

## Clean up resources

Delete the thread and agent after you verify the response:

```javascript
await client.threads.delete(thread.id);
await client.deleteAgent(agent.id);
console.log("Deleted thread and agent");
```

:::zone-end

:::zone pivot="rest"

+ Complete the [REST API quickstart](../../quickstart.md?pivots=rest-api) to set `AGENT_TOKEN` and `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`.
+ Install [`jq`](https://jqlang.github.io/jq/download/) to create request bodies, capture IDs, and inspect responses.

This classic tool requires the `2025-05-15-preview` API. Set the remaining values for the sample:

```bash
export API_VERSION="2025-05-15-preview"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
export AZURE_AI_SEARCH_CONNECTION_ID="/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource>/projects/<project>/connections/<search-connection>"
export AZURE_AI_SEARCH_INDEX_NAME="<your-index-name>"
```

Get the full connection ID from **Management center** > **Connected resources** in the Foundry portal. The calling identity must have access to the project connection and search index.

## Create an agent

Create an agent with the Azure AI Search tool, and capture its ID from the response:

```bash
AGENT_ID=$(
    jq -n \
        --arg model "$MODEL_DEPLOYMENT_NAME" \
        --arg connection "$AZURE_AI_SEARCH_CONNECTION_ID" \
        --arg index "$AZURE_AI_SEARCH_INDEX_NAME" \
        '{instructions:"Answer only from the search index and cite sources.",
            name:"my-search-agent", model:$model,
            tools:[{type:"azure_ai_search"}],
            tool_resources:{azure_ai_search:{indexes:[{
                index_connection_id:$connection, index_name:$index,
                query_type:"semantic"}]}}}' |
    curl --silent --show-error --fail-with-body --request POST \
        --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION" \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        --data-binary @- |
    jq -r '.id'
)
printf 'Agent ID: %s\n' "$AGENT_ID"
```

## Create a thread and add a question

Create a thread, capture its ID, and add a question that your index can answer:

```bash
THREAD_ID=$(
    curl --silent --show-error --fail-with-body --request POST \
        --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION" \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{}' |
    jq -r '.id'
)

curl --silent --show-error --fail-with-body --request POST \
    --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/$THREAD_ID/messages?api-version=$API_VERSION" \
    -H "Authorization: Bearer $AGENT_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"role":"user","content":"What is the temperature rating of the cozynights sleeping bag?"}' \
    | jq -r '"Message ID: \(.id)"'
```

## Run the agent

Start a run, capture its ID, and poll until the run reaches a terminal state:

```bash
RUN_ID=$(
    jq -n --arg agent "$AGENT_ID" '{assistant_id:$agent}' |
    curl --silent --show-error --fail-with-body --request POST \
        --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/$THREAD_ID/runs?api-version=$API_VERSION" \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        --data-binary @- |
    jq -r '.id'
)

while true; do
    RUN_STATUS=$(curl --silent --show-error --fail-with-body \
        --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/$THREAD_ID/runs/$RUN_ID?api-version=$API_VERSION" \
        -H "Authorization: Bearer $AGENT_TOKEN" | jq -r '.status')
    [[ "$RUN_STATUS" != "queued" && "$RUN_STATUS" != "in_progress" ]] && break
    sleep 1
done
printf 'Run status: %s\n' "$RUN_STATUS"
```

## Verify the response and citations

Retrieve the messages and print the grounded answer followed by its URL citations:

```bash
MESSAGES=$(
    curl --silent --show-error --fail-with-body \
        --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/$THREAD_ID/messages?api-version=$API_VERSION" \
        -H "Authorization: Bearer $AGENT_TOKEN"
)

jq -r '.data[] | select(.role == "assistant") | .content[] |
    select(.type == "text") | "Answer: \(.text.value)",
    (.text.annotations[]? | select(.type == "url_citation") |
    "Citation: [\(.url_citation.title)](\(.url_citation.url))")' \
    <<< "$MESSAGES"
```

Expected output resembles the following example. The answer and citations depend on your index:

```output
Agent ID: <agent-id>
Message ID: <message-id>
Run status: completed
Answer: <answer grounded in the search index>
Citation: [<source title>](<source URL>)
```

## Clean up resources

Delete the thread and agent after you verify the response:

```bash
curl --silent --show-error --fail-with-body --request DELETE \
    --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/$THREAD_ID?api-version=$API_VERSION" \
    -H "Authorization: Bearer $AGENT_TOKEN"

curl --silent --show-error --fail-with-body --request DELETE \
    --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants/$AGENT_ID?api-version=$API_VERSION" \
    -H "Authorization: Bearer $AGENT_TOKEN"
printf 'Deleted thread and agent.\n'
```

:::zone-end

:::zone pivot="java"

## Set environment variables

Set the values that the sample reads at runtime.

```bash
export PROJECT_ENDPOINT="<your-project-endpoint>"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
export AZURE_AI_CONNECTION_ID="<your-search-connection-id>"
export AZURE_AI_SEARCH_INDEX_NAME="<your-index-name>"
```

## Run the Java sample

The sample creates an agent and thread, runs a grounded question, prints the response, and deletes the resources in a `finally` block.

```java
package com.example.agents;

import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.models.AISearchIndexResource;
import com.azure.ai.agents.persistent.models.AzureAISearchToolDefinition;
import com.azure.ai.agents.persistent.models.AzureAISearchToolResource;
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
import com.azure.ai.agents.persistent.models.ToolResources;
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.core.http.rest.PagedIterable;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.util.Arrays;

public class AgentExample {

    public static void main(String[] args) {

        // variables for authenticating requests to the agent service 
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");
        String aiSearchConnectionId = System.getenv("AZURE_AI_CONNECTION_ID");
        String indexName = System.getenv("AZURE_AI_SEARCH_INDEX_NAME");
        
        PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder().endpoint(projectEndpoint)
            .credential(new DefaultAzureCredentialBuilder().build());
        PersistentAgentsClient agentsClient = clientBuilder.buildClient();
        PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
        ThreadsClient threadsClient = agentsClient.getThreadsClient();
        MessagesClient messagesClient = agentsClient.getMessagesClient();
        RunsClient runsClient = agentsClient.getRunsClient();

        AISearchIndexResource indexResource = new AISearchIndexResource()
            .setIndexConnectionId(aiSearchConnectionId)
            .setIndexName(indexName);
        ToolResources toolResources = new ToolResources()
            .setAzureAISearch(new AzureAISearchToolResource()
                .setIndexList(Arrays.asList(indexResource)));

        String agentName = "ai_search_example";
        CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName)
            .setName(agentName)
            .setInstructions("You are a helpful agent")
            .setTools(Arrays.asList(new AzureAISearchToolDefinition()))
            .setToolResources(toolResources);
        PersistentAgent agent = administrationClient.createAgent(createAgentOptions);
        System.out.printf("Created agent, ID: %s%n", agent.getId());

        PersistentAgentThread thread = threadsClient.createThread();
        System.out.printf("Created thread, ID: %s%n", thread.getId());
        ThreadMessage createdMessage = messagesClient.createMessage(
            thread.getId(),
            MessageRole.USER,
            "<question about information in search index>");
        System.out.printf("Created message, ID: %s%n", createdMessage.getId());

        try {
            //run agent
            CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
                .setAdditionalInstructions("");
            ThreadRun threadRun = runsClient.createRun(createRunOptions);

            threadRun = waitForRunCompletion(thread.getId(), threadRun, runsClient);
            System.out.printf("Run finished with status: %s, ID: %s%n",
                threadRun.getStatus(), threadRun.getId());
            printRunMessages(messagesClient, thread.getId());

        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            //cleanup
            threadsClient.deleteThread(thread.getId());
            administrationClient.deleteAgent(agent.getId());
            System.out.println("Deleted thread and agent");
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
    public static ThreadRun waitForRunCompletion(
        String threadId, ThreadRun threadRun, RunsClient runsClient)
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
        return threadRun;
    }
}
```

### Expected output

The answer depends on your index. A successful run produces output similar to:

```output
Created agent, ID: <agent-id>
Created thread, ID: <thread-id>
Created message, ID: <message-id>
Run finished with status: COMPLETED, ID: <run-id>
<timestamp> - AGENT : <answer grounded in the search index>
Deleted thread and agent
```
:::zone-end
