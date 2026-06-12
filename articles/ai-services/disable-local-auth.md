---
title: Disable local authentication in Foundry Tools
titleSuffix: Foundry Tools
description: "This article describes how to disable local authentication in Foundry Tools for improved security."
author: PatrickFarley
manager: mcleans
ms.service: foundry-tools
ms.topic: how-to
ms.date: 05/31/2026
ms.author: pafarley
ms.custom: FY25Q1-Linter
ai-usage: ai-assisted
#customer intent: As a developer, I want to disable local authentication in Foundry Tools so that I can enforce Microsoft Entra authentication.
---

# Disable local authentication in Foundry Tools

Foundry Tools provides Microsoft Entra authentication support for all resources. This feature provides you with seamless integration when you require centralized control and management of identities and resource credentials. Organizations can disable local authentication methods and enforce Microsoft Entra authentication instead.

## How to disable local authentication

You can disable local authentication using the Azure policy **Foundry Tools resources should have key access disabled (disable local authentication)**. Set it at the subscription level or resource group level to enforce the policy for a group of services.

If you're creating an account using Bicep / ARM template, you can set the property `disableLocalAuth` to `true` to disable local authentication. For more information, see 
[Microsoft.CognitiveServices accounts - Bicep, ARM template, & Terraform](/azure/templates/microsoft.cognitiveservices/accounts)

You can also use PowerShell to disable local authentication for an individual resource. First sign in with the `Connect-AzAccount` command. Then use the `Set-AzCognitiveServicesAccount` cmdlet with the parameter `-DisableLocalAuth $true`, like the following example:

```powershell
Set-AzCognitiveServicesAccount -ResourceGroupName "my-resource-group" -Name "my-resource-name" -DisableLocalAuth $true
```

> [!NOTE]
> If you get an error that `-DisableLocalAuth` is not recognized, update your Az.CognitiveServices module:
> ```powershell
> Update-Module -Name Az.CognitiveServices
> ```

## Verify local authentication status

Disabling local authentication doesn't take effect immediately. The change is made on the control plane right away, but the shared gateway that enforces authentication can continue to accept previously valid keys until its cached configuration refreshes. Propagation typically completes within a few minutes, but it can take up to several hours depending on region, load, and gateway cache state. Plan for this delay when you rotate keys or audit access, and don't rely on an immediate cutoff for security-sensitive workflows.

To confirm that the change has taken effect, send a data-plane request with the old key and verify that the service returns an HTTP 401 response with an `Access denied due to invalid subscription key or wrong API endpoint` error before you consider local authentication fully disabled.

You can use PowerShell to determine whether the local authentication policy is currently enabled. First sign in with the `Connect-AzAccount` command. Then use the cmdlet **[Get-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccount)** to retrieve your resource, and check the property `DisableLocalAuth`. A value of `true` means local authentication is disabled.

## Re-enable local authentication

To enable local authentication, execute the PowerShell cmdlet **[Set-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/set-azcognitiveservicesaccount)** with the parameter `-DisableLocalAuth $false`. As with disabling, the change doesn't take effect immediately. Propagation typically completes within a few minutes, but it can take up to several hours for the gateway to accept local authentication requests again.

## Next step

- [Authenticate requests to Foundry Tools](./authentication.md)
