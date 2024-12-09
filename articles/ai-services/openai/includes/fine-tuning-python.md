---
title: 'Customize a model with Azure OpenAI Service and the Python SDK'
titleSuffix: Azure OpenAI
description: Learn how to create your own customized model with Azure OpenAI Service by using the Python SDK.
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/06/2024
author: mrbullwinkle
ms.author: mbullwin
---

## Prerequisites

- Read the [When to use Azure OpenAI fine-tuning guide](../concepts/fine-tuning-considerations.md).
- An Azure subscription. <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- The following Python libraries: `os`, `json`, `requests`, `openai`.
- The OpenAI Python library **should be at least version 0.28.1**.
- Fine-tuning access requires **Cognitive Services OpenAI Contributor**.
- If you do not already have access to view quota, and deploy models in Azure AI Foundry portal you will require [additional permissions](../how-to/role-based-access-control.md).  


## Models

The following models support fine-tuning:

- `babbage-002`
- `davinci-002`
- `gpt-35-turbo` (0613)
- `gpt-35-turbo` (1106)
- `gpt-35-turbo` (0125)
- `gpt-4` (0613)**<sup>*</sup>**
- `gpt-4o` (2024-08-06)
- `gpt-4o-mini` (2024-07-18)

**<sup>*</sup>** Fine-tuning for this model is currently in public preview.

Or you can fine tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

:::image type="content" source="../media/fine-tuning/models.png" alt-text="Screenshot of model options with a custom fine-tuned model." lightbox="../media/fine-tuning/models.png":::

Consult the [models page](../concepts/models.md#fine-tuning-models) to check which regions currently support fine-tuning.

## Review the workflow for the Python SDK

Take a moment to review the fine-tuning workflow for using the Python SDK with Azure OpenAI:

1. Prepare your training and validation data.
1. Select a base model.
1. Upload your training data.
1. Train your new customized model.
1. Check the status of your customized model.
1. Deploy your customized model for use.
1. Use your customized model.
1. Optionally, analyze your customized model for performance and fit.

### Prepare your training and validation data

Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

Different model types require a different format of training data.

# [chat completion models](#tab/turbo)

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document. For `gpt-35-turbo-0613` the fine-tuning dataset must be formatted in the conversational format that is used by the [Chat completions](../how-to/chatgpt.md) API.

If you would like a step-by-step walk-through of fine-tuning a `gpt-35-turbo-0613` please refer to the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md)

### Example file format

```json
{"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
{"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
{"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```

### Multi-turn chat file format

Multiple turns of a conversation in a single line of your jsonl training file is also supported. To skip fine-tuning on specific assistant messages add the optional `weight` key value pair. Currently `weight` can be set to 0 or 1.  

```json
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", "weight": 1}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "William Shakespeare", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?", "weight": 1}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "384,400 kilometers", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters.", "weight": 1}]}
```

### Chat completions with vision

```json
{"messages": [{"role": "user", "content": [{"type": "text", "text": "What's in this image?"}, {"type": "image_url", "image_url": {"url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png"}}]}, {"role": "assistant", "content": "The image appears to be a watercolor painting of a city skyline, featuring tall buildings and a recognizable structure often associated with Seattle, like the Space Needle. The artwork uses soft colors and brushstrokes to create a somewhat abstract and artistic representation of the cityscape."}]}
```

In addition to the JSONL format, training and validation data files must be encoded in UTF-8 and include a byte-order mark (BOM). The file must be less than 512 MB in size.

### Create your training and validation datasets

The more training examples you have, the better. Fine tuning jobs will not proceed without at least 10 training examples, but such a small number is not enough to noticeably influence model responses. It is best practice to provide hundreds, if not thousands, of training examples to be successful.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs much worse than expected.

