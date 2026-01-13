---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/26/2025
ms.topic: include
---

Microsoft Foundry Models support keyless authorization with Microsoft Entra ID. Keyless authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. Keyless authorization is a strong choice for organizations adopting secure and scalable identity management solutions.

This article explains how to configure Microsoft Entra ID for inference in Foundry Models.

## Understand roles in the context of resource in Azure

Microsoft Entra ID uses role-based access control (RBAC) for authorization. Roles are central to managing access to your cloud resources. A role is a collection of permissions that define what actions can be performed on specific Azure resources. By assigning roles to users, groups, service principals, or managed identities—collectively known as security principals—you control their access within your Azure environment to specific resources.

When you assign a role, you specify the security principal, the role definition, and the scope. This combination is known as a role assignment. Foundry Models is a capability of the Foundry Tools resources, and hence, roles assigned to that particular resource control the access for inference.

You identify two different types of access to the resources:

* **Administration access**: The actions related to the administration of the resource. They usually change the state of the resource and its configuration. In Azure, those operations are control-plane operations and can be executed using the Azure portal, the Azure CLI, or with infrastructure as code. Examples include creating new model deployments, changing content filtering configurations, changing the version of the model served, or changing SKU of a deployment.

* **Developer access**: The actions related to the consumption of the resources. For example, invoking the chat completions API. However, the user can't change the state of the resource and its configuration.

In Azure, Microsoft Entra ID always performs administration operations. Roles like **Cognitive Services Contributor** allow you to perform those operations. On the other hand, developer operations can be performed using either access keys or/and Microsoft Entra ID. Roles like **Cognitive Services User** allow you to perform those operations.

> [!IMPORTANT]
> Having administration access to a resource doesn't necessarily grant developer access to it. Explicit access by granting roles is still required. It's analogous to how database servers work. Having administrator access to the database server doesn't mean you can read the data inside of a database.


## Prerequisites

To complete this article, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)] 

* An account with `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Authorization/roleAssignments/delete` permissions, such as the **Administrator** role-based access control.

* To assign a role, you must specify three elements: 
  
  * Security principal: your user account.
  * Role definition: the *Cognitive Services User* role.
  * Scope: the Foundry Tools resource.

* If you want to create a custom role definition instead of using the *Cognitive Services User* role, ensure the role has the following permissions:

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
