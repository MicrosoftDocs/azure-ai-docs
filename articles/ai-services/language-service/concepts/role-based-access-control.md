---
title: Role-based access control for Azure Language service
titleSuffix: Foundry Tools
description: Learn how to use Azure role based access control (RBAC) for managing individual access to Azure resources.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
---
# Language role-based access control

Azure Language in Foundry Tools supports Azure role-based access control (Azure RBAC), an authorization system for managing individual access to Azure resources. Using Azure RBAC, you assign different team members different levels of permissions for your projects authoring resources. For more information, *see* the [Azure RBAC documentation](/azure/role-based-access-control/).

<a name='enable-azure-active-directory-authentication'></a>

## Enable Microsoft Entra authentication 

To use Azure RBAC, you must enable Microsoft Entra authentication. You can [create a new resource with a custom subdomain](../../authentication.md#create-a-resource-with-a-custom-subdomain) or [create a custom subdomain for your existing resource](../../cognitive-services-custom-subdomains.md#how-does-this-impact-existing-resources).

## Add role assignment to Azure resource

Azure RBAC can be assigned to an Azure resource. To do so, you can add a role assignment.
1. In the [Azure portal](https://portal.azure.com/), select **All services**. 
1. Select **Foundry Tools**, and navigate to your specific Azure resource. 
   > [!NOTE]
   > You can also set up Azure RBAC for whole resource groups, subscriptions, or management groups. Complete your configuration by selecting the desired scope level and then navigating to the desired item. For example, selecting **Resource groups** and then navigating to a specific resource group.

1. Select **Access control (IAM)** on the left pane.
1. Select **Add**, then select **Add role assignment**.
1. On the **Role** tab on the next screen, select a role you want to add.
1. On the **Members** tab, select a user, group, service principal, or managed identity.
1. On the **Review + assign** tab, select **Review + assign** to assign the role.

Within a few minutes, the target is assigned to the selected role at the selected scope. For help with these steps, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

## Language role types

Use the following table to determine access needs for your Language projects.

These custom roles only apply to Language resources. 
> [!NOTE]
> * All prebuilt capabilities are accessible to all roles.
> * *Owner* and *Contributor* roles take priority over the custom language roles.
> * Microsoft Entra ID is only used with custom Language roles.
> * If you're assigned as a *Contributor* on Azure, your role is shown as *Owner* in Language studio portal.


### Cognitive Services Language Reader

A user that should only be validating and reviewing Azure Language apps, typically a tester to ensure the application is performing well before deploying the project. They might want to review the application's assets to notify the app developers of any changes that need to be made, but don't have direct access to make them. Readers have access to view the evaluation results.


:::row:::
    :::column span="":::
        **Capabilities**
    :::column-end:::
    :::column span="":::
        **API Access**
    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::
        * Read
        * Test
    :::column-end:::
    :::column span="":::
      All GET APIs under: 
        * [Language authoring conversational language understanding APIs](/rest/api/language/2023-04-01/conversational-analysis-authoring)
        * [Language authoring text analysis APIs](/rest/api/language/2023-04-01/text-analysis-authoring)
        * [Question answering projects](/rest/api/questionanswering/question-answering-projects)
      Only `TriggerExportProjectJob` POST operation under: 
         * [Language authoring conversational language understanding export API](/rest/api/language/2023-04-01/text-analysis-authoring/export)
         * [Language authoring text analysis export API](/rest/api/language/2023-04-01/text-analysis-authoring/export)
      Only Export POST operation under: 
         * [Question Answering Projects](/rest/api/questionanswering/question-answering-projects/export)
      All the Batch Testing Web APIs
         *[Language Runtime `CLU` APIs](/rest/api/language)
         *[Language Runtime Text Analysis APIs](https://go.microsoft.com/fwlink/?linkid=2239169)
    :::column-end:::
:::row-end:::

### Cognitive Services Language Writer

A user responsible for building and modifying an application as a collaborator in a larger team. The collaborator can modify Azure Language apps in any way, train those changes, and validate/test those changes in the portal. However, this user shouldn't have access to deploying this application to the runtime, as they might accidentally reflect their changes in production. They also shouldn't be able to delete the application or alter its prediction resources and endpoint settings (assigning or unassigning prediction resources, making the endpoint public). This restriction prevents the role from altering an application currently being used in production. They might also create new applications under this resource, but with the restrictions mentioned.

:::row:::
    :::column span="":::
        **Capabilities**
    :::column-end:::
    :::column span="":::
        **API Access**
    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::
      * All functionalities under Cognitive Services Language Reader.
      * Ability to: 
          * Train
          * Write
    :::column-end:::
    :::column span="":::
      * All APIs under Language reader
      * All POST, PUT, and PATCH APIs under:
         * [Language conversational language understanding APIs](/rest/api/language/2023-04-01/conversational-analysis-authoring)
         * [Language text analysis APIs](/rest/api/language/2023-04-01/text-analysis-authoring)
         * [question answering projects](/rest/api/questionanswering/question-answering-projects)
          Except for
          * Delete deployment
          * Delete trained model
          * Delete Project
          * Deploy Model
    :::column-end:::
:::row-end:::

### Cognitive Services Language Owner

> [!NOTE]
> If you're assigned as an Owner and Language Owner,* you considered a *Cognitive Services Language Owner* by Azure Language studio portal.


These users are the gatekeepers for Azure Language applications in production environments. They should have full access to any of the underlying functions and thus can view everything in the application and have direct access to edit any changes for both authoring and runtime environments

:::row:::
    :::column span="":::
        **Functionality**
    :::column-end:::
    :::column span="":::
        **API Access**
    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::
      * All functionalities under Cognitive Services Language Writer
      * Deploy
      * Delete
    :::column-end:::
    :::column span="":::
      All APIs available under:
        * [Language authoring conversational language understanding APIs](/rest/api/language/2023-04-01/conversational-analysis-authoring)
        * [Language authoring text analysis APIs](/rest/api/language/2023-04-01/text-analysis-authoring)
        * [question answering projects](/rest/api/questionanswering/question-answering-projects)
         
    :::column-end:::
:::row-end:::
