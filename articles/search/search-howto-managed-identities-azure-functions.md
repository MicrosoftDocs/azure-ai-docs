---
title: Set up an indexer connection to Azure functions using "EasyAuth"
titleSuffix: Azure AI Search
description: Learn how to set up an indexer connection to an Azure Function using built-in authentication also known as "EasyAuth"
author: arv100kri
ms.author: arjagann

ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/20/2025
ms.custom:
  - subject-rbac-steps
---

# Authenticate to Azure Functions using "EasyAuth" (Azure AI Search)

This article explains how to set up an indexer connection to an Azure function app using the [built-in authentication capabilities of App services](/azure/app-service/overview-authentication-authorization), also known as "EasyAuth". Azure function apps are a great solution for hosting Custom Web APIs that an Azure AI Search service can use either to enrich content ingested during an indexer run, or to vectorize content in a search query.

You can use either a system-assigned or a user-assigned identity of the search service to authenticate against the Azure function app.

## Prerequisites

* [Create a managed identity](search-howto-managed-identities-data-sources.md) for your search service.
* Configure Azure function app with [Microsoft Entra sign-in](/azure/app-service/configure-authentication-provider-aad).

## Limitations

* Only Microsoft Entra authentication provider is supported with Azure AI Search. 
* When using Microsoft Entra as the authentication provider, you're required to create another Microsoft Entra application registration to use as the target audience for the indexer to request a token. This application can either use the OAuth 2.0 implicit flow (without a client secret), or use the client secret. In either case, this application needs to expose a scope for delegated permissions.

## Configure Microsoft Entra application to use as authentication provider

