---
title: Enable role-based access control
titleSuffix: Azure AI Search
description: Enable or disable role-based access control for token authentication using Microsoft Entra ID on Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/22/2026
ms.update-cycle: 180-days
ms.custom:
  - dev-focus
ai-usage: ai-assisted
---

# Enable or disable role-based access control in Azure AI Search

This article explains how to enable role-based access control (RBAC) for data plane operations on Azure AI Search. With RBAC enabled, you can use Microsoft Entra ID authentication instead of API keys.

> [!IMPORTANT]
> When you create a search service, key-based authentication is the default, but it's not the most secure option. We recommend that you replace it with role-based access as described in this article.

Only [data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane) roles can be disabled. Roles for service administration (control plane) are built in and can't be enabled or disabled. 

If you observe key-related activity, such as Get Admin Keys, in the **Activity Log** on a roles-only search service, those actions are initiated on the control plane and don't affect your content or content-related operations.

## Prerequisites

+ A search service in any region, on any tier, including free.
+ **Owner**, **User Access Administrator**, or a custom role with [Microsoft.Authorization/roleAssignments/write](/azure/templates/microsoft.authorization/roleassignments) permissions to enable RBAC.
+ After enabling RBAC, you need data plane roles to access content: **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader**. See [Assign roles](search-security-rbac.md) for details.

## Enable role-based access for data plane operations

Configure your search service to recognize an **authorization** header on data requests that provide an OAuth2 access token.

When you enable roles for the data plane, the change is effective immediately, but wait a few seconds before assigning roles.

The default failure mode for unauthorized requests is `http401WithBearerChallenge`. Alternatively, you can set the failure mode to `http403`. 

### [**Azure portal**](#tab/config-svc-portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. Select **Settings** and then select **Keys** in the left pane.

   :::image type="content" source="media/search-security-rbac/search-security-enable-roles.png" lightbox="media/search-security-rbac/search-security-enable-roles.png" alt-text="Screenshot of the keys page with authentication options." border="true":::

1. Choose **Role-based control**. Only choose **Both** if you're currently using keys and need time to transition clients to role-based access control. 

   | Option | Description |
   |--------|--------------|
   | API Key (default) | Requires [API keys](search-security-api-keys.md) on the request header for authorization. |
   | Role-based access control (recommended) | Requires membership in a role assignment to complete the task. It also requires an authorization header on the request. |
   | Both | Requests are valid using either an API key or role-based access control, but if you provide both in the same request, the API key is used. |

1. As an administrator, if you choose a roles-only approach, [assign data plane roles](search-security-rbac.md) to your user account to restore full administrative access over data plane operations in the Azure portal. Roles include Search Service Contributor, Search Index Data Contributor, and Search Index Data Reader. You need the first two roles if you want equivalent access.

   Sometimes it can take five to ten minutes for role assignments to take effect. Until that happens, the following message appears in the Azure portal pages used for data plane operations.

   :::image type="content" source="media/search-security-rbac/you-do-not-have-access.png" alt-text="Screenshot of portal message indicating insufficient permissions.":::

### [**Azure CLI**](#tab/config-svc-cli)

Run this script to support roles only:

```azurecli
az search service update \
  --name YOUR-SEARCH-SERVICE-NAME \
  --resource-group YOUR-RESOURCE-GROUP-NAME \
  --disable-local-auth
```

Or, run this script to support both keys and roles:

```azurecli
az search service update \
  --name YOUR-SEARCH-SERVICE-NAME \
  --resource-group YOUR-RESOURCE-GROUP-NAME \
  --aad-auth-failure-mode http401WithBearerChallenge \
  --auth-options aadOrApiKey
```

