---
title: Create File Knowledge Source for Agentic Retrieval
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
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

Use a *file knowledge source* (preview) to upload small and medium file sets directly to Azure AI Search for agentic retrieval. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

A file knowledge source is useful when you want a managed upload experience instead of provisioning Azure Storage, configuring access, and creating an indexer pipeline over an external container. Azure AI Search processes uploaded files so their extracted content can be retrieved from a knowledge base. Use [blob knowledge sources](agentic-knowledge-source-how-to-blob.md) instead when your content already lives in Azure Blob Storage or ADLS Gen2, when you need large-scale ingestion, or when you depend on storage-account capabilities.

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). If you need paid usage beyond the monthly free allowance, set the `knowledgeRetrieval` service property to `standard` by using the [Search Management REST API](/rest/api/searchmanagement/services/create-or-update).

+ Files in a [supported format](#supported-formats-and-limits).

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ The latest preview [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package: `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest preview [azure-search-documents](https://pypi.org/project/azure-search-documents/) package: `pip install azure-search-documents --pre`

::: zone-end

::: zone pivot="rest"

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Check for existing knowledge sources

Before you create a new file knowledge source, list the knowledge sources that already exist on your search service. You can avoid name conflicts and reuse an existing source instead of creating a duplicate.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

await foreach (var ks in indexClient.GetKnowledgeSourcesAsync())
{
    Console.WriteLine($"{ks.Name} ({ks.GetType().Name})");
}
```

**Reference:** [SearchIndexClient.GetKnowledgeSourcesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

for ks in index_client.list_knowledge_sources():
    print(f"{ks.name} ({ks.kind})")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version=2026-05-01-preview&$select=name,kind
api-key: {{api-key}}
```

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
api-key: {{api-key}}
```

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

::: zone-end

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

**Reference:** [FileKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.fileknowledgesource?view=azure-dotnet-preview&preserve-view=true), [FileKnowledgeSourceParameters](/dotnet/api/azure.search.documents.indexes.models.fileknowledgesourceparameters?view=azure-dotnet-preview&preserve-view=true)

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

**Reference:** [FileKnowledgeSource](/python/api/azure-search-documents/azure.search.documents.indexes.models.fileknowledgesource), [FileKnowledgeSourceParameters](/python/api/azure-search-documents/azure.search.documents.indexes.models.fileknowledgesourceparameters)

::: zone-end

::: zone pivot="rest"

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a file knowledge source.

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

::: zone-end

### Source-specific properties

You can pass the following properties to create a file knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `FileParameters` | Parameters specific to file knowledge sources: `IngestionParameters`. | Object | Only nested model credentials are editable | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `file_parameters` | Parameters specific to file knowledge sources: `ingestion_parameters`. | Object | Only nested model credentials are editable | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `file` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `fileParameters` | Parameters specific to file knowledge sources: `ingestionParameters`. | Object | Only nested model credentials are editable | No |

::: zone-end

### Ingestion parameters properties

You can pass the following ingestion parameter properties to control how uploaded files are processed.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `ContentExtractionMode` | Controls how content is extracted from files. File knowledge sources support only `minimal`. | String | No | No |
| `EmbeddingModel` | A [vectorizer](vector-search-how-to-configure-vectorizer.md) that generates embeddings for content during ingestion and for queries at retrieval time. Supported `Kind` values are `azureOpenAI`, `customWebApi`, `aiServicesVision`, and `aml`. | Object | Vectorizer credentials are editable | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `content_extraction_mode` | Controls how content is extracted from files. File knowledge sources support only `minimal`. | String | No | No |
| `embedding_model` | A [vectorizer](vector-search-how-to-configure-vectorizer.md) that generates embeddings for content during ingestion and for queries at retrieval time. Supported `kind` values are `azureOpenAI`, `customWebApi`, `aiServicesVision`, and `aml`. | Object | Vectorizer credentials are editable | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `contentExtractionMode` | Controls how content is extracted from files. File knowledge sources support only `minimal`. | String | No | No |
| `embeddingModel` | A [vectorizer](vector-search-how-to-configure-vectorizer.md) that generates embeddings for content during ingestion and for queries at retrieval time. Supported `kind` values are `azureOpenAI`, `customWebApi`, `aiServicesVision`, and `aml`. | Object | Vectorizer credentials are editable | No |

::: zone-end

## Upload files

After the source exists, upload files directly to it. Each upload is a synchronous call: Azure AI Search extracts content from the uploaded file, chunks the content, creates embeddings when needed, and prepares the extracted content for retrieval before the call returns. You don't have to configure or run a separate ingestion pipeline.

The request body contains the file content. The listed `fileName` is taken from the `Content-Disposition: attachment; filename="..."` header on the upload request; if the header isn't set, the service assigns an auto-generated `fileName`.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Core;
using Azure.Core.Pipeline;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

string fileName = "installation-guide.pdf";
byte[] fileBytes = await File.ReadAllBytesAsync(fileName);

var context = new RequestContext();
context.AddPolicy(
    new SetHeaderPolicy("Content-Disposition", $"attachment; filename=\"{fileName}\""),
    HttpPipelinePosition.PerCall);

Response response = await indexClient.UploadKnowledgeSourceFileAsync(
    "my-file-ks",
    RequestContent.Create(BinaryData.FromBytes(fileBytes)),
    context);

KnowledgeSourceFile uploadedFile = (KnowledgeSourceFile)response;
Console.WriteLine($"Uploaded file ID: {uploadedFile.FileId}");

sealed class SetHeaderPolicy(string name, string value) : HttpPipelineSynchronousPolicy
{
    public override void OnSendingRequest(HttpMessage message) =>
        message.Request.Headers.SetValue(name, value);
}
```

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
    content_type="application/octet-stream",
    headers={"Content-Disposition": f'attachment; filename="{file_path.name}"'},
)
print(f"Uploaded file ID: {uploaded_file.file_id}")
```

::: zone-end

::: zone pivot="rest"

```http
POST {{search-url}}/knowledgesources/my-file-ks/files?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="installation-guide.pdf"

<binary file content>
```

::: zone-end

> [!NOTE]
> Uploading a file doesn't replace an existing file even if you reuse the same `fileName`. Each upload creates a new file with its own `fileId`, and the list of uploaded files can contain multiple entries that share a `fileName`. To replace content, delete the prior file by `fileId` before or after the new upload.

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

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

for file in index_client.list_knowledge_source_files("my-file-ks"):
    print(f"{file.file_name} ({file.file_size_bytes} bytes) error={file.error_message}")
```

::: zone-end

::: zone pivot="rest"

```http
GET {{search-url}}/knowledgesources/my-file-ks/files?api-version=2026-05-01-preview
api-key: {{api-key}}
```

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

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

index_client.delete_knowledge_source_file("my-file-ks", "file-abc123")
```

::: zone-end

::: zone pivot="rest"

```http
DELETE {{search-url}}/knowledgesources/my-file-ks/files/file-abc123?api-version=2026-05-01-preview
api-key: {{api-key}}
```

::: zone-end

## Create a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var knowledgeBase = new KnowledgeBase(
    name: "my-file-kb",
    knowledgeSources: new[] { new KnowledgeSourceReference("my-file-ks") }
)
{
    Description = "A knowledge base for uploaded product manuals.",
    OutputMode = KnowledgeRetrievalOutputMode.ExtractiveData,
    RetrievalReasoningEffort = new KnowledgeRetrievalMinimalReasoningEffort()
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBase.Name}' created or updated successfully.");
```

**Reference:** [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    KnowledgeBase,
    KnowledgeRetrievalOutputMode,
    KnowledgeSourceReference,
)
from azure.search.documents.knowledgebases.models import KnowledgeRetrievalMinimalReasoningEffort

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

knowledge_base = KnowledgeBase(
    name="my-file-kb",
    description="A knowledge base for uploaded product manuals.",
    knowledge_sources=[KnowledgeSourceReference(name="my-file-ks")],
    output_mode=KnowledgeRetrievalOutputMode.EXTRACTIVE_DATA,
    retrieval_reasoning_effort=KnowledgeRetrievalMinimalReasoningEffort(),
)

index_client.create_or_update_knowledge_base(knowledge_base=knowledge_base)
print(f"Knowledge base '{knowledge_base.name}' created or updated successfully.")
```

**Reference:** [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-url}}/knowledgebases/my-file-kb?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json
Prefer: return=representation

{
  "name": "my-file-kb",
  "description": "A knowledge base for uploaded product manuals.",
  "outputMode": "extractiveData",
  "retrievalReasoningEffort": {
    "kind": "minimal"
  },
  "knowledgeSources": [
    {
      "name": "my-file-ks"
    }
  ]
}
```

::: zone-end

## Retrieve from the knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

The simplest retrieve call sends an intent and lets the knowledge base apply its configured defaults for each attached knowledge source.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var kbClient = new KnowledgeBaseRetrievalClient(
    new Uri(searchEndpoint),
    "my-file-kb",
    new AzureKeyCredential(apiKey));

var request = new KnowledgeBaseRetrievalRequest
{
    IncludeActivity = true
};
request.Intents.Add(new KnowledgeRetrievalSemanticIntent(
    "What does the installation guide say about network prerequisites?"));

var result = await kbClient.RetrieveAsync(request);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
)

kb_client = KnowledgeBaseRetrievalClient(
    endpoint="search_url",
    knowledge_base_name="my-file-kb",
    credential=AzureKeyCredential("api_key"),
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="What does the installation guide say about network prerequisites?"
        )
    ],
    include_activity=True,
)

result = kb_client.retrieve(request)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient)

::: zone-end

::: zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/my-file-kb/retrieve?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json
Accept: application/json

{
  "includeActivity": true,
  "intents": [
    {
      "type": "semantic",
      "search": "What does the installation guide say about network prerequisites?"
    }
  ],
  "knowledgeSourceParams": [
    {
      "kind": "file",
      "knowledgeSourceName": "my-file-ks",
      "includeReferences": true,
      "includeReferenceSourceData": true
    }
  ]
}
```

::: zone-end

## Supported formats and limits

The following file types are supported in this preview.

| Category | Extensions |
|--|--|
| Text | `.txt`, `.md`, `.html`, `.json`, `.csv` |
| Code | `.c`, `.cs`, `.cpp`, `.java`, `.py`, `.js`, `.ts`, `.php`, `.rb`, `.sh` |
| Documents | `.pdf`, `.docx`, `.pptx`, `.doc` |

The file knowledge source preview has the following limits.

| Limit | Value |
|--|--|
| Maximum file size per upload | 50 MB |
| Maximum files per file knowledge source | 100 |

> [!NOTE]
> Uploaded content is stored in the generated search index. For total storage limits by SKU, see [Service limits](search-limits-quotas-capacity.md#service-limits).

File knowledge sources are designed for direct upload scenarios, not large-scale scheduled crawling. If you need recurring ingestion from durable external storage, use a [blob knowledge source](agentic-knowledge-source-how-to-blob.md) instead.

## Delete a knowledge source

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

// List knowledge bases on the service.
await foreach (var kb in indexClient.GetKnowledgeBasesAsync())
{
    Console.WriteLine(kb.Name);
}

// Delete the knowledge base that references the file knowledge source.
await indexClient.DeleteKnowledgeBaseAsync("my-file-kb");

// Delete the file knowledge source.
await indexClient.DeleteKnowledgeSourceAsync("my-file-ks");
```

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

# List knowledge bases on the service.
for kb in index_client.list_knowledge_bases():
    print(kb.name)

# Delete the knowledge base that references the file knowledge source.
index_client.delete_knowledge_base("my-file-kb")

# Delete the file knowledge source.
index_client.delete_knowledge_source("my-file-ks")
```

::: zone-end

::: zone pivot="rest"

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version=2026-05-01-preview&$select=name
    api-key: {{api-key}}
    ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

1. Either delete the knowledge base or update the knowledge base by removing the knowledge source if you have multiple sources. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
