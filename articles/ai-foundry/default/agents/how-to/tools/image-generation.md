---
title: Use the image generation tool in Foundry Agent Service (preview)
titleSuffix: Microsoft Foundry
description: Learn how to generate images from text prompts in Microsoft Foundry Agent Service by using the image generation tool with gpt-image-1. Configure agents, deploy models, and save output.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom: dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
ms.date: 02/04/2026
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-image-generation
---

# Use the image generation tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!IMPORTANT] 
> - The image generation tool requires the `gpt-image-1` model. See the [Azure OpenAI transparency note](../../../../responsible-ai/openai/transparency-note.md?tabs=image) for limitations and responsible AI considerations.
> - You also need a compatible orchestrator model (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, or `gpt-5` series) deployed in the same Foundry project.

The **image generation tool** in Microsoft Foundry Agent Service generates images from text prompts in conversations and multistep workflows. Use it to create AI-generated visuals and return base64-encoded output that you can save to a file.

## Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An Azure account with an active subscription.
- A Foundry project.
- A basic or standard agent environment. See [agent environment setup](../../../../agents/environment-setup.md).
- Permissions to create and manage agent versions in the project.
- Two model deployments in the same Foundry project:
  - A compatible Azure OpenAI model deployment for the agent (for example, `gpt-4o`).
  - An image generation model deployment (`gpt-image-1`).

Set these environment variables for the samples:

- `FOUNDRY_PROJECT_ENDPOINT`
- `FOUNDRY_MODEL_DEPLOYMENT_NAME`
- `IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME`

## Configure the image generation tool

1. Deploy your orchestrator model (for example, `gpt-4o`) to your Foundry project.
1. Deploy `gpt-image-1` to the same Foundry project.
1. Confirm your region and model support for image generation. See [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).
1. Configure the environment variables listed in the prerequisites.

## Code examples

Before you start, install the `azure-ai-projects` package (version 2.0.0b1 or later). For package installation instructions, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true).

:::zone pivot="python"
## Create an agent with the image generation tool

This sample creates an agent with the image generation tool, generates an image, and saves it to a file.

```python
import base64
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, ImageGenTool

project_client = AIProjectClient(
  endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
  credential=DefaultAzureCredential(),
)

with project_client:
  openai_client = project_client.get_openai_client()

  agent = project_client.agents.create_version(
    agent_name="agent-image-generation",
    definition=PromptAgentDefinition(
      model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
      instructions="Generate images based on user prompts.",
      tools=[ImageGenTool(quality="low", size="1024x1024")],
    ),
    description="Agent for image generation.",
  )
  print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

  response = openai_client.responses.create(
    input="Generate an image of the Microsoft logo.",
    extra_headers={
      "x-ms-oai-image-generation-deployment": os.environ["IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME"],
    },
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
  )
  print(f"Response created: {response.id}")

  image_items = [item for item in (response.output or []) if item.type == "image_generation_call"]
  if image_items and getattr(image_items[0], "result", None):
    print("Downloading generated image...")
    file_path = os.path.abspath("microsoft.png")
    with open(file_path, "wb") as f:
      f.write(base64.b64decode(image_items[0].result))
    print(f"Image downloaded and saved to: {file_path}")
  else:
    print("No image data found in the response.")

  project_client.agents.delete_version(agent.name, agent.version)
  print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"
## Sample for image generation in Azure.AI.Projects.OpenAI.

In this example, you generate an image based on a simple prompt. The code in this example is synchronous. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample2_Image_Generation.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
// Read the environment variables
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
var imageGenerationDeploymentName = System.Environment.GetEnvironmentVariable("IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME");

// Create the AI Project client with custom header policy
AIProjectClientOptions projectOptions = new();
projectOptions.AddPolicy(new HeaderPolicy(imageGenerationDeploymentName), PipelinePosition.PerCall);

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
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
Instructions = "Generate images based on user prompts.",
Tools = {
        ResponseTool.CreateImageGenerationTool(
            model: imageGenerationDeploymentName,
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

The following example creates an agent that uses the image generation tool.

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Test agent for image generation capabilities",
  "definition": {
  "kind": "prompt",
  "model": "{{model}}",
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
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -H "x-ms-oai-image-generation-deployment: $IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME" \
  -d '{
  "agent": {
    "type": "agent_reference",
    "name": "{{agentVersion.name}}",
    "version": "{{agentVersion.version}}"
  },
  "metadata": {
    "test_response": "image_generation_enabled",
    "test_scenario": "basic_imagegen"
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
  "background": true,
  "stream": false
}'
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
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const imageDeploymentName =
  process.env["IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME"] || "<image generation deployment name>";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with image generation tool...");

  // Create Agent with image generation tool
  const agent = await project.agents.createVersion("agent-image-generation", {
    kind: "prompt",
    model: deploymentName,
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
  console.log("\nGenerating image...");
  const response = await openAIClient.responses.create(
    {
      input: "Generate an image of Microsoft logo.",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
      headers: { "x-ms-oai-image-generation-deployment": imageDeploymentName },
    },
  );
  console.log(`Response created: ${response.id}`);

  // Extract and save the generated image
  const imageData = response.output?.filter((output) => output.type === "image_generation_call");

  if (imageData && imageData.length > 0 && imageData[0].result) {
    console.log("Downloading generated image...");

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
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nImage generation sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

When you run the sample, you see the following output:

```console
Creating agent with image generation tool...
Agent created (id: <agent-id>, name: agent-image-generation, version: 1)
Generating image...
Response created: <response-id>
Downloading generated image...
Image downloaded and saved to: /path/to/microsoft.png
Cleaning up resources...
Agent deleted
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
> Image generation typically takes 10-30 seconds depending on the `quality` setting and prompt complexity. For time-sensitive applications, consider using `quality: "low"` or enabling `partial_images` for streaming.

Use the Responses API if you want to: 

- Build conversational image experiences with GPT Image. 
- Stream partial image results during generation for a smoother user experience. 

## Write effective text-to-image prompts

Effective prompts produce better images. Describe the subject, visual style, and composition you want. Use action words like "draw," "create," or "edit" to guide the model's output.

Content filtering can block image generation if the service detects unsafe content in your prompt. For more information, see [Content filter](../../../../openai/concepts/content-filter.md).

> [!TIP] 
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see [Image prompt engineering techniques](../../../../openai/concepts/gpt-4-v-prompt-engineering.md). 

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
| Agent uses wrong deployment | Environment variable misconfiguration | Confirm `FOUNDRY_MODEL_DEPLOYMENT_NAME` is set to your orchestrator deployment name, not the image generation deployment. |
| Prompt doesn't produce an image | Content filtering blocked the request | Check content filtering logs. See [Content filter](../../../../openai/concepts/content-filter.md) for guidelines on acceptable prompts. |
| Tool not available | Regional or model limitation | Confirm the image generation tool is available in your region and with your orchestrator model. See [Best practices for using tools](../../concepts/tool-best-practice.md). |
| Generated image has low quality | Prompt lacks detail | Provide more specific and detailed prompts describing the desired image style, composition, and elements. |
| Image generation times out | Large or complex image request | Simplify the prompt or increase timeout settings. Consider breaking complex requests into multiple simpler ones. |
| Unexpected image content | Ambiguous prompt | Refine your prompt to be more specific. Include negative prompts to exclude unwanted elements. |

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Image generation in Azure OpenAI](../../../../openai/how-to/dall-e.md)
- [Responses API in Azure OpenAI](../../../../openai/how-to/responses.md)
- [Content filter](../../../../openai/concepts/content-filter.md)
