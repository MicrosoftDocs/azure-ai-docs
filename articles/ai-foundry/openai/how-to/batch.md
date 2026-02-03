---
title: "How to use global batch processing with Azure OpenAI in Microsoft Foundry Models"
titleSuffix: Azure OpenAI
description: Learn how to use global batch with Azure OpenAI
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 01/27/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2025
zone_pivot_groups: openai-fine-tuning-batch
monikerRange: 'foundry-classic || foundry'
---

# Getting started with Azure OpenAI batch deployments

The Azure OpenAI Batch API is designed to handle large-scale and high-volume processing tasks efficiently. Process asynchronous groups of requests with separate quota, with 24-hour target turnaround, at [50% less cost than global standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than send one request at a time you send a large number of requests in a single file. Global batch requests have a separate enqueued token quota avoiding any disruption of your online workloads.  

Key use cases include:

* **Large-Scale Data Processing:** Quickly analyze extensive datasets in parallel.

* **Content Generation:** Create large volumes of text, such as product descriptions or articles.

* **Document Review and Summarization:** Automate the review and summarization of lengthy documents.

* **Customer Support Automation:** Handle numerous queries simultaneously for faster responses.

* **Data Extraction and Analysis:** Extract and analyze information from vast amounts of unstructured data.

* **Natural Language Processing (NLP) Tasks:** Perform tasks like sentiment analysis or translation on large datasets.

* **Marketing and Personalization:** Generate personalized content and recommendations at scale.

> [!TIP]
> If your batch jobs are so large that you are hitting the enqueued token limit even after maxing out the quota for your deployment, certain regions now support a new feature that allows you to queue multiple batch jobs with exponential backoff. 
>
>Once your enqueued token quota is available, the next batch job can be created and kicked off automatically. To learn more, see [**automating retries of large batch jobs with exponential backoff**](#queueing-batch-jobs).

> [!IMPORTANT]
> We aim to process batch requests within 24 hours; we don't expire the jobs that take longer. You can [cancel](#cancel-batch) the job anytime. When you cancel the job, any remaining work is canceled and any already completed work is returned. You'll be charged for any completed work.
>
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).  

## Batch support

# [Global Batch](#tab/global-batch)

### Global batch model availability

[!INCLUDE [Global batch](../includes/model-matrix/global-batch.md)]

Registration is required for access to `gpt-5` and `o3` For more information see, our [reasoning models guide](./reasoning.md).

# [Data Zone Batch](#tab/datazone-batch)

### Data zone batch model availability

[!INCLUDE [Data zone batch](../includes/model-matrix/global-batch-datazone.md)]

Registration is required for access to `gpt-5` and `o3`. For more information see, our [reasoning models guide](./reasoning.md).

---


> [!NOTE]
> While Global Batch supports older API versions, some models require newer API versions. For example, `o3-mini` isn't supported with `2024-10-21` since it was released after this date. To access the newer models with global batch use the v1 API.<br><br> All batch models support text and image input except `o3-mini`.

### Feature support

The following aren't currently supported:

- Integration with the Assistants API.
- Integration with Azure OpenAI On Your Data feature.

### Batch deployment

> [!NOTE]
> In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) the batch deployment types will appear as `Global-Batch` and `Data Zone Batch`. To learn more about Azure OpenAI deployment types, see our [deployment types guide](../../foundry-models/concepts/deployment-types.md).

> [!TIP]
> We recommend enabling **dynamic quota** for all global batch model deployments to help avoid job failures due to insufficient enqueued token quota. Using dynamic quota allows your deployment to opportunistically take advantage of more quota when extra capacity is available. When dynamic quota is set to off, your deployment will only be able to process requests up to the enqueued token limit that was defined when you created the deployment.

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Foundry portal](../includes/batch/batch-studio.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python](../includes/batch/batch-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST](../includes/batch/batch-rest.md)]

::: zone-end

