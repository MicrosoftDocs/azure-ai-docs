---
title: Include file
description: Create a managed DPO job with Python or REST.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/05/2026
ms.custom: include
ai-usage: ai-assisted
---

## Create a DPO job with code

Set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` for your resource. These examples use `gpt-4.1-mini-2025-04-14` and Global training; check [model support](../../fine-tuning/overview.md#supported-models) and [training types](../../fine-tuning/overview.md#training-types) before running them.

### [Python](#tab/python)

[!INCLUDE [DPO Python job workflow](fine-tuning-direct-preference-optimization-python.md)]

### [REST](#tab/rest)

[!INCLUDE [DPO REST job workflow](fine-tuning-direct-preference-optimization-rest.md)]

---

For DPO after SFT, set `model` to the supported fine-tuned model's identifier, not its deployment name.
