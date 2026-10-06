---
title: Customize a premium healthcare AI model with fine-tuning
titleSuffix: Microsoft Foundry
description: Learn how to fine-tune a premium healthcare AI model in Microsoft Foundry — prepare data, create a job, deploy, and evaluate.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 08/18/2026
ms.reviewer: jmerkow
reviewer: jmerkow
ms.author: ssalgado
author: ssalgadodev
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a data scientist, I want to fine-tune a premium healthcare model so that I can improve model performance for my use case.

---

# Customize a premium healthcare AI model with fine-tuning

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

Fine-tuning adapts a premium healthcare AI model to your institution's data distribution and reporting conventions while the model's fundamental task stays the same. Its output aligns more closely to your label vocabulary and institutional style.
To fine-tune a model, you prepare and upload a model-specific training file, create a fine-tuning job, and deploy the result. A job can remain pending until training capacity is available, moves to running, and then reaches a terminal status.

> [!NOTE]
> Premium healthcare models use the OpenAI Python client's Files and
> fine-tuning interfaces after you obtain the client through the Foundry
> project SDK. [Customize a model with fine-tuning](../../openai/how-to/fine-tuning.md)
> covers fine-tuning OpenAI models with the Foundry SDK; this article covers
> premium healthcare models. Model names, schemas, supported training types,
> hyperparameters, and deployment details differ for premium healthcare
> models. Use the fine-tuning page for your selected healthcare model for
> model-specific information.

## Prerequisites

- An Azure subscription. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project in a region that supports your target fine-tuning model.
  If you don't have one, [create a project](../create-projects.md).
- Access to a [premium healthcare model](healthcare-ai-models.md) such as
  [MedImageInsight Premium (preview)](deploy-medimageinsight-premium.md) or
  [CxrReportGen Premium (preview)](deploy-cxrreportgen-premium.md) in the
  model catalog for your project.
- To fine-tune with Entra ID authentication, the **Foundry User** role at the
  AIServices account scope. This role grants
  `Microsoft.CognitiveServices/accounts/AIServices/agents/write`, which the
  fine-tuning data plane requires. Account-key authentication doesn't require
  this role assignment.
- Control-plane permission to create and manage deployments, such as
  **Cognitive Services Contributor** or **Azure AI Account Owner**. For
  details, see
  [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).

> [!IMPORTANT]
> Foundry stores uploaded training and validation data as needed to provide
> fine-tuning. Your training data and fine-tuned models aren't available to
> other customers or model providers. Your training data isn't used to train
> AI foundation models without your permission or instruction.
> For details, see [Data, privacy, and security for Foundry Models
> sold by Azure](../../responsible-ai/openai/data-privacy.md).

## Overview of the fine-tuning process

This process is common to all premium healthcare models. Each model has unique
training data schemas, input and preprocessing requirements, supported
hyperparameters, and evaluation guidance.
Use the individual model page for model-specific information.

Current model-specific guides:

- [CxrReportGen Premium](fine-tune-cxrreportgen-premium.md)
- [MedImageInsight Premium](fine-tune-medimageinsight-premium.md)

1. Verify regional support for inference deployments and fine-tuning jobs.
  Check training capacity and deployment quota separately.
1. Prepare training data in the model-specific format.
1. Upload the training file and, optionally, a validation file.
1. Create the job using model-specific hyperparameter settings.
1. The job remains pending until capacity is available, moves to running, and
   ends in succeeded, failed, or cancelled status.
1. Deploy the fine-tuned model as a distinct deployment.
1. Evaluate whether the fine-tuned model meets your application requirements.

## Capacity, quota, and regional availability

### Check fine-tuning availability and deployment quota

Each premium healthcare model has its own quota for base model and fine-tuned
model deployments. Models don't share quota with each other, and base and
fine-tuned deployments don't share quota. Each quota query is scoped to a
subscription and region.

To determine whether you can fine-tune a particular premium healthcare model
in a region, check for its model-specific
`AIServices.GlobalStandard.<model-name>-finetune` regional quota row. If the
row is absent for your subscription and region, you can't fine-tune the model
there.

