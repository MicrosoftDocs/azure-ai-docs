---
title: "Use Custom Bing Search with classic Foundry agents"
description: "Learn how to ground classic Foundry agents with Custom Bing Search results by using supported SDK and REST API samples and configurations."
ai-usage: ai-assisted
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
manager: mcleans
ms.date: 08/05/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.custom:
- azure-ai-agents
- build-2025
- doc-kit-assisted
zone_pivot_groups: selection-bing-custom-grounding
---

# How to use Grounding with Bing Custom Search (preview) (classic)

> [!NOTE]
> This document refers to the Microsoft Foundry (classic) agents.
>
> 🔍 [View the new Grounding with Bing Search documentation](../../../../foundry/agents/how-to/tools/bing-tools.md).
> Agents (classic) are deprecated and retire on March 31, 2027. Use the new agents in the generally available [Foundry Agent Service](../../../../foundry/agents/overview.md). Follow the [migration guide](../../../../foundry/agents/how-to/migrate.md) to update your workloads.

This article provides step-by-step instructions and code samples for using the Grounding with Bing Custom Search tool in the Foundry Agent Service.

## Prerequisites

- A Grounding with Bing Custom Search resource and configuration. Creating the resource requires the **Contributor** role scoped to the resource group where you create it. Activate this role only for provisioning, preferably through Microsoft Entra Privileged Identity Management (PIM) for Azure resources, and deactivate it after you create the resource and configuration.
- The `2025-05-15-preview` Agent Service API.
- Sign in locally with `az login` so `DefaultAzureCredential` can authenticate.
- For Python 3.9 or later, install `pip install --pre "azure-ai-projects==1.1.0b4" "azure-ai-agents==1.2.0b6" azure-identity`.
- For REST, install [`jq`](https://jqlang.github.io/jq/download/) to create request bodies, capture IDs, and inspect responses.
- Don't use `azure-ai-projects` 2.x with these classic threads-and-runs samples.
- For the Python samples, collect these values:
    - Your Foundry Project endpoint. In the Foundry portal, open your project's **Overview** page, and then select **Libraries** > **Foundry**. Save the endpoint to an environment variable named `PROJECT_ENDPOINT`.
    - The name of your Grounding with Bing Custom Search resource. In the Foundry portal, select **Management center** > **Connected resources**, and save the resource name to an environment variable named `BING_CUSTOM_CONNECTION_NAME`.
    - The name of your Grounding with Bing Custom Search configuration, which contains the URLs you want to allow or disallow. In the [Azure portal](https://portal.azure.com/), open the overview page for your resource, select **Configurations**, and then select your configuration. Save the configuration name to an environment variable named `BING_CUSTOM_INSTANCE_NAME`.
    - Your model deployment name. In the Foundry portal, select **Models + Endpoints**, and save the deployment name to an environment variable named `MODEL_DEPLOYMENT_NAME`.

Grounding with Bing Custom Search incurs separate charges, requires publicly indexed content, and sends queries outside the Azure compliance boundary. Private endpoints and VPN routing don't apply to Bing traffic. Display returned citations without altering their URLs.

::: zone pivot="portal"
1. Go to the **Agents** screen for your agent in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). Scroll down the Setup pane on the right to **knowledge**. Then select **Add**.

1. Select the **Grounding with Bing Custom Search** tool.  

1. Select to create a new connection or use an existing connection. 

    1. For a new connection, select your Grounding with Bing Custom Search resource. 

1. After you connect to a resource, select the configuration name. 

1. Save the tool and start chatting with your agent. 

:::zone-end

::: zone pivot="python"
## Create a project client

Create a client object that holds the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingCustomSearchTool

# Create an Azure AI Client from an endpoint, copied from your Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)
```

## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent.

```python
bing_custom_connection = project_client.connections.get(name=os.environ["BING_CUSTOM_CONNECTION_NAME"])
conn_id = bing_custom_connection.id

print(conn_id)

configuration_name = os.environ["BING_CUSTOM_INSTANCE_NAME"]
# Initialize Bing Custom Search tool with connection id and configuration name
bing_custom_tool = BingCustomSearchTool(connection_id=conn_id, instance_name=configuration_name)

# Keep the client open until the final cleanup step.
agents_client = project_client.agents
agent = agents_client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful agent",
    tools=bing_custom_tool.definitions,
)
print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create thread for communication
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content="How many medals did the USA win in the 2024 summer olympics?",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

```python
# Create and process Agent run in thread with tools
run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = agents_client.messages.list(thread_id=thread.id)
for msg in messages:
    if msg.text_messages:
        for text_message in msg.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in msg.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")

agents_client.threads.delete(thread.id)
agents_client.delete_agent(agent.id)
project_client.close()
print("Deleted thread and agent, and closed the project client")
```

### Expected output

The response text depends on your custom search domains. A successful run ends with output similar to:

