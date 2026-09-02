---
title: Include file
description: Include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 08/27/2026
ms.service: microsoft-foundry
ms.topic: include
ai-usage: ai-assisted
ms.custom:
  - include
  - classic-and-new
---

Run the following command:

```azurecli
az cognitiveservices account project delete \
--name my-foundry-resource \
--resource-group my-foundry-rg \
--project-name my-foundry-project
```

To verify deletion, run `az cognitiveservices account project show` with the same resource and project names. The command returns a resource-not-found error.

References: [az cognitiveservices account project delete](/cli/azure/cognitiveservices/account/project#az-cognitiveservices-account-project-delete).
