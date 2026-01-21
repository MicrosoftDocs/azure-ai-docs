---
title: Configure key-less authentication with Microsoft Entra ID
titleSuffix: Microsoft Foundry
description: Learn how to configure key-less authorization to use Microsoft Foundry Models with Microsoft Entra ID and enhance security.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/26/2025
ms.custom: ignite-2024, github-universe-2024, dev-focus
author: msakande
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-models-deployment
ms.reviewer: fasantia
reviewer: santiagxf
ai-usage: ai-assisted

#CustomerIntent: As a developer, I want to configure keyless authentication with Microsoft Entra ID for Microsoft Foundry Models so that I can secure my AI model deployments without relying on API keys and leverage role-based access control for better security and compliance.
---

# Configure key-less authentication with Microsoft Entra ID

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

This article explains how to configure Microsoft Entra ID for inference in Foundry Models. Use of keyless authorization with Microsoft Entra ID enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. Keyless authorization is a strong choice for organizations adopting secure and scalable identity management solutions.


## Prerequisites

To complete this article, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)] 

### Required Azure roles and permissions

Microsoft Entra ID uses role-based access control (RBAC) to manage access to Azure resources. You need different roles depending on whether you're setting up authentication (administrator) or using it to make API calls (developer).

#### For setting up authentication

* **Subscription owner or administrator**: An account with `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Authorization/roleAssignments/delete` permissions, such as the **Owner** or **User Access Administrator** role. Required to assign the **Cognitive Services User** role to developers.

#### For making authenticated API calls

* **Cognitive Services User** role: Required for developers to authenticate and make inference API calls using Microsoft Entra ID. This role must be assigned at the scope of your Foundry resource (formerly known as Azure AI Services resource).

#### Role assignment requirements

When assigning roles, specify these three elements:

* **Security principal**: Your user account, service principal, or security group (recommended for managing multiple users)
* **Role definition**: The **Cognitive Services User** role
* **Scope**: Your specific Foundry resource

> [!TIP]
> Azure role assignments can take up to five minutes to propagate. When using security groups, changes to group membership propagate immediately.

#### Custom role (optional)

If you prefer a custom role instead of **Cognitive Services User**, ensure it includes these permissions:

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

Microsoft Entra ID uses role-based access control (RBAC) for authorization. Roles are central to managing access to your cloud resources. A role is a collection of permissions that define what actions can be performed on specific Azure resources. By assigning roles to users, groups, service principals, or managed identities—collectively known as security principals—you control their access within your Azure environment to specific resources.

When you assign a role, you specify the security principal, the role definition, and the scope. This combination is known as a role assignment. Foundry Models is a capability of the Foundry Tools resources, and hence, roles assigned to that particular resource control the access for inference.

You identify two different types of access to the resources:

* **Administration access**: The actions related to the administration of the resource. They usually change the state of the resource and its configuration. In Azure, those operations are control-plane operations and can be executed using the Azure portal, the Azure CLI, or with infrastructure as code. Examples include creating new model deployments, changing content filtering configurations, changing the version of the model served, or changing SKU of a deployment.

* **Developer access**: The actions related to the consumption of the resources. For example, invoking the chat completions API. However, the user can't change the state of the resource and its configuration.

In Azure, Microsoft Entra ID always performs administration operations. Roles like **Cognitive Services Contributor** allow you to perform those operations. On the other hand, developer operations can be performed using either access keys or/and Microsoft Entra ID. Roles like **Cognitive Services User** allow you to perform those operations.

> [!IMPORTANT]
> Having administration access to a resource doesn't necessarily grant developer access to it. Explicit access by granting roles is still required. It's analogous to how database servers work. Having administrator access to the database server doesn't mean you can read the data inside of a database.

## Troubleshooting

[!INCLUDE [troubleshooting](../includes/configure-entra-id/troubleshooting.md)]

## Next step

* [Develop applications using Microsoft Foundry Models](../../model-inference/supported-languages.md)
