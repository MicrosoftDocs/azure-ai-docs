---
title: "Batch analysis and processing"
titleSuffix: Foundry Tools
description: Learn about the Document Intelligence Batch analysis API
author: laujan
ms.service: azure-ai-document-intelligence
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-4.0.0'
---

# Document Intelligence batch analysis

The batch analysis API allows you to bulk process up to 10,000 documents using one request. Instead of analyzing documents one by one and keeping track of their respective request IDs, you can simultaneously analyze a collection of documents like invoices, loan papers, or custom documents. The input documents must be stored in an Azure blob storage container. Once the documents are processed, the API writes the results to a specified storage container.

## Batch analysis limits

* The maximum number of document files that can be in a single batch request is 10,000.
* Batch operation results are retained for 24 hours after completion. The batch operation status is no longer available 24 hours after batch processing is completed. The input documents and respective result files remain in the storage containers provided.

## Prerequisites

* An active Azure subscription. If you don't have an Azure subscription, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

*  A [Document Intelligence Azure Resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer): once you have your Azure subscription, create a Document Intelligence resource in the Azure portal. You can use the free pricing tier (F0) to try the service. After your resource is deployed, select **"Go to resource"** to retrieve your **key** and **endpoint**. You need the resource key and endpoint to connect your application to the Document Intelligence service. You can also find these values on the **Keys and Endpoint** page in Azure portal.

*  An [Azure Blob Storage account](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). [Create two containers](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) in your Azure Blob Storage account for your source and result files:

     * **Source container**: This container is where you upload document files for analysis.
     * **Result container**: This container is where results from the batch analysis API are stored.

### Storage container authorization

To allow the API to process documents and write results in your Azure storage containers, you must authorize using one of the following two options:


**✔️ Managed Identity**. A managed identity is a service principal that creates a Microsoft Entra identity and specific permissions for an Azure managed resource. Managed identities enable you to run your Document Intelligence application without having to embed credentials in your code, a safer way to grant access to storage data without including access signature tokens (SAS) in your code.

Review [Managed identities for Document Intelligence](../authentication/managed-identities.md) to learn how to enable a managed identity for your resource and grant it access to your storage container.

> [!IMPORTANT]
>
> When using managed identities, don't include a SAS token URL with your HTTP requests. Using managed identities replaces the requirement for you to include shared access signature tokens (SAS).


**✔️ Shared Access Signature (SAS)**. A shared access signature is a URL that grants restricted access to your storage container. To use this method, create Shared Access Signature (SAS) tokens for your source and result containers. Go to the storage container in Azure portal and select **"Shared access tokens"** to generate SAS token and URL.

* Your **source** container or blob must designate **read**, **write**, **list**, and **delete** permissions.
* Your **result** container or blob must designate **write**, **list**, **delete** permissions.

:::image type="content" source="../media/sas-tokens/sas-permissions.png" alt-text="Screenshot that shows the SAS permission fields in the Azure portal.":::

Review [**Create SAS tokens**](../authentication/create-sas-tokens.md) to learn more about generating SAS tokens and how they work.

## Call the batch analysis API

### 1. Specify the input files

The batch API supports two options for specifying the files to be processed.

* If you want to process all the files in a container or a folder, and the number of files is less than the 10000 limit, use the ```azureBlobSource``` object in your request.

    ```bash
    POST {endpoint}/documentintelligence/documentModels/{modelId}:analyzeBatch?api-version=2024-11-30

    {
      "azureBlobSource": {
        "containerUrl": "https://myStorageAccount.blob.core.windows.net/myContainer?mySasToken"
      
    },
    {
       "resultContainerUrl": "https://myStorageAccount.blob.core.windows.net/myOutputContainer?mySasToken",
       "resultPrefix": "trainingDocsResult/"
    }


    ```

* If you don't want to process all the files in a container or folder, but rather specific files in that container or folder, use the ```azureBlobFileListSource``` object. This operation requires a File List JSONL file which lists the files to be processed. Store the JSONL file in the root folder of the container. Here's an example JSONL file with two files listed:

  ```json
  {"file": "Adatum Corporation.pdf"}
  {"file": "Best For You Organics Company.pdf"}
  ```

Use a file list `JSONL` file with the following conditions:

  * When you need to process specific files instead of all files in a container;
  * When the total number of files in the input container or folder exceeds the 10,000 file batch processing limit;
  * When you want more control over which files get processed in each batch request;

   ```bash
   POST {endpoint}/documentintelligence/documentModels/{modelId}:analyzeBatch?api-version=2024-11-30

   {
     "azureBlobFileListSource": {
       "containerUrl": "https://myStorageAccount.blob.core.windows.net/myContainer?mySasToken",
       "fileList": "myFileList.jsonl"
       ...
     },
     ...
   }

   ```

A container URL or a container SAS URL is required in both options. Use container URL if using managed Identity to access your storage container. If you're using Shared Access Signature (SAS), use a SAS URL.


### 2. Specify the results location

* Specify the Azure Blob Storage container URL (or container SAS URL) for where you want your results to be stored using `resultContainerURL` parameter. We recommend using separate containers for source and results to prevent accidental overwriting.

* Set the `overwriteExisting` Boolean property to `False` and prevent overwriting any existing results for the same document. If you'd like to overwrite any existing results, set the Boolean to `True`. You're still billed for processing the document even if any existing results aren't overwritten.

* Use `resultPrefix` to group and store results in a specific container folder.


### 3. Build and run the POST request

