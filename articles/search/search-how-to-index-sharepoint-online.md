---
title: SharePoint in Microsoft 365 indexer (preview)
titleSuffix: Azure AI Search
description: Set up a SharePoint in Microsoft 365 indexer to automate indexing of document library content in Azure AI Search.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/28/2026
ms.custom:
  - ignite-2025
  - sfi-image-nochange
  - sfi-ropc-nochange
---

# Index data from SharePoint document libraries

> [!IMPORTANT]
> SharePoint in Microsoft 365 indexer support is in public preview. It's offered "as-is", under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and supported on best effort only. Preview features aren't recommended for production workloads and aren't guaranteed to become generally available.
>
> See [known limitations](#limitations-and-considerations) section before you start.
>
> [Fill out this form](https://aka.ms/azure-cognitive-search/indexer-preview) to register for the preview. All requests are approved automatically. After you fill out the form, use a [preview REST API](search-api-preview.md) to index your content. 

This article explains how to configure a [search indexer](search-indexer-overview.md) to index documents stored in SharePoint document libraries for full text search in Azure AI Search. Configuration steps are first, followed by behaviors and scenarios.

In Azure AI Search, an indexer extracts searchable data and metadata from a data source. The SharePoint in Microsoft 365 indexer provides the following functionality:

+ Indexes files and metadata from one or more document libraries.
+ Indexes incrementally, picking up just the new and changed files and metadata. 
+ Detects deleted content automatically. Document deletion in the library is picked up on the next indexer run, and the corresponding search document is removed from the index.
+ Extracts text and normalized images from indexed documents automatically. Optionally, you can add a [skillset](cognitive-search-working-with-skillsets.md) for deeper [AI enrichment](cognitive-search-concept-intro.md), such as optical character recognition (OCR) or entity recognition.
+ Supports document [basic Access Control Lists (ACL) ingestion](search-indexer-sharepoint-access-control-lists.md) in public preview during initial document sync. It also supports full data set incremental data sync.
+ Supports [Microsoft Purview sensitivity label ingestion and honoring at query time](search-indexer-sensitivity-labels.md). This functionality is in public preview.
  
## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), Basic pricing tier or higher.

+ [SharePoint in Microsoft 365](/sharepoint/introduction) cloud service (OneDrive isn't a supported data source).

+ Files in a [document library](https://support.microsoft.com/office/what-is-a-document-library-3b5976dd-65cf-4c9e-bf5a-713c10ca2872).

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for setting up and running the indexer pipeline.

## Supported document formats

The SharePoint in Microsoft 365 indexer can extract text from the following document formats:

[!INCLUDE [search-document-data-sources](./includes/search-blob-data-sources.md)]

## Limitations and considerations

Here are the limitations of this feature:

+ The indexer can index content from supported document formats in a document library. There's no indexer support for [SharePoint Lists](https://support.microsoft.com/office/introduction-to-lists-0a1c3ace-def0-44af-b225-cfa8d92c52d7), .ASPX site content, or OneNote notebook files. Furthermore, indexing sub-sites recursively from a specific site isn't supported.

+ Incremental indexing limitations:

  + Renaming a SharePoint folder breaks incremental indexing. A renamed folder is treated as new content.

  + Microsoft 365 processes that update SharePoint file system metadata can trigger incremental indexing, even if there are no other changes to content. Test your setup and check your document processing behaviors in Microsoft 365 platform before using the indexer or any AI enrichment.

+ Security limitations:

  + No support for [Private endpoint](search-indexer-howto-access-private.md). Secure network configuration must be enabled [via a firewall](service-configure-firewall.md).

  + No support for tenants with [Microsoft Entra ID Conditional Access](/entra/identity/conditional-access/overview) enabled.
    
  +  User-encrypted files and password-protected ZIP files aren't supported. However, encrypted content is allowed if it's protected by [Purview sensitivity labels](/purview/sensitivity-labels) and if the [configuration to preserve and honor those labels (preview)](search-indexer-sensitivity-labels.md) is enabled.

  + Limited support for document-level access permissions. A basic level of Access Control Lists (ACL) sync is currently in public preview. Review the [SharePoint ACL configuration documentation](search-indexer-sharepoint-access-control-lists.md) for details and setup.


Here are some considerations when using this feature:

+ To build a custom Copilot or Retrieval-Augmented Generation (RAG) app that interacts with SharePoint data using Azure AI Search, Microsoft recommends using the [SharePoint (Remote) Knowledge Source](agentic-knowledge-source-how-to-sharepoint-remote.md). This knowledge source uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) to query textual content directly from SharePoint in Microsoft 365, returning results to the agentic retrieval engine for merging, ranking, and response formulation. There's no search index used by this knowledge source, and only textual content is queried. Azure AI Search doesn't replicate data. It enforces the SharePoint permission model by returning only the results that each user is authorized to see.

+ If you need to create a custom Copilot / RAG (Retrieval Augmented Generation) application or AI agent to chat with SharePoint data in production environments, consider first building it directly via [Microsoft Copilot Studio](/microsoft-copilot-studio/knowledge-add-sharepoint).

+ If you still need a custom copilot / RAG application or agent indexing data from SharePoint in Azure AI Search in a production environment, despite the recommendation to use Copilot Studio, consider:

  + Creating a custom connector with [SharePoint Webhooks](/sharepoint/dev/apis/webhooks/overview-sharepoint-webhooks), calling [Microsoft Graph API](/graph/use-the-api) to export the data to an Azure Blob container, and then use the [Azure blob indexer](search-how-to-index-azure-blob-storage.md) for incremental indexing.

  + Creating your own [Azure Logic Apps workflow](/azure/logic-apps/logic-apps-overview) using [Azure Logic Apps SharePoint connector](/connectors/sharepointonline/) and [Azure AI Search connector](/connectors/azureaisearch/) when reaching General Availability. You can use the workflow generated by the [Azure portal wizard](search-how-to-index-logic-apps.md) as a starting point and then customize it in the [Azure Logic Apps designer](/azure/logic-apps/quickstart-create-example-consumption-workflow#add-the-trigger) to include the transformation steps you need. The Azure Logic App workflow created when using the [Azure AI Search wizard](search-how-to-index-logic-apps.md) to index SharePoint in Microsoft 365 data is a [consumption workflow](/azure/logic-apps/logic-apps-overview#key-terms). When setting up production workloads, switch to a [standard logic app workflow](/azure/logic-apps/logic-apps-overview#key-terms) to use its extra enterprise features.
  
Regardless of the approach you choose, whether building a custom connector with SharePoint hooks or creating an Azure Logic Apps workflow, be sure to implement robust security measures. These measures include configuring shared private links, setting up firewalls, preserving user permissions from the source and honor those permissions at query time, among others. You should also regularly audit and monitor your pipeline.

## Configure the SharePoint in Microsoft 365 indexer

To set up the SharePoint in Microsoft 365 indexer, use a preview REST API. This section provides the steps. 

### Step 1 (Optional): Enable system assigned managed identity

Enable a [system-assigned managed identity](search-how-to-managed-identities.md#create-a-system-managed-identity) to automatically detect the tenant in which the search service is provisioned. 

Perform this step if the SharePoint site is in the same tenant as the search service. Skip this step if the SharePoint site is in a different tenant. The identity is used for tenant detection. You can also skip this step if you want to put the tenant ID in the [connection string](#connection-string-format). If you would like to use the system-managed identity or configure a user-assigned managed identity for secretless indexing, configure the [application permissions with secretless authentication](#using-secretless-authentication-to-obtain-application-tokens)

:::image type="content" source="media/search-howto-index-sharepoint-online/enable-managed-identity.png" alt-text="Screenshot showing how to enable system assigned managed identity.":::

After selecting **Save**, you receive an Object ID assigned to your search service.

<!-- Replace this with a new image without GUID
:::image type="content" source="media/search-howto-index-sharepoint-online/system-assigned-managed-identity.png" alt-text="Screenshot the object identifier."::: -->

### Step 2: Decide which permissions the indexer requires

The SharePoint in Microsoft 365 indexer supports both [delegated and application](/graph/auth/auth-concepts#delegated-and-application-permissions) permissions. Choose which permissions you want to use based on your scenario.

We recommend app-based permissions. See [limitations](#limitations-and-considerations) for known issues related to delegated permissions.

+ Application permissions (recommended), where the indexer runs under the [identity of the SharePoint tenant](/sharepoint/dev/solution-guidance/security-apponly-azureacs) with access to all sites and files. The indexer requires a [client secret](/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow). The indexer also requires [tenant admin approval](/azure/active-directory/manage-apps/grant-admin-consent) before it can index content. This permission type is the only one that supports basic [ACL preservation (preview)](search-indexer-sharepoint-access-control-lists.md) configuration. Delegated permissions can't be used for ACL sync.

+ Delegated permissions, where the indexer runs under the identity of the user or app sending the request. Data access is limited to the sites and files to which the caller has access. To support delegated permissions, the indexer requires a [device code prompt](/azure/active-directory/develop/v2-oauth2-device-code) to sign in on behalf of the user. User-delegated permissions enforce token expiration every 75 minutes, per the most recent security libraries used to implement this authentication type. This isn't a behavior that can be adjusted. An expired token requires manual indexing using [Run Indexer (preview)](/rest/api/searchservice/indexers/run?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true). For this reason, you should use app-based permissions instead. This configuration is only recommended for small testing operations, due to token expiration period and since this permission type doesn't support any level of [ACL preservation](search-indexer-sharepoint-access-control-lists.md) configuration.

<a name='step-3-create-an-azure-ad-application'></a>

### Step 3: Create a Microsoft Entra application registration

The SharePoint in Microsoft 365 indexer uses a Microsoft Entra application for authentication. Create the application registration in the same tenant as Azure AI Search.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Search for or navigate to **Microsoft Entra ID**, then select **Add** > **App registrations**. 

1. Select **+ New registration**:
    1. Provide a name for your app.
    1. Select **Single tenant**.
    1. Skip the URI designation step. No redirect URI required.
    1. Select **Register**.

1. On the navigation pane under **Manage**, select **API permissions**, then **Add a permission**, then **Microsoft Graph**.

    + If your indexer uses application API permissions, choose **Application** permissions.
      - For standard indexing, select:
        `Sites.Read.All`

      - If you're enabling content indexing and [basic ACL sync (preview)](search-indexer-sharepoint-access-control-lists.md), select:
        `Sites.FullControl.All` (instead of Sites.Read.All)

      - If you need to enable content indexing and limit [ACL sync (preview)](search-indexer-sharepoint-access-control-lists.md) to specific sites, select:
        `Sites.Selected`
         Then grant the application full control only for those selected sites.

      
      :::image type="content" source="media/search-howto-index-sharepoint-online/application-api-permissions.png" alt-text="Screenshot of application API permissions." lightbox="media/search-howto-index-sharepoint-online/application-api-permissions.png":::

      Using application permissions means that the indexer accesses the SharePoint site in a service context. So when you run the indexer, it has access to all content in the SharePoint tenant, which requires tenant admin approval. A client secret or secretless configuration is also required for authentication. Setting up the authentication mechanism is described later in this article under [authentication modes for application API permissions only](#available-authentication-methods-for-application-api-permissions-only).

    + If the indexer is using delegated API permissions, select **Delegated permissions** and then select `Delegated - Files.Read.All`, `Delegated - Sites.Read.All`, and `Delegated - User.Read`.

      <!-- RESTORE THIS SCREENSHOT -->
      :::image type="content" source="media/search-howto-index-sharepoint-online/delegated-api-permissions.png" alt-text="Screenshot showing delegated API permissions." lightbox="media/search-howto-index-sharepoint-online/delegated-api-permissions.png":::

      Delegated permissions allow the search client to connect to SharePoint under the security identity of the current user.

1. Give admin consent.

    Tenant admin consent is required when using application API permissions. Some tenants are locked down in such a way that tenant admin consent is required for delegated API permissions as well. If either of these conditions apply, you'll need to have a tenant admin grant consent for this Microsoft Entra application before creating the indexer.

    <!-- RESTORE THIS SCREENSHOT -->
    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-grant-admin-consent.png" alt-text="Screenshot showing Microsoft Entra app grant admin consent." lightbox="media/search-howto-index-sharepoint-online/aad-app-grant-admin-consent.png":::

1. Select the **Authentication** tab.

1. Set **Allow public client flows** to **Yes** then select **Save**.

1. Select **+ Add a platform**, then **Mobile and desktop applications**, then check `https://login.microsoftonline.com/common/oauth2/nativeclient`, then **Configure**.

    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-authentication-configuration.png" alt-text="Screenshot showing Microsoft Entra app authentication configuration." lightbox="media/search-howto-index-sharepoint-online/aad-app-authentication-configuration.png" :::

1. Configure the indexer [authentication method](#available-authentication-methods-for-application-api-permissions-only) according to your solution needs.

#### Available authentication methods for application API permissions only

To authenticate the Microsoft Entra application with application permissions, the indexer uses either a client secret or a secretless configuration.

##### Using client secret

These are the instructions to configure the application to use a client secret to authenticate the indexer, so it can ingest data from SharePoint.

  + Select **Certificates & Secrets** from the menu on the left, then **Client secrets**, then **New client secret**.

      :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret.png" alt-text="Screenshot showing new client secret." lightbox="media/search-howto-index-sharepoint-online/application-client-secret.png" :::

  + In the menu that pops up, enter a description for the new client secret. Adjust the expiration date if necessary. If the secret expires, it needs to be recreated and the indexer needs to be updated with the new secret.

      :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret-setup.png" alt-text="Screenshot showing how to set up a client secret." lightbox="media/search-howto-index-sharepoint-online/application-client-secret-setup.png":::

  + The new client secret appears in the secret list. Once you navigate away from the page, the secret is no longer be visible, so copy the value using the copy button and save it in a secure location.

       :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret-copy.png" alt-text="Screenshot showing where to copy a client secret.":::

##### Using secretless authentication to obtain application tokens

These are the instructions to configure the application so Microsoft Entra trusts a managed identity to obtain an application token to authenticate without a client secret, so the indexer can ingest data from SharePoint.

###### Configuring the registered application with a managed identity

1. Create (or select) a [user-assigned managed identity and assign to your search service](search-how-to-managed-identities.md#create-a-user-assigned-managed-identity) or a [system-assigned managed identity](search-how-to-managed-identities.md#create-a-system-managed-identity), depending on your scenario requirements.
   
1. Capture the **object (principal) ID**. This will be used as part of the credentials configuration when creating the data source.
    <!-- GIA TO ADD THIS SCREENSHOT OF UAMI OBJECT PRINCIPAL --> 
    <!-- GIA TO ADD THIS SCREENSHOT OF SAMI OBJECT PRINCIPAL -->
   
1. Select **Certificates & Secrets** from the menu on the left.
      <!-- GIA TO ADD THIS SCREENSHOT -->

1. Under **Federated credentials** select **+ Add a credential**.

      <!-- GIA TO ADD THIS SCREENSHOT -->

1. Under **Federated credential scenario** select **Managed Identity**. 

    <!-- GIA TO ADD THIS SCREENSHOT OF SAMI OBJECT PRINCIPAL -->

1. Select managed identity: Choose the created managed identity created as part of step 1.

    <!-- GIA TO ADD THIS SCREENSHOT OF UAMI SELECTION --> 
    <!-- GIA TO ADD THIS SCREENSHOT OF SAMI SELECTION -->

1. Add a name for your credential and click on **Save**.

<a name="create-data-source"></a>

### Step 4: Create data source

Starting in this section, use the latest preview REST API and a REST client or the latest supported beta SDK of your preference for the remaining steps.

A data source specifies which data to index, credentials, and policies to efficiently identify changes in the data (new, modified, or deleted rows). Multiple indexers in the same search service can use the same data source.

For SharePoint indexing, the data source must have the following required properties:

+ **name** is the unique name of the data source within your search service.
+ **type** must be "sharepoint". This value is case-sensitive.
+ **credentials** provide the SharePoint endpoint and the authentication method allowed for the application to request the Microsoft Entra tokens. An example SharePoint endpoint is `https://microsoft.sharepoint.com/teams/MySharePointSite`. You can get the endpoint by navigating to the home page of your SharePoint site and copying the URL from the browser. Review the [connection string format](#connection-string-format) for the supported syntax.
+ **container** specifies which document library to index. Properties [control which documents are indexed](#controlling-which-documents-are-indexed).

To create a data source, call [Create Data Source (preview)](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

Here's a data source definition sample for credentials with application secret or service-assigned managed identity.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sharepoint-datasource",
    "type" : "sharepoint",
    "credentials" : { "connectionString" : "[connection-string]" },
    "container" : { "name" : "defaultSiteLibrary", "query" : null }
}
```

Here's a data source definition sample for credentials with user-assigned managed identity.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sharepoint-datasource",
    "type" : "sharepoint",
    "credentials" : { "connectionString" : "[connection-string]" },
    "container" : { "name" : "defaultSiteLibrary", "query" : null },
    "identity": {
      "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
      "userAssignedIdentity": "/subscriptions/[Azure subscription ID]/resourceGroups/[resource-group]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[user-assigned managed identity]"
    }
}
```

#### Connection string format

The format of the connection string changes based on whether the indexer is using delegated API permissions or application API permissions.

+ Delegated API permissions connection string format

    `SharePointOnlineEndpoint=[SharePoint site url];ApplicationId=[Azure AD App ID];TenantId=[SharePoint site tenant id]`

+ Application API permissions with application secret connection string format

    `SharePointOnlineEndpoint=[SharePoint site url];ApplicationId=[Azure AD App ID];ApplicationSecret=[Azure AD App client secret];TenantId=[SharePoint site tenant id]`

+ Application API permissions with secretless (system-assigned managed identity) connection string format

    `SharePointOnlineEndpoint=[SharePoint site url];ApplicationId=[Azure AD App ID];FederatedCredentialObjectId=[selected managed identity object (principal) ID];TenantId=[SharePoint site tenant id]`

You can get `tenantId` from the overview page in the Microsoft Entra admin center in your Microsoft 365 subscription.
You can get the managed identity `object (principal) ID` from the section [Configuring the registered application with a managed identity](#configuring-the-registered-application-with-a-managed-identity)

> [!NOTE]
> If the SharePoint site is in the same tenant as the search service and system-assigned managed identity is enabled, `TenantId` doesn't have to be included in the connection string. If the SharePoint site is in a different tenant from the search service, `TenantId` must be included.
>

If your indexer uses [SharePoint ACL configuration (preview)](search-indexer-sharepoint-access-control-lists.md) or [preserves and honors Microsoft Purview sensitivity labels (preview)](search-indexer-sensitivity-labels.md), review the related articles for data source setup before creating the indexer. Each feature has specific configuration steps.


### Step 5: Create an index

The index specifies the fields in a document, attributes, and other constructs that shape the search experience.

To create an index, call [Create Index (preview)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true):

```http
POST https://[service name].search.windows.net/indexes?api-version=2025-11-01-preview
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sharepoint-index",
    "fields": [
        { "name": "id", "type": "Edm.String", "key": true, "searchable": false },
        { "name": "metadata_spo_item_name", "type": "Edm.String", "key": false, "searchable": true, "filterable": false, "sortable": false, "facetable": false },
        { "name": "metadata_spo_item_path", "type": "Edm.String", "key": false, "searchable": false, "filterable": false, "sortable": false, "facetable": false },
        { "name": "metadata_spo_item_content_type", "type": "Edm.String", "key": false, "searchable": false, "filterable": true, "sortable": false, "facetable": true },
        { "name": "metadata_spo_item_last_modified", "type": "Edm.DateTimeOffset", "key": false, "searchable": false, "filterable": false, "sortable": true, "facetable": false },
        { "name": "metadata_spo_item_size", "type": "Edm.Int64", "key": false, "searchable": false, "filterable": false, "sortable": false, "facetable": false },
        { "name": "content", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false }
    ]
}

```

> [!IMPORTANT]
> Only [`metadata_spo_site_library_item_id`](#metadata) may be used as the key field in an index populated by the SharePoint in Microsoft 365 indexer. If a key field doesn't exist in the data source, `metadata_spo_site_library_item_id` is automatically mapped to the key field.

If your indexer will use either [SharePoint ACL configuration (preview)](search-indexer-sharepoint-access-control-lists.md) or will [preserve and honor Microsoft Purview sensitivity labels (preview)](search-indexer-sensitivity-labels.md), review each article for index and skillset configuration before proceeding with indexer creation since those functionalities have specific configurations.

### Step 6: Create an indexer

An indexer connects a data source with a target search index and provides a schedule to automate the data refresh. Once the index and data source are created, you can create the indexer.

If you're using delegated permissions, during this step, you're asked to sign in with organization credentials that have access to the SharePoint site. If possible, we recommend creating a new organizational user account and giving that new user the exact permissions that you want the indexer to have. 

There are a few steps to creating the indexer:

1. Send a [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) request:

    ```http
    POST https://[service name].search.windows.net/indexers?api-version=2025-11-01-preview
    Content-Type: application/json
    api-key: [admin key]
    
    {
        "name" : "sharepoint-indexer",
        "dataSourceName" : "sharepoint-datasource",
        "targetIndexName" : "sharepoint-index",
        "parameters": {
        "batchSize": null,
        "maxFailedItems": null,
        "base64EncodeKeys": null,
        "maxFailedItemsPerBatch": null,
        "configuration": {
            "indexedFileNameExtensions" : ".pdf, .docx",
            "excludedFileNameExtensions" : ".png, .jpg",
            "dataToExtract": "contentAndMetadata"
          }
        },
        "schedule" : { },
        "fieldMappings" : [
            { 
              "sourceFieldName" : "metadata_spo_site_library_item_id", 
              "targetFieldName" : "id", 
              "mappingFunction" : { 
                "name" : "base64Encode" 
              } 
             }
        ]
    }
    ```

    If you're using application permissions, it's necessary to wait until the initial run is complete before starting to query your index. The following instructions provided in this step pertain specifically to delegated permissions, and aren't applicable to application permissions.

1. When you create the indexer for the first time, the [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) request waits until you complete the next step. You must call [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) to get the link and enter your new device code. 

    ```http
    GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2025-11-01-preview
    Content-Type: application/json
    api-key: [admin key]
    ```

    If you don't run the [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) within 10 minutes, the code expires and you'll need to recreate the [data source](#create-data-source).

1. Copy the device login code from the [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) response. The device login can be found in the "errorMessage".

    ```http
    {
        "lastResult": {
            "status": "transientFailure",
            "errorMessage": "To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code <CODE> to authenticate."
        }
    }
    ```

1. Provide the code that was included in the error message.

    :::image type="content" source="media/search-howto-index-sharepoint-online/enter-device-code.png" alt-text="Screenshot showing how to enter a device code.":::

1. The SharePoint in Microsoft 365 indexer will access the SharePoint content as the signed-in user. The user that logs in during this step will be that signed-in user. So, if you sign in with a user account that doesn't have access to a document in the Document Library that you want to index, the indexer won't have access to that document.

    If possible, we recommend creating a new user account and giving that new user the exact permissions that you want the indexer to have.

1. Approve the permissions that are being requested.

    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-approve-api-permissions.png" alt-text="Screenshot showing how to approve API permissions.":::

1. The [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) initial request completes if all the permissions provided above are correct and within the 10 minute timeframe.

> [!NOTE]
> If the Microsoft Entra application requires admin approval and was not approved before logging in, you may see the following screen. [Admin approval](/azure/active-directory/manage-apps/grant-admin-consent) is required to continue.
:::image type="content" source="media/search-howto-index-sharepoint-online/no-admin-approval-error.png" alt-text="Screenshot showing admin approval required.":::

### Step 7: Check the indexer status

After the indexer has been created, you can call [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true):

```http
GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2025-11-01-preview
Content-Type: application/json
api-key: [admin key]
```

## Updating the data source

If there are no updates to the data source object, the indexer runs on a schedule without any user interaction. 

If you change the data source while the device code is expired, sign in again to run the indexer. For example, if you change the data source query, sign in again using the `https://microsoft.com/devicelogin` and get the new device code.

Here are the steps for updating a data source, assuming an expired device code:

1. Call [Run Indexer (preview)](/rest/api/searchservice/indexers/run?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true) to manually start [indexer execution](search-howto-run-reset-indexers.md).

    ```http
    POST https://[service name].search.windows.net/indexers/sharepoint-indexer/run?api-version=2025-11-01-preview  
    Content-Type: application/json
    api-key: [admin key]
    ```

1. Check the [indexer status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2025-11-01-preview&tabs=HTTP&preserve-view=true). 

    ```http
    GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2025-11-01-preview
    Content-Type: application/json
    api-key: [admin key]
    ```

1. If you get an error asking you to visit `https://microsoft.com/devicelogin`, open the page and copy the new code. 

1. Paste the code into the dialog box.

1. Manually run the indexer again and check the indexer status. This time, the indexer run should successfully start.

<a name="metadata"></a>

## Indexing document metadata

If you're indexing document metadata (`"dataToExtract": "contentAndMetadata"`), the following metadata is available to index.

| Identifier | Type | Description | 
| ------------- | -------------- | ----------- |
| metadata_spo_site_library_item_id | Edm.String | The combination key of site ID, library ID, and item ID, which uniquely identifies an item in a document library for a site. |
| metadata_spo_site_id | Edm.String | The ID of the SharePoint site. |
| metadata_spo_library_id | Edm.String | The ID of document library. |
| metadata_spo_item_id | Edm.String | The ID of the (document) item in the library. |
| metadata_spo_item_last_modified | Edm.DateTimeOffset | The last modified date/time (UTC) of the item. |
| metadata_spo_item_name | Edm.String | The name of the item. |
| metadata_spo_item_size | Edm.Int64 | The size (in bytes) of the item. | 
| metadata_spo_item_content_type | Edm.String | The content type of the item. | 
| metadata_spo_item_extension | Edm.String | The extension of the item. |
| metadata_spo_item_weburi | Edm.String | The URI of the item. |
| metadata_spo_item_path | Edm.String | The combination of the parent path and item name. | 

The SharePoint in Microsoft 365 indexer also supports metadata specific to each document type. More information can be found in [Content metadata properties used in Azure AI Search](search-blob-metadata-properties.md).

> [!NOTE]
> To index custom metadata, "additionalColumns" must be specified in the [query parameter of the data source](#query).

## Include or exclude by file type

You can control which files are indexed by setting inclusion and exclusion criteria in the "parameters" section of the indexer definition.

Include specific file extensions by setting `"indexedFileNameExtensions"` to a comma-separated list of file extensions (with a leading dot). Exclude specific file extensions by setting `"excludedFileNameExtensions"` to the extensions that should be skipped. If the same extension is in both lists, it's excluded from indexing.

```http
PUT /indexers/[indexer name]?api-version=2025-11-01-preview
{
    "parameters" : { 
        "configuration" : { 
            "indexedFileNameExtensions" : ".pdf, .docx",
            "excludedFileNameExtensions" : ".png, .jpeg" 
        } 
    }
}
```

<a name="controlling-which-documents-are-indexed"></a>

## Controlling which documents are indexed

A single SharePoint in Microsoft 365 indexer can index content from one or more document libraries. To specify which sites and document libraries to index, use the "container" parameter in the data source definition.

The [data source "container" section](#create-data-source) has two properties for this task: "name" and "query".

### Name

The "name" property is required and must be one of three values:

| Value | Description |
|-|-|
| defaultSiteLibrary | Index all content from the site's default document library. |
| allSiteLibraries | Index all content from all document libraries in a site. Document libraries from a subsite are out of scope/ If you need content from subsites, choose "useQuery" and specify "includeLibrariesInSite". |
| useQuery | Only index the content defined in the "query". |

<a name="query"></a>

### Query

The "query" parameter of the data source is made up of keyword/value pairs. The below are the keywords that can be used. The values are either site URLs or document library URLs.

> [!NOTE]
> To get the value for a particular keyword, we recommend navigating to the document library that you're trying to include/exclude and copying the URI from the browser. This is the easiest way to get the value to use with a keyword in the query.

| Keyword | Value description and examples |
| ------- | ------------------------ |
| null | If null or empty, index either the default document library or all document libraries depending on the container name.	<br><br>Example: <br><br>``` "container" : { "name" : "defaultSiteLibrary", "query" : null } ``` |
| includeLibrariesInSite | Index content from all libraries under the specified site in the connection string. The value should be the URI of the site or subsite. <br><br>Example 1: <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/mysite" }``` <br><br>Example 2 (include a few subsites only): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/sites/TopSite/SubSite1;includeLibrariesInSite=https://mycompany.sharepoint.com/sites/TopSite/SubSite2" }``` |
| includeLibrary | Index all content from this library. The value is the fully qualified path to the library, which can be copied from your browser: <br><br>Example 1 (fully qualified path): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/mysite/MyDocumentLibrary" }``` <br><br>Example 2 (URI copied from your browser): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx" }``` |
| excludeLibrary | Don't index content from this library. The value is the fully qualified path to the library, which can be copied from your browser: <br><br> Example 1 (fully qualified path): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mysite.sharepoint.com/subsite1; excludeLibrary=https://mysite.sharepoint.com/subsite1/MyDocumentLibrary" }``` <br><br> Example 2 (URI copied from your browser): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/teams/mysite; excludeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx" }``` |
| additionalColumns | Index columns from the document library. The value is a comma-separated list of column names you want to index. Use a double backslash to escape semicolons and commas in column names: <br><br> Example 1 (additionalColumns=MyCustomColumn,MyCustomColumn2):  <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/mysite/MyDocumentLibrary;additionalColumns=MyCustomColumn,MyCustomColumn2" }``` <br><br> Example 2 (escape characters using double backslash): <br><br> ```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx;additionalColumns=MyCustomColumnWith\\,,MyCustomColumnWith\\;" }``` |

## Handling errors

By default, the SharePoint in Microsoft 365 indexer stops as soon as it encounters a document with an unsupported content type (for example, an image). You can use the `excludedFileNameExtensions` parameter to skip certain content types. However, you might need to index documents without knowing all the possible content types in advance. To continue indexing when an unsupported content type is encountered, set the `failOnUnsupportedContentType` configuration parameter to false:

```http
PUT https://[service name].search.windows.net/indexers/[indexer name]?api-version=2025-11-01-preview
Content-Type: application/json
api-key: [admin key]

{
    ... other parts of indexer definition
    "parameters" : { "configuration" : { "failOnUnsupportedContentType" : false } }
}
```

For some documents, Azure AI Search is unable to determine the content type, or unable to process a document of otherwise supported content type. To ignore this failure mode, set the `failOnUnprocessableDocument` configuration parameter to false:

```http
"parameters" : { "configuration" : { "failOnUnprocessableDocument" : false } }
```

Azure AI Search limits the size of documents that are indexed. These limits are documented in [Service Limits in Azure AI Search](./search-limits-quotas-capacity.md). Oversized documents are treated as errors by default. However, you can still index storage metadata of oversized documents if you set `indexStorageMetadataOnlyForOversizedDocuments` configuration parameter to true:

```http
"parameters" : { "configuration" : { "indexStorageMetadataOnlyForOversizedDocuments" : true } }
```

You can also continue indexing if errors happen at any point of processing, either while parsing documents or while adding documents to an index. To ignore a specific number of errors, set the `maxFailedItems` and `maxFailedItemsPerBatch` configuration parameters to the desired values. For example:

```http
{
    ... other parts of indexer definition
    "parameters" : { "maxFailedItems" : 10, "maxFailedItemsPerBatch" : 10 }
}
```

If a file on the SharePoint site has encryption enabled, you might see the following error message:
 
```
Code: resourceModified Message: The resource has changed since the caller last read it; usually an eTag mismatch Inner error: Code: irmEncryptFailedToFindProtector
```

The error message will also include the SharePoint site ID, drive ID, and drive item ID in the following pattern: `<sharepoint site id> :: <drive id> :: <drive item id>`. This information can be used to identify which item is failing on the SharePoint end. The user can then remove the encryption from the item to resolve the issue.

## See also

+ [YouTube video: SharePoint in Microsoft 365 indexer](https://www.youtube.com/watch?v=QmG65Vgl0JI)
+ [Indexers in Azure AI Search](search-indexer-overview.md)
+ [Content metadata properties used in Azure AI Search](search-blob-metadata-properties.md)
+ [Index SharePoint content and other sources in Azure AI Search using Azure Logic App connectors](search-how-to-index-logic-apps.md)
+ [Ingest SharePoint ACL configuration (preview)](search-indexer-sharepoint-access-control-lists.md)
+ [Preserve and honor Microsoft Purview sensitivity labels (preview)](search-indexer-sensitivity-labels.md)
