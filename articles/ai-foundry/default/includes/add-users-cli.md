---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/04/2025
ms.custom: include
---

1. Get the project's resource ID:

     ```azurecli
   PROJECT_ID=$(az cognitiveservices account project show \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --project-name my-foundry-project \
       --query id -o tsv)
   ```

1. Assign the **Azure AI User** role to a team member:

   ```azurecli
   az role assignment create \
       --role "Azure AI User" \
       --assignee "user@contoso.com" \
       --scope $PROJECT_ID
   ```

   To add a security group instead of an individual user:

   ```azurecli
   az role assignment create \
       --role "Azure AI User" \
       --assignee-object-id "<security-group-object-id>" \
       --assignee-principal-type Group \
       --scope $PROJECT_ID
   ```

1. Verify the role assignment:

   ```azurecli
   az role assignment list \
       --scope $PROJECT_ID \
       --role "Azure AI User" \
       --output table
   ```

Reference: [az role assignment](/cli/azure/role/assignment)