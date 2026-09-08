---
title: "Use Code Interpreter with Microsoft Foundry agents"
description: "Create agents that run Python code in a sandboxed environment using Code Interpreter in Microsoft Foundry. Upload files, analyze data, and download generated charts."
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
ms.custom: azure-ai-agents, references_regions, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
zone_pivot_groups: selection-code-interpreter-new
ai-usage: ai-assisted
#CustomerIntent: As a developer building AI agents, I want to enable Code Interpreter so that my agent can execute Python code for data analysis and visualization.
---

# Code Interpreter tool for Microsoft Foundry agents

Code Interpreter enables a Microsoft Foundry agent to run Python code in a sandboxed execution environment. The agent's Foundry model writes and executes code for data analysis, chart generation, and iterative problem-solving tasks.

[!INCLUDE [toolbox-recommended](../../includes/toolbox-recommended.md)]

In this article, you create an agent that uses Code Interpreter, upload a CSV file for analysis, and download a generated chart.

When you enable Code Interpreter, your agent can write and run Python code iteratively to solve data analysis and math tasks, and to generate charts.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token-based fees for Azure OpenAI usage. If your agent calls Code Interpreter simultaneously in two different conversations, it creates two Code Interpreter sessions. Each session is active by default for one hour with an idle timeout of 30 minutes.

## Prerequisites

- Basic or standard agent environment. See [agent environment setup](../../../agents/environment-setup.md) for details.
- Latest SDK package installed for your language. The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md) for installation steps.
- Azure AI model deployment configured in your project.

> [!NOTE]
> Code Interpreter isn't available in all regions. See [Check regional and model availability](#check-regional-and-model-availability).

## Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Create an agent with Code Interpreter

The following samples demonstrate how to create an agent with Code Interpreter enabled, upload a file for analysis, and download the generated output. Each file-upload sample generates a small CSV in the current working directory, uploads it, and then deletes the local temporary file.

> [!TIP]
> You can customize Code Interpreter behavior at runtime, such as specifying which files to include or adjusting tool parameters per request, by using [structured inputs](../structured-inputs.md).

:::zone pivot="python"
## Sample of using agent with code interpreter tool in Python SDK

The following Python sample shows how to add the code interpreter tool to a toolbox, attach the toolbox to an agent, upload a CSV file for analysis, and request a bar chart based on the data. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### Prompt agents

This sample demonstrates a complete workflow: upload a file, create an agent with Code Interpreter enabled, request data visualization, and download the generated chart.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool, AutoCodeInterpreterToolParam

CSV_DATA = """name,sector,operating_profit
SkyBridge Logistics,TRANSPORTATION,185.2
Velocity Rail Freight,TRANSPORTATION,310.2
AeroJet Airlines,TRANSPORTATION,510.6
"""
csv_path = os.path.abspath("synthetic-company-financial-results.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
    csv_file.write(CSV_DATA)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Upload the generated CSV file for the code interpreter to use
with open(csv_path, "rb") as csv_file:
    file = openai.files.create(purpose="assistants", file=csv_file)
os.remove(csv_path)

# Create agent with code interpreter tool
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant.",
        tools=[CodeInterpreterTool(container=AutoCodeInterpreterToolParam(file_ids=[file.id]))],
    ),
    description="Code interpreter agent for data analysis and visualization.",
)

# Create a conversation for the agent interaction
conversation = openai.conversations.create()

# Send request to create a chart and generate a file
response = openai.responses.create(
    conversation=conversation.id,
    input="Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Extract file information from response annotations
file_id = ""
filename = ""
container_id = ""

# Get the last message which should contain file citations
last_message = response.output[-1]  # ResponseOutputMessage
if (
    last_message.type == "message"
    and last_message.content
    and last_message.content[-1].type == "output_text"
    and last_message.content[-1].annotations
):
    file_citation = last_message.content[-1].annotations[-1]  # AnnotationContainerFileCitation
    if file_citation.type == "container_file_citation":
        file_id = file_citation.file_id
        filename = file_citation.filename
        container_id = file_citation.container_id
        print(f"Found generated file: {filename} (ID: {file_id})")

# Clean up resources
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)

# Download the generated file if available
if file_id and filename:
    file_content = openai.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
    print(f"File ready for download: {filename}")
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, "wb") as f:
        f.write(file_content.read())
    print(f"File downloaded successfully: {file_path}")
