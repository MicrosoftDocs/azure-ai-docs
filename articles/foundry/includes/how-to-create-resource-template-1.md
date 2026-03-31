---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/31/2026
ms.custom: include
---

## Review the Bicep file (optional)

Optionally, review the Bicep template to understand the resource definitions. 

You can find the Bicep file used in this article at [https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/00-basic](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/00-basic).

This template creates the following resources:

- [microsoft.cognitiveservices/accounts](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep)
- [microsoft.cognitiveservices/accounts/projects](/azure/templates/microsoft.cognitiveservices/accounts/projects?pivots=deployment-language-bicep)

## Review deployed resources

Use the [Foundry portal](https://ai.azure.com/?cid=learnDocs) to view the created resources. You can also use Azure CLI or Azure PowerShell to list the resources.

# [Azure CLI](#tab/cli)

```azurecli
az resource list --resource-group exampleRG
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Get-AzResource -ResourceGroupName exampleRG
```

---

## Clean up resources

If you plan to continue working with subsequent quickstarts and tutorials, you can keep the resources you created in this quickstart. If you want to remove the resources, use the following command.

# [Azure CLI](#tab/cli)

```azurecli
az group delete --name exampleRG
```

Reference: [az group delete](/cli/azure/group#az-group-delete)

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Remove-AzResourceGroup -Name exampleRG
```

Reference: [Remove-AzResourceGroup](/powershell/module/az.resources/remove-azresourcegroup)

---

## Related content

- [Get started with the SDK](../quickstarts/get-started-code.md)
- [Configure network isolation with private endpoints](../how-to/configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Security configurations samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) — See example Bicep template configurations for enterprise security configurations, including network isolation, customer-managed key encryption, advanced identity options, and Agents standard setup.
