---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/09/2025
ms.custom: include, build-2024, ignite-2024
---


You can create other projects on an existing `AIServices` resource.

Your first project (default project) plays a special role and has access to more features:

| Feature | Default project | Nondefault project |
|--|--|--|
| Model inference | ✓ | ✓ |
| Playgrounds | ✓ | ✓ |
| Agents | ✓ | ✓ |
| Evaluations | ✓ | ✓ |
| Connections | ✓ | ✓ |
| AI Foundry API that works with agents and across models | ✓ | ✓ |
| Project-level isolation of files and outputs | ✓ | ✓ |
| Azure OpenAI with Batch, StoredCompletions, Fine-tuning | ✓ |  |
| Backwards compatible with project-less {account}.cognitiveservices.com data plane API | ✓ |  |
| Content safety | ✓ |  |

To add a nondefault project to a resource:

# [Azure AI Foundry portal](#tab/ai-foundry)

1. In [Azure AI Foundry](https://ai.azure.com), select either the [!INCLUDE [fdp-project-name](fdp-project-name.md)] or its associated resource.
1. In the left pane, select **Management center**.
1. In the resource section, select  **Overview**.
1. Select **New project** and provide a name.

    :::image type="content" source="../media/how-to/projects/second-project.png" alt-text="Screenshot shows how to create a second project on an existing resource.":::


# [Python SDK](#tab/python)

```python
# add a project to the resource
```


# [Azure CLI](#tab/azurecli)

```azurecli
az ...
```


---