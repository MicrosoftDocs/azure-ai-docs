---
title: 'How to use the deep research tool'
titleSuffix: Microsoft Foundry
description: Find code samples and instructions for using deep research in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/20/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: references_regions
zone_pivot_groups: selection-deep-research
---

# How to use the Deep Research tool

> [!NOTE]
> * The **parent** Foundry project resource and the contained  `o3-deep-research` model and GPT models **must exist** in the same Azure subscription and region. Supported regions are **West US** and **Norway East**.
> * This tool is only available in `2025-05-15-preview` API. We highly recommend that you migrate to use the `2025-11-15-preview` API. This enables you to use the `o3-deep-research` model with [web search](../../../default/agents/how-to/tools/web-search.md) or MCP tool.

Use this article to learn how to use the Deep Research tool with the Azure AI Projects SDK, including code examples and setup instructions.

## Prerequisites

* The requirements in the [Deep Research overview](./deep-research.md).
* Your Microsoft Foundry Project endpoint.

    
    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`.

* The deployment names of your `o3-deep-research-model` and `gpt-4o` models. You can find them in **Models + Endpoints** in the left navigation menu.

   :::image type="content" source="../../media/tools/deep-research/model-deployments.png" alt-text="A screenshot showing the model deployment screen the Foundry portal." lightbox="../../media/tools/deep-research/model-deployments.png":::
    
    Save the name of your `o3-deep-research` deployment name as an environment variable named `DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME` and the `gpt-4o` deployment name as an environment variable named `MODEL_DEPLOYMENT_NAME`.

> [!NOTE]
> Other GPT-series models including GPT-4o-mini and the GPT-4.1 series are not supported for scope clarification.

:::zone pivot="csharp"

* The connection ID for your Grounding with Bing Search resource. You can find it in the Foundry portal by selecting **Management center** from the left navigation menu. Then selecting **Connected resources**. Then select your bing resource.
    
    :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Grounding with Bing Search resource name. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::

    Copy the ID, and save it to an environment variable named `AZURE_BING_CONECTION_ID`. 

    :::image type="content" source="../../media/tools/deep-research/bing-id.png" alt-text="A screenshot showing the Grounding with Bing Search ID. " lightbox="../../media/tools/deep-research/bing-id.png":::

## Create an agent with the Deep Research tool

>[!NOTE]
> You need version `1.1.0-beta.4` or later of the `Azure.AI.Agents.Persistent` package, and the `Azure.Identity` package.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using System.Collections.Generic;
using System.Text;

var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var deepResearchModelDeploymentName = System.Environment.GetEnvironmentVariable("DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME");
var connectionId = System.Environment.GetEnvironmentVariable("AZURE_BING_CONECTION_ID");
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

// DeepResearchToolDefinition should be initialized with the name of deep research model and the Bing connection ID,
// needed to perform the search in the internet.

DeepResearchToolDefinition deepResearch = new(
    new DeepResearchDetails(
        model: deepResearchModelDeploymentName,
        bingGroundingConnections: [
            new DeepResearchBingGroundingConnection(connectionId)
        ]
    )
);

// NOTE: To reuse existing agent, fetch it with get_agent(agent_id)
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "Science Tutor",
    instructions: "You are a helpful Agent that assists in researching scientific topics.",
    tools: [deepResearch]
);

//Create a thread and run and wait for the run to complete.

PersistentAgentThreadCreationOptions threadOp = new();
threadOp.Messages.Add(new ThreadMessageOptions(
        role: MessageRole.User,
        content: "Research the current state of studies on orca intelligence and orca language, " +
        "including what is currently known about orcas' cognitive capabilities, " +
        "communication systems and problem-solving reflected in recent publications in top their scientific" +
        "journals like Science, Nature and PNAS."
    ));
ThreadAndRunOptions opts = new()
{
    ThreadOptions = threadOp,
};
ThreadRun run = client.CreateThreadAndRun(
    assistantId: agent.Id,
    options: opts
);

Console.WriteLine("Start processing the message... this may take a few minutes to finish. Be patient!");
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(run.ThreadId, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

// We will create a helper function PrintMessagesAndSaveSummary, which prints the response from the agent,
// and replaces the reference placeholders by links in Markdown format.
// It also saves the research summary in the file for convenience.

static void PrintMessagesAndSaveSummary(IEnumerable<PersistentThreadMessage> messages, string summaryFilePath)
{
    string lastAgentMessage = default;
    foreach (PersistentThreadMessage threadMessage in messages)
    {
        StringBuilder sbAgentMessage = new();
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
                        if (annotation is MessageTextUriCitationAnnotation uriAnnotation)
                        {
                            response = response.Replace(uriAnnotation.Text, $" [{uriAnnotation.UriCitation.Title}]({uriAnnotation.UriCitation.Uri})");
                        }
                    }
                }
                if (threadMessage.Role == MessageRole.Agent)
                    sbAgentMessage.Append(response);
                Console.Write($"Agent response: {response}");
            }
            else if (contentItem is MessageImageFileContent imageFileItem)
            {
                Console.Write($"<image from ID: {imageFileItem.FileId}");
            }
            Console.WriteLine();
        }
        if (threadMessage.Role == MessageRole.Agent)
            lastAgentMessage = sbAgentMessage.ToString();
    }
    if (!string.IsNullOrEmpty(lastAgentMessage))
    {
        File.WriteAllText(
            path: summaryFilePath,
            contents: lastAgentMessage);
    }
}

//List the messages, print them and save the result in research_summary.md file.
//The file will be saved next to the compiled executable.

Pageable<PersistentThreadMessage> messages
    = client.Messages.GetMessages(
        threadId: run.ThreadId, order: ListSortOrder.Ascending);
PrintMessagesAndSaveSummary([.. messages], "research_summary.md");

// NOTE: Comment out these two lines if you want to delete the agent.
client.Threads.DeleteThread(threadId: run.ThreadId);
client.Administration.DeleteAgent(agentId: agent.Id);
```

