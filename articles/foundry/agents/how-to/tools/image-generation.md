---
title: "Use the image generation tool in Foundry Agent Service"
description: "Generate images from text prompts with the image generation tool in Microsoft Foundry Agent Service. Configure agents, deploy models, and save output."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom: dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
ms.date: 03/06/2026
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-image-generation
---

# Use the image generation tool

> [!IMPORTANT] 
> - The image generation tool requires the `gpt-image-1` model. See the [Azure OpenAI transparency note](../../../responsible-ai/openai/transparency-note.md?tabs=image) for limitations and responsible AI considerations.
> - You also need a compatible orchestrator model (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, or `gpt-5` series) deployed in the same Foundry project.

The **image generation tool** in Microsoft Foundry Agent Service generates images from text prompts in conversations and multistep workflows. Use it to create AI-generated visuals and return base64-encoded output that you can save to a file.

## Usage support

✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ | ✔️ |

## Prerequisites

- An Azure account with an active subscription.
- A Foundry project.
- A basic or standard agent environment. See [agent environment setup](../../../agents/environment-setup.md).
- Permissions to create and manage agent versions in the project.
- Two model deployments in the same Foundry project:
  - A compatible Azure OpenAI model deployment for the agent (for example, `gpt-4o`).
  - An image generation model deployment (`gpt-image-1`).

## Configure the image generation tool

1. Deploy your orchestrator model (for example, `gpt-4o`) to your Foundry project.
1. Deploy `gpt-image-1` to the same Foundry project.
1. Confirm your region and model support for image generation. See [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Code examples

Before you start, install the latest SDK package. The .NET and Java SDKs are currently in preview. For package installation instructions, see the [quickstart](../../../quickstarts/get-started-code.md).

:::zone pivot="python"
## Create an agent with the image generation tool

This sample creates an agent with the image generation tool, generates an image, and saves it to a file.

```python
import base64
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, ImageGenTool

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
IMAGE_MODEL = "gpt-image-1"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create an agent with the image generation tool
agent = project.agents.create_version(
    agent_name="agent-image-generation",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Generate images based on user prompts.",
        tools=[ImageGenTool(model=IMAGE_MODEL, quality="low", size="1024x1024")],
    ),
    description="Agent for image generation.",
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Generate an image using the agent
response = openai.responses.create(
    input="Generate an image of the Microsoft logo.",
    extra_headers={
        "x-ms-oai-image-generation-deployment": IMAGE_MODEL,
    },
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Clean up the agent
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)

# Extract and save the generated image
image_data = [output.result for output in response.output if output.type == "image_generation_call"]
if image_data and image_data[0]:
    file_path = os.path.abspath("microsoft.png")
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image_data[0]))
    print(f"Image saved to: {file_path}")
```
:::zone-end

:::zone pivot="csharp"
## Sample for image generation in Azure.AI.Projects.OpenAI.

In this example, you generate an image based on a simple prompt. The code in this example is synchronous. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample2_Image_Generation.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var imageModel = "gpt-image-1";

// Create the AI Project client with custom header policy
AIProjectClientOptions projectOptions = new();
projectOptions.AddPolicy(new HeaderPolicy(imageModel), PipelinePosition.PerCall);

// Create the AI Project client
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential(),
    options: projectOptions
);

// Use the client to create the versioned agent object.
// To generate images, we need to provide agent with the ImageGenerationTool
// when creating this tool. The ImageGenerationTool parameters include
// the image generation model, image quality and resolution.
// Supported image generation models include gpt-image-1.
PromptAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
Instructions = "Generate images based on user prompts.",
Tools = {
        ResponseTool.CreateImageGenerationTool(
            model: imageModel,
            quality: ImageGenerationToolQuality.Low,
            size:ImageGenerationToolSize.W1024xH1024
        )
    }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

ProjectOpenAIClient openAIClient = projectClient.GetProjectOpenAIClient();
ProjectResponsesClient responseClient = openAIClient.GetProjectResponsesClientForAgent(new AgentReference(name: agentVersion.Name));

ResponseResult response = responseClient.CreateResponse("Generate parody of Newton with apple.");

// Parse the ResponseResult object and save the generated image.
foreach (ResponseItem item in response.OutputItems)
{
    if (item is ImageGenerationCallResponseItem imageItem)
    {
        File.WriteAllBytes("newton.png", imageItem.ImageResultBytes.ToArray());
        Console.WriteLine($"Image downloaded and saved to: {Path.GetFullPath("newton.png")}");
    }
}

// Clean up resources by deleting the Agent.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);

