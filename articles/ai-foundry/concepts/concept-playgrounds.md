---
title: Azure AI Foundry Playgrounds
titleSuffix: Azure AI Foundry
description: Learn to use Azure AI Foundry playgrounds for exploration, experimentation, and iteration with different models.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 05/06/2025
ms.reviewer: mopeakande
reviewer: msakande
ms.author: tgokal
author: tgokal
ms.custom: build-2025 ai-assisted
#customer intent: I'm a developer and want to use Azure AI Foundry Playground for quick experimentation and prototyping with models and agents before going to code.
---

# Azure AI Foundry Playgrounds

In today's development cycle, speed and clarity are everything. As you build with the latest state-of-the-art models - and build agents and apps with them - Azure AI Foundry playgrounds are your on-demand, zero-setup environment designed for rapid prototyping, API exploration, and technical validation—before committing a single line to your production codebase. Think of the playground as your technical sketchpad—built to help you build better, faster, and smarter.

> [!IMPORTANT]  
> The Azure AI Foundry playground experience has been updated to include:
>   - **AgentOps support** for Evaluations and Tracing in the **Agents playground.**
>   - **Open in VS Code** for Chat and Agents playground; automatic endpoint and key importing from Foundry to VS Code for multi-lingual code samples. Save time from going from six clicks to  one click.
>   - Introducing **[Images Playground 2.0](https://devblogs.microsoft.com/foundry/images-playground-may-2025/)** for [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai), [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai) and [Bria 2.3 Fast](https://ai.azure.com/explore/models/Bria-2.3-Fast/version/1/registry/azureml-bria).
>   - Revamped **Audio playground** for [gpt-4o-audio](https://ai.azure.com/explore/models/gpt-4o-transcribe/version/2025-03-20/registry/azure-openai), [gpt-4o-transcribe](https://ai.azure.com/explore/models/gpt-4o-transcribe/version/2025-03-20/registry/azure-openai), [gpt-4o-mini-tts](https://ai.azure.com/explore/models/gpt-4o-mini-tts/version/2025-03-20/registry/azure-openai) models.
>   - Introducing the new **Video playground** for Azure OpenAI Sora.

:::image type="content" source="../media/concept-playgrounds/playground-landing-page.png" alt-text="Azure AI Foundry playground landing page showcasing features for rapid prototyping and experimentation." lightbox="../media/concept-playgrounds/playground-landing-page.png":::

## The playground; the prelude to production

Modern development involves working across multiple systems—APIs, services, SDKs, and data models—often before you're ready to fully commit to a framework, write tests, or spin up infrastructure. As the complexity of software ecosystems increases, the need for safe, lightweight environments to validate ideas becomes critical. The playground was built to meet this need.

The playground provides a ready-to-use environment with all necessary tools and features pre-installed, eliminating the need to set up projects, manage dependencies, or solve compatibility issues.

#### Get clarity quicker

The playground is ideal for quickly answering questions like:

- How does this endpoint behave under edge conditions?
- What's the minimal prompt I need to get the output I want?
- Will this logic work before I write a full integration?
- How does latency or token usage change with different configurations?
- What model provides the best price-to-performance ratio before I evolve it into an agent?
- How do I evaluate performance and safety metrics for my agent?
  
You can get these answers in seconds, not hours. Think of the playground as the place where you test and validate ideas before you commit to building at scale. 

#### Accelerating developer velocity

- **Reduce cost of experimentation:** In traditional workflows, the cost of experimentation is high: setting up the project, writing scaffolding code, waiting on builds, and rolling back changes. As a result, many developers skip the experiment phase entirely, which leads to brittle assumptions, broken behavior, or inefficient code. The playground changes this dynamic by removing risk from experimentation. It compresses the distance between intention and insight, so you can validate before you invest. It also acts as a bridge between development and documentation. The examples you build in the Playground often become the reference points for future code, internal tooling, or user education.
- **Iterate faster:** Experiment with text prompts, adjust generation parameters, and explore editing variations — all in real time with model-specific native API support.
- **Accelerate integration:** Validate API behavior, test edge cases, and inspect responses directly in an interactive console.
- **Prompt optimization:** Debug and tune prompts, and build your own prompt variations available in the playground, grounded in model behavior.
- **Consistent model interface:** Common foundations established. No matter what model or agent, no matter the model provider.
- **Go to code quicker:** Using the "View Code" multi-lingual code samples for your output, prompts and generation controls within the API structure, what you create within Foundry playgrounds can be easily ported into VS Code - with predictability and repeatability.
- **Reduce time to ship:** No need to find, build, or configure a custom UI to localhost just for image generation, hope that it will automatically work for the next state-of-the-art model, or spend time resolving cascading build errors due to packages or code changes required for new models. The images playground in Azure AI Foundry gives you version-aware access. Build with the latest and most performant models with API updates surfaced in a consistent UI.
- **Collaboration & feedback:** Share your visual experiments directly with stakeholders, artists, or PMs without requiring them to install tools.
- **Human-in-the-loop refinement:** You can explore subtle tweaks with immediate visual feedback before hardcoding or automating anything.

Whether you're prototyping with the latest LLM from Foundry Models, validating prompts for edge cases, or optimizing output consistency, Foundry playgrounds removes friction from early experimentation. It's where ideas are pressure-tested before they're shipped into production. Optimize for prompt adherence, latency, and use cases through experimentation; accelerate your "Build-Measure-Learn" development loop; and ship faster with higher confidence.

Let's look through the various capabilities available.

## Open in VS Code

**For Chat and Agents playground**, we're introducing the **"Open in VS Code"** button through the Azure AI Foundry extension in VS Code. 

Available on the multi-lingual sample code samples, "Open in VS Code" enables the automatic import of your code sample, API endpoint and key to a VS Code workspace in /azure environment. Instead of going back and forth between Foundry and IDE, "Open in VS Code" reduces six clicks to one click:

1. Select  View Code in Chat playground and Agents playground to see the code sample.
1. Select  "Open in VS Code" button.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-foundry.png" alt-text="Open in VS Code button in Azure AI Foundry playground for seamless code integration." lightbox="../media/concept-playgrounds/open-in-vs-code-foundry.png":::

1. You're redirected to /azure environment of VS Code with importing of your code sample, API endpoint and key.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-vscode.png" alt-text="VS Code environment showing imported code sample, API endpoint, and key from Foundry playground." lightbox="../media/concept-playgrounds/open-in-vs-code-vscode.png":::

1. Browse through the `READ.ME` file for instructions to run your model.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-readme.png" alt-text="README file in VS Code with instructions for running the imported model." lightbox="../media/concept-playgrounds/open-in-vs-code-readme.png":::

1. Your code sample is automatically transferred to the `run_model.py`.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-run-model.png" alt-text="Code sample automatically transferred to run_model.py in VS Code." lightbox="../media/concept-playgrounds/open-in-vs-code-run-model.png":::
   
1. Relevant dependencies in the `requirements.txt` file.
    :::image type="content" source="../media/concept-playgrounds/open-in-vs-code-requirements.png" alt-text="Relevant dependencies listed in the requirements.txt file in VS Code." lightbox="../media/concept-playgrounds/open-in-vs-code-requirements.png":::


## Agents playground

The Agents playground allows you to explore, prototype, and test agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas. Get started with Agents playground with this [quickstart](../../ai-services/agents/quickstart.md).

:::image type="content" source="../media/concept-playgrounds/agents-playground.png" alt-text="Agents playground interface for exploring, prototyping, and testing agents without code." lightbox="../media/concept-playgrounds/agents-playground.png":::

## Chat playground

Test the latest reasoning models from Azure OpenAI, DeepSeek, and Meta with the chat playground experience through this [Quickstart: Use the chat playground in Azure AI Foundry portal](../quickstarts/get-started-playground.md).

For all reasoning models, we introduce a chain-of-thought summary drop-down to see how the model was thinking through its response ahead of sharing the output.

:::image type="content" source="../media/concept-playgrounds/chat-playground-cot-summary.png" alt-text="Chat Playground interface for exploring, prototyping, and testing chat models without code." lightbox="../media/concept-playgrounds/agents-playground.png":::

## Audio playground

With the audio playground, you can use text-to-speech and transcription capabilities with the latest audio models from Azure OpenAI.

1. Start with a text input prompt and rewrite the input with AI (coming soon).
1. Adjust model parameters like voice and language.
1. Receive a speech output with playback controls (play, rewind, forward, adjust speed and volume).
1. Download to local as a .wav file.
    :::image type="content" source="../media/concept-playgrounds/audio-playground-text-to-speech.png" alt-text="Audio playground interface showcasing text-to-speech capabilities with playback controls." lightbox="../media/concept-playgrounds/audio-playground-text-to-speech.png":::

1. Start with an audio file by either upload audio file, recording the audio from the prompt bar or speaking directly to the model.
1. Include a phrase list as a text mechanism to guide the audio input.
1. Once the audio input has been sent to the model, receive a transcribed output as text and JSON.
    :::image type="content" source="../media/concept-playgrounds/audio-playground-transcribe.png" alt-text="Audio playground interface demonstrating transcription output from audio input." lightbox="../media/concept-playgrounds/audio-playground-transcribe.png":::

## Images playground

> [!NOTE]  
> See the [60-second reel of Images playground for gpt-image-1](https://youtu.be/btA8njJjLXY) and our DevBlog for how to transform your [enterprise-ready use case by industry.](https://devblogs.microsoft.com/foundry/images-playground-may-2025/)

We built the images playground for developers who build image generation flows. The Images playground is a full-featured, controlled environment for high-fidelity experiments designed for model-specific APIs for generation and editing.

### How to use images playground

1. **Start with a pre-built text prompt**: Select an option to get started with a prebuilt text prompt that automatically fills the prompt bar.
1. **Explore the model API-specific generation controls after model deployment:** Adjust key controls (e.g. number of variants, quality, strength) to deeply understand specific model responsiveness and constraints.
1. **Side-by-side observations in grid view:** Visually observe outputs across prompt tweaks or parameter changes.
1. **Transform with API tooling:** Inpainting with text transformation is available for gpt-image-1. Alter parts of your original image with inpainting selection. Use text prompts to specify the change.
1. **Port to production with multi-lingual code samples:** Use Python, Java, JavaScript, C# code samples with "View Code". Images playground is your launchpad to development work in VS Code.


### Applicable models

- [gpt-image-1](https://ai.azure.com/explore/models/gpt-image-1/version/2025-04-15/registry/azure-openai) from Azure OpenAI.
- [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai), [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai), [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai) from Stability AI.
- [Bria 2.3 Fast](https://ai.azure.com/explore/models/Bria-2.3-Fast/version/1/registry/azureml-bria) from Bria AI.

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

> [!NOTE]  
> See the [60-second reel of Video playground for Azure OpenAI Sora](https://aka.ms/VideoPlaygroundReel) and our DevBlog for how to transform your [enterprise-ready use case by industry.](https://aka.ms/VideoPlaygroundDevBlog). 

The Video playground is your rapid iteration environment for exploring, refining, and validating generative video workflows—designed for developers who need to go from idea to prototype with precision, control, and speed. The playground gives you a low-friction interface to test prompt structures, assess motion fidelity, evaluate model consistency across frames, and compare outputs across models—without writing boilerplate or wasting compute cycles – and a great demo interface for your Chief Product Officer and Engineering VP.


### Applicable models

- Azure OpenAI Sora.

### How to use the Video playground:

> [!CAUTION]
> Videos generated are retained for 24 hours due to data privacy. Download videos to local for longer retention.

1. Once your model is deployed, navigate to the Video playground and get inspired by **pre-built prompts sorted by industry filter**. From here, you can view the videos in full display and copy the prompt to build from it.

1.  **Understand the model API specific generation controls in your prompt bar:** Enter your text prompt and adjust key controls (e.g. aspect ratio, resolution) to deeply understand specific model responsiveness and constraints.

1. **Rewrite your text prompt** syntax with gpt-4o using "Rewrite with AI" with industry based system prompts. Switch on the capability, select the industry and specify the change required for your original prompt.

1. From the Generation history tab, review your generations as a Grid or List view. When you select  the videos, open them in full screen mode for full immersion. Visually observe outputs across prompt tweaks or parameter changes.
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