:::zone-end 

:::zone pivot="typescript"

* The name of your Grounding with Bing Search resource name. You can find it in the Foundry portal by selecting **Management center** from the left navigation menu. Select **Connected resources**, then select your Grounding with Bing Search resource.
    
    :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Grounding with Bing Search resource name. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::


    Copy the ID, and save it to an environment variable named `AZURE_BING_CONECTION_ID`. 

    :::image type="content" source="../../media/tools/deep-research/bing-id.png" alt-text="A screenshot showing the Grounding with Bing Search resource ID. " lightbox="../../media/tools/deep-research/bing-id.png":::

    Save this endpoint to an environment variable named `BING_RESOURCE_NAME`. 

## Create an agent with the Deep Research tool

> [!NOTE]
> You need the latest preview version of the `@azure/ai-projects` package.

```typescript
import type {
  MessageTextContent,
  ThreadMessage,
  DeepResearchToolDefinition,
  MessageTextUrlCitationAnnotation,
} from "@azure/ai-agents";
import { AgentsClient, isOutputOfType } from "@azure/ai-agents";
import { DefaultAzureCredential } from "@azure/identity";

import "dotenv/config";

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project endpoint>";
const modelDeploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "gpt-4o";
const deepResearchModelDeploymentName =
  process.env["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"];
const bingConnectionId = process.env["AZURE_BING_CONNECTION_ID"] || "<connection-id>";

/**
 * Fetches and prints new agent response from the thread
 * @param threadId - The thread ID
 * @param client - The AgentsClient instance
 * @param lastMessageId - The ID of the last message processed
 * @returns The ID of the newest message, or undefined if no new message
 */
async function fetchAndPrintNewAgentResponse(
  threadId: string,
  client: AgentsClient,
  lastMessageId?: string,
): Promise<string | undefined> {
  const messages = client.messages.list(threadId);
  let latestMessage: ThreadMessage | undefined;
  for await (const msg of messages) {
    if (msg.role === "assistant") {
      latestMessage = msg;
      break;
    }
  }

  if (!latestMessage || latestMessage.id === lastMessageId) {
    return lastMessageId;
  }

  console.log("\nAgent response:");

  // Print text content
  for (const content of latestMessage.content) {
    if (isOutputOfType<MessageTextContent>(content, "text")) {
      console.log(content.text.value);
    }
  }

  const urlCitations = getUrlCitationsFromMessage(latestMessage);
  if (urlCitations.length > 0) {
    console.log("\nURL Citations:");
    for (const citation of urlCitations) {
      console.log(`URL Citations: [${citation.title}](${citation.url})`);
    }
  }

  return latestMessage.id;
}

/**
 * Extracts URL citations from a thread message
 * @param message - The thread message
 * @returns Array of URL citations
 */
function getUrlCitationsFromMessage(message: ThreadMessage): Array<{ title: string; url: string }> {
  const citations: Array<{ title: string; url: string }> = [];

  for (const content of message.content) {
    if (isOutputOfType<MessageTextContent>(content, "text")) {
      for (const annotation of content.text.annotations) {
        if (isOutputOfType<MessageTextUrlCitationAnnotation>(annotation, "url_citation")) {
          citations.push({
            title: annotation.urlCitation.title || annotation.urlCitation.url,
            url: annotation.urlCitation.url,
          });
        }
      }
    }
  }

  return citations;
}

/**
 * Creates a research summary from the final message
 * @param message - The thread message containing the research results
 * @param filepath - The file path to write the summary to
 */
function createResearchSummary(message: ThreadMessage): void {
  if (!message) {
    console.log("No message content provided, cannot create research summary.");
    return;
  }

  let content = "";

  // Write text summary
  const textSummaries: string[] = [];
  for (const contentItem of message.content) {
    if (isOutputOfType<MessageTextContent>(contentItem, "text")) {
      textSummaries.push(contentItem.text.value.trim());
    }
  }
  content += textSummaries.join("\n\n");

  // Write unique URL citations, if present
  const urlCitations = getUrlCitationsFromMessage(message);
  if (urlCitations.length > 0) {
    content += "\n\n## References\n";
    const seenUrls = new Set<string>();
    for (const citation of urlCitations) {
      if (!seenUrls.has(citation.url)) {
        content += `- [${citation.title}](${citation.url})\n`;
        seenUrls.add(citation.url);
      }
    }
  }

  // writeFileSync(filepath, content, "utf-8");
  console.log(`Research summary created:\n${content}`);
  // console.log(`Research summary written to '${filepath}'.`);
}

export async function main(): Promise<void> {
  // Create an Azure AI Client
  const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());

  // Create Deep Research tool definition
  const deepResearchTool: DeepResearchToolDefinition = {
    type: "deep_research",
    deepResearch: {
      deepResearchModel: deepResearchModelDeploymentName,
      deepResearchBingGroundingConnections: [
        {
          connectionId: bingConnectionId,
        },
      ],
    },
  };

  // Create agent with the Deep Research tool
  const agent = await client.createAgent(modelDeploymentName, {
    name: "my-agent",
    instructions: "You are a helpful Agent that assists in researching scientific topics.",
    tools: [deepResearchTool],
  });
  console.log(`Created agent, ID: ${agent.id}`);

  // Create thread for communication
  const thread = await client.threads.create();
  console.log(`Created thread, ID: ${thread.id}`);

  // Create message to thread
  const message = await client.messages.create(
    thread.id,
    "user",
    "Research the current scientific understanding of orca intelligence and communication, focusing on recent (preferably past 5 years) peer-reviewed studies, comparisons with other intelligent species such as dolphins or primates, specific cognitive abilities like problem-solving and social learning, and detailed analyses of vocal and non-vocal communication systems—please include notable authors or landmark papers if applicable.",
  );
  console.log(`Created message, ID: ${message.id}`);

  console.log("Start processing the message... this may take a few minutes to finish. Be patient!");

  // Create and poll the run
  const run = await client.runs.create(thread.id, agent.id);
  let lastMessageId: string | undefined;

  // Poll the run status
  let currentRun = run;
  while (currentRun.status === "queued" || currentRun.status === "in_progress") {
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second
    currentRun = await client.runs.get(thread.id, run.id);

    lastMessageId = await fetchAndPrintNewAgentResponse(thread.id, client, lastMessageId);
    console.log(`Run status: ${currentRun.status}`);
  }

  console.log(`Run finished with status: ${currentRun.status}, ID: ${currentRun.id}`);

  if (currentRun.status === "failed") {
    console.log(`Run failed: ${currentRun.lastError}`);
  }

  // Fetch the final message from the agent and create a research summary
  const messages = client.messages.list(thread.id, { order: "desc", limit: 10 });
  let finalMessage: ThreadMessage | undefined;

  for await (const msg of messages) {
    if (msg.role === "assistant") {
      finalMessage = msg;
      break;
    }
  }

  if (finalMessage) {
    createResearchSummary(finalMessage);
  }

  // Clean-up and delete the agent once the run is finished
  await client.deleteAgent(agent.id);
  console.log("Deleted agent");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

:::zone-end 

:::zone pivot="python"

* The name of your Grounding with Bing Search resource name. You can find it in the Foundry portal by selecting **Management center** from the left navigation menu. Then select **Connected resources**.
    
    :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Grounding with Bing Search resource name. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::

    Save this endpoint to an environment variable named `BING_RESOURCE_NAME`. 

## Create an agent with the Deep Research tool

The Deep Research tool requires the latest prerelease versions of the `azure-ai-projects` library. First we recommend creating a [virtual environment](https://docs.python.org/3/library/venv.html) to work in:

```console
python -m venv env
# after creating the virtual environment, activate it with:
.\env\Scripts\activate
```

You can install the package with the following command:

```console
pip install --pre azure-ai-projects
```


```python
import os, time
from typing import Optional
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage


