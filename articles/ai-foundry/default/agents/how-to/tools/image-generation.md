---
title: 'How to use Foundry Agent Service with image generation'
titleSuffix: Microsoft Foundry
description: Learn how to use Azure AI Agents with image generation.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/12/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-image-generation
---



# Image generation tool (preview) 

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!IMPORTANT] 
> - The Image Generation tool is powered by the `gpt-image-1` model.  Learn more about intended uses, capabilities, limitations, risks, and considerations when choosing a use case model in the [Azure OpenAI transparency note](/azure/ai-foundry/responsible-ai/openai/transparency-note?tabs=image).
> - You also need to have a compatible Azure OpenAI model deployed in the same Foundry project that you are using, including `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, and `gpt-5` series models.

The Foundry Agent Service enables image generation as part of conversations and multi-step workflows. It supports image inputs and outputs within context and includes built-in tools for generating and editing images. 

:::zone pivot="python"
Before you start, make sure you have the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

## Create an agent with the image generation tool
```python
with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
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

:::zone pivot="rest-api"
## Create an agent with the image generation tool
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
  -H 'Content-Type: applicat ion/json' \
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

## When to use the image generation tool

Compared to Azure OpenAI's Image API, the image generation tool in Agent Service offers several advantages: 

**Streaming**: Display partial image outputs during generation to improve perceived latency. 

**Flexible inputs**: Accept image file IDs as inputs, in addition to raw image bytes. 

## Optional parameters

|Parameter  |Description  |
|---------|---------|
|size     | Specifies the image dimensions, such as 1024x1024. The default value is "auto".        |
|quality     | Specifies the rendering quality, such as low, medium, high. The default value is "auto".         |
|format     | file output format, it supports "png", "WebP" and "jpeg".         |
|compression     | the compression level for jpeg and webp format images, the value is in the range of 0 to 100 (%)        |
|background     |  Either "transparent", "opaque" or "auto".       |
|partial images     |  Supports streaming partial images. you can set the number to be in the range of 1 to 3.       |

Use the Responses API if you want to: 

* Build conversational image experiences with GPT Image. 
* Stream partial image results during generation for a smoother user experience. 

## Best practices for writing text-to-image prompts  

Your prompts should describe the content you want to see in the image, and the visual style of image. You can use terms like "draw" or "edit" in your prompt. 

When you write prompts, consider that the Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filter](../../../../openai/concepts/content-filter.md). 

> [!TIP] 
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see [Image prompt engineering techniques](../../../../openai/concepts/gpt-4-v-prompt-engineering.md). 
