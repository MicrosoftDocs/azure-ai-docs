---
title: Enable Microsoft Entra ID authentication
description: How to enable Microsoft Entra ID authentication.
ms.service: azure-ai-translator
ms.topic: install-set-up-deploy
manager: nitinme
ms.author: lajanuar
author: laujan
ms.date: 11/18/2025
---

# Enable Microsoft Entra ID authentication

Microsoft Entra ID is a cloud-based identity solution designed to manage user access and permissions for Microsoft services, resources, and applications. Organizations that subscribe to Microsoft's online business services, such as Microsoft Azure, have access to Microsoft Entra ID.

Microsoft Entra ID enables you to authenticate requests to your Azure resources without the need for passwords or keys. Instead, a robust layer of security is created by registering an identity application with the Microsoft Entra ID platform. This registration enables your identity application to make secure requests to your Azure resource API, thus establishing a trust relationship with the Microsoft identity platform.

This article guides you on how to create and utilize a Microsoft Entra ID identity application to authenticate requests to your Azure resources. Here are the steps:

* [Set up prerequisites](#prerequisites).
* [Disable key-based (local) authentication](#disable-key-authentication)
* [Register an identity application with Microsoft Entra ID](#register-an-identity-application-with-microsoft-entra-id)
* [Add a client secret](#add-a-client-secret-credential)
* [Assign an `RBAC` (role-based access control) role to grant access permissions to your application.](#add-api-permissions)
* [Obtain an access token](#obtain-an-access-token-with-oauth-client-credentials-flow)
* [Make a request to the Azure Translator API](#use-access-token-authentication-for-a-rest-api-request)

## Prerequisites

Before you get started, you need an Azure account and a Foundry Tools subscription.

* An active Azure subscription. If you don't have an Azure subscription, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* An Azure Translator resource. Once you have your Azure subscription, create a [Translator single-service global resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) in the Azure portal.

> [!IMPORTANT]
> [Regional endpoints](../../cognitive-services-custom-subdomains.md#is-there-a-list-of-regional-endpoints) don't support Microsoft Entra authentication.

* cURL command-line tool installed.

* **PowerShell version 7.*+** (or a similar command-line application.):
  * [Windows](/powershell/scripting/install/installing-powershell-on-windows)
  * [macOS](/powershell/scripting/install/installing-powershell-on-macos)
  * [Linux](/powershell/scripting/install/installing-powershell-on-linux)

* To check your PowerShell version, type the following command relative to your operating system:
  * Windows: `Get-Host | Select-Object Version`
  * macOS or Linux: `$PSVersionTable`

## Disable key authentication

To use Microsoft Entra authentication, key-based (local) authentication must be turned off. Once key access is disabled, Microsoft Entra ID becomes the sole authorization method. Your organization can choose to deactivate local authentication and mandate Microsoft Entra for Azure resources. If not, you can disable key authentication for specific resources following these steps in `PowerShell`:

1. **Connect to Azure**

   ```powershell
    Connect-AzAccount
   ```

1. **Verify local authentication status**

   ```powershell
    Get-AzCognitiveServicesAccount
   ```

1. **Check that the property `DisableLocalAuth` is set to `$true` (local authentication *is* disabled)**

   ```powershell
   Get-AzCognitiveServicesAccount -ResourceGroupName "my-resource-group" -Name "my-resource-name"
   ```

   If the `DisableLocalAuth` is blank or set to False, you must set it to $true.

1. **Disable local authentication**

   ```powershell
   Set-AzCognitiveServicesAccount -ResourceGroupName "my-resource-group" -Name "my-resource-name" -DisableLocalAuth $true

   ```

You can check once more to ensure that local authentication is disabled using the [`Get-AzCognitiveServicesAccount`](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccount) cmdlet. A value of True means local authentication is disabled.

## Register an identity application with Microsoft Entra ID

1. Navigate to the [Azure portal](https://portal.azure.com/#home)

1. Enter `Microsoft Entra ID` in the search box at the top of the page.

    :::image type="content" source="../media/entra-id/azure-portal-search.png" alt-text="Screenshot of the Azure portal search box.":::

1. Select the `Microsoft Entra ID` service from the drop-down menu.

    :::image type="content" source="../media/entra-id/portal-search-results.png" alt-text="Screenshot of Microsoft Entra ID search results in the Azure portal.":::

1. Selecting `Microsoft Entra ID` opens your organization's overview page in the Azure portal.


1. From the left rail menu `Manage` node, select `App registrations`.

    :::image type="content" source="../media/entra-id/manage-app-registrations.png" alt-text="Screenshot of App registrations selection from the Manage menu.":::

1. Select `New registration` from the menu at the top of the main window.

    :::image type="content" source="../media/entra-id/new-registration-selection.png" alt-text="Screenshot of the New registration selection in the main window of the page.":::

1. Complete the application registration fields:<br><br>

   * **Name**. Select a name for your application. In our case, let's use `azure-ai-auth-app`.
   * **Supported account types**. Specify who can use the application.
   * **Redirect URI**. This selection is optional. We're skipping it for this project.
   * **Register**. Select the `Register` button and complete the `App registration`.

   For more information on registering an application, *see* [Register an application](/entra/identity-platform/quickstart-register-app?tabs=certificate#register-an-application)

1. Once registration completes, The `App's registration` **Overview** pane is displayed. The **Application (client) ID**, also called the `client ID`, value uniquely identifies your application in the Microsoft identity platform.

   :::image type="content" source="../media/entra-id/app-registration-overview.png" alt-text="Screenshot of the App registration overview page.":::

1. **Before you leave the App registration overview page**, copy and paste the following values in a secure and convenient location, such as Windows Notepad:

   * `Application (client) ID`
   * `Directory (tenant) ID`

You completed your App registration. Next we [add a client secret](#add-a-client-secret-credential) to your application.

## Add a client secret credential

Client applications utilize credentials to gain access to a web API. These credentials enable the application to authenticate independently, eliminating the need for user interaction, such as key entry, during runtime. Your application's client secret (application password) is a string that the application uses to prove its identity when requesting a token.

1. Select the Overview page from the left navigation menu.

   :::image type="content" source="../media/entra-id/application-overview.png" alt-text="Screenshot of the App registration overview page in the Azure portal.":::

1. Select **`Add a certificate or secret`**.

    :::image type="content" source="../media/entra-id/add-secret.png" alt-text="Screenshot of add secret link in the Azure portal.":::

1. Next select **`New client secret`**.

   :::image type="content" source="../media/entra-id/new-client-secret.png" alt-text="Screenshot of new client secret button in the Azure portal.":::


1. In the **`Add a client secret`** window, add a description, set an expiry period, and then select the **`Add`** button.

   :::image type="content" source="../media/entra-id/add-new-client-secret.png" alt-text="Screenshot of the Add a client secret setup window.":::

1. Copy and paste the client secret **`Value`** in the same secure location as the `Application (client) ID` and `Directory (tenant) ID`, such as Windows Notepad. Client secret values can only be viewed immediately after creation. Be sure to save the secret before leaving the page.

    :::image type="content" source="../media/entra-id/client-secret-value.png" alt-text="Screenshot of the client secret value location for a registered application in the Azure portal.":::

Now that your application has the proper authentication credentials, we add permissions for your application to access Microsoft Foundry resources.

## Add API permissions

Next, let's add a permission that allows the application to access the Foundry Tools (Cognitive Services) APIs, including Azure Translator, as a user.

1. In the left navigation menu, navigate to **`API permissions`** then select **`Add a permission`** from the main window.

   :::image type="content" source="../media/entra-id/add-api-permissions.png" alt-text="Screenshot of API permissions view in the Azure portal.":::

1. From the new window that appears select **`APIs my organization uses`** and then type **`Microsoft Cognitive Services`** in the search bar.

   :::image type="content" source="../media/entra-id/request-api-permissions.png" alt-text="Screenshot of the Request API permissions search window.":::

1. Select **`Microsoft Cognitive Services`** from the search results.

   * In the new window, under **`Permissions`**, select **`Delegated permissions`**.
   * Mark the **`Access Cognitive Services API as organization users`** checkbox.
   * Select **`Add permissions`**.

      :::image type="content" source="../media/entra-id/add-permissions.png" alt-text="Screenshot of the Azure Cognitive Services application permissions window.":::

That's it! The setup for your Microsoft Entra ID application is complete. Next, your Translator resource needs to grant your application access by adding a role assignment to your application specifically for the Translator resource. For more information, *see* [Azure role-based access control](/azure/role-based-access-control/overview)

## Assign the Cognitive Services User role to Azure Translator resource

Role-based access control (Azure `RBAC`) is a security principal that enables you to control access to Azure resources. You can use `RBAC` to grant access to any resource that supports Microsoft Entra authentication, in our case, your Azure Translator instance. To grant your Microsoft Entra ID application access to your Translator resource, assign an Azure role using [Azure role-based access control (`Azure RBAC`)](/azure/role-based-access-control/overview).

1. Staying in the Azure portal, navigate to your Azure Translator global resource.

1. In the left menu, select **`Access control (IAM)`**.

1. Select **`Add role assignment`** from the main window.

   :::image type="content" source="../media/entra-id/add-role-assignment.png" alt-text="Screenshot of the Access control window.":::

1. In the left navigation name menu, select **`Cognitive Services User`** and select the **`Next`** button.

1. On the `Add role assignment page`, assign access to **`User, group, or service principal`** .

1. Choose **`Select members`**.

    :::image type="content" source="../media/entra-id/add-members.png" alt-text="Screenshot of add role assignment members window.":::

1. In the window that opens, type the name of your registered application in the search box (for example, text-translation-app). Select your application and choose the `Select` button.

   :::image type="content" source="../media/entra-id/select-members.png" alt-text="Screenshot of select members window in the Azure portal.":::

1. Complete the assignment process by selecting the `Review + assign` button.

Now, we're ready to test out using your application to obtain a security token for REST API calls.

## Obtain an access token with OAuth client credentials flow

Access tokens are a type of security token designed for authorization, granting access to specific resources on behalf on an authenticated user and enable clients to securely call protected web APIs. In our case, the access token grants your Microsoft Entra ID registered application authorization to access your Translator resource on your behalf.

> [!NOTE]
>
> * The default lifespan of an access token isn't fixed.
> * Upon issuance, the Microsoft identity platform assigns it a random duration ranging from 60 to 90 minutes, with an average of 75 minutes.
> * When the token expires, repeat the request to the /token endpoint to acquire a fresh access token.
> * Refresh tokens aren't issued with the client credentials flow. Since the `client_id` and `client_secret` (which are required to obtain a refresh token) are already used to obtain an access token eliminating the need for a refresh token in this context. For more information, *see* [OAuth 2.0 client credentials flow](/entra/identity-platform/v2-oauth2-client-creds-grant-flow#use-a-token)

1. Prepare for the token request. You need the following values from your registered application:

    * **Application (client) ID**. Located on your registered application's overview page. Copied and stored during the earlier [register an identity application](#register-an-identity-application-with-microsoft-entra-id) step.(#register-an-identity-application-with-microsoft-entra-id).
    * **Tenant ID**. Located on your registered application's overview page. Copied and stored during the earlier [register an identity application](#register-an-identity-application-with-microsoft-entra-id) step.
    * **Client secret value**. Copied and stored during the earlier [Add a client secret credential](#add-a-client-secret-credential) step.

1. Let's use `cURL` to make a token request. Here's the code:

   ***Linux or macOS***

   ```bash
   curl -X POST https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id={client-id}" \
     -d "scope= https://cognitiveservices.azure.com/.default" \
     -d "client_secret={client-secret}" \
     -d "grant_type=client_credentials" |json_pp
   ```

   ***Windows***

   ```bash
   curl -X POST https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token ^
     -H "Content-Type: application/x-www-form-urlencoded" ^
     -d "client_id={client-id}" ^
     -d "scope= https://cognitiveservices.azure.com/.default" ^
     -d "client_secret={client-secret}" ^
     -d "grant_type=client_credentials" |json
   ```

1. Replace {`tenant-id`} in the request URL, {`client-id`}, and {`client-secret`} with your actual values.

   * The `|json_pp` (macOS) and `|json` (Windows) commands enable prettify Json with cURL.

   * Your access token is received in the response.

1. Save the obtained access in a secure and convenient location, such as Windows Notepad.

Great! Now let's make an REST API call to the Azure Translator AI API.

## Use access token authentication for a REST API request

To make a valid REST API request, the following values are required:

* Identity of your Translator instance. You can provide that in two ways (choose one):

  * [Use the global endpoint](#use-the-global-endpoint) and pass `resourceId` as a request header.

  * Use your [custom endpoint](#use-your-custom-domain-endpoint) as part of the POST request URL.

* A Microsoft Entra ID access token acquired from your Microsoft Entra ID application.

### Use the global endpoint

1. Navigate to your resource instant page in the Azure portal.

    * The global endpoint is found on under `Resource Management` → `Keys and Endpoint` → `Web API` → `Text translation`.

    * The `ResourceID` is found under `Resource Management` → `Properties`.

    * Resource ID format:
      `/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.CognitiveServices/accounts/<resourceName>/`

      :::image type="content" source="../media/managed-identities/resource-id-property.png" alt-text="Screenshot of Resource ID value location in the Azure portal.":::

1. Replace {your-resource-ID} with the value from the Azure portal and {access-token} with the value obtained from the previous step: [obtain an access token](#obtain-an-access-token-with-oauth-client-credentials-flow).

    ***Linux or macOS***

    ```bash
    curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en" \
         -H "Authorization: Bearer {access-token}"\
         -H "Ocp-Apim-ResourceId: {your-resource-ID}" \
         -H "Content-Type: application/json" \
         -d "[{'Text':'Hola'}]"
    ```

    ***Windows***

    ```bash
    curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en" ^
         -H "Authorization: Bearer {access-token}" ^
         -H "Ocp-Apim-ResourceId: {your-resource-id}" ^
         -H "Content-Type: application/json" ^
         -d "[{'Text':'Hola'}]"
    ```

### Use your custom domain endpoint

 Your custom domain endpoint is a URL formatted with your resource name and hostname and is available in the Azure portal. When you created your Translator resource, the value that you entered in the `Name` field is the custom domain name parameter for the endpoint. You can find your custom domain endpoint URL in the Document translation and Containers Text translation fields.

***Linux or macOS***

```bash
curl -X POST "https://{your-custom-domain}.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=en" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d "[{'Text':'Hola'}]"
```

***Windows***

```bash
curl -X POST "https://{your-custom-domain}.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=en" ^
  -H "Authorization: Bearer {access-token}" ^
  -H "Content-Type: application/json" ^
  -d "[{'Text':'Hola'}]"
```

Replace {your-custom-domain} with the value form the Azure portal and {access-token} with the token obtained from the previous step, [obtain an access token](#obtain-an-access-token-with-oauth-client-credentials-flow).

Here's an example of the JSON response:

  ```json
  [{"detectedLanguage":{"language":"es","score":1.0},"translations":[{"text":"Hello","to":"en"}]}]
  ```

Well done! You now know how to use Microsoft Entra ID to authenticate requests to your Azure resource.
