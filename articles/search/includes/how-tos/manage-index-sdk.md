---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/03/2025
---

After you [create an index](../../search-how-to-create-search-index.md), you can use the Azure SDK for [.NET](/dotnet/api/overview/azure/search), [Java](/java/api/overview/azure/search-documents-readme), [JavaScript](/javascript/api/overview/azure/search-documents-readme), or [Python](/python/api/overview/azure/search-documents-readme) to access its statistics and definition or remove it from your search service.

This article describes how to manage an index without affecting its content. For guidance on modifying an index definition, see [Update or rebuild an index in Azure AI Search](../../search-howto-reindex.md).

## Limitations

The pricing tier of your search service determines the maximum number and size of your indexes, fields, and documents. For more information, see [Service limits in Azure AI Search](../../search-limits-quotas-capacity.md).

Otherwise, the following limitations apply to index management:

+ You can't take an index offline for maintenance. Indexes are always available for search operations.

+ You can't directly copy or duplicate an index within or across search services. However, you can use the backup and restore sample for [.NET](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) or [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) to achieve similar functionality.

## View all indexes

Use your preferred Azure SDK to retrieve all indexes on your search service.

### [.NET](#tab/list-dotnet)

The Azure SDK for .NET provides [GetIndexesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getindexesasync) for this task.

```csharp
// Create a SearchIndexClient
var endpoint = new Uri("[service endpoint]");
var credential = new AzureKeyCredential("[admin key]");
var indexClient = new SearchIndexClient(endpoint, credential);

// List all indexes
await foreach (var index in indexClient.GetIndexesAsync())
{
    Console.WriteLine(index.Name);
}
```

### [Java](#tab/list-java)

The Azure SDK for Java provides `listIndexes` in the [SearchIndexAsyncClient](/java/api/com.azure.search.documents.indexes.searchindexasyncclient) class for this task.

```java
// Create a SearchIndexAsyncClient
String endpoint = "[service endpoint]";
String adminKey = "[admin key]";
SearchIndexAsyncClient searchIndexAsyncClient = new SearchIndexClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(adminKey))
    .buildAsyncClient();
        
// List all indexes
searchIndexAsyncClient.listIndexes()
    .subscribe(
        index -> System.out.println(index.getName())
    );
```

### [JavaScript](#tab/list-javascript)

The Azure SDK for JavaScript provides `listIndexes` in the [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient) class for this task.

```javascript
// Create a SearchIndexClient
const endpoint = "[service endpoint]";
const adminKey = "[admin key]";
const client = new SearchIndexClient(endpoint, new AzureKeyCredential(adminKey)
);

// List all indexes
(async () => {
    for await (const index of client.listIndexes()) {
        console.log(index.name);
    }
})();
```

### [Python](#tab/list-python)

The Azure SDK for Python provides `list_indexes` in the [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient) class for this task.

```python
# Create a SearchIndexClient
endpoint = "[service endpoint]"
admin_key = AzureKeyCredential("[admin key]")
client = SearchIndexClient(endpoint=endpoint, credential=admin_key)

# List all indexes
for index in client.list_indexes():
    print(index.name)
```

---

## View an index's statistics

Use your preferred Azure SDK to retrieve the document count, storage usage, and vector storage usage of an index.

### [.NET](#tab/stats-dotnet)

The Azure SDK for .NET provides [GetIndexStatisticsAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getindexstatisticsasync) for this task.

```csharp
// Create a SearchIndexClient
var endpoint = new Uri("[service endpoint]");
var credential = new AzureKeyCredential("[admin key]");
var indexClient = new SearchIndexClient(endpoint, credential);

// Get index statistics
var statsResponse = await indexClient.GetIndexStatisticsAsync("[index name]");
var stats = statsResponse.Value;
Console.WriteLine($"Number of documents: {stats.DocumentCount:N0}");
Console.WriteLine($"Storage consumed by index: {stats.StorageSize:N0} bytes");
Console.WriteLine($"Storage consumed by vectors: {stats.VectorIndexSize:N0} bytes");
```

### [Java](#tab/stats-java)

The Azure SDK for Java provides `getIndexStatistics` in the [SearchIndexAsyncClient](/java/api/com.azure.search.documents.indexes.searchindexasyncclient) class for this task.

```java
// Create a SearchIndexAsyncClient
String endpoint = "[service endpoint]";
String adminKey = "[admin key]";
SearchIndexAsyncClient searchIndexAsyncClient = new SearchIndexClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(adminKey))
    .buildAsyncClient();

// Get index statistics
SearchIndexStatistics stats = searchIndexAsyncClient.getIndexStatistics("[index name]").block();
System.out.println("Number of documents: " + stats.getDocumentCount());
System.out.println("Storage consumed by index: " + stats.getStorageSize() + " bytes");
System.out.println("Storage consumed by vectors: " + stats.getVectorIndexSize() + " bytes");
```

### [JavaScript](#tab/stats-javascript)

The Azure SDK for JavaScript provides `getIndexStatistics` in the [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient) class for this task.

```javascript
// Create a SearchIndexClient
const endpoint = "[service endpoint]";
const adminKey = "[admin key]";
const client = new SearchIndexClient(endpoint, new AzureKeyCredential(adminKey)
);

// Get index statistics
(async () => {
    const stats = await client.getIndexStatistics("[index name]");
    console.log(`Number of documents: ${stats.documentCount}`);
    console.log(`Storage consumed by index: ${stats.storageSize} bytes`);
    console.log(`Storage consumed by vectors: ${stats.vectorIndexSize} bytes`);
})();
```

