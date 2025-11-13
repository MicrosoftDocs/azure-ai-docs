---
title: Create a Document Intelligence Resource
titleSuffix: Foundry Tools
description: Create a Document Intelligence resource in the Azure portal.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---


# Create a Document Intelligence resource

::: moniker range="<=doc-intel-4.0.0"
 [!INCLUDE [applies to v4.0 v3.1 v3.0 v2.1](../includes/applies-to-v40-v31-v30-v21.md)]
::: moniker-end

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../../../ai-services/index.yml) that uses machine-learning models to extract key/value pairs, text, and tables from your documents. In this article, learn how to create a Document Intelligence resource in the Azure portal.

## Visit the Azure portal

The Azure portal is a single platform that you can use to create and manage Azure services.

To get started:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. On the Azure home page, select **Create a resource**.

1. In the search bar, search for and choose **Document Intelligence**.

1. Select **Create**.

## Create a resource

1. Fill out the **Create Form Recognizer** fields with the following values:

    * **Subscription**: Select your current subscription.
    * **Resource group**: The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Region**: Select your local region.
    * **Name**: Enter a name for your resource. We recommend that you use a descriptive name, for example, *YourNameDocumentIntelligence*.
    * **Pricing tier**: The cost of your resource depends on the pricing tier you choose and your usage. For more information, see [Pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/). You can use the free pricing tier (F0) to try the service. You can upgrade later to a paid tier for production.

1. Select **Review + create**.

    :::image type="content" source="../media/logic-apps-tutorial/logic-app-connector-demo-two.png" alt-text="Screenshot that shows the correct values for creating a Document Intelligence resource.":::

1. Azure runs a quick validation check. After a few seconds, a green banner appears that says **Validation Passed**.

1. After the validation banner appears, select **Create**.

1. A new page opens that says **Deployment in progress**. After a few seconds, a message appears that says **Your deployment is complete**.

## Get endpoint URL and keys

1. After you receive the message, select **Go to resource**.

1. Copy the key and endpoint values from your Document Intelligence resource. Paste the values in a convenient location, such as Notepad. You need the key and endpoint values to connect your application to the Document Intelligence API.

1. If your overview page doesn't show the keys and endpoint, select **Keys and Endpoint** on the left pane, and retrieve them there.

    :::image border="true" type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot that shows how to access the resource key and endpoint URL.":::

## Related content

* Try [Document Intelligence Studio](../concept-document-intelligence-studio.md), an online tool that helps you visually explore, understand, and integrate features from Document Intelligence into your applications.
* Finish a Document Intelligence quickstart and then create a document processing app in the development language of your choice:

  * [C#](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)
  * [Python](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)
  * [Java](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)
  * [JavaScript](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)
