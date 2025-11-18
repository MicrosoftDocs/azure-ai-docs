---
title: 'How to use Code Interpreter for the Microsoft Foundry agents'
titleSuffix: Microsoft Foundry
description: Learn how to use Microsoft Foundry Agent Service Code Interpreter for the agents API
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/13/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents, references_regions
---
# Code Interpreter tool for agents

Use this article to learn how to use the Code Interpreter tool for agents.

Code Interpreter allows the agents to write and run Python code in a sandboxed execution environment. With Code Interpreter enabled, your agent can run code iteratively to solve more challenging code, math, and data analysis problems or create graphs and charts. When your Agent writes code that fails to run, it can iterate on this code by modifying and running different code until the code execution succeeds.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your Agent calls Code Interpreter simultaneously in two different threads, two code interpreter sessions are created. Each session is active by default for 1 hour with an idle timeout of 30 minutes.

## Prerequisites

- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

> [!NOTE]
> The code interpreter tool is not available in [some regions](#regional-restrictions).

## Code samples

> [!NOTE]
> You will need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

```python
import os
import httpx
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool, CodeInterpreterToolAuto

load_dotenv()

# Load the CSV file to be processed
asset_file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../assets/synthetic_500_quarterly_results.csv")
)

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with project_client:
    openai_client = project_client.get_openai_client()

    # Upload the CSV file for the code interpreter to use
    file = openai_client.files.create(purpose="assistants", file=open(asset_file_path, "rb"))
    print(f"File uploaded (id: {file.id})")

    # Create agent with code interpreter tool
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[CodeInterpreterTool(container=CodeInterpreterToolAuto(file_ids=[file.id]))],
        ),
        description="Code interpreter agent for data analysis and visualization.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Create a conversation for the agent interaction
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send request to create a chart and generate a file
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response completed (id: {response.id})")

    # Extract file information from response annotations
    file_id = ""
    filename = ""
    container_id = ""

    # Get the last message which should contain file citations
    last_message = response.output[-1]  # ResponseOutputMessage
    if last_message.type == "message":
        # Get the last content item (contains the file annotations)
        text_content = last_message.content[-1]  # ResponseOutputText
        if text_content.type == "output_text":
            # Get the last annotation (most recent file)
            if text_content.annotations:
                file_citation = text_content.annotations[-1]  # AnnotationContainerFileCitation
                if file_citation.type == "container_file_citation":
                    file_id = file_citation.file_id
                    filename = file_citation.filename
                    container_id = file_citation.container_id
                    print(f"Found generated file: {filename} (ID: {file_id})")

    # Download the generated file if available
    if file_id and filename:
        file_content = openai_client.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
        with open(filename, "wb") as f:
            f.write(file_content.read())
            print(f"File {filename} downloaded successfully.")
        print(f"File ready for download: {filename}")
    else:
        print("No file generated in response")
    #uncomment these lines if you want to delete your agent
    #print("\nCleaning up...")
    #project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    #print("Agent deleted")
```

## Regional restrictions

The code interpreter tool for the agents v2 API is not available in the following regions:

* Canada central
* Central US
* Japan east
* South central US
* Southeast Asia
* Spain central

### Supported file types

|File format|MIME Type|
|---|---|
|`.c`| `text/x-c` |
|`.cpp`|`text/x-c++` |
|`.csv`|`application/csv`|
|`.docx`|`application/vnd.openxmlformats-officedocument.wordprocessingml.document`|
|`.html`|`text/html`|
|`.java`|`text/x-java`|
|`.json`|`application/json`|
|`.md`|`text/markdown`|
|`.pdf`|`application/pdf`|
|`.php`|`text/x-php`|
|`.pptx`|`application/vnd.openxmlformats-officedocument.presentationml.presentation`|
|`.py`|`text/x-python`|
|`.py`|`text/x-script.python`|
|`.rb`|`text/x-ruby`|
|`.tex`|`text/x-tex`|
|`.txt`|`text/plain`|
|`.css`|`text/css`|
|`.jpeg`|`image/jpeg`|
|`.jpg`|`image/jpeg`|
|`.js`|`text/javascript`|
|`.gif`|`image/gif`|
|`.png`|`image/png`|
|`.tar`|`application/x-tar`|
|`.ts`|`application/typescript`|
|`.xlsx`|`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`|
|`.xml`|`application/xml` or `text/xml`|
|`.zip`|`application/zip`|
