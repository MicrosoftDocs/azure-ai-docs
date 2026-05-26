---
title: Register and deploy a custom-weight (BYOW) model on managed compute
description: Learn how to register a Bring Your Own Weights (BYOW) model in Microsoft Foundry by uploading model files from your local machine, and deploy it on managed compute GPUs.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.custom:
  - build-2026
ms.topic: how-to
ms.date: 05/25/2026
ms.author: mopeakande
author: msakande
ms.reviewer: mabables
reviewer: ManojBableshwar
ai-usage: ai-assisted

#CustomerIntent: As an Azure AI developer, I want to register a fine-tuned or custom-weight model in Microsoft Foundry by uploading the weights from my local machine and deploy it on managed compute so that I can serve my own model with the same APIs, identity, and scaling experience as a catalog model.
---

# Register and deploy a custom-weight (BYOW) model on managed compute

Bring Your Own Weights (BYOW) in Microsoft Foundry lets you register a full-weight model — a complete checkpoint that you fine-tuned, distilled, or assembled yourself — into a Foundry project and serve it on [managed compute](deploy-models.md). After registration, your custom model uses the same deployment templates, GPU families, scaling, endpoints, and SDKs as a catalog model.

This article walks through the **local upload** ingestion path: you upload weight files from your local machine to project-managed storage, finalize registration against a catalog **base model**, resolve a deployment template, and deploy the model on managed compute.

> [!NOTE]
> Local upload is the primary ingestion path for BYOW. Other paths — registering from an Azure Machine Learning training job or importing from Hugging Face — follow the same registration object model but are documented separately.

In this article, you learn how to:

> [!div class="checklist"]
> * Register a local model with the one-call `AIProjectClient.beta.models.create()` helper, or with the three-step REST API.
> * Inspect, update, and manage registered model versions.
> * Resolve a deployment template from the base model.
> * Deploy the model on managed compute and send an inference request.

## Prerequisites

- An active Azure subscription with permission to create Microsoft Foundry resources.
- A Microsoft Foundry account and project. To create one, see [Create a Foundry project](../../how-to/create-projects.md).
- The **Cognitive Services Contributor** role (or an equivalent custom role) on the Foundry resource.
- Approved managed-compute quota for the GPU accelerator family you plan to use (A100, H100, H200, or MI300X). For details, see [Deploy open-source AI models with managed compute](deploy-models.md).
- A **base model** in the Foundry model catalog that your weights are derived from or architecturally compatible with — for example, `azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4`. The base model determines which deployment templates and accelerator families are available at deployment time.
- Model artifacts on your local machine:

    | Artifact | Required | Notes |
    |---|---|---|
    | Model weights (`.safetensors`) | Yes | Only SafeTensors is accepted. Can be multi-file sharded. |
    | `config.json` | Yes | Hugging Face-style architecture configuration. |
    | `tokenizer.json` / `tokenizer_config.json` | Recommended | Required by most inference runtimes at serving time. |
    | `generation_config.json`, `special_tokens_map.json` | Optional | Default generation parameters and special tokens. |

- For the SDK examples, Python 3.10 or later and the following packages:

    ```bash
    pip install "azure-ai-projects>=2.2.0" azure-identity azure-mgmt-cognitiveservices python-dotenv openai
    ```

- [AzCopy](/azure/storage/common/storage-use-azcopy-v10) on your `PATH`. The SDK helper and the REST flow both rely on AzCopy to upload weight files directly to project storage.

    ```bash
    # Windows (winget)
    winget install --id Microsoft.Azure.AZCopy.10 -e
    ```

- The `FOUNDRY_PROJECT_ENDPOINT` environment variable set to your project endpoint, which you can find on the **Overview** page of your Foundry project:

    ```bash
    set FOUNDRY_PROJECT_ENDPOINT=https://my-foundry-account.services.ai.azure.com/api/projects/my-project
    ```

## How BYOW registration works

BYOW registration is a **data-plane** operation against your Foundry project; deployment is a **control-plane** operation against the Foundry account. A single BYOW workflow spans both planes:

