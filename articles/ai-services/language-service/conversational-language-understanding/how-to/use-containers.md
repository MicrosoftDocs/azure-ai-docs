---
title: Use conversational language understanding (CLU) Docker containers on-premises
titleSuffix: Foundry Tools
description: Use Docker containers for the conversational language understanding (CLU) API to determine the language of written text, on-premises.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---
# Install and run Conversational Language Understanding (CLU) containers

> [!NOTE]
> The data limits in a single synchronous API call for the CLU container are 5,120 characters per document and up to 10 documents per call.

Containers enable you to host the CLU API on your own infrastructure. If you have security or data governance requirements that can't be fulfilled by calling CLU remotely, then containers might be a good option.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Prerequisites

You must meet the following prerequisites before using CLU containers.

* An active Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* [Docker](https://docs.docker.com/) installed on a host computer. Docker must be configured to allow the containers to connect with and send billing data to Azure.
    * On Windows, Docker must also be configured to support Linux containers.
    * You should have a basic understanding of [Docker concepts](https://docs.docker.com/get-started/overview/).
* A <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics"  title="Create a Language resource"  target="_blank">Language resource </a>

[!INCLUDE [Gathering required parameters](../../../containers/includes/container-gathering-required-parameters.md)]

## Host computer requirements and recommendations

[!INCLUDE [Host Computer requirements](../../../includes/cognitive-services-containers-host-computer.md)]

The following table describes the minimum and recommended specifications for the available container. Each CPU core must be at least 2.6 gigahertz (GHz) or faster.

We recommended that you have a CPU with AVX-512 instruction set, for the best experience (performance and accuracy).

|  Processor   | Minimum host specs     | Recommended host specs |
|---------------------|------------------------|------------------------|
| **CPU**     | 1-core, 2-GB memory     | 4-cores, 8-GB memory    |

CPU core and memory correspond to the `--cpus` and `--memory` settings, which are used as part of the `docker run` command.

## Export your Conversational Language Understanding model

Before you proceed with running the docker image, you need to export your own trained model to expose it to your container. Use the following command to extract your model and replace the placeholders with your own values:

|Placeholder |Value|Format or example|
|------------|-----|-----------------|
|**{API_KEY}** |The key for your Language resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal.|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
|**{ENDPOINT_URI}**|The endpoint for accessing the Conversational Language Understanding API. You can find it on your resource's **Key and endpoint** page, on the Azure portal.|`https://<your-custom-subdomain>.cognitiveservices.azure.com`|
|**{PROJECT_NAME}**|The name of the project containing the model that you want to export. You can find it on your projects tab in Azure Language Studio portal.|myProject|
|**{TRAINED_MODEL_NAME}** |The name of the trained model you want to export. You can find your trained models on your model evaluation tab under your project in Azure Language Studio portal|myTrainedModel|
|**{EXPORTED_MODEL_NAME}** |The name to assign for the new exported model created.|myExportedModel |

```bash
curl --location --request PUT '{ENDPOINT_URI}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}/exported-models/{EXPORTED_MODEL_NAME}?api-version=2024-11-15-preview' \
--header 'Ocp-Apim-Subscription-Key: {API_KEY}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "TrainedModelLabel": "{TRAINED_MODEL_NAME}"
}'
```

## Get the container image with `docker pull`

The CLU container image can be found on the `mcr.microsoft.com` container registry syndicate. It resides within the `azure-cognitive-services/language/` repository and is named `clu`. The fully qualified container image name is, `mcr.microsoft.com/azure-cognitive-services/language/clu`

 To use the latest version of the container, you can use the `latest` tag, which is for English. You can also find a full list of containers for supported languages using the [tags on the MCR](https://mcr.microsoft.com/product/azure-cognitive-services/language/clu/tags).

The latest CLU container is available in several languages. To download the container for the English container, use the following command:

```bash
  docker pull mcr.microsoft.com/azure-cognitive-services/language/clu:latest
```

[!INCLUDE [Tip for using docker list](../../../includes/cognitive-services-containers-docker-list-tip.md)]

## Run the container in download model mode

After the exported model is created, users have to run the container to download the deployment package that was created specifically for their exported models.

| Placeholder| Value | Format or example  |
|---|---|---|
| **{API_KEY}**| The key for your Language resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal. | See Azure portal |
| **{ENDPOINT_URI}** | The endpoint for accessing the API. You can find it on your resource's **Key and endpoint** page, on the Azure portal. | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
| **{IMAGE_TAG}** | The image tag representing the language of the container you want to run. Make sure the tag matches the `docker pull` command you used.  | latest|
| **{LOCAL_CLU_PORT}** | Port number assigned for the container in local machine.| 5000 |
| **{LOCAL_MODEL_DIRECTORY}** | Absolute directory in host machine where exported models are saved in. | `C:\usr\local\myDeploymentPackage` |
| **{PROJECT_NAME}**| Name of the project that the exported model belongs to  | myProject  |
| **{EXPORTED_MODEL_NAME}**   | Exported model to be downloaded | myExportedModel   |


  
  ```bash
    docker run --rm -it -p {LOCAL_CLU_PORT}:80 \
    mcr.microsoft.com/azure-cognitive-services/language/clu:{IMAGE_TAG} \ 
    -v {LOCAL_MODEL_DIRECTORY}:/DeploymentPackage \
    Billing={ENDPOINT_URI} \ 
    ApiKey={API_KEY} \
    downloadmodel \
    projectName={PROJECT_NAME} \
    exportedModelName={EXPORTED_MODEL_NAME}
  ```

DO NOT alter the downloaded files. Even altering the name or folder structure can affect the integrity of the container and might break it.

Repeat those steps to download as many models as you'd like to test. Your models can belong to different projects and have different (exported) model names.

## Run the container with `docker run`

Once the container is on the host computer, use the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command to run the containers. The container continues to run until you stop it. Replace the placeholders with your own values:


> [!IMPORTANT]
> * The docker commands in the following sections use the back slash, `\`, as a line continuation character. Replace or remove the back slash based on your host operating system's requirements.
> * The `Eula`, `Billing`, and `ApiKey` options must be specified to run the container; otherwise, the container doesn't start. For more information, see [Billing](#billing).

To run the CLU container, execute the following `docker run` command. Replace the placeholders with your own values:

| Placeholder | Value | Format or example |
|-------------|-------|---|
| **{API_KEY}** | The key for your Language resource. You can find it on your resource's **Key and endpoint** page, on the Azure portal. |`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`|
| **{ENDPOINT_URI}** | The endpoint for accessing the API. You can find it on your resource's **Key and endpoint** page, on the Azure portal. | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
| **{IMAGE_TAG}** | The image tag representing the language of the container you want to run. Make sure the tag matches the `docker pull` command you used. | `latest` |
|**{LOCAL_CLU_PORT}** |Port number assigned for the container in local machine. |5000 |
|**{LOCAL_NER_PORT}** |Port number of the `NER` container. See Run `NER` Container section. |5001 (Has to be different than the port number) |
|**{LOCAL_LOGGING_DIRECTORY}** |Absolute directory in host machine where that logs are saved in. |`C:\usr\local\mylogs` |
|**{LOCAL_MODEL_DIRECTORY}** |Absolute directory in host machine where exported models are saved in. |`C:\usr\local\myDeploymentPackage` |

```bash
docker run --rm -it -p 5000:5000 --memory 8g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/language/clu:{IMAGE_TAG} \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

This command:

* Runs a *CLU* container from the container image
* Allocates one CPU core and 8 gigabytes (GB) of memory
* Exposes `TCP` port 5000 and allocates a pseudo-TTY for the container
* Automatically removes the container after it exits. The container image is still available on the host computer.

[!INCLUDE [Running multiple containers on the same host](../../../includes/cognitive-services-containers-run-multiple-same-host.md)]

## Running named entity recognition (NER) Container
CLU relies on NER to handle prebuilt entities. The CLU container works properly without NER if users decide not to integrate it. NER billing is turned off when accessed via CLU, so there are no added charges unless you make a direct call to the NER container.

To set up NER in CLU container
- Follow the [NER container documentation](../../named-entity-recognition/how-to/use-containers.md).
- When running CLU container, make sure to set the parameter `Ner_Url `so that `Ner_Url=http://host.docker.internal:{LOCAL_NER_PORT}`

## Query the container's prediction endpoint

The container provides REST-based query prediction endpoint APIs.

Use the host, `http://localhost:5000`, for container APIs.

<!-- ## Validate container is running -->

[!INCLUDE [Container's API documentation](../../../includes/cognitive-services-containers-api-documentation.md)]

For information on how to call CLU see [our guide](call-api.md).

## Run the container disconnected from the internet

[!INCLUDE [configure-disconnected-container](../../../containers/includes/configure-disconnected-container.md)]

## Stop the container

[!INCLUDE [How to stop the container](../../../includes/cognitive-services-containers-stop.md)]

## Troubleshooting

If you run the container with both an output [mount](../../concepts/configure-containers.md#mount-settings) and logging enabled, the container generates log files. The log files can help you troubleshoot any issues that occur during startup or while the container is running.

[!INCLUDE [Foundry Tools FAQ note](../../../containers/includes/cognitive-services-faq-note.md)]

## Billing

The CLU containers send billing information to Azure, using a _Language_ resource on your Azure account.

[!INCLUDE [Container's Billing Settings](../../../includes/cognitive-services-containers-how-to-billing-info.md)]

For more information about these options, see [Configure containers](../../concepts/configure-containers.md).

## Summary

In this article, you learned concepts and workflow for downloading, installing, and running CLU containers. In summary:

* CLU provides Linux containers for Docker
* Container images are downloaded from the Microsoft Container Registry (MCR).
* Container images run in Docker.
* You must specify billing information when instantiating a container.

> [!IMPORTANT]
> Azure AI containers aren't licensed to run without being connected to Azure for metering. Customers must enable containers to always communicate billing information to the metering service. Azure AI containers don't send customer data (for example, text that is being analyzed) to Microsoft.

## Next steps

* See [Configure containers](../../concepts/configure-containers.md) for configuration settings.
