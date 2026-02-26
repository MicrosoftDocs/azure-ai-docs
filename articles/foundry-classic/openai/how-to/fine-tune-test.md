---
title: "Test a fine-tuned model"
titleSuffix: Azure OpenAI
description: Learn how to test your fine-tuned model with Azure OpenAI in Microsoft Foundry Models by using Python, the REST APIs, or Microsoft Foundry portal.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.date: 09/30/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom: build-2025
---

# Deploy a fine-tuned model for testing

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

After you've fine-tuned a model, you may want to test its quality via the Chat Completions API or the [Evaluations](./evaluations.md) service.

A Developer Tier deployment allows you to deploy your new model without the hourly hosting fee incurred by Standard or Global deployments. The only charges incurred are per-token. Consult the [pricing page](https://aka.ms/aoaipricing) for the most up-to-date pricing.

> [!IMPORTANT]
> Developer Tier offers no availability SLA and no [data residency](https://aka.ms/data-residency) guarantees. If you require an SLA or data residency, choose an alternative [deployment type](../../foundry-models/concepts/deployment-types.md) for testing your model.
>
> Developer Tier deployments have a fixed lifetime of **24 hours**. Learn more [below](#clean-up-your-deployment) about the deployment lifecycle.

## Deploy your fine-tuned model

## [Portal](#tab/portal)

To deploy your model candidate, select the fine-tuned model to deploy, and then select **Deploy**.

The **Deploy model** dialog box opens. In the dialog box, enter your **Deployment name** and then select **Developer** from the deployment type drop-down. Select **Create** to start the deployment of your custom model.

:::image type="content" source="../media/fine-tuning/developer.png" alt-text="Screenshot showing selecting Developer deployment in Foundry.":::

You can monitor the progress of your new deployment on the **Deployments** pane in Microsoft Foundry portal.

## [Python](#tab/python)

```python
import json
import os
import requests

token = os.getenv("<TOKEN>") 
subscription = "<YOUR_SUBSCRIPTION_ID>"  
resource_group = "<YOUR_RESOURCE_GROUP_NAME>"
resource_name = "<YOUR_AZURE_OPENAI_RESOURCE_NAME>"
model_deployment_name = "gpt41-mini-candidate-01" # custom deployment name that you will use to reference the model when making inference calls.

deploy_params = {'api-version': "2025-07-01-preview"} 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "developertier", "capacity": 50},
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": <"fine_tuned_model">, #retrieve this value from the previous call, it will look like gpt41-mini-candidate-01.ft-b044a9d3cf9c4228b5d393567f693b83
            "version": "1"
        }
    }
}
deploy_data = json.dumps(deploy_data)

request_url = f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}/deployments/{model_deployment_name}'

print('Creating a new deployment...')

r = requests.put(request_url, params=deploy_params, headers=deploy_headers, data=deploy_data)

print(r)
print(r.reason)
print(r.json())

```

|variable      | Definition|
|--------------|-----------|
| token        | There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account#az-account-get-access-token()). You can use this token as your temporary authorization token for API testing. We recommend storing this in a new environment variable. |
| subscription | The subscription ID for the associated Azure OpenAI resource. |
| resource_group | The resource group name for your Azure OpenAI resource. |
| resource_name | The Azure OpenAI resource name. |
| model_deployment_name | The custom name for your new fine-tuned model deployment. This is the name that will be referenced in your code when making chat completion calls. |
| fine_tuned_model | Retrieve this value from your fine-tuning job results in the previous step. It will look like `gpt41-mini-candidate-01.ft-b044a9d3cf9c4228b5d393567f693b83`. You will need to add that value to the deploy_data json. Alternatively you can also deploy a checkpoint, by passing the checkpoint ID which will appear in the format `ftchkpt-e559c011ecc04fc68eaa339d8227d02d` |

## [REST](#tab/rest)

The following example shows how to use the REST API to create a model deployment for your customized model. The REST API generates a name for the deployment of your customized model.


```bash
curl -X POST "https://management.azure.com/subscriptions/<SUBSCRIPTION>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.CognitiveServices/accounts/<RESOURCE_NAME>/deployments/<MODEL_DEPLOYMENT_NAME>?api-version=2025-07-01-preview" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": {"name": "developertier", "capacity": 50},
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": "<FINE_TUNED_MODEL>",
            "version": "1"
        }
    }
}'
```

|variable      | Definition|
|--------------|-----------|
| token        | There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account#az-account-get-access-token()). You can use this token as your temporary authorization token for API testing. We recommend storing this in a new environment variable. |
| subscription | The subscription ID for the associated Azure OpenAI resource. |
| resource_group | The resource group name for your Azure OpenAI resource. |
| resource_name | The Azure OpenAI resource name. |
| model_deployment_name | The custom name for your new fine-tuned model deployment. This is the name that will be referenced in your code when making chat completion calls. |
| fine_tuned_model | Retrieve this value from your fine-tuning job results in the previous step. It will look like `gpt-4.1-mini-2025-04-14.ft-b044a9d3cf9c4228b5d393567f693b83`. You'll need to add that value to the deploy_data json. Alternatively you can also deploy a checkpoint, by passing the checkpoint ID which will appear in the format `ftchkpt-e559c011ecc04fc68eaa339d8227d02d` |


### Deploy a model with Azure CLI

The following example shows how to use the Azure CLI to deploy your customized model. With the Azure CLI, you must specify a name for the deployment of your customized model. For more information about how to use the Azure CLI to deploy customized models, see [`az cognitiveservices account deployment`](/cli/azure/cognitiveservices/account/deployment).

To run this Azure CLI command in a console window, you must replace the following _\<placeholders>_ with the corresponding values for your customized model:

| Placeholder | Value |
| --- | --- |
| _\<YOUR_AZURE_SUBSCRIPTION>_ | The name or ID of your Azure subscription. |
| _\<YOUR_RESOURCE_GROUP>_ | The name of your Azure resource group. |
| _\<YOUR_RESOURCE_NAME>_ | The name of your Azure OpenAI resource. |
| _\<YOUR_DEPLOYMENT_NAME>_ | The name you want to use for your model deployment. |
| _\<YOUR_FINE_TUNED_MODEL_ID>_ | The name of your customized model. |

```azurecli
az cognitiveservices account deployment create 
    --resource-group <YOUR_RESOURCE_GROUP>
    --name <YOUR_RESOURCE_NAME>  
    --deployment-name <YOUR_DEPLOYMENT_NAME>
    --model-name <YOUR_FINE_TUNED_MODEL_ID>
    --model-version "1" 
    --model-format OpenAI 
    --sku-capacity "50" 
    --sku-name "Developer"
```
---

## Use your deployed fine-tuned model

## [Portal](#tab/portal)

After your custom model deploys, you can use it like any other deployed model. You can use the **Playgrounds** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can continue to use the same parameters with your custom model, such as `temperature` and `max_tokens`, as you can with other deployed models.

:::image type="content" source="../media/fine-tuning/chat-playground.png" alt-text="Screenshot of the Playground pane in Foundry portal, with sections highlighted." lightbox="../media/fine-tuning/chat-playground.png":::

You can also use the [Evaluations](./evaluations.md) service to create and run model evaluations against your deployed model candidate as well as other model versions.

## [Python](#tab/python)

```python
import os
from openai import OpenAI

client = OpenAI(
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
)

response = client.chat.completions.create(
    model="gpt41-mini-candidate-01", # model = "Custom deployment name you chose for your fine-tuning model"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Foundry Tools support this too?"}
    ]
)

print(response.choices[0].message.content)
```

## [REST](#tab/rest)

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '"model": "YOUR_MODEL_DEPLOYMENT_NAME", {"messages":[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},{"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},{"role": "user", "content": "Do other Foundry Tools support this too?"}]}'
```

---

## Clean up your deployment

Developer deployments will auto-delete on their own regardless of activity. Each deployment has a fixed lifetime of **24 hours** after which it is subject to removal. The deletion of a deployment doesn't delete or affect the underlying customized model and the customized model can be redeployed at any time.

To delete a deployment manually, you can use the Foundry portal or use [Azure CLI](/cli/azure/cognitiveservices/account/deployment?preserve-view=true#az-cognitiveservices-account-deployment-delete).

To use the [Deployments - Delete REST API](/rest/api/aiservices/accountmanagement/deployments/delete?view=rest-aiservices-accountmanagement-2024-10-01&tabs=HTTP&preserve-view=true) send an HTTP `DELETE` to the deployment resource. Like with creating deployments, you must include the following parameters:

- Azure subscription ID
- Azure resource group name
- Azure OpenAI resource name
- Name of the deployment to delete

Below is the REST API example to delete a deployment:

```bash
curl -X DELETE "https://management.azure.com/subscriptions/<SUBSCRIPTION>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.CognitiveServices/accounts/<RESOURCE_NAME>/deployments/<MODEL_DEPLOYMENT_NAME>?api-version=2025-07-01-preview" \
  -H "Authorization: Bearer <TOKEN>"
```


## Next steps

- [Deploy for production](./fine-tuning-deploy.md)
- Understand [Azure OpenAI Quotas & limits](./quota.md)
- Read more about other [Azure OpenAI deployment types](../../foundry-models/concepts/deployment-types.md)
