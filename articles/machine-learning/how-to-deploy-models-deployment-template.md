---
title: Deploy models that use deployment templates
titleSuffix: Azure Machine Learning
description: Learn how to deploy a model from an Azure Machine Learning registry to a managed online endpoint using the model's default deployment template, or by overriding the default with another allowed deployment template.
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

#CustomerIntent: As a model consumer, I want to deploy a registered model to a managed online endpoint using its default deployment template (or a different allowed deployment template) so I don't have to specify environment or infrastructure settings myself.
---

# Deploy models that use deployment templates

This article shows you how to deploy a registry model that pins a [deployment template](concept-deployment-template.md) to a managed online endpoint. When the model has a `default_deployment_template`, your deployment YAML only needs to reference the model — the deployment template supplies the environment, environment variables, scoring port, and probes. You can also override the default with another deployment template. The model's `allowed_deployment_templates` list is the author's curated set of validated overrides to choose from — it's guidance, not an enforced restriction.

[!INCLUDE [machine-learning-preview-old-json-schema-note](includes/machine-learning-preview-old-json-schema-note.md)]

## Prerequisites

- An Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/free/).
- An Azure Machine Learning workspace. For more information, see [Manage Azure Machine Learning workspaces](how-to-manage-workspace.md).
- Read access to an Azure Machine Learning registry that contains a model with a `default_deployment_template` set. For information about publishing such a model, see [Manage models with deployment templates](how-to-manage-models-deployment-templates.md).
- The Azure CLI and the `ml` extension installed and signed in. For more information, see [Install and use the CLI (v2)](how-to-configure-cli.md).
- Permissions to create endpoints and deployments in the workspace. The `AzureML Data Scientist` role is sufficient for this article.

## Step 1: Find a model that uses a deployment template

Inspect the model in the registry to confirm that it has a `default_deployment_template`, and to see which other deployment templates are in `allowed_deployment_templates`.

# [REST](#tab/rest)

A model's `defaultDeploymentTemplate` and `allowedDeploymentTemplates` are returned by the registry **data plane**, which you reach through the registry's resource provider host. The Azure Resource Manager (`management.azure.com`) model GET doesn't include these fields. First look up the data plane host with a one-time *discovery* call, then get the model version from it.

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

RP_HOST=$(curl -s \
  "https://<your-region>.api.azureml.ms/registrymanagement/v1.0/registries/<your-registry>/discovery?api-version=v1.0" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.primaryRegionResourceProviderUri')

curl -X GET \
  "${RP_HOST%/}/mferp/managementfrontend/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/registries/<your-registry>/models/my-model/versions/1?api-version=2021-10-01-dataplanepreview" \
  -H "Authorization: Bearer $TOKEN"
```

Look for `properties.defaultDeploymentTemplate.assetId` and `properties.allowedDeploymentTemplates[].assetId` in the response.

# [Azure CLI](#tab/cli)

```azurecli
az ml model show \
  --name my-model --version 1 \
  --registry-name <your-registry>
```

Look for `default_deployment_template.asset_id` in the output. The `az ml model show` output doesn't surface `allowed_deployment_templates` yet — use the **REST** tab to see the full allow-list.

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

registry_client = MLClient(
    credential=DefaultAzureCredential(),
    registry_name="<your-registry>",
)

model = registry_client.models.get(name="my-model", version="1")
print(model.default_deployment_template)
# The SDK Model object doesn't expose allowed_deployment_templates yet; use the REST tab to see the full allow-list.
```

---

## Step 2: Create an online endpoint

# [REST](#tab/rest)

Use the [Online Endpoints - Create Or Update](/rest/api/azureml/online-endpoints/create-or-update) operation:

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

curl -X PUT \
  "https://management.azure.com/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>/onlineEndpoints/my-endpoint?api-version=2023-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "<your-region>",
    "identity": { "type": "SystemAssigned" },
    "properties": {
      "authMode": "Key"
    }
  }'
