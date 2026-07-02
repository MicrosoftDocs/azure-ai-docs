---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/21/2026
ms.custom: include
ai-usage: ai-assisted
---

> [!NOTE]
> These steps require Azure CLI and **Contributor** or **Owner** role on the resource group. Run `az login` to sign in before you start. For supported regions, see [Region support](../reference/region-support.md).

1. Create a resource group or use an existing one. For example, create `my-foundry-rg` in `eastus`:

   ```azurecli
   az group create --name my-foundry-rg --location eastus
   ```

1. Create the Foundry resource with project management enabled. For example, create `my-foundry-resource` in the `my-foundry-rg` resource group:

   ```azurecli
   az cognitiveservices account create \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --kind AIServices \
       --sku S0 \
       --location eastus \
       --custom-domain my-foundry-resource \
       --allow-project-management
   ```

   Set the `--allow-project-management` flag to enable project management. You can't change this flag after resource creation. The `--custom-domain` value must be globally unique - if `my-foundry-resource` is already taken, choose a different name.

1. Create a project. For example, create `my-foundry-project` in the `my-foundry-resource`:

   ```azurecli
   az cognitiveservices account project create \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --project-name my-foundry-project \
       --location eastus
   ```

1. Verify that the resource is provisioned:

   ```azurecli
   az cognitiveservices account show \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --query properties.provisioningState --output tsv
   ```

   The output should show `Succeeded`. If the output shows a different state, check your permissions, region availability, and resource quotas. For more help, see [Create a multi-service resource](../../ai-services/multi-service-resource.md).

1. Verify the project was created:

   ```azurecli
   az cognitiveservices account project show \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --project-name my-foundry-project \
       --query properties.provisioningState --output tsv
   ```

   The output should show `Succeeded`.
