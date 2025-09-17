---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 09/09/2025
ms.custom: include
---

To use LLMs deployed in Azure AI Foundry portal, you need the endpoint and credentials to connect to it. Follow these steps to get the information you need from the model you want to use:

1. Sign in to the [Azure AI Foundry portal](https://aka.ms/nextgen-canary/?cid=learnDocs).

1. Open the project where the model is deployed, if it isn't already open.

1. Copy the endpoint URL and the key.

In this scenario, set the endpoint URL and key as environment variables. (If the endpoint you copied includes additional text after `/models`, remove it so the URL ends at `/models` as shown below.)

```bash
export AZURE_INFERENCE_ENDPOINT="https://<resource>.services.ai.azure.com/models"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```