else:
    print("No file generated in response")
```

### Expected output

The sample code produces output similar to the following example:

```console
Found generated file: transportation_operating_profit_bar_chart.png (ID: file-xxxxxxxxxxxxxxxxxxxx)
File ready for download: transportation_operating_profit_bar_chart.png
File downloaded successfully: transportation_operating_profit_bar_chart.png
```

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, filters transportation-sector companies, generates a PNG bar chart showing operating profit by company, and downloads the chart to your local directory. The file annotations in the response provide the file ID and container information needed to retrieve the generated chart.

### Hosted agents

This sample creates the code-interpreter toolbox, then uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework and connects to the toolbox MCP endpoint using [`FoundryToolbox`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox). Set the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` environment variables, and sign in with `az login`.

```python
import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterToolboxTool, AutoCodeInterpreterToolParam

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
CSV_DATA = """name,sector,operating_profit
SkyBridge Logistics,TRANSPORTATION,185.2
Velocity Rail Freight,TRANSPORTATION,310.2
AeroJet Airlines,TRANSPORTATION,510.6
"""


async def main() -> None:
    credential = AzureCliCredential()

    csv_path = os.path.abspath("synthetic-company-financial-results.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
        csv_file.write(CSV_DATA)

    # 1. Add the code interpreter tool to a toolbox. Using a toolbox is the recommended way
    #    to give agents tools: you curate tools once and reuse the toolbox across agents.
    #    See /azure/foundry/agents/concepts/toolbox-overview
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    openai = project.get_openai_client()
    with open(csv_path, "rb") as csv_file:
        file = openai.files.create(purpose="assistants", file=csv_file)
    os.remove(csv_path)
    toolbox = project.toolboxes.create_version(
        name="code-interpreter-toolbox",
        description="Toolbox with the code interpreter tool",
        tools=[CodeInterpreterToolboxTool(container=AutoCodeInterpreterToolParam(file_ids=[file.id]))],
    )

    # 2. The toolbox exposes an MCP-compatible endpoint.
    TOOLBOX_MCP_URL = (
        f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
        f"/versions/{toolbox.version}/mcp?api-version=v1"
    )

    # 3. Attach the toolbox to the hosted agent as an MCP tool.
, timeout=120.0)
    toolbox_tool = FoundryToolbox(credential, url=TOOLBOX_MCP_URL)

agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions="You are a helpful assistant that can write and execute Python code to solve problems.",
        tools=[toolbox_tool],
    )

    result = await agent.run("Use code to calculate the factorial of 100.")
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent generates Python code, runs it in the sandboxed container, and returns the answer:

```console
Agent: 100! = 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
```

For the full sample (including file inputs and extracting the generated code), see [foundry_chat_client_with_code_interpreter.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_code_interpreter.py) and [foundry_chat_client_code_interpreter_files.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_code_interpreter_files.py).

---

:::zone-end

:::zone pivot="csharp"
## Create a chart with Code Interpreter in C#

The following C# sample shows how to add the Code Interpreter tool to a toolbox, attach the toolbox to an agent, upload a CSV file for analysis, and download the generated chart. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### Prompt agents

For asynchronous usage, see the [code sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample32_CodeInterpreterFileGeneration.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using System.IO;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Files;

const string CsvData = """
name,sector,operating_profit
SkyBridge Logistics,TRANSPORTATION,185.2
Velocity Rail Freight,TRANSPORTATION,310.2
AeroJet Airlines,TRANSPORTATION,510.6
""";
string csvPath = Path.GetFullPath("synthetic-company-financial-results.csv");
File.WriteAllText(csvPath, CsvData);

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Upload a CSV file for Code Interpreter to analyze
OpenAIFileClient fileClient = projectClient.ProjectOpenAIClient.GetOpenAIFileClient();
OpenAIFile uploadedFile = fileClient.UploadFile(
  filePath: csvPath,
    purpose: FileUploadPurpose.Assistants);
File.Delete(csvPath);
Console.WriteLine($"Uploaded file: {uploadedFile.Id}");

// Create an agent with Code Interpreter enabled
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful assistant.",
    Tools = {
        ResponseTool.CreateCodeInterpreterTool(
            new CodeInterpreterToolContainer(
                CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration(
                    fileIds: [uploadedFile.Id]
                )
            )
        ),
    }
};
ProjectsAgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myChartAgent",
    options: new(agentDefinition));

// Request chart generation from the uploaded CSV data
AgentReference agentReference = new(name: agentVersion.Name, version: agentVersion.Version);
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentReference);

ResponseResult response = responseClient.CreateResponse(
    "Could you please create bar chart in TRANSPORTATION sector for the operating profit " +
    "from the uploaded csv file and provide file to me?");

Console.WriteLine(response.GetOutputText());

// Extract file information from response annotations
ContainerFileCitationMessageAnnotation containerAnnotation = null;
foreach (ResponseItem item in response.OutputItems)
{
    if (item is MessageResponseItem messageItem)
    {
        foreach (ResponseContentPart content in messageItem.Content)
        {
            foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
            {
                if (annotation is ContainerFileCitationMessageAnnotation cntrAnnotation)
                {
                    containerAnnotation = cntrAnnotation;
                }
            }
        }
    }
}

// Download the generated chart if available
if (containerAnnotation is not null)
{
    ContainerClient containerClient = projectClient.ProjectOpenAIClient.GetContainerClient();
    BinaryData fileData = containerClient.DownloadContainerFile(
        containerId: containerAnnotation.ContainerId,
        fileId: containerAnnotation.FileId);
    File.WriteAllBytes("chart.png", fileData.ToArray());
    Console.WriteLine($"Chart downloaded: {Path.GetFullPath("chart.png")}");
}
else
{
    Console.WriteLine("No file generated in response");
}

// Clean up resources
projectClient.AgentAdministrationClient.DeleteAgentVersion(
    agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The sample code produces output similar to the following example:

```console
Uploaded file: file-xxxxxxxxxxxxxxxxxxxx
Here is the bar chart showing operating profit by company in the TRANSPORTATION sector...
Chart downloaded: C:\Users\you\chart.png
```

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, analyzes the data to filter transportation sector records, and generates a PNG bar chart. The annotation parsing extracts the container ID and file ID from the response, which are used to download the chart to your local directory.

### Hosted agents

This sample creates the code interpreter toolbox, then uses the Microsoft Agent Framework `AddFoundryToolboxes` integration to make Code Interpreter available to the hosted agent. Set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`.

