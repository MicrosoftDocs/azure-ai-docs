---
title: Azure AI Foundry Playgrounds
titleSuffix: Azure AI Foundry
description: Learn to use Azure AI Foundry playgrounds for exploration, experimentation, and iteration with different models.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-articl
ms.date: 06/09/2025
ms.reviewer: mopeakande
reviewer: msakande
ms.author: tgokal
author: tgokal
ms.custom: build-2025 ai-assisted
#customer intent: I'm a developer and want to use Azure AI Foundry Playground for quick experimentation and prototyping with models and agents before going to code.
---

# Azure AI Foundry Playgrounds

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

As you build with state-of-the-art models and build agents and apps with them, Azure AI Foundry playgrounds provide an on-demand, zero-setup environment designed for rapid prototyping, API exploration, and technical validation before you commit a single line of code to your production codebase.

## Some highlights of the Azure AI Foundry playgrounds experience

Some highlights of the Azure AI Foundry playground experience includes:

- **AgentOps support** for Evaluations and Tracing in the **Agents playground.**
- **Open in VS Code** for Chat and Agents playground. This feature saves you time by automatically importing your endpoint and key from Azure AI Foundry to VS Code for multi-lingual code samples.
- **Images Playground 2.0** for [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai), [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai) and [Bria 2.3 Fast](https://ai.azure.com/explore/models/Bria-2.3-Fast/version/1/registry/azureml-bria) models.
- **Audio playground** for [gpt-4o-audio](https://ai.azure.com/explore/models/gpt-4o-transcribe/version/2025-03-20/registry/azure-openai), [gpt-4o-transcribe](https://ai.azure.com/explore/models/gpt-4o-transcribe/version/2025-03-20/registry/azure-openai), and [gpt-4o-mini-tts](https://ai.azure.com/explore/models/gpt-4o-mini-tts/version/2025-03-20/registry/azure-openai) models.
- **Video playground** for Azure OpenAI Sora.

:::image type="content" source="../media/concept-playgrounds/playground-landing-page.png" alt-text="Screenshot of the Azure AI Foundry playground landing page showcasing features for rapid prototyping and experimentation. The left pane of the portal has been customized to show the Playgrounds tab." lightbox="../media/concept-playgrounds/playground-landing-page.png":::

> [!TIP]
> In the screenshot of the playground landing page, the left pane of the portal has been customized to show the Playgrounds tab. To learn more about seeing the other items in the left pane, see [Customize the left pane](../what-is-azure-ai-foundry.md#left-pane).

## Playgrounds as the prelude to production

Modern development involves working across multiple systems—APIs, services, SDKs, and data models—often before you're ready to fully commit to a framework, write tests, or spin up infrastructure. As the complexity of software ecosystems increases, the need for safe, lightweight environments to validate ideas becomes critical. The playgrounds were built to meet this need.

The playgrounds provide ready-to-use environments with all the necessary tools and features pre-installed, eliminating the need to set up projects, manage dependencies, or solve compatibility issues. The Azure AI Foundry playgrounds help provide clarity quickly when you have questions and they can accelerate developer velocity.

#### Get clarity quicker

The playgrounds are ideal for quickly answering questions like:

- How does this endpoint behave under edge conditions?

- What's the minimal prompt I need to get the output I want?

- Will this logic work before I write a full integration?

- How does latency or token usage change with different configurations?

- What model provides the best price-to-performance ratio before I evolve it into an agent?

- How do I evaluate performance and safety metrics for my agent?
  
The playgrounds help you to get answers to these questions in seconds, rather than hours—allowing you to test and validate ideas before you commit to building at scale. 

#### Accelerate developer velocity

- **Reduce cost of experimentation:** In traditional workflows, the cost of experimentation is high, as it includes setting up the project, writing scaffolding code, waiting on builds, and rolling back changes. This cost makes many developers to skip the experiment phase entirely, which leads to brittle assumptions, broken behavior, or inefficient code. The playgrounds change this dynamic by removing risk from experimentation, so you can validate before you invest. Playgrounds also act as the bridge between development and documentation. The examples you build in the playgrounds often become the reference points for future code, internal tooling, or user education.
 
- **Iterate faster:** Experiment with text prompts, adjust generation parameters, and explore editing variations — all in real time with model-specific native API support.

- **Accelerate integration:** Validate API behavior, test edge cases, and inspect responses directly in an interactive console.

- **Optimize prompts:** Debug and tune prompts; build prompt variations available in the playgrounds and grounded in model behavior.

- **Provide a consistent model interface:** Common foundations established. No matter what model or agent, no matter the model provider.

- **Go to code quicker:** Using the "View Code" multi-lingual code samples for your output, prompts and generation controls within the API structure, what you create within Azure AI Foundry playgrounds can be easily ported into VS Code—with predictability and repeatability.

- **Reduce time to ship:** No need to find, build, or configure a custom UI to localhost just for image generation, hope that it automatically works for the next state-of-the-art model, or spend time resolving cascading build errors due to packages or code changes required for new models. The images playground in Azure AI Foundry gives you version-aware access. Build with the latest and most performant models with API updates surfaced in a consistent UI.

- **Collaborate and get feedback easily:** Share your visual experiments directly with stakeholders, artists, or product managers, without requiring them to install tools.

- **Provides human-in-the-loop refinement:** You can explore subtle tweaks with immediate visual feedback before hardcoding or automating anything.

Whether you're prototyping with the latest LLM from Azure AI Foundry Models, validating prompts for edge cases, or optimizing output consistency, Azure AI Foundry playgrounds remove friction from early experimentation. It's where ideas are pressure-tested before they're shipped into production. Optimize for prompt adherence, latency, and use cases through experimentation; accelerate your "Build-Measure-Learn" development loop; and ship faster with higher confidence.


## Open in VS Code capability

The **Chat playground** and **Agents playground** allow you to work in VS Code, by using the **Open in VS Code** button that's available through the Azure AI Foundry extension in VS Code. 

Available on the multi-lingual sample code samples, "Open in VS Code" enables the automatic import of your code sample, API endpoint, and key to a VS Code workspace in an `/azure` environment. This functionality makes it easy to work in the VS Code IDE from the Azure AI Foundry portal.

Follow these steps to use the "Open in VS Code" functionality from the chat and agents playgrounds:

1. Select **Try the Chat playground** to open it. Alternatively, you could follow these steps in the Agents playground by selecting **Let's go** on the Agents playground card.
1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-mini`.
1. Ensure that your deployment is selected in the Deployment box.
1. Select **View code** to see the code sample.
1. Select **Open in VS Code** to open VS Code in a new tab of your browser window.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-foundry.png" alt-text="Screenshot showing the Open in VS Code button in Azure AI Foundry playground for seamless code integration." lightbox="../media/concept-playgrounds/open-in-vs-code-foundry.png":::

1. You're redirected to the `/azure` environment of VS Code where your code sample, API endpoint and key are already imported from the Azure AI Foundry playground.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-vscode.png" alt-text="Screenshot of the VS Code environment showing imported code sample, API endpoint, and key from the Azure AI Foundry playground." lightbox="../media/concept-playgrounds/open-in-vs-code-vscode.png":::

1. Browse the `READ.ME` file for instructions to run your model.
1. View your code sample in the `run_model.py`.
1. View relevant dependencies in the `requirements.txt` file.


## Agents playground

The agents playground allows you to explore, prototype, and test agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas. to get started with the Agents playground, see the [Quickstart: Create a new agent](../../ai-services/agents/quickstart.md).

:::image type="content" source="../media/concept-playgrounds/agents-playground.png" alt-text="Screenshot of the agents playground interface for exploring, prototyping, and testing agents without code." lightbox="../media/concept-playgrounds/agents-playground.png":::

## Chat playground

The chat playground is the place to test the latest reasoning models from Azure OpenAI, DeepSeek, and Meta. To learn more about the chat playground, see the [Quickstart: Use the chat playground in Azure AI Foundry portal](../quickstarts/get-started-playground.md).

For all reasoning models, the chat playground provides a chain-of-thought summary drop-down that let's you see how the model was thinking through its response ahead of sharing the output.

:::image type="content" source="../media/concept-playgrounds/chat-playground-cot-summary.png" alt-text="Screenshot of the Chat playground interface for exploring, prototyping, and testing chat models without code." lightbox="../media/concept-playgrounds/chat-playground-cot-summary.png":::

## Audio playground

The audio playground (preview) let's you use text-to-speech and transcription capabilities with the latest audio models from Azure OpenAI.

Follow these steps to try the text to speech capability:

1. Select **Try the Audio playground** to open it.
1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-mini-tts`.
1. Ensure that your deployment is selected in the Deployment box.
1. Input a text prompt.
1. Adjust model parameters such as voice and response format.
1. Select **Generate** to receive a speech output with playback controls that include play, rewind, forward, adjust speed, and volume.
1. Download the audio file to your local computer.
    :::image type="content" source="../media/concept-playgrounds/audio-playground-text-to-speech.png" alt-text="Screenshot of the Audio playground interface showcasing text-to-speech capabilities with playback controls." lightbox="../media/concept-playgrounds/audio-playground-text-to-speech.png":::

Follow these steps to try the transcription capability:

1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-4o-transcribe`.
1. (Optional) Include a phrase list as a text mechanism to guide your audio input.
1. Input an audio file, by either uploading one or recording the audio from the prompt bar.
1. Select **Generate transcription** to send the audio input to the model and receive a transcribed output in both text and JSON formats.
    :::image type="content" source="../media/concept-playgrounds/audio-playground-transcribe.png" alt-text="Screenshot of the Audio playground interface demonstrating transcription output from audio input." lightbox="../media/concept-playgrounds/audio-playground-transcribe.png":::

## Images playground

The images playground is ideal for developers who build image generation flows. This playground is a full-featured, controlled environment for high-fidelity experiments designed for model-specific APIs to generate and edit images.

> [!TIP]  
> See the [60-second reel of the Images playground for gpt-image-1](https://youtu.be/btA8njJjLXY) and our DevBlog for how to transform your [enterprise-ready use case by industry.](https://devblogs.microsoft.com/foundry/images-playground-may-2025/)

You can use the images playground with these models:

- [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai) from Azure OpenAI.
- [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai), [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai), [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai) from Stability AI.
- [Bria 2.3 Fast](https://ai.azure.com/explore/models/Bria-2.3-Fast/version/1/registry/azureml-bria) from Bria AI.

Follow these steps to use the images playground:

1. Select **Try the Images playground** to open it.
1. If you don't have a deployment already, select **Create new deployment** and deploy a model such as `gpt-image-1`.
1. **Start with a pre-built text prompt**: Select an option to get started with a prebuilt text prompt that automatically fills the prompt bar.
1. **Explore the model API-specific generation controls after model deployment:** Adjust key controls (e.g. number of variants, quality, strength) to deeply understand specific model responsiveness and constraints.
1. **Side-by-side observations in grid view:** Visually observe outputs across prompt tweaks or parameter changes.
1. **Transform with API tooling:** Inpainting with text transformation is available for gpt-image-1. Alter parts of your original image with inpainting selection. Use text prompts to specify the change.
1. **Port to production with multi-lingual code samples:** Use Python, Java, JavaScript, C# code samples with "View Code". Images playground is your launchpad to development work in VS Code.

### What to validate when experimenting in Images playground

By using the images playground, you can explore and validate the following as you plan your production workload:

- **Prompt Effectiveness**
    - What kind of visual output does this prompt generate for my enterprise use case?
    - How specific or abstract can my language be and still get good results?
    - Does the model understand style references like "surrealist" or "cyberpunk" accurately?

- **Stylistic Consistency**
    - How do I maintain the same character, style, or theme across multiple images?
    - Can I iterate on variations of the same base prompt with minimal drift?

- **Parameter Tuning**
    - What's the effect of changing model parameters like guidance scale, seed, steps, etc.?
    - How can I balance creativity vs. prompt fidelity?

- **Model Comparison**
    - How do results differ between models (e.g., SDXL vs. DALL·E)?
    - Which model performs better for realistic faces vs. artistic compositions?

- **Composition Control**
    - What happens when I use spatial constraints like bounding boxes or inpainting masks?
    - Can I guide the model toward specific layouts or focal points?

- **Input Variation**
    - How do slight changes in prompt wording or structure impact results?
    - What's the best way to prompt for symmetry, specific camera angles, or emotions?

- **Integration Readiness**
    - Will this image meet the constraints of my product's UI (aspect ratio, resolution, content safety)?
    - Does the output conform to brand guidelines or customer expectations?


## Video playground

The video playground (preview) is your rapid iteration environment for exploring, refining, and validating generative video workflows—designed for developers who need to go from idea to prototype with precision, control, and speed. The playground gives you a low-friction interface to test prompt structures, assess motion fidelity, evaluate model consistency across frames, and compare outputs across models—without writing boilerplate or wasting compute cycles. It's aso a great demo interface for your Chief Product Officer and Engineering VP.

You can use the video playground with the **Azure OpenAI Sora** model.

> [!TIP]  
> See the [60-second reel of the video playground for Azure OpenAI Sora](https://aka.ms/VideoPlaygroundReel) and the DevBlog for how to transform your [enterprise-ready use case by industry](https://aka.ms/VideoPlaygroundDevBlog).

Follow these steps to use the video playground:

> [!CAUTION]
> Videos generated are retained for 24 hours due to data privacy. Download videos to your local computer for longer retention.

1. Select **Try the Video playground** to open it.
1. If you don't have a deployment already, select **Deploy now** from the top righ side of the homepage and deploy the `sora` model.
1. On the homepage of the video playground, get inspired by **pre-built prompts** sorted by the **industry** filter. From here, you can view the videos in full display and copy the prompt to build from it.
    :::image type="content" source="../media/concept-playgrounds/video-playground-copy-prompt.png" alt-text="Screenshot of the video playground highlighting the Use prompt button to copy a prompt." lightbox="../media/concept-playgrounds/video-playground-copy-prompt.png":::

1. Copying the prompt pastes it in the prompt bar. Adjust key controls (e.g. aspect ratio, resolution) to deeply understand specific model responsiveness and constraints.

1. Rewrite your text prompt syntax with gpt-4o using **Re-write with AI** with industry based system prompts. Switch on the capability, select the industry and specify the change required for your original prompt.

1. From the Generation history tab, review your generations as a Grid or List view. When you select the videos, open them in full screen mode for full immersion. Visually observe outputs across prompt tweaks or parameter changes.
1. In Full Screen mode, edit the prompt and submit for regeneration.
1. Either in Full Screen mode or through the overflow button, download to local, view the information generation tag, or delete the video.
1. **Port to production with multi-lingual code samples:** Use Python, Java, JavaScript, C# contextual code samples with "View Code" that reflect your generations and copy into VS Code.
1. **Azure AI Content Safety integration:** With all model endpoints integrated with Azure AI Content Safety, harmful and unsafe images are filtered out prior to being surfaced in video playground. If your text prompt and video generation is flagged by content moderation policies, you get a warning notification appear.
   
### Video generation: what you can validate or de-risk

When using the video playground as you plan your production workload, you can explore and validate the following:

- **Prompt-to-Motion Translation**
    - Does the video model interpret my prompt in a way that makes logical and temporal sense?
    - Is motion coherent with the described action or scene?
- **Frame Consistency**
    - Do characters, objects, and styles remain consistent across frames?
    - Are there visual artifacts, jitter, or unnatural transitions?
- **Scene Control**
    - How well can I control scene composition, subject behavior, or camera angles?
    - Can I guide scene transitions or background environments?

- **Length and Timing**
    - How do different prompt structures affect video length and pacing?
    - Does the video feel too fast, too slow, or too short?

- **Multimodal Input Integration**
    - What happens when I provide a reference image, pose data, or audio input?
    - Can I generate video with lip-sync to a given voiceover?

- **Post-Processing Needs**
    - What level of raw fidelity can I expect before I need editing tools?
    - Do I need to upscale, stabilize, or retouch the video before using it in production?

- **Latency & Performance**
    - How long does it take to generate video for different prompt types or resolutions?
    - What's the cost-performance tradeoff of generating 5s vs. 15s clips?

## Related resources
- [Use the chat playground in Azure AI Foundry portal](../quickstarts/get-started-playground.md)
- [Quickstart: Create a new agent (Preview)](../../ai-services/agents/quickstart.md)
