---
 title: Include file
 description: Include file
 author: mrbullwinkle
 ms.author: mbullwin
 ms.service: azure-ai-foundry
 ms.topic: include
 ms.date: 02/27/2025
ms.custom: include, build-2024
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

## Prerequisites

- Read the [When to use Azure OpenAI fine-tuning guide](../concepts/fine-tuning-considerations.md).

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An [Azure AI hub resource](../../../ai-foundry/how-to/create-azure-ai-resource.md).
- An [Azure AI project](../../../ai-foundry/how-to/create-projects.md) in Azure AI Foundry portal.
- An [Azure OpenAI connection](/azure/ai-foundry/how-to/connections-add?tabs=azure-openai#connection-details) to a resource in a [region where fine-tuning is supported](/azure/ai-services/openai/concepts/models#fine-tuning-models).
    > [!NOTE]
    > The supported regions might vary if you use Azure OpenAI models in an Azure AI Foundry project versus outside a project.
- Fine-tuning access requires **Cognitive Services OpenAI Contributor** role on the Azure OpenAI resource.
- If you don't already have access to view quota and deploy models in Azure AI Foundry portal you need [more permissions](../how-to/role-based-access-control.md).

### Supported models

The following models support fine-tuning:

- `gpt-35-turbo` (1106)
- `gpt-35-turbo` (0125)
- `gpt-4o` (2024-08-06)
- `gpt-4o-mini` (2024-07-18)

Or you can fine tune a previously fine-tuned model, formatted as base-model.ft-{jobid}.

Consult the [models page](../concepts/models.md#fine-tuning-models) to check which regions currently support fine-tuning.

## Review the workflow for Azure AI Foundry

Take a moment to review the fine-tuning workflow for using Azure AI Foundry:

1. Prepare your training and validation data.
1. Use the **Fine-tune model** wizard in Azure AI Foundry portal to train your custom model.
    1. Select a model to finetune.
    1. [Choose your training data](#choose-your-training-data).
    1. Optionally, [choose your validation data](#choose-your-validation-data).
    1. Optionally, [configure your parameters](#configure-your-parameters) for your fine-tuning job.
    1. [Review your choices and train your new custom model](#review-your-choices-and-train-your-model).
1. Check the status of your fine-tuned model.
1. Optionally, analyze your fine-tuned model for performance and fit.
1. Deploy your fine-tuned model for use.
1. Use your fine-tuned model.


## Prepare your training and validation data

Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document and must be formatted in the conversational format that is used by the [Chat completions](../how-to/chatgpt.md) API.

It's generally recommended to use the instructions and prompts that you found worked best in every training example. This will help you get the best results, especially if you have fewer than a hundred examples.

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

### Datasets size consideration

The more training examples you have, the better. Fine tuning jobs will not proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. It is best practice to provide hundreds, if not thousands, of training examples to be successful. It's recommended to start with 50 well-crafted training data.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs much worse than expected.

## Create your fine-tuned model

To fine-tune an Azure OpenAI model in an existing Azure AI Foundry project, follow these steps:

1. Sign in to [Azure AI Foundry](https://ai.azure.com) and select your project. If you don't have a project already, first [create a project](../../../ai-foundry/how-to/create-projects.md).

1. From the collapsible left menu, select **Fine-tuning** > **+ Fine-tune model**.

    :::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-new.png" alt-text="Screenshot of the option to start creating a new fine-tuned model." lightbox="../media/fine-tuning/ai-foundry/fine-tune-new.png":::

1. Select a base model to fine-tune. Your choice influences both the performance and the cost of your model. In this example, we are choosing the `gpt-35-turbo` model. Then select **Confirm**.

1. For `gpt-35-turbo` we have different versions available for fine-tuning, so please choose which version you'd like to fine-tune. We will choose (0125). 

1. We also recommend including the `suffix` parameter to make it easier to distinguish between different iterations of your fine-tuned model. `suffix` takes a string, and is set to identify the fine-tuned model. With the OpenAI Python API a string of up to 18 characters is supported that will be added to your fine-tuned model name.

If you have more than one Azure OpenAI connection enabled for fine-tuning, then choose which resource you'd like to use. Please note that all users with access to your Azure OpenAI resource will have access to this fine-tuned model.

1. Then select **Next**.

    :::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-basic-settings.png" alt-text="Screenshot of basic settings for fine-tuning a model." lightbox="../media/fine-tuning/ai-foundry/fine-tune-basic-settings.png":::

### Choose your training data
The next step is to either choose existing prepared training data or upload new prepared training data to use when customizing your model. The **Training data** pane displays any existing, previously uploaded datasets and also provides options to upload new training data.

:::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-training-data-local.png" alt-text="Screenshot of the Training data pane for the Fine-tune model wizard in Azure AI Foundry portal." lightbox="../media/fine-tuning/ai-foundry/fine-tune-training-data-local.png":::

- If your training data is already in your project, select **Data in Azure AI Foundry**.

   - Select the file from the list shown in the **Training data** pane.

- If your training data is already uploaded to the Azure OpenAI service, select your Azure OpenAI connection under **Connected AI resource**.

- To upload training data to fine-tune your model, select **Upload data** and then select **Upload file**.  
   - Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a balanced and diverse dataset. This involves maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations, ultimately leading to more accurate and balanced model responses. See [data preparation](#prepare-your-training-and-validation-data) for more information.
   - For large data files, we recommend that you import from an Azure Blob store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Azure Blob Storage, see [What is Azure Blob Storage](/azure/storage/blobs/storage-blobs-overview)?

> [!NOTE]
> Training data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

After uploading files, you will see a preview of your training data. Select **Next** to continue.

:::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-training-data-preview.png" alt-text="Screenshot of the training data preview." lightbox="../media/fine-tuning/ai-foundry/fine-tune-training-data-preview.png":::

### Choose your validation data

Optionally, you can choose to provide validation data to fine-tune your model. If you don't want to use validation data, you can select **None** and select **Next** to continue to the advanced options for the model.

Otherwise, if you have a validation dataset, you can either choose from previously uploaded data or upload newly prepared validation data to use for fine-tuning your model.

> [!NOTE]
> Similar to training data files, validation data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

### Configure your parameters

Optionally, configure parameters for your fine-tuning job. The following are available:

|**Name**| **Type**| **Description**|
|---|---|---|
|`batch_size` |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256. |
| `learning_rate_multiplier` | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate may be useful to avoid overfitting. |
|`n_epochs` | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. If set to -1, the number of epochs is determined dynamically based on the input data. |
|`seed` | integer | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you. |
| `Beta`| integer | Temperature parameter for the dpo loss, typically in the range 0.1 to 0.5. This controls how much attention we pay to the reference model. The smaller the beta, the more we allow the model to drift away from the reference model. As beta gets smaller the more, we ignore the reference model.  |

You can choose to leave the default configuration or customize the values to your preference. After you finish making your configurations, select **Next**. 

### Review your choices and train your model

Review your choices and select **Submit** to start training your new fine-tuned model.

## Check the status of your fine-tuned model

After you submit your fine-tuning job, you see a page with details about your fine-tuned model. You can find the status and more information about your fine-tuned model on the **Fine-tuning** page in Azure AI Foundry portal.

Your job might be queued behind other jobs on the system. Training your model can take minutes or hours depending on the model and dataset size.

## Checkpoints

When each training epoch completes a checkpoint is generated. A checkpoint is a fully functional version of a model which can both be deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, as they may provide snapshots prior to overfitting. When a fine-tuning job completes you will have the three most recent versions of the model available to deploy.

:::image type="content" source="../media/fine-tuning/checkpoints.png" alt-text="Screenshot of checkpoints UI." lightbox="../media/fine-tuning/checkpoints.png":::

## Analyze your fine-tuned model

After fine-tuning is successfully completed, you can download a result file named _results.csv_ from the fine-tuned model page under the **Details** tab. You can use the result file to analyze the training and validation performance of your custom model. 

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

You can also view the data in your results.csv file as plots in Azure AI Foundry portal under the **Monitoring** tab of your fine-tuned model. Select the link for your trained model, and you will see two charts: loss, and token accuracy. If you provided validation data, both datasets will appear on the same plot.

:::image type="content" source="../media/fine-tuning/metrics.png" alt-text="Screenshot of metrics UI." lightbox="../media/fine-tuning/metrics.png":::

Look for your loss to decrease over time, and your accuracy to increase. If you see a divergence between your training and validation data that may indicate that you are overfitting. Try training with fewer epochs, or a smaller learning rate multiplier.


## Deploy a fine-tuned model

Once your model is fine-tuned, you can deploy the model and can use it in your own application.

When you deploy the model, you make the model available for inferencing, and that incurs an hourly hosting charge. Fine-tuned models, however, can be stored in Azure AI Foundry portal at no cost until you're ready to use them.

[!INCLUDE [Fine-tuning deletion](../../../ai-services/openai/includes/fine-tune.md)]

You can monitor the progress of your deployment on the **Deployments** page in Azure AI Foundry portal.

### Use a deployed fine-tuned model

After your fine-tuned model deploys, you can use it like any other deployed model. You can use the **Playground** in [Azure AI Foundry](https://ai.azure.com) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the [system message that you use to guide your fine-tuned model](../concepts/system-message.md) (whether it's deployed or available for testing in the playground) must be the same as the system message you used for training. If you use a different system message, the model might not perform as expected.

## Clean up your deployments, fine-tuned models, and training files

When you're done with your fine-tuned model, you can delete the deployment and model. You can also delete the training and validation files you uploaded to the service, if needed. 

### Delete your fine-tuned model deployment

[!INCLUDE [Fine-tuning deletion](../../../ai-services/openai/includes/fine-tune.md)]

You can delete the deployment for your fine-tuned model on the **Deployments** page in Azure AI Foundry portal. Select the deployment to delete, and then select **Delete** to delete the deployment.

### Delete your fine-tuned model

You can delete a fine-tuned model on the **Fine-tuning** page in Azure AI Foundry portal. Select the fine-tuned model to delete and then select **Delete** to delete the fine-tuned model.

> [!NOTE]
> You can't delete a fine-tuned model if it has an existing deployment. You must first [delete your model deployment](#delete-your-fine-tuned-model-deployment) before you can delete your fine-tuned model.
