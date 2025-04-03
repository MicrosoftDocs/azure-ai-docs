---
title: Create a Translator resource
titleSuffix: Azure AI services
description: Learn how to create an Azure AI Translator resource and obtain your API key and endpoint URL through the Azure portal.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 01/27/2025
ms.service: azure-ai-translator
ms.topic: how-to

---

# Create a Translator resource

In this article, you learn how to create a Translator resource in the Azure portal. [Azure AI Translator](../overview.md) is a cloud-based machine translation service that is part of the [Azure AI services](../../what-are-ai-services.md) family. Azure resources are instances of services that you create. All API requests to Azure AI services require an *endpoint* URL and a read-only *key* for authenticating access.

## Prerequisites

To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).

## Create your resource

With your Azure account, you can access the Translator service through two different resource types:

* [**Single-service**](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) resource types enable access to a single service API key and endpoint.

* [**Multi-service**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) resource types enable access to multiple Azure AI services by using a single API key and endpoint.

## Complete your project and instance details

After you decide which resource type you want use to access the Translator service, you can enter the details for your project and instance.

1. **Subscription**. Select one of your available Azure subscriptions.

1. **Resource Group**. You can create a new resource group or add your resource to a preexisting resource group that shares the same lifecycle, permissions, and policies.

1. **Resource Region**. Choose **Global** unless your business or application requires a specific region. If you're planning on using the Document Translation feature with [managed identity authorization](../document-translation/how-to-guides/create-use-managed-identities.md), choose a geographic region such as **East US**.

1. **Name**. Enter a name for your resource. The name you choose must be unique within Azure.

   > [!NOTE]
   > If you're using a Translator feature that needs a custom domain endpoint, such as Document Translation, the input in the `name` field it the custom domain name parameter for the endpoint.
  > Make sure to enter the correct value in the `name` field to ensure proper functionality.

1. **Pricing tier**. Select a [pricing tier](https://azure.microsoft.com/pricing/details/cognitive-services/translator) that meets your needs:

   * Each subscription has a free tier.
   * The free tier has the same features and functionality as the paid plans and doesn't expire.
   * Only one free tier resource is available per subscription.
   * Document Translation is supported in paid tiers. The Language Studio only supports the S1 or D3 instance tiers. If you just want to try Document Translation, select the Standard S1 instance tier.

1. If you created a multi-service resource, the links at the bottom of the **Basics** tab provides technical documentation regarding the appropriate operation of the service.

1. Select **Review + Create**.

1. Review the service terms, and select **Create** to deploy your resource.

1. After your resource successfully deploys, select **Go to resource**.

### Authentication keys and endpoint URL

All Azure AI services API requests require an endpoint URL and a read-only key for authentication.

* **Authentication keys**. Your key is a unique string that is passed on every request to the Translation service. You can pass your key through a query-string parameter or by specifying it in the HTTP request header.

* **Endpoint URL**. Use the Global endpoint in your API request unless you need a specific Azure region or custom endpoint. For more information, see [Base URLs](../text-translation/reference/v3/reference.md#base-urls). The Global endpoint URL is `api.cognitive.microsofttranslator.com`.

## Get your authentication keys and endpoint

To authenticate your connection to your Translator resource, you need the key and endpoint for your resource.

1. After your new resource deploys, select **Go to resource** or go to your resource page.
1. In the left navigation pane, under **Resource Management**, select **Keys and Endpoint**.
1. Copy and paste your keys and endpoint URL in a convenient location, such as Notepad.

:::image type="content" source="../media/keys-and-endpoint-resource.png" alt-text="Screenshot of the Azure portal showing the Keys and Endpoint page of a Translator resource. The keys and endpoints are highlighted.":::

## Create a Text Translation client

Text Translation supports both [global and regional endpoints](#complete-your-project-and-instance-details). Once you have your [authentication keys](#authentication-keys-and-endpoint-url), you need to create an instance of the `TextTranslationClient`, using an `AzureKeyCredential` for authentication, to interact with the Text Translation service:

* To create a `TextTranslationClient` using a global resource endpoint, you need your resource **API key**:

    ```bash
      AzureKeyCredential credential = new('<apiKey>');
      TextTranslationClient client = new(credential);
    ```

* To create a `TextTranslationClient` using a regional resource endpoint, you need your resource **API key** and the name of the **region** where your resource is located:

    ```bash
     AzureKeyCredential credential = new('<apiKey>');
     TextTranslationClient client = new(credential, '<region>');
    ```

## How to delete a  resource or resource group

> [!WARNING]
>
> Deleting a resource group also deletes all resources contained in the group.

To delete the resource:

1. Search and select **Resource groups** in the Azure portal, and select your resource group.
1. Select the resources to be deleted by selecting the adjacent check box.
1. Select **Delete** from the top menu near the right edge.
1. Enter *delete* in the **Delete Resources** dialog box.
1. Select **Delete**.

To delete the resource group:

1. Go to your Resource Group in the Azure portal.
1. Select **Delete resource group** from the top menu bar.
1. Confirm the deletion request by entering the resource group name and selecting **Delete**.

## How to get started with Azure AI Translator REST APIs

In our quickstart, you learn how to use the Translator service with REST APIs.

> [!div class="nextstepaction"]
> [Get Started with Translator](../text-translation/quickstart/rest-api.md)

## Next Steps

Learn more about Azure AI Translator features:

* [Text Translation](../text-translation/overview.md)
* [Document Translation](../document-translation/overview.md)
* [Custom Translation](../custom-translator/overview.md)