---
title: Manage models with deployment templates
titleSuffix: Azure Machine Learning
description: Learn how to publish a deployment template to an Azure Machine Learning registry and pin it to a model so consumers can deploy the model to managed online endpoints with a consistent infrastructure configuration.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
ms.custom: build-2026
author: s-polly
ms.author: scottpolly
ms.date: 05/12/2026
ms.reviewer: sehan
ai-usage: ai-assisted

#CustomerIntent: As a model author, I want to publish a deployment template alongside my registered model so that consumers can deploy the model to a managed online endpoint without configuring infrastructure themselves.
---

# Manage models with deployment templates

This article shows you how to publish a [deployment template](concept-deployment-template.md) to an Azure Machine Learning registry and pin it to a registered model. After you complete the steps, consumers can deploy the model to a managed online endpoint without specifying environment or infrastructure settings themselves.

[!INCLUDE [machine-learning-preview-old-json-schema-note](includes/machine-learning-preview-old-json-schema-note.md)]

## Prerequisites

- An Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/free/).
- An Azure Machine Learning workspace. For more information, see [Manage Azure Machine Learning workspaces](how-to-manage-workspace.md).
- An Azure Machine Learning registry. For more information, see [Create and manage registries](how-to-manage-registries.md).
- The Azure CLI and the `ml` extension installed and signed in. For more information, see [Install and use the CLI (v2)](how-to-configure-cli.md).
- Permissions to create assets in the workspace and in the registry. The `AzureML Data Scientist` role on the workspace and the `AzureML Registry User` role on the registry are sufficient for this article.

## Step 1: Create an environment in your workspace

Author the environment that the deployment template uses. Save the following YAML as `environment.yml` and edit the `image` value to reference your inference image.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: my-inference-env
version: 1
image: <your-acr>.azurecr.io/my-inference-image:1
```

**Example (TF Serving):** TensorFlow Serving publishes a public container image that can be used directly. Use it to follow the rest of this article end-to-end against the well-known `half_plus_two` test model.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: tfs-env
version: 1
image: docker.io/tensorflow/serving:latest
```

# [REST](#tab/rest)

Create the environment version with the [Environment Versions - Create Or Update](/rest/api/azureml/environment-versions/create-or-update) operation.

Get an access token for Azure Resource Manager:

```azurecli
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)
```

Save the request body as `environment-version.json`. For a bring-your-own-container image, set `image` and `osType`:

```json
{
  "properties": {
    "image": "docker.io/tensorflow/serving:latest",
    "osType": "Linux"
  }
}
```

Send a `PUT` request to the workspace environment version path:

```bash
curl -X PUT \
  "https://management.azure.com/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>/environments/my-inference-env/versions/1?api-version=2024-04-01" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @environment-version.json
```

> [!NOTE]
> If you want to create the environment version directly in the registry (and skip Step 2), use the [Registry Environment Versions - Create Or Update](/rest/api/azureml/registry-environment-versions/create-or-update) operation against the registry path.

# [Azure CLI](#tab/cli)

```azurecli
az ml environment create -f environment.yml \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>
```

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<your-subscription-id>",
    resource_group_name="<your-resource-group>",
    workspace_name="<your-workspace>",
)

env = Environment(
    name="my-inference-env",
    version="1",
    image="<your-acr>.azurecr.io/my-inference-image:1",
)
ml_client.environments.create_or_update(env)
```

---

## Step 2: Share the environment to a registry

A deployment template's `environment` field must point to a registry-scoped environment. Share the workspace environment that you created in Step 1 to your registry.

# [REST](#tab/rest)

Sharing copies the workspace environment into the registry. This is a registry data plane operation that runs against the registry's resource provider host, which you look up with a one-time *discovery* call.

First, discover the registry's data plane host. Get a Microsoft Entra token for Azure Resource Manager (you can reuse the `$TOKEN` from Step 1), then read `primaryRegionResourceProviderUri` from the discovery response. Use the registry's primary region in `<your-region>`.

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

RP_HOST=$(curl -s \
  "https://<your-region>.api.azureml.ms/registrymanagement/v1.0/registries/<your-registry>/discovery?api-version=v1.0" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.primaryRegionResourceProviderUri')
```

The `sourceAssetId` uses the workspace's immutable ID (a GUID) and region, not the workspace name. Get both from `az ml workspace show` (the `workspace_id` and `location` fields) or from a workspace `GET` request.

Save the request body as `share-environment.json`:

