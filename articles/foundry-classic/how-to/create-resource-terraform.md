---
title: "Use Terraform to create Microsoft Foundry (classic)"
description: "In this article, you create a Microsoft Foundry resource, a Microsoft Foundry project, using Terraform infrastructure as code templates. (classic)"
ms.topic: how-to
ms.date: 04/08/2026
ms.service: azure-ai-foundry
ms.reviewer: deeikele 
ms.author: sgilley
author: sdgilley
ms.custom: 
  - classic-and-new
  - devx-track-terraform
  - update-code2
  - dev-focus
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a Terraform user, I want to see how to configure Microsoft Foundry using Terraform, so I can automate my setup.
ROBOTS: NOINDEX, NOFOLLOW
---

# Use Terraform to manage Microsoft Foundry resources (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/create-resource-terraform.md)

Use Terraform to automate the creation of [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resources, projects, deployments, and connections.

You can use either the Terraform [AzAPI Provider](/azure/developer/terraform/overview-azapi-provider) or [AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) to manage Foundry resources. The AzAPI provider lets you access all Foundry control plane configurations including preview features. The AzureRM variant is limited to core management capabilities.

The following table shows which actions each provider supports:

|Action|AzAPI Provider|AzureRM Provider|
| --- | --- | --- |
| Create a resource group | ✅ | ✅ |
| Create a Foundry resource | ✅ | ✅ |
| Configure deployments | ✅ | ✅ |
| Configure projects | ✅ | ✅ |
| Configure a connection to knowledge and tools | ✅ | - |
| Configure a capability host (for advanced tool configurations like [Agent standard setup](../agents/concepts/capability-hosts.md)) | ✅ | - |

[!INCLUDE [About Terraform](~/azure-dev-docs-pr/articles/terraform/includes/abstract.md)]

[!INCLUDE [create-resource-terraform 1](../../foundry/includes/how-to-create-resource-terraform-1.md)]

## Verify your deployment

Run the following commands to verify deployed resources:

```terraform
terraform state list
terraform output
```

[!INCLUDE [create-resource-terraform 2](../../foundry/includes/how-to-create-resource-terraform-2.md)]
