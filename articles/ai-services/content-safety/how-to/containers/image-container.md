---
title: Analyze image container - Azure AI content safety 
titleSuffix: Azure AI services
description: Install and run content safety analyze image containers with Docker to detect harmful content in image.
author: 
manager: 
ms.service: azure-ai-content-safety
ms.topic: 
ms.date: 9/11/2024
ms.author: 
keywords: on-premises, Docker, container
---

# Analyze image content with docker containers

The analyze image container scans image for sexual content, violence, hate, and self harm with multi-severity levels. In this article, you learn how to download, install, and run a content safety to image container.

For more information about prerequisites, validating that a container is running, running multiple containers on the same host, and running disconnected containers, see [Install and run content safety containers with Docker](container-install-run.md).

## Container images

The content safety analyze image container image for all supported versions can be found on the [Microsoft Container Registry (MCR)]( https://mcr.microsoft.com/en-us/product/azure-cognitive-services/contentsafety/image-analyze/tags) syndicate. It resides within the `azure-cognitive-services/contentsafety` repository and is named `image-analyze`.

 

**to do: update MCR screenshot** **[to-do]** update MCR screenshot for AACS image analyze image. the MCR release is in progress, expect to finish by EOD 9/20 PST. the MCR link is  https://mcr.microsoft.com/en-us/product/azure-cognitive-services/contentsafety/image-analyze/tags


The fully qualified container image name is, `mcr.microsoft.com/en-us/product/azure-cognitive-services/contentsafety/image-analyze`. Either append a specific version or append `:latest` to get the most recent version.

| Version | Path |
|-----------|------------|
| Latest | `mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest`<br/><br/>The `latest` tag pulls the latest image. |
|1.0.0-amd64-preview|`mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:1.0.0-amd64-preview`|

## Get the container image with docker pull

You need the [prerequisites](container-install-run.md#prerequisites) including required hardware. Also see the [recommended allocation of resources](container-install-run.md#host-computer-requirements-and-recommendations)
for each content safety container. 

Use the [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to download a container image from Microsoft Container Registry:

```bash
docker mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest
```


## Run the container with docker run

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container. 

# [Standard container](#tab/standard)

The following table represents the various `docker run` parameters and their corresponding descriptions:

| Parameter | Description |
|---------|---------|
| `{ENDPOINT_URI}` | The endpoint is required for metering and billing. For more information, see [billing arguments](content safety-container-howto.md#billing-arguments). |
| `{API_KEY}` | The API key is required. For more information, see [billing arguments](content safety-container-howto.md#billing-arguments). |

When you run the content safety to image container, configure the port, memory, and CPU according to the content safety to image container [requirements and recommendations](content safety-container-howto.md#container-requirements-and-recommendations).

Here's an example `docker run` command with placeholder values. You must specify the `ENDPOINT_URI` and `API_KEY` values:

```bash
docker run --rm -it -p 5000:5000 --gpus all \
mcr.microsoft.com/azure-cognitive-services/contentsafety/image-analyze:latest \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

This command:
* Runs an `image-analyze` container from the container image.
* `--gpus all` Use all available GPU resources. Content safety container requires CUDA for optimal performance. See more in  [host requirements and recommendations](./container-install-run.md#host-computer-requirements-and-recommendations). Also make sure your host install [NVIDIA container toolkit](./container-install-run.md#installing-the-nvidia-container-toolkit).
* Exposes TCP port 5000 and allocates a pseudo-TTY for the container.
* Automatically removes the container after it exits. The container image is still available on the host computer.

# [Disconnected container](#tab/disconnected)

To run disconnected containers (not connected to the internet), you must submit [this request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../containers/disconnected-containers.md) in the Azure AI services documentation.

If you're approved to run the container disconnected from the internet, the following example shows the formatting of the `docker run` command to use, with placeholder values. Replace these placeholder values with your own values.

The `DownloadLicense=True` parameter in your `docker run` command downloads a license file to enable your Docker container to run when it isn't connected to the internet. It also contains an expiration date, after which the license file is invalid to run the container. You can only use a license file with the appropriate container that you're approved for. For example, you can't use a license file for a `content safety-to-image` container with a `neural-image-to-content safety` container.

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

Once the license file is downloaded, you can run the container in a disconnected environment. The following example shows the formatting of the `docker run` command you use, with placeholder values. Replace these placeholder values with your own values.

Wherever the container is run, the license file must be mounted to the container and the location of the license folder on the container's local filesystem must be specified with `Mounts:License=`. An output mount must also be specified so that billing usage records can be written.

Placeholder | Value | Format or example |
|-------------|-------|---|
| `{IMAGE}` | The container image you want to use.<br/><br/>For example: `mcr.microsoft.com/azure-cognitive-services/content safety-to-image:latest` |
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

Content safety containers provide a default directory for writing the license file and billing log at runtime. The default directories are /license and /output respectively. 

When you're mounting these directories to the container with the `docker run -v` command, make sure the local machine directory is set ownership to `user:group nonroot:nonroot` before running the container.

Here's a sample command to set file/directory ownership.

```bash
sudo chown -R nonroot:nonroot <YOUR_LOCAL_MACHINE_PATH_1> <YOUR_LOCAL_MACHINE_PATH_2> ...
```

---

## Test the container

Once the container is up and running, you can validate its operation by sending a request to the REST endpoint deployed within the container. To do this, follow below article. Note, you need to replace the endpoint URL with the Docker URL specific to your container deployment. Also, ensure that you're using host authentication, rather than key-based authentication.

[Analyze image quick start](./quickstart-text.md#analyze-image-content)





## Next steps

* See the [content safety containers overview](./container-overview.md)
* Review [configure containers](./install-run-container.md) for configuration settings
* Use more [Azure AI containers](../../../cognitive-services-container-support.md)