```csharp
using System;
using System.IO;
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;
using OpenAI.Files;

const string CsvData = """
name,sector,operating_profit
SkyBridge Logistics,TRANSPORTATION,185.2
Velocity Rail Freight,TRANSPORTATION,310.2
AeroJet Airlines,TRANSPORTATION,510.6
""";
const string AgentInstructions = "You are a personal math tutor. When asked a math question, write and run code using the python tool to answer the question.";
const string AgentName = "CoderAgent";

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

DefaultAzureCredential credential = new();

// 1. Add the code interpreter tool to a toolbox. Using a toolbox is the recommended
//    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);
OpenAIFileClient fileClient = projectClient.ProjectOpenAIClient.GetOpenAIFileClient();
string csvPath = Path.GetFullPath("synthetic-company-financial-results.csv");
File.WriteAllText(csvPath, CsvData);
OpenAIFile uploadedFile = fileClient.UploadFile(
  filePath: csvPath,
    purpose: FileUploadPurpose.Assistants);
File.Delete(csvPath);

ProjectsAgentTool codeInterpreterTool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateCodeInterpreterTool(
        new CodeInterpreterToolContainer(
            CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration(
                fileIds: [uploadedFile.Id]
            )
        )
    ));

ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "code-interpreter-toolbox",
        tools: [codeInterpreterTool],
        description: "Toolbox with the code interpreter tool");

// Create the hosted agent and register the toolbox integration.
AIAgent agent = projectClient.AsAIAgent(
    model: deploymentName,
    instructions: "You are a helpful assistant with access to the toolbox tools.",
    name: "hosted-toolbox-agent");

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.Services.AddFoundryToolboxes(credential, toolboxVersion.Name);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
```

### Expected output

The hosted agent uses the toolbox MCP endpoint to run Python in the sandbox and return the final answer:

```console
Response: One solution is x ≈ 6.36, since sin(x) + x^2 is approximately 42 at that value.
```

