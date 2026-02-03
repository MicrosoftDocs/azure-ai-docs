---
title: Load an index
titleSuffix: Azure AI Search
description: Import and refresh data in a search index using the Azure portal, REST APIs, or an Azure SDK.
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

# Load data into a search index in Azure AI Search

This article explains how to import documents into a predefined search index using REST APIs, Azure SDKs, or the Azure portal.

> [!TIP]
> For the fastest path to loading data, use the [Import data wizard](search-import-data-portal.md) in the Azure portal, which creates an index and loads it in one workflow.

## Prerequisites

+ An Azure AI Search service (any tier). [Create a service](search-create-service-portal.md) or [find an existing one](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

+ An existing search index. This article assumes you already [created an index](search-how-to-create-search-index.md). If you need to create and load in one step, use an [Import wizard](search-import-data-portal.md) or [indexer](search-indexer-overview.md).

+ Permissions to load documents:
  + **Key-based authentication**: An [admin API key](search-security-api-keys.md) for your search service.
  + **Role-based authentication**: [Search Index Data Contributor](search-security-rbac.md) role on the search service.

+ For SDK development, install the Azure Search client library:
  + .NET: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
  + Python: [azure-search-documents](https://pypi.org/project/azure-search-documents/)
  + JavaScript: [@azure/search-documents](https://www.npmjs.com/package/@azure/search-documents)
  + Java: [azure-search-documents](https://central.sonatype.com/artifact/com.azure/azure-search-documents)

## Use the Azure portal

In the Azure portal, use an [import wizard](search-import-data-portal.md) to create and load indexes in a seamless workflow. If you want to load an existing index, choose an alternative approach.

1. Sign in to the [Azure portal](https://portal.azure.com/) with your Azure account and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** page, select **Import data** or **Import data (new)** on the command bar to create and populate a search index.

   :::image type="content" source="media/search-import-data-portal/import-wizards.png" alt-text="Screenshot of the Import data command." border="true":::

    You can follow these links to review the workflow: [Quickstart: Create an Azure AI Search index](search-get-started-portal.md) and [Quickstart: Integrated vectorization](search-get-started-portal-import-vectors.md).

1. After the wizard is finished, use [Search Explorer](search-explorer.md) to check for results.

> [!TIP]
> The import wizards create and run indexers. If indexers are already defined, you can [reset and run an indexer](search-howto-run-reset-indexers.md) from the Azure portal, which is useful if you're adding fields incrementally. Reset forces the indexer to start over, picking up all fields from all source documents.

## Use the REST APIs

[Documents - Index](/rest/api/searchservice/documents) is the REST API for importing data into a search index. 

The body of the request contains one or more documents to be indexed. Documents are uniquely identified through a case-sensitive key. Each document is associated with an action: "upload", "delete", "merge", or "mergeOrUpload". Upload requests must include the document data as a set of key/value pairs.

REST APIs are useful for initial proof-of-concept testing, where you can test indexing workflows without having to write much code. The `@search.action` parameter determines whether documents are added in full, or partially in terms of new or replacement values for specific fields.

[**Quickstart: Full-text search using REST**](search-get-started-text.md) explains the steps. The following example is a modified version of the example. The value is trimmed for brevity and the first HotelId value is altered to avoid overwriting an existing document.

1. Formulate a POST call specifying the index name, the "docs/index" endpoint, and a request body that includes the `@search.action` parameter.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key] 
    {
        "value": [
        {
        "@search.action": "upload",
        "HotelId": "1111",
        "HotelName": "Stay-Kay City Hotel",
        "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
        "Category": "Boutique",
        "Tags": [ "pool", "air conditioning", "concierge" ]
        },
        {
        "@search.action": "mergeOrUpload",
        "HotelId": "2",
        "HotelName": "Old Century Hotel",
        "Description": "This is description is replacing the original one for this hotel. New and changed values overwrite the previous ones. In a comma-delimited list like Tags, be sure to provide the full list because there is no merging of values within the field itself.",
        "Category": "Boutique",
        "Tags": [ "pool", "free wifi", "concierge", "my first new tag", "my second new tag" ]
        }
      ]
    }
    ```

1. Set the `@search.action` parameter to `upload` to create or overwrite a document. Set it to `merge` or `uploadOrMerge` if you're targeting updates to specific fields within the document. The previous example shows both actions. 

   | Action | Effect |
   |--------|--------|
   | upload | Similar to an "upsert" where the document is inserted if it's new, and updated or replaced if it exists. If the document is missing values that the index requires, the document field's value is set to null. |
   | merge | Updates a document that already exists, and fails a document that can't be found. Merge replaces existing values. For this reason, be sure to check for collection fields that contain multiple values, such as fields of type `Collection(Edm.String)`. For example, if a `tags` field starts with a value of `["budget"]` and you execute a merge with `["economy", "pool"]`, the final value of the `tags` field is `["economy", "pool"]`. It isn't `["budget", "economy", "pool"]`. |
   | mergeOrUpload | Behaves like merge if the document exists, and upload if the document is new. This is the most common action for incremental updates. |
   | delete | Delete removes the specified document from the index. Any field you specify in a delete operation, other than the key field, is ignored. If you want to remove an individual field from a document, use merge instead and set the field explicitly to null. For more information, see [Delete documents in a search index](search-how-to-delete-documents.md).|

   There are no ordering guarantees for which action in the request body is executed first. It's not recommended to have multiple "merge" actions associated with the same document in a single request body. If there are multiple "merge" actions required for the same document, perform the merging client-side before updating the document in the search index.

   In primitive collections, if the document contains a Tags field of type `Collection(Edm.String)` with a value of ["budget"], and you execute a merge with a value of ["economy", "pool"] for Tag, the final value of the Tags field will be ["economy", "pool"]. It isn't ["budget", "economy", "pool"].

   In complex collections, if the document contains a complex collection field named Rooms with a value of [{ "Type": "Budget Room", "BaseRate": 75.0 }], and you execute a merge with a value of [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }], the final value of the Rooms field will be [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }]. It won't be either of the following:

   + [{ "Type": "Budget Room", "BaseRate": 75.0 }, { "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }] (append elements)

   + [{ "Type": "Standard Room", "BaseRate": 75.0 }, { "Type": "Budget Room", "BaseRate": 60.5 }] (merge elements in order, then append any extras)

   > [!NOTE]
   > When you upload DateTimeOffset values with time zone information to your index, Azure AI Search normalizes these values to UTC. For example, 2025-01-13T14:03:00-08:00 will be stored as 2025-01-13T22:03:00Z. If you need to store time zone information, add an extra column to your index.

1. Send the request.

   The following table explains the various per-document [status codes](/rest/api/searchservice/http-status-codes) that can be returned in the response. Some status codes indicate problems with the request itself, while others indicate temporary error conditions. The latter you should retry after a delay.

   |Status code|Meaning|Retryable|Notes|
   |-----------|-------|---------|-----| 
   |200|Document was successfully modified or deleted.|n/a|Delete operations are [idempotent](https://en.wikipedia.org/wiki/Idempotence). That is, even if a document key doesn't exist in the index, attempting a delete operation with that key results in a 200 status code.|
   |201|Document was successfully created.|n/a||
   |400|There was an error in the document that prevented it from being indexed.|No|The error message in the response indicates what is wrong with the document.|
   |404|The document couldn't be merged because the given key doesn't exist in the index.|No|This error doesn't occur for uploads since they create new documents, and it doesn't occur for deletes because they're [idempotent](https://en.wikipedia.org/wiki/Idempotence).|
   |409|A version conflict was detected when attempting to index a document.|Yes|This can happen when you're trying to index the same document more than once concurrently.|
   |422|The index is temporarily unavailable because it was updated with the 'allowIndexDowntime' flag set to 'true'.|Yes||
   |429|Indicates that you have exceeded your quota on the number of documents per index. |No | You must either create a new index or upgrade for higher capacity limits.|
   |503|Your search service is temporarily unavailable, possibly due to heavy load.|Yes|Your code should wait before retrying in this case or you risk prolonging the service unavailability.|

   > [!NOTE]  
   > If your client code frequently encounters a 207 response, one possible reason is that the system is under load. You can confirm this by checking the `statusCode` property for 503. If this is the case, we recommend throttling indexing requests. Otherwise, if indexing traffic doesn't subside, the system could start rejecting all requests with 503 errors.  

1. [Look up the documents](/rest/api/searchservice/documents/get) you just added as a validation step:

    ```http
    GET https://[service name].search.windows.net/indexes/hotel-sample-index/docs/1111?api-version=2025-09-01
    ```

**Reference:** [Documents - Index](/rest/api/searchservice/documents), [Documents - Get](/rest/api/searchservice/documents/get)

A successful index request returns HTTP 200 (OK) for a batch where all documents succeeded, or HTTP 207 (Multi-Status) if some documents failed. The response body contains status for each document:

```json
{
    "value": [
        { "key": "1111", "status": true, "statusCode": 201 },
        { "key": "2", "status": true, "statusCode": 200 }
    ]
}
```

When the document key or ID is new, **null** becomes the value for any field that's unspecified in the document. For actions on an existing document, updated values replace the previous values. Any fields that weren't specified in a "merge" or "mergeUpload" are left intact in the search index.

## Use the Azure SDKs

Programmability is provided in the following Azure SDKs.

### [**Python**](#tab/sdk-python)

The Azure SDK for Python provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBatch](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)

**Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [IndexDocumentsBatch](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch)

Code samples include:

+ [sample_crud_operations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_documents_crud.py)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**C#**](#tab/sdk-csharp)

The Azure SDK for .NET provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync)
+ [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)

The following example uploads documents to an existing index:

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

// Create the search client
string serviceName = "<your-search-service-name>";
string indexName = "hotels-sample-index";
string apiKey = "<your-admin-api-key>";

Uri endpoint = new Uri($"https://{serviceName}.search.windows.net");
AzureKeyCredential credential = new AzureKeyCredential(apiKey);
SearchClient searchClient = new SearchClient(endpoint, indexName, credential);

// Define documents to upload
var documents = new[]
{
    new { HotelId = "1111", HotelName = "Stay-Kay City Hotel", Category = "Boutique" },
    new { HotelId = "1112", HotelName = "Old Century Hotel", Category = "Luxury" }
};

// Upload documents
IndexDocumentsResult result = await searchClient.IndexDocumentsAsync(
    IndexDocumentsBatch.Upload(documents));

Console.WriteLine($"Uploaded {result.Results.Count} documents");
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync), [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch)

There are several samples that illustrate indexing in context of simple and large-scale indexing:

+ [**"Load an index"**](search-howto-dotnet-sdk.md#load-an-index) explains basic steps.

+ [**Azure.Search.Documents Samples - Indexing Documents**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample05_IndexingDocuments.md) from the Azure SDK team adds [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1).

+ [**Tutorial: Index any data**](tutorial-optimize-indexing-push-api.md) couples batch indexing with testing strategies for determining an optimum size.

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBath](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

**Reference:** [SearchClient](/javascript/api/@azure/search-documents/searchclient), [IndexDocumentsBatch](/javascript/api/@azure/search-documents/indexdocumentsbatch)

Code samples include:

+ See this quickstart for basic steps: [Quickstart: Full-text search](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=javascript)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for simple and bulk document uploads into an index:

+ [indexactiontype enumerator](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [IndexDocumentsBatch](/java/api/com.azure.search.documents.indexes.models)

Code samples include:

+ [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

---

## Verify your data load

After loading documents, verify the data is indexed correctly.

### [**Portal**](#tab/verify-portal)

1. In the Azure portal, open the search service **Overview** page.
1. Select **Search explorer** from the command bar.
1. Select your index from the dropdown.
1. Select **Search** to run an empty query that returns all documents.
1. Verify the document count and spot-check field values.

### [**REST**](#tab/verify-rest)

Use the [Get Document](/rest/api/searchservice/documents/get) API to retrieve a specific document by key:

```http
GET https://[service-name].search.windows.net/indexes/hotels-sample-index/docs/1111?api-version=2025-09-01
api-key: [admin-key]
```

Expected response: HTTP 200 with the document JSON if found, or HTTP 404 if the key doesn't exist.

### [**.NET**](#tab/verify-dotnet)

```csharp
// Verify document was indexed
var document = await searchClient.GetDocumentAsync<Hotel>("1111");
Console.WriteLine($"Found: {document.Value.HotelName}");
```

### [**Other SDKs**](#tab/verify-other)

Use the `get_document()` (Python), `getDocument()` (JavaScript/Java) method on the SearchClient to retrieve a document by key.

---

## How data import works

A search service accepts JSON documents that conform to the index schema. A search service can import and index plain text content and vector content in JSON documents.

+ Plain text content is retrieved from fields in the external data source, from metadata properties, or from enriched content that's generated by a [skillset](cognitive-search-working-with-skillsets.md). Skills can extract or infer textual descriptions from images and unstructured content.

+ Vector content is retrieved from a data source that provides it, or it's created by a skillset that implements [integrated vectorization](vector-search-integrated-vectorization.md) in an Azure AI Search indexer workload.

You can prepare these documents yourself, but if content resides in a [supported data source](search-indexer-overview.md#supported-data-sources), running an [indexer](search-indexer-overview.md) or using an Import wizard can automate document retrieval, JSON serialization, and indexing.

Once data is indexed, the physical data structures of the index are locked in. For guidance on what can and can't be changed, see [Update and rebuild an index](search-howto-reindex.md).

Indexing isn't a background process. A search service balances indexing and query workloads, but if [query latency is too high](search-performance-analysis.md#impact-of-indexing-on-queries), you can either [add capacity](search-capacity-planning.md#add-or-remove-partitions-and-replicas) or identify periods of low query activity for loading an index.

For more information, see [Data import strategies](search-what-is-data-import.md).

## Troubleshoot common errors

| Error | Cause | Solution |
|-------|-------|----------|
| HTTP 400 Bad Request | Document contains invalid data or missing required fields | Check the error message for the specific field. Ensure all required fields are present and data types match the index schema. |
| HTTP 404 Not Found (merge) | Attempting to merge a document that doesn't exist | Use `mergeOrUpload` instead of `merge` if the document might not exist. |
| HTTP 409 Conflict | Concurrent updates to the same document | Implement retry logic with exponential backoff. |
| HTTP 413 Payload Too Large | Batch size exceeds limits | Reduce the number of documents per batch. Maximum batch size is 1,000 documents or 16 MB. |
| HTTP 429 Too Many Requests | Quota exceeded | Check your service tier limits. Consider upgrading or creating a new index. |
| HTTP 503 Service Unavailable | Service is under heavy load | Implement retry logic with exponential backoff. Reduce indexing request frequency. |
