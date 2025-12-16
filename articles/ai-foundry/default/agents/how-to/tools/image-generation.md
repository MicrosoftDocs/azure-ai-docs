---
title: Use Foundry Agent Service with image generation
titleSuffix: Microsoft Foundry
description: Create Foundry Agents with image generation. Stream partial images, generate visuals from text prompts, and integrate GPT models. Get started now.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom: dev-focus
ai-usage: ai-assisted
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-image-generation
---

# Use the image generation tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!IMPORTANT] 
> - The Image Generation tool uses the `gpt-image-1` model.  Learn more about intended uses, capabilities, limitations, risks, and considerations when choosing a use case model in the [Azure OpenAI transparency note](/azure/ai-foundry/responsible-ai/openai/transparency-note?tabs=image).
> - You also need to deploy a compatible Azure OpenAI model in the same Foundry project that you're using. Compatible models include `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, and `gpt-5` series models.

The Foundry Agent Service enables image generation by using the image generation tool in conversations and multistep workflows. It supports image inputs and outputs within context and includes built-in tools for generating and editing images. 

## Prerequisites

- An Azure account with an active subscription.
- A Foundry project.
- Permissions to create and manage agent versions in the project.
- Two model deployments in the same Foundry project:
  - A compatible Azure OpenAI model deployment for the agent (for example, `gpt-4o`).
  - An image generation model deployment (`gpt-image-1`).
- The environment variables used by the sample you run (names vary by SDK and language):
  - `FOUNDRY_PROJECT_ENDPOINT`
  - `FOUNDRY_MODEL_DEPLOYMENT_NAME`
  - `IMAGE_GENERATION_DEPLOYMENT_NAME`
  - `IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME`

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Code examples

Before you start, make sure you have the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate).

:::zone pivot="python"
## Create an agent with the image generation tool

The following example creates an agent that uses the image generation tool with low quality and 1024x1024 size.

```python
with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="Generate images based on user prompts",
            tools=[ImageGenTool(quality="low", size="1024x1024")],
        ),
        description="Agent for image generation.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

## Create a response 

```python
    response = openai_client.responses.create(
        input="Generate an image of Microsoft logo.",
        extra_headers={
            "x-ms-oai-image-generation-deployment": "gpt-image-1"
        },  # this is required at the moment for image generation
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response created: {response.id}")
```

## Save the image

```python
    # Save the image to a file
    image_data = [output.result for output in response.output if output.type == "image_generation_call"]

    if image_data and image_data[0]:
        print("Downloading generated image...")
        filename = "microsoft.png"
        file_path = os.path.abspath(filename)

        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data[0]))

        print(f"Image downloaded and saved to: {file_path}")
```
:::zone-end

:::zone pivot="csharp"
## Sample for image generation in Azure.AI.Projects.OpenAI.

In this example, you generate an image based on a simple prompt. The code in this example is synchronous. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample2_Image_Generation.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
// Read the environment variables
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
var imageGenerationModelName = System.Environment.GetEnvironmentVariable("IMAGE_GENERATION_DEPLOYMENT_NAME");

// Create the AI Project client with custom header policy
AIProjectClientOptions projectOptions = new();
projectOptions.AddPolicy(new HeaderPolicy(imageGenerationModelName), PipelinePosition.PerCall);

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
// Supported image generation models are gpt-image-1 and gpt-image-1-mini.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "Generate images based on user prompts.",
    Tools = {
        ResponseTool.CreateImageGenerationTool(
            model: imageGenerationModelName,
            quality: ImageGenerationToolQuality.Low,
            size:ImageGenerationToolSize.W1024xH1024
        )
    }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

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

// Use the policy to create the `OpenAIClient` object and create
// the `ResponsesClient` by asking the Agent to generate the image.
ProjectOpenAIClientOptions options = new();
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
```

### Expected output

The following output is expected when you run the sample:

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
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
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
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'x-ms-oai-image-generation-deployment: gpt-image-1' \
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

This sample demonstrates how to create an AI agent with image generation capabilities using the `ImageGenTool` and synchronous Azure AI Projects client. The agent can generate images based on text prompts and save them to files. For a JavaScript example, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentImageGeneration.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["IMAGE_GENERATION_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

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

The following output is expected when you run the sample:

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

Compared to Azure OpenAI's Image API, the image generation tool in Agent Service offers several advantages: 

**Streaming**: Display partial image outputs during generation to improve perceived latency. 

**Flexible inputs**: Accept image file IDs as inputs, in addition to raw image bytes. 

## Optional parameters

| Parameter | Description |
|---------|---------|
|size     | Specifies the image dimensions, such as 1024x1024. The default value is "auto".        |
|quality     | Specifies the rendering quality, such as low, medium, high. The default value is "auto".         |
|format     | File output format. Supported formats are "png", "WebP", and "jpeg".         |
|compression     | The compression level for jpeg and webp format images. The value is in the range of 0 to 100 (%).        |
|background     |  Either "transparent", "opaque", or "auto".       |
|partial images     |  Supports streaming partial images. You can set the number to be in the range of 1 to 3.       |

Use the Responses API if you want to: 

- Build conversational image experiences with GPT Image. 
- Stream partial image results during generation for a smoother user experience. 

## Best practices for writing text-to-image prompts  

Your prompts should describe the content you want to see in the image, and the visual style of the image. You can use terms like "draw" or "edit" in your prompt. 

When you write prompts, consider that the Image APIs include a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filter](../../../../openai/concepts/content-filter.md). 

> [!TIP] 
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see [Image prompt engineering techniques](../../../../openai/concepts/gpt-4-v-prompt-engineering.md). 