```output
Run finished with status: RunStatus.COMPLETED
Agent response: <grounded answer>
URL Citation: [<source title>](<source URL>)
Deleted thread and agent, and closed the project client
```

### Understand URL citations in the response

When the agent response includes URL citations, you can show them to users as a list of references.

In the Python SDK, you can find the answer text in `msg.text_messages[*].text.value`. You can find the citations in `msg.url_citation_annotations[*].url_citation`.
:::zone-end

<!--
::: zone pivot="csharp"

## Create a project client

Create a client object that holds the connection string for connecting to your AI project and other resources.

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.TestFramework;
using NUnit.Framework;

var connectionString = System.Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var bingConnectionName = System.Environment.GetEnvironmentVariable("BING_CONNECTION_NAME");

var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

AgentsClient agentClient = projectClient.GetAgentsClient();
```

## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

```csharp
AgentsClient agentClient = projectClient.GetAgentsClient();
ConnectionResponse bingConnection = await projectClient.GetConnectionsClient().GetConnectionAsync(bingConnectionName);
var connectionId = bingConnection.Id;
var instanceName = "<your_config_instance_name>";

SearchConfigurationList searchConfigurationList = new SearchConfigurationList(
    new List<SearchConfiguration>
    {
        new SearchConfiguration(connectionId, instanceName)
    });

BingCustomSearchToolDefinition bingGroundingTool = new(searchConfigurationList);
Agent agent = await agentClient.CreateAgentAsync(
    model: modelDeploymentName,
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: [ bingGroundingTool ]);
```

## Create a thread

```csharp
AgentThread thread = agentClient.CreateThread();

// Create message to thread
ThreadMessage message = agentClient.CreateMessage(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

```csharp

// Run the agent
ThreadRun run = agentClient.CreateRun(thread, agent);
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = agentClient.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

Assert.AreEqual(
    RunStatus.Completed,
    run.Status,
    run.LastError?.Message);

PageableList<ThreadMessage> messages = agentClient.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (ThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            string response = textItem.Text;
            if (textItem.Annotations != null)
            {
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUrlCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UrlCitation.Title}]({urlAnnotation.UrlCitation.Url})");
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

agentClient.DeleteThread(threadId: thread.Id);
agentClient.DeleteAgent(agentId: agent.Id);
```

:::zone-end
-->

::: zone pivot="rest"

>[!IMPORTANT]
> * This REST API enables developers to invoke the Grounding with Bing Custom Search tool through the Agent Service. It doesn't send calls to the Grounding with Bing Custom Search API directly.
> * Your connection ID should be in this format: `/subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-bing-connection-name>`.

Complete the [REST API quickstart](../../quickstart.md?pivots=rest-api) to set `AGENT_TOKEN` and `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`. Then set the classic preview version and tool values:

```bash
export API_VERSION="2025-05-15-preview"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
export BING_CUSTOM_CONNECTION_ID="/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource>/projects/<project>/connections/<bing-connection>"
export BING_CUSTOM_INSTANCE_NAME="<your-custom-search-configuration-name>"
```

## Create an agent

Create an agent with the Grounding with Bing Custom Search tool, and capture its ID:

```bash
AGENT_ID=$(
    jq -n \
        --arg model "$MODEL_DEPLOYMENT_NAME" \
        --arg connection "$BING_CUSTOM_CONNECTION_ID" \
        --arg instance "$BING_CUSTOM_INSTANCE_NAME" \
        '{instructions:"Answer with citations from the configured domains.",
            name:"my-custom-search-agent", model:$model,
            tools:[{type:"bing_custom_search", bing_custom_search:{
                search_configurations:[{connection_id:$connection,
                    instance_name:$instance, count:7, market:"en-US",
                    set_lang:"en"}]}}]}' |
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
    --data '{"role":"user","content":"<ask a question answered by your configured domains>"}' \
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

Retrieve the assistant message and print its answer and citations:

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

Expected output resembles the following example. The answer and citations depend on your configured domains:

```output
Agent ID: <agent-id>
Message ID: <message-id>
Run status: completed
Answer: <grounded answer>
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

::: zone-end

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `ImportError` for `BingCustomSearchTool` | Install the preview package versions listed in [Prerequisites](#prerequisites). Current `azure-ai-projects` 2.x doesn't expose the classic threads-and-runs API used here. |
| The run fails with a connection error | Confirm the project connection ID and custom search configuration name, and verify the Bing resource is available to the project. |
| The run completes without citations | Confirm your allowed domains are publicly indexed by Bing and contain results relevant to the question. |
| Requests time out from a secured network | Allow public outbound Bing traffic. VPN and private endpoint routing don't carry Bing requests. |

## Related content

- [Ground agents with Bing Search tools](../../../../foundry/agents/how-to/tools/bing-tools.md)
- [Migrate classic agents](../../../../foundry/agents/how-to/migrate.md)
