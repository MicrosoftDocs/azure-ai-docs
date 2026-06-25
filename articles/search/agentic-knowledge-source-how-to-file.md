---
title: Create a File Knowledge Source for Agentic Retrieval
description: Learn how to create a file knowledge source in Azure AI Search, upload files directly, and use the processed content in a knowledge base.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a file knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *file knowledge source* (preview) uploads small and medium file sets directly to Azure AI Search for agentic retrieval. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

File knowledge sources are useful when you want a managed upload experience instead of provisioning Azure Storage, configuring access, and creating an indexer pipeline over an external container. Azure AI Search processes uploaded files so their extracted content can be retrieved from a knowledge base.

If your content already lives in Azure Blob Storage or ADLS Gen2, or if you need large-scale ingestion or storage account capabilities, use a [blob knowledge source](agentic-knowledge-source-how-to-blob.md) instead.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ A dedicated Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md). File knowledge sources aren't supported on serverless search services. For more information about dedicated tiers, see [Choose a service tier](search-sku-tier.md). If you need paid usage beyond the monthly free allowance, set the `knowledgeRetrieval` service property to `standard` by using the [Search Management REST API](/rest/api/searchmanagement/services/create-or-update).

+ Files in a [supported format](#supported-formats-and-limits).

+ Permissions to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge source specifies an Azure OpenAI model for embeddings, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Supported formats and limits

The following file types are supported.

| Category | Extensions |
|--|--|
| Text | `.txt`, `.md`, `.html`, `.json`, `.csv` |
| Code | `.c`, `.cs`, `.cpp`, `.java`, `.py`, `.js`, `.ts`, `.php`, `.rb`, `.sh` |
| Documents | `.pdf`, `.docx`, `.pptx`, `.doc` |

The following limits apply to file knowledge sources.

| Limit | Value |
|--|--|
| Maximum file size per upload | 50 MB |
| Maximum files per file knowledge source | 100 |

> [!NOTE]
> Uploaded content is stored in the generated search index. For total storage limits by pricing tier, see [Service limits](search-limits-quotas-capacity.md#service-limits).


## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a file knowledge source.

```json
{
  "name": "my-file-ks",
  "kind": "file",
  "description": "A sample file knowledge source.",
  "encryptionKey": null,
  "fileParameters": {
    "ingestionParameters": {
      "contentExtractionMode": "minimal",
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<REDACTED>",
          "deploymentId": "text-embedding-3-large",
          "modelName": "text-embedding-3-large"
        }
      }
    }
  }
}
```

## Create a knowledge source

Create a file knowledge source that specifies the embedding model used to vectorize uploaded content.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var embeddingParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiEmbeddingDeployment,
    ModelName = aoaiEmbeddingModel
};

var ingestionParams = new KnowledgeSourceIngestionParameters
{
    ContentExtractionMode = "minimal",
    EmbeddingModel = new KnowledgeSourceAzureOpenAIVectorizer
    {
        AzureOpenAIParameters = embeddingParams
    }
};

var fileParams = new FileKnowledgeSourceParameters
{
    IngestionParameters = ingestionParams
};

var knowledgeSource = new FileKnowledgeSource(
    name: "my-file-ks",
    fileParameters: fileParams
)
{
    Description = "This knowledge source uses directly uploaded product manuals."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    FileKnowledgeSource,
    FileKnowledgeSourceParameters,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeSourceAzureOpenAIVectorizer,
    KnowledgeSourceIngestionParameters,
)

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

embedding_params = AzureOpenAIVectorizerParameters(
    resource_url="aoai_endpoint",
    deployment_name="aoai_embedding_deployment",
    model_name="aoai_embedding_model",
)

ingestion_params = KnowledgeSourceIngestionParameters(
    content_extraction_mode="minimal",
    embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
        azure_open_ai_parameters=embedding_params
    ),
)

knowledge_source = FileKnowledgeSource(
    name="my-file-ks",
    description="This knowledge source uses directly uploaded product manuals.",
    file_parameters=FileKnowledgeSourceParameters(ingestion_parameters=ingestion_params),
)

index_client.create_or_update_knowledge_source(knowledge_source=knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-url}}/knowledgesources/my-file-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json
Prefer: return=representation

