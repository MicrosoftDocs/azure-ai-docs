---
title: Delete Documents
titleSuffix: Azure AI Search
description: Learn how to delete documents in a search index using the REST APIs or an Azure SDK.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 01/20/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Delete documents in a search index

This article explains how to delete whole documents from a search index on Azure AI Search using REST APIs or Azure SDKs. It covers these tasks:

+ Understand when manual deletion is required
+ Identify specific documents to delete
+ Get document counts and storage metrics
+ Delete a single or orphaned document
+ Delete documents in bulk
+ Confirm deletion

> [!TIP]
> For a quick single-document delete, skip to [Delete a single document](#delete-a-single-document).

## Prerequisites

+ An Azure AI Search service (any tier). [Create a service](search-create-service-portal.md) or [find an existing one](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

+ An existing search index with documents to delete. This article assumes you already [created an index](search-how-to-create-search-index.md) and [loaded documents](search-how-to-load-search-index.md).

+ Permissions to delete documents:
  + **Key-based authentication**: An [admin API key](search-security-api-keys.md) for your search service.
  + **Role-based authentication**: [Search Index Data Contributor](search-security-rbac.md) role or the `Microsoft.Search/searchServices/indexes/documents/delete` permission.

+ For SDK development, install the Azure Search client library:
  + Python: [azure-search-documents](https://pypi.org/project/azure-search-documents/)
  + .NET: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
  + JavaScript: [@azure/search-documents](https://www.npmjs.com/package/@azure/search-documents)
  + Java: [azure-search-documents](https://central.sonatype.com/artifact/com.azure/azure-search-documents)

## Understand when manual deletion is required

Manual document deletion is necessary when you use the [push mode approach to indexing](search-what-is-data-import.md#pushing-data-to-an-index), where application code handles data import and drives indexing.

You also need manual document deletion if you use [Logic Apps to load an index (preview)](search-how-to-index-logic-apps.md#limitations).

You might also need manual document deletion in indexer-driven workloads if search documents become "orphaned" from source documents. An important benefit of indexers is automated content retrieval and synchronization via the change and deletion detection features of the target data source. All of the supported data sources provide some level of detection. But in some cases, synchronized deletion is predicated on a soft-delete strategy where you flag a source document (or record) for deletion, run the indexer to delete the indexed content, and only after the index is updated do you physically delete the source content. If source content is deleted first, you have *orphan documents* in the search index. You must manually delete orphan documents in your index to re-establish parity between source and indexed content.

The following links provide more information about change and deletion detection for each data source in indexer-driven workloads.

+ [Azure Storage](search-how-to-index-azure-blob-changed-deleted.md)
+ [Azure SQL](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows)
+ [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md#indexing-deleted-documents)
+ [Azure Database for MySQL (preview)](search-how-to-index-mysql.md#indexing-deleted-rows)
+ [SharePoint indexer](search-how-to-index-sharepoint-online.md)
+ [OneLake indexer](search-how-to-index-onelake-files.md#supported-tasks)

## Identify specific documents for deletion

All documents are uniquely identified by a [document key](search-how-to-create-search-index.md#document-keys) in a search index. To delete a document, you must identify which field is the document key and provide the key on the deletion request.

In the Azure portal, you can view the fields of each index. Document keys are string fields and are denoted with a key icon to make them easier to spot.

### Find the document key

Once you know which field is the document key, you can get the key value by running a query that returns the key field in the search results.

In this example, the search string is used to find the document in the index, and the select statement determines what fields are in the results. The "HotelId" is the document key in this example. 

```http
POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "this query has terms that pertain to the document I want to delete",
    "select": "HotelName, HotelId",
    "count": true
}
```

Results for this keyword search are the top 50 by default. If the document you want to delete satisfies the search criteria, you should see it (and it's key) in the results. Make sure the query includes a descriptive field that helps you confirm you have the correct document.

```json
{
  "@odata.count": 50,
  "value": [
    {
      "@search.score": 4.5116634,
      "HotelId": "18",
      "HotelName": "Ocean Water Resort & Spa"
    }
   ...
  ]
}
```

A simple string is straightforward, but if the index uses a base-64 encoded field, or if search documents were generated from a `parsingMode` setting, you might be working with values that you aren't familiar with. If you're working with chunked documents create by an indexer, the document key is often a generated "chunked_id" composed of a long sequence of numbers and letters.

## Look up a specific document

Now that you have the document key, run a [look up query](/rest/api/searchservice/documents/get) that retrieves the entire document. If the document is a chunk, you should see the ID of the parent document. The document key is included as a query parameter.

The first example returns the hotel having a document key value of `18`.

```http
GET https://[service name].search.windows.net/indexes/hotels-sample-index/docs('18')&api-version=2025-09-01
```

The second example returns a chunk document. The "chunk_id" is the document key.

```http
GET https://[service name].search.windows.net/indexes/chunking-example-index/docs('aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb')&api-version=2025-09-01
```

The response from the second example includes all fields, which you should review to ensure you know what you're deleting. Fields that include parent information are useful if you need to manually reindex a single parent document into constituent chunked documents in the search index.

```json
{
  "chunk_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
  "parent_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
  "chunk": "Unpopulated Slopes of an Active Volcano\u2014Naples, Italy ... 90\n\nDazzling Coastlines\u2014Italy ... .92\n\nLiving on Fertile Land\u2014Nile River, Egypt  ... 94\n\n\n\n vii",
  "title": "earth_at_night_508.pdf",
  "text_vector": [ <omitted> ]
}
```

> [!TIP]
> Use a [REST client](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=rest#query-the-index), an Azure SDK client library, or a [command line tool](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=powershell#query-the-index) to run a lookup query. The Azure portal doesn't support GET requests for a query.

## Get document counts and storage metrics

Before you delete documents, get initial metrics for the index document count and storage so that you can confirm deletion later.

You can get document counts and index storage using:

+ The Azure portal, under **Search management** > **Indexes**.
+ The [Indexes - Get Statistics](/rest/api/searchservice/indexes/get-statistics) REST API

Here's an example response:

```json
{
  "documentCount": 12,
  "storageSize": 123456,
  "vectorIndexSize": 123456
}
```

## Delete a single document

### [**REST**](#tab/rest)

1. Use the [Documents - Index](/rest/api/searchservice/documents) REST API with a delete `@search.action` to remove it from the search index. 

1. Formulate a POST call specifying the index name and the `docs/index` endpoint. 

1. Make sure the body of the request includes the key of the document you want to delete.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key]
    
    {  
      "value": [  
        {  
          "@search.action": "delete",  
          "id": "18"  
        }  
      ]  
    }
    ```

1. Send the request.

   The following table explains the various per-document [status codes](/rest/api/searchservice/http-status-codes) that can be returned in the response. Some status codes indicate problems with the request itself, while others indicate temporary error conditions. The latter you should retry after a delay.

   |Status code|Meaning|Retryable|Notes|
   |-----------|-------|---------|-----| 
   |200|Document was successfully deleted.|n/a|Delete operations are [idempotent](https://en.wikipedia.org/wiki/Idempotence). That is, even if a document key doesn't exist in the index, attempting a delete operation with that key results in a 200 status code.|
   |400|There was an error in the document that prevented it from being deleted.|No|The error message in the response provides details.|
   |422|The index is temporarily unavailable because it was updated with the 'allowIndexDowntime' flag set to 'true'.|Yes|Wait for index to become available.|
   |503|Your search service is temporarily unavailable, possibly due to heavy load.|Yes|Your code should wait before retrying in this case or you risk prolonging the service unavailability.|

   > [!NOTE]  
   > If your client code frequently encounters a 207 response, one possible reason is that the system is under load. You can confirm this by checking the `statusCode` property for 503. If so, we recommend throttling indexing requests. Otherwise, if indexing traffic doesn't subside, the system could start rejecting all requests with 503 errors.  

1. You can resend the [Lookup query](/rest/api/searchservice/documents/get) to confirm the deletion. You should get a 404 document not found message. 

    ```http
    GET https://[service name].search.windows.net/indexes/hotel-sample-index/docs/18?api-version=2025-09-01
    ```

**Reference:** [Documents - Index](/rest/api/searchservice/documents)

A successful delete request returns HTTP 200 (OK). The response body contains status for each document:

```json
{
    "value": [
        { "key": "18", "status": true, "statusCode": 200 }
    ]
}
```

### [**Python**](#tab/sdk-python)

The following example deletes a document from an index:

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Set up the client
service_name = "<your-search-service-name>"
index_name = "hotels-sample-index"
api_key = "<your-admin-api-key>"

endpoint = f"https://{service_name}.search.windows.net"
credential = AzureKeyCredential(api_key)
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Delete a document by key
result = client.delete_documents(documents=[{"HotelId": "18"}])
print(f"Deleted {len(result)} document(s)")
```

**Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [delete_documents](/python/api/azure-search-documents/azure.search.documents.searchclient#azure-search-documents-searchclient-delete-documents)

### [**C#**](#tab/sdk-csharp)

The following example deletes a document from an index:

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

// Set up the client
string serviceName = "<your-search-service-name>";
string indexName = "hotels-sample-index";
string apiKey = "<your-admin-api-key>";

Uri endpoint = new Uri($"https://{serviceName}.search.windows.net");
AzureKeyCredential credential = new AzureKeyCredential(apiKey);
SearchClient searchClient = new SearchClient(endpoint, indexName, credential);

// Delete a document by key
var batch = IndexDocumentsBatch.Delete("HotelId", new[] { "18" });
IndexDocumentsResult result = await searchClient.IndexDocumentsAsync(batch);

Console.WriteLine($"Deleted {result.Results.Count} document(s)");
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync), [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch)

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for document deletion:

+ [IndexDocumentsBatch](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

**Reference:** [SearchClient](/javascript/api/@azure/search-documents/searchclient), [IndexDocumentsBatch](/javascript/api/@azure/search-documents/indexdocumentsbatch)

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for document deletion:

+ [IndexActionType](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

Code sample: [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [IndexActionType](/java/api/com.azure.search.documents.models.indexactiontype)

---

## Delete documents in bulk

### [**REST**](#tab/rest)

1. Use the [Documents - Index](/rest/api/searchservice/documents) REST API with a delete `@search.action` to remove it from the search index. Formulate a POST call specifying the index name and the `docs/index` endpoint.

1. Make sure the body of the request includes the keys of all of the documents you want to delete.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key]
    
    {
      "value": [
        {
          "@search.action": "delete",
          "id": "doc1"
        },
        {
          "@search.action": "delete",
          "id": "doc2"
        }
      ]
    }
    ```

+ **Batch limits**: It is recommended to limit batches to 1,000 documents or roughly 16 MB per request to ensure optimal performance.

+ **Idempotency**: Deletion is idempotent; if you attempt to delete a document ID that does not exist, the API will still return a 200 OK status.

+ **Latency**: Documents are not always removed instantly from storage. A background process performs the physical deletion every few minutes.

+ **Vector storage**: Deleting documents does not immediately free up vector storage quotas. It takes several minutes for physical deletion. For immediate reclamation of vector space, you may need to drop and rebuild the index.

**Reference:** [Documents - Index](/rest/api/searchservice/documents)

### [**Python**](#tab/sdk-python)

The following example deletes multiple documents in bulk:

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Set up the client
service_name = "<your-search-service-name>"
index_name = "hotels-sample-index"
api_key = "<your-admin-api-key>"

endpoint = f"https://{service_name}.search.windows.net"
credential = AzureKeyCredential(api_key)
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Delete multiple documents by key
documents_to_delete = [
    {"HotelId": "doc1"},
    {"HotelId": "doc2"},
    {"HotelId": "doc3"}
]
result = client.delete_documents(documents=documents_to_delete)
print(f"Deleted {len(result)} document(s)")
```

**Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [delete_documents](/python/api/azure-search-documents/azure.search.documents.searchclient#azure-search-documents-searchclient-delete-documents)

### [**C#**](#tab/sdk-csharp)

The following example deletes multiple documents in bulk:

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

// Set up the client
string serviceName = "<your-search-service-name>";
string indexName = "hotels-sample-index";
string apiKey = "<your-admin-api-key>";

Uri endpoint = new Uri($"https://{serviceName}.search.windows.net");
AzureKeyCredential credential = new AzureKeyCredential(apiKey);
SearchClient searchClient = new SearchClient(endpoint, indexName, credential);

// Delete multiple documents by key
var batch = IndexDocumentsBatch.Delete("HotelId", new[] { "doc1", "doc2", "doc3" });
IndexDocumentsResult result = await searchClient.IndexDocumentsAsync(batch);

Console.WriteLine($"Deleted {result.Results.Count} document(s)");
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync), [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch)

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for bulk document deletion:

+ [IndexDocumentsBatch](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

**Reference:** [SearchClient](/javascript/api/@azure/search-documents/searchclient), [IndexDocumentsBatch](/javascript/api/@azure/search-documents/indexdocumentsbatch)

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for bulk document deletion:

+ [IndexActionType](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

Code sample: [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [IndexActionType](/java/api/com.azure.search.documents.models.indexactiontype)

---

## Verify document deletion

After deleting documents, verify the deletion was successful.

### [**Portal**](#tab/verify-portal)

1. In the Azure portal, open the search service **Overview** page.
1. Select **Search management** > **Indexes**.
1. Check the **Document count** column for your index.
1. Wait a few minutes and refresh if the count hasn't changed (deletion is asynchronous).

### [**REST**](#tab/verify-rest)

Use the [Get Document](/rest/api/searchservice/documents/get) API to confirm the document no longer exists:

```http
GET https://[service-name].search.windows.net/indexes/hotels-sample-index/docs/18?api-version=2025-09-01
api-key: [admin-key]
```

Expected response: HTTP 404 Not Found if the document was deleted successfully.

You can also check index statistics:

```http
GET https://[service-name].search.windows.net/indexes/hotels-sample-index/stats?api-version=2025-09-01
api-key: [admin-key]
```

### [**SDK**](#tab/verify-sdk)

```python
# Python - verify document was deleted
try:
    document = client.get_document(key="18")
    print("Document still exists")
except Exception as e:
    print(f"Document not found (expected): {e}")
```

```csharp
// C# - verify document was deleted
try
{
    var document = await searchClient.GetDocumentAsync<Hotel>("18");
    Console.WriteLine("Document still exists");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Document not found (expected)");
}
```

---

Deleting a document doesn't immediately free up space in the index. Every few minutes, a background process performs the physical deletion. Whether you use the Azure portal or the Get Statistics API to return index statistics, you can expect a small delay before the deletion is reflected in the Azure portal and API metrics.

## Troubleshoot document deletion

The following table lists common issues when deleting documents and how to resolve them.

| Issue | Cause | Resolution |
| ----- | ----- | ---------- |
| Document count unchanged | Deletion is asynchronous. Background process runs every few minutes. | Wait 2-3 minutes and refresh. Check index statistics again. |
| 400 Bad Request | Invalid document key or malformed request body. | Verify the document key field name matches your index schema. Check JSON syntax. |
| 403 Forbidden | Insufficient permissions. | Use an admin API key or ensure your identity has Search Index Data Contributor role. |
| 404 Not Found on index | Index name is incorrect or doesn't exist. | Verify the index name in your request URL. |
| Storage not reclaimed | Physical deletion happens asynchronously in background. | Wait several minutes. For immediate vector storage reclamation, drop and rebuild the index. |
| Orphaned documents remain | Source documents deleted before indexer ran with deletion detection. | Manually delete orphaned documents using their document keys. |

## See also

+ [Documents - Index (REST API)](/rest/api/searchservice/documents)
+ [Indexes - Get Statistics (REST API)](/rest/api/searchservice/indexes/get-statistics)
+ [Load documents into a search index](search-how-to-load-search-index.md)
+ [Create a search index](search-how-to-create-search-index.md)
