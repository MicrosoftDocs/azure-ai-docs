---
title: Role-based access control for Azure OpenAI
description: Learn how to use Azure RBAC for managing individual access to Azure OpenAI resources.
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 1/31/2026
ms.author: mbullwin
recommendations: false
---

# Role-based access control for Azure OpenAI in Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI supports Azure role-based access control (Azure RBAC), an authorization system for managing individual access to Azure resources. Using Azure RBAC, you assign different team members different levels of permissions based on their needs for a given project. For more information, see the [Azure RBAC documentation](/azure/role-based-access-control/).

## Add role assignment to an Azure OpenAI resource

Azure RBAC can be assigned to an Azure OpenAI resource. To grant access to an Azure resource, you add a role assignment.
1. In the [Azure portal](https://portal.azure.com/), search for **Azure OpenAI**. 
1. Select **Azure OpenAI**, and navigate to your specific resource.
   > [!NOTE]
   > You can also set up Azure RBAC for whole resource groups, subscriptions, or management groups. Do this by selecting the desired scope level and then navigating to the desired item. For example, selecting **Resource groups** and then navigating to a specific resource group.

1. Select **Access control (IAM)** on the left pane.
1. Select **Add**, then select **Add role assignment**.
1. On the **Role** tab on the next screen, select a role you want to add.
1. On the **Members** tab, select a user, group, service principal, or managed identity.
1. On the **Review + assign** tab, select **Review + assign** to assign the role.

Within a few minutes, the target will be assigned the selected role at the selected scope. For help with these steps, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

## Azure OpenAI roles

- **Cognitive Services OpenAI User**
- **Cognitive Services OpenAI Contributor**
- **Cognitive Services Contributor**
- **Cognitive Services Usages Reader**

> [!NOTE]
> Subscription level *Owner* and *Contributor* roles are inherited and take priority over the custom Azure OpenAI roles applied at the Resource Group level.

This section covers common tasks that different accounts and combinations of accounts are able to perform for Azure OpenAI resources. To view the full list of available **Actions** and **DataActions**, an individual role is granted from your Azure OpenAI resource go **Access control (IAM)** > **Roles** > Under the **Details** column for the role you're interested in select **View**. By default the **Actions** radial button is selected. You need to examine both **Actions** and **DataActions** to understand the full scope of capabilities assigned to a role.

### Cognitive Services OpenAI User

If a user were granted role-based access to only this role for an Azure OpenAI resource, they would be able to perform the following common tasks:

✅ View the resource in [Azure portal](https://portal.azure.com) <br>
✅ View the resource endpoint under **Keys and Endpoint** <br>
✅ Ability to view the resource and associated model deployments in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). <br>
✅ Ability to view what models are available for deployment in [Foundry portal](https://ai.azure.com/?cid=learnDocs). <br>
✅ Use the Chat, Completions, and DALL-E (preview) playground experiences to generate text and images with any models that have already been deployed to this Azure OpenAI resource. <br>
✅ Make inference API calls with Microsoft Entra ID.

A user with only this role assigned would be unable to:

❌ Create new Azure OpenAI resources <br>
❌ View/Copy/Regenerate keys under **Keys and Endpoint** <br>
❌ Create new model deployments or edit existing model deployments <br>
❌ Create/deploy custom fine-tuned models <br>
❌ Upload datasets for fine-tuning <br>
❌ View, query, filter Stored completions data <br>
❌ Access quota <br>
❌ Create customized guardrails 

### Cognitive Services OpenAI Contributor

This role has all the permissions of Cognitive Services OpenAI User and is also able to perform additional tasks like:

✅ Create custom fine-tuned models <br>
✅ Upload datasets for fine-tuning <br>
✅ View, query, filter Stored completions data <br>
✅ Create new model deployments or edit existing model deployments **[Added Fall 2023]** <br>
✅ Grant access to the Assistants API <br> 
✅ Add data sources to Azure OpenAI On Your Data.

A user with only this role assigned would be unable to:

❌ Create new Azure OpenAI resources <br>
❌ View/Copy/Regenerate keys under **Keys and Endpoint** <br>
❌ Access quota <br>
❌ Create customized guardrails <br>

### Cognitive Services Contributor

This role is typically granted access at the resource group level for a user in conjunction with additional roles. By itself this role would allow a user to perform the following tasks.

✅ Create new Azure OpenAI resources within the assigned resource group. <br>
✅ View resources in the assigned resource group in the [Azure portal](https://portal.azure.com). <br>
✅ View the resource endpoint under **Keys and Endpoint** <br>
✅ View/Copy/Regenerate keys under **Keys and Endpoint** <br>
✅ Ability to view what models are available for deployment in [Foundry portal](https://ai.azure.com/?cid=learnDocs) <br>
✅ Use the Chat, Completions, and DALL-E (preview) playground experiences to generate text and images with any models that have already been deployed to this Azure OpenAI resource <br>
✅ Create customized guardrails <br>
✅ Add data sources to Azure OpenAI On Your Data. <br>
✅ Create new model deployments or edit existing model deployments (via API) <br>
✅ Create custom fine-tuned models **[Added Fall 2023]**<br>
✅ Upload datasets for fine-tuning **[Added Fall 2023]**<br>
✅ Create new model deployments or edit existing model deployments (via Foundry) **[Added Fall 2023]**<br>
✅ View, query, filter Stored completions data <br>

A user with only this role assigned would be unable to:

❌ Access quota <br>
❌ Make inference API calls with Microsoft Entra ID.

### Cognitive Services Usages Reader

Viewing quota requires the **Cognitive Services Usages Reader** role. This role provides the minimal access necessary to view quota usage across an Azure subscription.

This role can be found in the Azure portal under **Subscriptions** > ***Access control (IAM)** > **Add role assignment** > search for **Cognitive Services Usages Reader**. The role must be applied at the subscription level, it does not exist at the resource level.

If you don't wish to use this role, the subscription **Reader** role provides equivalent access, but it also grants read access beyond the scope of what is needed for viewing quota. Model deployment via the [Foundry portal](https://ai.azure.com/?cid=learnDocs) is also partially dependent on the presence of this role.

This role provides little value by itself and is instead typically assigned in combination with one or more of the previously described roles.

#### Cognitive Services Usages Reader + Cognitive Services OpenAI User

All the capabilities of Cognitive Services OpenAI User plus the ability to:

✅ View quota allocations in [Foundry portal](https://ai.azure.com/?cid=learnDocs)

#### Cognitive Services Usages Reader + Cognitive Services OpenAI Contributor

All the capabilities of Cognitive Services OpenAI Contributor plus the ability to:

✅ View quota allocations in [Foundry portal](https://ai.azure.com/?cid=learnDocs)

#### Cognitive Services Usages Reader + Cognitive Services Contributor

All the capabilities of Cognitive Services Contributor plus the ability to:

✅ View & edit quota allocations in [Foundry portal](https://ai.azure.com/?cid=learnDocs) <br>
✅ Create new model deployments or edit existing model deployments (via Foundry) <br>

## Summary

| Permissions | Cognitive Services OpenAI User | Cognitive Services OpenAI Contributor |Cognitive Services Contributor |  Cognitive Services Usages Reader |
|-------------|--------------------|------------------------|------------------|-------------------------|
|View the resource in Azure portal |✅|✅|✅| ➖ |
|View the resource endpoint under “Keys and Endpoint” |✅|✅|✅| ➖ |
|View the resource and associated model deployments in [Foundry portal](https://ai.azure.com/?cid=learnDocs) |✅|✅|✅| ➖ |
|View what models are available for deployment in [Foundry portal](https://ai.azure.com/?cid=learnDocs)|✅|✅|✅| ➖ |
|Use the Chat, Completions, and DALL-E (preview) playground experiences with any models that have already been deployed to this Azure OpenAI resource.|✅|✅|✅| ➖ |
|Create or edit model deployments|❌|✅|✅| ➖ |
|Create or deploy custom fine-tuned models|❌|✅|✅| ➖ |
|Upload datasets for fine-tuning|❌|✅|✅| ➖ |
|View, query, filter Stored completions data|❌|✅|✅| ➖ |
|Create new Azure OpenAI resources|❌|❌|✅| ➖ |
|View/Copy/Regenerate keys under “Keys and Endpoint”|❌|❌|✅| ➖ |
|Create customized guardrails|❌|❌|✅| ➖ |
|Add a data source for the "on your data" feature|✅|✅|✅| ➖ |
|Access quota|❌|❌|❌|✅|
|Make inference API calls with Microsoft Entra ID| ✅ | ✅ | ❌ |  ➖ | 
## Common Issues

### Unable to view Azure Cognitive Search option in Foundry portal

**Issue:**

When selecting an existing Azure Cognitive Search resource the search indices don't load, and the loading wheel spins continuously. In [Foundry portal](https://ai.azure.com/?cid=learnDocs), go to **Playground Chat** > **Add your data (preview)** under Assistant setup. Selecting **Add a data source** opens a modal that allows you to add a data source through either Azure Cognitive Search or Blob Storage. Selecting the Azure Cognitive Search option and an existing Azure Cognitive Search resource should load the available Azure Cognitive Search indices to select from.

**Root cause** 

To make a generic API call for listing Azure Cognitive Search services, the following call is made:

``` https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Search/searchServices?api-version=2021-04-01-Preview ```
  
Replace {subscriptionId} with your actual subscription ID.

For this API call, you need a **subscription-level scope** role. You can use the **Reader** role for read-only access or the **Contributor** role for read-write access. If you only need access to Azure Cognitive Search services, you can use the **Azure Cognitive Search Service Contributor** or **Azure Cognitive Search Service Reader** roles.

**Solution options**

- Contact your subscription administrator or owner: Reach out to the person managing your Azure subscription and request the appropriate access. Explain your requirements and the specific role you need (for example, Reader, Contributor, Azure Cognitive Search Service Contributor, or Azure Cognitive Search Service Reader).

- Request subscription-level or resource group-level access: If you need access to specific resources, ask the subscription owner to grant you access at the appropriate level (subscription or resource group). This enables you to perform the required tasks without having access to unrelated resources.

- Use API keys for Azure Cognitive Search: If you only need to interact with the Azure Cognitive Search service, you can request the admin keys or query keys from the subscription owner. These keys allow you to make API calls directly to the search service without needing an Azure RBAC role. Keep in mind that using API keys will **bypass** the Azure RBAC access control, so use them cautiously and follow security best practices.

### Unable to upload files in Foundry portal for on your data

**Symptom:** Unable to access storage for the **on your data** feature using Foundry.

**Root cause:**

Insufficient subscription-level access for the user attempting to access the blob storage in [Foundry portal](https://ai.azure.com/?cid=learnDocs). The user may **not** have the necessary permissions to call the Azure Management API endpoint: ```https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{accountName}/listAccountSas?api-version=2022-09-01```

Public access to the blob storage is disabled by the owner of the Azure subscription for security reasons.

Permissions needed for the API call:
**`Microsoft.Storage/storageAccounts/listAccountSas/action`:** This permission allows the user to list the Shared Access Signature (SAS) tokens for the specified storage account.

Possible reasons why the user may **not** have permissions:

- The user is assigned a limited role in the Azure subscription, which does not include the necessary permissions for the API call.
- The user's role has been restricted by the subscription owner or administrator due to security concerns or organizational policies.
- The user's role has been recently changed, and the new role does not grant the required permissions.

**Solution options**

- Verify and update access rights: Ensure the user has the appropriate subscription-level access, including the necessary permissions for the API call (Microsoft.Storage/storageAccounts/listAccountSas/action). If required, request the subscription owner or administrator to grant the necessary access rights.
- Request assistance from the owner or admin: If the solution above is not feasible, consider asking the subscription owner or administrator to upload the data files on your behalf. This approach can help import the data into Foundry without **user** requiring subscription-level access or public access to the blob storage.

## Next steps

- [Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=python)
- Learn more about [Azure-role based access control (Azure RBAC)](/azure/role-based-access-control/).
- Also check out[assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).