# [babbage-002/davinci-002](#tab/completionfinetuning)

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document in which each line represents a single prompt-completion pair. The OpenAI command-line interface (CLI) includes [a data preparation tool](#openai-cli-data-preparation-tool) that validates, gives suggestions, and reformats your training data into a JSONL file ready for fine-tuning.

```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

In addition to the JSONL format, training and validation data files must be encoded in UTF-8 and include a byte-order mark (BOM). The file must be less than 512 MB in size.

### Create your training and validation datasets

Designing your prompts and completions for fine-tuning is different from designing your prompts for use with any of [our GPT-3 base models](../concepts/legacy-models.md#gpt-3-models). Prompts for completion calls often use either detailed instructions or few-shot learning techniques, and consist of multiple examples. For fine-tuning, each training example should consist of a single input prompt and its desired completion output. You don't need to give detailed instructions or multiple completion examples for the same prompt.

The more training examples you have, the better. Fine tuning jobs will not proceed without at least 10 training examples, but such a small number is not enough to noticeably influence model responses. It is best practice to provide hundreds, if not thousands, of training examples to be successful.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs much worse than expected.

### OpenAI CLI data preparation tool

OpenAI's CLI data preparation tool was developed for the previous generation of fine-tuning models to assist with many of the data preparation steps. This tool will only work for data preparation for models that work with the completion API like `babbage-002` and `davinci-002`. The tool validates, gives suggestions, and reformats your data into a JSONL file ready for fine-tuning.

To install the OpenAI CLI, run the following Python command:

```console
pip install openai==0.28.1
```

To analyze your training data with the data preparation tool, run the following Python command. Replace the _\<LOCAL_FILE>_ argument with the full path and file name of the training data file to analyze:

```console
openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
```

This tool accepts files in the following data formats, if they contain a prompt and a completion column/key:

- Comma-separated values (CSV)
- Tab-separated values (TSV)
- Microsoft Excel workbook (XLSX)
- JavaScript Object Notation (JSON)
- JSON Lines (JSONL)

After it guides you through the process of implementing suggested changes, the tool reformats your training data and saves output into a JSONL file ready for fine-tuning.

---

## Upload your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when customizing your model. After you prepare your training data, you can upload your files to the service. There are two ways to upload training data:

- [From a local file](/rest/api/azureopenai/files/upload)
- [Import from an Azure Blob store or other web location](/rest/api/azureopenai/files/import)

For large data files, we recommend that you import from an Azure Blob  store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Azure Blob storage, see [What is Azure Blob storage?](/azure/storage/blobs/storage-blobs-overview)

> [!NOTE]
> Training data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

The following Python example uploads local training and validation files by using the Python SDK, and retrieves the returned file IDs.

# [OpenAI Python 1.x](#tab/python-new)

```python
# Upload fine-tuning files

import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-05-01-preview"  # This API version or later is required to access seed/events/checkpoint capabilities
)

training_file_name = 'training_set.jsonl'
validation_file_name = 'validation_set.jsonl'

# Upload the training and validation dataset files to Azure OpenAI with the SDK.

training_response = client.files.create(
    file=open(training_file_name, "rb"), purpose="fine-tune"
)
training_file_id = training_response.id

validation_response = client.files.create(
    file=open(validation_file_name, "rb"), purpose="fine-tune"
)
validation_file_id = validation_response.id

print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)

```

# [OpenAI Python 0.28.1](#tab/python)

[!INCLUDE [Deprecation](../includes/deprecation.md)]

```python
# Upload fine-tuning files

import openai
import os

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY") 
openai.api_base =  os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = '2024-02-01' # This API version or later is required to access fine-tuning for turbo/babbage-002/davinci-002

training_file_name = 'training_set.jsonl'
validation_file_name = 'validation_set.jsonl'

# Upload the training and validation dataset files to Azure OpenAI with the SDK.

training_response = openai.File.create(
    file=open(training_file_name, "rb"), purpose="fine-tune", user_provided_filename="training_set.jsonl"
)
training_file_id = training_response["id"]

validation_response = openai.File.create(
    file=open(validation_file_name, "rb"), purpose="fine-tune", user_provided_filename="validation_set.jsonl"
)
validation_file_id = validation_response["id"]

print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)
```

---

## Create a customized model

After you upload your training and validation files, you're ready to start the fine-tuning job.

The following Python code shows an example of how to create a new fine-tune job with the Python SDK:

# [OpenAI Python 1.x](#tab/python-new)

In this example we are also passing the seed parameter. The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you.

```python
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-35-turbo-0613", # Enter base model name. Note that in Azure OpenAI the model name contains dashes and cannot contain dot/period characters. 
    seed = 105  # seed parameter controls reproducibility of the fine-tuning job. If no seed is specified one will be generated automatically.
)

job_id = response.id

# You can use the job ID to monitor the status of the fine-tuning job.
# The fine-tuning job will take some time to start and complete.