// To use image generation, provide the custom header to web requests,
// which contain the model deployment name, for example:
// `x-ms-oai-image-generation-deployment: gpt-image-1`.
// To implement it, create a custom header policy.
internal class HeaderPolicy(string image_deployment) : PipelinePolicy
{
    private const string image_deployment_header = "x-ms-oai-image-generation-deployment";

    public override void Process(PipelineMessage message, IReadOnlyList<PipelinePolicy> pipeline, int currentIndex)
    {
        message.Request.Headers.Add(image_deployment_header, image_deployment);
        ProcessNext(message, pipeline, currentIndex);
    }

    public override async ValueTask ProcessAsync(PipelineMessage message, IReadOnlyList<PipelinePolicy> pipeline, int currentIndex)
    {
        // Add your desired header name and value
        message.Request.Headers.Add(image_deployment_header, image_deployment);
        await ProcessNextAsync(message, pipeline, currentIndex);
    }
}
```

### Expected output

When you run the sample, you see the following output:

```console
Agent created (id: <agent-id>, name: myAgent, version: 1)
Image downloaded and saved to: /path/to/newton.png
Agent deleted
```
:::zone-end

:::zone pivot="rest-api"
## Create an agent with the image generation tool

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

The following example creates an agent that uses the image generation tool.

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "image-gen-agent",
    "description": "Test agent for image generation capabilities",
    "definition": {
      "kind": "prompt",
      "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
      "tools": [
        {
          "type": "image_generation"
        }
      ],
      "instructions": "You are a creative assistant that generates images when requested. Please respond to image generation requests clearly and concisely."
    }
  }'
```

## Create a response

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "x-ms-oai-image-generation-deployment: $IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME" \
  -d '{
    "agent": {
      "type": "agent_reference",
      "name": "image-gen-agent"
    },
    "input": [{
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Please generate small image of a sunset over a mountain lake."
        }
      ]
    }],
    "stream": false
  }'
```

### Expected output

The response JSON includes an `image_generation_call` output item with a `result` field containing base64-encoded image data:

```json
{
  "id": "resp_<id>",
  "status": "completed",
  "output": [
    {
      "type": "image_generation_call",
      "result": "<base64-encoded-image-data>",
      "status": "completed"
    },
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Here is the image of a sunset over a mountain lake."
        }
      ]
    }
  ]
}
```

To extract and save the image, pipe the response through `jq` and `base64`:

```bash
RESPONSE=$(curl -s -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "x-ms-oai-image-generation-deployment: $IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME" \
  -d '{ ... }')

echo "$RESPONSE" | jq -r '.output[] | select(.type=="image_generation_call") | .result' \
  | base64 --decode > generated_image.png
```

:::zone-end

:::zone pivot="typescript"
## Create an agent with image generation tool

This sample demonstrates how to create an AI agent with image generation capabilities by using the Azure AI Projects client. The agent generates images based on text prompts and saves them to files. For a JavaScript example, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentImageGeneration.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const IMAGE_MODEL = "gpt-image-1";

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create Agent with image generation tool
  const agent = await project.agents.createVersion("agent-image-generation", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "Generate images based on user prompts",
    tools: [
      {
        type: "image_generation",
        quality: "low",
        size: "1024x1024",
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Generate image using the agent
  const response = await openai.responses.create(
    {
      input: "Generate an image of Microsoft logo.",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
      headers: { "x-ms-oai-image-generation-deployment": IMAGE_MODEL },
    },
  );

  // Extract and save the generated image
  const imageData = response.output?.filter((output) => output.type === "image_generation_call");

  if (imageData && imageData.length > 0 && imageData[0].result) {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    const filename = "microsoft.png";
    const filePath = path.join(__dirname, filename);

    // Decode base64 and save to file
    const imageBuffer = Buffer.from(imageData[0].result, "base64");
    fs.writeFileSync(filePath, imageBuffer);

    console.log(`Image downloaded and saved to: ${path.resolve(filePath)}`);
  } else {
    console.log("No image data found in the response.");
  }

  // Clean up resources
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

When you run the sample, you see the following output:

```console
Agent created (id: <agent-id>, name: agent-image-generation, version: 1)
Image downloaded and saved to: /path/to/microsoft.png
```
:::zone-end

:::zone pivot="java"

## Use image generation in a Java agent

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0-beta.1</version>
</dependency>
```

