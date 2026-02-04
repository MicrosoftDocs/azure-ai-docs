---
title: Configure keyless authentication with Microsoft Entra ID
titleSuffix: Microsoft Foundry
description: Learn how to configure keyless authentication with Microsoft Entra ID for Microsoft Foundry Models. Eliminate the need for API keys, enhance security with RBAC, and simplify compliance.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/22/2026
ms.custom: ignite-2024, github-universe-2024, dev-focus, time-to-complete=15
monikerRange: 'foundry-classic || foundry'
author: msakande
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-models-deployment
ms.reviewer: fasantia
reviewer: santiagxf
ai-usage: ai-assisted

#CustomerIntent: As a developer, I want to configure keyless authentication with Microsoft Entra ID for Microsoft Foundry Models so that I can secure my AI model deployments without relying on API keys and leverage role-based access control for better security and compliance.
---

# Configure keyless authentication with Microsoft Entra ID

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article explains how to configure keyless authentication with Microsoft Entra ID for Microsoft Foundry Models. Keyless authentication enhances security by eliminating the need for API keys, simplifies the user experience with role-based access control (RBAC), and reduces operational complexity while providing robust compliance support.

## Prerequisites

To complete this article, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Foundry (Foundry projects)](../../how-to/create-projects.md)

- The endpoint's URL.

- An account with `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Authorization/roleAssignments/delete` permissions, such as the **Administrator** role-based access control. See the next section on [Required Azure roles and permissions](#required-azure-roles-and-permissions) for more details.

### Required Azure roles and permissions

Microsoft Entra ID uses role-based access control (RBAC) to manage access to Azure resources. You need different roles, depending on whether you're setting up authentication (administrator) or using it to make API calls (developer).

#### For setting up authentication

* **Subscription owner or administrator**: An account with `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Authorization/roleAssignments/delete` permissions, such as the **Owner** or **User Access Administrator** role, required to assign the **Cognitive Services User** role to developers.

#### For making authenticated API calls

* **Cognitive Services User** role: Required for developers to authenticate and make inference API calls using Microsoft Entra ID. This role must be assigned at the scope of your Foundry resource.

#### Role assignment requirements

When assigning roles, specify these three elements:

* **Security principal**: Your user account, service principal, or security group (recommended for managing multiple users)
* **Role definition**: The **Cognitive Services User** role
* **Scope**: Your specific Foundry resource

> [!TIP]
> Azure role assignments can take up to 5 minutes to propagate. When using security groups, changes to group membership propagate immediately.

#### Custom role (optional)

If you prefer a custom role instead of **Cognitive Services User**, make sure it includes these permissions:

```json
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/MaaS/*"
      ]
    }
  ]
}
```

For more context on how roles work with Azure resources, see [Understand roles in the context of resource in Azure](#understand-roles-in-the-context-of-resource-in-azure).


::: zone pivot="ai-foundry-portal"
[!INCLUDE [portal](../../foundry-models/includes/configure-entra-id/portal.md)]
::: zone-end

::: zone pivot="programming-language-cli"
[!INCLUDE [cli](../../foundry-models/includes/configure-entra-id/cli.md)]
::: zone-end

::: zone pivot="programming-language-bicep"
[!INCLUDE [bicep](../../foundry-models/includes/configure-entra-id/bicep.md)]
::: zone-end

## Understand roles in the context of resource in Azure

Microsoft Entra ID uses role-based access control (RBAC) for authorization, which controls what actions users can perform on Azure resources. Roles are central to managing access to cloud resources. A role is a collection of permissions that define what actions can be performed on specific Azure resources. By assigning roles to users, groups, service principals, or managed identities—collectively known as security principals—you control their access within your Azure environment to specific resources.

When you assign a role, you specify the security principal, role definition, and scope. This combination is known as a role assignment. Foundry Models is a capability of the Foundry Tools resources, therefore, roles assigned to that particular resource control the access for inference.

There are two types of access to the resources:

* **Administration access**: Actions related to the administration of the resource. These actions usually change the resource state and its configuration. In Azure, these operations are control-plane operations that you can execute using the Azure portal, Azure CLI, or infrastructure as code. Examples include creating new model deployments, changing content filtering configurations, changing the version of the model served, or changing the SKU of a deployment.

* **Developer access**: Actions related to consuming the resources, such as invoking the chat completions API. However, the user can't change the resource state and its configuration.

In Azure, Microsoft Entra ID always performs administration operations. Roles like **Cognitive Services Contributor** allow you to perform those operations. Developer operations can be performed using either access keys or Microsoft Entra ID. Roles like **Cognitive Services User** allow you to perform those operations.

> [!IMPORTANT]
> Having administration access to a resource doesn't grant developer access to it. Explicit access by granting roles is still required. This is analogous to how database servers work. Having administrator access to the database server doesn't mean you can read the data inside of a database.

## Troubleshooting

[!INCLUDE [troubleshooting](../includes/configure-entra-id/troubleshooting.md)]

## Next step

- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
