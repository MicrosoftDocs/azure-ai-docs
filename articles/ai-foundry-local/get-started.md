---
title: Get started with AI Foundry Local
titleSuffix: AI Foundry Local
description: Learn how to install, configure, and run your first AI model with AI Foundry Local
manager: scottpolly
keywords: Azure AI services, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.date: 02/20/2025
ms.reviewer: samkemp
ms.author: samkemp
author: samuel100
ms.custom: build-2025
#customer intent: As a developer, I want to get started with AI Foundry Local so that I can run AI models locally.
---

# Get started with AI Foundry Local

This article shows you how to get started with AI Foundry Local to run AI models on your device. Follow these steps to install the tool, discover available models, and run your first local AI model.

## Prerequisites

- A PC with sufficient specifications to run AI models locally
  - Windows 10 or later
  - Greater than 8GB RAM
  - Greater than 3GB of free disk space for model caching
- Administrator access to install software

## Quickstart in 2-steps

Follow these steps to get started with AI Foundry Local:

1. **Install Foundry Local**
    1. Download AI Foundry Local from the Microsoft Store.
    2. Follow the installation prompts to complete the setup.
    3. Once installed, you can access AI Foundry Local through the command line using the `foundry` command.
1. **Run your first model**
    1. Open a command prompt or terminal window.
    2. Run the DeepSeek-R1 model using the following command:
        ```bash
        foundry model run deepseek-r1-1.5b-cpu
        ```

> [!TIP]
> The `foundry model run <model>` command will automatically download the model if it is not already cached on your local machine, and then start an interactive chat session with the model.

## Explore Foundry Local CLI commands

To see all available commands, use the help option:

```bash
foundry --help
```

The foundry CLI is structured into several categories:

- **Model**: Commands related to managing and running models.
- **Service**: Commands for managing the AI Foundry Local service.
- **Cache**: Commands for managing the local cache where models are stored.


### Managing models

The following table summarizes the commands related to managing and running models:

| **Command**                          | **Description**                                                                 |
|--------------------------------------|---------------------------------------------------------------------------------|
| `foundry model --help`               | Displays all available model-related commands and their usage.                 |
| `foundry model run <model>`     | Runs a specified model, downloading it if not cached, and starts an interaction.|
| `foundry model list`                 | Lists all available models for local use.                                      |
| `foundry model info <model>`    | Displays detailed information about a specific model.                          |
| `foundry model download <model>`| Downloads a model to the local cache without running it.                       |
| `foundry model load <model>`    | Loads a model into the service.                                                |
| `foundry model unload <model>`  | Unloads a model from the service.                                              |


## Managing the service

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command**                          | **Description**                                                                 |
|--------------------------------------|---------------------------------------------------------------------------------|
| `foundry service --help`              | Displays all available service-related commands and their usage.               |
| `foundry service start`               | Starts the AI Foundry Local service.                                           |
| `foundry service stop`                | Stops the AI Foundry Local service.                                            |
| `foundry service restart`             | Restarts the AI Foundry Local service.                                         |
| `foundry service status`              | Displays the current status of the AI Foundry Local service.                   |
| `foundry service ps`                | Lists all models currently loaded in the AI Foundry Local service.             |
| `foundry service logs`                | Displays the logs of the AI Foundry Local service.                             |
| `foundry service set`              | Set configuration of the AI Foundry Local service.            |



## Managing the cache

The following table summarizes the commands related to managing the local cache where models are stored:

| **Command**                          | **Description**                                                                 |
|--------------------------------------|---------------------------------------------------------------------------------|
| `foundry cache --help`                | Displays all available cache-related commands and their usage.                 |
| `foundry cache pwd`                  | Displays the current cache directory.                                          |
| `foundry cache list`                 | Lists all models stored in the local cache.                                   |
| `foundry cache remove <model>`    | Deletes a model from the local cache.                                          |
| `foundry cache cd <path>`         | Changes the cache directory.                                 |    

## Next steps

- [Learn how to integrate AI Foundry Local with your applications](how-to/integrate-with-inference-sdks.md)
- [Explore the AI Foundry Local documentation](index.yml)