def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
) -> Optional[str]:
    response = agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )
    if not response or response.id == last_message_id:
        return last_message_id  # No new content

    print("\nAgent response:")
    print("\n".join(t.text.value for t in response.text_messages))

    for ann in response.url_citation_annotations:
        print(f"URL Citation: [{ann.url_citation.title}]({ann.url_citation.url})")

    return response.id


def create_research_summary(
        message : ThreadMessage,
        filepath: str = "research_summary.md"
) -> None:
    if not message:
        print("No message content provided, cannot create research summary.")
        return

    with open(filepath, "w", encoding="utf-8") as fp:
        # Write text summary
        text_summary = "\n\n".join([t.text.value.strip() for t in message.text_messages])
        fp.write(text_summary)

        # Write unique URL citations, if present
        if message.url_citation_annotations:
            fp.write("\n\n## References\n")
            seen_urls = set()
            for ann in message.url_citation_annotations:
                url = ann.url_citation.url
                title = ann.url_citation.title or url
                if url not in seen_urls:
                    fp.write(f"- [{title}]({url})\n")
                    seen_urls.add(url)

    print(f"Research summary written to '{filepath}'.")


project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

conn_id = project_client.connections.get(name=os.environ["BING_RESOURCE_NAME"]).id


# Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
deep_research_tool = DeepResearchTool(
    bing_grounding_connection_id=conn_id,
    deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
)

