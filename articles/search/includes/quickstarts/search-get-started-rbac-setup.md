---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/08/2025
---

## Configure role-based access

In this section, you enable RBAC on your Azure AI Search service and assign the necessary roles for creating, loading, and querying search objects. For more information about these steps, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

To configure access:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Settings > Keys**.

1. Select **Role-based access control** or **Both** if you need time to transition clients to RBAC.

   :::image type="content" source="../../media/search-get-started-rbac/access-control-options.png" lightbox="../../media/search-get-started-rbac/access-control-options.png" alt-text="Screenshot of the access control options in the Azure portal.":::

1. From the left pane, select **Access control (IAM)**.

1. Select **Add** > **Add role assignment**.

   :::image type="content" source="../../media/search-get-started-rbac/add-role-assignment.png" lightbox="../../media/search-get-started-rbac/add-role-assignment.png" alt-text="Screenshot of the dropdown menu for adding a role assignment in the Azure portal.":::

1. Assign the **Search Service Contributor** role to your user account or managed identity.

1. Repeat the role assignment for **Search Index Data Contributor**.

## Get service information

In this section, you retrieve the subscription ID and endpoint of your Azure AI Search service. If you only have one subscription, skip the subscription ID and only retrieve the endpoint. You use these values in the remaining sections of this quickstart.

To get your service information:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Overview**.

1. Make a note of the subscription ID and endpoint.

   :::image type="content" source="../../media/search-get-started-rbac/subscription-and-endpoint.png" lightbox="../../media/search-get-started-rbac/subscription-and-endpoint.png" alt-text="Screenshot of the subscription ID and endpoint in the Azure portal.":::
