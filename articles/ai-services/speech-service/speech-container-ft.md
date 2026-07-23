---
title: Fast transcription containers - Speech service
titleSuffix: Foundry Tools
description: Install and run fast transcription containers with Docker to perform synchronous audio transcription, speaker diarization, and multi-channel processing on-premises.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.custom: devx-track-extended-java, devx-track-go, devx-track-js, devx-track-python
ms.topic: how-to
ms.date: 07/09/2026
ms.author: pafarley
keywords: on-premises, Docker, container, transcription
ai-usage: ai-assisted
---

# Fast transcription containers with Docker

The fast transcription container transcribes audio files synchronously, returning results faster than real-time. It's suitable for scenarios where you need transcription results as quickly as possible, such as audio and video subtitles, meeting transcripts, and voicemail. It supports speaker diarization, multichannel processing, and word-level timestamps. This article describes how to download, install, and run a fast transcription container.

For more information about prerequisites, validating that a container is running, running multiple containers on the same host, and running disconnected containers, see [Install and run Speech containers with Docker](speech-container-howto.md).

## Container images

You can find the fast transcription container image for all supported versions and locales on the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/fast-transcription/tags). It resides within the `azure-cognitive-services/speechservices/` repository and is named `fast-transcription`.

The fully qualified container image name is `mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription`. Either append a specific version or append `:latest` to get the most recent version.

| Version | Path |
|-----------|------------|
| Latest | `mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription:latest`<br/><br/>The `latest` tag pulls the latest image for the `en-US` locale. |
| 1.0.0 | `mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription:en-gpu-1.0.0-preview` |

All tags, except for `latest`, follow this format and are case sensitive:

```
<language>-gpu-<major>.<minor>.<patch>-preview
```


For your convenience, the tags are also available [in JSON format](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/fast-transcription/tags/list). The body includes the container path and list of tags. The tags aren't sorted by version, but `"latest"` is always included at the end of the list as shown in this snippet:

```json
{
  "name": "azure-cognitive-services/speechservices/fast-transcription",
  "tags": [
    <--redacted for brevity-->    
    "gpu-1.0.0-en-us",
    "gpu-1.0.0-en-gb",
    "gpu-1.0.0-en-au",
    "gpu-1.0.0-en-in",
    "gpu-1.0.0-de-de"
  ]
}
```

### Locale support 

The following model and locale groups map to supported transcription locales:

