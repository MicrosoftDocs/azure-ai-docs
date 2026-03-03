---
title: "Use Code Interpreter with Microsoft Foundry agents"
description: "Create agents that run Python code in a sandboxed environment using Code Interpreter in Microsoft Foundry. Upload files, analyze data, and download generated charts."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/02/2026
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

✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ | ✔️ |

## Prerequisites

- Basic or standard agent environment. See [agent environment setup](../../../agents/environment-setup.md) for details.
- Latest SDK package installed for your language. The .NET and Java SDKs are currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md) for installation steps.
- Azure AI model deployment configured in your project.
- For file operations: CSV or other supported files to upload for analysis.

> [!NOTE]
> Code Interpreter isn't available in all regions. See [Check regional and model availability](#check-regional-and-model-availability).

## Create an agent with Code Interpreter

The following samples demonstrate how to create an agent with Code Interpreter enabled, upload a file for analysis, and download the generated output.

:::zone pivot="python"
## Sample of using agent with code interpreter tool in Python SDK

The following Python sample shows how to create an agent with the code interpreter tool, upload a CSV file for analysis, and request a bar chart based on the data. It demonstrates a complete workflow: upload a file, create an agent with Code Interpreter enabled, request data visualization, and download the generated chart.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool, CodeInterpreterContainerAuto

# Load the CSV file to be processed
asset_file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../assets/synthetic_500_quarterly_results.csv")
)

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Upload the CSV file for the code interpreter to use
    file = openai_client.files.create(purpose="assistants", file=open(asset_file_path, "rb"))

    # Create agent with code interpreter tool
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[CodeInterpreterTool(container=CodeInterpreterContainerAuto(file_ids=[file.id]))],
        ),
        description="Code interpreter agent for data analysis and visualization.",
    )

    # Create a conversation for the agent interaction
    conversation = openai_client.conversations.create()

    # Send request to create a chart and generate a file
    response = openai_client.responses.create(
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
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)

    # Download the generated file if available
    if file_id and filename:
        file_content = openai_client.containers.files.content.retrieve(file_id=file_id, container_id=container_id)
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

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, analyzes the data to filter transportation sector records, generates a PNG bar chart showing operating profit by quarter, and downloads the chart to your local directory. The file annotations in the response provide the file ID and container information needed to retrieve the generated chart.

:::zone-end

:::zone pivot="csharp"
## Create a chart with Code Interpreter in C#

The following C# sample shows how to create an agent with the code interpreter tool and use it to generate a bar chart. The agent writes and executes Python code (using matplotlib) in a sandboxed container. For asynchronous usage, refer to the [code sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample7_CodeInterpreter.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

// Create project client and read the environment variables.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create an agent with Code Interpreter enabled.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a data visualization assistant. When asked to create charts, write and run Python code using matplotlib to generate them.",
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
    agentName: "myChartAgent",
    options: new(agentDefinition));

// Ask the agent to create a bar chart from inline data.
AgentReference agentReference = new(name: agentVersion.Name, version: agentVersion.Version);
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentReference);

ResponseResult response = responseClient.CreateResponse(
    "Create a bar chart showing quarterly revenue for 2025: Q1=$2.1M, Q2=$2.8M, Q3=$3.2M, Q4=$2.9M. " +
    "Use a blue color scheme, add data labels on each bar, and title the chart 'Quarterly Revenue 2025'. " +
    "Save the chart as a PNG file.");

Console.WriteLine(response.GetOutputText());

// Clean up
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The sample code produces output similar to the following example:

```console
Here is the bar chart showing quarterly revenue for 2025. The chart displays Q1 ($2.1M), Q2 ($2.8M), Q3 ($3.2M), and Q4 ($2.9M) with a blue color scheme, data labels on each bar, and the title "Quarterly Revenue 2025".
```

The agent creates a Code Interpreter session, writes Python code using matplotlib to generate the bar chart, executes the code in a sandboxed environment, and returns the chart as a generated file. For an example that uploads a CSV file and downloads the generated chart, select **Python** or **TypeScript** from the language selector at the top of this article.

:::zone-end

:::zone pivot="typescript"
## Sample of using agent with code interpreter tool in TypeScript SDK

