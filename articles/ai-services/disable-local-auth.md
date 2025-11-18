---
title: Disable local authentication in Foundry Tools
titleSuffix: Foundry Tools
description: "This article describes how to disable local authentication in Foundry Tools for improved security."
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.topic: how-to
ms.date: 10/02/2025
ms.author: pafarley
ms.custom: FY25Q1-Linter
#customer intent: As a developer, I want to disable local authentication in Foundry Tools so that I can enforce Microsoft Entra authentication.
---

# Disable local authentication in Foundry Tools

Foundry Tools provides Microsoft Entra authentication support for all resources. This feature provides you with seamless integration when you require centralized control and management of identities and resource credentials. Organizations can disable local authentication methods and enforce Microsoft Entra authentication instead.

## How to disable local authentication

You can disable local authentication using the Azure policy **Foundry Tools resources should have key access disabled (disable local authentication)**. Set it at the subscription level or resource group level to enforce the policy for a group of services.

If you're creating an account using Bicep / ARM template, you can set the property `disableLocalAuth` to `true` to disable local authentication. For more information, see 
[Microsoft.CognitiveServices accounts - Bicep, ARM template, & Terraform](/azure/templates/microsoft.cognitiveservices/accounts)

You can also use PowerShell with the Azure CLI to disable local authentication for an individual resource. First sign in with the `Connect-AzAccount` command. Then use the `Set-AzCognitiveServicesAccount` cmdlet with the parameter `-DisableLocalAuth $true`, like the following example:

```powershell
Set-AzCognitiveServicesAccount -ResourceGroupName "my-resource-group" -Name "my-resource-name" -DisableLocalAuth $true
```

## Verify local authentication status

Disabling local authentication doesn't take effect immediately. Allow a few minutes for the service to block future authentication requests.

You can use PowerShell to determine whether the local authentication policy is currently enabled. First sign in with the `Connect-AzAccount` command. Then use the cmdlet **[Get-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccount)** to retrieve your resource, and check the property `DisableLocalAuth`. A value of `true` means local authentication is disabled.

## Re-enable local authentication

To enable local authentication, execute the PowerShell cmdlet **[Set-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/set-azcognitiveservicesaccount)** with the parameter `-DisableLocalAuth $false`.  Allow a few minutes for the service to accept the change to allow local authentication requests.

## Next step

- [Authenticate requests to Foundry Tools](./authentication.md)
