---
title: "Configure Blob Storage for Azure OpenAI Batch (classic)"
description: "Configure Azure Blob Storage for Azure OpenAI Batch (classic), then create, monitor, and download a batch job in an end-to-end workflow."
author: alvinashcraft
ms.author: aashcraft
manager: mcleans
ms.date: 07/23/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - build-2025
  - doc-kit-assisted
---

# Configure Azure Blob Storage for Azure OpenAI Batch (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Use [Azure Blob Storage](/azure/storage/blobs/storage-blobs-introduction) for Azure OpenAI Batch input and output files. By using your own storage, you remove the Batch API restrictions on the number of input files. This article shows how to configure storage access once, then create, monitor, and download a batch job without returning to the Azure portal.

## Prerequisites

- An Azure Blob Storage account.
- An Azure OpenAI resource in a [region that supports batch deployments](./batch.md), with a model deployed as `Global-Batch` or `DataZoneBatch`. For deployment instructions, see [Create a resource and deploy a model](./create-resource.md).
- An account that can update the Azure OpenAI resource and assign Azure roles on the storage account.
- The **Cognitive Services OpenAI User** or **Cognitive Services OpenAI Contributor** role on the Azure OpenAI resource.
- Python 3.9 or later.
- The [Azure CLI](/cli/azure/install-azure-cli).

## Understand the workflow

Complete the storage access setup once. The Azure OpenAI resource uses its system-assigned managed identity to read the input blob and write the result blobs. Your user identity creates the input file, uploads it, submits the batch job, monitors the job, and downloads the results.

