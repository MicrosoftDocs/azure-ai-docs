---
title: Create a File Knowledge Source for Agentic Retrieval
description: Learn how to create a file knowledge source in Azure AI Search, upload files directly, and use the processed content in a knowledge base.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/21/2026
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a file knowledge source (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The preview APIs support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *file knowledge source* (preview) uploads small-to-medium file sets directly to Azure AI Search for agentic retrieval. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

File knowledge sources are useful when you want a managed upload experience instead of provisioning Azure Storage, configuring access, and creating an indexer pipeline over an external container. Azure AI Search processes uploaded files so their extracted content can be retrieved from a knowledge base.

Use a [blob knowledge source](agentic-knowledge-source-how-to-blob.md) instead when your files are already in Azure Blob Storage or Azure Data Lake Storage Gen2, when your file set exceeds or is likely to exceed the [file knowledge source limits](#file-support-and-limits), or when you need scheduled ingestion. Also use a blob knowledge source when you want to manage source blobs with [Azure Blob Storage lifecycle management policies](/azure/storage/blobs/lifecycle-management-overview) or when you need [document-level permissions (preview)](agentic-knowledge-source-how-to-blob.md#enforce-document-level-permissions-preview) based on permissions in Azure Storage.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| -- | -- | -- | -- | -- | -- | -- |
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md). File knowledge sources support both the Dedicated and Serverless pricing models. For model and tier details, see [Choose a pricing model and service tier](search-sku-tier.md).

+ Review [Azure AI Search costs](search-sku-manage-costs.md). Model calls, vectorization, and other AI processing can incur separate charges.

+ On Serverless, successful file ingestion operations consume billable compute. Failed uploads don't incur Serverless compute charges.

+ If you need paid agentic retrieval beyond the monthly free allowance, [enable the standard agentic retrieval plan](agentic-retrieval-how-to-enable-disable.md). The `knowledgeRetrieval=standard` setting is separate from Serverless compute and storage charges and doesn't select a pricing model.

+ Files in a [supported format](#file-support-and-limits).

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ If the knowledge source specifies an Azure OpenAI model for embeddings, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

  + If the Foundry resource has public network access disabled, create a `foundry_account` [shared private link](search-indexer-howto-access-private.md#supported-resource-types) from the search service to the Foundry resource and keep the resource's **Allow Azure services on the trusted services list** setting enabled.

+ If the knowledge source specifies the `standard` content extraction mode, review the requirements for the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md).

  + Usage is charged at [Azure Content Understanding in Foundry Tools pricing](https://azure.microsoft.com/pricing/details/content-understanding/) to the Foundry resource configured through `aiServices`.

  + The 20-document daily free allowance available to some built-in skills doesn't apply.

  + For the example in this article, you need the Foundry resource endpoint and key, plus Azure OpenAI embedding and chat completion model information.

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ The [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true) version of the Search Service REST API.

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## File support and limits

Before you create a file knowledge source, review the requirements and limits that affect file upload, extraction, and management.

### Supported content types

File knowledge sources accept files based on detected content type. A caller-provided content type doesn't override detection.

Supported content types include:

+ PDF
+ Word (`.doc`, `.docx`)
+ PowerPoint (`.ppt`, `.pptx`)
+ Excel (`.xls`, `.xlsx`)
+ JSON
+ Shell scripts
+ Content detected as `text/*`, such as `.txt`, `.md`, `.html`, and `.csv`

### Supported extraction modes

+ For the listed content types, both `2026-05-01-preview` and `2026-08-01-preview` support `minimal`. `standard` is available only in `2026-08-01-preview`.

+ Content detected as `image/*` isn't supported in `2026-05-01-preview`. In `2026-08-01-preview`, use `standard` extraction. `minimal` extraction returns HTTP status `415` in both versions.

### Limits and file operations

Limits and supported file operations differ by API version.

| Capability | `2026-05-01-preview` | `2026-08-01-preview` |
| -- | -- | -- |
| Maximum files per knowledge source | 100 | 200 |
| Maximum file size | 50 MB on all supported pricing tiers | 50 MB on Free and Basic; 100 MB on other supported Dedicated tiers and Serverless |
| Processing duration | Upload can run for up to 180 seconds | Upload and update can run for up to 180 seconds |
| Upload content and metadata | Raw file content | Raw file content or multipart content with metadata |
| List uploaded files | List files | Filter by path or file name, and return richer file details |
| Replace existing file content | Delete and re-upload | Use update operation |
| Browser access to file operations | CORS isn't available | Configure CORS |

> [!NOTE]
> + The generated search index stores the uploaded content. For total storage limits by pricing tier, see [Service limits](search-limits-quotas-capacity.md#service-limits).
> + If you configure the file knowledge source to chunk or vectorize uploaded content, model and downstream processing limits also apply.

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

Each file knowledge source creates an index, but not an indexer or schedule. You must include the `fileParameters.ingestionParameters` object. The service rejects requests that specify `networkAccessMode`.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

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
from azure.identity import DefaultAzureCredential
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

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

embedding_params = AzureOpenAIVectorizerParameters(
    resource_url="<aoai-endpoint>",
    deployment_name="<aoai-embedding-deployment>",
    model_name="<aoai-embedding-model>",
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
PUT {{search-endpoint}}/knowledgesources/my-file-ks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
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

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

### Configure standard extraction

Starting with the `2026-08-01-preview` API version, `standard` extraction uses Content Understanding to extract, semantically chunk, and enrich uploaded files. Azure AI Search manages this processing as part of the knowledge source, and [Content Understanding charges](https://azure.microsoft.com/pricing/details/content-understanding/) apply separately.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

var embeddingParameters = new AzureOpenAIVectorizerParameters
{
  ResourceUri = new Uri(aoaiEndpoint),
  DeploymentName = aoaiEmbeddingDeployment,
  ModelName = aoaiEmbeddingModel
};

var ingestionParameters = new KnowledgeSourceIngestionParameters
{
  ContentExtractionMode = KnowledgeSourceContentExtractionMode.Standard,
  AiServices = new AIServices(new Uri(foundryEndpoint)) { ApiKey = foundryKey },
  EmbeddingModel = new KnowledgeSourceAzureOpenAIVectorizer
  {
    AzureOpenAIParameters = embeddingParameters
  },
  ChatCompletionModel = new KnowledgeBaseAzureOpenAIModel(
    new AzureOpenAIVectorizerParameters
    {
      ResourceUri = new Uri(aoaiEndpoint),
      DeploymentName = aoaiChatDeployment,
      ModelName = aoaiChatModel
    })
};

var knowledgeSource = new FileKnowledgeSource(
  "my-file-ks",
  new FileKnowledgeSourceParameters { IngestionParameters = ingestionParameters });

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Configured standard extraction for '{knowledgeSource.Name}'.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
  AzureOpenAIVectorizerParameters,
  FileKnowledgeSource,
  FileKnowledgeSourceParameters,
  KnowledgeBaseAzureOpenAIModel,
)
from azure.search.documents.knowledgebases.models import (
  AIServices,
  KnowledgeSourceAzureOpenAIVectorizer,
  KnowledgeSourceIngestionParameters,
)

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

embedding_parameters = AzureOpenAIVectorizerParameters(
  resource_url="<aoai-endpoint>",
  deployment_name="<aoai-embedding-deployment>",
  model_name="<aoai-embedding-model>",
)
ingestion_parameters = KnowledgeSourceIngestionParameters(
  content_extraction_mode="standard",
  ai_services=AIServices(
    uri="<foundry-resource-endpoint>",
    api_key="<foundry-resource-key>",
  ),
  embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
    azure_open_ai_parameters=embedding_parameters
  ),
  chat_completion_model=KnowledgeBaseAzureOpenAIModel(
    azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
      resource_url="<aoai-endpoint>",
      deployment_name="<aoai-gpt-deployment>",
      model_name="<aoai-gpt-model>",
    )
  ),
)
knowledge_source = FileKnowledgeSource(
  name="my-file-ks",
  file_parameters=FileKnowledgeSourceParameters(
    ingestion_parameters=ingestion_parameters
  ),
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Configured standard extraction for '{knowledge_source.name}'.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-endpoint}}/knowledgesources/my-file-ks?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}
Prefer: return=representation

{
  "name": "my-file-ks",
  "kind": "file",
  "description": "This knowledge source uses standard extraction.",
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
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "{{aoai-endpoint}}",
          "deploymentId": "{{aoai-gpt-deployment}}",
          "modelName": "{{aoai-gpt-model}}"
        }
      },
      "contentExtractionMode": "standard",
      "aiServices": {
        "uri": "{{foundry-resource-endpoint}}",
        "apiKey": "{{foundry-resource-key}}"
      }
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

