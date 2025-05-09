---  
title: Indexing ACLs and RBAC using REST API in Azure AI Search  
titleSuffix: Azure AI Search  
description: Learn how to use the REST API for indexing documents with ACLs and RBAC metadata.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 05/08/2025  
author: admayber
ms.author: admayber  
---  

# Indexing Access Control Lists (ACLs) and Role-Based Access Control (RBAC) using REST API in Azure AI Search  

Indexing documents, along with their associated ACLs and container RBAC roles, into an Azure AI Search index via the [REST API](/rest/api/searchservice/) offers fine-grained control over the indexing pipeline. This enables the inclusion of document entries with precise, document-level permissions directly within the index. This article provides an overview of how to leverage the REST API to index Access Control Lists (ACLs) and Role-Based Access Control (RBAC) roles in Azure AI Search to have your index ready to later query and honor end-user permissions.

## Supported Scenarios  
- Indexing ACLs metadata from [ENTRA-based](/en-us/entra/fundamentals/whatis), POSIX-style ACL systems, such as [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction)
- Indexing RBAC container metadata from ADLS Gen2

### Limitations
- An ACL field with permission filter type `userIds` or `groupIds` can hold at most 32 values
- An index can hold at most 5 unique values among fields of type `rbacScope` on all documents. There is no limit on the number of documents that share the same value of `rbacScope`.
- A pre-existing field cannot be converted into a `permissionFilter` field type for use with built-in ACLs / RBAC metadata filtering. To enable filtering on an existing index, new field(s) must be created of the correct permission filter type.
- Only one field of each `permissionFilter` type such as `groupIds`, `usersIds` and `rbacScope` can exist on an index

## Key Features  
- Flexible control over ingestion pipelines.  
- Standardized schema for permissions metadata.  
- Support for hierarchical permissions (e.g., folder-level ACLs). 

## Requirements
- ACLs and RBAC container roles are only supported in API version [2025-05-01-preview](/rest/api/searchservice/documents/?view=rest-searchservice-2025-05-01-preview) and later
- You must create an index which has a schema with `permissionFilterOption` defined to hold the RBAC metadata and / or ACL values as desired (see below for an example) 

## Creating an index with RBAC / ACL fields
Indexing document ACLs and RBAC metadata with the REST API requires setting up an index schema that uses the desired field types for ACLs. See [How to Index Permission Information](tutorial-adls-gen2-indexer-acls.md) for a full walkthrough on how to set up an index with a schema that supports ACLs and RBAC metadata.

Note that permission filter field types can be added to an existing index as well. The value of `permissionFilterOption` can be set to either "enabled" or "disabled" while indexing documents. However, setting it to "disabled" will turn off the permission filter functionality

Here is a basic example schema that includes both user and group ACLs as well as RBAC metadata:

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
Once you have an index with the desired permission filter fields, you can populate those values using the Indexing Push API as with any other document fields. Here is an example using the above index schema:

```https
POST https://exampleservice.search.windows.net/indexes('indexdocumentsexample')/docs/search.index?api-version=2025-05-01-preview
{
  "value": [
    {
      "@search.action": "upload",
      "DocumentId": "1",
      "UserIds": ["dff329dc-0c65-424c-a77d-13f5f6d17145", "f2e63ece-1190-4366-a3d1-67f623a57b2b", "cb1d2c74-0ffb-40bc-9774-869e5375867c"],
      "GroupIds": ["none"]
      "RbacScope": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/Example-Storage-rg/providers/Microsoft.Storage/storageAccounts/azurestorage12345/blobServices/default/containers/blob-container-01"
    },
    {
      "@search.action": "merge",
      "DocumentId": "2",
      "UserIds": ["all"],
      "GroupIds": ["cca97cfc-5ee0-4b49-ac72-3134f58c1898", "9fc8129f-cd4e-4609-abe1-0df360661243"]
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
This section explains how document access is evaluated for a given user based on the values of the ACLs of each document. The most important rule is that **a user only needs to "match" one ACL type in order to be granted access to the document.** That is to say, if a document has a field each of type `userIds`, `groupIds`, and `rbacScope`, a user will be permitted access to the document so long as they match at least one of these ACL fields.

### Special ACL values "all` and "none"
ACL fields of type `userIds` and `groupIds` will usually contain lists of GUIDs identifying users and groups that have access to the document. We also support two special string values that can be in these ACL field types: "all" and "none". They are used as broad filters to control access at the global level. See table below for reference.

| userIds / groupIds value | Meaning |
| --- | --- |
| ["all"] | Any user can access the document |
| ["none"] | No user can access the document by matching this ACL type |
| [] (empty array) | No user can access the document by matching this ACL type |

Note that because a user needs to only match one field type, the special value `all` grants public access regardless of the contents of any other ACL field since all users will be matched and granted permission. In contrast, for example, setting userIds to the value `["none"]` or `[]` simply means that no users will be granted access to the document _based on their user ID_. It might be possible that they are still granted access by matching their group ID or by RBAC metadata.

### Access control example
The below example illustrates how the document access rules are resolved based on the specific document ACL field values. For readability, in this example we will use ACL aliases such as "user1", "group1", etc. in place of GUIDs.

| Document # | userIds | groupIds | RBAC Scope | Permitted users list | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | ["none"] | [] | Empty | No users have access | The values ["none"] and [] behave exactly the same |
| 2 | ["none"] | [] | scope/to/container1 | Users with RBAC permissions to container1 | The value of "none" does not block access by matching other ACL fields |
| 3 | ["none"] | ["group1", "group2"] | Empty | Members of group1 or group2 | |
| 4 | ["all"] | ["none"] | Empty | Any user | Any querying user will match the ACL filter "all", so all users have access |
| 5 | ["all"] | ["group1", "group2"] | scope/to/container1 | Any user | Since all users match the "all" filter for userID, the groupID and RBAC filters don't have any impact |
| 5 | ["user1", "user2"] | ["group1"] | Empty | User1, user2, or any member of group1 | |
| 5 | ["user1", "user2"] | [] | Empty | User1, user2, or any user with RBAC permissions to container1 | |

## Next Steps
[How to query the index using end user ENTRA-token to enforce document-level permissions](https://aka.ms/azs-query-preserving-permissions)
[How to index ADLS Gen2 document-level permission information using indexers](tutorial-adls-gen2-indexer-acls.md)
