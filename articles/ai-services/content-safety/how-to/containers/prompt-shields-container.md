---
title: Prompt Shields container - Azure AI Content Safety 
titleSuffix: Azure AI services
description: Install and run content safety prompt shields containers with Docker to detect and mitigate user prompt attacks.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 02/05/2026
ms.author: pafarley
keywords: on-premises, Docker, container
---

# Prompt Shields for user prompts and documents with Docker container (preview) 

The prompt shields for user prompts and documents container scans for both User Prompt Attacks (malicious or harmful user-generated inputs) and Document Attacks (inputs containing harmful content embedded within documents). This guide shows you how to download, install, and run a content safety prompt shields container. 

For more information about prerequisites, validating that a container is running, running multiple containers on the same host, and running disconnected containers, see [Install and run content safety containers with Docker](./install-run-container.md).

## Specify a container image

The content safety prompt shields container image for all supported versions can be found on the [Microsoft Container Registry (MCR)](https://aka.ms/aacscontainermcr) syndicate. It resides within the `azure-cognitive-services/contentsafety` repository and is named `promptshields`. 

:::image type="content" source="../../media/prompt-shields-container.png" lightbox="../../media/prompt-shields-container.png" alt-text="Screenshot of Prompt Shields container on registry website.":::

The fully qualified container image name is, `mcr.microsoft.com/azure-cognitive-services/contentsafety/promptshields`. Append a specific container version, or append `:latest` to get the most recent version. For example:

| Version | Path |
|-----------|------------|
| Latest | `mcr.microsoft.com/azure-cognitive-services/contentsafety/promptshields:latest`<br/><br/>The `latest` tag pulls the latest image. |
|1.0.0-amd64-preview|`mcr.microsoft.com/azure-cognitive-services/contentsafety/promptshields:1.0.0-amd64-preview`|


## Get the container image

Make sure you meet the [prerequisites](./install-run-container.md#prerequisites) including required hardware. Also see the [recommended allocation of resources](./install-run-container.md#host-computer-requirements-and-recommendations) section for each content safety container. 

Use the [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to download a container image from Microsoft Container Registry:

```bash
docker pull mcr.microsoft.com/azure-cognitive-services/contentsafety/promptshields:latest
```

## Run the container

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container. 

# [Standard Container](#tab/standard)

The following table represents the various `docker run` parameters and their corresponding descriptions:

| Parameter | Description |
|---------|---------|
| `{ENDPOINT_URI}` | The endpoint is required for metering and billing. For more information, see [billing arguments](./install-run-container.md#billing-information). |
| `{API_KEY}` | The API key is required. For more information, see [billing arguments](./install-run-container.md#billing-information). |

When you run the content safety prompt shields container, configure the port, GPU according to the content safety container [requirements and recommendations](./install-run-container.md#host-computer-requirements-and-recommendations).

Here's a sample `docker run` command with placeholder values. You must specify the `ENDPOINT_URI` and `API_KEY` values:

```bash
docker run --rm -it -p 5000:5000 --gpus all \
mcr.microsoft.com/azure-cognitive-services/contentsafety/promptshields:latest \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

Command details:
* Runs a `content safety` container from the container image.
* Uses all available GPU resources (by specifying `--gpus all`). Content safety container requires CUDA for optimal performance. See more in  [host requirements and recommendations](./install-run-container.md#host-computer-requirements-and-recommendations). Also make sure your host install [NVIDIA container toolkit](./install-run-container.md#install-the-nvidia-container-toolkit)
* Exposes TCP port 5000 and allocates a pseudo-TTY for the container.
* Automatically removes the container after it exits. The container image is still available on the host computer.

If you're testing the container on a machine without CUDA, the container exits when trying to use CUDA. Use below command to disable CUDA to continue the testing.

```bash
docker run -e CUDA_ENABLED=false
```



## Test the container

Once the container is up and running, you can validate its operation by sending a request to the REST endpoint deployed within the container. To do this, follow the steps in the quickstart. Note, you need to replace the endpoint URL with the Docker URL specific to your container deployment. Also, ensure that you're using host authentication, rather than key-based authentication.

[Prompt shields quickstart](../../quickstart-jailbreak.md)


## Next steps

* See the [content safety containers overview](./container-overview.md)
* Use more [Azure AI containers](../../../cognitive-services-container-support.md)