```

# [Azure CLI](#tab/cli)

```azurecli
az ml online-endpoint create --name my-endpoint \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>
```

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.identity import DefaultAzureCredential

ws_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<your-subscription-id>",
    resource_group_name="<your-resource-group>",
    workspace_name="<your-workspace>",
)

ws_client.online_endpoints.begin_create_or_update(
    ManagedOnlineEndpoint(name="my-endpoint")
).result()
```

---

## Step 3: Deploy with the model's default deployment template

When the model has a `default_deployment_template`, the deployment template supplies infrastructure settings such as `environment`, request settings, and probes. The deployment payload still must include the SKU/instance settings required by the underlying ARM resource.

# [REST](#tab/rest)

Use the [Online Deployments - Create Or Update](/rest/api/azureml/online-deployments/create-or-update) operation. Save the following JSON as `deployment-default.json`. The top-level `sku` block (`name` and `capacity`) is required for the ARM resource, and `properties.endpointComputeType` must be `Managed`. The `properties.model` reference points to the registry model whose default deployment template supplies the environment, request settings, and probes.

```json
{
  "name": "blue",
  "endpointName": "my-endpoint",
  "tags": {},
  "location": "<your-region>",
  "properties": {
    "environmentVariables": {},
    "properties": {},
    "appInsightsEnabled": false,
    "endpointComputeType": "Managed",
    "instanceType": "Standard_DS3_v2",
    "model": "azureml://registries/<your-registry>/models/my-model/versions/1"
  },
  "sku": {
    "name": "Default",
    "capacity": 1
  }
}
```

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

curl -X PUT \
  "https://management.azure.com/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>/onlineEndpoints/my-endpoint/deployments/blue?api-version=2023-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-default.json
```

# [Azure CLI](#tab/cli)

Save the following YAML as `deployment-default.yml`:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
name: blue
endpoint_name: my-endpoint
model: azureml://registries/<your-registry>/models/my-model/versions/1
instance_type: Standard_DS3_v2
instance_count: 1
```

```azurecli
az ml online-deployment create -f deployment-default.yml --all-traffic \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>
```

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import ManagedOnlineDeployment

deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="my-endpoint",
    model="azureml://registries/<your-registry>/models/my-model/versions/1",
    instance_type="Standard_DS3_v2",
    instance_count=1,
)
ws_client.online_deployments.begin_create_or_update(deployment).result()
```

---

## Step 4: (Optional) Deploy with an override deployment template

To use a different deployment template than the model's default, specify the override on the deployment. The model's `allowed_deployment_templates` list is the author's curated set of validated override templates to choose from; it's guidance, not an enforced restriction, so the platform doesn't block an override that isn't in the list. The override deployment can be a separate deployment under the same endpoint, so the deployment from Step 3 keeps serving traffic until you update the endpoint's traffic allocation.

# [REST](#tab/rest)

In the REST API, set the override inside the nested `properties.properties` bag using the `azureml.deploymentTemplateOverride` key. Save the following JSON as `deployment-override.json`:

```json
{
  "name": "green",
  "endpointName": "my-endpoint",
  "tags": {},
  "location": "<your-region>",
  "properties": {
    "environmentVariables": {},
    "properties": {
      "azureml.deploymentTemplateOverride": "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template2/versions/1"
    },
    "appInsightsEnabled": false,
    "endpointComputeType": "Managed",
    "instanceType": "Standard_DS3_v2",
    "model": "azureml://registries/<your-registry>/models/my-model/versions/1"
  },
  "sku": {
    "name": "Default",
    "capacity": 1
  }
}
```

```bash
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

curl -X PUT \
  "https://management.azure.com/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>/onlineEndpoints/my-endpoint/deployments/green?api-version=2023-04-01-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @deployment-override.json
```

# [Azure CLI](#tab/cli)

In the YAML, set `properties."azureml.deploymentTemplateOverride"` to the registry asset URI of the override. Save the following YAML as `deployment-override.yml`:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
name: green
endpoint_name: my-endpoint
model: azureml://registries/<your-registry>/models/my-model/versions/1
instance_type: Standard_DS3_v2
instance_count: 1
properties:
  azureml.deploymentTemplateOverride: azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template2/versions/1
```

