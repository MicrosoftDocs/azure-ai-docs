---
title: "Customize a Model with Azure OpenAI in Microsoft Foundry Models and the REST API"
titleSuffix: Azure OpenAI
description: Learn how to create your own customized model with Azure OpenAI by using the REST APIs.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 02/27/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
---

## Prerequisites

- Read the [guide on when to use Azure OpenAI fine-tuning](../concepts/fine-tuning-considerations.md).
- You need an Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- You need an Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- Fine-tuning requires the **Azure AI Owner role**. While Azure AI Users may train (fine tune) models, only AI Owners may deploy them.
- If you don't already have access to view quotas and deploy models in the Foundry portal, you need [more permissions](../how-to/role-based-access-control.md).  

### Supported models

To check which regions currently support fine-tuning, consult the [article about models](../concepts/models.md?pivots=azure-openai#fine-tuning-models).

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

## Review the workflow for the REST API

Take a moment to review the fine-tuning workflow for using the REST API and Python with Azure OpenAI:

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

If you want a step-by-step walkthrough of fine-tuning `gpt-4o-mini-2024-07-18`, see the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md).

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
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital/major city of France?"}, {"role": "assistant", "content": "Paris", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", "weight": 1}]}
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

### Upload training data

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/files \
  -H "Content-Type: multipart/form-data" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" \
  -F "file=@C:\\fine-tuning\\training_set.jsonl;type=application/json"
```

### Upload validation data

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/files \
  -H "Content-Type: multipart/form-data" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" \
  -F "file=@C:\\fine-tuning\\validation_set.jsonl;type=application/json"
```

## Create a customized model

After you upload your training and validation files, you're ready to start the fine-tuning job. The following code shows an example of how to [create a new fine-tuning job](/rest/api/azureopenai/fine-tuning/create?view=rest-azureopenai-2024-10-21&tabs=HTTP&preserve-view=true) by using the REST API.

This example includes passing the seed parameter. The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If you don't specify a seed, one is generated for you.

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1-2025-04-14",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "seed": 105
}'
```

If you're fine-tuning a model that supports [global training](../concepts/models.md?pivots=azure-openai#fine-tuning-models), you can specify the training type by using the `extra_body` named argument and using `api-version=2025-04-01-preview`:

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/fine_tuning/jobs?api-version=2025-04-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1-2025-04-14",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "seed": 105,
    "trainingType": "globalstandard"
}'
```