To use Microsoft Entra as an authentication provider to the Azure function application, an application registration must be created. There are 2 options to do so - either creating one automatically via the function app itself, or using an already created existing application. To learn more about these steps follow [Azure App services' documentation](/azure/app-service/configure-authentication-provider-aad?tabs=workforce-configuration#choose-the-app-registration.md).

Regardless of either option, ensure that the app registration is configured per the following steps to ensure it being compatible with Azure AI Search.

### Ensure the app registration has application ID URI configured

The app registration should be configured with an application ID URI, which can then be used as the token audience with Azure functions and Azure AI Search. Configure it in the format `api://<applicationId>`

![Configure application ID URI](./media/search-howto-managed-identities-azure-functions/app-registration-overview.png "Configure application ID URI")

### Set supported account types for authentication

Configure the "supported account types" so that only accounts in the same organization directory as the app registration can utilize it for authentication.

![Set supported account types](./media/search-howto-managed-identities-azure-functions/authentication-supported-account.png "Set supported account types")

### (Optional) Configure a client secret

App services recommend utilizing a client secret for the authentication provider application. Authentication still works without client secret, as long as the delegated permissions are set up.

![Configure client secret](./media/search-howto-managed-identities-azure-functions/client-secret.png "Configure client secret")

### Add a scope to delegate permissions

Configure the app registration to have a scope that delegates admin and user permissions to it to ensure that it's compatible with the indexer's authentication flow.

![Add delegated permission scope](./media/search-howto-managed-identities-azure-functions/expose-api-user-impersonation.png "Add delegated permission scope")

Once the delegated permissions scope is set up, you should notice the "API permissions" has a "User.Read" API on Microsoft.Graph configured.

![Delegated permissions](./media/search-howto-managed-identities-azure-functions/api-permissions.png "Delegated permissions")

## Configure Microsoft Entra authentication provider in Azure function app

With the client application registered with the exact specifications above, Microsoft Entra authentication for the Azure function application can be set up by following the [guide from App Services](/azure/app-service/configure-authentication-provider-aad). Ensure the following settings are configured to ensure that Azure AI Search can successfully authenticate to the function app.

### Configure authentication settings

* Ensure that "App Service authentication" is "Enabled"
* Restrict access to the function app to "Require authentication"
* For "Unauthenticated requests" prefer "HTTP 401: Unauthorized"

The following screenshot highlights these specific settings for a sample Azure function app.

![Configure authentication settings](./media/search-howto-managed-identities-azure-functions/function-app-authentication.png "Configure authentication settings")

### Add Microsoft Entra authentication provider

* Add Microsoft Entra as the authentication provider for the Azure function application.
* Either create a new app registration or choose a previously configured app registration. Ensure that it's configured according to the guidelines in the previous section of this document.
* Ensure that in the "Allowed token audiences" section, the application ID URI of the app registration is specified. It should be in the `api://<applicationId>` format, matching what was configured with the app registration created earlier.
* If you desire, you can configure additional checks to restrict access specifically to the indexer. 

![Add Microsoft Entra Authentication provider](./media/search-howto-managed-identities-azure-functions/identity-provider.png "Microsoft Entra Authentication provider")

### Configure additional checks

* Ensure that the Object (principal) ID of the specific Azure AI Search service's identity is specified as the **"Identity requirement"**, by checking the option "Allow requests from specific identities" and entering the Object (principal) ID in the "Identity blade"

![Search service identity](./media/search-howto-managed-identities-azure-functions/search-service-identity.png)

* In **"Client application requirement"** select the option "Allow requests from specific client application". You need to look up the Client ID for the Azure AI Search service's identity. To do this, copy over the Object (principal) ID from the previous step and look up in your Microsoft Entra tenant. There should be a matching "Enterprise Application" whose overview page lists an "Application ID", which is the GUID that needs to be specified as the client application requirement.

![Search service entra identity](./media/search-howto-managed-identities-azure-functions/search-identity-entra.png)

>[!NOTE]
> This step is the most important configuration on the Azure function app and doing it wrongly can result in the indexer being forbidden from accessing the function app. Ensure that you perform the lookup of the identity's enterprise application details correctly, and you specify the "Application ID" and "Object (principal) ID" in the right places.

* For the **"Tenant requirement"**, choose any of the options that aligns with your security posture. Check out the [Azure App service documentation](/azure/app-service/configure-authentication-provider-aad) for more details.

## Configure Custom Web API skill/vectorizer to connect to the Azure function application

For the Custom Web API skill/vectorizer to connect to the Azure function application and successfully authenticate with the configured Microsoft Entra authentication provider, ensure that you specify the correct URI to the function application and set the `authResourceId` to be the same value as the "Allowed token audience" configured for the authentication provider. 

### Using system assigned identity
Here's an example to call into a function call "test" for the sample Azure function application, where the system assigned identity of the search service is allowed to authenticate via "EasyAuth".

```json
"uri": "https://contoso-function-app.azurewebsites.net/api/test?",
"authResourceId": "api://00000000-0000-0000-0000-000000000000"
```

### Using user assigned identity

Here's an example to call into the same function, where the specific user assigned identity is allowed to authenticate via "EasyAuth".

```json
"uri": "https://contoso-function-app.azurewebsites.net/api/test?",
"authResourceId": "api://00000000-0000-0000-0000-000000000000",
"identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity": "/subscriptions/[subscription-id]/resourcegroups/[rg-name]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[my-user-managed-identity-name]" 
    }
```

>[!NOTE]
> This user assigned identity should actually be assigned to the Azure AI Search service for it to be specified in the Custom Web skill/vectorizer definition.

## Run the indexer/vectorizer to verify permissions

For Custom Web API skills, permissions are validated during indexer run-time. For vectorizer, they're validated when a vector query is issued utilizing the Custom Web API vectorizer. To rule out any specific issues with authentication, you can test by disabling the authentication provider on the function app and ensuring that calls from indexer/vectorizer succeed.

* If authentication issues persist, ensure that the right identity information - namely Application ID, Object (principal) ID for the Azure AI Search service's identity is specified in the function app's authentication provider.

## See also

* [Custom Web API skill](cognitive-search-custom-skill-web-api.md)
* [Custom Web API vectorizer](vector-search-vectorizer-custom-web-api.md)