### [Python](#tab/stats-python)

The Azure SDK for Python provides [get_index_statistics](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient) for this task.

```python
# Create a SearchIndexClient
endpoint = "[service endpoint]"
admin_key = AzureKeyCredential("[admin key]")
client = SearchIndexClient(endpoint=endpoint, credential=admin_key)

# Get index statistics
stats = client.get_index_statistics("[index name]")
print(f"Number of documents: {stats['document_count']}")
print(f"Storage consumed by index: {stats['storage_size']} bytes")
print(f"Storage consumed by vectors: {stats['vector_index_size']} bytes")
```

---

## View an index's definition

Each index is defined by fields and optional components that enhance search capabilities, such as analyzers, normalizers, tokenizers, and synonym maps. This definition determines the index's structure and behavior during indexing and querying.

Use your preferred Azure SDK to retrieve the JSON definition of an index.

### [.NET](#tab/definition-dotnet)

The Azure SDK for .NET provides [GetIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getindexasync) for this task.

```csharp
// Create a SearchIndexClient
var endpoint = new Uri("[service endpoint]");
var credential = new AzureKeyCredential("[admin key]");
var indexClient = new SearchIndexClient(endpoint, credential);

// Get index definition
var index = await indexClient.GetIndexAsync("[index name]");
string indexJson = JsonSerializer.Serialize(index.Value, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine(indexJson);
```

### [Java](#tab/definition-java)

The Azure SDK for Java provides `getIndex` in the [SearchIndexAsyncClient](/java/api/com.azure.search.documents.indexes.searchindexasyncclient) class for this task.

```java
// Create a SearchIndexAsyncClient
String endpoint = "[service endpoint]";
String adminKey = "[admin key]";
SearchIndexAsyncClient searchIndexAsyncClient = new SearchIndexClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(adminKey))
    .buildAsyncClient();

// Get index definition
searchIndexAsyncClient.getIndex("[index name]")
    .subscribe(index -> {
        try {
            String prettyJson = new ObjectMapper()
                .writerWithDefaultPrettyPrinter()
                .writeValueAsString(index);
            System.out.println(prettyJson);
        } catch (Exception e) {
            e.printStackTrace();
        }
    });
```

### [JavaScript](#tab/definition-javascript)

The Azure SDK for JavaScript provides `getIndex` in the [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient) class for this task.

```javascript
// Create a SearchIndexClient
const endpoint = "[service endpoint]";
const adminKey = "[admin key]";
const client = new SearchIndexClient(endpoint, new AzureKeyCredential(adminKey)
);

// Get index definition
(async () => {
    const index = await client.getIndex("[index name]");
    console.log(JSON.stringify(index, null, 2));
})();
```

### [Python](#tab/definition-python)

The Azure SDK for Python provides `get_index` in the [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient) class for this task.

```python
# Create a SearchIndexClient
endpoint = "[service endpoint]"
admin_key = AzureKeyCredential("[admin key]")
client = SearchIndexClient(endpoint=endpoint, credential=admin_key)

# Get index definition
index = client.get_index("[index name]")
print(json.dumps(index.as_dict(), indent=2, sort_keys=True, ensure_ascii=False))
```

---

## Delete an index

> [!WARNING]
> You can't undo an index deletion. Before you proceed, make sure that you want to permanently remove the index and its documents from your search service.

Use your preferred Azure SDK to permanently delete an index.

### [.NET](#tab/delete-dotnet)

The Azure SDK for .NET provides [DeleteIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.deleteindexasync) for this task.

```csharp
// Create a SearchIndexClient
var endpoint = new Uri("[service endpoint]");
var credential = new AzureKeyCredential("[admin key]");
var indexClient = new SearchIndexClient(endpoint, credential);

// Delete the index
await indexClient.DeleteIndexAsync("[index name]");
Console.WriteLine("Index deleted successfully.");
```

### [Java](#tab/delete-java)

The Azure SDK for Java provides `deleteIndex` in the [SearchIndexAsyncClient](/java/api/com.azure.search.documents.indexes.searchindexasyncclient) class for this task.

```java
// Create a SearchIndexAsyncClient
String endpoint = "[service endpoint]";
String adminKey = "[admin key]";
SearchIndexAsyncClient searchIndexAsyncClient = new SearchIndexClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(adminKey))
    .buildAsyncClient();

// Delete the index
searchIndexAsyncClient.deleteIndex("[index name]")
    .subscribe(
        unused -> System.out.println("Index deleted successfully.")
    );
```

### [JavaScript](#tab/delete-javascript)

The Azure SDK for JavaScript provides `deleteIndex` in the [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient) class for this task.

```javascript
// Create a SearchIndexClient
const endpoint = "[service endpoint]";
const adminKey = "[admin key]";
const client = new SearchIndexClient(endpoint, new AzureKeyCredential(adminKey)
);

// Delete the index
(async () => {
    await client.deleteIndex("[index name]");
    console.log("Index deleted successfully.");
})();
```

### [Python](#tab/delete-python)

The Azure SDK for Python provides `delete_index` in the [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient) class for this task.

```python
# Create a SearchIndexClient
endpoint = "[service endpoint]"
admin_key = AzureKeyCredential("[admin key]")
client = SearchIndexClient(endpoint=endpoint, credential=admin_key)

# Delete the index
client.delete_index("[index name]")
print("Index deleted successfully.")
```

---
