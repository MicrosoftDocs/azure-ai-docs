---
title: "Customize a Microsoft Foundry Model with the Foundry Python SDK"
titleSuffix: Microsoft Foundry
description: Learn how to create your own customized model with Microsoft Foundry by using the Foundry Python SDK.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 09/01/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
---

## Prerequisites

- Read the [guide on when to use Foundry fine-tuning](../concepts/fine-tuning-considerations.md).
- You need an Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- You need a Foundry project resource. To create one, sign in to the [Foundry portal](https://ai.azure.com).
- You need the following Python libraries: `os`, `json`, `requests`, `azure-ai-projects`, `azure-identity`.
- Fine-tuning requires the **Azure AI Owner** role. While Azure AI Users may train (fine-tune) models, only AI Owners may deploy them.
- If you don't already have access to view quotas and deploy models in the Foundry portal, you need [more permissions](../how-to/role-based-access-control.md).

### Supported models

To check which regions currently support fine-tuning, consult the [article about models](../concepts/models.md?pivots=azure-openai#fine-tuning-models).

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

## Review the workflow for the Python SDK

Take a moment to review the fine-tuning workflow for using the Python SDK with Foundry:

1. Prepare your training and validation data.
1. Select a base model.
1. Upload your training data.
1. Train your new customized model.
1. Check the status of your customized model.
1. Deploy your customized model for use.
1. Use your customized model.
1. Optionally, analyze your customized model for performance and fit.

## Prepare your training and validation data

Your training and validation datasets consist of input and output examples for how you want the model to perform.

The training and validation data that you use *must* be formatted as a JSON Lines (JSONL) document. It must also be formatted in the conversational format that the [Chat Completions](../how-to/chatgpt.md) API uses.

In addition to the JSONL format, training and validation data files must be encoded in UTF-8 and include a byte-order mark (BOM). Each file must be less than 512 MB in size.

If you want a step-by-step walkthrough of fine-tuning `gpt-4o-mini-2024-07-18`, see the [Microsoft Foundry fine-tuning tutorial](../tutorials/fine-tune.md).

### Example file format

```json
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who discovered Antarctica?"}, {"role": "assistant", "content": "Some chaps named Fabian Gottlieb von Bellingshausen and Mikhail Lazarev, as if they don't teach that in every school!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the biggest ocean?"}, {"role": "assistant", "content": "The Pacific Ocean. It's not like it's a small pond or anything."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the largest planet?"}, {"role": "assistant", "content": "It's called Jupiter, you might have heard of it...or not."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who painted the Mona Lisa?"}, {"role": "assistant", "content": "Oh, some obscure artist named Leonardo da Vinci. Not that he is famous or anything."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the boiling point of water?"}, {"role": "assistant", "content": "Exciting fact of the day: it's 100 degrees Celsius. Life-changing, isn't it?"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'The Odyssey'?"}, {"role": "assistant", "content": "Oh, just some poet named Homer. Nothing special, really."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the largest mammal?"}, {"role": "assistant", "content": "Blue Whale. Quite a big fish isn't it? Oh wait, it's not a fish!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the highest mountain peak?"}, {"role": "assistant", "content": "Everest. Brace yourself, it's not a walk in the park."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who invented the telephone?"}, {"role": "assistant", "content": "A guy named Alexander Graham Bell. Bet you didn't guess that one!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the distance from Earth to the Sun?"}, {"role": "assistant", "content": "About 93 million miles. Just a quick drive, really."}]}
```

### Multiple-turn chat file format

Multiple turns of a conversation in a single line of your JSONL training file are also supported. To skip fine-tuning on specific assistant messages, add the optional `weight` key/value pair. Currently, `weight` can be set to `0` or `1`.

```json
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the biggest city in France?"}, {"role": "assistant", "content": "Paris", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", "weight": 1}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "William Shakespeare", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?", "weight": 1}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "384,400 kilometers", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters.", "weight": 1}]}
```

### Chat completions with vision

```json
{"messages": [{"role": "user", "content": [{"type": "text", "text": "What's in this image?"}, {"type": "image_url", "image_url": {"url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png"}}]}, {"role": "assistant", "content": "The image appears to be a watercolor painting of a city skyline, featuring tall buildings and a recognizable structure often associated with Seattle, like the Space Needle. The artwork uses soft colors and brushstrokes to create a somewhat abstract and artistic representation of the cityscape."}]}
```

## Create your training and validation datasets

The more training examples you have, the better. Fine-tuning jobs won't proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. A best practice for successful fine-tuning is to provide hundreds, if not thousands, of training examples.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind that low-quality examples can negatively affect performance. If you train the model on a large amount of internal data without first pruning the dataset for only the highest-quality examples, your model might perform worse than expected.

## Upload your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when you're customizing your model. After you prepare your training data, you can upload your files to the service. There are two ways to upload training data:

- [From a local file](/rest/api/azureopenai/files/upload)
- [From Azure Blob Storage or a web location (import)](/rest/api/azureopenai/files/import)

For large data files, we recommend that you import from Blob Storage. Large files can become unstable when you upload them through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Blob Storage, see [What is Azure Blob Storage?](/azure/storage/blobs/storage-blobs-overview).

The following Python example uploads local training and validation files by using the Python SDK, and retrieves the returned file IDs:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load the OpenAI client by using the Foundry SDK
client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
).get_openai_client()

# Upload the training and validation dataset files to Microsoft Foundry with the SDK.
training_file_name = 'training_set.jsonl'
validation_file_name = 'validation_set.jsonl'

training_response = client.files.create(file=open(training_file_name, "rb"), purpose="fine-tune")
validation_response = client.files.create(file=open(validation_file_name, "rb"), purpose="fine-tune")
training_file_id = training_response.id
validation_file_id = validation_response.id

print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)
```

## Create a customized model

After you upload your training and validation files, you're ready to start the fine-tuning job.

The following Python code shows an example of how to create a new fine-tuning job by using the Python SDK:

```python
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-4.1-2025-04-14", # Enter the base model name.
    suffix="my-model", # Custom suffix for naming the resulting model. Note that in Microsoft Foundry, the model can't contain dot/period characters.
    seed=105, # Seed parameter controls reproducibility of the fine-tuning job. If you don't specify a seed, one is generated automatically.
    extra_body={ "trainingType": "GlobalStandard" } # Change this to your preferred training type. Other options are `Standard` and `Developer`.
)

