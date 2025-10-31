---
title: Create a SharePoint (Remote) Knowledge Source
titleSuffix: Azure AI Search
description: A remote Sharepoint knowledge source tells the agentic retrieval engine to query SharePoint sites directly.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/30/2025
---

# Create a remote SharePoint knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *remote SharePoint knowledge source* specifies a connection to a SharePoint site and uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) to query textual content directly from SharePoint, returning results to the agentic retrieval engine for merging, ranking, and response formulation. There's no search index used by this knowledge source, and only textual content is queried.

SharePoint permissions and Purview labels are honored in requests for content. Usage is billed through Microsoft 365 and a Copilot license.

Like any other knowledge source, you specify a remote SharePoint knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and use the results as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

## Prerequisites

+ Azure AI Search in an Azure tenant, configured for Microsoft Entra ID authentication.

+ SharePoint Online in a Microsoft 365 tenant. You need the tenant ID to set up the connection string.

+ An application registration in the Azure AI Search tenant used for Microsoft Entra ID authentication to SharePoint.

+ A personal access token for local development. The agentic retrieval engine uses your access token to call SharePoint on your behalf. For more information about using a personal access token on requests, see [Connect to Azure AI Search](search-get-started-rbac.md).

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

## Limitations

The following limitations in the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) apply to remote SharePoint knowledge sources.

+ Limit of 200 requests per user per hour.

+ Query character limit of 1,500 characters.

+ Hybrid queries are only supported for the following file extensions: .doc, .docx, .pptx, .pdf, .aspx, and .one.

+ Multimodal retrieval (nontextual content, including tables, images, and charts) isn't supported/

+ Maximum of 25 results from a query.

+ Results are returned by Copilot Retrieval API as unordered.

+ Invalid filter expressions (Keyword Query Language KQL) are ignored and the query continues to execute without the filter.

## Register an application with Microsoft Entra ID

To create a SharePoint Online connection string with a tenant ID, application ID, and application secret, you must register a new application in the Microsoft Entra admin center and grant it permissions. Using an app registration is recommended for application-only authentication to SharePoint Online. 

### Step 1: Register an application in Microsoft Entra ID

1. Navigate to the Microsoft Entra admin center by going to https://entra.microsoft.com/. You must have an account with permissions to register applications.

1. Select **Microsoft Entra ID** from the left-hand menu.

1. Choose **App registrations** and then select **New registration**.

1. Fill in the registration details:

   + Name: Enter a descriptive name for your application (for example, "SharePoint Connection App").
   + Supported account types: Select Accounts in this organizational directory only.
   + Redirect URI (optional): This isn't needed for a client secret flow, but you can enter https://localhost.

1. Select **Register**.

### Step 2: Record the application and tenant IDs

After the app is registered, you'll be taken to its Overview page. Copy and save the following values for your connection string: 

+ Application (client) ID: The unique identifier for your app.

+ Directory (tenant) ID: The unique ID for your organization's Microsoft Entra instance. 

### Step 3: Create a client secret

1. On the app's management page, select **Certificates & secrets** from the menu.

1. Select **New client secret**.

1. Add a **Description** and select an **Expires** duration for the secret. Microsoft recommends a shorter expiry for better security.

1. Select **Add**.

1. Immediately copy the **Value** of the client secret. *This is your only chance to save this value*. Once you leave the page, it can't be retrieved again. 

### Step 4: Grant API permissions to SharePoint

1. On the app's management page, select **API permissions**.

1. Select **Add a permission**.

1. Select the SharePoint API.

1. Choose **Application permissions**, then select the required permissions for your application, such as `Sites.FullControl.All` for full access or `Sites.Read.All` for read-only.

1. Select **Add permissions**.

1. Select **Grant admin consent for [Your Organization]** and confirm the consent. 

### Step 5: Form the connection string

With your Tenant ID, Application ID (Client ID), and Application Secret (Client Secret), you can now construct your connection string. The format expected by Azure AI Search is:

```
SharePointOnlineEndpoint=https://YOUR-ACCOUNT-NAME.sharepoint.com/;ApplicationId=YOUR-APPLICATION-ID;ApplicationSecret=YOUR-APPLICATION-SECRET;TenantId=YOUR-TENANT-ID
```

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for a remote SharePoint knowledge source. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json
{
  "name": "my-sharepoint-ks",
  "kind": "remoteSharePoint",
  "description": "A sample remote sharepoint knowledge source",
  "encryptionKey": null,
  "remoteSharePointParameters": {
    "filterExpression": "filetype:docx",
    "containerTypeId": null,
    "resourceMetadata": [
      "Author",
      "Title"
    ]
  }
}
```

## Create a knowledge source

To create a remote SharePoint knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR SEARCH SERVICE ADMIN API KEY>
    @aoai-endpoint = <YOUR AZURE OPENAI RESOURCE PROVIDING A CHAT COMPLETION MODEL>
    @aoai-key = <YOUR AZURE OPENAI KEY>
    @access-token = <YOUR PERSONAL ACCESS TOKEN USED FOR RETRIEVING PERMITTED CONTENT ON SHAREPOINT>
    @sharepoint-connection-string = <YOUR SHAREPOINT CONNECTION STRING>
    ```

    API keys are used for your client connection to Azure AI Search and Azure OpenAI. Your access token is used by Azure AI Search to connect to SharePoint Online on your behalf. You can only retrieve content that you're permitted to access. For more information about getting a personal access token and other values, see [Connect to Azure AI Search](search-get-started-rbac.md). You can also use your personal access token to access Azure AI Search and Azure OpenAI if you set up role assignments on each resource. Using keys allows you to omit this step.

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    POST {{search-url}}/knowledgesources/my-remote-sharepoint-ks?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
        "name": "my-remote-sharepoint-ks",
        "kind": "remoteSharePoint",
        "description": "This knowledge source queries a remote SharePoint site for text and images.",
        "encryptionKey": null,
        "remoteSharePointParameters": {
            "filterExpression": "filetype:docx",
            "resourceMetadata": [ "Author", "Title" ],
            "containerTypeId": null
        }
    }
    ```

1. Select **Send Request**.

<!-- Should we include a response and do we need to say anything about purview sensitivity labels? -->

### Source-specific properties

You can pass the following properties to create a remote SharePoint knowledge source.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `kind` | The kind of knowledge source, which is `remoteSharePoint` in this case. | String | Yes |
| `description` | A description of the knowledge source. | String | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No |
| `filterExpression` | An expression written in the SharePoint in Keyword Query Language. Used to specify sites and paths to content. | String | No |
| `resourceMetadata` | A comma-delimited list of the standard metadata fields: author, file name, creation date, content type, and file type. | Array | No |
| `containerTypeId` | Ignored for now. | String| No |

<!-- SharePoint embedded is containers. Many moving parts. Defer for now. -->

### Filter expression examples

Learn more about the full [Keyword Query Language (KQL)](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/copilotroot-retrieval?pivots=graph-v1#example-7-use-filter-expressions) syntax reference.

+ Filter to a single site by ID: `"filterExpression": "SiteID:\"e2cf7e40-d689-41de-99ee-a423811a253c\""`

+ Filter to multiple sites by ID: `"filterExpression": "SiteID:\"e2cf7e40-d689-41de-99ee-a423811a253c\" OR SiteID:\"523fcf40-d689-41de-99ee-a423811a253c\""` 

+ Filter to files under a specific path: `"filterExpression": "Path:\"https://azuresearchdev4.sharepoint.com/sites/miml/Shared Documents/en/mydocs\""` 

+ Filter to a specific date range: `"filterExpression": "LastModifiedTime >= 2024-07-22 AND LastModifiedTime <= 2025-01-08"` 

+ Filter to files of a specific file type: `"filterExpression": "FileExtension:\"docx\" OR FileExtension:\"pdf\" OR FileExtension:\"pptx\""` 

+ Filter to files of a specific information protection label: `"filterExpression": "InformationProtectionLabelId:\"f0ddcc93-d3c0-4993-b5cc-76b0a283e252\""` 

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge base, there are more properties to set on the knowledge source that are specific to query operations.

<!-- Deviating from pattern here. SharePoint remote needs answerSynthesis-->
Here's an example of a knowledge base that specifies a remote SharePoint knowledge source. Make sure you set `outputMode` to `answerSynthesis`. Currently, GPT 4 series is recommended for chat completion in agentic retrieval.

```json
{
  "name": "remote-sp-kb",
  "description": "A sample federated SharePoint knowledge base",
  "retrievalInstructions": null,
  "answerInstructions": null,
  "outputMode": "answerSynthesis",
  "knowledgeSources": [
    {
      "name": "my-sharepoint-ks"
    }
  ],
  "models": [
    {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "<redacted>",
        "deploymentId": "gpt-4.1-mini",
        "apiKey": "<redacted>",
        "modelName": "gpt-4.1-mini",
        "authIdentity": null
      }
    }
  ],
  "encryptionKey": null,
  "retrievalReasoningEffort": {
    "kind": "low"
  }
}
```

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