For a maintained .NET Agent Framework integration, see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md).

---

:::zone-end

:::zone pivot="typescript"
## Sample of using agent with code interpreter tool in TypeScript SDK

The following TypeScript sample shows how to add the code interpreter tool to a toolbox, attach the toolbox to an agent, upload a CSV file for analysis, and request a bar chart based on the data. For a JavaScript version, see the [JavaScript sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentCodeInterpreterWithFiles.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const CSV_DATA = `name,sector,operating_profit
SkyBridge Logistics,TRANSPORTATION,185.2
Velocity Rail Freight,TRANSPORTATION,310.2
AeroJet Airlines,TRANSPORTATION,510.6
`;

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Generate and upload the CSV file
  const csvPath = "synthetic-company-financial-results.csv";
  fs.writeFileSync(csvPath, CSV_DATA);
  const fileStream = fs.createReadStream(csvPath);

  // Upload CSV file
  const uploadedFile = await openai.files.create({
    file: fileStream,
    purpose: "assistants",
  });
  fs.unlinkSync(csvPath);

  console.log("Creating a toolbox with the code interpreter tool...");

  // 1. Add the code interpreter tool to a toolbox. Using a toolbox is the recommended
  //    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
  const toolbox = await project.toolboxes.createVersion(
    "code-interpreter-toolbox",
    [
      {
        type: "code_interpreter",
        container: {
          type: "auto",
          file_ids: [uploadedFile.id],
        },
      },
    ],
    { description: "Toolbox with the code interpreter tool" },
  );

  // 2. The toolbox exposes an MCP-compatible endpoint.
  const toolboxMcpUrl =
    `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
    `/versions/${toolbox.version}/mcp?api-version=v1`;

  // 3. Create a remote-tool project connection that points at the toolbox endpoint.
  //    Use a user Entra token so the caller's identity is passed through
  //    (audience https://ai.azure.com). Create the connection once, for example
  //    with the Azure Developer CLI:
  //
  //    azd ai connection create code-interpreter-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "code-interpreter-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant.",
    tools: [
      {
        type: "mcp",
        server_label: "toolbox",
        server_url: toolboxMcpUrl,
        require_approval: "never",
        project_connection_id: toolboxConnectionName,
      },
    ],
  });

  // Create a conversation
  const conversation = await openai.conversations.create();

  // Request chart generation
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input:
        "Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
    },
    {
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Extract file information from response annotations
  let fileId = "";
  let filename = "";
  let containerId = "";

  // Get the last message which should contain file citations
  const lastMessage = response.output?.[response.output.length - 1];
  if (lastMessage && lastMessage.type === "message") {
    // Get the last content item
    const textContent = lastMessage.content?.[lastMessage.content.length - 1];
    if (textContent && textContent.type === "output_text" && textContent.annotations) {
      // Get the last annotation (most recent file)
      const fileCitation = textContent.annotations[textContent.annotations.length - 1];
      if (fileCitation && fileCitation.type === "container_file_citation") {
        fileId = fileCitation.file_id;
        filename = fileCitation.filename;
        containerId = fileCitation.container_id;
        console.log(`Found generated file: ${filename} (ID: ${fileId})`);
      }
    }
  }

  // Download the generated file if available
  if (fileId && filename) {
    const safeFilename = path.basename(filename);
    const fileContent = await openai.containers.files.content.retrieve(
      fileId,
      { container_id: containerId },
    );
    const buffer = Buffer.from(await fileContent.arrayBuffer());

    fs.writeFileSync(safeFilename, buffer);
    console.log(`File ${safeFilename} downloaded successfully.`);
    console.log(`File ready for download: ${safeFilename}`);
  } else {
    console.log("No file generated in response");
  }

  // Clean up resources
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The sample code produces output similar to the following example:

```console
Found generated file: transportation_operating_profit_bar_chart.png (ID: file-xxxxxxxxxxxxxxxxxxxx)
File transportation_operating_profit_bar_chart.png downloaded successfully.
File ready for download: transportation_operating_profit_bar_chart.png
```

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, filters transportation-sector companies, generates a PNG bar chart showing operating profit by company, and downloads the chart to your local directory. The file annotations in the response provide the file ID and container information needed to retrieve the generated chart.

:::zone-end

:::zone pivot="java"

## Create a chart with Code Interpreter in Java

For most agents, add the code interpreter tool through a [toolbox](../../concepts/toolbox-overview.md) and attach the toolbox to your agent as an MCP tool. The Java SDK doesn't yet expose a toolbox creation API, so create the toolbox by using one of the currently supported methods (Python, REST API, C#, TypeScript, or the [Foundry portal](../../how-to/tools/toolbox.md)). Once the toolbox is created, reference its MCP endpoint from your Java agent as an `McpTool`. The following example attaches the code-interpreter toolbox MCP endpoint to the agent.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
</dependency>
```

### Create an agent and generate a chart

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.McpTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class CodeInterpreterChartExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String toolboxMcpUrl = projectEndpoint
            + "/toolboxes/code-interpreter-toolbox/versions/1/mcp?api-version=v1";
        String toolboxConnectionName = "code-interpreter-toolbox-conn";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // The Java SDK doesn't yet expose a toolbox creation API. Create the
        // code-interpreter toolbox with Python, REST, C#, TypeScript, or the
        // Foundry portal, then attach its MCP endpoint as an MCP tool.
        McpTool toolboxTool = new McpTool("toolbox")
            .setServerUrl(toolboxMcpUrl)
            .setProjectConnectionId(toolboxConnectionName)
            .setRequireApproval("never");

        // Create agent with the code-interpreter toolbox MCP tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a data visualization assistant. When asked to create charts, "
                + "write and run Python code using matplotlib to generate them.")
            .setTools(Collections.singletonList(toolboxTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("chart-agent", agentDefinition);

        // Request a bar chart with inline data
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("Create a bar chart showing quarterly revenue for 2025: "
                    + "Q1=$2.1M, Q2=$2.8M, Q3=$3.2M, Q4=$2.9M. "
                    + "Use a blue color scheme, add data labels on each bar, "
                    + "and title the chart 'Quarterly Revenue 2025'. "
                    + "Save the chart as a PNG file."));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```console
Response: Here is the bar chart showing quarterly revenue for 2025 with Q1 ($2.1M), Q2 ($2.8M), Q3 ($3.2M), and Q4 ($2.9M) displayed in blue with data labels.
```

The agent uses Code Interpreter through the toolbox MCP endpoint, writes Python code by using matplotlib to generate the chart, and executes the code in a sandboxed environment. For an example that uploads a CSV file and downloads the generated chart, select **Python** or **TypeScript** from the language selector at the top of this article. For more examples, see the [Azure AI Agents Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/).

:::zone-end

:::zone pivot="rest"

## Create a chart with Code Interpreter using the REST API

The following example shows how to upload a CSV file, create an agent with Code Interpreter, request a chart, and download the generated file.

### Prerequisites

Set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: Your project endpoint URL.
- `AGENT_TOKEN`: A bearer token for Foundry.

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

### Use Code Interpreter in a toolbox

To upload a file for Code Interpreter to use through a toolbox, upload the file at the **resource-level** Files endpoint (`POST {account_endpoint}/openai/v1/files`) with the `x-aml-project-id` header. Unlike the prompt agent flow, files uploaded through the project-scoped Files endpoint (`/api/projects/{name}/openai/v1/files`) receive an `owner_id` that the toolbox container can't verify, so `tools/call` fails with an ownership-verification error.

1. Get the project GUID from Azure Resource Manager. Use `properties.amlWorkspace.internalId` (dashed UUID format), **not** `properties.internalId` (no dashes - the toolbox container rejects it):

    ```bash
    ARM_TOKEN=$(az account get-access-token --query accessToken -o tsv)
    PROJECT_GUID=$(curl -s -H "Authorization: Bearer $ARM_TOKEN" \
      "https://management.azure.com/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}?api-version=2025-06-01" \
      | jq -r '.properties.amlWorkspace.internalId')
    ```

1. Upload the file at the account (resource) level with the `x-aml-project-id` header:

    ```bash
    cat > synthetic-company-financial-results.csv <<'CSV'
    name,sector,operating_profit
    SkyBridge Logistics,TRANSPORTATION,185.2
    Velocity Rail Freight,TRANSPORTATION,310.2
    AeroJet Airlines,TRANSPORTATION,510.6
    CSV

    TOKEN=$(az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv)
    curl -X POST "https://{account}.services.ai.azure.com/openai/v1/files" \
      -H "Authorization: Bearer $TOKEN" \
      -H "x-aml-project-id: $PROJECT_GUID" \
      -F "purpose=assistants" \
      -F "file=@synthetic-company-financial-results.csv"
    rm synthetic-company-financial-results.csv
    ```

The returned file `id` is the value you supply as `<FILE_ID>` in the tool configuration. Files are mounted in the sandbox at `/mnt/data/{file-id}-{original-filename}`.

> [!IMPORTANT]
> When Code Interpreter is used through a toolbox in a hosted agent, **user isolation isn't supported**. All users in the same project share the same container context.

### Add Code Interpreter to a toolbox

Add Code Interpreter by creating a toolbox, and then attach the toolbox to your agent as an MCP tool. For more information, see [What is a toolbox?](../../concepts/toolbox-overview.md)

- Create a toolbox that contains the code interpreter tool:

    ```bash
    curl --request POST \
      --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/code-interpreter-toolbox/versions?api-version=v1" \
      -H "Authorization: Bearer $AGENT_TOKEN" \
      -H "Content-Type: application/json" \
      --data '{
        "description": "Toolbox with the code interpreter tool",
        "tools": [
          {
            "type": "code_interpreter",
            "container": {
              "type": "auto",
              "file_ids": ["<FILE_ID>"]
            }
          }
        ]
      }'
    ```

   The toolbox exposes an MCP-compatible endpoint at `$FOUNDRY_PROJECT_ENDPOINT/toolboxes/code-interpreter-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

- Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).

    ```bash
    azd ai connection create code-interpreter-toolbox-conn \
      --kind remote-tool \
      --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/code-interpreter-toolbox/versions/<version>/mcp?api-version=v1" \
      --auth-type user-entra-token \
      --audience https://ai.azure.com
    ```

### Create an agent with the code interpreter toolbox

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "chart-agent",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
      "instructions": "You are a data visualization assistant. When asked to create charts, write and run Python code using matplotlib to generate them.",
      "tools": [
        {
          "type": "mcp",
          "server_label": "toolbox",
          "server_url": "'$FOUNDRY_PROJECT_ENDPOINT'/toolboxes/code-interpreter-toolbox/versions/<version>/mcp?api-version=v1",
          "require_approval": "never",
          "project_connection_id": "code-interpreter-toolbox-conn"
        }
      ]
    }
  }'
```

### Generate a chart

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {"type": "agent_reference", "name": "chart-agent"},
    "input": "Create a bar chart of operating profit by company for the TRANSPORTATION sector from the uploaded CSV file. Use a blue color scheme and add data labels."
  }'