| Model or locale group | Supported transcription locales |
| --- | --- |
| `en` | `en-AU`, `en-CA`, `en-GB`, `en-GH`, `en-HK`, `en-IE`, `en-KE`, `en-NG`, `en-NZ`, `en-PH`, `en-SG`, `en-TZ`, `en-US`, `en-ZA` |
| `multilingual-15-locales` | `de-DE`, `en-AU`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `es-ES`, `es-MX`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `zh-CN` |
| `t4-35-locales` | `af-ZA`, `am-ET`, `az-AZ`, `bn-IN`, `bs-BA`, `et-EE`, `eu-ES`, `fil-PH`, `ga-IE`, `gl-ES`, `hy-AM`, `is-IS`, `jv-ID`, `ka-GE`, `kk-KZ`, `km-KH`, `lo-LA`, `lt-LT`, `mk-MK`, `ml-IN`, `mn-MN`, `mt-MT`, `my-MM`, `ne-NP`, `ps-AF`, `si-LK`, `so-SO`, `sq-AL`, `sr-RS`, `sw-KE`, `ur-IN`, `uz-UZ`, `wuu-CN`, `zh-CN-SICHUAN`, `zu-ZA` |
| `ar` | `ar-AE`, `ar-BH`, `ar-EG`, `ar-IL`, `ar-IQ`, `ar-JO`, `ar-KW`, `ar-LB`, `ar-LY`, `ar-OM`, `ar-PS`, `ar-QA`, `ar-SA`, `ar-SY`, `ar-YE` |
| `t3-16-locales` | `bg-BG`, `ca-ES`, `cy-GB`, `fa-IR`, `hr-HR`, `hu-HU`, `lv-LV`, `mr-IN`, `ms-MY`, `nb-NO`, `ro-RO`, `sk-SK`, `sl-SI`, `uk-UA`, `vi-VN`, `zh-HK` |
| `es` | `es-AR`, `es-BO`, `es-CL`, `es-CR`, `es-CU`, `es-DO`, `es-EC`, `es-GQ`, `es-GT`, `es-HN`, `es-MX`, `es-NI`, `es-PA`, `es-PE`, `es-PR`, `es-PY`, `es-SV`, `es-US`, `es-UY`, `es-VE` |
| `fr` | `fr-BE`, `fr-CH`, `fr-FR` |
| `it` | `it-CH`, `it-IT` |
| `india-13-locales` | `ta-IN`, `hi-IN`, `te-IN`, `gu-IN`, `mr-IN`, `kn-IN`, `bn-IN`, `ml-IN`, `pa-IN`, `ur-IN`, `or-IN`, `as-IN`, `bho-IN` |
| Single-locale entries | `de-DE`, `en-IN`, `en-Latn-IN`, `es-CO`, `es-ES`, `fr-CA`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN` |


## Get the container image with `docker pull`

You need the [prerequisites](speech-container-howto.md#prerequisites) including required hardware. Also see the [recommended allocation of resources](speech-container-howto.md#container-requirements-and-recommendations) for each Speech container.

Use the [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to download a container image from Microsoft Container Registry:

```bash
docker pull mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription:latest
```

> [!IMPORTANT]
> The `latest` tag pulls the latest image for the `en-US` locale. For additional versions and locales, see [fast transcription container images](#container-images).

## Hardware requirements

The fast transcription container requires a GPU to run.

| Configuration | GPU | vCPU | Memory |
|------|-----|------|------|
| Minimum | NVIDIA T4 or higher | 8 cores | 16 GB |
| Recommended | NVIDIA T4 | 16 cores | 110 GB |

> [!IMPORTANT]
> GPU required. The fast transcription container doesn't support CPU.

## Run the container with `docker run`

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container.

# [Fast transcription](#tab/container)

The following table lists the `docker run` parameters and their descriptions:

| Parameter | Description |
|---------|---------|
| `{ENDPOINT_URI}` | The endpoint is required for metering and billing. For more information, see [billing arguments](speech-container-howto.md#billing-arguments). |
| `{API_KEY}` | The API key is required. For more information, see [billing arguments](speech-container-howto.md#billing-arguments). |

When you run the fast transcription container, configure the port, memory, and GPU according to the fast transcription container [requirements and recommendations](speech-container-howto.md#container-requirements-and-recommendations).

Here's an example `docker run` command with placeholder values. You must specify the `ENDPOINT_URI` and `API_KEY` values:

```bash
docker run --gpus all -p 5000:5000 \
-e ASPNETCORE_URLS=http://+:5000 \
mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

This command:
- Runs a `fast-transcription` container from the container image.
- Exposes all available GPUs to the container.
- Exposes TCP port 5000.
- Sets ASP.NET Core to listen on port 5000.

# [Disconnected fast transcription](#tab/disconnected)

To run disconnected containers (not connected to the internet), you must submit [this request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../containers/disconnected-containers.md) in the Foundry Tools documentation.

If you're approved to run the container disconnected from the internet, the following example shows the formatting of the `docker run` command to use, with placeholder values. Replace these placeholder values with your own values.

The `DownloadLicense=True` parameter in your `docker run` command downloads a license file to enable your Docker container to run when it isn't connected to the internet. It also contains an expiration date, after which the license file is invalid to run the container. You can only use a license file with the appropriate container that you're approved for. For example, you can't use a license file for a `fast-transcription` container with a `speech-to-text` container.

| Placeholder | Description | 
|-------------|-------|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription:latest` |
| `{LICENSE_MOUNT}` | The path where the license is downloaded and mounted.<br/><br/>For example: `/host/license:/path/to/license/directory` |
| `{ENDPOINT_URI}` | The endpoint for authenticating your service request. You can find it on your resource's **Key and endpoint** page, on the Azure portal.<br/><br/>For example: `https://<your-resource-name>.cognitiveservices.azure.com` |
| `{API_KEY}` | The key for your Speech resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal. |
| `{CONTAINER_LICENSE_DIRECTORY}` | Location of the license folder on the container's local filesystem.<br/><br/>For example: `/path/to/license/directory` |

