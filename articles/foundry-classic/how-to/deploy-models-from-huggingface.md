---
title: Deploy models from Hugging Face Hub (classic)
description: "Learn how to deploy open-source models from the Hugging Face hub to managed online endpoints for real-time inference in Microsoft Foundry. (classic)"
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 05/12/2026
ms.author: mopeakande
ms.reviewer: osiotugo
author: msakande
reviewer: ositanachi
ai-usage: ai-assisted
---

# Deploy models from Hugging Face Hub to online endpoints (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Microsoft has partnered with Hugging Face to bring open-source models from Hugging Face Hub to the Foundry model catalog. Hugging Face is the creator of Transformers, a widely popular library for building large language models. The Hugging Face Hub has thousands of open-source models. The integration with Microsoft Foundry enables you to deploy open-source models of your choice to secure and scalable inference infrastructure on Azure.

You can search from thousands of Transformers models in the model catalog and deploy models to a managed online endpoint through a guided wizard. Once deployed, the managed online endpoint provides a secure REST API to score your model in real time.

Models sourced from Hugging Face are Non-Microsoft Products that has not been tested or evaluated by Microsoft. Customers should ensure that the model is appropriate for their specific use, including by evaluating any legal or export-control considerations and conducting their own model risk and safety evaluations. You can learn about Foundry risk and safety evaluations [here](../concepts/safety-evaluations-transparency-note.md#the-basics-of-microsoft-foundry-risk-and-safety-evaluations-preview)). You can learn about Hugging Face security measures and requirements for models offered in Foundry [here](https://huggingface.co/docs/microsoft-azure/security). 

> [!NOTE]
> Models from Hugging Face are subject to third-party license terms available on the Hugging Face model details page. It's your responsibility to comply with the model's license terms.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- A [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. For more information, see [Create a project](hub-create-projects.md).
- Azure role-based access controls (Azure RBAC). Your user account must be assigned the **Azure AI Developer** role on the resource group. For more information, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).
- Virtual machine (VM) quota in your Azure subscription for the specific VM SKUs needed to run your model. Each deployment consumes VM core quota on a per-region basis.

## Benefits of using online endpoints for real-time inference

Managed online endpoints in Foundry help you deploy models to powerful CPU and GPU machines in Azure in a turnkey manner. Managed online endpoints take care of serving, scaling, securing, and monitoring your models, freeing you from the overhead of setting up and managing the underlying infrastructure. The virtual machines are provisioned on your behalf when you deploy models.

Key capabilities include:

- **Traffic management** - Split or mirror traffic across multiple deployments. Mirror traffic helps you test new model versions on production traffic without releasing to production. Splitting traffic lets you gradually increase production traffic to new model versions while observing performance.
- **Autoscaling** - Dynamically ramp up or ramp down resources based on utilization metrics, a specific schedule, or a combination of both. For example, add nodes if CPU utilization goes higher than 70%, or add nodes based on peak business hours.

This article covers three deployment methods. Use the **portal** for guided first-time deployments, the **Python SDK** for programmatic workflows, or the **CLI** for automation and CI/CD pipelines.

## Deploy Hugging Face hub models by using the portal

To find a model to deploy, open the model catalog in Foundry portal. Select **All Filters**, then select **HuggingFace** in the **Filter by collections** section. Select a model tile to open the model page.

### Deploy the model

Choose the real-time deployment option to open the quick deploy dialog. Specify the following options:

1. Select the template for GPU or CPU. CPU instance types are good for testing. GPU instance types offer better performance in production. Large models might not fit in a CPU instance type.
1. Select the instance type. The list of instances is filtered to the ones where the model is expected to deploy without running out of memory.
1. Select the number of instances. One instance is sufficient for testing, but consider two or more instances for production.
1. Optionally, specify an endpoint and deployment name.
1. Select **Deploy**. You're then navigated to the endpoint page, which might take a few seconds. The deployment takes several minutes to complete based on the model size and instance type.

#### Gated models

Gated models require approval from the model's author before use. To deploy a gated model:

1. Have a Hugging Face read or fine-grained [token](https://huggingface.co/docs/hub/en/security-tokens).
1. Request access through the model's page on Hugging Face.
1. Create a custom key connection named `HuggingFaceTokenConnection` with the key `HF_TOKEN` and your Hugging Face token as the secret value.
1. Create an endpoint with `enforce_access_to_default_secret_stores` set to `enabled`.
1. Deploy the model by using the newly created endpoint.

### Test the model

Once the deployment completes, find the REST endpoint on the endpoints page to score the model. The endpoints page provides options to add more deployments, manage traffic, and configure scaling. Use the **Test** tab on the endpoint page to test the model with sample inputs.

You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

## Deploy Hugging Face hub models by using the Python SDK

[Set up the Python SDK](/python/api/overview/azure/ai-ml-readme).

### Find the model to deploy

Browse the model catalog in Foundry portal and find the model you want to deploy. Copy the model name. The models shown in the catalog are listed from the `HuggingFace` registry. Create the `model_id` by using the model name you copied and the `HuggingFace` registry. This example deploys the `bert_base_uncased` model.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<your-subscription-id>",
    resource_group_name="<your-resource-group>",
    workspace_name="<your-workspace-name>"
)

registry_name = "HuggingFace"
model_name = "bert_base_uncased"
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
        instance_type="Standard_DS2_v2",
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

### Test the model

Create a file with inputs to submit to the online endpoint for scoring. This code sample allows an input for the `fill-mask` type since we deployed the `bert-base-uncased` model. You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

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

## Deploy Hugging Face hub models by using the CLI

[Set up the CLI](../../machine-learning/how-to-configure-cli.md).

### Find the model to deploy

Browse the model catalog in Foundry portal and find the model you want to deploy. Copy the model name. The models shown in the catalog are listed from the `HuggingFace` registry. This example deploys the `bert_base_uncased` model.

### Deploy the model

You need the `model` and `instance_type` to deploy the model. You can find the optimal CPU or GPU `instance_type` for a model by opening the quick deployment dialog from the model page in the model catalog. Make sure you use an `instance_type` for which you have quota.

The fully qualified `model` asset ID based on the model name and registry is `azureml://registries/HuggingFace/models/bert-base-uncased/labels/latest`. Create the `deploy.yml` file used for the `az ml online-deployment create` command inline.

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

# verify deployment status
az ml online-deployment show --name demo \
    --endpoint-name $endpoint_name \
    --workspace-name $workspace_name \
    --resource-group $resource_group_name \
    --query "provisioningState" -o tsv
```

### Test the model

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

## Hugging Face model example code

For example code that covers token classification, translation, question answering, and zero-shot classification, see [Hugging Face model examples](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/huggingface/inference).

## Troubleshooting

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

## Frequently asked questions

**Where are the model weights stored?**

Hugging Face models are featured in the model catalog through the `HuggingFace` registry. Hugging Face creates and manages this registry and makes it available as a Community Registry. The model weights aren't hosted on Azure. The weights download directly from Hugging Face Hub to the online endpoints in your workspace when these models deploy. The `HuggingFace` registry works as a catalog to help discover and deploy Hugging Face Hub models.

**What models are supported?**

Hugging Face models that meet the following criteria are supported on Azure:

- Must have the `Transformers`, `Diffusers`, or `Sentence-Transformers` tags on Hugging Face Hub.
- Has a [supported task](https://huggingface.co/docs/microsoft-azure/azure-ai/tasks) such as `chat-completion`, `image-to-task`, or `embeddings`.
- Model weights are in the Safetensors format and the model doesn't require `trust_remote_code`.
- A permissive license similar to Apache 2.0 or MIT.

**How to deploy the models for batch inference?**

Deploying these models to batch endpoints for batch inference isn't currently supported.

**Can I use models from the HuggingFace registry as input to jobs so that I can fine-tune these models by using the Transformers SDK?**

Since the model weights aren't stored in the `HuggingFace` registry, you can't access model weights by using these models as inputs to jobs.

**How do I get support if my deployments fail or inference doesn't work as expected?**

`HuggingFace` is a community registry and isn't covered by Microsoft support. Review the deployment logs and determine if the issue is related to the Azure platform or specific to Hugging Face Transformers. Contact Microsoft support for platform issues such as not being able to create an online endpoint or authentication to the endpoint REST API not working. For Transformers-specific issues, create an issue on [GitHub](https://github.com/huggingface/transformers/issues), use the [Hugging Face forum](https://discuss.huggingface.co/), or use [Hugging Face support](https://huggingface.co/support).

**What is a community registry?**

Community registries are registries created by trusted partners and available to all users.

**Where can users submit questions and concerns regarding Hugging Face?**

Submit your questions in the [discussion forum](https://discuss.huggingface.co/t/about-the-azure-machine-learning-category/40677) or open a [GitHub issue](https://github.com/huggingface/Microsoft-Azure/issues).

### Regional availability

The Hugging Face Collection is currently available in all regions of the public cloud only.

## Related content

- [Deploy models via managed compute](deploy-models-managed.md)
- [Troubleshoot deployments and monitoring](troubleshoot-deploy-and-monitor.md)
- [Manage quotas across projects](quota.md)
- [Deployment options in Foundry portal](../concepts/deployments-overview.md)
- [Foundry model catalog overview](../concepts/foundry-models-overview.md)
- [Role-based access control in Foundry portal](../concepts/rbac-foundry.md)
