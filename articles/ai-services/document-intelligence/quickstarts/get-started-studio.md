---
title: "Quickstart: Document Intelligence Studio"
titleSuffix: Azure AI Services
description: How to get started processing forms and documents using Document Intelligence Studio
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: quickstart
ms.date: 03/17/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-3.0.0'
---

<!-- markdownlint-disable MD001 -->

# Get started: Document Intelligence Studio

[Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/) is an online tool for visually exploring, understanding, and integrating features from the Document Intelligence service in your applications. You can get started by exploring the pretrained models with sample or your own documents. You can also create projects to build custom template models and reference the models in your applications.

## Prerequisites for new users

To use Document Intelligence Studio, you need to acquire the following assets from the Azure portal:

* Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/).

* An Azure AI services or Document Intelligence resource. Once you have your Azure subscription, create a [single-service](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) or [Azure AI multi-service](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) resource, in the Azure portal, to get your key and endpoint.

* You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.

> [!TIP]
> Create an Azure AI Foundry resource if you plan to access multiple Azure AI services under a single endpoint/key. For Document Intelligence access only, create a Document Intelligence resource. You need a single-service resource if you intend to use [Microsoft Entra authentication](/azure/active-directory/authentication/overview-authentication).
>
> Document Intelligence now supports Azure Active Directory (Azure AD) token authentication in addition to local (key-based) authentication when accessing the Document Intelligence resources and storage accounts. Be sure to follow below instructions to set up correct access roles, especially if your resources are applied with `DisableLocalAuth` policy.

There are added prerequisites for using custom models in Document Intelligence Studio. Refer to the [documentation](studio-custom-project.md) for step by step guidance.

### Authorization policies

Your organization can opt to disable local authentication and enforce Microsoft Entra (formerly Azure Active Directory) authentication for Azure AI Document Intelligence resources and Azure blob storage.

* Microsoft Entra authentication requires that key based authorization is disabled. After key access is disabled, Microsoft Entra ID is the only available authorization method.

* Microsoft Entra allows granting minimum privileges and granular control for Azure resources.

For more information, *see* the following guidance:

  * [Disable local authentication for Azure AI Services](../../disable-local-auth.md).
  * [Prevent Shared Key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent)
 
 > [!NOTE]
 > If local (key-based) authentication is disabled for your Document Intelligence service resource, be sure to obtain **Cognitive Services User** role and your Azure AD token to authenticate requests on Document Intelligence Studio. The **Contributor** role only allows you to list keys but doesn't give you permission to use the resource when key-access is disabled.

* **Designating role assignments**. Document Intelligence Studio basic access requires the [`Cognitive Services User`](/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-user) role. For more information, *see* [Document Intelligence role assignments](try-document-intelligence-studio.md#azure-role-assignments).

> [!IMPORTANT]
>
> * Make sure you have the **Cognitive Services User role**, and not the Cognitive Services Contributor role when setting up Microsoft Entra ID authentication.
> * ✔️ **Cognitive Services User**: you need this role to Document Intelligence or Azure AI Foundry resource to enter the analyze page.
> * ✔️ **Contributor**: you need this role to create resource group, Document Intelligence service, or Azure AI Foundry resource.
> * In Azure context, Contributor role can only perform actions to control and manage the resource itself, including listing the access keys.
> * User accounts with a Contributor are only able to access the Document Intelligence service by calling with access keys. However, when setting up access with Microsoft Entra ID, key-access is disabled and **Cognitive Services User** role is required for an account to use the resources.

### Authentication in Studio

Navigate to the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/). If it's your first time logging in, a popup window appears prompting you to configure your service resource. In accordance with your organization's policy, you have one or two options:

* **Microsoft Entra authentication: access by Resource (recommended)**.

  * Choose your existing subscription.
  * Select an existing resource group within your subscription or create a new one.
  * Select your existing Document Intelligence or Azure AI Foundry resource.

    :::image type="content" source="../media/studio/configure-service-resource.png" lightbox="../media/studio/configure-service-resource.png" alt-text="Screenshot of configure service resource form from the Document Intelligence Studio.":::

* **Local authentication: access by API endpoint and key**.

  * Retrieve your endpoint and key from the Azure portal.
  * Go to the overview page for your resource and select **Keys and Endpoint** from the left pane.
  * Enter the values in the appropriate fields.

      :::image type="content" source="../media/studio/keys-and-endpoint.png" lightbox="../media/studio/keys-and-endpoint.png" alt-text="Screenshot of the keys and endpoint page in the Azure portal.":::