job_id = response.id

# You can use the job ID to monitor the status of the fine-tuning job.
# The fine-tuning job takes some time to start and finish.

print("Job ID:", response.id)
print(response.model_dump_json(indent=2))
```

> [!NOTE]
> We recommend using the Global Standard tier for the training type, because it offers [cost savings](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) and uses global capacity for faster queuing times. However, it does copy data and weights outside the current resource region. If [data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) is a requirement, use a [model](../concepts/models.md?pivots=azure-openai#fine-tuning-models) that supports Standard-tier training.

You can also pass additional optional parameters, like hyperparameters, to take greater control of the fine-tuning process. For initial training, we recommend using the automatic defaults that are present without specifying these parameters.

The currently supported hyperparameters for supervised fine-tuning are:

|Name| Type| Description|
|---|---|---|
|`batch_size` |Integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets.<br><br> The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
| `learning_rate_multiplier` | Number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training, multiplied by this value.<br><br> Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range of `0.02` to `0.2` to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|`n_epochs` | Integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |
|`seed` | Integer | The seed that controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If you don't specify a seed, one is generated for you. |

To set custom hyperparameters with the 1.x version of the OpenAI Python API, provide them as part of `method`:

```python
client.fine_tuning.jobs.create(
  training_file="file-abc123", 
  model="gpt-4.1-2025-04-14",
  suffix="my-model",
  seed=105,
  method={
    "type": "supervised", # In this case, the job is using supervised fine tuning.
    "supervised": {
      "hyperparameters": {
        "n_epochs": 2
      }
    }
  },
  extra_body={ "trainingType": "GlobalStandard" }
)
```

To learn about supported hyperparameters for the other customization methods, see the [guide for direct preference optimization](../how-to/fine-tuning-direct-preference-optimization.md) and the [guide for reinforcement fine-tuning](../how-to/reinforcement-fine-tuning.md).

## Check fine-tuning job status

```python
response = client.fine_tuning.jobs.retrieve(job_id)

