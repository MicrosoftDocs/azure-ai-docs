---
title: Troubleshoot SharePoint Permission Filtering
description: Diagnose missing, unexpected, or failed query results when Azure AI Search applies permission filters to indexed SharePoint content.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: troubleshooting-general
ms.date: 08/08/2026
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
---

# Troubleshoot SharePoint permission filtering in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Use this article if query-time permission filtering for indexed SharePoint content returns missing or unexpected results, or if a permission-filtered query fails.

## Prerequisites

+ An index populated by the [SharePoint in Microsoft 365 indexer](search-how-to-index-sharepoint-online.md) with [ACL ingestion configured](search-indexer-sharepoint-access-control-lists.md).
+ Query-time permission filtering configured as described in [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).
+ REST API version `2026-05-01-preview` or an equivalent preview SDK package when you use SharePoint site groups.
+ Access to the index definition, generated or explicit indexer status, and the SharePoint permissions for a test user.
+ **Search Index Data Contributor** or equivalent elevated-read permission if you need to compare filtered and unfiltered results.

## Follow the troubleshooting decision tree

Complete these checks in order. Stop when the observed result identifies the configuration or permission that needs correction.

### 1. Confirm the failure occurs at query time

This article covers permission filtering after SharePoint content and ACL metadata are indexed.

+ If data source creation or an indexer run reports `Invalid AAD tenant`, follow the [Microsoft Entra tenant remediation](cognitive-search-common-errors-warnings.md#error-invalid-aad-tenant).
+ If you need to correct `TenantId`, authentication, or the data source connection string, see [Configure the SharePoint in Microsoft 365 indexer](search-how-to-index-sharepoint-online.md#configure-the-sharepoint-in-microsoft-365-indexer).
+ If `UserIds`, `GroupIds`, or `SharePointSiteUrl` are missing during indexing, use the [ACL ingestion troubleshooting table](search-indexer-sharepoint-access-control-lists.md#troubleshooting).

Continue here only when indexed permission metadata exists and the symptom occurs when you query it.

### 2. Identify the three identities

Record which identity fills each role. Don't substitute one identifier for another.

| Identity | Purpose | Where to verify it |
|---|---|---|
| Querying user | The delegated user token in `x-ms-query-source-authorization` determines which protected documents the user can retrieve. | Your application authentication flow and the query request. |
| SharePoint connector app registration | The `sharePointConnectorAppRegistration` on the index lets Azure AI Search resolve the querying user's SharePoint site group memberships. | The index definition and the app registration described in [Configure SharePoint groups support](search-indexer-sharepoint-access-control-lists.md#configure-sharepoint-groups-support). |
| Azure AI Search request identity | The Microsoft Entra bearer token in the `Authorization` header, or the API key in the `api-key` header, authenticates the request to the search service. The identity must have permission to query the index. | Your query client and [Azure AI Search data plane role assignment](search-security-rbac.md#built-in-roles). |

### 3. Check the permission-filter configuration

Compare the index, indexer, and generated objects against their owner articles.

1. Confirm the index has `permissionFilterOption` set to `enabled`.
1. Confirm `UserIds` and `GroupIds` have the correct `permissionFilter` values.
1. For SharePoint site groups, confirm the index has `sharePointConnectorAppRegistration` and a `SharePointSiteUrl` field with `sharepointSiteUrl: true`.
1. Confirm every indexed document or chunk carries the applicable permission fields. If the skillset uses index projections, verify the ACL fields are in `indexProjections.mappings`.

If any value is absent, return to [Configure your search service for ACL ingestion and query-time enforcement](search-indexer-sharepoint-access-control-lists.md#configure-your-search-service-for-acl-ingestion-and-query-time-enforcement).

### 4. Check the query token safely

Never log, paste into a support request, or share a full access token. Decode only the token payload locally, and sanitize identifiers before you capture diagnostic output.

1. Confirm the request includes `x-ms-query-source-authorization` with a current delegated token for the test user.
1. Decode the payload locally and confirm the `oid` identifies the intended test user. Record a sanitized value such as `<test-user-object-id>`.
1. Reauthenticate the user and retry if the token is missing or expired.

If the user token is omitted, permission-protected content isn't returned. The `Authorization` header alone doesn't replace `x-ms-query-source-authorization`.

### 5. Check Microsoft Entra permissions

1. Confirm the indexed `UserIds` or `GroupIds` contain the expected Microsoft Entra object ID. Use an [elevated-read query](search-query-access-control-rbac-enforcement.md#elevated-permissions-for-investigating-incorrect-results) only for this diagnostic comparison.
1. Confirm the test user has a direct assignment or reaches the assigned Microsoft Entra group through transitive Microsoft Entra group membership.
1. If the Microsoft Entra group is nested within a SharePoint group, change the assignment. This mixed relationship isn't expanded and can cause missing results. Add the user directly to the SharePoint group, or grant permission through a supported Microsoft Entra group assignment.

For the exact support boundary, see [Supported group relationships](search-indexer-sharepoint-access-control-lists.md#supported-group-relationships).

### 6. Check SharePoint site group permissions

Complete this step when the document ACL depends on an Owners, Members, Visitors, or custom SharePoint site group.

1. Use an elevated-read query to confirm `GroupIds` contains the expected `spg:`-prefixed group ID and `SharePointSiteUrl` identifies the source site.
1. Confirm the test user is a direct member of that SharePoint group.
1. Confirm the index's `sharePointConnectorAppRegistration` uses the identifiers and permissions required by [SharePoint groups support](search-indexer-sharepoint-access-control-lists.md#configure-sharepoint-groups-support).

If the indexed fields are empty or stale, fix ingestion or [synchronize the SharePoint permissions](search-indexer-sharepoint-access-control-lists.md#synchronize-permissions-between-indexed-and-source-content) before you retest the query.

### 7. Check the query request

1. Use REST API version `2026-05-01-preview` or an equivalent preview SDK package for SharePoint site-group permission filters.
1. Confirm `Authorization` authenticates a principal that can query the index.
1. Confirm `x-ms-query-source-authorization` contains the delegated test-user token.
1. Retry the same query without unrelated filters or ranking changes so you can isolate permission behavior.

Use the [general query example](search-query-access-control-rbac-enforcement.md#query-example) as the request-shape owner. Don't include full tokens in saved requests or logs.

### 8. Compare expected and actual results

1. Choose one document the test user can access and one document the user can't access in SharePoint.
1. Run the permission-filtered query as the test user and record only document keys or other nonsecret identifiers.
1. Run an elevated-read query and compare the stored `UserIds`, `GroupIds`, and `SharePointSiteUrl` values with the source permissions.
1. If elevated read returns the expected document but the user query doesn't, focus on the user token and group resolution. If elevated read also misses it, focus on ingestion, mappings, and ACL synchronization.

Elevated read is for investigation. Don't use it to return unrestricted results to end users.

### 9. Capture request correlation details

If the query still fails, capture the API version, UTC timestamp, sanitized request body, HTTP status, response headers, and any request or correlation ID returned by the service. Include the index name and whether the same document appears under elevated read.

Remove access tokens, API keys, secrets, user names, and tenant-specific URLs before you share diagnostics with [Microsoft Support](https://azure.microsoft.com/support).

## Related content

+ [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
+ [Use a SharePoint indexer to ingest permission metadata](search-indexer-sharepoint-access-control-lists.md)
+ [Configure the SharePoint in Microsoft 365 indexer](search-how-to-index-sharepoint-online.md)