* After validating the scenario in the Document Intelligence Studio, use the [**C#**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [**Java**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [**JavaScript**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), or [**Python**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) client libraries or the [**REST API**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) to get started incorporating Document Intelligence models into your own applications.


### Try a Document Intelligence model

To learn more about the available Document Intelligence models, *see* our [model support](../studio-overview.md#document-intelligence-model-support) page.

* Once your resource is configured, you can try the different models offered by Document Intelligence Studio. From the front page, select any Document Intelligence model to try using with a no-code approach.

* To test any of the document analysis or prebuilt models, select the model and use one of the sample documents or upload your own document to analyze. The analysis result is displayed at the right in the content-result-code window.

* Custom models need to be trained on your documents. See [custom models overview](../train/custom-model.md) for an overview of custom models.

* After validating the scenario in the Document Intelligence Studio, use the [**C#**](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), [**Java**](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), [**JavaScript**](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), or [**Python**](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) client libraries or the [**REST API**](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) to get started incorporating Document Intelligence models into your own applications.

#### View resource details

 To view resource details such as name and pricing tier, select the **Settings** icon in the top-right corner of the Document Intelligence Studio home page and select the **Resource** tab. If you have access to other resources, you can switch resources as well.

:::image type="content" source="../media/studio/form-recognizer-studio-resource-page.png" lightbox="../media/studio/form-recognizer-studio-resource-page.png" alt-text="Screenshot of the studio settings page resource tab.":::

With Document Intelligence, you can quickly automate your data processing in applications and workflows, easily enhance data-driven strategies, and skillfully enrich document search capabilities.

#### Manage third-party settings for Studio access

**Edge**:

* Go to **Settings** for Microsoft Edge
* Search for "**third-party**"
* Go to **Manage and delete cookies and site data**
* Turn off the setting of **Block third-party cookies**

**Chrome**:

* Go to **Settings** for Chrome
* Search for "**Third-party**"
* Under **Default behavior**, select **Allow third-party cookies**

**Firefox**:

* Go to **Settings** for Firefox
* Search for "**cookies**"
* Under **Enhanced Tracking Protection**, select **Manage Exceptions**
* Add exception for **`https://documentintelligence.ai.azure.com`** or the Document Intelligence Studio URL of your environment

**Safari**:

* Choose **Safari** > **Preferences**
* Select **Privacy**
* Deselect **Block all cookies**

### Troubleshooting

|Scenario     |Cause| Resolution|
|-------------|------|----------|
|You receive the error message</br> `Form Recognizer Not Found` when opening a custom project.|Your Document Intelligence resource, bound to the custom project was deleted or moved to another resource group.| There are two ways to resolve this problem: </br>&bullet; Re-create the Document Intelligence resource under the same subscription and resource group with the same name.</br>&bullet; Re-create a custom project with the migrated Document Intelligence resource and specify the same storage account.|
|You receive the error message</br> `PermissionDenied` when using prebuilt apps or opening a custom project.|The principal doesn't have access to API/Operation when analyzing against prebuilt models or opening a custom project. It's likely the local (key-based) authentication is disabled for your Document Intelligence resource don't have enough permission to access the resource.|Reference [Azure role assignments](try-document-intelligence-studio.md#azure-role-assignments) to configure your access roles.|
|You receive the error message</br> `AuthorizationPermissionMismatch` when opening a custom project.|The request isn't authorized to perform the operation using the designated permission. It's likely the local (key-based) authentication is disabled for your storage account and you don't have the granted permission to access the blob data.|Reference [Azure role assignments](try-document-intelligence-studio.md#azure-role-assignments) to configure your access roles.|
|You can't sign in to Document Intelligence Studio and receive the error message</br> `InteractionRequiredAuthError:login_required:AADSTS50058:A silent sign-request was sent but no user is signed in`|It's likely that your browser is blocking third-party cookies so you can't successfully sign in.|To resolve, see [Manage third-party settings](#manage-third-party-settings-for-studio-access) for your browser.|

## Next steps

* [Learn how to create custom projects in Document Intelligence Studio](studio-custom-project.md)

* [Get started with Document Intelligence client libraries](get-started-sdks-rest-api.md)
