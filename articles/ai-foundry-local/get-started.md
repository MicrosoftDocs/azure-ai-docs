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
  - 8GB+ RAM
  - Ample storage space (5GB+) for model caching
  - A modern CPU
- Administrator access to install software

## Install AI Foundry Local

1. Download AI Foundry Local from the Microsoft Store.
2. Follow the installation prompts to complete the setup.
3. Once installed, you can access AI Foundry Local through the command line using the `foundry` command.

## Using the CLI

The AI Foundry Local CLI provides several commands to manage models and the local inference service.

### View available commands

To see all available commands, use the help option:

```bash
foundry --help
```

### Discover available models

To list all available models that you can run locally:

```bash
foundry model list
```

### Get information about a specific model

To view details about a specific model:

```bash
foundry model info <model-name>
```

### Run your first model

To start a chat completion interaction with a model:

```bash
foundry model run deepseek-r1-1.5b-cpu
```

This command downloads the model if not already cached, loads it into the service, and starts an interactive chat session.

## Managing models

### Download a model

To download a model to your local cache without running it:

```bash
foundry model download <model-name>
```

### Load and unload models

Load a model into the service:

```bash
foundry model load <model-name>
```

Unload a model from the service:

```bash
foundry model unload <model-name>
```

## Managing the service

### Check service status

To check the status of the AI Foundry Local service:

```bash
foundry service status
```

### Start, stop, and restart the service

Note that the service will start automatically when attempting to run a model. To manually start, stop, or restart the service:

```bash
foundry service start
foundry service stop 
foundry service restart
```

### List loaded models

To see which models are currently loaded in the service:

```bash
foundry service list
```

## Managing the cache

### View cache location

To see where models are stored locally:

```bash
foundry cache pwd
```

### List cached models

To list all models stored in your local cache:

```bash
foundry cache list
```

### Remove a model from cache

To delete a model from your local cache:

```bash
foundry cache remove <model-name>
```

### Change cache directory

To change the directory where models are stored:

```bash
foundry cache cd <path>
```

## Next steps

- Explore the [AI Foundry Local documentation](index.yml) for more advanced scenarios
- Learn how to [integrate AI Foundry Local with your applications](integration-guide.md)
- See [sample projects and code examples](samples.md) that use AI Foundry Local
```
