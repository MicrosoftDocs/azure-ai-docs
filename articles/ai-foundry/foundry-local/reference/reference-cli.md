---
title: Foundry Local CLI Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local command-line interface.
manager: scottpolly
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.author: jburchel
ms.reviewer: samkemp
author: jburchel
reviewer: samuel100
ms.topic: concept-article
ms.date: 05/20/2025
---

# Foundry Local CLI Reference

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article provides a comprehensive reference for the Foundry Local command-line interface (CLI). The CLI organizes commands into logical categories to help you manage models, control the service, and maintain your local cache.

## Overview

View all available commands with the help option:

```bash
foundry --help
```

The CLI organizes commands into three main categories:

- **Model**: Commands for managing and running AI models
- **Service**: Commands for controlling the Foundry Local service
- **Cache**: Commands for managing your local model storage

## Model commands

The following table summarizes the commands related to managing and running models:

> [!NOTE]
> You can specify the `model` argument by its **alias** or **model ID**. Using an alias will:
> - Select the *best model* for your available hardware. For example, if you have a Nvidia CUDA GPU available, Foundry Local selects the CUDA model. If you have a supported NPU available, Foundry Local selects the NPU model.
> - Allow you to use a shorter name without needing to remember the model ID.
>
> If you want to run a specific model, you can use the model ID. For example, to run the `qwen2.5-0.5b` on CPU - irrespective of your available hardware - use: `foundry model run qwen2.5-0.5b-instruct-generic-cpu`.


| **Command**                                     | **Description**                                                                  |
| --------------------------------------          | -------------------------------------------------------------------------------- |
| `foundry model --help`                          | Displays all available model-related commands and their usage.                   |
| `foundry model run <model>`            | Runs a specified model, downloading it if not cached, and starts an interaction. |
| `foundry model list`                            | Lists all available models for local use.                                        |
| `foundry model info <model>`           | Displays detailed information about a specific model.                            |
| `foundry model info <model> --license` | Displays the license information for a specific model.                           |
| `foundry model download <model>`       | Downloads a model to the local cache without running it.                         |
| `foundry model load <model>`           | Loads a model into the service.                                                  |
| `foundry model unload <model>`         | Unloads a model from the service.     |


## Service commands

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command**                     | **Description**                                                  |
| ------------------------------- | ---------------------------------------------------------------- |
| `foundry service --help`        | Displays all available service-related commands and their usage. |
| `foundry service start`         | Starts the Foundry Local service.                                |
| `foundry service stop`          | Stops the Foundry Local service.                                 |
| `foundry service restart`       | Restarts the Foundry Local service.                              |
| `foundry service status`        | Displays the current status of the Foundry Local service, including its dynamically assigned endpoint URL. Use this command to discover the current port. |
| `foundry service ps`            | Lists all models currently loaded in the Foundry Local service.  |
| `foundry service diag`          | Displays the logs of the Foundry Local service.                  |
| `foundry service set <options>` | Set configuration of the Foundry Local service.                  |

## Cache commands

The following table summarizes the commands related to managing the local cache where models are stored:

| **Command**                             | **Description**                                                |
| ------------------------------          | -------------------------------------------------------------- |
| `foundry cache --help`                  | Displays all available cache-related commands and their usage. |
| `foundry cache location`                | Displays the current cache directory.                          |
| `foundry cache list`                    | Lists all models stored in the local cache.                    |
| `foundry cache cd <path>`               | Changes the cache directory.                                   |
| `foundry cache remove <model>` | Deletes a model from the local cache.      |
