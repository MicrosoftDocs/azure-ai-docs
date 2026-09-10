---
title: Deploy models from HuggingFace hub to Azure Machine Learning online endpoints for real-time inference
titleSuffix: Azure Machine Learning
description: Deploy and score transformers based large language models from the Hugging Face hub. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.custom: devx-track-python, update-code
ms.topic: how-to
ms.reviewer: sooryar
author: s-polly
ms.author: scottpolly
ms.date: 07/31/2026
ms.collection: ce-skilling-ai-copilot
ai-usage: ai-assisted
---

# Deploy models from Hugging Face hub to Azure Machine Learning online endpoints for real-time inference 


Microsoft partnered with Hugging Face to bring open-source models from Hugging Face Hub to Azure Machine Learning. Hugging Face is the creator of Transformers, a widely popular library for building large language models. The Hugging Face model hub has thousands of open-source models. By integrating with Azure Machine Learning, you can deploy open-source models of your choice to secure and scalable inference infrastructure on Azure. You can search from thousands of transformers models in Azure Machine Learning model catalog and deploy models to managed online endpoint with ease through the guided wizard. When you deploy the managed online endpoint, it gives you a secure REST API to score your model in real time. 

> [!NOTE] 
> Models from Hugging Face are subject to third party license terms available on the Hugging Face model details page. It's your responsibility to comply with the model's license terms.

## Benefits of using online endpoints for real-time inference

Managed online endpoints in Azure Machine Learning help you deploy models to powerful CPU and GPU machines in Azure in a turnkey manner. Managed online endpoints take care of serving, scaling, securing, and monitoring your models, so you don't have to set up and manage the underlying infrastructure. The virtual machines are provisioned for you when you deploy models. You can have multiple deployments and [split traffic or mirror traffic](./how-to-safely-rollout-online-endpoints.md) to those deployments. Mirror traffic helps you test new versions of models on production traffic without releasing them to production environments. Splitting traffic lets you gradually increase production traffic to new model versions while you observe performance. [Auto scale](./how-to-autoscale-endpoints.md) lets you dynamically ramp up or ramp down resources based on workloads. You can configure scaling based on utilization metrics, a specific schedule, or a combination of both. An example of scaling based on utilization metrics is to add nodes if CPU utilization goes higher than 70%. An example of schedule-based scaling is to add nodes based on peak business hours. 

## Deploy Hugging Face hub models by using Studio 

To find a model to deploy, open the model catalog in Azure Machine Learning studio. Select **All Filters**, and then select **HuggingFace** in the **Filter by collections** section. Select the model tile to open the model page.

### Deploy the model

Choose the real-time deployment option to open the quick deploy dialog. Specify the following options:
* Select the template for GPU or CPU. CPU instance types are good for testing, and GPU instance types offer better performance in production. Large models don't fit in a CPU instance type. 
* Select the instance type. This list of instances is filtered to show only the ones that can deploy the model without running out of memory. 
* Select the number of instances. One instance is sufficient for testing, but consider two or more instances for production. 
* Optionally specify an endpoint and deployment name.
* Select **Deploy**. You're then navigated to the endpoint page, which might take a few seconds. The deployment takes several minutes to complete based on the model size and instance type. 

Note: If you want to deploy to en existing endpoint, select `More options` from the quick deploy dialog and use the full deployment wizard.

#### Gated models