| Stage | Plane | Operation |
|---|---|---|
| 1. Start pending upload | Data plane | `POST /models/{name}/versions/{version}/startPendingUpload` — returns a SAS URI. |
| 2. Upload weights | Storage | Direct AzCopy upload to the SAS URI. Bypasses Foundry services. |
| 3. Register the model | Data plane | `PUT /models/{name}/versions/{version}` — finalizes the model asset. |
| 4. Resolve deployment template | Data plane | Read the base model's allowed deployment templates and accelerator maps. |
| 5. Deploy on managed compute | Control plane | `PUT /acceleratorDeployments/{name}` — same API as catalog model deployments. |

The Python SDK collapses stages 1–3 into a single `models_create()` call. The Azure Developer CLI does the same with `azd ai models create`. The REST API exposes the three steps individually for full control.

## Register the model

Pick the path that fits your workflow. All three produce the same `FoundryModelDto`.

# [Python SDK](#tab/python)

`AIProjectClient.beta.models.create()` packs the three required steps — `startPendingUpload` → AzCopy upload → `PUT /models` — into a single call and polls until the new model version is observable.

```python
import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FoundryModelWeightType

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_name = "my-gpt-oss-120B"
model_version = "1"
data_folder = "./model-weights"  # local folder with .safetensors, config.json, tokenizer files

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
):
    model = project_client.beta.models.create(
        name=model_name,
        version=model_version,
        source=data_folder,
        weight_type=FoundryModelWeightType.FULL_WEIGHT,
        base_model="azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4",
        description="Fine-tuned gpt-oss-120B for medical Q&A",
        tags={"team": "medical-ai"},
    )

    print(f"Registered: {model.name} v{model.version}")
    print(f"Blob URI:   {model.blob_uri}")
```

| Argument | Description |
|---|---|
| `name`, `version` | Identifier for the model version. |
| `source` | Local folder containing the weight files. The helper uploads every file via AzCopy. |
| `weight_type` | `FoundryModelWeightType.FULL_WEIGHT` for full checkpoints. |
| `base_model` | Catalog model URI. Determines which deployment templates are available later. |
| `description`, `tags` | Free-form metadata. |

# [Azure Developer CLI](#tab/azure-cli)

`azd ai models create` wraps the same three-step flow into one command and renders a progress bar for the upload phase.

```bash
# One-time defaults so you don't need --project-endpoint and --subscription each call
azd ai models init

azd ai models create \
  --name my-gpt-oss-120B \
  --version 1 \
  --source ./model-weights/ \
  --base-model "azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4" \
  --description "Fine-tuned for medical Q&A"
```

Expected output:

```output
Creating model: my-gpt-oss-120B (version 1)
✓ Upload location ready
Step 2/3: Uploading model files...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% (240.0 GB / 240.0 GB) | 53.0 MB/s | Elapsed: 1h 15m | ETA: done
✓ Upload complete
✓ Model registered successfully!
  Name:        my-gpt-oss-120B
  Version:     1
```

# [REST (three steps)](#tab/rest)

Use the REST flow when you need to script the upload yourself or run it from an environment where the SDK and `azd` aren't available.

**Step 1 — Start a pending upload.** Returns a SAS URI scoped to a project-managed blob container. Treat the URI as a secret.

```http
POST {endpoint}/models/my-gpt-oss-120B/versions/1/startPendingUpload?api-version=v1
Authorization: Bearer <token>
Content-Type: application/json

{
  "pendingUploadType": "TemporaryBlobReference"
}
```

```json
{
  "pendingUploadId": "upload-abc123",
  "pendingUploadType": "TemporaryBlobReference",
  "blobReference": {
    "sasUri": "https://projstorage.blob.core.windows.net/models/my-gpt-oss-120B/v1?sp=rcw&se=2026-05-26T20:00:00Z&...",
    "containerPath": "models/my-gpt-oss-120B/v1/",
    "expiresOn": "2026-05-26T20:00:00Z"
  }
}
```

**Step 2 — Upload weight files with AzCopy.** This call goes straight to Azure Storage and does not transit Foundry services.

```bash
azcopy copy "./model-weights/*" \
  "https://projstorage.blob.core.windows.net/models/my-gpt-oss-120B/v1?sp=rcw&se=..." \
  --recursive
```