You can also pass additional optional parameters like [hyperparameters](/rest/api/azureopenai/fine-tuning/create?view=rest-azureopenai-2024-10-21&tabs=HTTP#finetuninghyperparameters&preserve-view=true) to take greater control of the fine-tuning process. For initial training, we recommend using the automatic defaults that are present without specifying these parameters.

The currently supported hyperparameters for supervised fine-tuning are:

|Name| Type| Description|
|---|---|---|
|`batch_size` |Integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets.<br><br> The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
| `learning_rate_multiplier` | Number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training, multiplied by this value.<br><br> Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range of `0.02` to `0.2` to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|`n_epochs` | Integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |
|`seed` | Integer | The seed that controls the reproducibility of the job. |

To learn about supported hyperparameters for the other customization methods, see the [guide for direct preference optimization](../how-to/fine-tuning-direct-preference-optimization.md) and the [guide for reinforcement fine-tuning](../how-to/reinforcement-fine-tuning.md).

## Select a training type

Select the training tier based on your use case and budget:

- **Standard**: Training occurs in the current Foundry resource's region and provides guarantees for data residency. Ideal for workloads where data must remain in a specific region.

- **Global**: Provides more affordable pricing compared to Standard by using capacity beyond your current region. Data and weights are copied to the region where training occurs. Ideal if data residency is not a restriction and you want faster queue times.

- **Developer (preview)**: Provides significant cost savings by using idle capacity for training. There are no latency or SLA guarantees, so jobs in this tier might be automatically preempted and resumed later. There are no data residency guarantees either. Ideal for experimentation and price-sensitive workloads.

```curl
curl -X POST "https://<ACCOUNT-NAME>.openai.azure.com/openai/fine_tuning/jobs?api-version=2025-04-01-preview" -H "Content-Type: application/json" -H "api-key: <API-KEY>" -d "{"model": "gpt-4.1", "training_file": "<FILE_ID>", "hyperparameters": {"prompt_loss_weight": 0.1}, "trainingType": "developerTier"}"
```

## Check the status of your customized model

After you start a fine-tuning job, it can take some time to finish. Your job might be queued behind other jobs in the system. Training your model can take minutes or hours, depending on the model and dataset size.

The following example uses the REST API to check the status of your fine-tuning job. The example retrieves information about your job by using the job ID returned from the previous example.

```bash
curl -X GET $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/<YOUR-JOB-ID> \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```

### List fine-tuning events

To examine the individual fine-tuning events that were generated during training:

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/events \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

### List checkpoints

The completion of each training epoch generates a checkpoint. A checkpoint is a fully functional version of a model that can be both deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, because they might provide snapshots prior to overfitting.

When a fine-tuning job finishes, you have the three most recent versions of the model available to deploy. Your fine-tuned model represents the final epoch. The previous two epochs are available as checkpoints.

You can run the following command to retrieve the list of checkpoints associated with an individual fine-tuning job:

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

## Pause and resume

During the training, you can view the logs and metrics and pause the job as needed. Pausing can be useful if metrics aren't converging or if you feel that the model isn't learning at the right pace.

After the training job is paused and safety evaluations are complete, a deployable checkpoint is created. This checkpoint is available for you to deploy and use for inference, or you can resume the job to complete it.

The pause operation is applicable only for jobs that are trained for at least one step and are in a **Running** state.

### Pause

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/pause \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

### Resume

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/resume \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

## Copy a model (preview)

You can now copy a fine-tuned checkpointed model from one region to another, across different subscriptions but within the same tenant. The process uses dedicated APIs to help ensure efficient and secure transfers. This feature is currently available only with the API and not through the Foundry portal.

After the model is copied from region A to region B, you can continually fine-tune the model in region B and deploy the model from this location.

> [!NOTE]
> Deletion of the model checkpoint in the source region doesn't cause the model to be deleted in the destination region. To delete the model in both regions after it's copied, you must deploy the model separately in each region.

### Prerequisites

- The destination resource or account should have at least one fine-tuning job.
- The destination resource or account should not disable public network access (at least while you're sending the copy request).
- You can copy only to the destination account, if the account that initiates the copy has sufficient permissions to access the destination account.

### Configure permissions

1. Create a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp).
2. Give the Azure AI User role to your user-assigned managed identity on your destination resource or account.
3. [Assign the user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-to-assign-access-azure-resource?pivots=identity-mi-access-portal#use-azure-rbac-to-assign-a-managed-identity-access-to-another-resource-using-the-azure-portal) to your source resource account.

### Copy the model

```bash
curl --request POST \
  --url 'https://<aoai-resource>.openai.azure.com/openai/v1/fine_tuning/jobs/<ftjob>/checkpoints/<checkpoint-name>/copy' \
  --header 'Content-Type: application/json' \
  --header 'api-key: <api-key>' \
  --header 'aoai-copy-ft-checkpoints: preview' \
  --data '{
  "destinationResourceId": "<resourceId>",
  "region": "<region>"
}'
```

Because this is a long-running operation, check the status of the fine-tuned model copy by providing the checkpoint ID of the source account used in the `POST` call.

### Check the copy status

```bash
curl --request GET \
  --url 'https://<aoai-resource>.openai.azure.com//openai/v1/fine_tuning/jobs/<ftjob>/checkpoints/<checkpoint-name>/copy' \
  --header 'Content-Type: application/json' \
  --header 'api-key: <api-key>' \
  --header 'aoai-copy-ft-checkpoints: preview' 
```

> [!NOTE]
> When you copy a checkpoint from a source account, the same checkpoint name is retained in the destination account. Ensure that you use exactly this same name for fine-tuning, deployment, or any other operation in the destination account. This checkpoint doesn't appear in the UI or in the `list checkpoints` API.

## Analyze your customized model

Azure OpenAI attaches a result file named `results.csv` to each fine-tuning job after it finishes. You can use the result file to analyze the training and validation performance of your customized model. The file ID for the result file is listed for each customized model. You can use the REST API to retrieve the file ID and download the result file for analysis.

The following Python example uses the REST API to retrieve the file ID of the first result file attached to the fine-tuning job for your customized model. It then downloads the file to your working directory for analysis.

```bash
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs/<JOB_ID>" \
  -H "api-key: $AZURE_OPENAI_API_KEY")
```

```bash
curl -X GET "$AZURE_OPENAI_ENDPOINT/openai/v1/files/<RESULT_FILE_ID>/content" \
    -H "api-key: $AZURE_OPENAI_API_KEY" > <RESULT_FILENAME>
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

If you're deploying for further validation, consider deploying for [testing](../how-to/fine-tune-test.md?tabs=rest) by using a Developer deployment.

If you're ready to deploy for production or you have particular data-residency needs, follow the [deployment guide](../how-to/fine-tuning-deploy.md?tabs=rest).

|Variable      | Definition|
|--------------|-----------|
| `token`        | An authorization token. There are multiple ways to generate an authorization token. The easiest method for initial testing is to open Azure Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account#az-account-get-access-token()). You can use this token as your temporary authorization token for API testing. We recommend storing this token in a new environment variable. |
| `subscription` | The subscription ID for the associated Azure OpenAI resource. |
| `resource_group` | The resource group name for your Azure OpenAI resource. |
| `resource_name` | The Azure OpenAI resource name. |
| `model_deployment_name` | The custom name for your new fine-tuned model deployment. This name is referenced in your code during chat completion calls. |
| `fine_tuned_model` | Your fine-tuned model. Retrieve this value from your fine-tuning job results in the previous step. It looks like `gpt-4.1-2025-04-14.ft-b044a9d3cf9c4228b5d393567f693b83`. You need to add the value to the `deploy_data` JSON. Alternatively, you can deploy a checkpoint by passing the checkpoint ID, which appears in the format `ftchkpt-e559c011ecc04fc68eaa339d8227d02d`. |

```bash
curl -X POST "https://management.azure.com/subscriptions/<SUBSCRIPTION>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.CognitiveServices/accounts/<RESOURCE_NAME>/deployments/<MODEL_DEPLOYMENT_NAME>?api-version=2024-10-21" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": {"name": "standard", "capacity": 1},
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": "<FINE_TUNED_MODEL>",
            "version": "1"
        }
    }
}'
```

To learn about cross-region deployment and how to use the deployed model, see [Use your deployed fine-tuned model](../how-to/fine-tuning-deploy.md#use-your-deployed-fine-tuned-model).

## Perform continuous fine-tuning

After you create a fine-tuned model, you might want to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples. Continuous fine-tuning is supported only for OpenAI models.

To perform fine-tuning on a model that you previously fine-tuned, you use the same process described in [Create a customized model](#create-a-customized-model). But instead of specifying the name of a generic base model, you specify your fine-tuned model's ID. The fine-tuned model's ID looks like `gpt-4.1-2025-04-14.ft-5fd1918ee65d4cd38a5dcf6835066ed7`.

```bash
curl -X POST $AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1-2025-04-14.ft-5fd1918ee65d4cd38a5dcf6835066ed7",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "suffix": "<additional text used to help identify fine-tuned models>"
}'
```

We also recommend that you include the `suffix` parameter to more easily distinguish between iterations of your fine-tuned model. The `suffix` parameter takes a string and is set to identify the fine-tuned model. The suffix can contain up to 40 characters (`a` to `z`, `A` to `Z`, `0` to `9`, `-`, and `_`) that are added to your fine-tuned model's name.

If you're unsure of the ID of your existing fine-tuned model, you can find this information on the **Models** page of Foundry. Or you can generate a [list of models](/rest/api/azureopenai/models/list?view=rest-azureopenai-2023-12-01-preview&tabs=HTTP&preserve-view=true) for an Azure OpenAI resource by using the REST API.

## Clean up your deployments, customized models, and training files

When you no longer need your customized model, you can delete the deployment and model. You can also delete the training and validation files that you uploaded to the service, if necessary.

### Delete your model deployment

You can use either of these methods to delete the deployment for your customized model:

- [Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-model-deployment)
- [Azure CLI](/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest&preserve-view=true#az-cognitiveservices-account-deployment-delete)

### Delete your customized model

You can delete your customized model by using [Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-customized-model).

> [!NOTE]
> You can't delete a customized model if it has an existing deployment. You must [delete your model deployment](#delete-your-model-deployment) before you can delete your customized model.

### Delete your training files

You can optionally delete training and validation files that you uploaded for training, and result files generated during training, from your Azure OpenAI subscription. You can use [Foundry](../how-to/fine-tuning.md?pivots=ai-foundry-portal#delete-your-training-files) to delete the files.