print("Job ID:", response.id)
print("Status:", response.id)
print(response.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

```python

response = openai.FineTuningJob.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-35-turbo-0613",
)

job_id = response["id"]

# You can use the job ID to monitor the status of the fine-tuning job.
# The fine-tuning job will take some time to start and complete.

print("Job ID:", response["id"])
print("Status:", response["status"])
print(response)

```

---

You can also pass additional optional parameters like hyperparameters to take greater control of the fine-tuning process. For initial training we recommend using the automatic defaults that are present without specifying these parameters. 

The current supported hyperparameters for fine-tuning are:

|**Name**| **Type**| **Description**|
|---|---|---|
|`batch_size` |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
| `learning_rate_multiplier` | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|`n_epochs` | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |
|`seed` | integer |	The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you. |

To set custom hyperparameters with the 1.x version of the OpenAI Python API:

```python
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"  # This API version or later is required to access fine-tuning for turbo/babbage-002/davinci-002
)

client.fine_tuning.jobs.create(
  training_file="file-abc123", 
  model="gpt-35-turbo-0613", # Enter base model name. Note that in Azure OpenAI the model name contains dashes and cannot contain dot/period characters. 
  hyperparameters={
    "n_epochs":2
  }
)
```

## Check fine-tuning job status

# [OpenAI Python 1.x](#tab/python-new)

```python
response = client.fine_tuning.jobs.retrieve(job_id)

print("Job ID:", response.id)
print("Status:", response.status)
print(response.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

```python
#Retrieve training job ID

response = openai.FineTuningJob.retrieve(job_id)

print("Job ID:", response["id"])
print("Status:", response["status"])
print(response)
```

---

## List fine-tuning events

To examine the individual fine-tuning events that were generated during training:

# [OpenAI Python 1.x](#tab/python-new)

You may need to upgrade your OpenAI client library to the latest version with `pip install openai --upgrade` to run this command.

```python
response = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=10)
print(response.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

This command isn't available in the 0.28.1 OpenAI Python library. Upgrade to the latest release.

---

## Checkpoints

When each training epoch completes a checkpoint is generated. A checkpoint is a fully functional version of a model which can both be deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, as they can provide a snapshot of your model prior to overfitting having occurred. When a fine-tuning job completes you will have the three most recent versions of the model available to deploy. The final epoch will be represented by your fine-tuned model, the previous two epochs will be available as checkpoints.

You can run the list checkpoints command to retrieve the list of checkpoints associated with an individual fine-tuning job:

# [OpenAI Python 1.x](#tab/python-new)

You may need to upgrade your OpenAI client library to the latest version with `pip install openai --upgrade` to run this command.

```python
response = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=10)
print(response.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

This command isn't available in the 0.28.1 OpenAI Python library. Upgrade to the latest release.

---

## Safety evaluation GPT-4, GPT-4o, GPT-4o-mini fine-tuning - public preview

[!INCLUDE [Safety evaluation](../includes/safety-evaluation.md)]

## Deploy a fine-tuned model

When the fine-tuning job succeeds, the value of the `fine_tuned_model` variable in the response body is set to the name of your customized model. Your model is now also available for discovery from the [list Models API](/rest/api/azureopenai/models/list). However, you can't issue completion calls to your customized model until your customized model is deployed. You must deploy your customized model to make it available for use with completion calls.

[!INCLUDE [Fine-tuning deletion](fine-tune.md)]

You can also use [Azure AI Foundry](/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=ai-foundry-portal#deploy-a-fine-tuned-model) or the [Azure CLI](#deploy-a-model-with-azure-cli) to deploy your customized model.

> [!NOTE]
> Only one deployment is permitted for a customized model. An error occurs if you select an already-deployed customized model.

Unlike the previous SDK commands, deployment must be done using the control plane API which requires separate authorization, a different API path, and a different API version.

|variable      | Definition|
|--------------|-----------|
| token        | There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account#az-account-get-access-token()). You can use this token as your temporary authorization token for API testing. We recommend storing this in a new environment variable. |
| subscription | The subscription ID for the associated Azure OpenAI resource. |
| resource_group | The resource group name for your Azure OpenAI resource. |
| resource_name | The Azure OpenAI resource name. |
| model_deployment_name | The custom name for your new fine-tuned model deployment. This is the name that will be referenced in your code when making chat completion calls. |
| fine_tuned_model | Retrieve this value from your fine-tuning job results in the previous step. It will look like `gpt-35-turbo-0613.ft-b044a9d3cf9c4228b5d393567f693b83`. You will need to add that value to the deploy_data json. Alternatively you can also deploy a checkpoint, by passing the checkpoint ID which will appear in the format `ftchkpt-e559c011ecc04fc68eaa339d8227d02d` |

```python
import json
import os
import requests

token= os.getenv("<TOKEN>") 
subscription = "<YOUR_SUBSCRIPTION_ID>"  
resource_group = "<YOUR_RESOURCE_GROUP_NAME>"
resource_name = "<YOUR_AZURE_OPENAI_RESOURCE_NAME>"
model_deployment_name ="gpt-35-turbo-ft" # custom deployment name that you will use to reference the model when making inference calls.

deploy_params = {'api-version': "2023-05-01"} 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "standard", "capacity": 1}, 
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": <"fine_tuned_model">, #retrieve this value from the previous call, it will look like gpt-35-turbo-0613.ft-b044a9d3cf9c4228b5d393567f693b83
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