{
  "name": "my-file-ks",
  "kind": "file",
  "description": "This knowledge source uses directly uploaded product manuals.",
  "encryptionKey": null,
  "fileParameters": {
    "ingestionParameters": {
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "{{aoai-endpoint}}",
          "deploymentId": "{{aoai-embedding-deployment}}",
          "modelName": "{{aoai-embedding-model}}"
        }
      },
      "contentExtractionMode": "minimal"
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

For the complete knowledge source request schema, see [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true).

## Upload files

After the knowledge source exists, upload files directly to it. Each upload is a synchronous call: Azure AI Search extracts content from the uploaded file, chunks the content, creates embeddings when needed, and prepares the extracted content for retrieval before the call returns. You don't have to configure or run a separate ingestion pipeline.

The listed `fileName` is taken from the `Content-Disposition: attachment; filename="..."` header on the upload request. REST calls and the .NET SDK set this header directly, while the Python SDK accepts a `filename` parameter and builds the header automatically. If the header isn't set, the service assigns an auto-generated `fileName`.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

string fileName = "installation-guide.pdf";
byte[] fileBytes = await File.ReadAllBytesAsync(fileName);
string contentDisposition = $"attachment; filename=\"{fileName}\"";

KnowledgeSourceFile uploadedFile = (await indexClient.UploadKnowledgeSourceFileAsync(
    "my-file-ks",
    contentDisposition,
    BinaryData.FromBytes(fileBytes))).Value;

Console.WriteLine($"Uploaded file ID: {uploadedFile.FileId}");
```

**Reference:** [SearchIndexClient.UploadKnowledgeSourceFileAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.uploadknowledgesourcefileasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

file_path = Path("installation-guide.pdf")
uploaded_file = index_client.upload_knowledge_source_file(
    "my-file-ks",
    file_path.read_bytes(),
    filename=file_path.name,
)
print(f"Uploaded file ID: {uploaded_file.file_id}")
```

**Reference:** [SearchIndexClient.upload_knowledge_source_file](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-upload-knowledge-source-file)

::: zone-end

::: zone pivot="rest"

```http
POST {{search-url}}/knowledgesources/my-file-ks/files?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="installation-guide.pdf"

<binary file content>
```

**Reference:** [Knowledge Sources - Upload File](/rest/api/searchservice/knowledge-sources/upload-file?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

> [!NOTE]
> Uploading a file doesn't replace an existing file, even if you reuse the same `fileName`. Each upload creates a new file with its own `fileId`, so the list of uploaded files can contain multiple entries that share a `fileName`.
>
> To replace content, delete the prior file by `fileId` before or after the new upload.

## List uploaded files

List files on the knowledge source to inspect the uploaded file set.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

await foreach (KnowledgeSourceFile file in indexClient.GetKnowledgeSourceFilesAsync("my-file-ks"))
{
    Console.WriteLine($"{file.FileName} ({file.FileSizeBytes} bytes) error={file.ErrorMessage}");
}
```

**Reference:** [SearchIndexClient.GetKnowledgeSourceFilesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getknowledgesourcefilesasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

for file in index_client.list_knowledge_source_files("my-file-ks"):
    print(f"{file.file_name} ({file.file_size_bytes} bytes) error={file.error_message}")
```

**Reference:** [SearchIndexClient.list_knowledge_source_files](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-list-knowledge-source-files)

::: zone-end

::: zone pivot="rest"

```http
GET {{search-url}}/knowledgesources/my-file-ks/files?api-version=2026-05-01-preview
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List Files](/rest/api/searchservice/knowledge-sources/list-files?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

A response includes metadata for each uploaded file. The `errorMessage` value is `null` when the upload is processed without an error.

```json
{
  "value": [
    {
      "fileId": "file-abc123",
      "fileName": "installation-guide.txt",
      "fileSizeBytes": 89,
      "createdAt": "2026-05-07T18:10:00Z",
      "lastUpdatedAt": "2026-05-07T18:14:00.803Z",
      "errorMessage": null
    }
  ]
}
```

Because uploads are synchronous, a file is ready for retrieval as soon as its upload call succeeds. If processing fails, the upload response and any subsequent list entry include a non-`null` `errorMessage`. Review the value for unsupported file types, extraction failures, model access issues, or quota limits.

## Delete uploaded files

Delete files from the knowledge source when you no longer want them available for retrieval.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

await indexClient.DeleteKnowledgeSourceFileAsync("my-file-ks", "file-abc123");
```

**Reference:** [SearchIndexClient.DeleteKnowledgeSourceFileAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.deleteknowledgesourcefileasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

index_client.delete_knowledge_source_file("my-file-ks", "file-abc123")
```

**Reference:** [SearchIndexClient.delete_knowledge_source_file](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-delete-knowledge-source-file)

::: zone-end

::: zone pivot="rest"

```http
DELETE {{search-url}}/knowledgesources/my-file-ks/files/file-abc123?api-version=2026-05-01-preview
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Delete File](/rest/api/searchservice/knowledge-sources/delete-file?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
