---
title: "Create a private tool catalog in Foundry Agent Service"
description: "Learn how to create a private tool catalog for developers in your organization."
author: aahill
ms.author: aahi
ms.date: 10/27/2025
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# Create a private tool catalog (preview)

Use this article to learn how to build a private [tool catalog](../concepts/tool-catalog.md) that is restricted to developers in your organization, using the [Azure API center](/azure/api-center/register-discover-mcp-server).

## Prerequisites 

* An [Azure API Center](/azure/api-center/set-up-api-center) 

    > [!NOTE]
    > The API Center name is your private tool catalog name shown in the registry filter so make sure you provide an informative name. 

* One or more remote MCP servers that you want to share with your organization that have been [Registered with API Center](/azure/api-center/tutorials/configure-environments-deployments)

## Configure authentication (optional)

1. Navigate to your API Center resource in the [Azure portal](https://portal.azure.com). If your remote MCP server requires authentication, select **Governance** > **authorization** in the left panel

     :::image type="content" source="../media/tool-catalog/api-center-resource.png" alt-text="A screenshot showing the API Center resource in the Azure portal." lightbox="../media/tool-catalog/api-center-resource.png":::

1. Select **add configuration** and set the security scheme to be `API Key`, `OAuth` or `HTTP` (bearer token authorization) and provide the required information.

    > [!NOTE] 
    > If you choose `API key` the key you provide in the Azure Key Vault won't be used in Microsoft Foundry to configure the MCP server. Developers need to provide the API key during configuration.   

1. Select the MCP server > **details** > **versions** > **Manage Access (preview)**

     :::image type="content" source="../media/tool-catalog/api-center-versions.png" alt-text="A screenshot showing the API Center resource versions in the Azure portal." lightbox="../media/tool-catalog/api-center-versions.png":::

1. Select the authorization configuration you created.

## Give access to your organization. 

For developers to see the MCP servers in the Foundry tool catalog, you need to give them at least the [Azure API Center Data Reader](/azure/role-based-access-control/built-in-roles/integration#azure-api-center-data-reader) or equivalent role. The private tool catalog will be available in the Foundry portal for developers with this role.