---
title: SharePoint Online indexer (preview)
titleSuffix: Azure AI Search
description: Set up a SharePoint Online indexer to automate indexing of document library content in Azure AI Search.
author: gmndrg
ms.author: gimondra

ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 08/20/2024
---

# Index data from SharePoint document libraries

> [!IMPORTANT]
> SharePoint Online indexer support is in public preview. It's offered "as-is", under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and supported on best effort only. Preview features aren't recommended for production workloads and aren't guaranteed to become generally available.
>
> Be sure to visit the [known limitations](#limitations-and-considerations) section before you start.
>
>To use this preview, [fill out this form](https://aka.ms/azure-cognitive-search/indexer-preview). You won't be receiving any approval notification right after since any access request is automatically accepted after submission. After access is enabled, use a [preview REST API](search-api-preview.md) to index your content. 

This article explains how to configure a [search indexer](search-indexer-overview.md) to index documents stored in SharePoint document libraries for full text search in Azure AI Search. Configuration steps are first, followed by behaviors and scenarios

## Functionality

An indexer in Azure AI Search is a crawler that extracts searchable data and metadata from a data source. The SharePoint Online indexer connects to your SharePoint site and indexes documents from one or more document libraries. The indexer provides the following functionality:

+ Index files and metadata from one or more document libraries.
+ Index incrementally, picking up just the new and changed files and metadata. 
+ Deletion detection is built in. Deletion in a document library is picked up on the next indexer run, and the document is removed from the index.
+ Text and normalized images are extracted by default from the documents that are indexed. Optionally, you can add a [skillset](cognitive-search-working-with-skillsets.md) for deeper [AI enrichment](cognitive-search-concept-intro.md), like OCR or text translation. 

## Prerequisites

+ [SharePoint in Microsoft 365](/sharepoint/introduction) cloud service

+ Files in a [document library](https://support.microsoft.com/office/what-is-a-document-library-3b5976dd-65cf-4c9e-bf5a-713c10ca2872)

## Supported document formats

The SharePoint Online indexer can extract text from the following document formats:

[!INCLUDE [search-document-data-sources](./includes/search-blob-data-sources.md)]

## Limitations and considerations

Here are the limitations of this feature:

+ Indexing [SharePoint Lists](https://support.microsoft.com/office/introduction-to-lists-0a1c3ace-def0-44af-b225-cfa8d92c52d7) isn't supported.

+ Indexing SharePoint .ASPX site content isn't supported.

+ OneNote notebook files aren't supported.

+ [Private endpoint](search-indexer-howto-access-private.md) isn't supported.

+ Renaming a SharePoint folder doesn't trigger incremental indexing. A renamed folder is treated as new content.

+ SharePoint supports a granular authorization model that determines per-user access at the document level. The indexer doesn't pull these permissions into the index, and Azure AI Search doesn't support document-level authorization. When a document is indexed from SharePoint into a search service, the content is available to anyone who has read access to the index. If you require document-level permissions, you should consider [security filters to trim results](search-security-trimming-for-azure-search.md) and automate copying the permissions at a file level to a field in the index.

+ Indexing user-encrypted files, Information Rights Management (IRM) protected files, ZIP files with passwords or similar encrypted content isn't supported. For encrypted content to be processed, the user with proper permissions to the specific file must remove the encryption so the item can be indexed accordingly when the indexer runs the next scheduled iteration.

+ Indexing sub-sites recursively from a specific site provided isn't supported.

+ SharePoint Online indexer isn't supported when [Microsoft Entra ID Conditional Access](/entra/identity/conditional-access/overview) is enabled.

Here are the considerations when using this feature:

+ If you need to create a custom Copilot / RAG (Retrieval Augmented Generation) application to chat with SharePoint data, the recommended approach is to use [Microsoft Copilot Studio](https://www.microsoft.com/microsoft-copilot/microsoft-copilot-studio) instead of this preview feature. 

+ If you need a SharePoint content indexing solution in a production environment, consider creating a custom connector with [SharePoint Webhooks](/sharepoint/dev/apis/webhooks/overview-sharepoint-webhooks), calling [Microsoft Graph API](/graph/use-the-api) to export the data to an Azure Blob container, and then use the [Azure blob indexer](search-howto-indexing-azure-blob-storage.md) for incremental indexing.

<!-- + There could be Microsoft 365 processes that update SharePoint file system-metadata (based on different configurations in SharePoint) and will cause the SharePoint Online indexer to trigger. Make sure that you test your setup and understand the document processing count prior to using any AI enrichment. Since this is a third-party connector to Azure (SharePoint is located in Microsoft 365), SharePoint configuration is not checked by the indexer. -->

+ If your SharePoint configuration allows Microsoft 365 processes to update SharePoint file system metadata, be aware that these updates can trigger the SharePoint Online indexer, causing the indexer to ingest documents multiple times. Because the SharePoint Online indexer is a non-Microsoft connector to Azure, the indexer can't read the configuration or vary its behavior. It responds to changes in new and changed content, regardless of how those updates are made. For this reason, make sure that you test your setup and understand the document processing count prior to using the indexer and any AI enrichment.




## Configure the SharePoint Online indexer

To set up the SharePoint Online indexer, use both the Azure portal and a preview REST API. You can use 2020-06-30-preview or later. We recommend the latest preview API.

This section provides the steps. You can also watch the following video.
 
> [!VIDEO https://www.youtube.com/embed/QmG65Vgl0JI]

### Step 1 (Optional): Enable system assigned managed identity

Enable a [system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) to automatically detect the tenant the search service is provisioned in. 

Perform this step if the SharePoint site is in the same tenant as the search service. Skip this step if the SharePoint site is in a different tenant. The identity isn't used for indexing, just tenant detection. You can also skip this step if you want to put the tenant ID in the [connection string](#connection-string-format).

:::image type="content" source="media/search-howto-index-sharepoint-online/enable-managed-identity.png" alt-text="Screenshot showing how to enable system assigned managed identity.":::

After selecting **Save**, you get an Object ID that has been assigned to your search service.

:::image type="content" source="media/search-howto-index-sharepoint-online/system-assigned-managed-identity.png" alt-text="Screenshot the object identifier.":::

### Step 2: Decide which permissions the indexer requires

The SharePoint Online indexer supports both [delegated and application](/graph/auth/auth-concepts#delegated-and-application-permissions) permissions. Choose which permissions you want to use based on your scenario.

We recommend app-based permissions. See [limitations](#limitations-and-considerations) for known issues related to delegated permissions.

+ Application permissions (recommended), where the indexer runs under the [identity of the SharePoint tenant](/sharepoint/dev/solution-guidance/security-apponly-azureacs) with access to all sites and files. The indexer requires a [client secret](/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow). The indexer will also require [tenant admin approval](/azure/active-directory/manage-apps/grant-admin-consent) before it can index any content.

+ Delegated permissions, where the indexer runs under the identity of the user or app sending the request. Data access is limited to the sites and files to which the caller has access. To support delegated permissions, the indexer requires a [device code prompt](/azure/active-directory/develop/v2-oauth2-device-code) to sign in on behalf of the user. User-delegated permissions enforce token expiration every 75 minutes, per the most recent security libraries used to implement this authentication type. This isn't a behavior that can be adjusted. An expired token requires manual indexing using [Run Indexer (preview)](/rest/api/searchservice/indexers/run?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true). For this reason, you might want app-based permissions instead.


<a name='step-3-create-an-azure-ad-application'></a>

### Step 3: Create a Microsoft Entra application registration

The SharePoint Online indexer uses this Microsoft Entra application for authentication.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Search for or navigate to **Microsoft Entra ID**, then select **App registrations**. 

1. Select **+ New registration**:
    1. Provide a name for your app.
    1. Select **Single tenant**.
    1. Skip the URI designation step. No redirect URI required.
    1. Select **Register**.

1. On the left, select **API permissions**, then **Add a permission**, then **Microsoft Graph**.

    + If the indexer is using application API permissions, then select **Application permissions** and add the following:

        + **Application - Files.Read.All**
        + **Application - Sites.Read.All**
        
        :::image type="content" source="media/search-howto-index-sharepoint-online/application-api-permissions.png" alt-text="Screenshot of application API permissions.":::
        
        Using application permissions means that the indexer accesses the SharePoint site in a service context. So when you run the indexer it will have access to all content in the SharePoint tenant, which requires tenant admin approval. A client secret is also required for authentication. Setting up the client secret is described later in this article.

    + If the indexer is using delegated API permissions, select **Delegated permissions** and add the following:

        + **Delegated - Files.Read.All**
        + **Delegated - Sites.Read.All**
        + **Delegated - User.Read**
        
        :::image type="content" source="media/search-howto-index-sharepoint-online/delegated-api-permissions.png" alt-text="Screenshot showing delegated API permissions.":::
        
        Delegated permissions allow the search client to connect to SharePoint under the security identity of the current user.

1. Give admin consent.

    Tenant admin consent is required when using application API permissions. Some tenants are locked down in such a way that tenant admin consent is required for delegated API permissions as well. If either of these conditions apply, you’ll need to have a tenant admin grant consent for this Microsoft Entra application before creating the indexer.

    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-grant-admin-consent.png" alt-text="Screenshot showing Microsoft Entra app grant admin consent.":::

1. Select the **Authentication** tab. 

1. Set **Allow public client flows** to **Yes** then select **Save**.

1. Select **+ Add a platform**, then **Mobile and desktop applications**, then check `https://login.microsoftonline.com/common/oauth2/nativeclient`, then **Configure**.

    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-authentication-configuration.png" alt-text="Screenshot showing Microsoft Entra app authentication configuration.":::

1. (Application API Permissions only) To authenticate to the Microsoft Entra application using application permissions, the indexer requires a client secret.

    + Select **Certificates & Secrets** from the menu on the left, then **Client secrets**, then **New client secret**.
    
        :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret.png" alt-text="Screenshot showing new client secret.":::
    
    + In the menu that pops up, enter a description for the new client secret. Adjust the expiration date if necessary. If the secret expires, it needs to be recreated and the indexer needs to be updated with the new secret.
    
        :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret-setup.png" alt-text="Screenshot showing how to set up a client secret.":::
    
    + The new client secret appears in the secret list. Once you navigate away from the page, the secret is no longer be visible, so copy it using the copy button and save it in a secure location.
    
        :::image type="content" source="media/search-howto-index-sharepoint-online/application-client-secret-copy.png" alt-text="Screenshot showing where to copy a client secret.":::

<a name="create-data-source"></a>

### Step 4: Create data source

Starting in this section, use a preview REST API for the remaining steps. We recommend the latest preview API.

A data source specifies which data to index, credentials, and policies to efficiently identify changes in the data (new, modified, or deleted rows). A data source can be used by multiple indexers in the same search service.

For SharePoint indexing, the data source must have the following required properties:

+ **name** is the unique name of the data source within your search service.
+ **type** must be "sharepoint". This value is case-sensitive.
+ **credentials** provide the SharePoint endpoint and the Microsoft Entra application (client) ID. An example SharePoint endpoint is `https://microsoft.sharepoint.com/teams/MySharePointSite`. You can get the endpoint by navigating to the home page of your SharePoint site and copying the URL from the browser.
+ **container** specifies which document library to index. Properties [control which documents are indexed](#controlling-which-documents-are-indexed).

To create a data source, call [Create Data Source (preview)](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2024-05-01-preview&preserve-view=true).

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-05-01-preview
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sharepoint-datasource",
    "type" : "sharepoint",
    "credentials" : { "connectionString" : "[connection-string]" },
    "container" : { "name" : "defaultSiteLibrary", "query" : null }
}
```

#### Connection string format

The format of the connection string changes based on whether the indexer is using delegated API permissions or application API permissions

+ Delegated API permissions connection string format

    `SharePointOnlineEndpoint=[SharePoint site url];ApplicationId=[Azure AD App ID];TenantId=[SharePoint site tenant id]`

+ Application API permissions connection string format

    `SharePointOnlineEndpoint=[SharePoint site url];ApplicationId=[Azure AD App ID];ApplicationSecret=[Azure AD App client secret];TenantId=[SharePoint site tenant id]`

> [!NOTE]
> If the SharePoint site is in the same tenant as the search service and system-assigned managed identity is enabled, `TenantId` doesn't have to be included in the connection string. If the SharePoint site is in a different tenant from the search service, `TenantId` must be included.

### Step 5: Create an index

The index specifies the fields in a document, attributes, and other constructs that shape the search experience.

To create an index, call [Create Index (preview)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2024-05-01-preview&preserve-view=true):

```http
POST https://[service name].search.windows.net/indexes?api-version=2024-05-01-preview
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
> Only [`metadata_spo_site_library_item_id`](#metadata) may be used as the key field in an index populated by the SharePoint Online indexer. If a key field doesn't exist in the data source, `metadata_spo_site_library_item_id` is automatically mapped to the key field.

### Step 6: Create an indexer

An indexer connects a data source with a target search index and provides a schedule to automate the data refresh. Once the index and data source are created, you can create the indexer.

If you're using delegated permissions, during this step, you’re asked to sign in with organization credentials that have access to the SharePoint site. If possible, we recommend creating a new organizational user account and giving that new user the exact permissions that you want the indexer to have. 

There are a few steps to creating the indexer:

1. Send a [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) request:

    ```http
    POST https://[service name].search.windows.net/indexers?api-version=2024-05-01-preview
    Content-Type: application/json
    api-key: [admin key]
    
    {
        "name" : "sharepoint-indexer",
        "dataSourceName" : "sharepoint-datasource",
        "targetIndexName" : "sharepoint-index",
        "parameters": {
        "batchSize": null,
        "maxFailedItems": null,
        "maxFailedItemsPerBatch": null,
        "base64EncodeKeys": null,
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

1. When you create the indexer for the first time, the [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) request waits until you complete the next step. You must call [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) to get the link and enter your new device code. 

    ```http
    GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2024-05-01-preview
    Content-Type: application/json
    api-key: [admin key]
    ```

    If you don’t run the [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) within 10 minutes, the code expires and you’ll need to recreate the [data source](#create-data-source).

1. Copy the device login code from the [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) response. The device login can be found in the "errorMessage".

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

1. The SharePoint Online indexer will access the SharePoint content as the signed-in user. The user that logs in during this step will be that signed-in user. So, if you sign in with a user account that doesn’t have access to a document in the Document Library that you want to index, the indexer won’t have access to that document.

    If possible, we recommend creating a new user account and giving that new user the exact permissions that you want the indexer to have.

1. Approve the permissions that are being requested.

    :::image type="content" source="media/search-howto-index-sharepoint-online/aad-app-approve-api-permissions.png" alt-text="Screenshot showing how to approve API permissions.":::

1. The [Create Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) initial request completes if all the permissions provided above are correct and within the 10 minute timeframe.

> [!NOTE]
> If the Microsoft Entra application requires admin approval and was not approved before logging in, you may see the following screen. [Admin approval](/azure/active-directory/manage-apps/grant-admin-consent) is required to continue.
:::image type="content" source="media/search-howto-index-sharepoint-online/no-admin-approval-error.png" alt-text="Screenshot showing admin approval required.":::

### Step 7: Check the indexer status

After the indexer has been created, you can call [Get Indexer Status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true):

```http
GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2024-05-01-preview
Content-Type: application/json
api-key: [admin key]
```

## Updating the data source

If there are no updates to the data source object, the indexer runs on a schedule without any user interaction. 

However, if you modify the data source object while the device code is expired, you must sign in again in order for the indexer to run. For example, if you change the data source query, sign in again using the `https://microsoft.com/devicelogin` and get the new device code.

Here are the steps for updating a data source, assuming an expired device code:

1. Call [Run Indexer (preview)](/rest/api/searchservice/indexers/run?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true) to manually start [indexer execution](search-howto-run-reset-indexers.md).

    ```http
    POST https://[service name].search.windows.net/indexers/sharepoint-indexer/run?api-version=2024-05-01-preview  
    Content-Type: application/json
    api-key: [admin key]
    ```

1. Check the [indexer status](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2024-05-01-preview&tabs=HTTP&preserve-view=true). 

    ```http
    GET https://[service name].search.windows.net/indexers/sharepoint-indexer/status?api-version=2024-05-01-preview
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

The SharePoint Online indexer also supports metadata specific to each document type. More information can be found in [Content metadata properties used in Azure AI Search](search-blob-metadata-properties.md).

> [!NOTE]
> To index custom metadata, "additionalColumns" must be specified in the [query parameter of the data source](#query).

## Include or exclude by file type

You can control which files are indexed by setting inclusion and exclusion criteria in the "parameters" section of the indexer definition.

Include specific file extensions by setting `"indexedFileNameExtensions"` to a comma-separated list of file extensions (with a leading dot). Exclude specific file extensions by setting `"excludedFileNameExtensions"` to the extensions that should be skipped. If the same extension is in both lists, it's excluded from indexing.

```http
PUT /indexers/[indexer name]?api-version=2024-05-01-preview
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

A single SharePoint Online indexer can index content from one or more document libraries. Use the "container" parameter on the data source definition to indicate which sites and document libraries to index from.

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
> To get the value for a particular keyword, we recommend navigating to the document library that you’re trying to include/exclude and copying the URI from the browser. This is the easiest way to get the value to use with a keyword in the query.

| Keyword | Value description and examples |
| ------- | ------------------------ |
| null | If null or empty, index either the default document library or all document libraries depending on the container name.	<br><br>Example: <br><br>``` "container" : { "name" : "defaultSiteLibrary", "query" : null } ``` |
| includeLibrariesInSite | Index content from all libraries under the specified site in the connection string. The value should be the URI of the site or subsite. <br><br>Example 1: <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/mysite" }``` <br><br>Example 2 (include a few subsites only): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/sites/TopSite/SubSite1;includeLibrariesInSite=https://mycompany.sharepoint.com/sites/TopSite/SubSite2" }``` |
| includeLibrary | Index all content from this library. The value is the fully qualified path to the library, which can be copied from your browser: <br><br>Example 1 (fully qualified path): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/mysite/MyDocumentLibrary" }``` <br><br>Example 2 (URI copied from your browser): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx" }``` |
| excludeLibrary | Don't index content from this library. The value is the fully qualified path to the library, which can be copied from your browser: <br><br> Example 1 (fully qualified path): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mysite.sharepoint.com/subsite1; excludeLibrary=https://mysite.sharepoint.com/subsite1/MyDocumentLibrary" }``` <br><br> Example 2 (URI copied from your browser): <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrariesInSite=https://mycompany.sharepoint.com/teams/mysite; excludeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx" }``` |
| additionalColumns | Index columns from the document library. The value is a comma-separated list of column names you want to index. Use a double backslash to escape semicolons and commas in column names: <br><br> Example 1 (additionalColumns=MyCustomColumn,MyCustomColumn2):  <br><br>```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/mysite/MyDocumentLibrary;additionalColumns=MyCustomColumn,MyCustomColumn2" }``` <br><br> Example 2 (escape characters using double backslash): <br><br> ```"container" : { "name" : "useQuery", "query" : "includeLibrary=https://mycompany.sharepoint.com/teams/mysite/MyDocumentLibrary/Forms/AllItems.aspx;additionalColumns=MyCustomColumnWith\\,,MyCustomColumnWith\\;" }``` |

## Handling errors

By default, the SharePoint Online indexer stops as soon as it encounters a document with an unsupported content type (for example, an image). You can use the `excludedFileNameExtensions` parameter to skip certain content types. However, you might need to index documents without knowing all the possible content types in advance. To continue indexing when an unsupported content type is encountered, set the `failOnUnsupportedContentType` configuration parameter to false:

```http
PUT https://[service name].search.windows.net/indexers/[indexer name]?api-version=2024-05-01-preview
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

+ [Indexers in Azure AI Search](search-indexer-overview.md)
+ [Content metadata properties used in Azure AI Search](search-blob-metadata-properties.md)
