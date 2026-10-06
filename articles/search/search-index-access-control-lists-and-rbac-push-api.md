---
title: Indexing ACLs Using the Push REST API
description: Learn how to use the REST API for indexing documents with ACLs and RBAC metadata.
ms.reviewer: admayber
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/31/2026
ai-usage: ai-assisted
---

# Indexing document access control lists (ACLs) using the push REST APIs (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [preview-terms](./includes/previews/preview-terms.md)]

Document-level permission ingestion through the push REST APIs (preview) lets you index documents along with their associated [access control lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control) and container [role-based access control (RBAC) roles](/azure/role-based-access-control/overview). When you push content into an Azure AI Search index via the [push REST APIs](/rest/api/searchservice/documents/?view=rest-searchservice-2026-08-01-preview&preserve-view=true), the service preserves those permissions on indexed content and enforces them at query time.

Key features include:

- Flexible control over ingestion pipelines.
- Standardized schema for permissions metadata.
- Support for hierarchical permissions, such as folder-level ACLs.

This article explains how to use the push REST API to index document-level permission metadata in Azure AI Search. This process prepares your index to query and enforce end-user permissions on search results.

## Prerequisites

- Content with ACL metadata from [Microsoft Entra ID](/entra/fundamentals/whatis) or another POSIX-style ACL system. For `userIds` and `groupIds` ACL fields, use Microsoft Entra object IDs (GUIDs), not UPNs or email addresses. Stable object IDs ensure reliable identity matching at query time, even if directory attributes change.

- The [latest preview REST API](/rest/api/searchservice/documents/?view=rest-searchservice-2026-08-01-preview&preserve-view=true) or a preview Azure SDK package providing equivalent features.

- An index schema with `permissionFilterOption` enabled, plus `permissionFilter` field attributes that store document permissions.

## Limitations

- An ACL field with permission filter type `userIds` or `groupIds` can hold at most 1000 values.

- An index can hold at most five unique values among fields of type `rbacScope` on all documents. There's no limit on the number of documents that share the same value of `rbacScope`.

- An existing field can be updated to include a `permissionFilter` assignment for built-in ACL or RBAC metadata filtering. To enable filtering on an existing index, add new fields or update existing fields to include a `permissionFilter` value.

- Only one field of each `permissionFilter` type (one each of `groupIds`, `userIds`, and `rbacScope`) can exist in an index.

- Each `permissionFilter` field should have `filterable` set to `true`.

- Query-time permission enforcement reflects the ACL values last written to the index. If source permissions change, those updates aren't reflected until you reingest or update the affected documents. Schedule incremental reingestion or partial updates to keep ACLs current.

- This functionality is currently not supported in the Azure portal.

## Create an index with permission filter fields

Indexing document ACLs and RBAC metadata with the REST API requires setting up an index schema that enables permission filters and has fields with permission filter assignments.

First, add `permissionFilterOption`. Valid values are `enabled` or `disabled`, and you should set it to `enabled`. You can switch it to `disabled` if you want to turn off permission-filter functionality at the index level.

Second, create string fields for your permission metadata and include `permissionFilter`. Recall that you can have one of each permission filter type.

Here's a basic example schema that includes all `permissionFilter` types:

```json  
{  
  "fields": [  
    { "name": "UserIds", "type": "Collection(Edm.String)", "permissionFilter": "userIds", "filterable": true },  
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true },  
    { "name": "RbacScope", "type": "Edm.String", "permissionFilter": "rbacScope", "filterable": true },  
    { "name": "DocumentId", "type": "Edm.String", "key": true }  
  ],
  "permissionFilterOption": "enabled"
}
```

For enterprise repositories, such as SharePoint Online, resolve document-level or folder-level permissions to Microsoft Entra user and group object IDs during ingestion before calling the push API. You should then store those IDs in the corresponding permission fields.

## REST API indexing example

Once you have an index with permission-filter fields, you can populate those values using the push indexing API, just like any other document fields. Here's an example using the specified index schema, where each document specifies the indexing action, key field (`DocumentId`), and permission fields. Documents should also include content, but that field is omitted in this example for brevity.

