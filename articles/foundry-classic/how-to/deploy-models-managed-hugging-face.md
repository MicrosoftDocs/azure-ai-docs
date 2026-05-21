---
title: "Deploy Hugging Face Hub models in Microsoft Foundry (classic)"
description: "Deploy Hugging Face Hub models to managed compute endpoints in Microsoft Foundry for secure, scalable real-time inference. Follow this step-by-step guide to get started."
#customer intent: As a data scientist, I want to deploy an open-source Hugging Face model to a managed compute endpoint so that I can serve real-time predictions on Azure.
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/14/2026
ms.author: mopeakande
ms.reviewer: osiotugo
author: msakande
reviewer: ositanachi
ai-usage: ai-assisted
ms.custom: doc-kit-assisted, references_regions
---

# Deploy models from Hugging Face Hub to managed compute (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Microsoft has partnered with Hugging Face to bring open-source models from Hugging Face Hub to the Foundry model catalog. Hugging Face is the creator of Transformers, a widely popular library for building large language models. The Hugging Face Hub has thousands of open-source models. The integration with Microsoft Foundry enables you to deploy open-source models of your choice to secure and scalable inference infrastructure on Azure.

You can search from thousands of Transformers models in the model catalog and deploy models to managed compute endpoints (also called managed online endpoints). Once deployed, the managed online endpoint provides a secure REST API to score your model in real time.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- A [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. For more information, see [Create a project](hub-create-projects.md).
- Azure role-based access controls (Azure RBAC). Your user account must be assigned the **Azure AI Developer** role on the resource group. For more information, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).
- Virtual machine (VM) quota in your Azure subscription for the specific VM SKUs needed to run your model. Each deployment consumes VM core quota on a per-region basis.
- **Python SDK only**: Python 3.8 or later and the following packages:

  ```bash
  pip install "azure-ai-ml>=1.12.0" azure-identity
  ```

- **Azure CLI only**: The Azure Machine Learning CLI v2 extension:

  ```bash
  az extension add -n ml
  ```

## Use Hugging Face models responsibly