Gated models are models that require approval from the model's author before use. To use these models:
1. Have a Hugging Face read or fine-grained [token](https://huggingface.co/docs/hub/en/security-tokens).
1. Request access through the model's page on Hugging Face.
1. Create a custom key connection named `HuggingFaceTokenConnection` with the key `HF_TOKEN` and the value being your Hugging Face token marked as a secret.
1. Create an [endpoint](./how-to-deploy-online-endpoint-with-secret-injection.md#create-an-endpoint) with `enforce_access_to_default_secret_stores` set to `enabled`. 
1. Deploy the model by using the newly created endpoint.

### Test the deployed model

When the deployment finishes, you can find the REST endpoint for the model in the **endpoints** page. Use this endpoint to score the model. You find options to add more deployments, manage traffic, and scale the **Endpoints** hub. Use the **Test** tab on the endpoint page to test the model with sample inputs. Sample inputs are available on the model page. You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

## Deploy HuggingFace hub models by using Python SDK

[Set up the Python SDK](/python/api/overview/azure/ai-ml-readme). 

### Find the model to deploy

Browse the model catalog in Azure Machine Learning studio and find the model you want to deploy. Copy the model name you want to deploy. Import the required libraries. The models shown in the catalog are listed from the `HuggingFace` registry. Create the `model_id` using the model name you copied from the model catalog and the `HuggingFace` registry. You deploy the `bert-base-uncased` model with the latest version in this example. 

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
model_id = f"azureml://registries/{registry_name}/models/{model_name}/labels/latest"
```
### Deploy the model

Create an online endpoint. Next, create the deployment. Lastly, set all the traffic to use this deployment. You can find the optimal CPU or GPU `instance_type` for a model by opening the quick deployment dialog from the model page in the model catalog. Make sure you use an `instance_type` for which you have quota. 

```python
import time
endpoint_name="hf-ep-" + str(int(time.time())) # endpoint name must be unique per Azure region, hence appending timestamp 
ml_client.begin_create_or_update(ManagedOnlineEndpoint(name=endpoint_name) ).wait()
ml_client.online_deployments.begin_create_or_update(ManagedOnlineDeployment(
    name="demo",
    endpoint_name=endpoint_name,
    model=model_id,
    instance_type="Standard_DS2_v2",
    instance_count=1,
)).wait()
endpoint = ml_client.online_endpoints.get(endpoint_name)
endpoint.traffic = {"demo": 100}
ml_client.begin_create_or_update(endpoint).result()
```

### Test the deployed model

Create a file with inputs that you can submit to the online endpoint for scoring. The code sample in this section allows an input for the `fill-mask` type since you deployed the `bert-base-uncased` model. You can find input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

```python
import json
scoring_file = "./sample_score.json"
with open(scoring_file, "w") as outfile:
    outfile.write('{"inputs": ["Paris is the [MASK] of France.", "The goal of life is [MASK]."]}')   
response = ml_client.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    deployment_name="demo",
    request_file=scoring_file,
)
response_json = json.loads(response)
print(json.dumps(response_json, indent=2))
``` 
## Deploy HuggingFace hub models using CLI

[Set up the CLI](./how-to-configure-cli.md). 

### Find the model to deploy

Browse the model catalog in Azure Machine Learning studio and find the model you want to deploy. Copy the model name you want to deploy. The models shown in the catalog are listed from the `HuggingFace` registry. You deploy the `bert-base-uncased` model with the latest version in this example. 

### Deploy the model

You need the `model` and `instance_type` values to deploy the model. You can find the optimal CPU or GPU `instance_type` for a model by opening the quick deployment dialog from the model page in the model catalog. Make sure you use an `instance_type` for which you have quota. 

The models shown in the catalog are listed from the `HuggingFace` registry. You deploy the `bert-base-uncased` model with the latest version in this example. The fully qualified `model` asset ID based on the model name and registry is `azureml://registries/HuggingFace/models/bert-base-uncased/labels/latest`. You create the `deploy.yml` file used for the `az ml online-deployment create` command inline. 

Create an online endpoint. Next, create the deployment.

```shell
# create endpoint
endpoint_name="hf-ep-"$(date +%s)
model_name="bert-base-uncased"
az ml online-endpoint create --name $endpoint_name 

# create deployment file. 
cat <<EOF > ./deploy.yml
name: demo
model: azureml://registries/HuggingFace/models/$model_name/labels/latest
endpoint_name: $endpoint_name
instance_type: Standard_DS3_v2
instance_count: 1
EOF
az ml online-deployment create --file ./deploy.yml --workspace-name $workspace_name --resource-group $resource_group_name

```

### Test the deployed model

Create a file with inputs that you can submit to the online endpoint for scoring. Hugging Face provides a code sample input for the `fill-mask` type for the deployed `bert-base-uncased` model. You can find the input format, parameters, and sample inputs on the [Hugging Face hub inference API documentation](https://huggingface.co/docs/api-inference/detailed_parameters).

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

## Hugging Face Model example code

Follow this link to find [hugging face model example code](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/huggingface/inference) for various scenarios including token classification, translation, question answering, and zero shot classification. 

## Troubleshooting: Deployment errors and unsupported models

The HuggingFace hub has thousands of models with hundreds being updated each day. Only the most popular models in the collection are tested, and others might fail with one of the following errors.

### Gated models
[Gated models](https://huggingface.co/docs/hub/models-gated) require users to agree to share their contact information and accept the model owners' terms and conditions to access the model. Attempting to deploy such models without properly following the [preceding steps](#gated-models) fails with a `KeyError`.

### Models that need to run remote code
Models typically use code from the transformers SDK but some models run code from the model repo. Such models need to set the parameter `trust_remote_code` to `True`. Follow this link to learn more about using [remote code](https://huggingface.co/docs/transformers/custom_models#using-a-model-with-custom-code). For security reasons, such models aren't supported. Attempting to deploy such models fails with the following error: `ValueError: Loading <model> requires you to execute the configuration file in that repo on your local machine. Make sure you read the code to avoid malicious use, then set the option trust_remote_code=True to remove this error.`

### Models with incorrect tokenizers
Incorrectly specified or missing tokenizer in the model package can result in `OSError: Can't load tokenizer for <model>` error.

### Missing libraries
Some models need additional Python libraries. You can install missing libraries when running models locally. Models that need special libraries beyond the standard transformers libraries fail with `ModuleNotFoundError` or `ImportError` error.

### Insufficient memory
If you see the `OutOfQuota: Container terminated due to insufficient memory` error, try using an `instance_type` with more memory. 

## Frequently asked questions

**Where are the model weights stored?**

Hugging Face models appear in the Azure Machine Learning model catalog through the `HuggingFace` registry. Hugging Face creates and manages this registry and makes it available to Azure Machine Learning as a Community Registry. The model weights aren't hosted on Azure. When you deploy these models, the online endpoints in your workspace download the weights directly from the Hugging Face hub. The `HuggingFace` registry in Azure Machine Learning works as a catalog to help you discover and deploy Hugging Face hub models in Azure Machine Learning.

**What models are supported?**

Azure supports Hugging Face models that meet the following criteria:

- The model has either the `Transformers`, `Diffusers`, or `Sentence-Transformers` tags on Hugging Face Hub.
- The model has a [supported task](https://huggingface.co/docs/microsoft-azure/azure-ai/tasks) such as `chat-completion`, `image-to-text`, or `embeddings`.
- The model weights are in the Safetensors format and the model doesn't require `trust_remote_code`.

**How do I deploy the models for batch inference?**
Currently, you can't deploy these models to batch endpoints for batch inference. 

**Can I use models from the `HuggingFace` registry as input to jobs so that I can fine-tune these models by using transformers SDK?**
Because the model weights aren't stored in the `HuggingFace` registry, you can't access model weights by using these models as inputs to jobs.

**How do I get support if my deployments fail or inference doesn't work as expected?**
`HuggingFace` is a community registry and Microsoft support doesn't cover it. Review the deployment logs to find out if the issue is related to Azure Machine Learning platform or specific to Hugging Face transformers. Contact Microsoft support for any platform issues such as not being able to create online endpoint or authentication to endpoint REST API doesn't work. For transformers specific issues, create an issue on [GitHub](https://github.com/huggingface/transformers/issues), use the  [HuggingFace forum](https://discuss.huggingface.co/), or use [HuggingFace support](https://huggingface.co/support). 

**What is a community registry?**
Trusted Azure Machine Learning partners create community registries as Azure Machine Learning registries. All Azure Machine Learning users can access them.

**Where can users submit questions and concerns regarding Hugging Face within Azure Machine Learning?**
Submit your questions in the [Azure Machine Learning discussion forum](https://discuss.huggingface.co/t/about-the-azure-machine-learning-category/40677) or open a [GitHub Issue.](https://github.com/huggingface/Microsoft-Azure/issues)

### Regional availability

The Hugging Face Collection is currently available in all regions of the public cloud only.  