### CORS for file operations

To allow browser-based file operations, set `corsOptions` on the file knowledge source with the trusted origins and maximum preflight cache duration for your application.

> [!IMPORTANT]
> In the `2026-08-01-preview` API version, `corsOptions` applies to file upload, list, update, and delete endpoints independently of the extraction mode. If you omit `corsOptions`, the file knowledge source has no browser cross-origin policy. CORS doesn't authorize requests. Enabling origins can expose service operations and data in a browser context and introduce security risks. Specify only trusted origins, and don't use a wildcard origin in production. For browser requests, use Microsoft Entra token authentication with the minimum required role. Never expose access tokens or service keys in browser code.

## Upload files

After you create the knowledge source, upload files directly to it. Each upload is a synchronous call: Azure AI Search extracts content, chunks it, creates embeddings when needed, indexes the chunks, and persists file metadata before the call returns. You don't have to configure or run a separate ingestion pipeline.

For help with errors related to uploading and managing files, see [Troubleshoot file operations](#troubleshoot-file-operations).

### Upload a raw file

For a raw upload, the listed `fileName` comes from the `Content-Disposition: attachment; filename="..."` header. REST calls and the .NET SDK set this header directly, while the Python SDK accepts a `filename` parameter and builds the header automatically. If you don't provide a file name, the service assigns an autogenerated `fileName`.

File names can include a relative path, such as `manuals/installation-guide.pdf`. The service normalizes backslashes to forward slashes. It rejects absolute paths, empty path segments, `.` or `..` segments, colon-containing segments, and invalid file-name characters with HTTP status `400`.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

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

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

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
POST {{search-endpoint}}/knowledgesources/my-file-ks/files?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="installation-guide.pdf"

<binary file content>
```

**Reference:** [Knowledge Sources - Upload File](/rest/api/searchservice/knowledge-sources/upload-file?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

### Upload a file with optional metadata

Starting with the `2026-08-01-preview` API version, use a multipart request to upload one binary file with optional custom metadata. The request includes exactly one `content` part and an optional JSON `metadata` part.

If both names are specified, `metadata.fileName` takes precedence over the filename on the `content` part. If neither is specified, the service assigns an autogenerated file name.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
var metadata = new FileUploadMetadata
{
  FileName = "installation-guide.pdf",
  Metadata =
  {
    ["department"] = "support",
    ["product"] = "contoso-100"
  }
};

#pragma warning disable SCME0004
var request = new UploadKnowledgeSourceFileMultipartRequest(
  metadata,
  "installation-guide.pdf");
KnowledgeSourceFile uploadedFile = (await indexClient
  .UploadKnowledgeSourceFileMultipartAsync("my-file-ks", request)).Value;
#pragma warning restore SCME0004

Console.WriteLine($"Uploaded file ID: {uploadedFile.FileId}");
```

**Reference:** [SearchIndexClient.UploadKnowledgeSourceFileMultipartAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
  FileUploadMetadata,
  UploadKnowledgeSourceFileMultipartRequest,
)

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())
file_path = Path("installation-guide.pdf")
request = UploadKnowledgeSourceFileMultipartRequest(
  metadata=FileUploadMetadata(
    file_name=file_path.name,
    metadata={"department": "support", "product": "contoso-100"},
  ),
  content=(file_path.name, file_path.read_bytes(), "application/pdf"),
)