### Create an agent with image generation

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.*;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class ImageGenerationExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String imageModel = "gpt-image-1";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create image generation tool with model, quality, and size
        ImageGenTool imageGenTool = new ImageGenTool()
            .setModel(ImageGenToolModel.fromString(imageModel))
            .setQuality(ImageGenToolQuality.LOW)
            .setSize(ImageGenToolSize.fromString("1024x1024"));

        // Create agent with image generation tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a creative assistant that can generate images based on descriptions.")
            .setTools(Collections.singletonList(imageGenTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("image-gen-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createWithAgent(
            agentReference,
            ResponseCreateParams.builder()
                .input("Generate an image of a sunset over a mountain range"));

        // The response output includes image_generation_call items with base64-encoded image data.
        // Extract and save the image using the response output items.
        System.out.println("Response status: " + response.status().map(Object::toString).orElse("unknown"));
        System.out.println("Output items: " + response.output().size());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

> [!NOTE]
> The `response.output()` list contains `image_generation_call` items with base64-encoded image data in the `result` field. Use `java.util.Base64.getDecoder().decode()` to convert the result to bytes and write them to a file.

### Expected output

```output
Agent created: image-gen-agent (version 1)
Response status: completed
Output items: 2
```

:::zone-end

## When to use the image generation tool

The image generation tool in Agent Service offers advantages over the Azure OpenAI Image API:

| Advantage | Description |
| --- | --- |
| Streaming | Display partial image outputs during generation to improve perceived latency. |
| Flexible inputs | Accept image file IDs as inputs, in addition to raw image bytes. | 

## Optional parameters

Customize image generation by specifying these optional parameters when you create the tool:

| Parameter | Description |
| --- | --- |
| `size` | Image size. One of `1024x1024`, `1024x1536`, `1536x1024`, or `auto`. |
| `quality` | Image quality. One of `low`, `medium`, `high`, or `auto`. |
| `background` | Background type. One of `transparent`, `opaque`, or `auto`. |
| `output_format` | Output format. One of `png`, `webp`, or `jpeg`. |
| `output_compression` | Compression level for `webp` and `jpeg` output (0-100). |
| `moderation` | Moderation level for the generated image. One of `auto` or `low`. |
| `partial_images` | Number of partial images to generate in streaming mode (0-3). |
| `input_image_mask` | Optional mask for inpainting. Provide `image_url` (base64) or `file_id`. |

> [!NOTE]
> Image generation time varies based on the `quality` setting and prompt complexity. For time-sensitive applications, consider using `quality: "low"` or enabling `partial_images` for streaming.

Use the Responses API if you want to: 

- Build conversational image experiences with GPT Image. 
- Stream partial image results during generation for a smoother user experience. 

## Write effective text-to-image prompts

Effective prompts produce better images. Describe the subject, visual style, and composition you want. Use action words like "draw," "create," or "edit" to guide the model's output.

Content filtering can block image generation if the service detects unsafe content in your prompt. For more information, see [Guardrails and controls overview](../../../guardrails/guardrails-overview.md).

> [!TIP] 
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see [Image prompt engineering techniques](../../../openai/concepts/gpt-4-v-prompt-engineering.md). 

## Verify tool execution

Use either of these approaches to confirm that image generation ran successfully:

- In the response payload, look for an output item with `type` set to `image_generation_call`.
- In the Foundry portal, open tracing/debug for your run to confirm the tool call and inspect inputs and outputs.

When image generation succeeds, the response includes an `image_generation_call` output item with a `result` field containing base64-encoded image data.

If you see only text output and no `image_generation_call` item, the request might not be routed to image generation. Review the troubleshooting section.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Image generation fails | Missing deployment | Verify both the orchestrator model (for example, `gpt-4o`) and `gpt-image-1` deployments exist in the same Foundry project. |
| Image generation fails | Missing or incorrect header | Verify the header `x-ms-oai-image-generation-deployment` is present on the Responses request and matches your image generation deployment name. |
| Agent uses wrong deployment | Model name misconfiguration | Confirm the orchestrator model name in your agent definition differs from the image generation deployment name. |
| Prompt doesn't produce an image | Content filtering blocked the request | Check content filtering logs. See [Guardrails and controls overview](../../../guardrails/guardrails-overview.md) for guidelines on acceptable prompts. |
| Tool not available | Regional or model limitation | Confirm the image generation tool is available in your region and with your orchestrator model. See [Best practices for using tools](../../concepts/tool-best-practice.md). |
| Generated image has low quality | Prompt lacks detail | Provide more specific and detailed prompts describing the desired image style, composition, and elements. |
| Image generation times out | Large or complex image request | Simplify the prompt or increase timeout settings. Consider breaking complex requests into multiple simpler ones. |
| Unexpected image content | Ambiguous prompt | Refine your prompt to be more specific. Include negative prompts to exclude unwanted elements. |

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Image generation in Azure OpenAI](../../../openai/how-to/dall-e.md)
- [Responses API in Azure OpenAI](../../../openai/how-to/responses.md)
- [Guardrails and controls overview](../../../guardrails/guardrails-overview.md)
