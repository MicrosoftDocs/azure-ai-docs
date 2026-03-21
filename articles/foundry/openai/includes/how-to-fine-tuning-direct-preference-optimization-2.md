---
title: Include file
description: Include file
author: ssalgadodev
ms.reviewer: sgilley
ms.author: ssalgado
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Direct preference optimization - REST API

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs'
-H "api-key: $AZURE_OPENAI_API_KEY" 
-H 'Content-Type: application/json' 
-H 'task_type: chat' 
--data '{ "model": "gpt-4.1-mini-2025-04-14", "training_file": "file-d02c607351994d29987aece550ac81c0", "validation_file": "file-d02c607351994d29987aece550ac81c0", "prompt_loss_weight": 0.1, "suffix": "Pause_Resume", "method":{ "type":"dpo", "dpo":{ "beta":0.1, "l2_multiplier":0.1 }}}'

```

## Next steps

- Explore the fine-tuning capabilities in the [Azure OpenAI fine-tuning tutorial](../../../foundry-classic/openai/tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)