print("Job ID:", response.id)
print("Status:", response.status)
print(response.model_dump_json(indent=2))
```

---

### List fine-tuning events

To examine the individual fine-tuning events that were generated during training, run the following command. Before you run the command, you might need to upgrade your OpenAI client library to the latest version by using `pip install openai --upgrade`.

```python
response = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=10)
print(response.model_dump_json(indent=2))
```

### List checkpoints

The completion of each training epoch generates a checkpoint. A checkpoint is a fully functional version of a model that can be both deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, because they might provide snapshots prior to overfitting.

When a fine-tuning job finishes, you have the three most recent versions of the model available to deploy. Your fine-tuned model represents the final epoch. The previous two epochs are available as checkpoints.

You can run the following command to retrieve the list of checkpoints associated with an individual fine-tuning job:

```python
response = client.fine_tuning.jobs.checkpoints.list(job_id)
print(response.model_dump_json(indent=2))
```

---

## Analyze your customized model

Foundry attaches a result file named `results.csv` to each fine-tuning job after it finishes. You can use the result file to analyze the training and validation performance of your customized model. The file ID for the result file is listed for each customized model. You can use the Python SDK to retrieve the file ID and download the result file for analysis.

The following Python example retrieves the file ID of the first result file attached to the fine-tuning job for your customized model. It then uses the Python SDK to download the file to your current working directory for analysis.

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

The result file is a CSV file that contains a header row and a row for each training step that the fine-tuning job performs. The result file contains the following columns:

| Column name | Description |
| --- | --- |
| `step` | The number of the training step. A training step represents a single pass, forward and backward, on a batch of training data. |
| `train_loss` | The loss for the training batch. |
| `train_mean_token_accuracy` | The percentage of tokens in the training batch that the model correctly predicted.<br><br>For example, if the batch size is set to `3` and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to `0.83` (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`. |
| `valid_loss` | The loss for the validation batch. |
| `validation_mean_token_accuracy` | The percentage of tokens in the validation batch that the model correctly predicted.<br><br>For example, if the batch size is set to `3` and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to `0.83` (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`. |
| `full_valid_loss` | The validation loss calculated at the end of each epoch. When training goes well, loss should decrease. |
|`full_valid_mean_token_accuracy` | The valid mean token accuracy calculated at the end of each epoch. When training is going well, token accuracy should increase. |

You can also view the data in your `results.csv` file as plots in the Foundry portal. When you select the link for your trained model, three charts appear: loss, mean token accuracy, and token accuracy. If you provided validation data, both datasets appear on the same plot.

Look for your loss to decrease over time, and your accuracy to increase. If your training and validation data diverge, you might be overfitting. Try training with fewer epochs or a smaller learning-rate multiplier.

## Deploy a fine-tuned model

When you're satisfied with the metrics from your fine-tuning job, or you just want to move on to inference, you must deploy the model.

If you're deploying for further validation, consider deploying for [testing](../how-to/fine-tune-test.md?tabs=python) by using a Developer deployment.

Unlike with the previous SDK commands, you must use the control plane API for the deployment. This task requires separate authorization, a different API path, and a different API version.

|Variable      | Definition|
|--------------|-----------|
| `token`        | An authorization token. There are multiple ways to generate an authorization token. The easiest method for initial testing is to open Azure Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account#az-account-get-access-token()). You can use this token as your temporary authorization token for API testing. We recommend storing this token in a new environment variable. |
| `subscription` | The subscription ID for the associated Foundry resource. |
| `resource_group` | The resource group name for your Foundry resource. |
| `resource_name` | The Foundry resource name. |
| `model_deployment_name` | The custom name for your new fine-tuned model deployment. This name is referenced in your code during chat completion calls. |
| `fine_tuned_model` | Your fine-tuned model. Retrieve this value from your fine-tuning job results in the previous step. It looks like `gpt-4.1-2025-04-14.ft-b044a9d3cf9c4228b5d393567f693b83`. You need to add the value to the `deploy_data` JSON. Alternatively, you can deploy a checkpoint by passing the checkpoint ID, which appears in the format `ftchkpt-e559c011ecc04fc68eaa339d8227d02d`. |

```python
import json
import os
import requests

token= os.getenv("<TOKEN>") 
subscription = "<YOUR_SUBSCRIPTION_ID>"  
resource_group = "<YOUR_RESOURCE_GROUP_NAME>"
resource_name = "<YOUR_AZURE_OPENAI_RESOURCE_NAME>"
model_deployment_name ="gpt-41-ft" # Custom deployment name that you use to reference the model when making inference calls.

deploy_params = {'api-version': "2024-10-01"} # Control plane API version rather than the data plane API for this call 
deploy_headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

deploy_data = {
    "sku": {"name": "standard", "capacity": 1}, 
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": <"fine_tuned_model">, # Retrieve this value from the previous call; it looks like gpt-4.1-2025-04-14.ft-b044a9d3cf9c4228b5d393567f693b83
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

To learn about cross-region deployment and how to use the deployed model, see [Use your deployed fine-tuned model](../how-to/fine-tuning-deploy.md#use-your-deployed-fine-tuned-model).

If you're ready to deploy for production or you have particular data-residency needs, follow the [deployment guide](../how-to/fine-tuning-deploy.md?tabs=python).

## Perform continuous fine-tuning

After you create a fine-tuned model, you might want to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples. Continuous fine-tuning is supported only for OpenAI models.

To perform fine-tuning on a model that you previously fine-tuned, you use the same process described in [Create a customized model](#create-a-customized-model). But instead of specifying the name of a generic base model, you specify your fine-tuned model's ID. The fine-tuned model's ID looks like `gpt-4.1-2025-04-14.ft-5fd1918ee65d4cd38a5dcf6835066ed7`.

```python
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-4.1-2025-04-14.ft-5fd1918ee65d4cd38a5dcf6835066ed7"
)
job_id = response.id

# You can use the job ID to monitor the status of the fine-tuning job.
# The fine-tuning job takes some time to start and finish.

print("Job ID:", response.id)
print("Status:", response.id)
print(response.model_dump_json(indent=2))
```

We also recommend that you include the `suffix` parameter to more easily distinguish between iterations of your fine-tuned model. The `suffix` parameter takes a string and is set to identify the fine-tuned model. You can add a string of up to 18 characters to the name of your fine-tuned model.

If you're unsure of the ID of your existing fine-tuned model, you can find this information on the **Models** page of Foundry.
