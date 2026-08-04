---
title: How to use the Azure AI Content Safety Provenance Detect API
titleSuffix: Azure AI services
description: Learn how to use the Azure AI Content Safety Provenance Detect API, what signals it can detect, common use cases, and current limitations.
author: ssalgadodev
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 07/22/2026
ms.author: ssalgado
ai-usage: ai-assisted
---

# How to use the Content Provenance Detection API

The Detect API helps you identify C2PA Content Credentials and invisible watermarking markers in media files. This guide shows you how to use the API to analyze image, audio, and video content for supported provenance indicators.


You can also use the [website version](https://aka.ms/ProvenanceValidationSite) to perform provenance detection without writing code.

## About provenance detection

The Content Provenance Detection API analyzes media files to identify embedded provenance information that indicates:

- **Authenticity**: Whether content is certified by a trusted source.
- **Origin**: Where and when the media was created.
- **Modifications**: Whether the content is altered since creation.
- **Responsible AI markers**: Indicators that the content was created or modified using AI.

This information is particularly useful for organizations that need to verify the integrity of media content or ensure compliance with content authenticity requirements.


## Prerequisites

Before you begin, make sure you have:

- **An active Azure subscription**: If you don't have one, create a free account at [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/).
- **Azure CLI installed**: Download the [Azure CLI from](/cli/azure/install-azure-cli).
- **Access to the Provenance Detection API**: This API is available through the Azure AI Content Safety service.
- **PowerShell or another REST client**: You need a tool to send HTTP requests. The examples in this guide use PowerShell, but you can also use curl, Postman, or any REST client.
- **Media files to analyze**: Prepare image or video files that you want to analyze. You can store these files in Azure Blob Storage or make them accessible through a public URL.

## Set up your Azure environment

### Create an Azure AI Content Safety resource

The Content Provenance Detection API is part of the Azure AI Content Safety service. Follow these steps to create a new resource:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Select **Create a resource** and search for **Content Safety**.
1. Select **Create** on the Content Safety result.
1. Fill in the resource details:
   1. **Name**: Enter a descriptive name for your resource, such as `my-provenance-detector`
   1. **Subscription**: Select your Azure subscription
   1. **Resource group**: Create a new resource group or select an existing one
   1. **Region**: Choose a region close to your location or where your data resides
   1. **Pricing tier**: Select the appropriate tier for your usage needs
1. Select **Review + create**, and then select **Create**.

### Set up Azure Blob Storage

To use the Content Provenance Detection API efficiently, store your media files in Azure Blob Storage. By using Azure Blob Storage, the API can access your files securely without downloading them to your local machine.

**Create a storage account:**

If you already have a storage account, skip to the next step. Otherwise, run:

```bash
az storage account create \
  --name <your-storage-account> \
  --resource-group <your-rg> \
  --location <your-location> \
  --sku Standard_LRS
```

Replace the following values:
- `<your-storage-account>`: A globally unique name (lowercase, 3-24 characters, alphanumeric only)
- `<your-rg>`: The name of your resource group
- `<your-location>`: An Azure region (for example, `eastus`, `westeurope`)

**Create storage container:**

Create a storage container for media files you want to analyze as input.

```bash
az storage container create --name input --account-name <your-storage-account> --auth-mode login
```

**Enable managed identity authentication:**

The Content Provenance Detection API uses managed identity to access your storage account securely, so you don't need to store or manage credentials.

1. In the Azure portal, go to your **Content Safety resource**.
1. Select **Identity** in the left menu.
1. Under **System assigned**, toggle the status to **On**.
1. Select **Save** and wait for the operation to complete.
1. Copy the **Object (principal) ID** displayed on this page.

**Assign the necessary role:**

Now grant your Content Safety resource permission to read and write blobs in your storage account. Run the following command:

```bash
az role assignment create \
  --assignee <principal-id> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<your-subscription>/resourceGroups/<your-rg>/providers/Microsoft.Storage/storageAccounts/<your-storage-account>
```

Replace:
- `<principal-id>`: The Object (principal) ID you copied above
- `<your-subscription>`: Your Azure subscription ID
- `<your-rg>`: Your resource group name
- `<your-storage-account>`: Your storage account name

> [!NOTE]
> Role assignments can take up to 5 minutes to propagate. Wait before submitting detection jobs to ensure permissions are active.

**Alternative: Using SAS tokens**

If you prefer not to use managed identity, you can generate shared access signature (SAS) tokens for temporary access. See [Grant limited access to Azure Storage resources using shared access signatures](/azure/storage/common/storage-sas-overview) for details.

## Upload Media Files

Once your storage infrastructure is in place, upload the media files you want to analyze to the input container.

**Upload a file to Blob Storage:**

```bash
az storage blob upload \
  --account-name <your-storage-account> \
  --container-name input \
  --name <file-name> \
  --file <local-file-path> \
  --auth-mode login
```

Replace:
- `<your-storage-account>`: Your storage account name
- `<file-name>`: The name you want for the file in storage
- `<local-file-path>`: The path to your local media file

**Get the blob URI:**

After uploading, retrieve the blob URI. You'll need this when submitting detection requests.

```bash
az storage blob url \
  --account-name <your-storage-account> \
  --container-name input \
  --name <file-name> \
  --auth-mode login
```

Save this URI for the next step.

## Submit a Detection Request

Now you're ready to submit a detection request. The API operates asynchronously, which means it returns an operation ID immediately, and you poll for results until processing completes.

**Run the detection workflow:**

The following PowerShell script handles authentication, submits the detection request, and polls for results:

```powershell
# 1) Set your subscription context
az account set --subscription "<your-subscription>"

# 2) Configure your Content Safety resource and blob URI
$endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"
$blobUri = "<your-blob-uri>"  # From the previous step
$version = "2026-07-01-preview"

# 3) Obtain an Azure AD access token for the Content Safety data plane
$token = az account get-access-token `
  --resource "https://cognitiveservices.azure.com" `
  --query accessToken -o tsv

# 4) Prepare the request headers and body
$headers = @{ Authorization = "Bearer $token" }
$body = @{ content = @{ uri = $blobUri } } | ConvertTo-Json

# 5) Submit the detection request
$submit = Invoke-WebRequest -Method POST `
  "$endpoint/contentsafety/provenance/operations:detect?api-version=$version" `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body

# Extract the operation ID from the response
$op = ($submit.Content | ConvertFrom-Json).id
Write-Host "Detection job submitted. HTTP status: $($submit.StatusCode), Operation ID: $op"

# 6) Poll for results (checks for up to 2 minutes)
$deadline = (Get-Date).AddMinutes(2)
do {
  Start-Sleep -Seconds 5
  $poll = Invoke-RestMethod `
    "$endpoint/contentsafety/provenance/operations/${op}?api-version=$version" `
    -Headers $headers
  Write-Host "Status: $($poll.status)"
} while ($poll.status -in @("NotStarted", "Running") -and (Get-Date) -lt $deadline)

# 7) Display the final results
$poll | ConvertTo-Json -Depth 8
```

Replace:
- `<your-subscription>`: Your Azure subscription ID
- `<your-resource-name>`: Your Content Safety resource name
- `<your-blob-uri>`: The blob URI from the upload step

## Understand the Results

The Content Provenance Detection API returns different response structures depending on the outcome. Here's how to interpret each type:

### Successful Detection

When provenance information is found, the response includes a `ProvenanceDetected` outcome with an array of detected markers:

```json
{
  "id": "f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e",
  "kind": "Detect",
  "status": "Succeeded",
  "createdAt": "2026-07-09T14:30:00Z",
  "lastUpdatedAt": "2026-07-09T14:30:05Z",
  "result": {
    "outcome": "ProvenanceDetected",
    "results": [
      {
        "type": "Watermark",
        "provider": "[Example Provider]",
        "modelName": "[Example Model]",
        "timestamp": "2026-01-01T00:00:00Z"
      },
      {
        "type": "C2PA",
        "provider": "[Example Provider]",
        "modelName": "[Example Model]",
        "timestamp": "2026-01-01T00:00:00Z"
      }
    ]
  }
}
```

Each result object contains:
- **type**: The kind of provenance marker (`Watermark`, `C2PA`, etc.)
- **provider**: The organization that embedded or verified this marker
- **modelName**: The detection model used to identify the marker
- **timestamp**: When the marker was created or verified

### No Provenance Detected

When the API analyzes a file and finds no embedded provenance information, it returns:

```json
{
  "id": "f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e",
  "kind": "Detect",
  "status": "Succeeded",
  "createdAt": "2026-07-09T14:30:00Z",
  "lastUpdatedAt": "2026-07-09T14:30:03Z",
  "result": { "outcome": "NoProvenanceDetected" }
}
```

This doesn't mean the file is inauthentic; it simply means no recognized provenance markers were found.

### Detection Failure

If the API encounters an error during processing, you'll receive a failed status with error details:

```json
{
  "id": "f1e2d3c4-b5a6-47c8-9d0e-1f2a3b4c5d6e",
  "kind": "Detect",
  "status": "Failed",
  "createdAt": "2026-07-09T14:30:00Z",
  "lastUpdatedAt": "2026-07-09T14:30:02Z",
  "error": {
    "code": "InternalError",
    "message": "Detect operation failed. Please retry later."
  }
}
```

### Validation Error

If your request is malformed (for example, missing required fields), you'll receive an HTTP 400 error:

```json
{
  "error": {
    "code": "InvalidRequestBody",
    "message": "content.uri is required."
  }
}
```

## Troubleshooting

### Common Issues

**"Unauthorized" or "Forbidden" error**
- Verify that your API key is correct and associated with the right resource.
- Check that your managed identity has the "Cognitive Services User" role on your Content Safety resource.
- If using SAS tokens, ensure the token hasn't expired.

**"File not found" error**
- Verify that the blob URI is correct and the file exists in your storage container.
- Check that the managed identity has "Storage Blob Data Contributor" role on your storage account.
- Ensure 5 minutes have passed since you assigned the role.

**"Timeout" error**
- Detection can take several seconds depending on file size. Increase the polling timeout in the PowerShell script if needed.
- Check that your Content Safety resource is in a region close to your storage account for better performance.

**"Invalid request body" error**
- Ensure the `content.uri` field is included in your request JSON.
- Verify that the blob URI is properly formatted.

## Next Steps

- Explore the [Azure AI Content Safety documentation](/azure/ai-services/content-safety/) for additional features