Models sourced from Hugging Face are Non-Microsoft Products that haven't been tested or evaluated by Microsoft. Before you deploy a model, ensure it's appropriate for your specific use case, including by evaluating any legal or export-control considerations and conducting your own model risk and safety evaluations. Learn about [Foundry risk and safety evaluations](../concepts/safety-evaluations-transparency-note.md#the-basics-of-microsoft-foundry-risk-and-safety-evaluations-preview) and [Hugging Face security measures for models offered in Foundry](https://huggingface.co/docs/microsoft-azure/security).

> [!IMPORTANT]
> Models from Hugging Face are subject to third-party license terms available on the Hugging Face model details page. It's your responsibility to comply with the model's license terms.

## Benefits of using online endpoints for real-time inference

Managed online endpoints in Foundry help you deploy models to powerful CPU and GPU machines in Azure in a turnkey manner. Managed online endpoints take care of serving, scaling, securing, and monitoring your models, freeing you from the overhead of setting up and managing the underlying infrastructure. The virtual machines are provisioned on your behalf when you deploy models.

Key capabilities include:

- **Traffic management** - Split or mirror traffic across multiple deployments. Mirror traffic helps you test new model versions on production traffic without releasing to production. Splitting traffic lets you gradually increase production traffic to new model versions while observing performance.
- **Autoscaling** - Dynamically ramp up or ramp down resources based on utilization metrics, a specific schedule, or a combination of both. For example, add nodes if CPU utilization goes higher than 70%, or add nodes based on peak business hours. To configure autoscaling rules, see [Autoscale an online endpoint](../../machine-learning/how-to-autoscale-endpoints.md).

Select the tab that matches your preferred deployment method. Use the **Azure portal** for a guided, no-code experience. Use the **Python SDK** for programmatic control and pipeline integration. Use the **Azure CLI** for scripted or CI/CD deployments.

## Deploy a Hugging Face model

# [Portal](#tab/portal)

### Find the model

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. Select **Hugging Face** in the **Collections** filter to see available Hugging Face models.

1. Select a model tile to open the model card. If the selected model is a *gated model*, the model card includes the note: **Gated Model Access Required**. To request access to deploy a gated model, see [Gated models](#gated-models).

### Deploy the model

1. On the model's page, select **Use this model**. This action opens the deployment window that is pre-filled with some selections and parameter values.

1. Select the **Template** for GPU or CPU. CPU instance types are good for testing. GPU instance types offer better performance in production. Large models might not fit in a CPU instance type.

1. Select the **Virtual machine** instance type. The list of instances is pre-filtered to the ones where the model is expected to deploy without running out of memory.

1. Specify the **Instance count**. One instance is sufficient for testing, but consider two or more instances for production.

1. Optionally, specify an **Endpoint name** and a **Deployment name** that are different from the default ones suggested.

1. Select **Deploy** to create your deployment. The creation process might take a few minutes to complete. When it's complete, the portal opens the model deployment page.

#### Gated models

Gated models require approval from the model's author before use. When you open the model card of a gated model, you see the note: **Gated Model Access Required**.

To deploy a gated model:

1. Have a Hugging Face `read` or `fine-grained` [token](https://huggingface.co/docs/hub/security-tokens).

1. Request access through the model's page on Hugging Face.

1. Create a custom key connection named `HuggingFaceTokenConnection` with the key `HF_TOKEN` and your Hugging Face token as the secret value.

1. Create an endpoint with `enforce_access_to_default_secret_stores` set to `enabled`.

1. Use the newly created endpoint in the steps to [deploy the model](#deploy-the-model).


# [Python SDK](#tab/python-sdk)

[Set up the Python SDK](/python/api/overview/azure/ai-ml-readme).

### Find the model

Browse the model catalog in Foundry portal and find the model you want to deploy. Copy the model name. The models shown in the catalog are listed from the `HuggingFace` registry. Create the `model_id` by using the model name you copied and the `HuggingFace` registry. This example deploys the `bert-base-uncased` model.

> [!TIP]
> To list available versions for a model, run: `[v.version for v in ml_client.models.list(name=model_name, registry_name=registry_name)]`

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
)
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<your-subscription-id>",
    resource_group_name="<your-resource-group>",
    workspace_name="<your-workspace-name>"
)

registry_name = "HuggingFace"
model_name = "bert-base-uncased"
model_version = "25"
model_id = f"azureml://registries/{registry_name}/models/{model_name}/versions/{model_version}"
```

### Deploy the model

Create an online endpoint. Next, create the deployment. Lastly, set all the traffic to use this deployment. You can find the optimal CPU or GPU `instance_type` for a model by opening the quick deployment dialog from the model page in the model catalog. Make sure you use an `instance_type` for which you have quota.

```python
import time

endpoint_name = "hf-ep-" + str(int(time.time()))
ml_client.begin_create_or_update(
    ManagedOnlineEndpoint(name=endpoint_name)
).wait()

ml_client.online_deployments.begin_create_or_update(
    ManagedOnlineDeployment(
        name="demo",
        endpoint_name=endpoint_name,
        model=model_id,
        instance_type="Standard_DS3_v2",
        instance_count=1,
    )
).wait()

endpoint = ml_client.online_endpoints.get(endpoint_name)
endpoint.traffic = {"demo": 100}
ml_client.begin_create_or_update(endpoint).result()

# Verify deployment status
deployment = ml_client.online_deployments.get(
    endpoint_name=endpoint_name, name="demo"
)
print(f"Provisioning state: {deployment.provisioning_state}")
```

#### Gated models

To deploy a gated model with the Python SDK:

1. Have a Hugging Face `read` or `fine-grained` [token](https://huggingface.co/docs/hub/security-tokens).

1. Request access through the model's page on Hugging Face.

1. Create a custom key connection named `HuggingFaceTokenConnection` with the key `HF_TOKEN` and your Hugging Face token as the secret value. You can create this connection in Foundry portal under **Settings** > **Connections**.

1. Create the endpoint with `enforce_access_to_default_secret_stores` enabled:

   ```python
   endpoint = ManagedOnlineEndpoint(
       name=endpoint_name,
       properties={"enforce_access_to_default_secret_stores": "enabled"},
   )
   ml_client.begin_create_or_update(endpoint).wait()
   ```

1. Use the newly created endpoint in the steps to [deploy the model](#deploy-the-model-1).

# [Azure CLI](#tab/azure-cli)

[Set up the CLI](../../machine-learning/how-to-configure-cli.md).

### Find the model

Browse the model catalog in Foundry portal and find the model you want to deploy. Copy the model name. The models shown in the catalog are listed from the `HuggingFace` registry. This example deploys the `bert-base-uncased` model.

> [!TIP]
> To list available versions for a model, run: `az ml model list --name bert-base-uncased --registry-name HuggingFace`

### Deploy the model

You need the `model` and `instance_type` to deploy the model. You can find the optimal CPU or GPU `instance_type` for a model by opening the quick deployment dialog from the model page in the model catalog. Make sure you use an `instance_type` for which you have quota.

Create an online endpoint. Next, create the deployment.

```shell
# set your workspace and resource group
workspace_name="<your-workspace-name>"
resource_group_name="<your-resource-group-name>"

# create endpoint
endpoint_name="hf-ep-"$(date +%s)
model_name="bert-base-uncased"
model_version="25"
az ml online-endpoint create --name $endpoint_name \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name

# create deployment file
cat <<EOF > ./deploy.yml
name: demo
model: azureml://registries/HuggingFace/models/$model_name/versions/$model_version
endpoint_name: $endpoint_name
instance_type: Standard_DS3_v2
instance_count: 1
EOF
az ml online-deployment create --file ./deploy.yml \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name

# set all traffic to the deployment
az ml online-endpoint update --name $endpoint_name \
    --traffic "demo=100" \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name

# verify deployment status
az ml online-deployment show --name demo \
    --endpoint-name $endpoint_name \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name \
    --query "provisioningState" -o tsv
```

#### Gated models

To deploy a gated model with the Azure CLI:

1. Have a Hugging Face `read` or `fine-grained` [token](https://huggingface.co/docs/hub/security-tokens).

1. Request access through the model's page on Hugging Face.

1. Create a custom key connection named `HuggingFaceTokenConnection` with the key `HF_TOKEN` and your Hugging Face token as the secret value:

   ```bash
   cat <<EOF > ./hf-connection.yml
   name: HuggingFaceTokenConnection
   type: custom
   credentials:
     type: custom_keys
     keys:
       HF_TOKEN: "<your-hugging-face-token>"
   EOF
   az ml connection create --file ./hf-connection.yml \
       --workspace-name $workspace_name \
       --resource-group $resource_group_name
   ```

1. Create an endpoint with `enforce_access_to_default_secret_stores` set to `enabled`:

   ```bash
   az ml online-endpoint create --name $endpoint_name \
       --set properties.enforce_access_to_default_secret_stores=enabled \
       --workspace-name $workspace_name \
       --resource-group $resource_group_name
   ```

1. Use the newly created endpoint in the steps to [deploy the model](#deploy-the-model-2).

---

## Test the model

# [Portal](#tab/portal)

Once the deployment is complete, find the REST endpoint on the endpoints page to score the model. The endpoints page provides options to add more deployments, manage traffic, and configure scaling. Use the **Test** tab on the endpoint page to test the model with sample inputs.

You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

# [Python SDK](#tab/python-sdk)

Create a file with inputs to submit to the online endpoint for scoring. This code sample submits a `fill-mask` input, matching the `bert-base-uncased` model you deployed. You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

```python
import json

scoring_file = "./sample_score.json"
with open(scoring_file, "w") as outfile:
    outfile.write(
        '{"inputs": ["Paris is the [MASK] of France.",'
        ' "The goal of life is [MASK]."]}'
    )

response = ml_client.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    deployment_name="demo",
    request_file=scoring_file,
)
response_json = json.loads(response)
print(json.dumps(response_json, indent=2))
```

# [Azure CLI](#tab/azure-cli)

Create a file with inputs to submit to the online endpoint for scoring. This code sample provides input for the `fill-mask` type for the deployed `bert-base-uncased` model. You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

```shell
scoring_file="./sample_score.json"
cat <<EOF > $scoring_file
{
  "inputs": [
    "Paris is the [MASK] of France.",
    "The goal of life is [MASK]."
  ]
}
EOF
az ml online-endpoint invoke --name $endpoint_name --request-file $scoring_file
```

---

## Clean up resources

When you no longer need the deployment, delete the online endpoint to avoid ongoing charges. Deleting the endpoint also deletes all deployments under it.

# [Portal](#tab/portal)

1. In Foundry portal, go to **My assets** > **Models + endpoints**.
1. Select the endpoint you created.
1. Select **Delete** and confirm.

# [Python SDK](#tab/python-sdk)

```python
ml_client.online_endpoints.begin_delete(name=endpoint_name).wait()
```

# [Azure CLI](#tab/azure-cli)

```bash
az ml online-endpoint delete --name $endpoint_name \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name \
    --yes
```

---


## Regional availability

The Hugging Face Collection is currently available in all regions of the public cloud only.


## Troubleshooting

The following sections describe common errors you might encounter when deploying or scoring Hugging Face models, and how to resolve them.

### Gated models

[Gated models](https://huggingface.co/docs/hub/models-gated) require you to accept the model author's terms before access is granted. Deploying without proper setup results in a deployment failure or an unauthorized response status code. For the required steps, see [Gated models](#gated-models).

### Models that need to run remote code

Some models run code from the model repo rather than using the standard Transformers SDK. Such models require the `trust_remote_code` parameter set to `True`. For more information, see [remote code](https://huggingface.co/docs/transformers/custom_models#using-a-model-with-custom-code). These models aren't supported for security reasons.

Deploying such models fails with the following error:

`ValueError: Loading <model> requires you to execute the configuration file in that repo on your local machine. Make sure you have read the code there to avoid malicious use, then set the option trust_remote_code=True to remove this error.`

### Models with incorrect tokenizers

Incorrectly specified or missing tokenizer in the model package results in `OSError: Can't load tokenizer for <model>`.

### Missing libraries

Some models need extra Python libraries. Models that require special libraries beyond the standard Transformers libraries fail with `ModuleNotFoundError` or `ImportError`.

### Insufficient memory

If you see `OutOfQuota: Container terminated due to insufficient memory`, try using an `instance_type` with more memory.

### Authentication errors

If you see `CredentialUnavailableError` when running the Python SDK, run `az login` to authenticate the Azure CLI. Alternatively, configure a service principal by setting the `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` environment variables.

### Quota exceeded

If a deployment fails with `QuotaExceeded` or `SubscriptionCapacityReached`, you don't have sufficient quota for the selected `instance_type` in the deployment region. To resolve this, either request a quota increase in the [Azure portal](https://portal.azure.com) under **Subscriptions** > **Usage + quotas**, or choose a different `instance_type` or region where you have available quota. For more information, see [Manage quotas across projects](quota.md).

## Frequently asked questions

The following questions address common topics about model storage, supported models, and community registry support for Hugging Face Hub deployments.

### Where are the model weights stored?

Hugging Face models are featured in the model catalog through the `HuggingFace` registry. Hugging Face creates and manages this registry and makes it available as a Community Registry. The model weights aren't hosted on Azure. The weights download directly from Hugging Face Hub to the online endpoints in your workspace when these models deploy. The `HuggingFace` registry works as a catalog to help discover and deploy Hugging Face Hub models.

### What models are supported?

Hugging Face models that meet the following criteria are supported on Azure:

- Must have the `Transformers`, `Diffusers`, or `Sentence-Transformers` tags on Hugging Face Hub.
- Has a [supported task](https://huggingface.co/docs/microsoft-azure/azure-ai/tasks) such as `chat-completion`, `image-to-text`, or `embeddings`.
- Model weights are in the Safetensors format and the model doesn't require `trust_remote_code`.
- A permissive license similar to Apache 2.0 or MIT.

### How to deploy the models for batch inference?

Deploying these models to batch endpoints for batch inference isn't currently supported.

### Can I use models from the HuggingFace registry as input to jobs so that I can fine-tune these models by using the Transformers SDK?

Since the model weights aren't stored in the `HuggingFace` registry, you can't access model weights by using these models as inputs to jobs.

### How do I get support if my deployments fail or inference doesn't work as expected?

`HuggingFace` is a community registry and isn't covered by Microsoft support. Review the deployment logs and determine if the issue is related to the Azure platform or specific to Hugging Face Transformers. Contact Microsoft support for platform issues such as not being able to create an online endpoint or authentication to the endpoint REST API not working. For Transformers-specific issues, create an issue on [GitHub](https://github.com/huggingface/transformers/issues), use the [Hugging Face forum](https://discuss.huggingface.co/), or use [Hugging Face support](https://huggingface.co/support).

### What is a community registry?

Community registries are registries created by trusted partners and available to all users.

### Where can users submit questions and concerns regarding Hugging Face?

Submit your questions in the [discussion forum](https://discuss.huggingface.co/t/about-the-azure-machine-learning-category/40677) or open a [GitHub issue](https://github.com/huggingface/Microsoft-Azure/issues).

## Related content

- [Deploy models via managed compute](deploy-models-managed.md)
- [Troubleshoot deployments and monitoring](troubleshoot-deploy-and-monitor.md)
- [Manage quotas across projects](quota.md)
- [Deployment options in Foundry portal](../concepts/deployments-overview.md)
- [Foundry model catalog overview](../concepts/foundry-models-overview.md)
- [Role-based access control in Foundry portal](../concepts/rbac-foundry.md)
- [Hugging Face model examples (token classification, translation, question answering, zero-shot classification)](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/huggingface/inference)