One CxrReportGen Premium base model test observed usage accounted
subscription-wide across regions. If base model quota usage doesn't reconcile
with deployments in the queried region, check that model's deployments across
the subscription. All premium healthcare models use the `GlobalStandard`
deployment SKU. To query the model-specific quota rows for a subscription and
region:

```azurecli
az cognitiveservices usage list \
  --location "<region>" \
  --subscription "<subscription-id>" \
  --query "[?contains(name.value, '<model-name>')].{Quota:name.value,Limit:limit}" \
  --output table
```

The quota row without `-finetune` governs base-model deployments. The row with
`-finetune` governs live deployments of fine-tuned models. Its numeric limit
is deployment capacity, not training capacity. This command returns the quota
limit, not current usage or remaining capacity.

> [!NOTE]
> The `-finetune` row identifies regional fine-tuning availability, but its
> numeric value doesn't determine how much you can train. Training capacity is
> configured separately on the AIServices account, and training jobs don't
> consume this deployment quota.

| Model | Inference quota | Fine-tuned deployment quota |
|---|---|---|
| CxrReportGen Premium | `AIServices.GlobalStandard.CXRReportgen-Premium` | `AIServices.GlobalStandard.CXRReportgen-Premium-finetune` |
| MedImageInsight Premium | `AIServices.GlobalStandard.MedImageInsight-Premium` | `AIServices.GlobalStandard.MedImageInsight-Premium-finetune` |

### Regional availability

The following regions are officially supported for all premium healthcare
models. The combined fine-tuning column covers both fine-tuning jobs and
fine-tuned model deployments.

| Region | Base-model deployments | Fine-tuning and fine-tuned deployments |
|---|:---:|:---:|
| East US | ✅ | ✅ |
| East US 2 | ✅ | ✅ |
| West US 2 | ✅ | — |
| Central US | ✅ | — |
| West Central US | ✅ | — |

Experimental fine-tuning support is available in additional regions. Contact
your Microsoft account team for more information.

## Prepare your data

Create a required training file and an optional validation file, each using
the JSONL `messages` envelope used by the fine-tuning service.

### Anatomy of a single record

Each physical line in a JSONL file is one record with a top-level `messages`
array. The exact roles, order, image count, text, and output shape are
model-specific.

The following JSONC schematic shows the shared envelope. It isn't a complete
schema. The object is expanded across lines for readability; in a JSONL file,
store it on one physical line.

```jsonc
{
  "messages": [
    {"role": "...", "content": "..."},
    {"role": "...", "content": "..."}
  ]
}
```