Verify that every `.safetensors` shard, `config.json`, and the tokenizer files arrived in the container. Step 3 fails with `UploadIncomplete` if shards are missing.

**Step 3 — Finalize registration.** `PUT /models` is asynchronous; the 202 response includes a polling URL. Poll until `provisioningState` is `Succeeded`.

```http
PUT {endpoint}/models/my-gpt-oss-120B/versions/1?api-version=v1
Authorization: Bearer <token>
Content-Type: application/json

{
  "weightType": "FullWeight",
  "baseModel": "azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4",
  "description": "Fine-tuned gpt-oss-120B for medical Q&A",
  "tags": { "team": "medical-ai" }
}
```

Final response (200 OK after polling):

```json
{
  "name": "my-gpt-oss-120B",
  "version": "1",
  "weightType": "FullWeight",
  "baseModel": "azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4",
  "blobUri": "https://<storage>.blob.core.windows.net/<container>",
  "artifactProfile": { "category": "DataOnly", "signals": [] },
  "systemData": { "createdAt": "2026-05-25T15:30:00Z" }
}
```

---

> [!IMPORTANT]
> The `baseModel` field is required and immutable for a given version. If the base model isn't in the catalog or has no approved deployment templates, registration fails with `BaseModelNotFound` or `BaseModelNoDTs`. See [Validation errors](#validation-errors).

## Inspect, update, and manage versions

Once a model version exists, use `beta.models` to get it, list versions, update metadata, retrieve blob credentials, or delete it.

# [Python SDK](#tab/python)

```python
from azure.ai.projects.models import (
    ModelCredentialRequest,
    UpdateModelVersionRequest,
)

# Get a specific version
fetched = project_client.beta.models.get(name=model_name, version=model_version)

# List all versions of one model
for mv in project_client.beta.models.list_versions(name=model_name):
    print(f"  v{mv.version}")

# List the latest version of every model in the project
for mv in project_client.beta.models.list():
    print(f"  {mv.name}@{mv.version}")

# Retrieve a short-lived SAS for the model's blob storage (for inspection, audit, or download)
creds = project_client.beta.models.get_credentials(
    name=model_name,
    version=model_version,
    body=ModelCredentialRequest(blob_uri=fetched.blob_uri),
)

# Update description and tags (weight_type and base_model are immutable)
updated = project_client.beta.models.update(
    name=model_name,
    version=model_version,
    body=UpdateModelVersionRequest(
        description="Updated description",
        tags={"team": "medical-ai", "stage": "validated"},
    ),
)

# Delete a version (blocked if any accelerator deployment references it)
project_client.beta.models.delete(name=model_name, version=model_version)
```

# [Azure Developer CLI](#tab/azure-cli)

```bash
azd ai models list                                          # latest version of each model
azd ai models show --name my-gpt-oss-120B                   # latest version of one model
azd ai models show --name my-gpt-oss-120B --version 1       # specific version
azd ai models delete --name my-gpt-oss-120B --version 1 --force
```

# [REST](#tab/rest)

```http
GET    {endpoint}/models?api-version=v1
GET    {endpoint}/models/{name}/versions?api-version=v1
GET    {endpoint}/models/{name}/versions/{version}?api-version=v1
PATCH  {endpoint}/models/{name}/versions/{version}?api-version=v1
POST   {endpoint}/models/{name}/versions/{version}/getCredentials?api-version=v1
DELETE {endpoint}/models/{name}/versions/{version}?api-version=v1
```

---

`get_credentials` returns a short-lived SAS scoped to the model's blob storage — useful for downloading the weights back to a local machine for inspection or audit. It doesn't grant deployment permission; deployment uses the model reference, not the SAS.

## Resolve a deployment template from the base model

Managed compute deployments require three inputs that aren't on the registered model itself:

| Input | Source |
|---|---|
| `properties.model` | The model reference you just registered. |
| `properties.deploymentTemplate` | A template ID from the **base model's** allowed deployment templates. |
| `properties.acceleratorType` | An accelerator family from the template's `accelerator_maps`. |