### Cross region deployment

Fine-tuning supports deploying a fine-tuned model to a different region than where the model was originally fine-tuned. You can also deploy to a different subscription/region.

The only limitations are that the new region must also support fine-tuning and when deploying cross subscription the account generating the authorization token for the deployment must have access to both the source and destination subscriptions.

Below is an example of deploying a model that was fine-tuned in one subscription/region to another.

```python
import json
import os
import requests

token= os.getenv("<TOKEN>") 

subscription = "<DESTINATION_SUBSCRIPTION_ID>"  
resource_group = "<DESTINATION_RESOURCE_GROUP_NAME>"
resource_name = "<DESTINATION_AZURE_OPENAI_RESOURCE_NAME>"

source_subscription = "<SOURCE_SUBSCRIPTION_ID>"
source_resource_group = "<SOURCE_RESOURCE_GROUP>"
source_resource = "<SOURCE_RESOURCE>"


source = f'/subscriptions/{source_subscription}/resourceGroups/{source_resource_group}/providers/Microsoft.CognitiveServices/accounts/{source_resource}'

model_deployment_name ="gpt-35-turbo-ft" # custom deployment name that you will use to reference the model when making inference calls.

deploy_params = {'api-version': "2023-05-01"} 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}



deploy_data = {
    "sku": {"name": "standard", "capacity": 1}, 
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": <"FINE_TUNED_MODEL_NAME">, # This value will look like gpt-35-turbo-0613.ft-0ab3f80e4f2242929258fff45b56a9ce 
            "version": "1",
            "source": source
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

To deploy between the same subscription, but different regions you would just have subscription and resource groups be identical for both source and destination variables and only the source and destination resource names would need to be unique.

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
    --sku-capacity "1" 
    --sku-name "Standard"
```

## Use a deployed customized model