[!INCLUDE [Quota](../includes/global-batch-limits.md)]

## Batch object

|Property | Type | Definition|
|---|---|---|
| `id` | string | |
| `object` | string| `batch` |
| `endpoint` | string | The API endpoint used by the batch |
| `errors` | object | |
| `input_file_id` | string | The ID of the input file for the batch |
| `completion_window` | string | The time frame within which the batch should be processed |
| `status` | string | The current status of the batch. Possible values: `validating`, `failed`, `in_progress`, `finalizing`, `completed`, `expired`, `cancelling`, `cancelled`. |
| `output_file_id` | string |The ID of the file containing the outputs of successfully executed requests. |
| `error_file_id` | string | The ID of the file containing the outputs of requests with errors. |
| `created_at` | integer | A timestamp when this batch was created (in unix epochs). |
| `in_progress_at` | integer | A timestamp when this batch started progressing (in unix epochs). |
| `expires_at` | integer | A timestamp when this batch will expire (in unix epochs). |
| `finalizing_at` | integer | A timestamp when this batch started finalizing (in unix epochs). |
| `completed_at` | integer | A timestamp when this batch started finalizing (in unix epochs). |
| `failed_at` | integer | A timestamp when this batch failed (in unix epochs) |
| `expired_at` | integer | A timestamp when this batch expired (in unix epochs).|
| `cancelling_at` | integer | A timestamp when this batch started `cancelling` (in unix epochs). |
| `cancelled_at` | integer | A timestamp when this batch was `cancelled` (in unix epochs). |
| `request_counts` | object | Object structure:<br><br> `total` *integer* <br> The total number of requests in the batch.  <br>`completed`  *integer* <br> The number of requests in the batch that have been completed successfully. <br> `failed` *integer* <br> The number of requests in the batch that have failed. 
| `metadata` | map | A set of key-value pairs that can be attached to the batch. This property can be useful for storing additional information about the batch in a structured format. |

## Frequently asked questions (FAQ)

### Can images be used with the batch API?