You resolve the last two by reading the base model from the Azure ML Registry and inspecting the deployment template it points to. The same machinery powers catalog deployments — see [Deploy a catalog model](deploy-models.md#deploy-a-catalog-model).

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient

SUBSCRIPTION_ID = "<your-subscription-id>"

# Parse the base model URI: azureml://registries/{registry}/models/{model}/versions/{version}
base_model_uri = model.base_model
parts = base_model_uri.replace("azureml://registries/", "").split("/")
registry_name, base_name, base_version = parts[0], parts[2], parts[4]

ml_client = MLClient(
    credential,
    SUBSCRIPTION_ID,
    resource_group="my-rg",
    registry_name=registry_name,
)
base_model_asset = ml_client.models.get(name=base_name, version=base_version)

# Pick the default deployment template (or any entry in allowed_deployment_templates)
dt_uri = base_model_asset.default_deployment_template.asset_id
dt_parts = dt_uri.replace("azureml://registries/", "").split("/")
template = ml_client.deployment_templates.get(name=dt_parts[2], version=dt_parts[4])

# Pick the default accelerator family
accelerator = next(am for am in template.accelerator_maps if am.default)

print(f"Template:    {template.name} v{template.version}")
print(f"Accelerator: {accelerator.accelerator_type} "
      f"({accelerator.number_of_accelerators_per_model_instance} GPUs/instance)")
```

# [REST](#tab/rest)

```http
GET https://cert-<region>.experiments.azureml.net/mrsasset/v2.0/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.MachineLearningServices/registries/azureml-openai-oss/models/gpt-oss-120B/versions/4?api-version=2024-04-01-preview
Authorization: Bearer <token>
```

Relevant response fields:

```json
{
  "name": "gpt-oss-120B",
  "version": "4",
  "default_deployment_template": {
    "assetId": "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-vllm-throughput/versions/1"
  },
  "allowed_deployment_templates": {
    "assetIds": [
      "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-vllm-throughput/versions/1",
      "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-vllm-latency/versions/1",
      "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-sglang-throughput/versions/1"
    ]
  }
}
```

Then fetch the chosen deployment template to inspect its `accelerator_maps` and pick an accelerator family.

---

Most catalog models expose multiple deployment templates. Pick one based on your traffic shape:

| Template suffix | Runtime | Best for |
|---|---|---|
| `*-vllm-throughput` | vLLM | Batch workloads, maximum tokens/sec |
| `*-vllm-latency` | vLLM | Interactive use, low per-request latency |
| `*-sglang-throughput` | SGLang | Prefix-heavy or structured-output workloads |
| `*-sglang-latency` | SGLang | Multi-turn chat, latency-sensitive |

## Deploy on managed compute

Custom-weight deployments use the **same** `acceleratorDeployments` API as catalog model deployments. The only difference is that `properties.model` references your project-registered model with an `azureai://accounts/.../projects/.../models/...` URI instead of a catalog URI.

# [Python SDK](#tab/python)

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    AcceleratorDeployment,
    AcceleratorDeploymentProperties,
    Sku,
)

RG = "my-rg"
ACCOUNT = "my-foundry-account"
PROJECT = "my-project"

cog = CognitiveServicesManagementClient(credential, SUBSCRIPTION_ID)

deployment = AcceleratorDeployment(
    properties=AcceleratorDeploymentProperties(
        model=(
            f"azureai://accounts/{ACCOUNT}/projects/{PROJECT}"
            f"/models/{model_name}/versions/{model_version}"
        ),
        deployment_template=dt_uri,
        accelerator_type=accelerator.accelerator_type,
    ),
    sku=Sku(name="GlobalManagedCompute", capacity=1),  # 1 model instance
)

poller = cog.accelerator_deployments.begin_create_or_update(
    resource_group_name=RG,
    account_name=ACCOUNT,
    deployment_name=f"{model_name}-gpu",
    accelerator_deployment=deployment,
)

result = poller.result()  # blocks ~10-15 min

