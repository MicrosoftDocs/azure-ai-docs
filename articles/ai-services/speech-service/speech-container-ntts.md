---
title: Neural text to speech containers - Speech service
titleSuffix: Azure AI services
description: Install and run neural text to speech containers with Docker to perform speech synthesis and more on-premises.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.custom: devx-track-extended-java, devx-track-go, devx-track-js, devx-track-python
ms.topic: how-to
ms.date: 9/17/2024
ms.author: eur
zone_pivot_groups: programming-languages-speech-sdk-cli
keywords: on-premises, Docker, container
#Customer intent: As a developer, I want to learn how to install and run neural text to speech containers with Docker.
---

# Text to speech containers with Docker

The neural text to speech container converts text to natural-sounding speech by using deep neural network technology, which allows for more natural synthesized speech. In this article, you learn how to download, install, and run a Text to speech container.

For more information about prerequisites, validating that a container is running, running multiple containers on the same host, and running disconnected containers, see [Install and run Speech containers with Docker](speech-container-howto.md).

## Container images

The neural text to speech container image for all supported versions and locales can be found on the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/neural-text-to-speech/tags) syndicate. It resides within the `azure-cognitive-services/speechservices/` repository and is named `neural-text-to-speech`. 

:::image type="content" source="./media/containers/mcr-tags-neural-text-to-speech.png" alt-text="A screenshot of the search connectors and triggers dialog." lightbox="./media/containers/mcr-tags-neural-text-to-speech.png":::

The fully qualified container image name is, `mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech`. Either append a specific version or append `:latest` to get the most recent version.

| Version | Path |
|-----------|------------|
| Latest | `mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech:latest`<br/><br/>The `latest` tag pulls the `en-US` locale and `en-us-arianeural` voice. |
| 3.5.0 | `mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech:3.5.0-amd64-en-us-arianeural` |

All tags, except for `latest`, are in the following format and are case sensitive:

```
<major>.<minor>.<patch>-<platform>-<voice>-<preview>
```

The tags are also available [in JSON format](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/neural-text-to-speech/tags/list) for your convenience. The body includes the container path and list of tags. The tags aren't sorted by version, but `"latest"` is always included at the end of the list as shown in this snippet:

```json
{
  "name": "azure-cognitive-services/speechservices/neural-text-to-speech",
  "tags": [
    <--redacted for brevity-->
    "3.5.0-amd64-uk-ua-ostapneural",
    "3.5.0-amd64-zh-cn-xiaochenneural-preview",
    "3.5.0-amd64-zh-cn-xiaohanneural",
    "3.5.0-amd64-zh-cn-xiaomoneural",
    "3.5.0-amd64-zh-cn-xiaoqiuneural-preview",
    "3.5.0-amd64-zh-cn-xiaoruineural",
    "3.5.0-amd64-zh-cn-xiaoshuangneural-preview",
    "3.5.0-amd64-zh-cn-xiaoxiaoneural",
    "3.5.0-amd64-zh-cn-xiaoyanneural-preview",
    "3.5.0-amd64-zh-cn-xiaoyouneural",
    "3.5.0-amd64-zh-cn-yunxineural",
    "3.5.0-amd64-zh-cn-yunyangneural",
    "3.5.0-amd64-zh-cn-yunyeneural",
    "latest"
  ]
}
```

> [!IMPORTANT]
> We retired the standard speech synthesis voices and standard [text to speech](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/text-to-speech/tags) container on August 31, 2021. You should use neural voices with the [neural-text-to-speech](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/neural-text-to-speech/tags) container version 3.0 and higher instead. 
>
> Starting from February 29, 2024, the text to speech and neural text to speech container versions 2.19 and earlier aren't supported. For more information on updating your application, see [Migrate from standard voice to prebuilt neural voice](./how-to-migrate-to-prebuilt-neural-voice.md).

## Get the container image with docker pull

