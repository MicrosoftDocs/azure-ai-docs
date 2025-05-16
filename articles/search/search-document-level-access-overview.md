---  
title: Document-level access control    
titleSuffix: Azure AI Search    
description: Conceptual overview of document-level permissions in Azure AI Search.    
ms.service: azure-ai-search    
ms.topic: conceptual    
ms.date: 05/19/2025    
author: gmndrg    
ms.author: gimondra    
---  
  
# Document-level access control in Azure AI Search  
  
Azure AI Search offers support for document-level access control, enabling organizations to enforce fine-grained permissions seamlessly, from data ingestion through query execution. This capability is essential for building secure AI agentic systems grounding data, Retrieval-Augmented Generation (RAG) applications, and enterprise search solutions while maintaining compliance and user trust.  
  
Document-level access helps restrict content visibility to authorized users, based on predefined access rules. Azure AI Search supports this functionality through multiple approaches, providing flexibility for integration. 
  
## Feature overview
  
Azure AI Search provides two approaches for document-level access control: native support for permission inheritance (applies to Azure Data Lake Storage (ADLS) Gen2) and security trimming.

### Security trimming via filters  

For scenarios where native ACL and RBAC integration isn't supported, Azure AI Search enables [security trimming using query filters](search-security-trimming-for-azure-search.md). By creating a field in the index to represent user or group identities, you can use the filters to include or exclude documents from query results based on those identities. This approach is useful for systems with custom access models or non-Microsoft Entra-based security frameworks.

### Native support for POSIX-like ACL permissions (preview)

Through Microsoft Entra ID, the [ADLS Gen2 access control model](/azure/storage/blobs/data-lake-storage-access-control-model) supports both Azure role-based access control (Azure RBAC) and POSIX-like access control lists (ACLs). In Azure AI Search using the newest preview APIs, you can flow these permission through to a search index and queries. 

ADLS Gen2 provides ACLs in a format that works well for this approach, but you can use any data source that provides permission data in the same format.
  
#### Retrieve permissions metadata during data ingestion process

Azure AI Search enables you to push document permissions directly into the search index alongside the content, enabling consistent application of access rules at query time. This capability is achieved in two ways:  
  
- Use the [REST API](/rest/api/searchservice/operation-groups) or supported SDKs to [push documents and their associated permission metadata](search-index-access-control-lists-and-rbac-push-api.md) into the search index. This approach is ideal for systems with [Microsoft Entra](/Entra/fundamentals/what-is-Entra)-based [Access Control Lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control) and [Role-based access control (RBAC) roles](/azure/role-based-access-control/overview), such as [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction). By embedding ACLs and RBAC container metadata within the index, developers can reduce the need for custom security trimming logic during query execution.

- For [built-in ADLS Gen2 indexers](search-indexer-access-control-lists-and-role-based-access.md), you can use the preview REST API with the permission filter options to flow existing ACLs and RBAC permissions to your search index. This indexer pulls ACLs and RBAC roles at container level during the data ingestion process, enabling a low/no-code workflow for managing document-level permissions.  
  
#### Enforce document-level permissions at query time

With native [token-based querying](https://aka.ms/azs-query-preserving-permissions), Azure AI Search validates a user's [Microsoft Entra token](/Entra/identity/devices/concept-tokens-microsoft-Entra-id) to enforce ACLs and RBAC roles automatically. This functionality helps trim result sets to include only documents the user is authorized to access. You can achieve automatic trimming by attaching the user's Microsoft Entra token to your query request. For more information, see [Query-Time ACL and RBAC enforcement in Azure AI Search](search-query-access-control-rbac-enforcement.md).

## Benefits of document-level access control  
  
Document-level access control is critical for safeguarding sensitive information in AI-driven applications. It helps organizations build systems that align with their access policies, reducing the risk of exposing unauthorized or confidential data. By integrating access rules directly into the search pipeline, AI systems can provide responses grounded in secure and authorized information.  

By offloading permission enforcement to Azure AI Search, developers can focus on building high-quality retrieval and ranking systems. This approach helps reducing the need to handle nested groups, write custom filters, or manually trim search results.  

Document-level permissions in Azure AI Search provide a structured framework for enforcing access controls that align with organizational policies. By using Microsoft Entra-based ACLs and RBAC roles, organizations can create systems that support robust compliance and promote trust among users. These built-in capabilities reduce the need for custom coding, offering a standardized approach to document-level security.  

## Related content
  
To help you dive deeper into document-level access control in Azure AI Search, here are more articles and samples:  
  
| Functionality                                   | Content |  Sample |
|---|---|---|
| **Index permissions using Push APIs**           | [How to index permissions using REST API](search-index-access-control-lists-and-rbac-push-api.md)  |  [azure-search-rest-samples/Quickstart-ACL](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-ACL) or [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API) |
| **Index ADLS Gen2 permissions metadata using built-in indexers** | [How to index permissions using ADLS Gen2 indexer](search-indexer-access-control-lists-and-role-based-access.md) and [Tutorial: Index ADLS Gen2 permissions metadata using an indexer](tutorial-adls-gen2-indexer-acls.md) |  [azure-search-python-samples/Quickstart-Document-Permissions-Pull-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Pull-API) |
| **Query using Microsoft Entra token-based permissions** | [How to query using Microsoft Entra token-based permissions](https://aka.ms/azs-query-preserving-permissions) | See previous samples. |
| **Security trimming via filters**              | [Security trimming via filters](search-security-trimming-for-azure-search.md)               |  Not available. |
