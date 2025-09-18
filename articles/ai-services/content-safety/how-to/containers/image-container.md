---
title: Analyze image container - Azure AI Content Safety 
titleSuffix: Azure AI services
description: Install and run content safety analyze image containers with Docker to detect harmful content in image.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 09/16/2025
ms.author: pafarley
keywords: on-premises, Docker, container
---

# Analyze image content with docker containers (preview)

The Analyze image container scans images for sexual content, violence, hate, and self-harm with multi-severity levels. This guide shows how to download, install, and run a content safety image container.

For more information about prerequisites, validating that a container is running, running multiple containers on the same host, and running disconnected containers, see [Install and run content safety containers with Docker](./install-run-container.md).

## Specify a container image

The content safety analyze image container image for all supported versions can be found on the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/contentsafety/image-analyze/tags) syndicate. It resides in the `azure-cognitive-services/contentsafety` repository and is named `image-analyze`.

:::image type="content" source="../../media/image-container.png" lightbox="../../media/image-container.png" alt-text="Screenshot of image container on registry website.":::


The fully qualified container name is, `mcr.microsoft.com/en-us/product/azure-cognitive-services/contentsafety/image-analyze`. Append a specific container version, or append `:latest` to get the most recent version. For example:

| Version | Path |
|-----------|------------|
| Latest | `mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest`<br/><br/>The `latest` tag pulls the latest image. |
|`1.0.0-amd64-preview`|`mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:1.0.0-amd64-preview`|

## Get the container image

Make sure you meet the [prerequisites](./install-run-container.md#prerequisites), including required hardware. Also see the [recommended allocation of resources](./install-run-container.md#host-computer-requirements-and-recommendations) section for each content safety container.

Use the [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to download a container image from Microsoft Container Registry:

```bash
docker mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest
```


## Run the container

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container. 

# [Standard container](#tab/standard)

The following table represents the various `docker run` parameters and their corresponding descriptions:

| Parameter | Description |
|---------|---------|
| `{ENDPOINT_URI}` | The endpoint is required for metering and billing. For more information, see [billing arguments](./install-run-container.md#billing-information). |
| `{API_KEY}` | The API key is required. For more information, see [billing arguments](./install-run-container.md#billing-information). |

When you run the content safety analyze image container, configure the port, memory, and CPU according to the [requirements and recommendations](./install-run-container.md#host-computer-requirements-and-recommendations).

Here's a sample `docker run` command with placeholder values. You must specify the `ENDPOINT_URI` and `API_KEY` values:

```bash
docker run --rm -it -p 5000:5000 --gpus all \
mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

Command details::
* Runs an `image-analyze` container from the container image.
* Uses all available GPU resources (by specifying `--gpus all`). Content safety containers require CUDA for optimal performance. Learn more in [host requirements and recommendations](./install-run-container.md#host-computer-requirements-and-recommendations). Also make sure your host installs [NVIDIA container toolkit](./install-run-container.md#install-the-nvidia-container-toolkit).
* Exposes TCP port 5000 and allocates a pseudo-TTY for the container.
* Automatically removes the container after it exits. The container image is still available on the host computer.

# [Disconnected container](#tab/disconnected)

To run disconnected containers (not connected to the internet), you must submit a [request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../../../containers/disconnected-containers.md) in the Azure AI services documentation.

If you're approved to run the disconnected container, the following example shows the formatting of the `docker run` command to use, with placeholder values. Replace these values with your own values.


| Placeholder | Description | 
|-------------|-------|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/content safety-to-image:latest` |
| `{LICENSE_MOUNT}` | The path where the license is downloaded, and mounted.<br/><br/>For example: `/host/license:/path/to/license/directory` |
| `{ENDPOINT_URI}` | The endpoint for authenticating your service request. You can find it on your resource's **Key and endpoint** page, on the Azure portal.<br/><br/>For example: `https://<your-resource-name>.cognitiveservices.azure.com` |
| `{API_KEY}` | The key for your content safety resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal. |
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

The `DownloadLicense=True` parameter in your `docker run` command downloads a license file to enable your Docker container to run when it isn't connected to the internet. It also contains an expiration date, after which the license file is invalid to run the container. You can only use a license file with the appropriate container that you're approved for. For example, you can't use a license file for a `content safety-to-image` container with a `neural-image-to-content-safety` container.


Once the license file is downloaded, you can run the container in a disconnected environment. The following example shows the formatting of the `docker run` command you use, with placeholder values. Replace these values with your own values.

Wherever the container is run, the license file must be mounted to the container and the location of the license folder on the container's local filesystem must be specified with `Mounts:License=`. An output mount must also be specified so that billing usage records can be written.

Placeholder | Value | Format or example |
|-------------|-------|---|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/content safety-to-image:latest` |
 `{MEMORY_SIZE}` | The appropriate size of memory to allocate for your container.<br/><br/>For example: `4g` |
| `{NUMBER_CPUS}` | The appropriate number of CPUs to allocate for your container.<br/><br/>For example: `4` |
| `{LICENSE_MOUNT}` | The path where the license is located and mounted.<br/><br/>For example: `/host/license:/path/to/license/directory` |
| `{OUTPUT_PATH}` | The output path for logging.<br/><br/>For example: `/host/output:/path/to/output/directory`<br/><br/>For more information, see [usage records](../../../containers/disconnected-containers.md#usage-records) in the Azure AI services documentation. |
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

Content safety containers provide a default directory for writing the license file and billing log at runtime. The default directories are `/license` and `/output` respectively. 

When you're mounting these directories to the container with the `docker run -v` command, make sure the local machine directory has set ownership to `user:group nonroot:nonroot` before running the container.

Here's a sample command to set file/directory ownership:

```bash
sudo chown -R nonroot:nonroot <YOUR_LOCAL_MACHINE_PATH_1> <YOUR_LOCAL_MACHINE_PATH_2> ...
```

---

## Test the container

Once the container is up and running, you can validate its operation by sending a request to the REST endpoint deployed within the container. To do this, follow the steps in the quickstart. Note, you need to replace the endpoint URL with the Docker URL specific to your container deployment. Also, ensure that you're using host authentication, rather than key-based authentication.

[Analyze image quickstart](../../quickstart-image.md)


## Next steps

* See the [content safety containers overview](./container-overview.md)
* Review [configure containers](./install-run-container.md) for configuration settings
* Use more [Azure AI containers](../../../cognitive-services-container-support.md)