print(f"State: {result.properties.provisioning_state}")
print(f"GPUs:  {result.properties.total_accelerators}")
print(f"Route: {result.properties.routes.chat_completions_scoring_path}")
```

# [Azure CLI](#tab/azure-cli)

```bash
az cognitiveservices account accelerator-deployment create \
  --name my-foundry-account -g my-rg \
  --deployment-name my-gpt-oss-120B-gpu \
  --model "azureai://accounts/my-foundry-account/projects/my-project/models/my-gpt-oss-120B/versions/1" \
  --deployment-template "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-vllm-throughput/versions/1" \
  --accelerator-type H100_80GB \
  --sku-name GlobalManagedCompute \
  --sku-capacity 1
```

# [REST](#tab/rest)

```http
PUT https://management.azure.com/subscriptions/<sub>/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-foundry-account/acceleratorDeployments/my-gpt-oss-120B-gpu?api-version=2026-04-01-preview
Authorization: Bearer <token>
Content-Type: application/json

{
  "properties": {
    "model": "azureai://accounts/my-foundry-account/projects/my-project/models/my-gpt-oss-120B/versions/1",
    "deploymentTemplate": "azureml://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-vllm-throughput/versions/1",
    "acceleratorType": "H100_80GB"
  },
  "sku": { "name": "GlobalManagedCompute", "capacity": 1 }
}
```

---

Provisioning typically takes 10–15 minutes. When `provisioning_state` is `Succeeded`, the deployment exposes a standard Foundry endpoint and is ready to serve traffic.

For scaling, scale-to-zero, version upgrades, observability, and pricing, see [Manage and scale a deployment](deploy-models.md#manage-and-scale-a-deployment) and [Pricing and billing](deploy-models.md#pricing-and-billing) in the managed compute article.

## Send an inference request

Once the deployment reports `Succeeded`, your custom model is served exactly like a catalog model. Use the OpenAI-compatible route for chat completions:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://my-foundry-account.services.ai.azure.com/openai/v1/",
    api_key="<your-api-key>",
)

response = client.chat.completions.create(
    model="my-gpt-oss-120B-gpu",  # deployment name
    messages=[
        {"role": "user", "content": "Summarize the mechanism of action of metformin."}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
```

For endpoint routing details, custom routes (rerankers, embeddings, speech), and switching between the Azure AI Inference SDK and the OpenAI SDK, see [Send inference requests to the deployment](deploy-models.md#send-inference-requests-to-the-deployment).

## Validation errors

The most common errors you'll encounter during BYOW registration and deployment:

| Error code | Cause | Resolution |
|---|---|---|
| `BaseModelRequired` | The `baseModel` field is missing on `PUT /models`. | Set `baseModel` to a fully-qualified catalog model URI. |
| `BaseModelNotFound` | The catalog has no model matching the supplied URI. | Verify the registry name, model name, and version. |
| `BaseModelNoDTs` | The base model has no approved deployment templates. | Pick a different base model that exposes deployment templates. |
| `BaseModelDeprecated` | The base model has been deprecated. | Pick the current version of the base model in the catalog. |
| `UnsupportedWeightFormat` | One or more weight files are not `.safetensors`. | Re-export the model in SafeTensors format and re-upload. |
| `UploadIncomplete` | Fewer shard files were uploaded than expected. | Re-run AzCopy to upload missing shards before calling `PUT /models`. |
| `UploadExpired` | The SAS URI expired before `PUT /models` was called. | Call `startPendingUpload` again to get a new SAS URI. |
| `ModelVersionConflict` | The version already exists with different content. | Use a different version, or commit the pending upload to the new version. |
| `ModelInUse` | Deletion is blocked because active deployments reference the model. | Delete the dependent accelerator deployments first. |
| `DeploymentTemplateNotCompatible` | The requested template isn't in the base model's `allowed_deployment_templates`. | Pick a template from the base model's allowed list. |

For deployment-time errors (quota, capacity, cold-start latency), see [Troubleshooting](deploy-models.md#troubleshooting) in the managed compute article.

## Related content

- [Deploy open-source AI models with managed compute](deploy-models.md)
- [Create a Foundry project](../../how-to/create-projects.md)
- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Deployment templates reference](../foundry-models/reference/deployment-templates.md)
- [AzCopy documentation](/azure/storage/common/storage-use-azcopy-v10)
