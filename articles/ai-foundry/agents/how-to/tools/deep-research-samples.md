---
title: 'How to use the deep research tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for using deep research in the Azure AI Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 06/26/2025
author: aahill
ms.author: aahi
---

# How to use Deep Research
Use this article to find step-by-step instructions and code samples for the Deep Research tool.

## Prerequisites

* The requirements in the [Deep Research overview](./deep-research.md)

> [!NOTE]
> Limitation: The Deep Research tool is currently recommended only in non-streaming scenarios. Using it with streaming can work, but it may occasionally time-out and is therefore not recommended.

## Create a function to get and print an agent response

```python
import asyncio
import os
from typing import Optional

from azure.ai.projects.aio import AIProjectClient
from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import DeepResearchTool, MessageRole, ThreadMessage
from azure.identity.aio import DefaultAzureCredential

async def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
) -> Optional[str]:
    response = await agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )

    if not response or response.id == last_message_id:
        return last_message_id

    print("\nAgent response:")
    print("\n".join(t.text.value for t in response.text_messages))

    # Print citation annotations (if any)
    for ann in response.url_citation_annotations:
        print(f"URL Citation: [{ann.url_citation.title}]({ann.url_citation.url})")

    return response.id
```

## Create a function to create a research summary

```python
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
```



## Create a project client and initialize the Deep Research tool
Create a client object, which will contain the endpoint for connecting to your AI project and other resources. 

```python
async def main() -> None:

    project_client = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    # Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
    deep_research_tool = DeepResearchTool(
        bing_grounding_connection_id=os.environ["AZURE_BING_CONNECTION_ID"],
        deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
    )

```

## Create an agent 

To make the Deep Research tool available to your agent, use the `tools` paramter to initialize it and attach it to the agent. You can find your connection in the connected resources section of your project in the Azure AI Foundry portal. You also need to specify the deployment name of your Deep Research model.

```python
async with project_client:

        agents_client = project_client.agents

        # Create a new agent that has the Deep Research tool attached.
        # NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
        # update the agent with the Deep Research tool.
        agent = await agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-agent",
            instructions="You are a helpful Agent that assists in researching scientific topics.",
            tools=deep_research_tool.definitions,
        )
        print(f"Created agent, ID: {agent.id}")
```

## Create a thread

Create a thread and attach a message to it

```python
 # Create thread for communication
thread = await agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = await agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=(
        "Research the current state of studies on orca intelligence and orca language, including what is currently known about orcas' cognitive capabilities and communication systems."
    ),
)
print(f"Created message, ID: {message.id}")

```

## Create a run and check the output

Create a run and observe the response to the question.

> [!NOTE]
> According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/bing/apis/grounding-legal#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. See the [Grounding with Bing Search documentation](./bing-grounding.md#how-to-display-grounding-with-bing-search-results) for more information.

```python
print("Start processing the message... this may take a few minutes to finish. Be patient!")
# Poll the run as long as run status is queued or in progress
run = await agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
last_message_id: Optional[str] = None
while run.status in ("queued", "in_progress"):
    await asyncio.sleep(1)
    run = await agents_client.runs.get(thread_id=thread.id, run_id=run.id)

    last_message_id = await fetch_and_print_new_agent_response(
        thread_id=thread.id,
        agents_client=agents_client,
        last_message_id=last_message_id,
    )
    print(f"Run status: {run.status}")

print(f"Run finished with status: {run.status}, ID: {run.id}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch the final message from the agent in the thread and create a research summary
final_message = await agents_client.messages.get_last_message_by_role(
    thread_id=thread.id, role=MessageRole.AGENT
)
if final_message:
    create_research_summary(final_message)

# Clean-up and delete the agent once the run is finished.
# NOTE: Comment out this line if you plan to reuse the agent later.
await agents_client.delete_agent(agent.id)
print("Deleted agent")


if __name__ == "__main__":
    asyncio.run(main())
```

## Delete the agent (optional)

if you decide you don't need your agent, you can delete with:

```python
agents_client.delete_agent(agent.id)
print("Deleted agent")
```

## Next steps

* [Reference documentation](https://aka.ms/azsdk/azure-ai-projects/python/reference)
* [Sample on Github](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_async/sample_agents_deep_research_async.py) 
* [Library source code](https://aka.ms/azsdk/azure-ai-projects/python/code) 
* [Package (PyPi)](https://aka.ms/azsdk/azure-ai-projects/python/package) |
