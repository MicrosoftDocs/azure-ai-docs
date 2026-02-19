---
title: Sora video generation overview (preview)
description: Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
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
| **Size (Output resolution in width × height)** | String (optional) | Portrait: `720×1280`  <br> Landscape: `1280×720`  <br> **Default:** 720×1280 |
| **Seconds** | String (optional) | `4 / 8 / 12`  <br> **Default:** 4 | 
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

**Synchronous:**

Use this version if testing in Jupyter Notebooks to avoid `RuntimeError: asyncio.run() cannot be called from a running event loop`

```python
import time
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
    base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
    api_key=token_provider,
)

# Create the video (don't use create_and_poll)
video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cat on a motorcycle",
)

print(f"Video creation started. ID: {video.id}")
print(f"Initial status: {video.status}")

# Poll every 20 seconds
while video.status not in ["completed", "failed", "cancelled"]:
    print(f"Status: {video.status}. Waiting 20 seconds...")
    time.sleep(20)
    
    # Retrieve the latest status
    video = client.videos.retrieve(video.id)

# Final status
if video.status == "completed":
    print("Video successfully completed!")
    print(video)
else:
    print(f"Video creation ended with status: {video.status}")
    print(video)
```

**Async:**

```python
import asyncio
from openai import AsyncOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AsyncOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

async def main() -> None:
    video = await client.videos.create_and_poll(
        model="sora-2", # Replace with Sora 2 model deployment name
        prompt="A video of a cat on a motorcycle",
    )

    if video.status == "completed":
        print("Video successfully completed: ", video)
    else:
        print("Video creation failed. Status: ", video.status)


asyncio.run(main())
```

# [API Key](#tab/python-key)

**Synchronous:**

Use this version if testing in Jupyter Notebooks to avoid `RuntimeError: asyncio.run() cannot be called from a running event loop`


```python
import asyncio
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

# Create the video (don't use create_and_poll)
video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cat on a motorcycle",
)

print(f"Video creation started. ID: {video.id}")
print(f"Initial status: {video.status}")

# Poll every 20 seconds
while video.status not in ["completed", "failed", "cancelled"]:
    print(f"Status: {video.status}. Waiting 20 seconds...")
    time.sleep(20)
    
    # Retrieve the latest status
    video = client.videos.retrieve(video.id)

# Final status
if video.status == "completed":
    print("Video successfully completed!")
    print(video)
else:
    print(f"Video creation ended with status: {video.status}")
    print(video)
```

**Async:**

```python
import asyncio
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

async def main() -> None:
    video = await client.videos.create_and_poll(
        model="sora-2", # Replace with Sora 2 model deployment name 
        prompt="A video of a cat on a motorcycle",
    )

    if video.status == "completed":
        print("Video successfully completed: ", video)
    else:
        print("Video creation failed. Status: ", video.status)


asyncio.run(main())
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

**Synchronous:**

Use this version if testing in Jupyter Notebooks to avoid `RuntimeError: asyncio.run() cannot be called from a running event loop`

```python
from openai import OpenAI

client = OpenAI()

# Create the video (don't use create_and_poll)
video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cat on a motorcycle",
)

print(f"Video creation started. ID: {video.id}")
print(f"Initial status: {video.status}")

# Poll every 20 seconds
while video.status not in ["completed", "failed", "cancelled"]:
    print(f"Status: {video.status}. Waiting 20 seconds...")
    time.sleep(20)
    
    # Retrieve the latest status
    video = client.videos.retrieve(video.id)

# Final status
if video.status == "completed":
    print("Video successfully completed!")
    print(video)
else:
    print(f"Video creation ended with status: {video.status}")
    print(video)
```

**Async:**

```python
from openai import OpenAI

client = OpenAI()

async def main() -> None:
    video = await client.videos.create_and_poll(
        model="sora-2", # Replace with Sora 2 model deployment name
        prompt="A video of a cat on a motorcycle",
    )

    if video.status == "completed":
        print("Video successfully completed: ", video)
    else:
        print("Video creation failed. Status: ", video.status)


asyncio.run(main())
```

# [Response](#tab/python-output)

Response will vary based on if the synchronous or asynchronous version of the code is used. 

```json
Video creation started. ID: video_68f10c5428708190a98980c2d2b21a78
Initial status: queued
Status: queued. Waiting 20 seconds...
Status: in_progress. Waiting 20 seconds...
Status: in_progress. Waiting 20 seconds...
Status: in_progress. Waiting 20 seconds...
Video successfully completed!
Video(id='video_68f10c5428708190a98980c2d2b21a78', completed_at=1760627863, created_at=1760627796, error=None, expires_at=1760714196, model='sora-2', object='video', progress=100, remixed_from_video_id=None, seconds='4', size='720x1280', status='completed')
```

---

### Download video

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

video_id = "your_video_id_here"

content = client.videos.download_content(video_id, variant="video")
content.write_to_file("video.mp4")

print("Saved video.mp4")
```


# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

video_id = "your_video_id_here"

content = client.videos.download_content(video_id, variant="video")
content.write_to_file("video.mp4")

print("Saved video.mp4")


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

video_id = "your_video_id_here"

content = client.videos.download_content(video_id, variant="video")
content.write_to_file("video.mp4")

print("Saved video.mp4")

```

# [Response](#tab/python-output)

```json
Saved video.mp4
```

---

### Video generation from reference source

The `input_reference` parameter allows you to transform existing images using Sora 2. The resolution of the source image and final video must match. Supported values are `720x1280`, and `1280x720`.

# [Microsoft Entra ID](#tab/python-entra)

**Local reference file:**

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

# With local file
video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=open("test.png", "rb"), # This assumes the image test.png is in the same directory as the executing code
)

print("Video generation started:", video)

```

**URL based reference file:**

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import requests
from io import BytesIO

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# With image URL
image_url = "https://path-to-your-file/image_file_name.jpg"
response = requests.get(image_url)
image_data = BytesIO(response.content)
image_data.name = "image_file_name.jpg"

video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=image_data,
)

print("Video generation started:", video)
```

# [API Key](#tab/python-key)

**Local reference file:**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

# With local file
video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=open("test.png", "rb"), # This assumes the image test.png is in the same directory as the executing code
)

print("Video generation started:", video)

```

**URL based reference file:**

```python
import os
from openai import OpenAI
import requests
from io import BytesIO

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

# With image URL
image_url = "https://path-to-your-file/image_file_name.jpg"
response = requests.get(image_url)
image_data = BytesIO(response.content)
image_data.name = "image_file_name.jpg"

video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=image_data,
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

**Local reference file:**

```python
from openai import OpenAI

client = OpenAI()

# With local file
video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=open("test.png", "rb"), # This assumes the image test.png is in the same directory as the executing code
)

print("Video generation started:", video)

```

**URL based reference file:**

```python
from openai import OpenAI
import requests
from io import BytesIO

client = OpenAI()

# With image URL
image_url = "https://path-to-your-file/image_file_name.jpg"
response = requests.get(image_url)
image_data = BytesIO(response.content)
image_data.name = "image_file_name.jpg"

video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=image_data,
)

print("Video generation started:", video)
```

# [Response](#tab/python-output)

```json
Video generation started: Video(id='video_68ff672709d481908f1fa7c53265d835', completed_at=None, created_at=1761568551, error=None, expires_at=None, model='sora-2', object='video', progress=0, remixed_from_video_id=None, seconds='8', size='1280x720', status='queued')
```

---

### Remix video

The remix feature allows you to modify specific aspects of an existing video while preserving its core elements. By referencing the previous video `id` from a successfully completed generation, and supplying an updated prompt the system maintains the original video's framework, scene transitions, and visual layout while implementing your requested changes. For optimal results, limit your modifications to one clearly articulated adjustment—narrow, precise edits retain greater fidelity to the source material and minimize the likelihood of generating visual defects.


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

video = client.videos.remix(
    video_id="<previous_video_id>",
    prompt="Shift the color palette to teal, sand, and rust, with a warm backlight."
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

video = client.videos.remix(
    video_id="<previous_video_id>",
    prompt="Shift the color palette to teal, sand, and rust, with a warm backlight."
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

video = client.videos.remix(
    video_id="<previous_video_id>",
    prompt="Shift the color palette to teal, sand, and rust, with a warm backlight."
)

print("Video generation started:", video)
```

# [Response](#tab/python-output)

```json
Video generation started: Video(id='video_68ff7cef76cc8190b7eab9395e936d9e', completed_at=None, created_at=1761574127, error=None, expires_at=None, model='sora-2', object='video', progress=0, remixed_from_video_id='video_68ff61490a908190a6808139c0c753d0', seconds='8', size='1280x720', status='queued')
```

---

## How it works

Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You can check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL.

## Best practices for prompts

Write text prompts in English or other Latin script languages for the best video generation performance.  


## Limitations

### Content quality limitations

Sora might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Sora 2 Technical Limitations 

- Please see Sora 2 API details above 
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can create two video job requests per minute. The Sora 2 quota only counts video job requests: other types of requests are not rate-limited.

### Sora 1 Technical limitations

- Sora supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.
- Sora can produce videos between 1 and 20 seconds long.
- You can request multiple video variants in a single job: for 1080p resolutions, this feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can use up to two images as input (the generated video interpolates content between them).
- You can use one video up to five seconds as input.


## Related content
- [Video generation quickstart](../video-generation-quickstart.md)
- [Image generation quickstart](../dall-e-quickstart.md)