This capability is limited to certain multi-modal models. Currently only GPT-4o support images as part of batch requests. Images can be provided as input either via [image url or a base64 encoded representation of the image](#input-format). Images for batch are currently not supported with GPT-4 Turbo.

### Can I use the batch API with fine-tuned models?

This is currently not supported.

### Can I use the batch API for embeddings models?

This is currently not supported.

### Does content filtering work with Global Batch deployment?

Yes. Similar to other deployment types, you can create content filters and associate them with the Global Batch deployment type.

### Can I request additional quota?

Yes, from the quota page in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). Default quota allocation can be found in the [quota and limits article](../quotas-limits.md#batch-quota).

### What happens if the API doesn't complete my request within the 24 hour time frame?

We aim to process these requests within 24 hours; we don't expire the jobs that take longer. You can cancel the job anytime. When you cancel the job, any remaining work is canceled and any already completed work is returned. You'll be charged for any completed work.

### How many requests can I queue using batch?

There's no fixed limit on the number of requests you can batch, however, it will depend on your enqueued token quota. Your enqueued token quota includes the maximum number of input tokens you can enqueue at one time.  

Once your batch request is completed, your batch rate limit is reset, as your input tokens are cleared. The limit depends on the number of global requests in the queue. If the Batch API queue processes your batches quickly, your batch rate limit is reset more quickly.

## Troubleshooting

A job is successful when `status` is `Completed`. Successful jobs will still generate an error_file_id, but it will be associated with an empty file with zero bytes.

When a job failure occurs, you'll find details about the failure in the `errors` property:

```json
"value": [
        {
          "id": "batch_80f5ad38-e05b-49bf-b2d6-a799db8466da",
          "completion_window": "24h",
          "created_at": 1725419394,
          "endpoint": "/chat/completions",
          "input_file_id": "file-c2d9a7881c8a466285e6f76f6321a681",
          "object": "batch",
          "status": "failed",
          "cancelled_at": null,
          "cancelling_at": null,
          "completed_at": 1725419955,
          "error_file_id": "file-3b0f9beb-11ce-4796-bc31-d54e675f28fb",
          "errors": {
                "object": “list”,
                "data": [
                {
               "code": "empty_file",
               "message": "The input file is empty. Please ensure that the batch contains at least one   request."
                    }
                ]
          },
          "expired_at": null,
          "expires_at": 1725505794,
          "failed_at": null,
          "finalizing_at": 1725419710,
          "in_progress_at": 1725419572,
          "metadata": null,
          "output_file_id": "file-ef12af98-dbbc-4d27-8309-2df57feed572",

            "request_counts": {
                "total": 10,
                "completed": null,
                "failed": null
            },
        }
```

### Error codes

|Error code | Definition|
|---|---|
|`invalid_json_line`| A line (or multiple) in your input file wasn't able to be parsed as valid json.<br><br> Please ensure no typos, proper opening and closing brackets, and quotes as per JSON standard, and resubmit the request.|
| `too_many_tasks` |The number of requests in the input file exceeds the maximum allowed value of 100,000.<br><br>Please ensure your total requests are under 100,000 and resubmit the job.|
| `url_mismatch` | Either a row in your input file has a URL that doesn’t match the rest of the rows, or the URL specified in the input file doesn’t match the expected endpoint URL. <br><br>Please ensure all request URLs are the same, and that they match the endpoint URL associated with your Azure OpenAI deployment.|
|`model_not_found`|The Azure OpenAI model deployment name that was specified in the `model` property of the input file wasn't found.<br><br> Please ensure this name points to a valid Azure OpenAI model deployment.|
| `duplicate_custom_id` | The custom ID for this request is a duplicate of the custom ID in another request. |
|`empty_batch` | Please check your input file to ensure that the custom ID parameter is unique for each request in the batch.|
|`model_mismatch`| The Azure OpenAI model deployment name that was specified in the `model` property of this request in the input file doesn't match the rest of the file.<br><br>Please ensure that all requests in the batch point to the same Azure OpenAI in Foundry Models model deployment in the `model` property of the request.|
|`invalid_request`| The schema of the input line is invalid or the deployment SKU is invalid. <br><br>Please ensure the properties of the request in your input file match the expected input properties, and that the Azure OpenAI deployment SKU is `globalbatch` for batch API requests.|
| `input_modified` |Blob input has been modified after the batch job has been submitted. |
| `input_no_permissions` | It's not possible to access the input blob. Please check [permissions](/azure/ai-foundry/openai/how-to/role-based-access-control) and network access between the Azure OpenAI account and Azure Storage account.  |

### Known issues

- Resources deployed with Azure CLI won't work out-of-box with Azure OpenAI global batch. This is due to an issue where resources deployed using this method have endpoint subdomains that don't follow the `https://your-resource-name.openai.azure.com` pattern. A workaround for this issue is to deploy a new Azure OpenAI resource using one of the other common deployment methods which will properly handle the subdomain setup as part of the deployment process.

- UTF-8-BOM encoded `jsonl` files aren't supported. JSON lines files should be encoded using UTF-8. Use of Byte-Order-Mark (BOM) encoded files isn't officially supported by the JSON RFC spec, and Azure OpenAI will currently treat BOM encoded files as invalid. A UTF-8-BOM encoded file will currently return the generic error message: "Validation failed: A valid model deployment name couldn't be extracted from the input file. Please ensure that each row in the input file has a valid deployment name specified in the 'model' field, and that the deployment name is consistent across all rows."

- When using [your own storage for batch input data](batch-blob-storage.md), once the batch job is submitted, if the input blob is modified the scoring job will be failed by the service.

## See also

* Learn more about Azure OpenAI [deployment types](../../foundry-models/concepts/deployment-types.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
