---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 01/23/2025
ms.topic: include
---

[!INCLUDE [Feature preview](../../../includes/feature-preview.md)]

Models deployed to Azure AI model inference in Azure AI Services support key-less authorization using Microsoft Entra ID. Key-less authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. It makes it a strong choice for organizations adopting secure and scalable identity management solutions.

This article explains how to configure Microsoft Entra ID for inference in Azure AI model inference.

## Understand roles in the context of resource in Azure

Microsoft Entra ID uses the idea of Role-based Access Control (RBAC) for authorization. Roles are central to managing access to your cloud resources. A role is essentially a collection of permissions that define what actions can be performed on specific Azure resources. By assigning roles to users, groups, service principals, or managed identities—collectively known as security principals—you control their access within your Azure environment to specific resources.

When you assign a role, you specify the security principal, the role definition, and the scope. This combination is known as a role assignment. Azure AI model inference is a capability of the Azure AI Services resources, and hence, roles assigned to that particular resource control the access for inference.

You identify two different types of access to the resources:

* **Administration access**: The actions that are related with the administration of the resource. They usually change the state of the resource and its configuration. In Azure, those operations are control-plane operations and can be executed using the Azure portal, the Azure CLI, or with infrastructure as code. Examples of includes creating a new model deployments, changing content filtering configurations, changing the version of the model served, or changing SKU of a deployment.

* **Developer access**: The actions that are related with the consumption of the resources. For example, invoking the chat completions API. However, the user can't change the state of the resource and its configuration.

In Azure, administration operations are always performed using Microsoft Entra ID. Roles like **Cognitive Services Contributor** allow you to perform those operations. On the other hand, developer operations can be performed using either access keys or/and Microsoft Entra ID. Roles like **Cognitive Services User** allow you to perform those operations.

> [!IMPORTANT]
> Having administration access to a resource doesn't necessarily grants developer access to it. Explicit access by granting roles is still required. It's analogous to how database servers work. Having administrator access to the database server doesn't mean you can read the data inside of a database.

Follow these steps to configure developer access to Azure AI model inference in the Azure AI Services resource.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you are using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI model inference](../../how-to/quickstart-github-models.md) if it's your case.

* An Azure AI services resource. For more information, see [Create an Azure AI Services resource](../../how-to/quickstart-create-resources.md).

* An account with `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Authorization/roleAssignments/delete` permissions, such as the **Administrator** role-based access control.

* To assign a role, you must specify three elements: 
  
  * Security principal: e.g. your user account.
  * Role definition: the *Cognitive Services User* role.
  * Scope: the Azure AI Services resource.

* If you want to create a custom role definition instead of using *Cognitive Services User* role, ensure the role has the following permissions:

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
