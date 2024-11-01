---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 10/31/2024
ms.custom: include
---

Use pip to install the support for notebooks in the virtual environment that you created.

```bash
pip install ipython ipykernel
```

Now install the Azure AI SDK packages you need to use the Azure OpenAI service.

```bash
pip install azure_ai_projects azure_ai_inference azure-identity --force-reinstall
```

If you want to run evaluations, install the azure-ai-evaluation package with the remote extra:

```
pip install azure-ai-evaluation[remote]
```