```json
{
  "properties": {
    "referenceType": "Id",
    "destinationName": "my-inference-env",
    "destinationVersion": "1",
    "sourceAssetId": "azureml://locations/<workspace-location>/workspaces/<workspace-guid>/environments/my-inference-env/versions/1"
  }
}
```

Submit the copy with a `POST` to the registry's `import` endpoint on the discovered host. Sharing is a long-running operation, so the response is `202 Accepted` with an `Azure-AsyncOperation` header that you poll until the copy completes:

```bash
curl -X POST \
  "${RP_HOST%/}/mferp/managementfrontend/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/import?api-version=2021-10-01-dataplanepreview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @share-environment.json
```

# [Azure CLI](#tab/cli)

```azurecli
az ml environment share \
  --name my-inference-env --version 1 \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group> \
  --registry-name <your-registry> \
  --share-with-name my-inference-env --share-with-version 1
```

# [Python SDK](#tab/python)

The Python SDK exposes registry sharing through the workspace `MLClient`.

```python
ml_client.environments.share(
    name="my-inference-env",
    version="1",
    registry_name="<your-registry>",
    share_with_name="my-inference-env",
    share_with_version="1",
)
```

---

## Step 3: Create the deployment template in the registry

Author the deployment template payload and publish it to the registry. Replace `<your-registry>` and the environment reference to match your environment, and adjust `default_instance_type`, `allowed_instance_types`, `environment_variables`, scoring path and port, and probes for your model.

# [REST](#tab/rest)

Save the following JSON as `deployment-template.json` to use as the request body in Step 4. Note the camelCase property names and ISO 8601 durations (for example, `PT50S` is 50 seconds).

```json
{
  "name": "my-deployment-template",
  "version": "1",
  "type": "deploymenttemplates",
  "description": "Deployment template for my-model",
  "deploymentTemplateType": "Managed",
  "environmentId": "azureml://registries/<your-registry>/environments/my-inference-env/versions/1",
  "environmentVariables": {
    "EXAMPLE_VAR": "example-value"
  },
  "instanceCount": 1,
  "defaultInstanceType": "Standard_DS3_v2",
  "allowedInstanceType": [
    "Standard_DS3_v2",
    "Standard_DS4_v2",
    "Standard_DS5_v2"
  ],
  "scoringPath": "/score",
  "scoringPort": 5001,
  "requestSettings": {
    "requestTimeout": "PT50S",
    "maxConcurrentRequestsPerInstance": 2
  },
  "livenessProbe": {
    "initialDelay": "PT30S",
    "period": "PT10S",
    "timeout": "PT2S",
    "failureThreshold": 30,
    "successThreshold": 1
  },
  "readinessProbe": {
    "initialDelay": "PT30S",
    "period": "PT10S",
    "timeout": "PT2S",
    "failureThreshold": 30,
    "successThreshold": 1
  }
}
```

Create the deployment template by issuing a `POST` against the registry's deployment template asset path. Use the registry's primary region in `<your-region>` (the region you specified when you created the registry; for more information, see [Create and manage registries](how-to-manage-registries.md)). Get a Microsoft Entra token for Azure Resource Manager and send the deployment template payload as the request body.

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

curl -X POST \
  "https://<your-region>.api.azureml.ms/genericasset/v2.0/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

# [Azure CLI](#tab/cli)

Save the following YAML as `deployment-template.yml`.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: my-deployment-template
version: 1
description: Deployment template for my-model
deployment_template_type: Managed
environment: azureml://registries/<your-registry>/environments/my-inference-env/versions/1
instance_count: 1
default_instance_type: Standard_DS3_v2
allowed_instance_types:
  - Standard_DS3_v2
  - Standard_DS4_v2
  - Standard_DS5_v2
environment_variables:
  EXAMPLE_VAR: "example-value"
scoring_path: /score
scoring_port: 5001
request_settings:
  request_timeout_ms: 50000
  max_concurrent_requests_per_instance: 2
liveness_probe:
  initial_delay: 30
  period: 10
  timeout: 2
  failure_threshold: 30
  success_threshold: 1
readiness_probe:
  initial_delay: 30
  period: 10
  timeout: 2
  failure_threshold: 30
  success_threshold: 1
```

Create the deployment template in the registry:

```azurecli
az ml deployment-template create -f deployment-template.yml \
  --registry-name <your-registry>