For the exact record schemas and examples, see
[CxrReportGen Premium training data format](fine-tune-cxrreportgen-premium.md#training-data-format)
and
[MedImageInsight Premium training data format](fine-tune-medimageinsight-premium.md#training-data-format).

Before uploading, check these shared requirements:

- JSONL format — one record per line.
- UTF-8 encoding.
- Direct Files API upload and import operations require files smaller than
  512 MB.

> [!NOTE]
> The 512 MB limit applies to the upload method, not the training-data format.
> For files at or above 512 MB and through 9 GB, use the multipart
> [Uploads API](/azure/ai-foundry/openai/authoring-reference-preview#upload-file---start).

For model-specific image requirements, see
[CxrReportGen Premium image preprocessing and requirements](fine-tune-cxrreportgen-premium.md#image-preprocessing-and-requirements)
and
[MedImageInsight Premium image preprocessing and requirements](fine-tune-medimageinsight-premium.md#image-preprocessing-and-requirements).

> [!IMPORTANT]
> Follow the [CxrReportGen Premium training data requirements](fine-tune-cxrreportgen-premium.md#training-data-format)
> or [MedImageInsight Premium training data requirements](fine-tune-medimageinsight-premium.md#training-data-format)
> for the model you selected.
> You're responsible for data suitability, de-identification, retention, access
> control, and compliance. This article doesn't cover healthcare data governance.


## Upload the training file

Upload your training file before creating a job. With the SDK, use the Foundry
project client. For direct cURL requests, use the AIServices resource-host
Files endpoint. A successful upload returns a `file_id`; wait until the file
reaches `processed` status before creating a fine-tuning job.

# [Foundry portal](#tab/portal)

The upload occurs in the fine-tuning job wizard:

1. Start a fine-tuning job as described in
  [Create the fine-tuning job](#create-the-fine-tuning-job).
1. In **Datasets**, under **Training data source**, select an existing dataset
  or use **Upload or drag and drop**.
1. Optionally add a **Validation data source**, and then select **Next**.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = (
    "https://<resource-name>.services.ai.azure.com"
    "/api/projects/<project-name>"
)

credential = DefaultAzureCredential()
project_client = AIProjectClient(
    endpoint=project_endpoint, credential=credential
)
openai_client = project_client.get_openai_client()

with open("train.jsonl", "rb") as f:
    uploaded = openai_client.files.create(
        file=f, purpose="fine-tune"
    )
file_id = uploaded.id
print(f"file id: {file_id}")

# Wait until upload and scanning finish
openai_client.files.wait_for_processing(file_id)
print("file status: processed")
```

Upload an optional validation file through the same Files interface:

```python
with open("validation.jsonl", "rb") as f:
    uploaded_validation = openai_client.files.create(
        file=f, purpose="fine-tune"
    )
validation_file_id = uploaded_validation.id
print(f"validation file id: {validation_file_id}")

openai_client.files.wait_for_processing(validation_file_id)
print("validation file status: processed")
```

# [CLI](#tab/cli)

```bash
curl -s -X POST \
  "https://<resource-name>.services.ai.azure.com/openai/files?api-version=2024-10-21" \
  -H "api-key: <account-key>" \
  -F "purpose=fine-tune" \
  -F "file=@train.jsonl"
# -> { "id": "file-...", "status": "pending", ... }
```

---

For request parameters, response fields, and other file operations, see the
[Upload file REST API reference](/rest/api/azureopenai/files/upload).
To import a file from Azure Blob Storage or a web location instead of
uploading it directly, see the
[Import file REST API reference](/rest/api/azureopenai/files/import).
For files that are 512 MB or larger, use the multipart
[Uploads API](/rest/api/azureopenai/upload-file) instead.

## Create the fine-tuning job

Create a fine-tuning job after the training file reaches `processed` status.
You can create the job in the Foundry portal or programmatically.

All premium healthcare models configure `n_epochs`, `batch_size`, and
`learning_rate_multiplier` under `method.supervised.hyperparameters`. Accepted
ranges and service defaults vary by model. See the
[CxrReportGen Premium hyperparameters](fine-tune-cxrreportgen-premium.md#hyperparameters)
or
[MedImageInsight Premium hyperparameters](fine-tune-medimageinsight-premium.md#hyperparameters)
for the model you selected.

> [!IMPORTANT]
> The request body must include `"trainingType": "globalStandard"`. Omitting
> `trainingType` causes the service to default to `Standard`, which is
> rejected with `400 invalidPayload`.

# [Foundry portal](#tab/portal)

1. In your Foundry project, select **Build** > **Fine-tune**, and then select
   **Start a new fine-tuning job**.
1. In **Basic details**, select a supported **Customization method**, the
  **Model**, and a supported **Training type**. Select **Next**.
1. In **Datasets**, attach the required **Training data source** by selecting
   an existing dataset or **Upload or drag and drop**. Optionally, attach a
   **Validation data source**. Select **Next**.
1. In **Optional settings**, enter a **Display name** and, optionally, a
   **Seed**. Under **Hyperparameter tuning**, review **Batch size**,
   **Number of epochs**, and **Learning rate multiplier**, and select
   **Default** or **Custom** for each value. Select **Submit**.
1. After submission, the job appears in the **Fine-tune** jobs table.

# [Python](#tab/python)

Reuse `openai_client` and `file_id` from
[Upload the training file](#upload-the-training-file). Use your chosen model
name and hyperparameter values.
Optionally, set `suffix` to add a recognizable label to the fine-tuned model
name. The following example also includes the optional `validation_file` and
`seed` values; omit either argument if you don't use one.

```python
job = openai_client.fine_tuning.jobs.create(
    model="<model-name>",
    training_file=file_id,
    validation_file=validation_file_id,
    method={
        "type": "supervised",
        "supervised": {
            "hyperparameters": {
                "n_epochs": 1,
                "batch_size": 8,
                "learning_rate_multiplier": 1.0,
            }
        },
    },
    extra_body={"trainingType": "globalStandard"},
    suffix="<suffix>",
    seed=42,
)
print(f"job id: {job.id}")
print(f"job status: {job.status}")
```

# [CLI](#tab/cli)

Use your chosen model name and hyperparameter values. Replace `<file-id>` with
the ID returned by the upload request.

```bash
curl -s -X POST \
  "https://<resource-name>.services.ai.azure.com/openai/fine_tuning/jobs?api-version=2025-04-01-preview" \
  -H "api-key: <account-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model-name>",
    "training_file": "<file-id>",
    "method": {
      "type": "supervised",
      "supervised": {
        "hyperparameters": {
          "n_epochs": <number-of-epochs>,
          "batch_size": <batch-size>,
          "learning_rate_multiplier": <learning-rate-multiplier>
        }
      }
    },
    "trainingType": "globalStandard",
    "suffix": "<suffix>"
  }'
```

---

For shared fine-tuning operations, request and response fields, job events,
and cancellation, see the
[Fine-tuning REST API reference](/rest/api/microsoft-foundry/azureopenai/fine-tuning?view=rest-microsoft-foundry-2025-04-01-preview&preserve-view=true).

## Monitor the fine-tuning job

# [Foundry portal](#tab/portal)

In the Foundry portal, select **Build** > **Fine-tune** in your project. Use
the jobs table to monitor a job, and open the job details page for more
information.

# [Python](#tab/python)

Reuse `openai_client` from
[Upload the training file](#upload-the-training-file) to check the job status:

```python
job = openai_client.fine_tuning.jobs.retrieve("<job-id>")
print(f"job status: {job.status}")
print(f"fine-tuned model: {job.fine_tuned_model}")

for event in openai_client.fine_tuning.jobs.list_events(job.id):
    print(event.message)
```

Job events can contain warnings or errors. Run the status check again as needed.

# [CLI](#tab/cli)

```bash
curl -s \
  "https://<resource-name>.services.ai.azure.com/openai/fine_tuning/jobs/<job-id>?api-version=2025-04-01-preview" \
  -H "api-key: <account-key>"
```

---

A job stays `pending` while it waits for training capacity, moves to
`running` when capacity is available, and ends in `succeeded`, `failed`, or
`cancelled`. If it succeeds, keep the `fine_tuned_model` value for deployment.
Check the job events for warnings or errors.

For complete job statuses, response fields, events, and cancellation, see the
[Fine-tuning REST API reference](/rest/api/microsoft-foundry/azureopenai/fine-tuning?view=rest-microsoft-foundry-2025-04-01-preview&preserve-view=true).

## Deploy the fine-tuned model

Deploy the fine-tuned model before you run inference against it. Use a
deployment name different from your base model deployment.

Before running the deployment command, verify these shared requirements:

- **Deployment name**: different from any existing deployment in that account.
- **Model identifier** (`--model-name`): the `fine_tuned_model` value from
  the succeeded job, in the format `<Model>.ft-<jobhash>-<suffix>`.
- **Version**: always `1` for fine-tuned models.
- **Format**: `Microsoft`.
- **SKU**: `GlobalStandard`.
- **Capacity**: a value within the available fine-tuned-deployment quota for
  your model and region, such as `1000`.

# [Foundry portal](#tab/portal)

1. Open the completed job details page, and then select
   **Deploy the fine-tuned model**.
1. Enter a **Deployment name**.
1. Select **Global Standard** as the **Deployment type**.
1. Review **Tokens per Minute Rate Limit** and **Guardrails**.
1. Select **Deploy**. The endpoint is ready when the deployment status is
   **Succeeded**.

# [Python](#tab/python)

Use the management SDK to create or update the named deployment. Set
`<deployment-name>` to a distinct deployment name.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
  Deployment,
  DeploymentModel,
  DeploymentProperties,
  Sku,
)

client = CognitiveServicesManagementClient(
  DefaultAzureCredential(), "<subscription-id>"
)
deployment = client.deployments.begin_create_or_update(
  "<resource-group>",
  "<resource-name>",
  "<deployment-name>",
  Deployment(
    properties=DeploymentProperties(
      model=DeploymentModel(
        format="Microsoft",
        name="<fine_tuned_model>",
        version="1",
      )
    ),
    sku=Sku(
      name="GlobalStandard",
      capacity=1000,
    ),
  ),
).result()
print(f"deployment state: {deployment.properties.provisioning_state}")
```

# [CLI](#tab/cli)

```azurecli
az cognitiveservices account deployment create \
  -n "<resource-name>" \
  -g "<resource-group>" \
  --deployment-name "<ft-deployment-name>" \
  --model-name "<fine_tuned_model>" \
  --model-version "1" \
  --model-format "Microsoft" \
  --sku-name "GlobalStandard" \
  --sku-capacity "<capacity>"
```

---

Replace `<fine_tuned_model>` with the `fine_tuned_model` string from the
succeeded job. When `provisioningState` reaches `Succeeded`, the deployment
is ready for inference.

## Evaluate the fine-tuned model

[!INCLUDE [Fine-tuning evaluation caveat](includes/fine-tuning-evaluation-caveat.md)]

For model-specific approaches and metrics, see
[Evaluate CxrReportGen Premium](fine-tune-cxrreportgen-premium.md#evaluate-the-fine-tuned-model)
and
[Evaluate MedImageInsight Premium](fine-tune-medimageinsight-premium.md#evaluate-the-fine-tuned-model).

## Troubleshooting

| Error | Condition | Fix |
|---|---|---|
| File rejected — *"The maximum allowed size is 512 MB"* | Direct Files API operations require files smaller than 512 MB. | Reduce the file size to less than 512 MB, or use the multipart [Uploads API](/azure/ai-foundry/openai/authoring-reference-preview#upload-file---start) for files up to 9 GB. |
| Schema error after file reaches `processed` | `processed` covers upload and scanning only; model-schema validation runs at job preprocessing. | Read the job's error events, fix the records, and re-upload. |
| `400 invalidPayload` — *"does not support fine-tuning with Standard TrainingType"* | Job body is missing `trainingType`. | Set `"trainingType": "globalStandard"`. |
| Job `failed` despite *"Preprocessing completed"* event | That event marks the end of preprocessing, not success. | Treat the terminal job status and error events as authoritative. |
| *"images are not supported for provided model"* (Entra ID auth) | The identity lacks `Microsoft.CognitiveServices/accounts/AIServices/agents/write`. | Grant **Foundry User** at the AIServices account scope. |
| `InsufficientQuota` on fine-tuned deploy | Insufficient fine-tuned deployment quota. Base and fine-tuned deployments use separate quota pools per model. | Check the model's `-finetune` quota limit for the subscription and target region. Remove unused fine-tuned deployments or request more quota. |
| `400 DeploymentError` — *"not ready"* | Inference called before the fine-tuned deployment finished. | Poll `provisioningState` to `Succeeded` before calling the endpoint. |

## Clean up resources

When you no longer need a fine-tuned deployment or the files you uploaded for training and validation, delete them:

- To delete the fine-tuned deployment, see
  [az cognitiveservices account deployment delete](/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest&preserve-view=true#az-cognitiveservices-account-deployment-delete).
- To delete an uploaded file, see the
  [Delete file REST API reference](/rest/api/azureopenai/files/delete).

## Related content

For model-specific hyperparameter information, JSONL schemas, and runnable
examples, see:

- [Fine-tune CxrReportGen Premium](fine-tune-cxrreportgen-premium.md)
- [Fine-tune MedImageInsight Premium](fine-tune-medimageinsight-premium.md)
- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
