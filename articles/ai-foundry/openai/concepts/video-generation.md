---
title: Sora video generation overview (preview)
description: Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: article
monikerRange: 'foundry-classic || foundry'
ms.date: 12/1/2025
---

# Video generation with Sora (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Sora is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions and/or input images or video. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations.

Azure OpenAI supports two versions of Sora:
- Sora (or Sora 1): Azure OpenAI–specific implementation released as an API in early preview.
- Sora 2: The latest OpenAI-based API, now available with the Azure OpenAI [v1 API](../api-version-lifecycle.md).

## Capabilities

- Modalities: text → video, image → video, video (generated) → video
- Audio: Sora 2 supports audio generation in output videos (similar to the Sora app).
- Remix: Sora 2 introduces the ability to remix existing videos by making targeted adjustments instead of regenerating from scratch.
- Responsible AI and video generation: Azure OpenAI's video generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use. Sora 2 blocks all IP and photorealistic content.
    In addition, Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

    Customers can learn more about these safeguards and how to customize them on the [Content filtering](/azure/ai-foundry/openai/concepts/content-filter) page.

## Responsible AI and video generation

Azure OpenAI's image generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use.

In addition, Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

Currently the Sora 2 API enforces several content restrictions:
- Only content suitable for audiences under 18 (a setting to bypass this restriction will be available in the future).
- Copyrighted characters and copyrighted music will be rejected.
- Real people—including public figures—cannot be generated.
- Input images with faces of humans are currently rejected.

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

> [!NOTE] 
> We are allowing face uploads on a case-by-case basis for managed customers. 

## Sora 1 vs. Sora 2

| Aspect | **Sora 1 (Azure OpenAI)** | **Sora 2 (OpenAI-based API)** |
|--------|-----------------------------|-------------------------------|
| **Model type** | Azure-specific API implementation | Adapts OpenAI’s latest Sora API using [v1 API](../api-version-lifecycle.md)|
| **Availability** | Available exclusively on Azure OpenAI (Preview) | Rolling out on Azure; **Sora 2 Pro** coming later |
| **Modalities supported** | text → video, image → video, video → video | text → video, image → video, **video (generated) → video** |
| **Audio generation** | ❌ Not supported | ✅ Supported in outputs |
| **Remix capability** | ❌ Not supported | ✅ Supported — make targeted edits to existing videos |
| **API behavior** | Uses Azure-specific API schema | Aligns with OpenAI’s native Sora 2 schema |
| **Performance & fidelity** | Early preview; limited realism and motion range | Enhanced realism, physics, and temporal consistency |
| **Intended use** | Enterprise preview deployments | Broader developer availability with improved API parity |
| **Billing** | Billed differently across duration and resolutions | [Per second billing information](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) 

## Sora 2 API 
Provides 5 endpoints, each with distinct capabilities. 
- Create Video: Start a new render job from a prompt, with optional reference inputs or a remix ID.
- Get Video Status: Retrieve the current state of a render job and monitor its progress
- Download Video: Fetch the finished MP4 once the job is completed.
- List Videos: Enumerate your videos with pagination for history, dashboards, or housekeeping. 
- Delete Videos: Delete an individual video ID from Azure OpenAI’s storage

### API parameters

| Parameter | Type | **Sora 2** | 
|------------|------|------------|
| **Prompt** | String (required) | Natural-language description of the shot. Include shot type, subject, action, setting, lighting, and any desired camera motion to reduce ambiguity. Keep it *single-purpose* for best adherence. | 
| **Model** | String (optional) | `Sora-2` (default) |
| **Size (Output resolution, width × height)** | String (optional, response-visible) | Output frame size. Allowed values: `720×1280` (portrait), `1280×720` (landscape). **Units:** pixels. **Default:** `720×1280`. |
<!-- Changed to clarify units, allowed values, default, and response visibility per agent feedback -->
| **Seconds** | String (optional, response-visible) | Duration of the output video in seconds. Allowed values: `4`, `8`, `12`. **Units:** seconds. **Default:** `4`. | 
<!-- Changed to clarify meaning, units, allowed values, default, and response visibility per agent feedback -->
| **Input reference** | File (optional) | Single reference image used as a visual anchor for the first frame. <br> Accepted MIME types: `image/jpeg`, `image/png`, `image/webp`. Must match size exactly. | 
| **Remix_video_id** | String (optional) | ID of a previously completed video (e.g., `video_...`) to reuse structure, motion, and framing. Same as Sora 2 |

Sora 2 API uses the [v1 API](../api-version-lifecycle.md) and has the same structure as the [OpenAI API](https://platform.openai.com/docs/guides/video-generation).

### videos.create()

You'll need to update to the latest version of the OpenAI client with `pip install openai --upgrade` to prevent `AttributeError: 'OpenAI' object has no attribute 'videos'`.

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

# [Environment Variables](#tab/python-env)

If you use the default environment variables of:

- `OPENAI_BASE_URL`
- `OPENAI_API_KEY` 

These environment variables are automatically used by the client with no further configuration required.

| Environment Variable | Value |
|----------------|-------------|
| `OPENAI_BASE_URL`    | `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`|
| `OPENAI_API_KEY`     | Azure OpenAI or Foundry API key. |

```python
from openai import OpenAI

client = OpenAI()

video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

# [Response](#tab/python-output)

```json
Video generation started: Video(id='video_68f10985d6c4819097007665bdcfba5f', completed_at=None, created_at=1760627077, error=None, expires_at=None, model='sora-2', object='video', progress=0, remixed_from_video_id=None, seconds='4', size='720x1280', status='queued')
```

---

### Create a video and poll job status

Call `GET /videos/{video_id}` with the ID returned from the create call. The response shows the job’s current status, progress percentage, and any errors.

Expected states are `queued`, `in_progress`, `completed`, and `failed`. 


# [Microsoft Entra ID](#tab/python-entra)

Authentication and environment variable configuration are the same as described in the earlier Environment Variables section.
<!-- Deduplicated authentication and environment variable boilerplate per agent feedback -->

**Synchronous:**

Use this version if testing in Jupyter Notebooks to avoid `RuntimeError: asyncio.run() cannot be called from a running event loop`

```python
import time
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
...
```

*(rest of section content unchanged)*