```

For the full schema, see [CLI (v2) deployment template YAML schema](reference-yaml-deployment-template.md).

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import DeploymentTemplate
from azure.identity import DefaultAzureCredential

registry_client = MLClient(
    credential=DefaultAzureCredential(),
    registry_name="<your-registry>",
)

dt = DeploymentTemplate(
    name="my-deployment-template",
    version="1",
    deployment_template_type="Managed",
    environment="azureml://registries/<your-registry>/environments/my-inference-env/versions/1",
    instance_count=1,
    default_instance_type="Standard_DS3_v2",
    allowed_instance_types=["Standard_DS3_v2", "Standard_DS4_v2", "Standard_DS5_v2"],
    scoring_path="/score",
    scoring_port=5001,
)
registry_client.deployment_templates.create_or_update(dt)
```

---

**Example (TF Serving):** TF Serving needs `MODEL_BASE_PATH` and `MODEL_NAME` environment variables, listens on port 8501, and serves a REST predict endpoint at `/v1/models/<model-name>:predict`. The following deployment template captures all of those settings so that consumers don't need to know them.

# [REST](#tab/rest)

```json
{
  "name": "tfs-deployment-template",
  "version": "1",
  "type": "deploymenttemplates",
  "description": "TF Serving deployment template",
  "deploymentTemplateType": "Managed",
  "environmentId": "azureml://registries/<your-registry>/environments/tfs-env/versions/1",
  "environmentVariables": {
    "MODEL_BASE_PATH": "/var/azureml-app",
    "MODEL_NAME": "half_plus_two"
  },
  "modelMountPath": "/var/azureml-app",
  "instanceCount": 1,
  "defaultInstanceType": "Standard_F2s_v2",
  "allowedInstanceType": [
    "Standard_F2s_v2",
    "Standard_F4s_v2"
  ],
  "scoringPath": "/v1/models/half_plus_two:predict",
  "scoringPort": 8501,
  "requestSettings": {
    "requestTimeout": "PT50S",
    "maxConcurrentRequestsPerInstance": 2
  },
  "livenessProbe": {
    "initialDelay": "PT5M",
    "period": "PT10S",
    "timeout": "PT2S",
    "failureThreshold": 30,
    "successThreshold": 1,
    "scheme": "http",
    "httpMethod": "GET",
    "path": "/v1/models/half_plus_two",
    "port": 8501
  },
  "readinessProbe": {
    "initialDelay": "PT5M",
    "period": "PT10S",
    "timeout": "PT2S",
    "failureThreshold": 30,
    "successThreshold": 1,
    "scheme": "http",
    "httpMethod": "GET",
    "path": "/v1/models/half_plus_two",
    "port": 8501
  }
}
```

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

curl -X POST \
  "https://<your-region>.api.azureml.ms/genericasset/v2.0/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/tfs-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/deploymentTemplate.schema.json
name: tfs-deployment-template
version: 1
description: TF Serving deployment template
deployment_template_type: Managed
environment: azureml://registries/<your-registry>/environments/tfs-env/versions/1
instance_count: 1
default_instance_type: Standard_F2s_v2
allowed_instance_types:
  - Standard_F2s_v2
  - Standard_F4s_v2
environment_variables:
  MODEL_BASE_PATH: /var/azureml-app
  MODEL_NAME: half_plus_two
model_mount_path: /var/azureml-app
scoring_path: /v1/models/half_plus_two:predict
scoring_port: 8501
request_settings:
  request_timeout_ms: 50000
  max_concurrent_requests_per_instance: 2
liveness_probe:
  initial_delay: 300
  period: 10
  timeout: 2
  failure_threshold: 30
  success_threshold: 1
  scheme: HTTP
  method: GET
  path: /v1/models/half_plus_two
  port: 8501
readiness_probe:
  initial_delay: 300
  period: 10
  timeout: 2
  failure_threshold: 30
  success_threshold: 1
  scheme: HTTP
  method: GET
  path: /v1/models/half_plus_two
  port: 8501
```

```azurecli
az ml deployment-template create -f deployment-template.yml \
  --registry-name <your-registry>
```

# [Python SDK](#tab/python)

```python
dt = DeploymentTemplate(
    name="tfs-deployment-template",
    version="1",
    deployment_template_type="Managed",
    environment="azureml://registries/<your-registry>/environments/tfs-env/versions/1",
    instance_count=1,
    default_instance_type="Standard_F2s_v2",
    allowed_instance_types=["Standard_F2s_v2", "Standard_F4s_v2"],
    environment_variables={"MODEL_BASE_PATH": "/var/azureml-app", "MODEL_NAME": "half_plus_two"},
    model_mount_path="/var/azureml-app",
    scoring_path="/v1/models/half_plus_two:predict",
    scoring_port=8501,
)
registry_client.deployment_templates.create_or_update(dt)
```

---

## Step 4: Manage deployment template versions

Use the following commands to inspect, update, archive, or restore deployment template versions in the registry.

# [REST](#tab/rest)

Use the same `genericasset` data plane path as in Step 3. Get a token for `https://management.azure.com` first. All requests take the `api-version=2024-04-01-preview` query parameter.

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