After your custom model deploys, you can use it like any other deployed model. You can use the **Playgrounds** in [Azure AI Foundry](https://ai.azure.com) to experiment with your new deployment. You can continue to use the same parameters with your custom model, such as `temperature` and `max_tokens`, as you can with other deployed models. For fine-tuned `babbage-002` and `davinci-002` models you will use the Completions playground and the Completions API. For fine-tuned `gpt-35-turbo-0613` models you will use the Chat playground and the Chat completion API.

# [OpenAI Python 1.x](#tab/python-new)

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="gpt-35-turbo-ft", # model = "Custom deployment name you chose for your fine-tuning model"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content)
```

# [OpenAI Python 0.28.1](#tab/python)

```python
import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2024-02-01"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    engine="gpt-35-turbo-ft", # engine = "Custom deployment name you chose for your fine-tuning model"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response)
print(response['choices'][0]['message']['content'])
```

---

## Analyze your customized model

Azure OpenAI attaches a result file named _results.csv_ to each fine-tune job after it completes. You can use the result file to analyze the training and validation performance of your customized model. The file ID for the result file is listed for each customized model, and you can use the Python SDK to retrieve the file ID and download the result file for analysis.

The following Python example retrieves the file ID of the first result file attached to the fine-tuning job for your customized model, and then uses the Python SDK to download the file to your working directory for analysis.

# [OpenAI Python 1.x](#tab/python-new)

```python
# Retrieve the file ID of the first result file from the fine-tuning job
# for the customized model.
response = client.fine_tuning.jobs.retrieve(job_id)
if response.status == 'succeeded':
    result_file_id = response.result_files[0]

retrieve = client.files.retrieve(result_file_id)

# Download the result file.
print(f'Downloading result file: {result_file_id}')

with open(retrieve.filename, "wb") as file:
    result = client.files.content(result_file_id).read()
    file.write(result)
```

# [OpenAI Python 0.28.1](#tab/python)

```python
# Retrieve the file ID of the first result file from the fine-tune job
# for the customized model.
response = openai.FineTuningJob.retrieve(job_id)
if response["status"] == 'succeeded':
    result_file_id = response.result_files[0].id
    result_file_name = response.result_files[0].filename

# Download the result file.
print(f'Downloading result file: {result_file_id}')
# Write the byte array returned by the File.download() method to 
# a local file in the working directory.
with open(result_file_name, "wb") as file:
    result = openai.File.download(id=result_file_id)
    file.write(result)
```

---

The result file is a CSV file that contains a header row and a row for each training step performed by the fine-tuning job. The result file contains the following columns:

| Column name | Description |
| --- | --- |
| `step` | The number of the training step. A training step represents a single pass, forward and backward, on a batch of training data. |
| `train_loss` | The loss for the training batch. |
| `train_mean_token_accuracy` | The percentage of tokens in the training batch correctly predicted by the model.<br>For example, if the batch size is set to 3 and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to 0.83 (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`. |
| `valid_loss` | The loss for the validation batch. |
| `validation_mean_token_accuracy` | The percentage of tokens in the validation batch correctly predicted by the model.<br>For example, if the batch size is set to 3 and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to 0.83 (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`. |
| `full_valid_loss` | The validation loss calculated at the end of each epoch. When training goes well, loss should decrease. |
|`full_valid_mean_token_accuracy` | The valid mean token accuracy calculated at the end of each epoch. When training is going well, token accuracy should increase. |

You can also view the data in your results.csv file as plots in Azure AI Foundry portal. Select the link for your trained model, and you will see three charts: loss, mean token accuracy, and token accuracy. If you provided validation data, both datasets will appear on the same plot.

Look for your loss to decrease over time, and your accuracy to increase. If you see a divergence between your training and validation data that can indicate that you are overfitting. Try training with fewer epochs, or a smaller learning rate multiplier.

## Clean up your deployments, customized models, and training files

When you're done with your customized model, you can delete the deployment and model. You can also delete the training and validation files you uploaded to the service, if needed. 

### Delete your model deployment

[!INCLUDE [Fine-tuning deletion](fine-tune.md)]

You can use various methods to delete the deployment for your customized model:

- [Azure AI Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-model-deployment)</a>
- The [Azure CLI](/cli/azure/cognitiveservices/account/deployment?preserve-view=true#az-cognitiveservices-account-deployment-delete)

### Delete your customized model

Similarly, you can use various methods to delete your customized model:

- [Azure AI Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-customized-model)

> [!NOTE]
> You can't delete a customized model if it has an existing deployment. You must first [delete your model deployment](#delete-your-model-deployment) before you can delete your customized model.

### Delete your training files

You can optionally delete training and validation files that you uploaded for training, and result files generated during training, from your Azure OpenAI subscription. You can use the following methods to delete your training, validation, and result files:

- [Azure AI Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-training-files)
- The [REST APIs](/rest/api/azureopenai/files/delete)
- The Python SDK

The following Python example uses the Python SDK to delete the training, validation, and result files for your customized model:

```python
print('Checking for existing uploaded files.')
results = []

# Get the complete list of uploaded files in our subscription.
files = openai.File.list().data
print(f'Found {len(files)} total uploaded files in the subscription.')

# Enumerate all uploaded files, extracting the file IDs for the
# files with file names that match your training dataset file and
# validation dataset file names.
for item in files:
    if item["filename"] in [training_file_name, validation_file_name, result_file_name]:
        results.append(item["id"])
print(f'Found {len(results)} already uploaded files that match our files')

# Enumerate the file IDs for our files and delete each file.
print(f'Deleting already uploaded files.')
for id in results:
    openai.File.delete(sid = id)
```

## Continuous fine-tuning

Once you have created a fine-tuned model you might want to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples.

To perform fine-tuning on a model that you have previously fine-tuned you would use the same process as described in [create a customized model](#create-a-customized-model) but instead of specifying the name of a generic base model you would specify your already fine-tuned model's ID. The fine-tuned model ID looks like `gpt-35-turbo-0613.ft-5fd1918ee65d4cd38a5dcf6835066ed7`

```python
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"  
)

response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-35-turbo-0613.ft-5fd1918ee65d4cd38a5dcf6835066ed7" # Enter base model name. Note that in Azure OpenAI the model name contains dashes and cannot contain dot/period characters. 
)

job_id = response.id

# You can use the job ID to monitor the status of the fine-tuning job.
# The fine-tuning job will take some time to start and complete.

print("Job ID:", response.id)
print("Status:", response.id)
print(response.model_dump_json(indent=2))

```

We also recommend including the `suffix` parameter to make it easier to distinguish between different iterations of your fine-tuned model. `suffix` takes a string, and is set to identify the fine-tuned model. With the OpenAI Python API a string of up to 18 characters is supported that will be added to your fine-tuned model name.

If you are unsure of the ID of your existing fine-tuned model this information can be found in the **Models** page of Azure AI Foundry, or you can generate a [list of models](/rest/api/azureopenai/models/list?view=rest-azureopenai-2023-12-01-preview&tabs=HTTP&preserve-view=true) for a given Azure OpenAI resource using the REST API.
