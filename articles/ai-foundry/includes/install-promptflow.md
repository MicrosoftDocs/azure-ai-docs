---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/29/2024
ms.custom: include
---

Use pip to install the prompt flow SDK into the virtual environment that you created.
```
pip install promptflow
pip install azure-identity
```

The prompt flow SDK takes a dependency on multiple packages, that you can choose to separately install if you don't want all of them:
 * ```promptflow-core```: contains the core prompt flow runtime used for executing LLM code
 * ```promptflow-tracing```: lightweight library used for emitting OpenTelemetry traces in standards
 * ```promptflow-devkit```: contains the prompt flow test bed and trace viewer tools for local development environments
 * ```openai```: client libraries for using the Azure OpenAI in Azure AI Foundry Models
 * ```python-dotenv```: used to set environment variables by reading them from ```.env``` files