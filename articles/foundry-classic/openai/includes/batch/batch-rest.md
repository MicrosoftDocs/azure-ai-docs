---
title: Azure OpenAI Global Batch REST
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI model global batch REST
manager: nitinme
ms.date: 07/22/2024
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Azure OpenAI resource with a model of the deployment type `Global-Batch` deployed. You can refer to the [resource creation and model deployment guide](../../how-to/create-resource.md) for help with this process.


## Preparing your batch file

Like [fine-tuning](../../how-to/fine-tuning.md), global batch uses files in JSON lines (`.jsonl`) format. Below are some example files with different types of supported content:

### Input format

#### Responses API

# [Standard input](#tab/standard-input)

```JSONL
{"custom_id": "task-0", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": "When was Microsoft founded, and by whom?"}}
{"custom_id": "task-1", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": "When was XBOX merged into Microsoft?"}}
{"custom_id": "task-2", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": "What is Visual Basic?"}}
```

# [Base64 encoded image](#tab/base64)

**Input with base64 encoded image:**

```JSONL
{"custom_id": "task-3", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type":"input_text","text":"Describe this picture:"},{"type":"input_image","image_url":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=","detail":"auto"}]}],"max_output_tokens": 1000}}
```

# [Image url](#tab/image-url)

**Input with image url:**

```JSONL
{"custom_id": "task-3", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type": "input_text", "text": "What’s in this image?"},{"type": "input_image","image_url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-foundry/openai/media/how-to/generated-seattle.png", "detail": "low"}]}],"max_output_tokens": 1000}}
{"custom_id": "task-4", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type": "input_text", "text": "What’s in this image?"},{"type": "input_image","image_url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-foundry/openai/media/how-to/generated-seattle.png", "detail": "high"}]}],"max_output_tokens": 1000}}
{"custom_id": "task-5", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type": "input_text", "text": "What’s in this image?"},{"type": "input_image","image_url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-foundry/openai/media/how-to/generated-seattle.png", "detail": "auto"}]}],"max_output_tokens": 1000}}
```

# [Structured outputs](#tab/structured-outputs)

```JSONL
{"custom_id": "task-4", "method": "POST", "url": "/v1/responses", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "input": [{"role": "system", "content": "Extract the event information."}, {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}], "text": {"format": {"type": "json_schema", "name": "CalendarEventResponse", "schema": {"type": "object", "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "participants": {"type": "array", "items": {"type": "string"}}}, "required": ["name", "date", "participants"], "additionalProperties": false}, "strict": true}}}}
```

---

#### Chat completions API

# [Standard input](#tab/standard-input)


```JSONL
{"custom_id": "task-0", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "When was Microsoft founded?"}]}}
{"custom_id": "task-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "When was the first XBOX released?"}]}}
{"custom_id": "task-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are an AI assistant that helps people find information."}, {"role": "user", "content": "What is Altair Basic?"}]}}
```

# [Base64 encoded image](#tab/base64)

**Input with base64 encoded image:**

```JSONL
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type":"text","text":"Describe this picture:"},{"type":"image_url","image_url":{"url":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="}}]}],"max_tokens": 1000}}
```

# [Image url](#tab/image-url)

**Input with image url:**

```JSONL
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": [{"type": "text", "text": "What’s in this image?"},{"type": "image_url","image_url": {"url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-foundry/openai/media/how-to/generated-seattle.png", "detail": "high"}}]}],"max_tokens": 1000}}
```
The `detail` parameter tells the model what level of detail to use when processing and understanding the image (`low`, `high`, or `auto` to let the model decide). If you skip the parameter, the model will use `auto`.

# [Structured outputs](#tab/structured-outputs)

```JSONL
{"custom_id": "task-0", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME", "messages": [{"role": "system", "content": "Extract the event information."}, {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}], "response_format": {"type": "json_schema", "json_schema": {"name": "CalendarEventResponse", "strict": true, "schema": {"type": "object", "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "participants": {"type": "array", "items": {"type": "string"}}}, "required": ["name", "date", "participants"], "additionalProperties": false}}}}}
```

---


The `custom_id` is required to allow you to identify which individual batch request corresponds to a given response. Responses won't be returned in identical order to the order defined in the `.jsonl` batch file.

`model` attribute should be set to match the name of the Global Batch deployment you wish to target for inference responses.

> [!IMPORTANT]
> The `model` attribute must be set to match the name of the Global Batch deployment you wish to target for inference responses. The **same Global Batch model deployment name must be present on each line of the batch file.** If you want to target a different deployment you must do so in a separate batch file/job.
>
> For the best performance we recommend submitting large files for batch processing, rather than a large number of small files with only a few lines in each file.


### Create input file

For this article we'll create a file named `test.jsonl` and will copy the contents from standard input code block above to the file. You'll need to modify and add your global batch deployment name to each line of the file.

## Upload batch file

Once your input file is prepared, you first need to upload the file to then be able to initiate a batch job. File upload can be done both programmatically or via the Microsoft Foundry portal. This example demonstrates uploading a file directly to your Azure OpenAI resource. Alternatively, you can [configure Azure Blob Storage for Azure OpenAI Batch](../../how-to/batch-blob-storage.md).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```http
curl -X POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/files \
  -H "Content-Type: multipart/form-data" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=batch" \
  -F "file=@C:\\batch\\test.jsonl;type=application/json" \
  -F "expires_after.seconds=1209600" \
  -F "expires_after.anchor=created_at"

```

The above code assumes a particular file path for your test.jsonl file. Adjust this file path as necessary for your local system. 