Use either the Azure CLI or the Azure portal to complete all the steps in the next section. After you finish one setup path, continue with [Install the Python packages](#install-the-python-packages).

## Set up storage access

Enable a system-assigned managed identity for the Azure OpenAI resource. Then assign the **Storage Blob Data Contributor** role to both the resource identity and your user identity at the storage account scope.

> [!NOTE]
> Azure OpenAI Batch with Blob Storage currently doesn't support user-assigned managed identities.

# [Azure CLI](#tab/azure-cli)

Sign in to Azure and set the values that the following commands use:

```azurecli
az login

RESOURCE_GROUP="<resource-group-name>"
AZURE_OPENAI_RESOURCE="<azure-openai-resource-name>"
STORAGE_ACCOUNT="<storage-account-name>"
```

Enable the system-assigned managed identity and retrieve its principal ID:

```azurecli
az cognitiveservices account identity assign \
  --name "$AZURE_OPENAI_RESOURCE" \
  --resource-group "$RESOURCE_GROUP" \
  --output none

OPENAI_PRINCIPAL_ID=$(az cognitiveservices account show \
  --name "$AZURE_OPENAI_RESOURCE" \
  --resource-group "$RESOURCE_GROUP" \
  --query identity.principalId \
  --output tsv)

echo "Managed identity: $OPENAI_PRINCIPAL_ID"
```

```output
Managed identity: <principal-id>
```

Reference: [az cognitiveservices account identity assign](/cli/azure/cognitiveservices/account/identity#az-cognitiveservices-account-identity-assign)

Assign **Storage Blob Data Contributor** to the resource identity and your signed-in user:

```azurecli
STORAGE_ACCOUNT="<storage-account-name>"
STORAGE_ID=$(az storage account show \
  --name "$STORAGE_ACCOUNT" \
  --query id \
  --output tsv)
USER_ID=$(az ad signed-in-user show --query id --output tsv)

az role assignment create \
  --assignee-object-id "$OPENAI_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ID" \
  --output none

az role assignment create \
  --assignee-object-id "$USER_ID" \
  --assignee-principal-type User \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ID" \
  --output none

echo "Storage roles assigned."
```

```output
Storage roles assigned.
```

Reference: [az role assignment create](/cli/azure/role/assignment#az-role-assignment-create)

Role assignments can take several minutes to propagate. Create the input and output containers after the assignments take effect:

```azurecli
STORAGE_ACCOUNT="<storage-account-name>"

az storage container create \
  --account-name "$STORAGE_ACCOUNT" \
  --name batch-input \
  --auth-mode login \
  --output none

az storage container create \
  --account-name "$STORAGE_ACCOUNT" \
  --name batch-output \
  --auth-mode login \
  --output none

echo "Created batch-input and batch-output."
```

```output
Created batch-input and batch-output.
```

Reference: [az storage container create](/cli/azure/storage/container#az-storage-container-create)

# [Azure portal](#tab/azure-portal)

Complete all the portal configuration before you continue to the Python workflow:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Open your Azure OpenAI resource.
1. Under **Resource Management**, select **Identity** > **System assigned**.
1. Set **Status** to **On**, and then select **Save**.
1. Open your storage account, and then select **Access Control (IAM)** > **Add** > **Add role assignment**.
1. On the **Role** tab, select **Storage Blob Data Contributor**, and then select **Next**.
1. On the **Members** tab, select **Managed identity** > **Select members**.
1. Select your Azure OpenAI resource, and then select **Review + assign**.
1. Add another **Storage Blob Data Contributor** role assignment to your user account.
1. In the storage account, select **Data storage** > **Containers** > **+ Container**.
1. Create containers named `batch-input` and `batch-output`.

If you use a custom role instead of **Storage Blob Data Contributor**, grant these permissions:

- Input blobs: `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`
- Output blobs: `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read` and `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write`

---

## Install the Python packages

Sign in to Azure to provide a local credential for `DefaultAzureCredential`:

```azurecli
az login
```

Then install the OpenAI, Azure Identity, and Azure Blob Storage client libraries:

```cmd
python -m pip install --upgrade openai azure-identity azure-storage-blob
```

## Create the input file

Create `test.jsonl` with three chat completion requests. Set `BATCH_DEPLOYMENT` to the name of your batch model deployment:

```python
import json

BATCH_DEPLOYMENT = "<batch-deployment-name>"
INPUT_FILE = "test.jsonl"
SYSTEM_MESSAGE = "You are an AI assistant that helps people find information."
PROMPTS = [
  "When was Microsoft founded?",
  "When was the first Xbox released?",
  "What is Altair BASIC?",
]

with open(INPUT_FILE, "w", encoding="utf-8") as batch_file:
  for index, prompt in enumerate(PROMPTS):
    request = {
      "custom_id": f"task-{index}",
      "method": "POST",
      "url": "/v1/chat/completions",
      "body": {
        "model": BATCH_DEPLOYMENT,
        "messages": [
          {"role": "system", "content": SYSTEM_MESSAGE},
          {"role": "user", "content": prompt},
        ],
      },
    }
    batch_file.write(json.dumps(request) + "\n")

print(f"Created {INPUT_FILE} with {len(PROMPTS)} requests.")
```

```output
Created test.jsonl with 3 requests.
```

Don't modify the input blob after you submit the batch job. The job fails with an `input_modified` error if the blob changes while the job is running.

## Upload the input file

Use your user identity to upload `test.jsonl` to the `batch-input` container. Set `STORAGE_ACCOUNT` to your storage account name:

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient

STORAGE_ACCOUNT = "<storage-account-name>"
INPUT_CONTAINER = "batch-input"
INPUT_FILE = "test.jsonl"
ACCOUNT_URL = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net"

credential = DefaultAzureCredential()
input_blob = BlobClient(
  account_url=ACCOUNT_URL,
  container_name=INPUT_CONTAINER,
  blob_name=INPUT_FILE,
  credential=credential,
)

with open(INPUT_FILE, "rb") as data:
  input_blob.upload_blob(data, overwrite=True)

print(f"Uploaded: {input_blob.url}")
```

```output
Uploaded: https://<storage-account-name>.blob.core.windows.net/batch-input/test.jsonl
```

Reference: [BlobClient.upload_blob](/python/api/azure-storage-blob/azure.storage.blob.blobclient#azure-storage-blob-blobclient-upload-blob)

## Submit the batch job

Submit the input blob and specify the output container. Replace the Azure OpenAI resource and storage account placeholders with your values.

> [!NOTE]
> The Blob Storage integration doesn't currently support `metadata`.

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
AZURE_OPENAI_BASE_URL = (
  "https://<azure-openai-resource-name>.openai.azure.com/openai/v1/"
)
STORAGE_ACCOUNT = "<storage-account-name>"
INPUT_BLOB_URL = (
  f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/batch-input/test.jsonl"
)
OUTPUT_CONTAINER_URL = (
  f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/batch-output"
)

token_provider = get_bearer_token_provider(
  DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai = OpenAI(base_url=AZURE_OPENAI_BASE_URL, api_key=token_provider)

batch = openai.batches.create(
  input_file_id=None,
  endpoint="/chat/completions",
  completion_window="24h",
  extra_body={
    "input_blob": INPUT_BLOB_URL,
    "output_folder": {"url": OUTPUT_CONTAINER_URL},
  },
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
```

```output
Batch ID: <batch-id>
Status: validating
```

Save the batch ID for the next step.

Reference: [Azure OpenAI Batch](./batch.md)

## Monitor the batch job

Set `BATCH_ID` to the identifier returned when you submitted the job. The script checks the status every 60 seconds until the job reaches a terminal state:

```python
import time

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

AZURE_OPENAI_BASE_URL = (
  "https://<azure-openai-resource-name>.openai.azure.com/openai/v1/"
)
BATCH_ID = "<batch-id>"
TERMINAL_STATES = {"completed", "failed", "cancelled", "expired"}

token_provider = get_bearer_token_provider(
  DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai = OpenAI(base_url=AZURE_OPENAI_BASE_URL, api_key=token_provider)

batch = openai.batches.retrieve(BATCH_ID)
while batch.status not in TERMINAL_STATES:
  print(f"Batch {BATCH_ID}: {batch.status}")
  time.sleep(60)
  batch = openai.batches.retrieve(BATCH_ID)

print(f"Batch {BATCH_ID}: {batch.status}")
if batch.status == "completed":
  print(f"Output blob: {batch.output_blob}")
  print(f"Error blob: {batch.error_blob}")
elif batch.errors:
  for error in batch.errors.data:
    print(f"Error {error.code}: {error.message}")
```

```output
Batch <batch-id>: validating
Batch <batch-id>: in_progress
Batch <batch-id>: finalizing
Batch <batch-id>: completed
Output blob: https://<storage-account-name>.blob.core.windows.net/batch-output/<batch-output-path>/results.jsonl
Error blob: https://<storage-account-name>.blob.core.windows.net/batch-output/<batch-output-path>/errors.jsonl
```

Reference: [Azure OpenAI Batch status values](./batch.md)

## Download the results

Copy the output blob URL from the completed batch response. Use your user identity to download the results:

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient

OUTPUT_BLOB_URL = (
  "https://<storage-account-name>.blob.core.windows.net/"
  "batch-output/<batch-output-path>/results.jsonl"
)
OUTPUT_FILE = "results.jsonl"

credential = DefaultAzureCredential()
output_blob = BlobClient.from_blob_url(
  blob_url=OUTPUT_BLOB_URL,
  credential=credential,
)

with open(OUTPUT_FILE, "wb") as results_file:
  results_file.write(output_blob.download_blob().readall())

print(f"Downloaded: {OUTPUT_FILE}")
```

```output
Downloaded: results.jsonl
```

The batch response always includes `output_blob` and `error_blob` URLs. A blob is created only when it has content. For example, if every request succeeds, `errors.jsonl` isn't created.

Reference: [BlobClient.download_blob](/python/api/azure-storage-blob/azure.storage.blob.blobclient#azure-storage-blob-blobclient-download-blob)

## Related content

- [Use Azure OpenAI Batch](./batch.md)
- [Use Azure OpenAI Batch with the REST API](./batch.md?pivots=rest-api)
- [Authenticate to Azure OpenAI with Microsoft Entra ID](./managed-identity.md)
