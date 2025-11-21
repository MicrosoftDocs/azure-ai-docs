---
title: Azure OpenAI Global Batch Studio
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI model global batch Studio
manager: nitinme
ms.date: 11/06/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A resource with a model of the deployment type `GlobalBatch` or `DataZoneBatch` deployed.

## Preparing your batch file

Like [fine-tuning](../../how-to/fine-tuning.md), batch uses files in JSON lines (`.jsonl`) format. Below are some example files with different types of supported content:

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

For this article, we'll create a file named `test.jsonl` and will copy the contents from standard input code block above to the file. You'll need to modify and add your global batch deployment name to each line of the file.

## Create batch job

Once your input file is prepared, you first need to upload the file to then be able to initiate a batch job. File upload can be done both programmatically or via the Microsoft Foundry portal. This example demonstrates uploading a file directly to your Azure OpenAI resource. Alternatively, you can [configure Azure Blob Storage for Azure OpenAI Batch](../../how-to/batch-blob-storage.md). 

::: moniker range="foundry-classic"

1. [!INCLUDE [classic-sign-in](../../../includes/classic-sign-in.md)]
2. Select the Azure OpenAI resource where you have a global batch model deployment available.
3. Select **Batch jobs** > **+Create batch jobs**.

    :::image type="content" source="../../media/how-to/global-batch/create-batch-job-empty.png" alt-text="Screenshot that shows the batch job creation experience in Foundry portal." lightbox="../../media/how-to/global-batch/create-batch-job-empty.png":::

4. From the dropdown under **Batch data** > **Upload files** > select **Upload file** and provide the path for the `test.jsonl` file created in the previous step > **Next**.

    :::image type="content" source="../../media/how-to/global-batch/upload-file.png" alt-text="Screenshot that shows upload file experience." lightbox="../../media/how-to/global-batch/upload-file.png":::

Select **Create** to start your batch job.

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [classic-sign-in](../../../default/includes/foundry-sign-in.md)]
2. In the upper-right select **Build**
3. From the left-hand pane select **Models**
4. Select **Batch Jobs** > **create a batch job**

    :::image type="content" source="../../media/how-to/global-batch/batch-create.png" alt-text="Screenshot of new Foundry batch creation experience." lightbox="../../media/how-to/global-batch/batch-create.png":::

::: moniker-end

::: moniker range="foundry-classic"

## Track batch job progress

Once your job is created, you can monitor the job's progress by selecting the Job ID for the most recently created job. By default you will be taken to the status page for your most recently created batch job.


You can track job status for your job in the right-hand pane:

## Retrieve batch job output file

Once your job has completed or reached a terminal state, it will generate an error file and an output file which can be downloaded for review by selecting the respective button with the downward arrow icon.

## Cancel batch

Cancels an in-progress batch. The batch will be in status `cancelling` for up to 10 minutes, before changing to `cancelled`, where it will have partial results (if any) available in the output file.

::: moniker-end

::: moniker range="foundry"

## Track batch job progress

Once your job is created, you can monitor the job's progress by selecting the Job ID for the most recently created job. By default you will be taken to the status page for your most recently created batch job.

You can track job status for your job in the right-hand pane:

## Retrieve batch job output file

Once your job has completed or reached a terminal state, it will generate an error file and an output file which can be downloaded for review by selecting the respective button with the downward arrow icon.

## Cancel batch

Cancels an in-progress batch. The batch will be in status `cancelling` for up to 10 minutes, before changing to `cancelled`, where it will have partial results (if any) available in the output file.

::: moniker-end