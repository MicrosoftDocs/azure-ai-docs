---
title: 'How to use the deep research tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for using deep research in the Azure AI Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 07/10/2025
author: aahill
ms.author: aahi
---

# How to use the Deep Research tool

Use this article to learn how to use the Deep Research tool with the Azure AI Projects SDK, including code examples and setup instructions.

## Prerequisites

> [!NOTE]
> * The Agents service and SDK use the Azure OpenAI `o3-deep-research` model. This model is not accessible from Azure OpenAI Chat Completions and Responses APIs.
> * The  `o3-deep-research` model and the GPT model deployments should be part of your AI Foundry project resulting in all three resources in the same Azure subscription and same region. Supported regions are **West US** and **Norway East**.

* The requirements in the [Deep Research overview](./deep-research.md).
* The Deep Research tool requires the latest prerelease versions of the `azure-ai-projects` library. You can install it with the following command:

    ```console
    pip install --pre azure-ai-projects
    ```

* Your Azure AI Foundry Project endpoint.

    You can find your endpoint in the main project **overview** for your project in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs), under **Endpoint and keys** > **Libraries** > **Azure AI Foundry**.

    :::image type="content" source="../../media/quickstart/portal-endpoint-string.png" alt-text="A screenshot showing the endpoint in the Azure AI Foundry portal." lightbox="../../media/quickstart/portal-endpoint-string.png":::

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`. 

* The name of your Grounding with Bing Search resource name. You can find it in the Azure AI Foundry portal by selecting **Management center** from the left navigation menu. Then selecting **Connected resources**.
    
    :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Grounding with Bing Search resource name. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::

    Save this endpoint to an environment variable named `BING_RESOURCE_NAME`. 

* The names of your `o3-deep-research-model` deployment name and Azure OpenAI GPT model deployment name. You can find them in **Models + Endpoints** in the left navigation menu. 

    :::image type="content" source="../../media/tools/deep-research/model-deployments.png" alt-text="A screenshot showing the model deployment screen the AI Foundry portal." lightbox="../../media/tools/deep-research/model-deployments.png":::
    
    Save the name of your `o3-deep-research-model` deployment name as an environment variable named `DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME` and Azure OpenAI GPT model deployment name as an environment variable named `MODEL_DEPLOYMENT_NAME`. 

> [!NOTE]
> Limitation: The Deep Research tool is currently recommended only in nonstreaming scenarios. Using it with streaming can work, but it might occasionally time out and is therefore not recommended.

## Create an agent with the Deep Research tool

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
with project_client:

    with project_client.agents as agents_client:

        # Create a new agent that has the Deep Research tool attached.
        # NOTE: To add Deep Research to an existing agent, fetch it with `get_agent(agent_id)` and then,
        # update the agent with the Deep Research tool.
        agent = agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-agent",
            instructions="You are a helpful Agent that assists in researching scientific topics.",
            tools=deep_research_tool.definitions,
        )

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
                "Give me the latest research into quantum computing over the last year."
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

## Next steps

* [Reference documentation](https://aka.ms/azsdk/azure-ai-projects/python/reference)
* [Asynchronous sample on GitHub](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_async/sample_agents_deep_research_async.py) 
* [Library source code](https://aka.ms/azsdk/azure-ai-projects/python/code) 
* [Package (PyPi)](https://aka.ms/azsdk/azure-ai-projects/python/package) 