```azurecli
az ml online-deployment create -f deployment-override.yml \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>
```

# [Python SDK](#tab/python)

```python
deployment = ManagedOnlineDeployment(
    name="green",
    endpoint_name="my-endpoint",
    model="azureml://registries/<your-registry>/models/my-model/versions/1",
    instance_type="Standard_DS3_v2",
    instance_count=1,
    properties={
        "azureml.deploymentTemplateOverride": (
            "azureml://registries/<your-registry>/deploymenttemplates/my-deployment-template2/versions/1"
        ),
    },
)
ws_client.online_deployments.begin_create_or_update(deployment).result()
```

---

## Step 5: Invoke the endpoint

Send a scoring request to the deployment. The examples target the `blue` deployment from Step 3. To invoke the override deployment from Step 4 instead, replace `blue` with `green`.

For the TF Serving deployment template from [Manage models with deployment templates](how-to-manage-models-deployment-templates.md), the request payload is the standard TF Serving REST format. Save the following as `request.json`:

```json
{ "instances": [1.0, 2.0, 5.0] }
```

# [REST](#tab/rest)

Get the scoring URI and key, then `POST` the request payload to the scoring URI. For the TF Serving deployment template, the scoring path is `/v1/models/half_plus_two:predict`. For details, see [Invoke the endpoint to score data by using your model](how-to-deploy-online-endpoints.md#invoke-the-endpoint-to-score-data-by-using-your-model).

```bash
SCORING_URI=$(az ml online-endpoint show --name my-endpoint --query scoring_uri -o tsv \
  --workspace-name <your-workspace> --resource-group <your-resource-group>)
KEY=$(az ml online-endpoint get-credentials --name my-endpoint --query primaryKey -o tsv \
  --workspace-name <your-workspace> --resource-group <your-resource-group>)

curl -X POST "$SCORING_URI" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d @request.json
```

# [Azure CLI](#tab/cli)

```azurecli
az ml online-endpoint invoke --name my-endpoint \
  --deployment-name blue \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group> \
  --request-file request.json
```

# [Python SDK](#tab/python)

```python
result = ws_client.online_endpoints.invoke(
    endpoint_name="my-endpoint",
    deployment_name="blue",
    request_file="request.json",
)
print(result)
```

---

The response is the TF Serving predict response, for example: `{ "predictions": [2.5, 3.0, 4.5] }`.

## Step 6: Update or delete the deployment

To change traffic allocation, scale the deployment, or delete it, use the standard managed online endpoint commands. The deployment template doesn't change these operations. To shift live traffic to the override deployment from Step 4, replace `blue=100` with `green=100` in the traffic update.

```azurecli
az ml online-endpoint update --name my-endpoint \
  --traffic "blue=100" \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>

az ml online-deployment delete --name blue --endpoint-name my-endpoint \
  --workspace-name <your-workspace> \
  --resource-group <your-resource-group>
```

## Troubleshooting

- **The instance type isn't allowed for this deployment template.** The `instance_type` you set on the deployment isn't in the deployment template's `allowed_instance_types` list. Use `az ml deployment-template show` to list the allowed instance types, or omit `instance_type` to use the deployment template's `default_instance_type`.
- **The environment isn't a registry-scoped reference.** Deployment templates must reference an environment with the `azureml://registries/<registry-name>/environments/<name>/versions/<version>` syntax. Share workspace environments to a registry before you reference them.

## Related content

- [What are deployment templates?](concept-deployment-template.md)
- [Manage models with deployment templates](how-to-manage-models-deployment-templates.md)
- [CLI (v2) managed online deployment YAML schema](reference-yaml-deployment-managed-online.md)
- [CLI (v2) deployment template YAML schema](reference-yaml-deployment-template.md)
- [CLI (v2) model YAML schema](reference-yaml-model.md)
