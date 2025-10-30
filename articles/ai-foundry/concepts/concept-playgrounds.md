---
title: Azure AI Foundry Playgrounds
titleSuffix: Azure AI Foundry
description: Learn how to use Azure AI Foundry playgrounds for rapid prototyping, experimentation, and validation with AI models before production deployment.
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 09/22/2025
ms.author: mopeakande
author: msakande
ms.reviewer: tgokal
manager: nitinme
reviewer: tgokal
ms.custom: build-2025 ai-assisted
#CustomerIntent: As a developer, I want to use Azure AI Foundry playgrounds for rapid prototyping and experimentation with AI models and agents so that I can validate ideas, test API behavior, and optimize prompts before writing production code.
---

# Azure AI Foundry Playgrounds

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

As you build with state-of-the-art models and create agents and apps with them, Azure AI Foundry playgrounds provide an on-demand, zero-setup environment designed for rapid prototyping, API exploration, and technical validation before you commit a single line of code to your production codebase.

## Highlights of the Azure AI Foundry playgrounds experience

Some highlights of the Azure AI Foundry playgrounds experience include:

- **AgentOps support** for Evaluations and Tracing in the **Agents playground.**
- **Open in VS Code** for Chat and Agents playground. This feature saves you time by automatically importing your endpoint and key from Azure AI Foundry to VS Code for multilingual code samples.
- **Images Playground 2.0** for models such as [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai/?cid=learnDocs), [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai/?cid=learnDocs), and [FLUX.1-Kontext-pro](https://ai.azure.com/resource/models/Flux.1-Kontext-pro/version/1/registry/azureml-blackforestlabs/?cid=learnDocs) models.
- **Audio playground** for models such as [gpt-4o-audio-preview](https://ai.azure.com/resource/models/gpt-4o-audio-preview/version/2024-12-17/registry/azure-openai/?cid=learnDocs), [gpt-4o-transcribe](https://ai.azure.com/explore/models/gpt-4o-transcribe/version/2025-03-20/registry/azure-openai/?cid=learnDocs), and [gpt-4o-mini-tts](https://ai.azure.com/explore/models/gpt-4o-mini-tts/version/2025-03-20/registry/azure-openai/?cid=learnDocs) models.
- **Video playground** for [Azure OpenAI Sora](https://ai.azure.com/resource/models/sora/version/2025-05-02/registry/azure-openai/?cid=learnDocs).

:::image type="content" source="../media/concept-playgrounds/playground-landing-page.png" alt-text="Screenshot of the Azure AI Foundry playground landing page showcasing features for rapid prototyping and experimentation. The left pane of the portal has been customized to show the Playgrounds tab." lightbox="../media/concept-playgrounds/playground-landing-page.png":::

> [!TIP]
> In the screenshot of the playground landing page, the left pane of the portal is customized to show the Playgrounds tab. To learn more about seeing the other items in the left pane, see [Customize the left pane](../what-is-azure-ai-foundry.md#left-pane).

## Playgrounds as the prelude to production

Modern development involves working across multiple systems—APIs, services, SDKs, and data models—often before you're ready to fully commit to a framework, write tests, or spin up infrastructure. As the complexity of software ecosystems increases, the need for safe, lightweight environments to validate ideas becomes critical. The playgrounds are built to meet this need.

The Azure AI Foundry playgrounds provide ready-to-use environments with all the necessary tools and features preinstalled, so you don't need to set up projects, manage dependencies, or solve compatibility issues. The playgrounds can *accelerate developer velocity* by validating API behavior, going quicker to code, reducing cost of experimentation and time to ship, accelerating integration, optimizing prompts, and more.

Playgrounds also *provide clarity quickly* when you have questions, by providing answers in seconds—rather than hours—and allowing you to test and validate ideas before you commit to building at scale. For example, the playgrounds are ideal for quickly answering questions like:

- What's the minimal prompt I need to get the output I want?
- Will this logic work before I write a full integration?
- How does latency or token usage change with different configurations?
- What model provides the best price-to-performance ratio before I evolve it into an agent?

## Open in VS Code capability

The **Chat playground** and **Agents playground** let you work in VS Code by using the **Open in VS Code** button. You can find this button through the Azure AI Foundry extension in VS Code. 

Available on the multilingual sample code samples, **Open in VS Code** automatically imports your code sample, API endpoint, and key to a VS Code workspace in an `/azure` environment. This functionality makes it easy to work in the VS Code IDE from the Azure AI Foundry portal.

To use the **Open in VS Code** functionality from the chat and agents playgrounds, follow these steps:

1. Select **Try the Chat playground** to open it. Alternatively, you can follow these steps in the Agents playground by selecting **Let's go** on the Agents playground card.

1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-mini`.

1. Make sure your deployment is selected in the Deployment box.

1. Select **View code** to see the code sample.

1. Select **Open in VS Code** to open VS Code in a new tab of your browser window.

1. You're redirected to the `/azure` environment of VS Code where your code sample, API endpoint, and key are already imported from the Azure AI Foundry playground.

1. Browse the `INSTRUCTIONS.md` file for instructions to run your model.

1. View your code sample in the `run_model.py` file.

1. View relevant dependencies in the `requirements.txt` file.


## Agents playground

The agents playground lets you explore, prototype, and test agents without running any code. From this page, you can quickly iterate and experiment with new ideas. To get started with the agents playground, see the [Quickstart: Create a new agent](../../ai-services/agents/quickstart.md).


## Chat playground

The chat playground is the place to test the latest reasoning models from Azure OpenAI, DeepSeek, and Meta. To learn more about the chat playground, see the [Quickstart: Get answers in the chat playground](../quickstarts/get-started-playground.md).

For all reasoning models, the chat playground provides a chain-of-thought summary drop-down that lets you see how the model thinks through its response before sharing the output.


## Audio playground

The audio playground (preview) lets you use text-to-speech and transcription capabilities with the latest audio models from Azure OpenAI.

To try the text-to-speech capability, follow these steps:

1. Select **Try the Audio playground** to open it.

1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-mini-tts`.

1. Make sure your deployment is selected in the Deployment box.

1. Input a text prompt.

1. Adjust model parameters such as voice and response format.

1. Select **Generate** to receive a speech output with playback controls that include play, rewind, forward, adjust speed, and volume.

1. Download the audio file to your local computer.

To try the transcription capability, follow these steps:

1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-transcribe`.

1. Make sure your deployment is selected in the Deployment box. 

1. (Optional) Include a phrase list as a text mechanism to guide your audio input.

1. Input an audio file, by either uploading one or recording the audio from the prompt bar.

1. Select **Generate transcription** to send the audio input to the model and receive a transcribed output in both text and JSON formats.


## Video playground

The video playground (preview) is your rapid iteration environment for exploring, refining, and validating generative video workflows. It's designed for developers who need to go from idea to prototype with precision, control, and speed. The playground gives you a low-friction interface to test prompt structures, assess motion fidelity, evaluate model consistency across frames, and compare outputs across models—without writing boilerplate or wasting compute cycles. It's also a great demo interface for your chief product officer and engineering VP.

All model endpoints are integrated with **Azure AI Content Safety**. As a result, the video playground filters out harmful and unsafe images before they appear. If content moderation policies flag your text prompt or video generation, you get a warning notification.

You can use the video playground with the **Azure OpenAI Sora** model.

> [!TIP]  
> See the DevBlog for [Sora and video playground in Azure AI Foundry](https://devblogs.microsoft.com/foundry/sora-in-video-playground/).

Follow these steps to use the video playground:

> [!CAUTION]
> Videos you generate are retained for 24 hours due to data privacy. Download videos to your local computer for longer retention.

1. Select **Try the Video playground** to open it.

1. If you don't have a deployment already, select **Deploy now** from the top right side of the homepage and deploy the `sora` model.

1. On the homepage of the video playground, get inspired by **pre-built prompts** sorted by the **industry** filter. From here, you can view the videos in full display and copy the prompt from the bottom right corner of a video to build from it.

1. Copy the prompt to paste it in the prompt bar. Adjust key controls (for example, aspect ratio or resolution) to deeply understand specific model responsiveness and constraints.

1. Select **Generate** to generate a video based on the copied prompt.

1. Rewrite your text prompt syntax with gpt-4o by using **Re-write with AI**. 

1. Switch on the **Start with an industry system prompt** capability, choose an industry, and specify the change required for your original prompt.

1. Select **Update** to update the prompt, and then select **Generate** to create a new video.

1. Go to the **Generation history** tab to review your generations as a grid or list view. When you select the videos, you open them in full screen mode for full immersion. Visually observe outputs across prompt tweaks or parameter changes.

1. In full screen mode, edit the prompt and submit it for regeneration.

1. Either in full screen mode or through the options button that shows up when you hover across the video, download the videos to your local computer, view the video generation information tag, view code, or delete the video.

1. Select **View code**  from the options menu to view contextual sample code for your video generations in several languages, including Python, JavaScript, C#, JSON, Curl, and Go.  

1. Port the code samples to production by copying them into VS Code.

   
### What to validate when experimenting in video playground

When you use the video playground to plan your production workload, explore and validate the following attributes:

- **Prompt-to-Motion Translation**
    - Does the video model interpret your prompt in a way that makes logical and temporal sense?
    - Is motion coherent with the described action or scene?
- **Frame Consistency**
    - Do characters, objects, and styles remain consistent across frames?
    - Are there visual artifacts, jitter, or unnatural transitions?
- **Scene Control**
    - How well can you control scene composition, subject behavior, or camera angles?
    - Can you guide scene transitions or background environments?

- **Length and Timing**
    - How do different prompt structures affect video length and pacing?
    - Does the video feel too fast, too slow, or too short?

- **Multimodal Input Integration**
    - What happens when you provide a reference image, pose data, or audio input?
    - Can you generate video with lip-sync to a given voiceover?

- **Post-Processing Needs**
    - What level of raw fidelity can you expect before you need editing tools?
    - Do you need to upscale, stabilize, or retouch the video before using it in production?

- **Latency and Performance**
    - How long does it take to generate video for different prompt types or resolutions?
    - What's the cost-performance tradeoff of generating 5-second versus 15-second clips?


## Images playground

The images playground is ideal for developers who build image generation flows. This playground is a full-featured, controlled environment for high-fidelity experiments designed for model-specific APIs to generate and edit images.

> [!TIP]  
> See the [60-second reel of the Images playground for gpt-image-1](https://youtu.be/btA8njJjLXY) and our DevBlog for [Images Playground in Azure AI Foundry.](https://devblogs.microsoft.com/foundry/images-playground-may-2025/)

You can use the images playground with these models:

- [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai) and [dall-e-3](https://ai.azure.com/resource/models/dall-e-3/version/3.0/registry/azure-openai/?cid=learnDocs) from Azure OpenAI.
- [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai), [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai), [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai) from Stability AI.
- [FLUX.1-Kontext-pro](https://ai.azure.com/explore/models/FLUX.1-Kontext-pro/version/1/registry/azureml-blackforestlabs/?cid=learnDocs) and [FLUX-1.1-pro](https://ai.azure.com/explore/models/FLUX-1.1-pro/version/1/registry/azureml-blackforestlabs/?cid=learnDocs) from Black Forest Labs.

Follow these steps to use the images playground:

1. Select **Try the Images playground** to open it.

1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-image-1`.

1. **Start with a sample text prompt**: Select an option to get started with a prebuilt text prompt that automatically fills the prompt bar.

1. **Explore the model API-specific generation controls after model deployment:** Adjust key controls (for example, number of variants, quality, strength) to deeply understand specific model responsiveness and constraints.

1. Select **Generate**.

1. **Side-by-side observations in grid view:** Visually observe outputs across prompt tweaks or parameter changes.

1. **Transform with API tooling:** Inpainting with text transformation is available for gpt-image-1. Alter parts of your original image with inpainting selection. Use text prompts to specify the change.

1. **Port to production with multi-lingual code samples:** Use Python, Java, JavaScript, C# code samples with "View Code". Images playground is your launchpad to development work in VS Code.

### What to validate when experimenting in images playground

By using the images playground, you can explore and validate the following aspects as you plan your production workload:

- **Prompt Effectiveness**
    - What kind of visual output does this prompt generate for my enterprise use case?
    - How specific or abstract can my language be and still get good results?
    - Does the model understand style references like "surrealist" or "cyberpunk" accurately?

- **Stylistic Consistency**
    - How do I maintain the same character, style, or theme across multiple images?
    - Can I iterate on variations of the same base prompt with minimal drift?

- **Parameter Tuning**
    - What's the effect of changing model parameters like guidance scale, seed, steps, and others?
    - How can I balance creativity versus prompt fidelity?

- **Model Comparison**
    - How do results differ between models, such as SDXL versus DALL·E?
    - Which model performs better for realistic faces versus artistic compositions?

- **Composition Control**
    - What happens when I use spatial constraints like bounding boxes or inpainting masks?
    - Can I guide the model toward specific layouts or focal points?

- **Input Variation**
    - How do slight changes in prompt wording or structure impact results?
    - What's the best way to prompt for symmetry, specific camera angles, or emotions?

- **Integration Readiness**
    - Will this image meet the constraints of my product's UI, including aspect ratio, resolution, and content safety?
    - Does the output conform to brand guidelines or customer expectations?


## Related content

- [Use the chat playground in Azure AI Foundry portal](../quickstarts/get-started-playground.md)
- [Quickstart: Create a new agent (Preview)](../../ai-services/agents/quickstart.md)
- [Basic Azure AI Foundry chat reference architecture](/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat)