The following TypeScript sample shows how to create an agent with the code interpreter tool, upload a CSV file for analysis, and request a bar chart based on the data. For a JavaScript version, see the [JavaScript sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentCodeInterpreter.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

// Helper to resolve asset file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Load and upload CSV file
  const assetFilePath = path.resolve(
    __dirname,
    "../assets/synthetic_500_quarterly_results.csv",
  );
  const fileStream = fs.createReadStream(assetFilePath);

  // Upload CSV file
  const uploadedFile = await openAIClient.files.create({
    file: fileStream,
    purpose: "assistants",
  });

  // Create agent with Code Interpreter tool
  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant.",
    tools: [
      {
        type: "code_interpreter",
        container: {
          type: "auto",
          file_ids: [uploadedFile.id],
        },
      },
    ],
  });

  // Create a conversation
  const conversation = await openAIClient.conversations.create();

  // Request chart generation
  const response = await openAIClient.responses.create(
    {
      conversation: conversation.id,
      input:
        "Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
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
    const fileContent = await openAIClient.containers.files.content.retrieve({
      file_id: fileId,
      container_id: containerId,
    });

    // Read the readable stream into a buffer
    const chunks: Buffer[] = [];
    for await (const chunk of fileContent.body) {
      chunks.push(Buffer.from(chunk));
    }
    const buffer = Buffer.concat(chunks);

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

The agent uploads your CSV file to Azure storage, creates a sandboxed Python environment, analyzes the data to filter transportation sector records, generates a PNG bar chart showing operating profit by quarter, and downloads the chart to your local directory. The file annotations in the response provide the file ID and container information needed to retrieve the generated chart.

:::zone-end

:::zone pivot="java"

## Create a chart with Code Interpreter in Java

Set the following environment variables:

- `FOUNDRY_PROJECT_ENDPOINT` — Your project endpoint.
- `FOUNDRY_MODEL_DEPLOYMENT_NAME` — A deployed model name.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0-beta.1</version>
</dependency>
```

### Create an agent and generate a chart

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.CodeInterpreterTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.core.util.Configuration;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class CodeInterpreterChartExample {
    public static void main(String[] args) {
        String endpoint = Configuration.getGlobalConfiguration().get("FOUNDRY_PROJECT_ENDPOINT");
        String model = Configuration.getGlobalConfiguration().get("FOUNDRY_MODEL_DEPLOYMENT_NAME");

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(endpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create code interpreter tool
        CodeInterpreterTool codeInterpreter = new CodeInterpreterTool();

        // Create agent with code interpreter for data visualization
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition(model)
            .setInstructions("You are a data visualization assistant. When asked to create charts, "
                + "write and run Python code using matplotlib to generate them.")
            .setTools(Collections.singletonList(codeInterpreter));

        AgentVersionDetails agent = agentsClient.createAgentVersion("chart-agent", agentDefinition);

        // Request a bar chart with inline data
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createWithAgent(
            agentReference,
            ResponseCreateParams.builder()
                .input("Create a bar chart showing quarterly revenue for 2025: "
                    + "Q1=$2.1M, Q2=$2.8M, Q3=$3.2M, Q4=$2.9M. "
                    + "Use a blue color scheme, add data labels on each bar, "
                    + "and title the chart 'Quarterly Revenue 2025'. "
                    + "Save the chart as a PNG file.")
                .build());

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

The agent creates a Code Interpreter session, writes Python code using matplotlib to generate the chart, and executes the code in a sandboxed environment. For an example that uploads a CSV file and downloads the generated chart, select **Python** or **TypeScript** from the language selector at the top of this article. For more examples, see the [Azure AI Agents Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/).

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

### 1. Upload a CSV file

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/files" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F "purpose=assistants" \
  -F "file=@quarterly_results.csv"
```

Save the `id` from the response (for example, `file-abc123`).

### 2. Create an agent with code interpreter

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
          "type": "code_interpreter",
          "container": {
            "type": "auto",
            "file_ids": ["<FILE_ID>"]
          }
        }
      ]
    }
  }'
```

### 3. Generate a chart

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {"type": "agent_reference", "name": "chart-agent"},
    "input": "Create a bar chart of operating profit by quarter from the uploaded CSV file. Use a blue color scheme and add data labels."
  }'
```

The response includes `container_file_citation` annotations with the generated file details. Save the `container_id` and `file_id` values from the annotation.

### 4. Download the generated chart

```bash
curl -X GET "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/containers/<CONTAINER_ID>/files/<FILE_ID>/content" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  --output chart.png
```

### 5. Clean up

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

For examples of conversation and file cleanup patterns, see [Web search tool (preview)](web-search.md) and [File search tool for agents](file-search.md).

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Custom code interpreter tool for agents (preview)](custom-code-interpreter.md)