Remember to replace the following sample container URL values with real values from your Azure Blob storage containers.

This example shows a POST request with `azureBlobSource` input
```bash
POST {endpoint}/documentintelligence/documentModels/{modelId}:analyzeBatch?api-version=2024-11-30

{
  "azureBlobSource": {
    "containerUrl": "https://myStorageAccount.blob.core.windows.net/myContainer?mySasToken",
    "prefix": "inputDocs/"
  },
  {
  "resultContainerUrl": "https://myStorageAccount.blob.core.windows.net/myOutputContainer?mySasToken",
  "resultPrefix": "batchResults/",
  "overwriteExisting": true
}

```

This example shows a POST request with `azureBlobFileListSource` and a file list input


```bash
POST {endpoint}/documentintelligence/documentModels/{modelId}:analyzeBatch?api-version=2024-11-30

{
   "azureBlobFileListSource": {
      "containerUrl": "https://myStorageAccount.blob.core.windows.net/myContainer?mySasToken",
      "fileList": "myFileList.jsonl"
    },
{
  "resultContainerUrl": "https://myStorageAccount.blob.core.windows.net/myOutputContainer?mySasToken",
  "resultPrefix": "batchResults/",
  "overwriteExisting": true
}

```

Here's an example **successful** response

```bash
202 Accepted
Operation-Location: /documentintelligence/documentModels/{modelId}/analyzeBatchResults/{resultId}?api-version=2024-11-30
```

### 4. Retrieve API results

Use the `GET` operation to retrieve batch analysis results after the POST operation is executed. The GET operation fetches status information, batch completion percentage, and operation creation and update date/time. This information is **only retained for 24 hours** after the batch analysis is completed.


```bash
GET {endpoint}/documentintelligence/documentModels/{modelId}/analyzeBatchResults/{resultId}?api-version=2024-11-30
200 OK

{
  "status": "running",      // notStarted, running, completed, failed
  "percentCompleted": 67,   // Estimated based on the number of processed documents
  "createdDateTime": "2021-09-24T13:00:46Z",
  "lastUpdatedDateTime": "2021-09-24T13:00:49Z"
...
}
```

### 5. Interpret status messages

For each document processed, a status is assigned, either `succeeded`, `failed`, `running`, `notStarted`, or `skipped`. A source URL, which is the source blob storage container for the input document, is provided.

* Status `notStarted` or `running`. The batch analysis operation isn't initiated or isn't completed. Wait until the operation is completed for all documents.

* Status `completed`. The batch analysis operation is finished.

* Status `succeeded`. The batch operation was successful, and input document was processed. The results are available at `resultUrl`, which is created by combining `resultContainerUrl`, `resultPrefix`, `input filename`, and `.ocr.json` extension. **Only files that have succeeded have the property `resultUrl`**.

  Example of a `succeeded` status response:


  ```bash
  {
      "resultId": "myresultId-",
      "status": "succeeded",
      "percentCompleted": 100,
      "createdDateTime": "2025-01-01T00:00:000",
      "lastUpdatedDateTime": "2025-01-01T00:00:000",
      "result": {
          "succeededCount": 10,000,
          "failedCount": 0,
          "skippedCount": 0,
          "details": [
              {
                  "sourceUrl": "https://{your-source-container}/inputFolder/document1.pdf",
                  "resultUrl": "https://{your-result-container}/resultsFolder/document1.pdf.ocr.json",
                  "status": "succeeded"
              },
            ...
              {
                  "sourceUrl": "https://{your-source-container}/inputFolder/document10000.pdf",
                  "resultUrl": "https://{your-result-container}/resultsFolder/document10000.pdf.ocr.json",
                  "status": "succeeded"
              }
         ]

       }
  }
  ```

* Status `failed`. This error is only returned if there are errors in the overall batch request. Once the batch analysis operation starts, the individual document operation status doesn't affect the status of the overall batch job, even if all the files have the status `failed`.

    Example of a `failed` status response:

    ```bash
    [
        "result": {
        "succeededCount": 0,
        "failedCount": 2,
        "skippedCount": 0,
        "details": [
            "sourceUrl": "https://{your-source-container}/inputFolder/document1.jpg",
            "status": "failed",
            "error": {
                "code": "InvalidArgument",
                "message": "Invalid argument.",
                "innererror": {
                  "code": "InvalidSasToken",
                  "message": "The shared access signature (SAS) is invalid: {details}"
                    }
                }
            ]
        }
    ]
    ...
    ```

* Status `skipped`: Typically, this status happens when output for the document is already present in the specified output folder and the `overwriteExisting` Boolean property is set to `false`.

  Example of `skipped` status response:

   ```bash
   [
       "result": {
       "succeededCount": 3,
       "failedCount": 0,
       "skippedCount": 2,
       "details": [
           ...
           "sourceUrl": "https://{your-source-container}/inputFolder/document1.pdf",
           "status": "skipped",
           "error": {
               "code": "OutputExists",
               "message": "Analysis skipped because result file https://{your-result-container}/resultsFolder/document1.pdf.ocr.json already exists."
                }
           ]
       }
   ]
   ...
   ```

  > [!NOTE]
  > Analysis results aren't returned for individual files until analysis for the entire batch is completed. To track detailed progress beyond `percentCompleted`, you can monitor `*.ocr.json` files as they're written into the    `resultContainerUrl`.

## Next steps

[View code samples on GitHub.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/documentintelligence/azure-ai-documentintelligence/samples/sample_analyze_batch_documents.py)
