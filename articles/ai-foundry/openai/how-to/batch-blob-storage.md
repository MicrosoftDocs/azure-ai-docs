---
title: "How to configure Azure Blob Storage with Azure OpenAI Batch"
titleSuffix: Azure OpenAI
description: Learn how to configure Azure Blob Storage with Azure OpenAI Batch
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 11/26/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2025
---

# Configuring Azure Blob Storage for Azure OpenAI Batch

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI now supports using [Azure Blob Storage](/azure/storage/blobs/storage-blobs-introduction) for Azure OpenAI Batch input and output files. By using your own storage, you aren't subject to the batch restrictions on the number of files.

## Region Support

Now supported in [all regions where batch deployments are supported](./batch.md#batch-support).

## Azure Blob Storage configuration

### Prerequisites

- An [Azure Blob Storage account](/azure/storage/blobs/storage-blobs-introduction).
- An Azure OpenAI resource with a model of the deployment type `Global-Batch` or `DataZoneBatch` deployed. You can refer to the [resource creation and model deployment guide](./create-resource.md) for help with this process.

### Managed identity

In order for your Azure OpenAI resource to securely access your Azure Blob Storage account you need setup your resource with a **system assigned managed identity**.

> [!NOTE]
> Currently user assigned managed identities aren't supported.

1. Sign in to [https://portal.azure.com](https://portal.azure.com).
2. Find your Azure OpenAI resource > Select **Resource Management** > **Identity** > **System assigned** > set status to **On**.

    :::image type="content" source="../media/how-to/batch-blob-storage/identity.png" alt-text="Screenshot that shows system managed identity configuration." lightbox="../media/how-to/batch-blob-storage/identity.png":::

### Role-based access control

Once your Azure OpenAI resource has been configured for system assigned managed identity, you need to give it access to your Azure Blob Storage account.

1. From [https://portal.azure.com](https://portal.azure.com) find and select your Azure Blob Storage resource.
2. Select **Access Control (IAM)** > **Add** > **Add role assignment**.

    :::image type="content" source="../media/how-to/batch-blob-storage/access-control.png" alt-text="Screenshot that shows access control interface for an Azure Blob Storage resource." lightbox="../media/how-to/batch-blob-storage/access-control.png":::

3. Search for **Storage Blob Data Contributor** > **Next**.
4. Select **Managed identity** > **+Select members** > Select your Azure OpenAI resources's managed identity.

   :::image type="content" source="../media/how-to/batch-blob-storage/add-role.png" alt-text="Screenshot that shows Storage Blob Data Contributor role assignment." lightbox="../media/how-to/batch-blob-storage/add-role.png":::

If you prefer using custom roles for more granular access, the following permissions are required:

**Input data**:

- `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`

**Output data/folders**:

- `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`
- `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write`

### Create containers

For this example you'll create two containers named `batch-input`, and `batch-output`. You can name these whatever you want, but if you use an alternate name you'll need to adjust the examples in the following steps.

To create a container under **Data storage** > Select **+Container** > Name your containers.

:::image type="content" source="../media/how-to/batch-blob-storage/container.png" alt-text="Screenshot that shows Storage Blob Data containers." lightbox="../media/how-to/batch-blob-storage/container.png":::

Once your containers are created retrieve the URL for each container by selecting the container > **Settings** > **Properties** > Copy the URLs.

In this case we have:

- `https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-input`
- `https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-output`

### Create input file

For this article, we'll create a file named `test.jsonl` and will copy the contents below to the file. You'll need to modify and add your global batch deployment name to each line of the file.

```json
{"custom_id": "task-0", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "When was Microsoft founded?"}]}}
{"custom_id": "task-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "When was the first XBOX released?"}]}}
{"custom_id": "task-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "What is Altair Basic?"}]}}
```

### Upload training file

From your Azure Blob Storage account, open your **batch-input** container that you created previously.

Select **Upload** and select your `test.jsonl` file.

:::image type="content" source="../media/how-to/batch-blob-storage/upload.png" alt-text="Screenshot that shows Azure Storage Blob container upload UX." lightbox="../media/how-to/batch-blob-storage/upload.png":::

During the time that we're processing your `jsonl` file as part of the batch job, you can't make any changes to the file. If a file changes while the batch job is running the job will fail.

## Create batch job

> [!NOTE]
> `metadata` is currently not supported with this capability.

# [Python](#tab/python)

```python
import os
from datetime import datetime
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

batch_response = client.batches.create(
    input_file_id=None,
    endpoint="/chat/completions",
    completion_window="24h",
      extra_body={ 
        "input_blob": "https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-input/test.jsonl",
        "output_folder": {
                "url": "https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-output",
        }
    }   
)

# Save batch ID for later use
batch_id = batch_response.id

print(batch_response.model_dump_json(indent=2))

```

# [REST ](#tab/rest)

```HTTP
curl -X POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/batches \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input_file_id": null,
    "endpoint": "/chat/completions",
    "completion_window": "24h",
    "input_blob": "https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-input/test.jsonl",
    "output_folder": {
      "url": "https://{AZURE-BLOB-STORAGE-RESOURCE-NAME}.blob.core.windows.net/batch-output"
    }
  }'
```

---

**Output:**

```json
{
  "id": "batch_b632a805-797b-49ed-9c9c-86eb4057f2a2",
  "completion_window": "24h",
  "created_at": 1747516485,
  "endpoint": "/chat/completions",
  "input_file_id": null,
  "object": "batch",
  "status": "validating",
  "cancelled_at": null,
  "cancelling_at": null,
  "completed_at": null,
  "error_file_id": null,
  "errors": null,
  "expired_at": null,
  "expires_at": 1747602881,
  "failed_at": null,
  "finalizing_at": null,
  "in_progress_at": null,
  "metadata": null,
  "output_file_id": null,
  "request_counts": {
    "completed": 0,
    "failed": 0,
    "total": 0
  },
  "error_blob": "",
  "input_blob": "https://docstest002.blob.core.windows.net/batch-input/test.jsonl",
  "output_blob": ""
}
```

You can monitor the status the same way you would previously as outlined in our [comprehensive guide on using Azure OpenAI batch](./batch.md).

```python
import time
import datetime 

status = "validating"
while status not in ("completed", "failed", "canceled"):
    time.sleep(60)
    batch_response = client.batches.retrieve(batch_id)
    status = batch_response.status
    print(f"{datetime.datetime.now()} Batch Id: {batch_id},  Status: {status}")

if batch_response.status == "failed":
    for error in batch_response.errors.data:  
        print(f"Error code {error.code} Message {error.message}")
```

**Output:**

```cmd
2025-05-17 17:16:56.950427 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: validating
2025-05-17 17:17:57.532054 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: validating
2025-05-17 17:18:58.156793 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: in_progress
2025-05-17 17:19:58.739708 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: in_progress
2025-05-17 17:20:59.398508 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: finalizing
2025-05-17 17:22:00.242371 Batch Id: batch_b632a805-797b-49ed-9c9c-86eb4057f2a2,  Status: completed
```

Once the `status` is `completed` you can retrieve your `output_blob` path:

```python
print(batch_response.model_dump_json(indent=2))
```

**Output:**

```json
{
  "id": "batch_b632a805-797b-49ed-9c9c-86eb4057f2a2",
  "completion_window": "24h",
  "created_at": 1747516485,
  "endpoint": "/chat/completions",
  "input_file_id": null,
  "object": "batch",
  "status": "completed",
  "cancelled_at": null,
  "cancelling_at": null,
  "completed_at": 1747516883,
  "error_file_id": null,
  "errors": null,
  "expired_at": null,
  "expires_at": 1747602881,
  "failed_at": null,
  "finalizing_at": 1747516834,
  "in_progress_at": 1747516722,
  "metadata": null,
  "output_file_id": null,
  "request_counts": {
    "completed": 3,
    "failed": 0,
    "total": 3
  },
  "error_blob": "https://docstest002.blob.core.windows.net/batch-output/{GUID}/errors.jsonl",
  "input_blob": "https://docstest002.blob.core.windows.net/batch-input/test.jsonl",
  "output_blob": "https://docstest002.blob.core.windows.net/batch-output/{GUID}/results.jsonl"
}
```

Once your batch job is complete, you can download the `error_blob` and `output_blob` via the Azure Blob Storage interface in the Azure portal or you can download programmatically:

> [!NOTE]
> `error_blob`, and `output_blob` paths are always returned in the response even in cases where a corresponding file isn't created. In this case there were no errors so `errors.jsonl` wasn't created, only `results.jsonl` exists.

```cmd
pip install azure-identity azure-storage-blob
```

Keep in mind that while you have granted the Azure OpenAI resource programmatic access to your Azure Blob Storage, to download the results you might need to also give the user account that is executing the script below access as well. For downloading the file, `Storage Blob Data Reader` access is sufficient.

```python
# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Define storage account and container information
storage_account_name = "docstest002" # replace with your storage account name
container_name = "batch-output"

# Define the blob paths to download
blob_paths = [
    "{REPLACE-WITH-YOUR-GUID}/results.jsonl",
]

credential = DefaultAzureCredential()
account_url = f"https://{storage_account_name}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
container_client = blob_service_client.get_container_client(container_name)

for blob_path in blob_paths:
    blob_client = container_client.get_blob_client(blob_path)
    
    file_name = blob_path.split("/")[-1]
    
    print(f"Downloading {file_name}...")
    with open(file_name, "wb") as file:
        download_stream = blob_client.download_blob()
        file.write(download_stream.readall())
    
    print(f"Downloaded {file_name} successfully!")
```

## See also

For more information on Azure OpenAI Batch, see the [comprehensive batch guide](./batch.md).
