---
title: Use Code Interpreter with Microsoft Foundry agents
titleSuffix: Microsoft Foundry
description: Create agents that run Python code in a sandboxed environment using Code Interpreter in Microsoft Foundry. Upload files, analyze data, and download generated charts.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/03/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions, dev-focus, pilot-ai-workflow-jan-2026
zone_pivot_groups: selection-code-interpreter-new
ai-usage: ai-assisted
#CustomerIntent: As a developer building AI agents, I want to enable Code Interpreter so that my agent can execute Python code for data analysis and visualization.
---

# Code Interpreter tool for Microsoft Foundry agents

Code Interpreter enables a Microsoft Foundry agent to run Python code in a sandboxed execution environment. Use this tool for data analysis, chart generation, and iterative problem-solving tasks that benefit from code execution.

In this article, you create an agent that uses Code Interpreter, upload a CSV file for analysis, and download a generated chart.

When enabled, your agent can write and run Python code iteratively to solve data analysis and math tasks, and to generate charts.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token-based fees for Azure OpenAI usage. If your agent calls Code Interpreter simultaneously in two different conversations, two Code Interpreter sessions are created. Each session is active by default for one hour with an idle timeout of 30 minutes.

### Usage support

|Microsoft Foundry support|Python SDK|C# SDK|JavaScript SDK|Java SDK|REST API|Basic agent setup|Standard agent setup|
|---|---|---|---|---|---|---|---|
|✔️|✔️|✔️|-|-|-|✔️|✔️|

✔️ indicates the feature is supported. `-` indicates the feature isn't currently available for that SDK or API.

## Prerequisites

- Basic or standard agent environment. See [agent environment setup](../../../../agents/environment-setup.md) for details.
- Latest prerelease SDK package installed (`azure-ai-projects>=2.0.0b1` for Python). See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for installation steps.
- Azure AI model deployment configured in your project.
- For file operations: CSV or other supported files to upload for analysis.

> [!NOTE]
> Code Interpreter isn't available in all regions. See [Check regional and model availability](#check-regional-and-model-availability).

## Create an agent with Code Interpreter

The following samples demonstrate how to create an agent with Code Interpreter enabled, upload a file for analysis, and download the generated output.

> [!NOTE]
> You need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true).

:::zone pivot="python"
## Sample of using agent with code interpreter tool in Python SDK

The following Python sample shows how to create an agent with the code interpreter tool, upload a CSV file for analysis, and request a bar chart based on the data. It demonstrates a complete workflow: upload a file, create an agent with Code Interpreter enabled, request data visualization, and download the generated chart.

Set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`
- `FOUNDRY_MODEL_DEPLOYMENT_NAME`

```python
import os
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
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with project_client:
    openai_client = project_client.get_openai_client()

    # Upload the CSV file for the code interpreter to use
    with open(asset_file_path, "rb") as f:
        file = openai_client.files.create(purpose="assistants", file=f)
    print(f"File uploaded (id: {file.id})")

    # Create agent with code interpreter tool
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
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
        safe_filename = os.path.basename(filename)
        file_content = openai_client.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
        with open(safe_filename, "wb") as f:
            f.write(file_content.read())
            print(f"File {safe_filename} downloaded successfully.")
        print(f"File ready for download: {safe_filename}")
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

The following C# sample shows how to create an agent with the code interpreter tool and ask it to solve a mathematical equation. Replace the environment variable values (`FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`) with your actual resource details. The agent executes Python code in a sandboxed container to compute the solution. The code uses synchronous calls for simplicity. For asynchronous usage, refer to the [code sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample7_CodeInterpreter.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
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

## Check regional and model availability

Tool availability varies by region and model.

For the current list of supported regions and models for Code Interpreter, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

### Supported file types

|File format|MIME type|
|---|---|
|`.c`|`text/x-c`|
|`.cpp`|`text/x-c++`|
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

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| Code Interpreter doesn't run. | Tool not enabled or model doesn't support it in your region. | Confirm Code Interpreter is enabled on the agent. Verify your model deployment supports the tool in your region. See [Check regional and model availability](#check-regional-and-model-availability). |
| No file is generated. | Agent returned text-only response without file annotation. | Check response annotations for `container_file_citation`. If none exist, the agent didn't generate a file. Rephrase the prompt to explicitly request file output. |
| File upload fails. | Unsupported file type or wrong purpose. | Confirm the file type is in the [supported file types](#supported-file-types) list. Upload with `purpose="assistants"`. |
| Generated file is corrupt or empty. | Code execution error or incomplete processing. | Check the agent's response for error messages. Verify the input data is valid. Try a simpler request first. |
| Session timeout or high latency. | Code Interpreter sessions have time limits. | Sessions have a 1-hour active timeout and 30-minute idle timeout. Reduce the complexity of operations or split into smaller tasks. |
| Unexpected billing charges. | Multiple concurrent sessions created. | Each conversation creates a separate session. Monitor session usage and consolidate operations where possible. |
| Python package not available. | Code Interpreter has a fixed set of packages. | Code Interpreter includes common data science packages. For custom packages, use [Custom code interpreter](custom-code-interpreter.md). |
| File download fails. | Container ID or file ID incorrect. | Verify you're using the correct `container_id` and `file_id` from the response annotations. |

## Clean up resources

Delete resources you created in this sample when you no longer need them to avoid ongoing costs:

- Delete the agent version.
- Delete the conversation.
- Delete uploaded files.

For examples of conversation and file cleanup patterns, see [Web search tool (preview)](web-search.md) and [File search tool for agents](file-search.md).

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Custom code interpreter tool for agents (preview)](custom-code-interpreter.md)
