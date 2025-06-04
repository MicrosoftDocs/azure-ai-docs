---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 12/15/2024
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

## Configure Microsoft Entra ID for inference

Follow these steps to configure Microsoft Entra ID for inference: 

1. Go to the [Azure portal](https://portal.azure.com) and locate the **Azure AI Foundry (formerly known Azure AI Services)** resource you're using. If you're using Azure AI Foundry with projects or hubs, you can navigate to it by:

   1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

   2. On the landing page, select **Open management center**.

   3. Go to the section **Connected resources** and select the connection to the Azure AI Foundry (formerly known Azure AI Services) resource that you want to configure. If it isn't listed, select **View all** to see the full list.

      :::image type="content" source="../../media/configure-entra-id/resource-behind-select.png" alt-text="Screenshot showing how to navigate to the details of the connection in Azure AI Foundry in the management center." lightbox="../../media/configure-entra-id/resource-behind-select.png":::

   4. On the **Connection details** section, under **Resource**, select the name of the Azure resource. A new page opens.

   5. You're now in [Azure portal](https://portal.azure.com) where you can manage all the aspects of the resource itself.

      :::image type="content" source="../../media/configure-entra-id/locate-resource-ai-services.png" alt-text="Screenshot showing the resource to which we configure Microsoft Entra ID." lightbox="../../media/configure-entra-id/locate-resource-ai-services.png":::

2. On the left pane, select **Access control (IAM)** and then select **Add** > **Add role assignment**.

   :::image type="content" source="../../media/configure-entra-id/resource-aim.png" alt-text="Screenshot showing how to add a role assignment in the Access control section of the resource in the Azure portal." lightbox="../../media/configure-entra-id/resource-aim.png":::

   > [!TIP]
   > Use the **View my access** option to verify which roles are already assigned to you.

3. On **Job function roles**, type **Cognitive Services User**. The list of roles is filtered out.

   :::image type="content" source="../../media/configure-entra-id/cognitive-services-user.png" alt-text="Screenshot showing how to select the Cognitive Services User role assignment." lightbox="../../media/configure-entra-id/cognitive-services-user.png":::

4. Select the role and select **Next**.

5. On **Members**, select the user or group you want to grant access to. We recommend using security groups whenever possible as they are easier to manage and maintain. 

   :::image type="content" source="../../media/configure-entra-id/select-user.png" alt-text="Screenshot showing how to select the user to whom assign the role." lightbox="../../media/configure-entra-id/select-user.png":::

6. Select **Next** and finish the wizard.

7. The selected user can now use Microsoft Entra ID for inference.

    > [!TIP]
    > Keep in mind that Azure role assignments may take up to five minutes to propagate. When working with security groups, adding or removing users from the security group propagates immediately.

Notice that key-based access is still possible for users that already have keys available to them. If you want to revoke the keys, in the Azure portal, on the left navigation, select **Resource Management** > **Keys and Endpoints** > **Regenerate Key1** and **Regenerate Key2**.

## Use Microsoft Entra ID in your code

Once you configured Microsoft Entra ID in your resource, you need to update your code to use it when consuming the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Troubleshooting

[!INCLUDE [troubleshooting](troubleshooting.md)]

## Use Microsoft Entra ID in your project

Even when your resource has Microsoft Entra ID configured, your projects may still be using keys to consume predictions from the resource. When using the Azure AI Foundry playground, the credentials associated with the connection your project has are used. 

To change this behavior, you have to update the connections from your projects to use Microsoft Entra ID. Follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. Navigate to the projects or hubs that are using the Azure AI Foundry (formerly known Azure AI Services) resource through a connection.

3. Select **Management center**.

3. Go to the section **Connected resources** and select the connection to the Azure AI Foundry (formerly known Azure AI Services) resource that you want to configure. If it's not listed, select **View all** to see the full list.

4. On the **Connection details** section, next to **Access details**, select the edit icon.

5. Under **Authentication**, change the value to **Microsoft Entra ID**.

6. Select **Update**.

7. Your connection is configured to work with Microsoft Entra ID now.

## Disable key-based authentication in the resource

Disabling key-based authentication is advisable when you implemented Microsoft Entra ID and fully addressed compatibility or fallback concerns in all the applications that consume the service. Disabling key-based authentication is only available when deploying using Bicep/ARM.
