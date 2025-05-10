---  
title: Document-level access control    
titleSuffix: Azure AI Search    
description: Conceptual overview of document-level permissions in Azure AI Search    
ms.service: azure-ai-search    
ms.topic: conceptual    
ms.date: 05/10/2025    
author: gmndrg    
ms.author: gimondra    
---  
  
# Document-level access control in Azure AI Search  
  
Azure AI Search offers support for document-level access control, enabling organizations to enforce fine-grained permissions seamlessly, from data ingestion through query execution. This capability is essential for building secure AI agentic systems grounding data, Retrieval-Augmented Generation (RAG) applications, and enterprise search solutions while maintaining compliance and user trust.  
  
Document-level access helps restrict content visibility to authorized users, based on predefined access rules. Azure AI Search supports this functionality through multiple approaches, providing flexibility for integration. 
  
## Overview of document-level access control features  
  
Azure AI Search provides document-level access control in the following ways:  
  
### 1. Native support for integration with Microsoft ENTRA-based POSIX-style Access Control List (ACL) systems (preview)  
  
#### During data ingestion process  
Azure AI Search enables you to push document permissions directly into the search index alongside the content, enabling consistent application of access rules at query time. This is achieved in two ways:  
  
**a. REST API and SDK integration**    
You can use the [REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview) or supported SDKs to [push documents and their associated permission metadata](search-index-access-control-lists-and-rbac-push-api.md)into the search index. This approach is ideal for systems with [Microsoft ENTRA](/entra/fundamentals/what-is-entra)-based [Access Control Lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control) and [Role-based access control (RBAC) roles](/azure/role-based-access-control/overview), such as [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction). By embedding ACLs and RBAC container metadata within the index, developers can reduce the need for custom security trimming logic during query execution.      
  
**b. Built-in ADLS Gen2 indexers**    
If you're using ADLS Gen2 as your data source, [Azure AI Search's built-in indexer](search-indexer-access-control-lists-and-role-based-access.md) simplify data ingestion. This indexer pulls ACLs and RBAC roles at container level during the data ingestion process, enabling a low/no-code workflow for managing document-level permissions.  
  
#### At query time    
With native [token-based querying](https://aka.ms/azs-query-preserving-permissions), Azure AI Search validates a user's [Microsoft ENTRA token](/entra/identity/devices/concept-tokens-microsoft-entra-id) to enforce ACLs and RBAC roles automatically. This functionality helps trim result sets to include only documents the user is authorized to access. You can achieve this by attaching the user's ENTRA token to your query request: No additional custom filter logic is required.    

  
### 2. Security trimming via filters  
  
For scenarios where native ACL and RBAC integration isn't supported, Azure AI Search enables [security trimming using query filters](search-security-trimming-for-azure-search.md). By creating a field in the index to represent user or group identities, you can use the filters to include or exclude documents from query results based on those identities. This approach is useful for systems with custom access models or non-Microsoft ENTRA-based security frameworks.    

## Benefits of document-level access control  
  
Document-level access control is critical for safeguarding sensitive information in AI-driven applications. It helps organizations build systems that align with their access policies, reducing the risk of exposing unauthorized or confidential data. By integrating access rules directly into the search pipeline, AI systems can provide responses grounded in secure and authorized information.  
  
By offloading permission enforcement to Azure AI Search, developers can focus on building high-quality retrieval and ranking systems without the complexity of managing nested groups, custom filter logic, or manual security trimming. This reduces development time and allows teams to prioritize user experience and application functionality.  
  
Document-level permissions in Azure AI Search provide a structured framework for enforcing access controls that align with organizational policies. By leveraging Microsoft ENTRA-based ACLs and RBAC roles, organizations can create systems that support audit-ready compliance and promote trust among users. These built-in capabilities reduce the need for custom coding, offering a standardized approach to document-level security.  

## Reference documents  
  
To help you dive deeper into document-level access control in Azure AI Search, here’s a table of key resources:  
  
| Topic | Reference |  
|-------|-------------|------|  
| **Index permissions using REST API** | Using the REST API to push permission metadata into the search index. | [Index permissions using REST API](search-index-access-control-lists-and-rbac-push-api.md) |  
| **Index ADLS Gen2 permissions metadata using built-in indexers** | Using built-in ADLS Gen2 indexer to ingest ACLs and RBAC role metadata during data crawling. | [Index permissions using ADLS Gen2 idexer](search-indexer-access-control-lists-and-role-based-access.md) |  
| **Query using ENTRA token-based permissions** | Using a Microsoft ENTRA token to enforce ACL and RBAC permissions at query time. | [Query using ENTRA token-based permissions](https://aka.ms/azs-query-preserving-permissions) |  
| **Security trimming via filters** | Trim search results based on user or group identity. | [Security trimming via filters](search-security-trimming-for-azure-search.md) |  
 
  
  
## Next steps  
  
- [Tutorial: Index ADLS Gen2 permissions metadata](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)  