# Create Agent with the Deep Research tool and process Agent run
agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Create a new agent that has the Deep Research tool attached.
# NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
# update the agent with the Deep Research tool.
agent = agents_client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful Agent that assists in researching scientific topics.",
    tools=deep_research_tool.definitions,
)

# agent = agent_poller.result()  # Wait for completion


# [END create_agent_with_deep_research_tool]
print(f"Created agent, ID: {agent.id}")

# Create thread for communication
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=(
        "Assess the UK outlook for 2026 - economic growth and inflation, based on IMF sources and provide a detailed report."
    ),
)
print(f"Created message, ID: {message.id}")

print(f"Start processing the message... this may take a few minutes to finish. Be patient!")
# Poll the run as long as run status is queued or in progress
run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
last_message_id = None
while run.status in ("queued", "in_progress"):
    time.sleep(1)
    run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)

    last_message_id = fetch_and_print_new_agent_response(
        thread_id=thread.id,
        agents_client=agents_client,
        last_message_id=last_message_id,
    )
    print(f"Run status: {run.status}")

print(f"Run finished with status: {run.status}, ID: {run.id}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch the final message from the agent in the thread and create a research summary
final_message = agents_client.messages.get_last_message_by_role(
    thread_id=thread.id, role=MessageRole.AGENT
)
if final_message:
    create_research_summary(final_message)

# Clean-up and delete the agent once the run is finished.
# NOTE: Comment out this line if you plan to reuse the agent later.
agents_client.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end 

> [!NOTE]
> * Limitation: The Deep Research tool is currently recommended only in nonstreaming scenarios. Using it with streaming can work, but it might occasionally time out and is therefore not recommended.
> * Currently, Foundry Agent Playground UI only supports starting runs in streaming mode, and as a result, users might experience connection drops and timeouts. Use the supported methods above which uses runs in non-streaming mode.

## Next steps

* [Reference documentation](https://aka.ms/azsdk/azure-ai-projects/python/reference)
* [Asynchronous sample on GitHub](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_async/sample_agents_deep_research_async.py) 
* [Library source code](https://aka.ms/azsdk/azure-ai-projects/python/code) 
* [Package (PyPi)](https://aka.ms/azsdk/azure-ai-projects/python/package) 