uploaded_file = index_client.upload_knowledge_source_file_multipart(
  name="my-file-ks",
  body=request,
)
print(f"Uploaded file ID: {uploaded_file.file_id}")
```

**Reference:** [SearchIndexClient.upload_knowledge_source_file_multipart](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgesources('my-file-ks')/files?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: multipart/form-data; boundary=file-boundary

--file-boundary
Content-Disposition: form-data; name="metadata"
Content-Type: application/json

{
  "fileName": "installation-guide.pdf",
  "metadata": {
    "department": "support",
    "product": "contoso-100"
  }
}
--file-boundary
Content-Disposition: form-data; name="content"; filename="installation-guide.pdf"
Content-Type: application/octet-stream

< ./installation-guide.pdf
--file-boundary--
```

**Reference:** [Knowledge Sources - Upload File](/rest/api/searchservice/knowledge-sources/upload-file?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

> [!NOTE]
> Uploading a file doesn't replace an existing file, even if you reuse the same `fileName`. Each successful upload creates a new file with its own `fileId`, so the list of uploaded files can contain multiple entries that share a `fileName`.
>
> With `2026-05-01-preview`, replace content by deleting the prior file and uploading the replacement. With `2026-08-01-preview`, use the update operation.

## List uploaded files

List files on the knowledge source to inspect the uploaded file set.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

await foreach (KnowledgeSourceFile file in indexClient.GetKnowledgeSourceFilesAsync("my-file-ks"))
{
    Console.WriteLine($"{file.FileName} ({file.FileSizeBytes} bytes) error={file.ErrorMessage}");
}
```

**Reference:** [SearchIndexClient.GetKnowledgeSourceFilesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getknowledgesourcefilesasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

for file in index_client.list_knowledge_source_files("my-file-ks"):
    print(f"{file.file_name} ({file.file_size_bytes} bytes) error={file.error_message}")
```

**Reference:** [SearchIndexClient.list_knowledge_source_files](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-list-knowledge-source-files)

::: zone-end

::: zone pivot="rest"

```http
GET {{search-endpoint}}/knowledgesources/my-file-ks/files?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
```

**Reference:** [Knowledge Sources - List Files](/rest/api/searchservice/knowledge-sources/list-files?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

The response includes metadata for each uploaded file. Successfully listed files have an `errorMessage` value of `null`.

```json
{
  "value": [
    {
      "fileId": "file-abc123",
      "fileName": "installation-guide.pdf",
      "fileSizeBytes": 1048576,
      "createdAt": "2026-05-07T18:10:00Z",
      "lastUpdatedAt": "2026-05-07T18:14:00.803Z",
      "errorMessage": null
    }
  ]
}
```

If a new upload fails, the request returns an error and doesn't create a file metadata record. The failed upload doesn't appear in later list results and isn't billed.

If a model access failure occurs and the Foundry resource that hosts the embedding model uses private networking, confirm that the `foundry_account` shared private link is approved and the trusted-services bypass is enabled. A disabled bypass returns `403 Public access is disabled`. For setup details, see [Prerequisites](#prerequisites).

### List and filter files

Starting with the `2026-08-01-preview` API version, use `prefix` to filter files by relative path or `search` to filter by file-name prefix. Set `pageSize` to control the number of results.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

await foreach (KnowledgeSourceFile file in indexClient.GetKnowledgeSourceFilesAsync(
  "my-file-ks",
  prefix: "manuals/",
  pageSize: 100))
{
  Console.WriteLine($"{file.FileName} ({file.FileId})");
}
```

**Reference:** [SearchIndexClient.GetKnowledgeSourceFilesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.getknowledgesourcefilesasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

files = index_client.list_knowledge_source_files(
  "my-file-ks",
  prefix="manuals/",
  page_size=100,
)
for file in files:
  print(f"{file.file_name} ({file.file_id})")
```

**Reference:** [SearchIndexClient.list_knowledge_source_files](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-list-knowledge-source-files)

::: zone-end

::: zone pivot="rest"

```http
GET {{search-endpoint}}/knowledgesources('my-file-ks')/files?api-version=2026-08-01-preview&prefix=manuals/&pageSize=100
Authorization: Bearer {{search-access-token}}
```

**Reference:** [Knowledge Sources - List Files](/rest/api/searchservice/knowledge-sources/list-files?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

The response includes service-selected parsing and extraction modes, as well as user metadata for file management. User metadata isn't searchable or filterable.

```json
{
  "value": [
    {
      "fileId": "file-abc123",
      "fileName": "manuals/installation-guide.md",
      "prefix": "manuals/",
      "metadata": {
        "department": "support",
        "product": "contoso-100"
      },
      "parsingMode": "markdown",
      "extractionMode": "minimal",
      "fileSizeBytes": 1048576,
      "createdAt": "2026-08-03T18:10:00Z",
      "lastUpdatedAt": "2026-08-03T18:14:00Z",
      "errorMessage": null
    }
  ],
  "@odata.nextLink": "<service-generated continuation URL>"
}
```

To retrieve all results, follow `@odata.nextLink` until it's absent. Send the complete URL exactly as returned, without changing the query parameters.

## Update an uploaded file

Starting with the `2026-08-01-preview` API version, update a file by its `fileId`. The multipart request requires the binary `content` part. The metadata JSON part is optional, so a content-only update is supported. A metadata-only update isn't supported.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
var metadata = new FileUploadMetadata
{
  FileName = "installation-guide.pdf",
  Metadata =
  {
    ["department"] = "support",
    ["product"] = "contoso-200"
  }
};

#pragma warning disable SCME0004
var request = new UpdateKnowledgeSourceFileRequest(
  metadata,
  "installation-guide.pdf");
KnowledgeSourceFile updatedFile = (await indexClient.UpdateKnowledgeSourceFileAsync(
  fileId,
  "my-file-ks",
  request)).Value;
#pragma warning restore SCME0004

Console.WriteLine($"Updated file ID: {updatedFile.FileId}");
```

**Reference:** [SearchIndexClient.UpdateKnowledgeSourceFileAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
  FileUploadMetadata,
  UpdateKnowledgeSourceFileRequest,
)

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())
file_path = Path("installation-guide.pdf")
request = UpdateKnowledgeSourceFileRequest(
  metadata=FileUploadMetadata(
    file_name=file_path.name,
    metadata={"department": "support", "product": "contoso-200"},
  ),
  content=(file_path.name, file_path.read_bytes(), "application/pdf"),
)

updated_file = index_client.update_knowledge_source_file(
  name="my-file-ks",
  file_id=file_id,
  body=request,
)
print(f"Updated file ID: {updated_file.file_id}")
```

**Reference:** [SearchIndexClient.update_knowledge_source_file](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-endpoint}}/knowledgesources('my-file-ks')/files('{{file-id}}')?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: multipart/form-data; boundary=file-boundary

--file-boundary
Content-Disposition: form-data; name="metadata"
Content-Type: application/json

{
  "fileName": "installation-guide.pdf",
  "metadata": {
    "department": "support",
    "product": "contoso-200"
  }
}
--file-boundary
Content-Disposition: form-data; name="content"; filename="installation-guide.pdf"
Content-Type: application/octet-stream

< ./installation-guide.pdf
--file-boundary--
```

**Reference:** [Knowledge Sources - Update File](/rest/api/searchservice/knowledge-sources/update-file?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

If an update fails, the previous metadata record remains. Don't assume that an update changes indexed content transactionally.

## Delete uploaded files

Delete files from the knowledge source when you no longer want them available for retrieval.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

await indexClient.DeleteKnowledgeSourceFileAsync("my-file-ks", "file-abc123");
```

**Reference:** [SearchIndexClient.DeleteKnowledgeSourceFileAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.deleteknowledgesourcefileasync?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

index_client.delete_knowledge_source_file("my-file-ks", "file-abc123")
```

**Reference:** [SearchIndexClient.delete_knowledge_source_file](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true#azure-search-documents-indexes-searchindexclient-delete-knowledge-source-file)

::: zone-end

::: zone pivot="rest"

```http
DELETE {{search-endpoint}}/knowledgesources/my-file-ks/files/file-abc123?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
```

**Reference:** [Knowledge Sources - Delete File](/rest/api/searchservice/knowledge-sources/delete-file?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Troubleshoot file operations

The following status codes are specific to file knowledge source operations.

| Status code | Cause and action |
| -- | -- |
| `400` | The file is empty, contains no extractable text, has an unsafe relative path, or has an invalid continuation request. Verify the file has supported, readable content and a valid file name. For list operations, follow `@odata.nextLink` exactly as returned. Don't combine `$skiptoken` with `search` or `pageSize`. |
| `409` | The file knowledge source reached the file limit for the API version. Delete files before uploading more. |
| `415` | The service detected an unsupported MIME type, or it detected an image while the knowledge source uses minimal extraction. Use a supported format. For images, use standard extraction. Changing only the caller-provided content type doesn't override detection. |
| `429` | The processing queue is full. Use bounded parallelism and retry with exponential backoff. The service doesn't guarantee a `Retry-After` header. |
| `504` | Processing exceeded 180 seconds during file upload or update. Reduce the file size or complexity and try again. |

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
