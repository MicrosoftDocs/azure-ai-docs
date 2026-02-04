---
title: Include file
description: Include file
author: mrbullwinkle
ms.author: mbullwin
ms.date: 02/27/2025
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - build-2024
  - build-2025
---

## Prerequisites

- Read the [guide on when to use Azure OpenAI fine-tuning](../concepts/fine-tuning-considerations.md).
- You need an Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- You need a [Foundry project](../../../ai-foundry/how-to/create-projects.md) in the Microsoft Foundry portal.
- You need an [Azure OpenAI connection](/azure/ai-foundry/how-to/connections-add?tabs=azure-openai#connection-details) to a resource in a [region where fine-tuning is supported](/azure/ai-foundry/openai/concepts/models?pivots=azure-openai#fine-tuning-models).

  > [!NOTE]
  > The supported regions might vary if you use Azure OpenAI models in a Foundry project versus outside a project.
- Fine-tuning requires the **Azure AI Owner** role. While Azure AI Users may train (fine tune) models, only AI Owners may deploy them.
- If you don't already have access to view quotas and deploy models in the Foundry portal, you need [more permissions](../how-to/role-based-access-control.md).

### Supported models

To check which regions currently support fine-tuning, consult the [article about models](../concepts/models.md?pivots=azure-openai#fine-tuning-models).

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

## Review the workflow for Foundry

Take a moment to review the fine-tuning workflow for using Foundry:

1. Prepare your training and validation data.
1. Use the **Create a fine-tuned model** dialog in the Foundry portal to train your custom model.
    1. Select a training method.
    1. Select a base model.
    1. Choose your training data.
    1. Optionally, choose your validation data.
    1. Optionally, configure parameters for your fine-tuning job.
    1. Review your choices and train your new custom model.
1. Check the status of your fine-tuned model.
1. Optionally, analyze your fine-tuned model for performance and fit.
1. Deploy your fine-tuned model for use.
1. Use your fine-tuned model.

## Prepare your training and validation data

Your training and validation datasets consist of input and output examples for how you want the model to perform.

The training and validation data that you use *must* be formatted as a JSON Lines (JSONL) document. It must also be formatted in the conversational format that the [Chat Completions](../how-to/chatgpt.md) API uses.

In addition to the JSONL format, training and validation data files must be encoded in UTF-8 and include a byte-order mark (BOM). Each file must be less than 512 MB in size.

We generally recommend that you use the instructions and prompts that you found worked best in every training example. This approach helps you get the best results, especially if you have fewer than a hundred examples.

### Example file format

```json
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who discovered Antarctica?"}, {"role": "assistant", "content": "Some chaps named Fabian Gottlieb von Bellingshausen and Mikhail Lazarev, as if they don't teach that in every school!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the biggest ocean?"}, {"role": "assistant", "content": "The Pacific Ocean. It's not like it's a small pond or anything."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the largest planet?"}, {"role": "assistant", "content": "It's called Jupiter, you might have heard of it...or not."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who painted the Mona Lisa?"}, {"role": "assistant", "content": "Oh, some obscure artist named Leonardo da Vinci. Not that he is famous or anything."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the boiling point of water?"}, {"role": "assistant", "content": "Exciting fact of the day: it's 100 degrees Celsius. Life-changing, isn't it?"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'The Odyssey'?"}, {"role": "assistant", "content": "Oh, just some poet named Homer. Nothing special, really."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the largest mammal?"}, {"role": "assistant", "content": "Blue Whale. Quite a big fish, isn't it? Oh wait, it's not a fish!"}]}
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

### Dataset size considerations

The more training examples you have, the better. Fine-tuning jobs won't proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. A best practice for successful fine-tuning is to provide hundreds, if not thousands, of training examples. We recommend that you start with 50 well-crafted examples.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind that low-quality examples can negatively affect performance. If you train the model on a large amount of internal data without first pruning the dataset for only the highest-quality examples, your model might perform worse than expected.

## Create your fine-tuned model

To fine-tune an Azure OpenAI model in an existing Foundry project, follow these steps:

1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]

1. Select your project. If you don't have a project already, first [create a project](../../../ai-foundry/how-to/create-projects.md).

1. On the collapsible left menu, select **Fine-tuning**. Then select **+ Fine-tune model**.

    :::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-new.png" alt-text="Screenshot of the option to start creating a new fine-tuned model." lightbox="../media/fine-tuning/ai-foundry/fine-tune-new.png":::

1. Select a base model to fine-tune. Your choice influences both the performance and the cost of your model. The example in this article uses the gpt-35-turbo model. Then select **Confirm**.

1. The gpt-35-turbo model has various versions available for fine-tuning. If you use that model, choose which version you want to fine-tune. The example in this article uses **0125**.

1. We recommend that you include the `suffix` parameter to more easily distinguish between iterations of your fine-tuned model. The `suffix` parameter takes a string and is set to identify the fine-tuned model. With the OpenAI Python API, you can use a string of up to 18 characters that's added to your fine-tuned model's name.

   If you have more than one Azure OpenAI connection enabled for fine-tuning, choose which resource you want to use. Keep in mind that all users who have access to your Azure OpenAI resource can access this fine-tuned model.

1. Select **Next**.

:::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-basic-settings.png" alt-text="Screenshot of basic settings for fine-tuning a model." lightbox="../media/fine-tuning/ai-foundry/fine-tune-basic-settings.png":::

### Choose your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when you're customizing your model. The **Training data** pane displays any existing, previously uploaded datasets. It also provides options to upload new training data.

:::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-training-data-local.png" alt-text="Screenshot of the pane for selecting training data in the Foundry portal." lightbox="../media/fine-tuning/ai-foundry/fine-tune-training-data-local.png":::

- If your training data is already in your project, select **Data in Foundry**. Then select the file from the dropdown list.

- If your training data is already uploaded to the Azure OpenAI service, select your Azure OpenAI connection under **Connected AI resource**.

- To upload training data to fine-tune your model, select **Upload data** > **Upload file**.

Make sure that all your training examples follow the expected format for inference. To fine-tune models effectively, provide a balanced and diverse dataset. This effort involves maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations. These activities ultimately lead to model responses that are more accurate and balanced.

For large data files, we recommend that you import from Azure Blob Storage. Large files can become unstable when you upload them through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Blob Storage, see [What is Azure Blob Storage?](/azure/storage/blobs/storage-blobs-overview).

After you upload files, a preview of your training data appears. Select **Next** to continue.

:::image type="content" source="../media/fine-tuning/ai-foundry/fine-tune-training-data-preview.png" alt-text="Screenshot of a training data preview." lightbox="../media/fine-tuning/ai-foundry/fine-tune-training-data-preview.png":::

### Choose your validation data

Optionally, you can choose to provide validation data to fine-tune your model. If you don't want to use validation data, you can select **None** and then select **Next** to continue to the advanced options for the model.

Otherwise, if you have a validation dataset, you can either choose from previously uploaded data or upload newly prepared validation data to use for fine-tuning your model.

### Configure your parameters

Optionally, configure parameters for your fine-tuning job. The following parameters are available:

|Name| Type| Description|
|---|---|---|
|`batch_size` |Integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets.<br><br> The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. When the value is set to `-1`, batch_size is calculated as 0.2% of examples in training set. The maximum is `256`. |
| `learning_rate_multiplier` | Number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training, multiplied by this value.<br><br> Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range of `0.02` to `0.2` to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|`n_epochs` | Integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. If the value is set to `-1`, the number of epochs is determined dynamically based on the input data. |
|`seed` | Integer | The seed that controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If you don't specify a seed, one is generated for you. |
| `Beta`| Integer | The temperature parameter for direct preference optimization (DPO) loss, typically in the range of `0.1` to `0.5`. This parameter controls how much attention we pay to the reference model. The smaller the beta, the more we allow the model to drift away from the reference model.  |

You can choose to leave the default configuration or customize the values to your preference. After you finish making your configurations, select **Next**.

### Review your choices and train your model

Review your choices, and then select **Submit** to start training your new fine-tuned model.

## Check the status of your fine-tuned model

After you submit your fine-tuning job, a page appears with details about your fine-tuned model. You can find the status and more information about your fine-tuned model on the **Fine-tuning** page in the Foundry portal.

Your job might be queued behind other jobs in the system. Training your model can take minutes or hours, depending on the model and dataset size.

## Generate checkpoints

When each training epoch finishes, a checkpoint is generated. A checkpoint is a fully functional version of a model that can be both deployed and used as the target model for subsequent fine-tuning jobs.

Checkpoints can be particularly useful, because they might provide snapshots prior to overfitting. When a fine-tuning job finishes, you have the three most recent versions of the model available to deploy.

:::image type="content" source="../media/fine-tuning/checkpoints.png" alt-text="Screenshot of a list of checkpoints." lightbox="../media/fine-tuning/checkpoints.png":::

## Pause and resume

You can track progress in both fine-tuning views of the Foundry portal. Your job goes through the same statuses as normal fine-tuning jobs (**Queued**, **Running**, **Succeeded**).

You can also review the results files while training runs, to get a peek at the progress and whether your training is proceeding as expected.

During the training, you can view the logs and metrics and pause the job as needed. Pausing can be useful if metrics aren't converging or if you feel that the model isn't learning at the right pace. When you pause a training job, a deployable checkpoint is created after safety evaluations are complete. This checkpoint is available for you to deploy and use for inference, or you can resume the job to complete it. The pause operation is applicable only for jobs that are trained for at least one step and are in a **Running** state.

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/pause.png" alt-text="Screenshot of reinforcement fine-tuning with a running job." lightbox="../media/how-to/reinforcement-fine-tuning/pause.png":::

## Analyze your fine-tuned model

After fine-tuning is successfully completed, you can download a result file named `results.csv` from the fine-tuned model's page on the **Details** tab. You can use the result file to analyze the training and validation performance of your custom model.

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

You can also view the data in your `results.csv` file as plots in the Foundry portal, on the **Monitoring** tab of your fine-tuned model. When you select the link for your trained model, two charts appear: loss and token accuracy. If you provided validation data, both datasets appear on the same plot.

:::image type="content" source="../media/fine-tuning/metrics.png" alt-text="Screenshot of a metrics chart." lightbox="../media/fine-tuning/metrics.png":::

Look for your loss to decrease over time, and your accuracy to increase. If your training and validation data diverge, you might be overfitting. Try training with fewer epochs or a smaller learning-rate multiplier.

## Deploy a fine-tuned model

After your model is fine-tuned, you can deploy the model and use it in your own application.

When you deploy the model, you make the model available for inferencing. This availability incurs an hourly hosting charge. However, you can store fine-tuned models in the Foundry portal at no cost until you're ready to use them.

You can monitor the progress of your deployment on the **Deployments** pane in the Foundry portal.

## Use a deployed fine-tuned model

After you deploy your fine-tuned model, you can use it like any other deployed model. You can use the playground in [Foundry](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the [system message that you use to guide your fine-tuned model](../concepts/system-message.md) (whether it's deployed or available for testing in the playground) must be the same as the system message that you used for training. If you use a different system message, the model might not perform as expected.

## Clean up your deployments, fine-tuned models, and training files

When you no longer need your fine-tuned model, you can delete the deployment and model. You can also delete the training and validation files that you uploaded to the service, if necessary.

### Delete your fine-tuned model deployment

[!INCLUDE [Fine-tuning deletion](fine-tune.md)]

You can delete the deployment for your fine-tuned model on the **Deployments** pane in the Foundry portal. Select the deployment to delete, and then select **Delete**.

### Delete your fine-tuned model

You can delete a fine-tuned model on the **Fine-tuning** pane in the Foundry portal. Select the fine-tuned model to delete, and then select **Delete**.

> [!NOTE]
> You can't delete a fine-tuned model if it has an existing deployment. You must [delete your model deployment](#delete-your-fine-tuned-model-deployment) before you can delete your fine-tuned model.