```bash
docker run --gpus all -p 5000:5000 \
-e ASPNETCORE_URLS=http://+:5000 \
-v {LICENSE_MOUNT} \
{IMAGE} \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY} \
DownloadLicense=True \
Mounts:License={CONTAINER_LICENSE_DIRECTORY} 
```

Once the license file is downloaded, you can run the container in a disconnected environment. The following example shows the formatting of the `docker run` command you use, with placeholder values. Replace these placeholder values with your own values.

Wherever you run the container, you must mount the license file to the container and specify the location of the license folder on the container's local filesystem with `Mounts:License=`. You must also specify an output mount so that billing usage records can be written.

| Placeholder | Value | Format or example |
|-------------|-------|---|
| `{IMAGE}` | The container image you want to use | `mcr.microsoft.com/azure-cognitive-services/speechservices/fast-transcription:latest` |
| `{LICENSE_MOUNT}` | The path where the license is located and mounted | `/host/license:/path/to/license/directory` |
| `{OUTPUT_PATH}` | The output path for logging. For more information, see [usage records](../containers/disconnected-containers.md#usage-records) in the Foundry Tools documentation. | `/host/output:/path/to/output/directory` |
| `{CONTAINER_LICENSE_DIRECTORY}` | Location of the license folder on the container's local filesystem | `/path/to/license/directory` |
| `{CONTAINER_OUTPUT_DIRECTORY}` | Location of the output folder on the container's local filesystem | `/path/to/output/directory` |

```bash
docker run --gpus all -p 5000:5000 \
-e ASPNETCORE_URLS=http://+:5000 \
-v {LICENSE_MOUNT} \
-v {OUTPUT_PATH} \
{IMAGE} \
Eula=accept \
Mounts:License={CONTAINER_LICENSE_DIRECTORY} \
Mounts:Output={CONTAINER_OUTPUT_DIRECTORY}
```

Speech containers provide a default directory for writing the license file and billing log at runtime. The default directories are `/license` and `/output` respectively.

When you mount these directories to the container by using the `docker run -v` command, make sure the local machine directory ownership is set to `user:group nonroot:nonroot` before running the container.

Here's a sample command to set file and directory ownership.

```bash
sudo chown -R nonroot:nonroot <YOUR_LOCAL_MACHINE_PATH_1> <YOUR_LOCAL_MACHINE_PATH_2> ...
```

---

For more information about `docker run` with Speech containers, see [Install and run Speech containers with Docker](speech-container-howto.md#run-the-container).

## Use the container

The fast transcription container exposes an HTTP REST API for transcription requests. Unlike the speech-to-text container which supports WebSocket streaming, fast transcription processes complete audio files synchronously.

### API endpoints

Send transcription requests to:

```
POST http://localhost:5000/stt/transcriptions:transcribe
```

Health check endpoint:

```
GET http://localhost:5000/stt/health
```

### Audio input limits

| Limit | Value |
|--------|------|
| Maximum file size | 300 MB |
| Supported formats | WAV, MP3, OPUS/OGG, FLAC, WMA, AAC, ALAW (in WAV container), MULAW (in WAV container), AMR, WebM, SPEEX |

### Request format

The API accepts `multipart/form-data` requests with the following structure:

| Part | Content-Type | Description |
|------|--------------|-------------|
| `definition` | `application/json` | JSON object containing transcription options |
| `audio` | `audio/*` | The audio file to transcribe (mutually exclusive with `audioUrl`) |

### Request examples

Basic transcription:

```bash
curl -X POST "http://localhost:5000/stt/transcriptions:transcribe?api-version=2024-11-15" \
  -F "audio=@audio.wav" \
  -F 'definition={"locales":["en-US"]}'
```

Dual-channel separation:

```bash
curl -X POST "http://localhost:5000/stt/transcriptions:transcribe?api-version=2024-11-15" \
  -F "audio=@stereo.wav" \
  -F 'definition={"locales":["en-US"],"channels":[0,1]}'
```

Speaker diarization:

```bash
curl -X POST "http://localhost:5000/stt/transcriptions:transcribe?api-version=2024-11-15" \
  -F "audio=@meeting.wav" \
  -F 'definition={"locales":["en-US"],"diarization":{"enabled":true}}'
```

Profanity filter (masked):

```bash
curl -X POST "http://localhost:5000/stt/transcriptions:transcribe?api-version=2024-11-15" \
  -F "audio=@audio.wav" \
  -F 'definition={"locales":["en-US"],"profanityFilterMode":"Masked"}'
```

Health check:

```bash
curl http://localhost:5000/stt/health
```

### Transcription options

| Option | Type | Description |
|--------|------|-------------|
| `locales` | string[] | Locales for transcription, such as `["en-US"]`. |
| `audioUrl` | string | HTTP or HTTPS URL of the audio file. This option is mutually exclusive with file upload. |
| `profanityFilterMode` | string | How to handle profanity: `None`, `Masked`, `Removed`, `Tags`. |
| `punctuationMode` | string | Punctuation handling: `None`, `Dictated`, `Automatic`, `DictatedAndAutomatic`. |
| `channels` | int[] | Audio channels to process, such as `[0, 1]` for stereo. |
| `diarization` | object | Speaker diarization settings. |
| `diarization.enabled` | boolean | Enable speaker diarization. |
| `diarization.maxSpeakers` | int | Maximum number of speakers to identify (2-35). |
| `wordLevelTimestampsEnabled` | boolean | Include word-level timing information. |
| `disfluencyTaggingEnabled` | boolean | Enable disfluency tagging. |
| `prompt` | string | Prompt text to improve recognition accuracy. |
| `phraseList` | string | Phrase list (semicolon-separated) to improve recognition accuracy. |
| `localeHint` | string | Language hint. |

### Response example

```json
{
  "durationMilliseconds": 2029,
  "combinedPhrases": [
    {
      "text": "What's the weather like?"
    }
  ],
  "phrases": [
    {
      "offsetMilliseconds": 40,
      "durationMilliseconds": 1240,
      "text": "What's the weather like?",
      "words": [
        { "text": "What's", "offsetMilliseconds": 40, "durationMilliseconds": 360 },
        { "text": "the", "offsetMilliseconds": 400, "durationMilliseconds": 160 },
        { "text": "weather", "offsetMilliseconds": 560, "durationMilliseconds": 320 },
        { "text": "like?", "offsetMilliseconds": 880, "durationMilliseconds": 400 }
      ],
      "locale": "en-US",
      "confidence": 0.9874588
    }
  ]
}
```

### Response fields

| Field | Type | Description |
|------|------|-------------|
| `durationMilliseconds` | int | Total audio duration in milliseconds |
| `combinedPhrases` | array | Complete transcription text |
| `combinedPhrases[].text` | string | Complete transcription text |
| `combinedPhrases[].channel` | int | Channel index (shown for multichannel audio) |
| `phrases` | array | List of segmented phrases |
| `phrases[].offsetMilliseconds` | int | Phrase start time in milliseconds |
| `phrases[].durationMilliseconds` | int | Phrase duration in milliseconds |
| `phrases[].text` | string | Phrase text |
| `phrases[].words` | array | Word-level information (returned by default) |
| `phrases[].locale` | string | Recognized locale |
| `phrases[].confidence` | float | Confidence score (0-1) |
| `phrases[].channel` | int | Channel index (shown for multichannel audio) |
| `phrases[].speaker` | int | Speaker ID (shown when diarization is enabled) |

## Configuration options

Use the following environment variables to configure the fast transcription container:

| Variable | Default | Description |
|----------|---------|-------------|
| `EULA` | (required) | Set to `accept` |
| `BILLING` | (required) | Azure endpoint URL for billing |
| `APIKEY` | (required) | API key for authentication |
| `DECODER_COUNT` | `2` | Number of parallel decoder instances; at least 2 required for dual-channel audio |

## Related content

* See the [Speech containers overview](speech-container-overview.md).
* Review [configure containers](speech-container-configuration.md) for configuration settings.
* Use more [Azure AI containers](../cognitive-services-container-support.md).
