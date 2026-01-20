---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-foundry-foundry
ms.topic: include
ms.date: 01/19/2026
ms.custom: include
---

1. Create a resource group or use an existing one. For example, create `my-foundry-rg` in `eastus`:

   ```azurecli
   az group create --name my-foundry-rg --location eastus
   ```

1. Create the Foundry resource. For example, create `my-foundry-resource` in the `my-foundry-rg` resource group:

   ```azurecli
   az cognitiveservices account create \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --kind AIServices \
       --sku s0 \
       --location eastus \
      --allow-project-management
   ```

   The `--allow-project-management` flag enables project creation within this resource.

1. Create a custom subdomain for the resource. The custom domain name must be globally unique. If `my-foundry-resource` is taken, try a more unique name.

   ```azurecli
   az cognitiveservices account update \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --custom-domain my-foundry-resource
   ```

1. Create the project. For example, create `my-foundry-project` in the `my-foundry-resource`:

   ```azurecli
   az cognitiveservices account project create \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --project-name my-foundry-project \
       --location eastus
   ```

1. Verify the project was created:

   ```azurecli
   az cognitiveservices account project show \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --project-name my-foundry-project
   ```

   The output displays the project properties, including its resource ID.

Reference: [az cognitiveservices account](/cli/azure/cognitiveservices/account)