You need the [prerequisites](speech-container-howto.md#prerequisites) including required hardware. Also see the [recommended allocation of resources](speech-container-howto.md#container-requirements-and-recommendations) for each Speech container. 

Use the [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to download a container image from Microsoft Container Registry:

```bash
docker pull mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech:latest
```

> [!IMPORTANT]
> The `latest` tag pulls the `en-US` locale and `en-us-arianeural` voice. For additional locales and voices, see [text to speech container images](#container-images).

## Run the container with docker run

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container. 

# [Neural text to speech](#tab/container)

The following table represents the various `docker run` parameters and their corresponding descriptions:

| Parameter | Description |
|---------|---------|
| `{ENDPOINT_URI}` | The endpoint is required for metering and billing. For more information, see [billing arguments](speech-container-howto.md#billing-arguments). |
| `{API_KEY}` | The API key is required. For more information, see [billing arguments](speech-container-howto.md#billing-arguments). |

When you run the text to speech container, configure the port, memory, and CPU according to the text to speech container [requirements and recommendations](speech-container-howto.md#container-requirements-and-recommendations).

Here's an example `docker run` command with placeholder values. You must specify the `ENDPOINT_URI` and `API_KEY` values:

```bash
docker run --rm -it -p 5000:5000 --memory 12g --cpus 6 \
mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

This command:

* Runs a neural text to speech container from the container image.
* Allocates 6 CPU cores and 12 GB of memory.
* Exposes TCP port 5000 and allocates a pseudo-TTY for the container.
* Automatically removes the container after it exits. The container image is still available on the host computer.

# [Disconnected neural text to speech](#tab/disconnected)

To run disconnected containers (not connected to the internet), you must submit [this request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../containers/disconnected-containers.md) in the Azure AI services documentation.

If you're approved to run the container disconnected from the internet, the following example shows the formatting of the `docker run` command to use, with placeholder values. Replace these placeholder values with your own values.

The `DownloadLicense=True` parameter in your `docker run` command downloads a license file to enable your Docker container to run when it isn't connected to the internet. It also contains an expiration date, after which the license file is invalid to run the container. You can only use a license file with the appropriate container that you're approved for. For example, you can't use a license file for a `speech-to-text` container with a `neural-text-to-speech` container.

| Placeholder | Description | 
|-------------|-------|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/neural-text-to-speech:latest` |
| `{LICENSE_MOUNT}` | The path where the license is downloaded, and mounted.<br/><br/>For example: `/host/license:/path/to/license/directory` |
| `{ENDPOINT_URI}` | The endpoint for authenticating your service request. You can find it on your resource's **Key and endpoint** page, on the Azure portal.<br/><br/>For example: `https://<your-resource-name>.cognitiveservices.azure.com` |
| `{API_KEY}` | The key for your Speech resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal. |
| `{CONTAINER_LICENSE_DIRECTORY}` | Location of the license folder on the container's local filesystem.<br/><br/>For example: `/path/to/license/directory` |

```bash
docker run --rm -it -p 5000:5000 \ 
-v {LICENSE_MOUNT} \
{IMAGE} \
eula=accept \
billing={ENDPOINT_URI} \
apikey={API_KEY} \
DownloadLicense=True \
Mounts:License={CONTAINER_LICENSE_DIRECTORY} 
```

Once the license file is downloaded, you can run the container in a disconnected environment. The following example shows the formatting of the `docker run` command you use, with placeholder values. Replace these placeholder values with your own values.

Wherever the container is run, the license file must be mounted to the container and the location of the license folder on the container's local filesystem must be specified with `Mounts:License=`. An output mount must also be specified so that billing usage records can be written.

Placeholder | Value | Format or example |
|-------------|-------|---|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/neural-text-to-speech:latest` |
 `{MEMORY_SIZE}` | The appropriate size of memory to allocate for your container.<br/><br/>For example: `4g` |
| `{NUMBER_CPUS}` | The appropriate number of CPUs to allocate for your container.<br/><br/>For example: `4` |
| `{LICENSE_MOUNT}` | The path where the license is located and mounted.<br/><br/>For example: `/host/license:/path/to/license/directory` |
| `{OUTPUT_PATH}` | The output path for logging.<br/><br/>For example: `/host/output:/path/to/output/directory`<br/><br/>For more information, see [usage records](../containers/disconnected-containers.md#usage-records) in the Azure AI services documentation. |
| `{CONTAINER_LICENSE_DIRECTORY}` | Location of the license folder on the container's local filesystem.<br/><br/>For example: `/path/to/license/directory` |
| `{CONTAINER_OUTPUT_DIRECTORY}` | Location of the output folder on the container's local filesystem.<br/><br/>For example: `/path/to/output/directory` |

```bash
docker run --rm -it -p 5000:5000 --memory {MEMORY_SIZE} --cpus {NUMBER_CPUS} \ 
-v {LICENSE_MOUNT} \ 
-v {OUTPUT_PATH} \
{IMAGE} \
eula=accept \
Mounts:License={CONTAINER_LICENSE_DIRECTORY}
Mounts:Output={CONTAINER_OUTPUT_DIRECTORY}
```

Speech containers provide a default directory for writing the license file and billing log at runtime. The default directories are /license and /output respectively. 

When you're mounting these directories to the container with the `docker run -v` command, make sure the local machine directory is set ownership to `user:group nonroot:nonroot` before running the container.

Here's a sample command to set file/directory ownership.

```bash
sudo chown -R nonroot:nonroot <YOUR_LOCAL_MACHINE_PATH_1> <YOUR_LOCAL_MACHINE_PATH_2> ...
```

---

For more information about `docker run` with Speech containers, see [Install and run Speech containers with Docker](speech-container-howto.md#run-the-container).

## Use the container

[!INCLUDE [Speech container authentication](includes/containers-speech-config-http.md)]

[Try the text to speech quickstart](get-started-text-to-speech.md) using host authentication instead of key and region.

### SSML voice element

When you construct a neural text to speech HTTP POST, the [SSML](speech-synthesis-markup.md) message requires a `voice` element with a `name` attribute. The [locale of the voice](language-support.md?tabs=tts) must correspond to the locale of the container model. The [SSML tag](speech-synthesis-markup-structure.md) support is consistent for [each text to speech voice](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/neural-text-to-speech/tags) both in the Azure cloud and the container environment.

For example, a model that was downloaded via the `latest` tag (defaults to "en-US") would have a voice name of `en-US-AriaNeural`.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        This is the text that is spoken.
    </voice>
</speak>
```

## Next steps

* See the [Speech containers overview](speech-container-overview.md)
* Review [configure containers](speech-container-configuration.md) for configuration settings
* Use more [Azure AI containers](../cognitive-services-container-support.md)
