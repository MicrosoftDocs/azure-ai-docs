---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 01/22/2026
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

## Configure Microsoft Entra ID for inference

This section lists the steps to configure Microsoft Entra ID for inference from the Microsoft Foundry resource page in the [Azure portal](https://portal.azure.com).

:::image type="content" source="../../media/configure-entra-id/locate-resource-ai-services.png" alt-text="Screenshot showing the resource to which we configure Microsoft Entra ID." lightbox="../../media/configure-entra-id/locate-resource-ai-services.png":::

1. Select the resource name to open it.
 
1. In the left pane, select **Access control (IAM)**, and then select **Add** > **Add role assignment**.

   :::image type="content" source="../../media/configure-entra-id/resource-aim.png" alt-text="Screenshot showing how to add a role assignment in the Access control section of the resource in the Azure portal." lightbox="../../media/configure-entra-id/resource-aim.png":::

   > [!TIP]
   > Use the **View my access** option to verify which roles are already assigned to you.

1. In **Job function roles**, type **Cognitive Services User**.

   :::image type="content" source="../../media/configure-entra-id/cognitive-services-user.png" alt-text="Screenshot showing how to select the Cognitive Services User role assignment." lightbox="../../media/configure-entra-id/cognitive-services-user.png":::

1. Select the role and select **Next**.

1. On **Members**, select the user or group you want to grant access to. Use security groups whenever possible because they're easier to manage and maintain.

   :::image type="content" source="../../media/configure-entra-id/select-user.png" alt-text="Screenshot showing how to select the user to whom assign the role." lightbox="../../media/configure-entra-id/select-user.png":::

1. Select **Next** and finish the wizard.

1. The selected user can now use Microsoft Entra ID for inference.

    > [!TIP]
    > Azure role assignments can take up to five minutes to propagate. When working with security groups, adding or removing users from the security group propagates immediately.

1. Verify the role assignment:

   1. On the left pane in the Azure portal, select **Access control (IAM)**.
   
   1. Select **Check access**.
   
   1. Search for the user or security group you assigned the role to.
   
   1. Verify that **Cognitive Services User** appears in their assigned roles.

Key-based access is still possible for users who already have keys available to them. To revoke the keys, in Azure portal, on the left navigation, select **Resource Management** > **Keys and Endpoints** > **Regenerate Key1** and **Regenerate Key2**.

## Use Microsoft Entra ID in your code

After you configure Microsoft Entra ID in your resource, update your code to use it when you consume the inference endpoint. This example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Disable key-based authentication in the resource

Disable key-based authentication when you implement Microsoft Entra ID and fully address compatibility or fallback concerns in all applications that consume the service. You can disable key-based authentication by using Azure CLI or when deploying with Bicep or ARM.

Key-based access is still possible for users that already have keys available to them. To revoke the keys, in the Azure portal, on the left navigation, select **Resource Management** > **Keys and Endpoints** > **Regenerate Key1** and **Regenerate Key2**.
