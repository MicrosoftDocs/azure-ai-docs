---
title: Configure containers - Language service
titleSuffix: Foundry Tools
description: Language service provides each container with a common configuration framework, so that you can easily configure and manage storage, logging, and security settings for your containers.
author: laujan
manager: nitinme
ms.custom:
  - ignite-2023
  - ignite-2024
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 12/05/2025
ms.author: lajanuar
---
# Configure Language docker containers

Language provides each container with a common configuration framework, so that you can easily configure and manage storage, logging, and security settings for your containers. This article applies to the following containers:

* Sentiment Analysis
* Language Detection
* Key Phrase Extraction
* Text Analytics for Health
* Summarization
* Named Entity Recognition (NER)
* Personally Identifiable (PII) detection
* Conversational Language Understanding (CLU)

## Configuration settings

[!INCLUDE [Container shared configuration settings table](../../includes/cognitive-services-containers-configuration-shared-settings-table.md)]

> [!IMPORTANT]
> The [`ApiKey`](#apikey-configuration-setting), [`Billing`](#billing-configuration-setting), and [`Eula`](#end-user-license-agreement-eula-setting) settings are used together, and you must provide valid values for all three of them; otherwise your container doesn't start.

## ApiKey configuration setting

The `ApiKey` setting specifies the Azure resource key used to track billing information for the container. You must specify a value for the key and it must be a valid key for the _Language_ resource specified for the [`Billing`](#billing-configuration-setting) configuration setting.

## ApplicationInsights setting

[!INCLUDE [Container shared configuration ApplicationInsights settings](../../includes/cognitive-services-containers-configuration-shared-settings-application-insights.md)]

## Billing configuration setting

The `Billing` setting specifies the endpoint URI of the _Language_ resource on Azure used to meter billing information for the container. You must specify a value for this configuration setting, and the value must be a valid endpoint URI for a _Language_ resource on Azure. The container reports usage about every 10 to 15 minutes.

|Required| Name | Data type | Description |
|--|------|-----------|-------------|
|Yes| `Billing` | String | Billing endpoint URI. |


## End-user license agreement (EULA) setting

[!INCLUDE [Container shared configuration eula settings](../../includes/cognitive-services-containers-configuration-shared-settings-eula.md)]

## Fluentd settings

[!INCLUDE [Container shared configuration fluentd settings](../../includes/cognitive-services-containers-configuration-shared-settings-fluentd.md)]

## Http proxy credentials settings

[!INCLUDE [Container shared configuration proxy settings](../../includes/cognitive-services-containers-configuration-shared-settings-http-proxy.md)]

## Logging settings
 
[!INCLUDE [Container shared configuration logging settings](../../includes/cognitive-services-containers-configuration-shared-settings-logging.md)]

## Mount settings

Use bind mounts to read and write data to and from the container. You can specify an input mount or output mount by specifying the `--mount` option in the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command.

The Language containers don't use input or output mounts to store training or service data. 

The exact syntax of the host mount location varies depending on the host operating system. The host computer's mount location may not be accessible due to a conflict between the docker service account permissions and the host mount location permissions. 

|Optional| Name | Data type | Description |
|-------|------|-----------|-------------|
|Not allowed| `Input` | String | Language containers don't use this data type.|
|Optional| `Output` | String | The target of the output mount. The default value is `/output`. It's the location of the logs. This output includes container logs. <br><br>Example:<br>`--mount type=bind,src=c:\output,target=/output`|

## Next steps

* Use more [Azure AI containers](../../cognitive-services-container-support.md)