By adding the optional `"expires_after.seconds=1209600"` and `"expires_after.anchor=created_at"` parameters  you're setting your upload file to expire in 14 days. There's a max limit of 500 batch input files per resource when no expiration is set. By setting a value for expiration the number of batch files per resource is increased to 10,000 files per resource. You can set to a number between 1209600-2592000. This is equivalent to 14-30 days. To remove batch input file limits use [Batch with Azure Blob Storage](../../how-to/batch-blob-storage.md).



**Output:**

```json
{
  "status": "processed",
  "bytes": 817,
  "purpose": "batch",
  "filename": "test.jsonl",
  "expires_at": 1744607747,
  "id": "file-7733bc35e32841e297a62a9ee50b3461",
  "created_at": 1743398147,
  "object": "file"
}

```


## Track file upload status

Depending on the size of your upload file it might take some time before it's fully uploaded and processed. To check on your file upload status run:

```http
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/files/{file-id} \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

**Output:**

```json
{
  "status": "processed",
  "bytes": 686,
  "purpose": "batch",
  "filename": "test.jsonl",
  "expires_at": 1744607747,
  "id": "file-7733bc35e32841e297a62a9ee50b3461",
  "created_at": 1721408291,
  "object": "file"
}

```

## Create batch job

Once your file has uploaded successfully you can submit the file for batch processing.

```http
curl -X POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/batches \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_file_id": "file-abc123",
    "endpoint": "/chat/completions",
    "completion_window": "24h",
    "output_expires_after": {
        "seconds": 1209600
    },
    "anchor": "created_at"
  }'
```

Here you can optionally add  `"output_expires_after":{"seconds": 1209600},` and `"anchor": "created_at"` so that your output files expire in 14 days.

> [!NOTE]
> Currently the completion window must be set to `24h`. If you set any other value than `24h` your job will fail. Jobs taking longer than 24 hours will continue to execute until canceled.

**Output:**

```json
{
  "cancelled_at": null,
  "cancelling_at": null,
  "completed_at": null,
  "completion_window": "24h",
  "created_at": "2024-07-19T17:13:57.2491382+00:00",
  "error_file_id": null,
  "expired_at": null,
  "expires_at": "2024-07-20T17:13:57.1918498+00:00",
  "failed_at": null,
  "finalizing_at": null,
  "id": "batch_fe3f047a-de39-4068-9008-346795bfc1db",
  "in_progress_at": null,
  "input_file_id": "file-21006e70789246658b86a1fc205899a4",
  "errors": null,
  "metadata": null,
  "object": "batch",
  "output_file_id": null,
  "request_counts": {
    "total": null,
    "completed": null,
    "failed": null
  },
  "status": "Validating"
}

```

## Track batch job progress

Once you have created batch job successfully you can monitor its progress either in the Studio or programmatically. When checking batch job progress we recommend waiting at least 60 seconds in between each status call.

```http
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/batches/{batch_id} \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

**Output:**

```json
{
  "cancelled_at": null,
  "cancelling_at": null,
  "completed_at": null,
  "completion_window": "24h",
  "created_at": "2024-07-19T17:33:29.1619286+00:00",
  "error_file_id": null,
  "expired_at": null,
  "expires_at": "2024-07-20T17:33:29.1578141+00:00",
  "failed_at": null,
  "finalizing_at": null,
  "id": "batch_e0a7ee28-82c4-46a2-a3a0-c13b3c4e390b",
  "in_progress_at": null,
  "input_file_id": "file-c55ec4e859d54738a313d767718a2ac5",
  "errors": null,
  "metadata": null,
  "object": "batch",
  "output_file_id": null,
  "request_counts": {
    "total": null,
    "completed": null,
    "failed": null
  },
  "status": "Validating"
}

```

The following status values are possible:

|**Status**| **Description**|
|---|---|
|`validating`|The input file is being validated before the batch processing can begin. |
|`failed`|The input file has failed the validation process. |
| `in_progress`|The input file was successfully validated and the batch is currently running. |
| `finalizing`|The batch has completed and the results are being prepared. |
| `completed`|The batch has been completed and the results are ready.  |
| `expired`|The batch wasn't able to be completed within the 24-hour time window.|
| `cancelling`|The batch is being `cancelled` (This can take up to 10 minutes to go into effect.) |
| `cancelled`|the batch was `cancelled`.|


## Retrieve batch job output file

```http
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/files/{output_file_id}/content \
  -H "api-key: $AZURE_OPENAI_API_KEY" > batch_output.jsonl
```

### Additional batch commands

### Cancel batch

Cancels an in-progress batch. The batch will be in status `cancelling` for up to 10 minutes, before changing to `cancelled`, where it will have partial results (if any) available in the output file.

```http
curl -X POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/batches/{batch_id}/cancel \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

### List batch

List existing batch jobs for a given Azure OpenAI resource.

```http
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/batches \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

The list API call is paginated. The response contains a boolean `has_more` to indicate when there are more results to iterate through.

<a id="List"></a>

### List batch (Preview)

Use the REST API to list all batch jobs with additional sorting/filtering options.

```http
curl "YOUR_RESOURCE_NAME.openai.azure.com/batches?api-version=2025-04-01-preview&$filter=created_at%20gt%201728773533%20and%20created_at%20lt%201729032733%20and%20status%20eq%20'Completed'&$orderby=created_at%20asc" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

To avoid the error `URL rejected: Malformed input to a URL function` spaces are replaced with `%20`.
