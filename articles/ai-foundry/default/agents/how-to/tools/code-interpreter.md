---
title: Use Code Interpreter with Microsoft Foundry agents
titleSuffix: Microsoft Foundry
description: Learn to enable agents to execute Python code, analyze data, and generate charts using Code Interpreter in Microsoft Foundry. Get started today.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions, dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-code-interpreter-new
---

# Code Interpreter tool for Microsoft Foundry agents

In this article, you create an agent that uses Code Interpreter to execute Python code in a sandboxed environment. You learn how to enable agents to solve mathematical problems, analyze data from CSV files, and generate visualizations like charts and graphs.

Code Interpreter enables agents to write and run Python code in a sandboxed execution environment. By enabling Code Interpreter, your agent can run code iteratively to solve more challenging code, math, and data analysis problems or create graphs and charts. When your agent writes code that doesn't run, it can modify and run different code until the code execution succeeds.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your agent calls Code Interpreter simultaneously in two different conversations, two code interpreter sessions are created. Each session is active by default for 1 hour with an idle timeout of 30 minutes.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | - | - | - | ✔️ | ✔️ |

## Prerequisites

- Basic or standard agent environment. See [agent environment setup](../../../../agents/environment-setup.md) for details.
- Latest prerelease SDK package installed. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for installation steps.
- Azure AI model deployment configured in your project.
- For file operations: CSV or other supported files to upload for analysis.

> [!NOTE]
> Code Interpreter isn't available in [some regions](#regional-restrictions).

## Code samples

> [!NOTE]
> You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

:::zone pivot="python"
## Sample of using agent with code interpreter tool in Python SDK

The following Python sample shows how to create an agent with the code interpreter tool, upload a CSV file for analysis, and request a bar chart based on the data in the CSV file. It demonstrates a complete workflow: uploading a CSV file to Azure storage, creating an agent with Code Interpreter capability, requesting data analysis and visualization, and downloading the generated chart. Replace the environment variable values (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`) with your actual resource details. The code expects a CSV file at the specified path.

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

### Expected output

The sample code produces output similar to the following example:

```console
File uploaded (id: file-xxxxxxxxxxxxxxxxxxxx)
Agent created (id: agent-xxxxxxxxxxxxxxxxxxxx, name: MyAgent, version: 1)
Created conversation (id: conv-xxxxxxxxxxxxxxxxxxxx)
Response completed (id: resp-xxxxxxxxxxxxxxxxxxxx)
Found generated file: transportation_operating_profit_bar_chart.png (ID: file-xxxxxxxxxxxxxxxxxxxx)
File transportation_operating_profit_bar_chart.png downloaded successfully.
File ready for download: transportation_operating_profit_bar_chart.png
```

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, analyzes the data to filter transportation sector records, generates a PNG bar chart showing operating profit by quarter, and downloads the chart to your local directory. The file annotations in the response provide the file ID and container information needed to retrieve the generated chart.

:::zone-end

:::zone pivot="csharp"
## Sample of using agent with code interpreter and file attachment in C# SDK

The following C# sample shows how to create an agent with the code interpreter tool, upload a CSV file for analysis, and request a bar chart based on the data in the CSV file. It creates an agent with Code Interpreter capability and requests it to solve a mathematical equation. Replace the environment variable values (`PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`) with your actual resource details. The agent executes Python code in a sandboxed container to compute the solution. The code uses synchronous calls for simplicity. For asynchronous usage, refer to the [code sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample7_CodeInterpreter.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create Agent, capable to use Code Interpreter to answer questions.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent that can help fetch data from files you know about.",
    Tools = {
        ResponseTool.CreateCodeInterpreterTool(
            new CodeInterpreterToolContainer(
                CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration(
                    fileIds: []
                )
            )
        ),
    }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Ask the agent a question, which requires running python code in the container.
AgentReference agentReference = new(name: agentVersion.Name, version: agentVersion.Version);
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentReference);

ResponseResult response = responseClient.CreateResponse("I need to solve the equation sin(x) + x^2 = 42");

// Write out the output of a response, raise the exception if the request was not successful.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Clean up resources by deleting conversations and the Agent.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The sample code produces output similar to the following example:

```console
Response completed (id: resp-xxxxxxxxxxxxxxxxxxxx)
The solution to the equation sin(x) + x^2 = 42 is approximately x = 6.324555320336759
```

The agent creates a Code Interpreter session, writes Python code to solve the equation numerically, executes the code in a sandboxed environment, and returns the computed result. The agent iteratively refines its approach if the initial code doesn't produce a valid solution.

:::zone-end

## Regional restrictions

The code interpreter tool for the Foundry projects (new) API isn't available in the following regions:

* Canada Central
* Central US
* Japan East
* South Central US
* Southeast Asia
* Spain Central

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

## Sandboxed execution environment

Code Interpreter runs Python code in a Microsoft-managed sandbox. The sandbox is designed for running untrusted code and is implemented using [dynamic sessions (code interpreter sessions) in Azure Container Apps](https://learn.microsoft.com/azure/container-apps/sessions-code-interpreter), where each session is isolated by a Hyper-V boundary.

Key behaviors to plan for:

- **Region**: The Code Interpreter sandbox runs in the same Azure region as your Foundry project.
- **Session lifetime**: A Code Interpreter session is active for up to 1 hour, with an idle timeout (see the Important note earlier in this article).
- **Isolation**: Each session runs in an isolated environment. If your agent invokes Code Interpreter concurrently in different conversations, separate sessions are created.
- **Network isolation and internet access**: The sandbox doesn't inherit your agent subnet configuration, and dynamic sessions are prevented from making outbound network requests.
- **Files in the sandbox**: Files you attach for analysis are available to the sandboxed Python runtime. Code Interpreter can also generate files (for example, charts) and return them as downloadable outputs.

If you need more control over the sandbox runtime or you need a different isolation model, see the [custom code interpreter](./custom-code-interpreter.md).
