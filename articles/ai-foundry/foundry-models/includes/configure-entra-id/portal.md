---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 01/22/2026
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
monikerRange: 'foundry-classic || foundry'
---


## Configure Microsoft Entra ID for inference

Follow these steps to configure Microsoft Entra ID for inference: 

1. Go to the [Azure portal](https://portal.azure.com) and locate the **Microsoft Foundry resource** you're using.

::: moniker range="foundry-classic"

   You can also navigate to the Foundry resource from the Foundry portal as follows:

   1. [!INCLUDE [version-sign-in](../../../includes/version-sign-in.md)]

   1. On the landing page, select **Management center**.

   1. Go to the section **Connected resources** and select the connection to the Foundry resource that you want to configure. If it isn't listed, select **View all** to see the full list.

      :::image type="content" source="../../media/configure-entra-id/resource-behind-select.png" alt-text="Screenshot showing how to navigate to the details of the connection in Foundry in the management center." lightbox="../../media/configure-entra-id/resource-behind-select.png":::

   1. On the **Connection details** section, under **Resource**, select the name of the Azure resource. This action opens the resource in the Azure portal.

::: moniker-end

   :::image type="content" source="../../media/configure-entra-id/locate-resource-ai-services.png" alt-text="Screenshot showing the resource to which we configure Microsoft Entra ID." lightbox="../../media/configure-entra-id/locate-resource-ai-services.png":::

1. On the left pane, select **Access control (IAM)** and then select **Add** > **Add role assignment**.

   :::image type="content" source="../../media/configure-entra-id/resource-aim.png" alt-text="Screenshot showing how to add a role assignment in the Access control section of the resource in the Azure portal." lightbox="../../media/configure-entra-id/resource-aim.png":::

   > [!TIP]
   > Use the **View my access** option to verify which roles are already assigned to you.

1. On **Job function roles**, type **Cognitive Services User**.

   :::image type="content" source="../../media/configure-entra-id/cognitive-services-user.png" alt-text="Screenshot showing how to select the Cognitive Services User role assignment." lightbox="../../media/configure-entra-id/cognitive-services-user.png":::

1. Select the role and select **Next**.

1. On **Members**, select the user or group you want to grant access to. Use security groups whenever possible as they're easier to manage and maintain. 

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

Key-based access is still possible for users that already have keys available to them. To revoke the keys, in the Azure portal, on the left navigation, select **Resource Management** > **Keys and Endpoints** > **Regenerate Key1** and **Regenerate Key2**.

## Use Microsoft Entra ID in your code

After you configure Microsoft Entra ID in your resource, update your code to use it when consuming the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

::: moniker range="foundry-classic"

## Use Microsoft Entra ID in your project

Even when your resource has Microsoft Entra ID configured, your projects might still use keys to consume predictions from the resource. When you use the Foundry playground, the credentials associated with the connection in your project are used. 

To change this behavior, update the connections in your projects to use Microsoft Entra ID. Follow these steps:

1. [!INCLUDE [version-sign-in](../../../includes/version-sign-in.md)]

1. Go to the projects or hubs that use the Foundry resource through a connection.

1. Select **Management center**.

1. Go to the **Connected resources** section and select the connection to the Foundry resource that you want to configure. If it's not listed, select **View all** to see the full list.

1. In the **Connection details** section, next to **Access details**, select the edit icon.

1. Under **Authentication**, change the value to **Microsoft Entra ID**.

1. Select **Update**.

1. Your connection is now configured to work with Microsoft Entra ID.

::: moniker-end

## Disable key-based authentication in the resource

Disable key-based authentication when you implement Microsoft Entra ID and fully address compatibility or fallback concerns in all the applications that consume the service. You can disable key-based authentication using the Azure CLI and when deploying with Bicep or ARM.

Key-based access is still possible for users that already have keys available to them. To revoke the keys, in the Azure portal, on the left navigation, select **Resource Management** > **Keys and Endpoints** > **Regenerate Key1** and **Regenerate Key2**.