```

The response includes `container_file_citation` annotations with the generated file details. Save the `container_id` and `file_id` values from the annotation.

### Download the generated chart

```bash
curl -X GET "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/containers/<CONTAINER_ID>/files/<FILE_ID>/content" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  --output chart.png
```

### Clean up

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/chart-agent?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

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

For examples of conversation and file cleanup patterns, see [Web search tool](web-search.md) and [File search tool for agents](file-search.md).

## Sandboxed execution environment

Code Interpreter runs Python code in a Microsoft-managed sandbox. The sandbox is designed for running untrusted code and uses [dynamic sessions (code interpreter sessions) in Azure Container Apps](/azure/container-apps/sessions-code-interpreter). Each session is isolated by a Hyper-V boundary.

Key behaviors to plan for:

- **Region**: The Code Interpreter sandbox runs in the same Azure region as your Foundry project.
- **Session lifetime**: A Code Interpreter session is active for up to one hour, with an idle timeout (see the *Important* note at the beginning of this article).
- **Isolation**: Each session runs in an isolated environment. If your agent invokes Code Interpreter concurrently in different conversations, separate sessions are created.
- **Network isolation and internet access**: The sandbox doesn't inherit your agent subnet configuration, and dynamic sessions can't make outbound network requests.
- **Files in the sandbox**: The sandboxed Python runtime has access to files you attach for analysis. Code Interpreter can also generate files, such as charts, and return them as downloadable outputs.

If you need more control over the sandbox runtime or you need a different isolation model, see [Custom code interpreter tool for agents](custom-code-interpreter.md).

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Custom code interpreter tool for agents (preview)](custom-code-interpreter.md)
