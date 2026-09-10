---
title: Create a Work IQ Knowledge Source
description: Learn how to create a Work IQ knowledge source to ground an agentic retrieval pipeline in Azure AI Search with organizational intelligence from Work IQ.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/17/2026
ms.custom:
  - dev-focus
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Work IQ knowledge source (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> When you connect to Work IQ, you might incur costs, and data might be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It's your responsibility to manage whether your data flows outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This responsibility includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *Work IQ knowledge source* (preview) connects [Work IQ](/microsoft-365/copilot/extensibility/work-iq) to an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

Work IQ surfaces organizational intelligence from your Microsoft 365 content, including documents, emails, meetings, and activity across Microsoft 365 apps.

Unlike indexed knowledge sources, Work IQ knowledge sources query live data directly at retrieval time. No ingestion pipeline is needed. Queries require a user access token issued for your Microsoft Entra app registration. Azure AI Search exchanges that token for a delegated Work IQ token and calls Work IQ on the user's behalf.

> [!WARNING]
> In this preview, a Work IQ knowledge source might use Work IQ capabilities that perform actions, not just retrieve information. Use it with care, limit access to trusted applications and users, and review your scenario's permissions and governance controls before enabling it.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| --- | --- | --- | --- | --- | --- | --- |
| ❌ | ❌ | ✔️ | ✔️ | ❌ | ❌ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A [usage-based billing plan for Work IQ](/microsoft-365/copilot/extensibility/work-iq/enable-work-iq#prerequisites) set up in Copilot Studio with an Azure subscription and resource group. Assign each user who queries Work IQ to the billing plan.

+ Your [Microsoft Entra tenant enabled for Work IQ](/microsoft-365/copilot/extensibility/work-iq/enable-work-iq#enable-work-iq-api-in-your-organization). After billing is configured, a Microsoft Entra Global Administrator completes this one-time setup.

+ A client application that signs in users and sends retrieve requests.

+ Recommended Microsoft Entra roles for each app setup action:

  + [Application Developer](/entra/identity/role-based-access-control/permissions-reference#application-developer) to create an app registration.

  + App registration owner or a supported administrator role to [create its federated identity credential](/entra/workload-id/workload-identity-federation-create-trust#important-considerations-and-restrictions).

  + [Cloud Application Administrator or Application Administrator](/entra/identity/enterprise-apps/grant-admin-consent#prerequisites) to grant tenant-wide admin consent for the `WorkIQAgent.Ask` delegated permission.

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ The [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true) version of the Search Service REST API.

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Data governance and compliance

Before you enable Work IQ retrieval, review [Data, Privacy, and Security for Microsoft 365 Copilot](/microsoft-365/copilot/microsoft-365-copilot-privacy).

### Data use and privacy

Prompts, responses, and data accessed through Microsoft Graph aren't used to
train foundation language models.

### Access control

Work IQ applies Microsoft 365 permissions on every request. Retrieval returns
only organizational data that the signed-in user has permission to access.

### Data residency and compliance

Review the Microsoft 365 documentation for the data residency, privacy,
security, and compliance commitments that apply to your organization and
scenario.

## Set up Microsoft Entra authentication

Starting with the `2026-08-01-preview` API version, each Work IQ knowledge source uses a customer-owned Microsoft Entra app registration for authentication. [At query time](#enforce-permissions-at-query-time), authentication works as follows:

1. The client app signs in the user and sends a user assertion to Azure AI Search.
1. The search service managed identity authenticates as the customer-owned app through a federated credential.
1. Azure AI Search exchanges the user assertion for a delegated Work IQ token and calls Work IQ on behalf of the signed-in user.

No client secret is stored on the Work IQ knowledge source. Configure the app and its permissions once, and then create a federated credential for each search service identity that uses the app.

### Configure the Work IQ app registration

To configure the customer-owned app that Azure AI Search uses to call Work IQ:

1. [Register an application](/entra/identity-platform/quickstart-register-app) in the Microsoft Entra tenant where you want to manage Work IQ consent. For **Supported account types**, select **Accounts in this organizational directory only**.

1. On the app registration's **Overview** page, copy the **Application (client) ID** and **Directory (tenant) ID**. You need the application ID to configure Work IQ authentication and the tenant ID to sign in to the tenant that contains the app registration.

1. On the app registration's **Expose an API** page, [add the required delegated scope](/entra/identity-platform/quickstart-configure-app-expose-web-apis#add-a-scope) named exactly `access_as_user`. Use this lowercase name; don't substitute another scope name. The full scope is `api://<application-client-id>/access_as_user`.

1. On the app registration's **API permissions** page, select **Add a permission** > **APIs my organization uses**.

1. Search for **Work IQ** (application ID `fdcc1f02-fc51-4226-8753-f668596af7f7`), select **Delegated permissions** > **WorkIQAgent.Ask**, and then select **Add permissions**.

1. Have an administrator with a consent role listed in the prerequisites select **Grant admin consent for [your tenant]** on the same page. This consent allows the app to exchange a user assertion for a delegated Work IQ token.

### Configure the search service identity

To configure the identity that Azure AI Search uses to authenticate as your Work IQ app:

1. [Enable a system-assigned managed identity](search-how-to-managed-identities.md) on your search service. If you can't use a system-assigned identity, configure exactly one user-assigned identity. A search service with multiple user-assigned identities and no system-assigned identity isn't supported.

1. On the search service's **Identity** page, copy the **Object (principal) ID**. The federated credential uses this value as its `subject`.

1. Go to **Microsoft Entra ID** > **Overview** and copy the **Tenant ID**. The federated credential uses this value in its `issuer` URL.

### Create a federated credential

To create a federated credential for the search service identity:

1. Create a file named `credential.json`. Replace `<search-service-name>`, `<search-service-tenant-id>`, and `<search-service-principal-id>` with values for your search service.

    ```json
    {
      "name": "<search-service-name>-identity",
      "issuer": "https://login.microsoftonline.com/<search-service-tenant-id>/v2.0",
      "subject": "<search-service-principal-id>",
      "audiences": ["api://AzureADTokenExchange"]
    }
    ```

    The credential name must be unique on the app registration. The `subject` value must match the managed identity principal ID exactly. A mismatch surfaces when you query, not when you create the knowledge source.

1. Sign in to the [Azure CLI](/cli/azure/install-azure-cli) with the tenant that contains the app registration.

    ```azurecli
    az login --tenant <app-tenant-id> --allow-no-subscriptions
    ```

1. Create the federated credential.

    ```azurecli
    az ad app federated-credential create --id <application-client-id> --parameters credential.json --query id --output tsv
    ```

1. Copy the command output. Use this value for `federatedCredentialId` when you create the Work IQ knowledge source.

Each federated credential trusts one managed identity principal ID. If another search service identity uses the app registration, repeat this procedure with a unique credential name and that identity's tenant and principal IDs. Use the corresponding credential ID on each Work IQ knowledge source.

### Configure the client app

To configure the app that signs in users and sends retrieve requests:

1. On the client app's **API permissions** page, select **Add a permission** > **APIs my organization uses**.

1. Paste the **Application (client) ID** that you copied earlier into the search box, and then select the Work IQ app registration.

1. Select **Delegated permissions** > **access_as_user**, and then select **Add permissions**.

1. Complete any consent required by your tenant's user-consent policy. If admin consent is required, have an administrator select **Grant admin consent for [your tenant]**.

The client app can now request a user assertion for the Work IQ app registration. The `access_as_user` permission doesn't grant the client app direct access to Work IQ.

### Authentication values

When you create a Work IQ knowledge source, use the following `entraAppAuthentication` values from your Microsoft Entra app setup. Each value you provide must be a GUID.

| Property | Required | Value |
| --- | --- | --- |
| `applicationId` | Yes | Application (client) ID of your Work IQ app registration. |
| `federatedCredentialId` | Yes | Object ID of the federated credential you created on the app. It's not the credential name and isn't the search service principal ID. |
| `tenantId` | No | Directory (tenant) ID of the app registration. Omit this property when the app registration and search service are in the same tenant. If they're in different tenants, this property is required. |

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a Work IQ knowledge source.

```json
{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "A sample Work IQ knowledge source.",
  "workIQParameters": {
    "entraAppAuthentication": {
      "applicationId": "11111111-1111-1111-1111-111111111111",
      "federatedCredentialId": "22222222-2222-2222-2222-222222222222",
      "tenantId": null
    }
  },
  "encryptionKey": null
}
```

## Create a knowledge source

Run the following code to create a Work IQ knowledge source.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;

Uri searchEndpoint =
    new("https://<search-service-name>.search.windows.net");
var credential = new DefaultAzureCredential();
var indexClient = new SearchIndexClient(searchEndpoint, credential);

var entraAuthentication = new EntraAppAuthentication(
    Guid.Parse("<application-client-id>"),
    Guid.Parse("<federated-credential-id>"));
var knowledgeSource = new WorkIQKnowledgeSource(
    "my-workiq-ks",
    new WorkIQKnowledgeSourceParameters(entraAuthentication))
{
    Description = "A sample Work IQ knowledge source."
};

KnowledgeSource createdSource =
    await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Created knowledge source '{createdSource.Name}'.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [WorkIQKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.workiqknowledgesource?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    EntraAppAuthentication,
    WorkIQKnowledgeSource,
    WorkIQKnowledgeSourceParameters,
)

endpoint = "https://<search-service-name>.search.windows.net"
credential = DefaultAzureCredential()

knowledge_source = WorkIQKnowledgeSource(
    name="my-workiq-ks",
    description="A sample Work IQ knowledge source.",
    work_iq_parameters=WorkIQKnowledgeSourceParameters(
        entra_app_authentication=EntraAppAuthentication(
            application_id="<application-client-id>",
            federated_credential_id="<federated-credential-id>",
        )
    ),
)

with SearchIndexClient(endpoint, credential) as index_client:
    created_source = index_client.create_or_update_knowledge_source(
        knowledge_source
    )
print(f"Created knowledge source '{created_source.name}'.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [WorkIQKnowledgeSource](/python/api/azure-search-documents/azure.search.documents.indexes.models.workiqknowledgesource)

::: zone-end

::: zone pivot="rest"

```http
@search-endpoint = <search-endpoint> // Example: https://my-service.search.windows.net
@search-access-token = <search-access-token> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

### Create a Work IQ knowledge source
PUT {{search-endpoint}}/knowledgesources/my-workiq-ks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json
Prefer: return=representation

{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "A sample Work IQ knowledge source.",
  "workIQParameters": {
    "entraAppAuthentication": {
      "applicationId": "<application-client-id>",
      "federatedCredentialId": "<federated-credential-id>"
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query Work IQ content. This knowledge source has unique query-time permissions enforcement and response characteristics.

> [!IMPORTANT]
> Work IQ can take 40–60 seconds or more to respond. To avoid timeout errors, set `maxRuntimeInSeconds` on the retrieve request to `120` or higher.

### Enforce permissions at query time

Starting with the `2026-08-01-preview` API version, Work IQ knowledge sources use an on-behalf-of (OBO) token flow through your customer-owned Microsoft Entra app registration. In addition to authenticating the retrieve request to Azure AI Search, your client must provide an app-audience user assertion for the signed-in user.

Your client app must sign in the user and acquire the user assertion. How you acquire the assertion depends on the app's platform and language. Use Microsoft Authentication Library (MSAL) and the [authorization code flow with Proof Key for Code Exchange](/entra/identity-platform/v2-oauth2-auth-code-flow) (PKCE) to request the exact scope `api://<application-client-id>/access_as_user`.

Before you send the user assertion, confirm that:

+ `aud` identifies your Work IQ app registration.
+ `scp` contains `access_as_user`.
+ `oid` and `tid` identify the signed-in user and app tenant.

Send both credentials in the same retrieve request, as shown in the following example. Use an Azure AI Search token or API key for service authentication. Pass the raw user assertion in the `x-ms-query-work-iq-source-authorization` header, not `x-ms-query-source-authorization`.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

Uri searchEndpoint =
    new("https://<search-service-name>.search.windows.net");
string userAssertion = "<user-assertion>";
var credential = new DefaultAzureCredential();
var options = new SearchClientOptions();
options.Retry.NetworkTimeout = TimeSpan.FromSeconds(130);
var retrievalClient = new KnowledgeBaseRetrievalClient(
    searchEndpoint,
    "my-kb",
    credential,
    options);

var request = new KnowledgeBaseRetrievalRequest
{
    IncludeActivity = true,
    MaxRuntimeInSeconds = 120
};
request.Intents.Add(
    new KnowledgeRetrievalSemanticIntent("Find my project status."));
request.KnowledgeSourceParams.Add(
    new WorkIQKnowledgeSourceParams("my-workiq-ks")
    {
        IncludeReferences = true,
        IncludeReferenceSourceData = true
    });

var response = await retrievalClient.RetrieveAsync(
    request,
    querySourceAuthorization: null,
    queryWorkIQSourceAuthorization: userAssertion);
Console.WriteLine(response.Value);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import (
    KnowledgeBaseRetrievalClient,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
    WorkIQKnowledgeSourceParams,
)

endpoint = "https://<search-service-name>.search.windows.net"
user_assertion = "<user-assertion>"
credential = DefaultAzureCredential()

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="Find my project status."
        )
    ],
    knowledge_source_params=[
        WorkIQKnowledgeSourceParams(
            knowledge_source_name="my-workiq-ks",
            include_references=True,
            include_reference_source_data=True,
        )
    ],
    include_activity=True,
    max_runtime_in_seconds=120,
)

with KnowledgeBaseRetrievalClient(
    endpoint,
    credential,
    knowledge_base_name="my-kb",
) as retrieval_client:
    response = retrieval_client.retrieve(
        request,
        query_work_iq_source_authorization=user_assertion,
        timeout=130,
    )

print(response)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

::: zone-end

::: zone pivot="rest"

```http
@search-endpoint = <search-endpoint>
@search-access-token = <search-access-token>
@user-assertion = <user-assertion>

### Query a knowledge base with a Work IQ knowledge source
POST {{search-endpoint}}/knowledgebases/my-kb/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
x-ms-query-work-iq-source-authorization: {{user-assertion}}
Content-Type: application/json

{
  "messages": [{
    "role": "user",
    "content": [{
      "type": "text",
      "text": "Find my project status."
    }]
  }],
  "knowledgeSourceParams": [{
    "knowledgeSourceName": "my-workiq-ks",
    "kind": "workIQ",
    "includeReferences": true,
    "includeReferenceSourceData": true
  }],
  "includeActivity": true,
  "maxRuntimeInSeconds": 120
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

A successful request returns `200 OK`. Confirm that `activity` contains an entry whose `type` is `workIQ` and whose `knowledgeSourceName` matches your Work IQ knowledge source. Also confirm that `references` contains a `workIQ` entry.

The following table lists common configuration failures.

| Status | Cause |
| --- | --- |
| 400 | The Work IQ authorization header is missing or malformed, required user claims are absent, or the search service doesn't have a supported managed identity configuration. |
| 206 or 502 | The Work IQ source failed because token exchange, consent, the delegated permission, the federated credential, downstream authorization, or the Work IQ request failed or timed out. Inspect the source activity error. A `206` response means another source succeeded. A `502` response means every selected source failed or a required source failed. |

### Work IQ-specific response fields

Work IQ knowledge sources return results in the `references` array and query diagnostics in the `activity` array. Each reference entry contains:

+ `sourceData.parts[].text`: Grounded text passages from Work IQ.
+ `sourceData.parts[].data`: Work IQ citation data. Citation parts have the media type `application/vnd.ms-workiq-reference`.

The following example shows a retrieve response containing a Work IQ knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `includeReferenceSourceData` to `true` on the knowledge source entry within `knowledgeSourceParams` on the retrieve request.

```json
{
  "response": [],
  "activity": [
    {
      "type": "workIQ",
      "id": 0,
      "knowledgeSourceName": "my-workiq-ks",
      "queryTime": "2026-08-01T19:25:23.683Z",
      "count": 1,
      "elapsedMs": 1137,
      "workIQArguments": {
        "search": "my query"
      }
    }
  ],
  "references": [
    {
      "type": "workIQ",
      "id": "83dd7d40",
      "activitySource": 0,
      "rerankerScore": 3.5,
      "sourceData": {
        "parts": [
          {
            "text": "Have your VPN username and password ready."
          },
          {
            "data": {
              "1-abc123": {
                "targetLink": "https://contoso.sharepoint.com/doc.docx",
                "isCitedInResponse": true,
                "isSourceFiltered": false
              }
            },
            "mediaType": "application/vnd.ms-workiq-reference"
          }
        ]
      }
    }
  ]
}
```

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