```https
POST https://exampleservice.search.windows.net/indexes('indexdocumentsexample')/docs/search.index?api-version=2026-08-01-preview
{
  "value": [
    {
      "@search.action": "upload",
      "DocumentId": "1",
      "UserIds": ["00aa00aa-bb11-cc22-dd33-44ee44ee44ee", "11bb11bb-cc22-dd33-ee44-55ff55ff55ff", "22cc22cc-dd33-ee44-ff55-66aa66aa66aa"],
      "GroupIds": ["none"],
      "RbacScope": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/Example-Storage-rg/providers/Microsoft.Storage/storageAccounts/azurestorage12345/blobServices/default/containers/blob-container-01"
    },
    {
      "@search.action": "merge",
      "DocumentId": "2",
      "UserIds": ["all"],
      "GroupIds": ["33dd33dd-ee44-ff55-aa66-77bb77bb77bb", "44ee44ee-ff55-aa66-bb77-88cc88cc88cc"]
    },
    {
      "@search.action": "mergeOrUpload",
      "DocumentId": "3",
      "UserIds": ["1cdd8521-38cf-49ab-b483-17ddaa48f68f"],
      "RbacScope": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/Example-Storage-rg/providers/Microsoft.Storage/storageAccounts/azurestorage12345/blobServices/default/containers/blob-container-03"
    }
  ]
}
```

## ACL access resolution rules

This section explains how the system determines a user's document access based on the permission fields on each document. These fields are either ACLs (`userIds` and `groupIds`, where `groupIds` includes security groups and Microsoft 365 Groups) or an RBAC scope (`rbacScope`). Azure evaluates the RBAC scope and the ACLs in a defined order, consistent with the [ADLS Gen2 permission model](/azure/storage/blobs/data-lake-storage-access-control-model#how-permissions-are-evaluated).

A user gains access by satisfying one of the following fields: a matching `userIds` or `groupIds` entry, or a qualifying Azure role assignment for the `rbacScope`. For information about how caller identities are provided at query time, see [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).

### Special ACL values "all" and "none"

ACL fields, such as `userIds` and `groupIds`, typically contain lists of GUIDs (Globally Unique Identifiers) that identify users and groups with access to the document. Two special string values, "all" and "none", are supported for these ACL field types. These values act as broad filters to control access at the global level, as shown in the following table.

| userIds / groupIds value | Meaning |
| --- | --- |
| `["all"]` | Any user can access the document |
| `["none"]` | No user can access the document by matching this ACL type |
| [] (empty array) | No user can access the document by matching this ACL type |

Because a user needs to match only one field type, the special value "all" grants public access regardless of any other ACL field values. In contrast, setting `userIds` to "none" or an empty array means no users are granted access to the document *based on user ID*. They might still be granted access by matching group ID or RBAC metadata.

### Access control example

This example illustrates how document access rules are resolved based on permission field values in `userIds`, `groupIds`, and `rbacScope`. For readability, this scenario uses aliases such as "user1" and "group1" instead of GUIDs; in production, use Microsoft Entra object IDs (GUIDs).

| Document # | userIds | groupIds | RBAC Scope | Permitted users list | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | `["none"]` | `[]` | Empty | No users have access | The values `["none"]` and `[]` behave exactly the same |
| 2 | `["none"]` | `[]` | scope/to/container1 | Users with RBAC permissions to container1 | The value of "none" doesn't block access when other permission fields (`groupIds` or `rbacScope`) grant access |
| 3 | `["none"]` | `["group1", "group2"]` | Empty | Members of group1 or group2 | |
| 4 | `["all"]` | `["none"]` | Empty | Any user | Any querying user matches the ACL filter "all", so all users have access |
| 5 | `["all"]` | `["group1", "group2"]` | scope/to/container1 | Any user | Since all users match the "all" filter for userID, the groupID and RBAC filters don't have any impact |
| 6 | `["user1", "user2"]` | `["group1"]` | Empty | User1, user2, or any member of group1 | |
| 7 | `["user1", "user2"]` | `[]` | Empty | User1 or user2 | |

## Related content

- [Connect to Azure AI Search using roles](search-security-rbac.md)
- [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
- [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API)
