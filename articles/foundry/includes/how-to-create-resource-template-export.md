---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/15/2026
ms.custom: include
---

## Export an existing resource to a Bicep file

If you already configured a Foundry resource in the Azure portal, you can export that configuration as a Bicep file. The exported file captures your current resource settings, including network rules, identity configuration, and project associations. Use it as a starting point for repeatable deployments across environments.

1. In the [Azure portal](https://portal.azure.com), go to your Foundry resource.
1. In the left menu under **Automation**, select **Export template**.
1. Select the **Bicep** tab to view the generated Bicep code.
1. Select **Download** to save the file locally, or **Copy** to copy the code to your clipboard.

> [!NOTE]
> The export might complete with warnings if some resource types don't support full export. Review the output and fill in any missing properties manually.

### Customize the exported template

The exported Bicep file contains hardcoded values specific to your subscription and resource group. Before you reuse the template, review and update the following:

- Replace hardcoded subscription IDs, resource group names, and resource IDs with [Bicep parameters](/azure/azure-resource-manager/bicep/parameters).
- Remove any properties you don't need or that reference resources outside the deployment scope.
- Add or adjust security configurations to match your organization's requirements.

For production-ready Bicep templates with enterprise security configurations already built in, see the [infrastructure-setup-bicep](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) folder in the Foundry samples repository.