BASE="https://<your-region>.api.azureml.ms/genericasset/v2.0/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>"
```

Show a specific version. Read requests include the `deploymenttemplates` asset-type segment in the path:

```bash
curl -X GET "$BASE/deploymenttemplates/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN"
```

List all deployment templates in the registry:

```bash
curl -X GET "$BASE/deploymenttemplates?api-version=2024-04-01-preview&listViewType=ActiveOnly" \
  -H "Authorization: Bearer $TOKEN"
```

Create a new version (point `-d @` to a `deployment-template.json` that has `"version": "2"`). The asset type comes from the `"type": "deploymenttemplates"` field in the body, so the create `POST` path omits the asset-type segment:

```bash
curl -X POST "$BASE/my-deployment-template/versions/2?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

The `genericasset` data plane exposes only `GET` (show and list) and `POST` (create or update). Update, archive, and restore are therefore client-side read-modify-write operations: `GET` the version, change the relevant field in the returned object, then `POST` the whole object back to the same `versions` URL.

Update mutable fields on a version. `GET` the version, edit the field (for example, `description`) in the saved object, then `POST` it back:

```bash
curl -X GET "$BASE/deploymenttemplates/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" -o deployment-template.json

# Edit deployment-template.json, then POST the full object back.
curl -X POST "$BASE/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

Archive a version by setting `"isArchived": true` in the object and `POST`ing it back:

```bash
curl -X POST "$BASE/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

Restore an archived version by setting `"isArchived": false` in the object and `POST`ing it back:

```bash
curl -X POST "$BASE/my-deployment-template/versions/1?api-version=2024-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-template.json
```

# [Azure CLI](#tab/cli)

```azurecli
# Show a specific version
az ml deployment-template show \
  --name my-deployment-template --version 1 \
  --registry-name <your-registry>

# List all deployment templates in the registry
az ml deployment-template list --registry-name <your-registry>

# Create a new version (point -f to a deployment-template.yml that has version: 2)
az ml deployment-template create -f deployment-template.yml \
  --registry-name <your-registry>

# Update mutable fields on a version
az ml deployment-template update \
  --name my-deployment-template --version 1 \
  --registry-name <your-registry> \
  --set description="Updated description"

# Archive a version
az ml deployment-template archive \
  --name my-deployment-template --version 1 \
  --registry-name <your-registry>

# Restore an archived version
az ml deployment-template restore \
  --name my-deployment-template --version 1 \
  --registry-name <your-registry>
```

# [Python SDK](#tab/python)

```python
# Show a specific version
registry_client.deployment_templates.get(name="my-deployment-template", version="1")

# List all deployment templates in the registry
registry_client.deployment_templates.list()

# Create a new version (build a DeploymentTemplate with version="2" and call create_or_update)
dt_v2 = DeploymentTemplate(
    name="my-deployment-template",
    version="2",
    deployment_template_type="Managed",
    environment="azureml://registries/<your-registry>/environments/my-inference-env/versions/1",
    instance_count=1,
    default_instance_type="Standard_DS3_v2",
    allowed_instance_types=["Standard_DS3_v2", "Standard_DS4_v2", "Standard_DS5_v2"],
    scoring_path="/score",
    scoring_port=5001,
)
registry_client.deployment_templates.create_or_update(dt_v2)

# Archive and restore
registry_client.deployment_templates.archive(name="my-deployment-template", version="1")
registry_client.deployment_templates.restore(name="my-deployment-template", version="1")
```

---

## Step 5: Create a model that pins deployment templates

Author the model payload and publish it to the registry. The `default_deployment_template` value is applied when consumers deploy the model without an override. The `allowed_deployment_templates` list is author guidance that recommends which deployment templates a consumer should use as an override — a curated set of validated templates. It isn't enforced: the platform doesn't block an override that isn't in the list.

# [REST](#tab/rest)