**Reference:** [az search service update](/cli/azure/search/service#az-search-service-update)

For more information, see [Manage your Azure AI Search service with the Azure CLI](search-manage-azure-cli.md).

### [**Azure PowerShell**](#tab/config-svc-powershell)

Run this command to set the authentication type to roles only:

```azurepowershell
Set-AzSearchService `
  -Name YOUR-SEARCH-SERVICE-NAME `
  -ResourceGroupName YOUR-RESOURCE-GROUP-NAME `
  -DisableLocalAuth 1
```

Or, run this command to support both keys and roles:

```azurepowershell
Set-AzSearchService `
  -Name YOUR-SEARCH-SERVICE-NAME `
  -ResourceGroupName YOUR-RESOURCE-GROUP-NAME `
  -AuthOption AadOrApiKey
```

**Reference:** [Set-AzSearchService](/powershell/module/az.search/set-azsearchservice)

For more information, see [Manage your Azure AI Search service with PowerShell](search-manage-powershell.md).

### [**REST API**](#tab/config-svc-rest)

Use the Management REST API [Create or Update Service](/rest/api/searchmanagement/services/create-or-update) to configure your service for role-based access control.

All calls to the Management REST API are authenticated through Microsoft Entra ID. For help with setting up authenticated requests, see [Manage Azure AI Search using REST](search-manage-rest.md).

1. Get service settings so that you can review the current configuration.

   ```http
   GET https://management.azure.com/subscriptions/{{subscriptionId}}/providers/Microsoft.Search/searchServices?api-version=2025-05-01
   ```

1. Use PATCH to update service configuration. The following modifications enable both keys and role-based access. If you want a roles-only configuration, see [Disable API keys](#disable-api-key-authentication).

   Under "properties", set ["authOptions"](/rest/api/searchmanagement/services/create-or-update#dataplaneauthoptions) to "aadOrApiKey". The "disableLocalAuth" property must be false to set "authOptions".

   Optionally, set ["aadAuthFailureMode"](/rest/api/searchmanagement/services/create-or-update#aadauthfailuremode) to specify whether 401 is returned instead of 403 when authentication fails. Valid values are "http401WithBearerChallenge" or "http403".

    ```http
    PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2025-05-01
    {
        "properties": {
            "disableLocalAuth": false,
            "authOptions": {
                "aadOrApiKey": {
                    "aadAuthFailureMode": "http401WithBearerChallenge"
                }
            }
        }
    }
    ```

    A successful request returns `200 OK` with the updated service configuration.

    **Reference:** [Services - Create Or Update](/rest/api/searchmanagement/services/create-or-update)

---

## Disable role-based access control

It's possible to disable role-based access control for data plane operations and use key-based authentication instead. You might do this as part of a test workflow, for example to rule out permission issues.

To disable role-based access control in the Azure portal:

1. Sign in to the [Azure portal](https://portal.azure.com) and open the search service page.

1. Select **Settings** and then select **Keys** in the left pane.

1. Select **API Keys**.

## Disable API key authentication

[Key access](search-security-api-keys.md), or local authentication, can be disabled on your service if you're exclusively using the built-in roles and Microsoft Entra authentication. Disabling API keys causes the search service to refuse all data-related requests that pass an API key in the header.

Admin API keys can be disabled, but not deleted. Query API keys can be deleted.

Owner or Contributor permissions are required to disable security features.

### [**Azure portal**](#tab/disable-keys-portal)

1. In the Azure portal, navigate to your search service.

1. In the left-navigation pane, select **Keys**.

1. Select **Role-based access control**.

The change is effective immediately, but wait a few seconds before testing. Assuming you have permission to assign roles as a member of Owner, service administrator, or coadministrator, you can use portal features to test role-based access.

### [**Azure CLI**](#tab/disable-keys-cli)

To disable key-based authentication, set -disableLocalAuth to true. This is the same syntax as the "enable roles only" script presented in the previous section.

```azurecli
az search service update \
  --name YOUR-SEARCH-SERVICE-NAME \
  --resource-group YOUR-RESOURCE-GROUP-NAME \
  --disable-local-auth
```

To re-enable key authentication, set -disableLocalAuth to false. The search service resumes acceptance of API keys on the request automatically (assuming they're specified).

For more information, see [Manage your Azure AI Search service with the Azure CLI](search-manage-azure-cli.md).

### [**Azure PowerShell**](#tab/disable-keys-ps)

To disable key-based authentication, set DisableLocalAuth to true. This is the same syntax as the "enable roles only" script presented in the previous section.

```azurepowershell
Set-AzSearchService `
  -Name YOUR-SEARCH-SERVICE-NAME `
  -ResourceGroupName YOUR-RESOURCE-GROUP-NAME `
  -DisableLocalAuth 1
```

To re-enable key authentication, set DisableLocalAuth to false. The search service resumes acceptance of API keys on the request automatically (assuming they're specified).

For more information, see [Manage your Azure AI Search service with PowerShell](search-manage-powershell.md).

### [**REST API**](#tab/disable-keys-rest)

To disable key-based authentication, set "disableLocalAuth" to true.

1. Get service settings so that you can review the current configuration.

   ```http
   GET https://management.azure.com/subscriptions/{{subscriptionId}}/providers/Microsoft.Search/searchServices?api-version=2025-05-01
   ```

1. Use PATCH to update service configuration. The following modification sets "authOptions" to null.

    ```http
    PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2025-05-01
    {
        "properties": {
            "disableLocalAuth": true
        }
    }
    ```

    A successful request returns `200 OK` with the updated service configuration.

To re-enable key authentication, set "disableLocalAuth" to false. The search service resumes acceptance of API keys on the request automatically (assuming they're specified).

**Reference:** [Services - Create Or Update](/rest/api/searchmanagement/services/create-or-update)

---

## Next steps

> [!div class="nextstepaction"]
> [Set up roles for access to a search service](search-security-rbac.md)
