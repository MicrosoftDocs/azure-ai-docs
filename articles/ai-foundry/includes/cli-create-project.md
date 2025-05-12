---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 12/27/2024
ms.custom: include
---

```azurecli
az cognitiveservices account create --resource-group {my_resource_group} --account-name {foundry_resource_name} --sku "S0" --kind "AIServices" --parameters allowProjectManagement=true

az cognitiveservices account project create --resource-group {my_resource_group} --name {my_project_name} --account-name {foundry_resource_name} 
```