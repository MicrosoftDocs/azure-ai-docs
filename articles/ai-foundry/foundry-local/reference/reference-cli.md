---
title: Foundry Local CLI Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local command-line interface.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: conceptual
ms.date: 02/12/2025
ms.author: samkemp
author: samuel100
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

| **Command**                                     | **Description**                                                                  |
| --------------------------------------          | -------------------------------------------------------------------------------- |
| `foundry model --help`                          | Displays all available model-related commands and their usage.                   |
| `foundry model run <aliasOrModelId>`            | Runs a specified model, downloading it if not cached, and starts an interaction. |
| `foundry model list`                            | Lists all available models for local use.                                        |
| `foundry model info <aliasOrModelId>`           | Displays detailed information about a specific model.                            |
| `foundry model info <aliasOrModelId> --license` | Displays the license information for a specific model.                           |
| `foundry model download <aliasOrModelId>`       | Downloads a model to the local cache without running it.                         |
| `foundry model load <aliasOrModelId>`           | Loads a model into the service.                                                  |
| `foundry model unload <aliasOrModelId>`         | Unloads a model from the service.                                                |

## Service commands

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command**                     | **Description**                                                  |
| ------------------------------- | ---------------------------------------------------------------- |
| `foundry service --help`        | Displays all available service-related commands and their usage. |
| `foundry service start`         | Starts the Foundry Local service.                                |
| `foundry service stop`          | Stops the Foundry Local service.                                 |
| `foundry service restart`       | Restarts the Foundry Local service.                              |
| `foundry service status`        | Displays the current status of the Foundry Local service.        |
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
| `foundry cache remove <aliasOrModelId>` | Deletes a model from the local cache.                          |
| `foundry cache cd <path>`               | Changes the cache directory.                                   |