Model creation runs against the same registry data plane host as Step 2. Reuse the `$RP_HOST` and `$TOKEN` from the [discovery call in Step 2](#step-2-share-the-environment-to-a-registry), and make sure your model artifacts are already uploaded to accessible blob storage; set `modelUri` to that location. (The Azure CLI and Python SDK upload the artifacts for you; with raw REST you provide an existing `modelUri`.) To get a writable blob location for the upload, call the [Registry Model Versions - Create Or Get Start Pending Upload](/rest/api/azureml/registry-model-versions/create-or-get-start-pending-upload) operation, upload your model files to the returned location, then set `modelUri` to it.

Save the following JSON as `model.json` to use as the request body. The `allowedDeploymentTemplates` list is author guidance — a curated set of validated override templates — and isn't enforced by the platform:

```json
{
  "properties": {
    "modelType": "custom_model",
    "modelUri": "<blob-uri-for-model-artifacts>",
    "defaultDeploymentTemplate": {
      "assetId": "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template/versions/1"
    },
    "allowedDeploymentTemplates": [
      { "assetId": "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template/labels/latest" },
      { "assetId": "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template2/labels/latest" }
    ]
  }
}
```

Create the model by issuing a `PUT` against the registry's model version path. The model name and version go in the URL. The response is `202 Accepted` with an `Azure-AsyncOperation` header that you poll until creation completes:

```bash
curl -X PUT \
  "${RP_HOST%/}/mferp/managementfrontend/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/models/my-model/versions/1?api-version=2021-10-01-dataplanepreview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @model.json
```

# [Azure CLI](#tab/cli)

Save the following YAML as `model.yml`:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/model.schema.json
name: my-model
version: 1
type: custom_model
description: Model with a default deployment template
path: ./model
default_deployment_template:
  asset_id: azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template/versions/1
```

Create the model in the registry:

```azurecli
az ml model create -f model.yml --registry-name <your-registry>
```

For the full model schema, see [CLI (v2) model YAML schema](reference-yaml-model.md).

> [!NOTE]
> Setting `allowed_deployment_templates` (the override allow-list) isn't supported in the Azure CLI yet. To define the allow-list, use the **REST** tab. This example sets only `default_deployment_template`.

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Model

model = Model(
    name="my-model",
    version="1",
    type="custom_model",
    path="./model",
    default_deployment_template={
        "asset_id": "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template/versions/1",
    },
)
registry_client.models.create_or_update(model)
```

> [!NOTE]
> Setting `allowed_deployment_templates` (the override allow-list) isn't supported in the Python SDK yet. To define the allow-list, use the **REST** tab. This example sets only `default_deployment_template`.

---

**Example (TF Serving):** Pin the TF Serving deployment template that you created earlier as the model's default. The `path` points to a TF Serving SavedModel directory (such as `half_plus_two/00000123/`).

# [REST](#tab/rest)

```json
{
  "properties": {
    "modelType": "custom_model",
    "modelUri": "<blob-uri-for-tfs-model-artifacts>",
    "defaultDeploymentTemplate": {
      "assetId": "azureml://registries/<your-registry>/deploymenttemplates/tfs-deployment-template/versions/1"
    }
  }
}
```

```bash
curl -X PUT \
  "${RP_HOST%/}/mferp/managementfrontend/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/models/tfs-model/versions/1?api-version=2021-10-01-dataplanepreview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @model.json
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/model.schema.json
name: tfs-model
version: 1
type: custom_model
description: TF Serving model with default deployment template
path: ./tfs-model
default_deployment_template:
  asset_id: azureml://registries/<your-registry>/deploymenttemplates/tfs-deployment-template/versions/1
```

```azurecli
az ml model create -f model.yml --registry-name <your-registry>
```

# [Python SDK](#tab/python)

```python
tfs_model = Model(
    name="tfs-model",
    version="1",
    type="custom_model",
    path="./tfs-model",
    default_deployment_template={
        "asset_id": "azureml://registries/<your-registry>/deploymenttemplates/tfs-deployment-template/versions/1",
    },
)
registry_client.models.create_or_update(tfs_model)
```

---

> [!NOTE]
> `default_deployment_template.asset_id` must use the **versioned** asset ID format (`.../deploymenttemplates/<name>/versions/<n>`), so that the default is pinned to a specific version. `allowed_deployment_templates[].asset_id` uses the **labels/latest** format (`.../deploymenttemplates/<name>/labels/latest`), which points to any current version of the named deployment template.

## Related content

- [What are deployment templates?](concept-deployment-template.md)
- [Deploy models that use deployment templates](how-to-deploy-models-deployment-template.md)
- [CLI (v2) deployment template YAML schema](reference-yaml-deployment-template.md)
- [CLI (v2) model YAML schema](reference-yaml-model.md)
- [CLI (v2) managed online deployment YAML schema](reference-yaml-deployment-managed-online.md)
