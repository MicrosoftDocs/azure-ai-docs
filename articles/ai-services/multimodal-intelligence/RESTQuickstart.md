---
title: Quickstart: Azure AI Multimodal Intelligence REST APIs
titleSuffix: Azure AI services
description: Learn about Multimodal Intelligence REST APIs
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/22/2024
---

# Azure AI Multimodal Intelligence content extraction
Before you get started using Multimodal Intelligence, you need an Azure AI services multi-service resource. The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

1.  To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).

1. Sign in to the [Azure portal](https://portal.azure.com) and select **Create a resource** from the Azure portal home page. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal as shown here:

    :::image type="content" source="media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::
  
    > [!IMPORTANT]
    > Azure provides more than one resource types named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.

1. Select the **Create** button.

1. Next, you're going to fill out the **`Create Document Intelligence`** fields with the following values:

    * **Subscription**. Select one of your available Azure subscriptions.
    * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Region**. Select your local region. Different locations may introduce latency, but have no impact on the runtime availability of your resource.
    * **Name**. Enter a name for your resource. We recommend using a descriptive name, for example *YourNameAIServicesResource*.
    * **Pricing tier**. The cost of your resource depends on the pricing tier and options you choose and your usage. For more information, see [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/). You can use the free pricing tier (F0) to try the service, and upgrade later to a paid tier for production.

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

1. Azure will run a quick validation check, after a few seconds you should see a green banner that says **Validation Passed**.

1. Once the validation banner appears, select the **Create** button from the bottom-left corner.

1. After you select create, you'll be redirected to a new page that says **Deployment in progress**. After a few seconds, you'll see a message that says, **Your deployment is complete**.