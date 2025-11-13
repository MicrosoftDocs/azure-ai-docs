---
title: Install and run content safety containers with Docker - Content Safety service
titleSuffix: Azure AI Foundry Tools
description: Use the content safety containers with Docker to perform content safety check on-premises.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 09/16/2025
ms.author: pafarley
keywords: on-premises, Docker, container
---

# Install and run content safety containers with Docker (preview)

By using containers, you can use a subset of the Azure AI Content Safety features in your own environment. In this article, you learn how to download, install, and run a content safety container.

> [!NOTE]
> Disconnected container pricing and commitment tiers vary from standard containers. For more information, see [content safety service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Prerequisites

You must meet the following prerequisites before you use content safety containers. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin. You need:
* [Docker](https://docs.docker.com/) installed on a host computer. Docker must be configured to allow the containers to connect with and send billing data to Azure.
    * On Windows, Docker must also be configured to support Linux containers.
    * You should have a basic understanding of [Docker concepts](https://docs.docker.com/get-started/overview/). 
* A <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicescontent safetyServices"  title="Create a content safety service resource"  target="_blank">content safety service resource </a> with the standard (S) [pricing tier](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Billing information

Content safety containers aren't licensed to run without being connected to Azure for metering. You must configure your container to always communicate billing information with the metering service. 

Three primary parameters for all Azure AI containers are required. The Microsoft Software License Terms must be present with a value of **accept**. An endpoint URL and API key are also needed.

Queries to the container are billed at the pricing tier of the Azure resource that's used for the `ApiKey` parameter.

The <a href="https://docs.docker.com/engine/reference/commandline/run/" target="_blank">`docker run` <span class="docon docon-navigate-external x-hidden-focus"></span></a> command starts the container when all three of the following options are provided with valid values:

| Option | Description |
|--------|-------------|
| `ApiKey` | The API key of the content safety resource that's used to track billing information.<br/>The `ApiKey` value is used to start the container and is available on the Azure portal's **Keys** page of the corresponding content safety resource. Go to the **Keys** page, and select the **Copy to clipboard** <span class="docon docon-edit-copy x-hidden-focus"></span> icon.|
| `Billing` | The endpoint of the content safety resource that's used to track billing information.<br/>The endpoint is available on the Azure portal **Overview** page of the corresponding content safety resource. Go to the **Overview** page, hover over the endpoint, and a **Copy to clipboard** <span class="docon docon-edit-copy x-hidden-focus"></span> icon appears. Copy and use the endpoint where needed.|
| `Eula` | Indicates that you accepted the license for the container.<br/>The value of this option must be set to **accept**. |

> [!IMPORTANT]
> These subscription keys are used to access your Azure AI services API. Don't share your keys. Store them securely. For example, use Azure Key Vault. We also recommend that you regenerate these keys regularly. Only one key is needed to make an API call. When you regenerate the first key, you can use the second key for continued access to the service.

The container needs the billing argument values to run. These values allow the container to connect to the billing endpoint. The container reports usage about every 10 to 15 minutes. If the container doesn't connect to Azure within the allowed time window, the container continues to run but doesn't serve queries until the billing endpoint is restored. The connection is attempted 10 times at the same time interval of 10 to 15 minutes. If it can't connect to the billing endpoint within the 10 tries, the container stops serving requests. For an example of the information sent to Microsoft for billing, see the [Azure AI container FAQ](../../../containers/container-faq.yml#how-does-billing-work) in the Azure AI services documentation.


## Host computer requirements and recommendations

The host is an x64-based computer that runs the Docker container. It can be a computer on your premises or a Docker hosting service in Azure.

The following table describes the minimum and recommended specifications for the content safety containers. It applies to both text and image container. 

| Recommended number of CPU cores  | Recommended memory | Notes |
|---------|--------------------|-------|
| 4               | 16 GB         | Requires NVIDIA CUDA.|


Content safety containers require NVIDIA CUDA for optimal performance. The container is tested on CUDA 11.8 and CUDA 12.6. 

The minimum GPU requirement for these containers is NVIDIA's T4, however, we recommend using the A100 for optimal performance.

The table below presents the requests per second (RPS) and latency metrics obtained when the containers were tested on a single-node GPU configuration using NVIDIA's T4 and A100 GPUs.

Even with identical GPUs, performance can fluctuate based on the GPU load and the specific configuration of the environment. The benchmark data we provide should be used as a reference point when considering the deployment of content safety containers in your environment. For the most accurate assessment, we recommend conducting tests within your specific environment.

#### [Analyze text](#tab/text)

|GPU| Max RPS| Average latency (at Max RPS)|
|---|---|---|
| T4 | 130 | 50.4 ms |
| A100 | 360 | 8.7 |

#### [Analyze image](#tab/image)

|GPU| Max RPS| Average latency (at Max RPS)|
|---|---|---|
| T4 | 15 | 229 ms |
| A100 | 30 | 799 ms |

---

## Install the NVIDIA container toolkit

The `host` is the computer that runs the docker container. The host must support NVIDIA container toolkit. Follow the below guidance to install the toolkit in your environment.

[Install the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)


## Run the container

Use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the container. Once running, the container continues to run until you [stop the container](#stop-the-container).

Note the following best practices for the `docker run` command:

- **Line-continuation character**: The Docker commands in the following sections use the back slash, `\`, as a line continuation character. Replace or remove this character based on your host operating system's requirements.
- **Argument order**: Don't change the order of the arguments unless you're familiar with Docker containers.

You can use the [docker images](https://docs.docker.com/engine/reference/commandline/images/) command to list your downloaded container images. The following command lists the ID, repository, and tag of each downloaded container image, formatted as a table:

```bash
docker images --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
```

Here's an example result:

```
IMAGE ID         REPOSITORY                TAG
<image-id>       <repository-path/name>    <tag-name>
```

## Validate the container

There are several ways to validate that the container is running. Locate the *External IP* address and exposed port of the container in question, and open your preferred web browser. Use the various request URLs that follow to validate the container is running. 

The example request URLs listed here are `http://localhost:5000`, but your specific container might vary. Make sure to rely on your container's *External IP* address and exposed port.

| Request URL | Purpose |
|--|--|
| `http://localhost:5000/ready` | Requested with GET, this URL provides a verification that the container is ready to accept a query against the model. This request can be used for Kubernetes [liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/). |
| `http://localhost:5000/status` | Also requested with GET, this URL verifies if the api-key used to start the container is valid without causing an endpoint query. This request can be used for Kubernetes [liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/). |
| `http://localhost:5000/api-docs/index.html` | The container provides a full set of documentation for the endpoints and a **Try it out** feature. With this feature, you can enter your settings into a web-based HTML form and make the query without having to write any code. After the query returns, an example CURL command is provided to demonstrate the HTTP headers and body format that's required. |

## Stop the container

To shut down the container, enter <kbd>Ctrl+C</kbd> in the command-line environment where the container is running.

## Run multiple containers on the same host

If you intend to run multiple containers with exposed ports, make sure to run each container with a different exposed port. For example, run the first container on port 5000 and the second container on port 5001.

You can have this container and a different Azure AI container running on the host together. You also can have multiple instances of the same Azure AI container running.

### Host URLs 

> [!NOTE]
> Use a unique port number if you're running multiple containers.
>
> |Protocol | Host URL |
> |---|---|
> | WS | `ws://localhost:5000` | 
> | HTTP | `http://localhost:5000` |

For more information on using WSS and HTTPS protocols, see [Container security](../../../cognitive-services-container-support.md#foundry-tools-container-security) in the Azure AI Foundry Tools documentation.

## Troubleshooting

When you start or run the container, you might experience issues. Use an output mount and enable logging. Doing so allows the container to generate log files that are helpful when you troubleshoot issues.

> [!TIP]
> For more troubleshooting information and guidance, see [Azure AI containers frequently asked questions (FAQ)](../../../containers/container-faq.yml) in the Azure AI Foundry Tools documentation.

### Logging settings

Content safety containers come with ASP.NET Core logging support. Here's an example of the `neural-text-to-content safety container` started with default logging to the console:

```bash
docker run --rm -it -p 5000:5000 --memory 12g --cpus 6 \
mcr.microsoft.com/azure-cognitive-services/content safetyservices/neural-text-to-content safety \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY} \
Logging:Console:LogLevel:Default=Information
```

For more information about logging, see [usage records](../../../containers/disconnected-containers.md#usage-records) in the Azure AI Foundry Tools documentation.

### Microsoft diagnostics container

If you're having trouble running an Azure AI container, you can try using the Microsoft diagnostics container. Use this container to diagnose common errors in your deployment environment that might prevent Azure AI containers from functioning as expected.

To get the container, use the following `docker pull` command:

```bash
docker pull mcr.microsoft.com/azure-cognitive-services/diagnostic
```

Then run the container. Replace `{ENDPOINT_URI}` with your endpoint, and replace `{API_KEY}` with your key to your resource:

```bash
docker run --rm mcr.microsoft.com/azure-cognitive-services/diagnostic \
eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

The container tests for network connectivity to the billing endpoint.

## Run disconnected containers

To run disconnected containers (not connected to the internet), you must submit [this request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../../../containers/disconnected-containers.md) in the Azure AI Foundry Tools documentation.

## Related content

* Review [analyze text container](./text-container.md) for text container configuration settings.
*  Review [analyze image container](./image-container.md) for image container configuration settings.
* Use more [Azure AI containers](../../../cognitive-services-container-support.md).
