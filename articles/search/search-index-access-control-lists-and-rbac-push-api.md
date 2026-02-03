---  
title: Indexing ACLs using the push REST API
titleSuffix: Azure AI Search  
description: Learn how to use the REST API for indexing documents with ACLs and RBAC metadata.  
ms.service: azure-ai-search  
ms.topic: how-to 
ms.date: 01/28/2025 
author: admayber
ms.author: admayber  
---  

# Indexing document Access Control Lists (ACLs) using the push REST APIs

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Indexing documents, along with their associated [Access Control Lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control) and container [Role-Based Access Control (RBAC) roles](/azure/role-based-access-control/overview), into an Azure AI Search index via the [push REST APIs](/rest/api/searchservice/documents/?view=rest-searchservice-2025-11-01-preview&preserve-view=true) preserves document-level permission on indexed content at query time.

Key features include:

- Flexible control over ingestion pipelines.
- Standardized schema for permissions metadata.
- Support for hierarchical permissions, such as folder-level ACLs.

This article explains how to use the push REST API to index document-level permissions' metadata in Azure AI Search. This process prepares your index to query and enforce end-user permissions on search results.

## Prerequisites

- Content with ACL metadata from [Microsoft Entra ID](/entra/fundamentals/whatis) or another POSIX-style ACL system. 

- The [latest preview REST API](/rest/api/searchservice/documents/?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or a preview Azure SDK package providing equivalent features.

- An index schema with a `permissionFilterOption` enabled, plus `permissionFilter` field attributes that store the permissions associated with the document.

## Limitations

- An ACL field with permission filter type `userIds` or `groupIds` can hold at most 1000 values.

- An index can hold at most five unique values among fields of type `rbacScope` on all documents. There's no limit on the number of documents that share the same value of `rbacScope`.

- A preexisting field can be converted into a `permissionFilter` field type for use with built-in ACLs or RBAC metadata filtering. To enable filtering on an existing index, create new fields or modify an existing field to include a `permissionFilter`.

- Only one field of each `permissionFilter` type (one each of `groupIds`, `usersIds`, and `rbacScope`) can exist in an index.

- Each permissionFilter field should have `filterable` set to true.

- This functionality is currently not supported in the Azure portal.

## Create an index with permission filter fields

Indexing document ACLs and RBAC metadata with the REST API requires setting up an index schema that enables permission filters and has fields with permission filter assignments.

First, add a `permissionFilterOption` option. Valid values are `enabled` or `disabled`, and you should set it to `enabled`. You can switch it to `disabled` if you want to turn off the permission filter functionality at the index level.

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

## REST API indexing example

Once you have an index with permission filter fields, you can populate those values using the indexing push API as with any other document fields. Here's an example using the specified index schema, where each document specifies the upload action, the key field (DocumentId), and permission fields. It should also have content, but that field is omitted in this example for brevity.

```https
POST https://exampleservice.search.windows.net/indexes('indexdocumentsexample')/docs/search.index?api-version=2025-11-01-preview
{
  "value": [
    {
      "@search.action": "upload",
      "DocumentId": "1",
      "UserIds": ["00aa00aa-bb11-cc22-dd33-44ee44ee44ee", "11bb11bb-cc22-dd33-ee44-55ff55ff55ff", "22cc22cc-dd33-ee44-ff55-66aa66aa66aa"],
      "GroupIds": ["none"]
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

This section explains how document access is determined for a user based on the ACL values assigned to each document. The key rule is that *a user only needs to match one ACL type to gain access to the document*. For example, if a document has fields for `userIds`, `groupIds`, and `rbacScope`, the user can access the document by matching any one of these ACL fields.

### Special ACL values "all" and "none"

ACL fields, such as `userIds` and `groupIds`, typically contain lists of GUIDs (Globally Unique Identifiers) that identify the users and groups with access to the document. Two special string values, "all" and "none", are supported for these ACL field types. These values act as broad filters to control access at the global level as showcased in the following table. 

| userIds / groupIds value | Meaning |
| --- | --- |
| ["all"] | Any user can access the document |
| ["none"] | No user can access the document by matching this ACL type |
| [] (empty array) | No user can access the document by matching this ACL type |

Because a user needs to match only one field type, the special value "all" grants public access regardless of the contents of any other ACL field, as all users are matched and granted permission. In contrast, setting `userIds` to "none" or "empty" means no users are granted access to the document _based on their user ID_. It might be possible that they're still granted access by matching their group ID or by RBAC metadata.

### Access control example

This example illustrates how the document access rules are resolved based on the specific document ACL field values. For readability, this scenario uses ACL aliases such as "user1," "group1," instead of GUIDs.

| Document # | userIds | groupIds | RBAC Scope | Permitted users list | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | ["none"] | [] | Empty | No users have access | The values ["none"] and [] behave exactly the same |
| 2 | ["none"] | [] | scope/to/container1 | Users with RBAC permissions to container1 | The value of "none" doesn't block access by matching other ACL fields |
| 3 | ["none"] | ["group1", "group2"] | Empty | Members of group1 or group2 | |
| 4 | ["all"] | ["none"] | Empty | Any user | Any querying user matches the ACL filter "all", so all users have access |
| 5 | ["all"] | ["group1", "group2"] | scope/to/container1 | Any user | Since all users match the "all" filter for userID, the groupID and RBAC filters don't have any impact |
| 6 | ["user1", "user2"] | ["group1"] | Empty | User1, user2, or any member of group1 | |
| 7 | ["user1", "user2"] | [] | Empty | User1, user2, or any user with RBAC permissions to container1 | |

## See also

- [Connect to Azure AI Search using roles](search-security-rbac.md)
- [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
- [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API)
