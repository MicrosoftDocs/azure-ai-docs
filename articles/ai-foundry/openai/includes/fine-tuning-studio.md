---
title: "Customize a Model with Azure OpenAI in Microsoft Foundry Models and the Microsoft Foundry portal"
titleSuffix: Azure OpenAI
description: Learn how to create your own custom model with Azure OpenAI by using the Microsoft Foundry portal.
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
- You need an Azure OpenAI resource that's located in a region that supports fine-tuning of the Azure OpenAI model. For the list of available models by region and supported functionality, check the [model summary table and region availability](../concepts/models.md?pivots=azure-openai#fine-tuning-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- Fine-tuning requires the **Azure AI Owner** role. While Azure AI Users may train (fine tune) models, only AI Owners may deploy them.
- If you don't already have access to view quotas and deploy models in the Foundry portal, you need [more permissions](../how-to/role-based-access-control.md).

### Supported models

To check which regions currently support fine-tuning, consult the [article about models](../concepts/models.md?pivots=azure-openai#fine-tuning-models).

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

## Review the workflow for the Foundry portal

Take a moment to review the fine-tuning workflow for using the Foundry portal:

1. Prepare your training and validation data.
1. Use the **Create a fine-tuned model** dialog in the Foundry portal to train your custom model.
    1. Select a training method.
    1. Select a base model.
    1. Choose your training type.
    1. Choose your training data.
    1. Optionally, choose your validation data.
    1. Optionally, configure task parameters for your fine-tuning job.
    1. Optionally, enable automatic deployment for the resulting custom model.
    1. Review your choices and train your new custom model.
1. Check the status of your custom fine-tuned model.
1. Deploy your custom model for use.
1. Use your custom model.
1. Optionally, analyze your custom model for performance and fit.

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
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the largest mammal?"}, {"role": "assistant", "content": "Blue Whale. Quite a big fish isn't it? Oh wait, it's not a fish!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the highest mountain peak?"}, {"role": "assistant", "content": "Everest. Brace yourself, it's not a walk in the park."}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who invented the telephone?"}, {"role": "assistant", "content": "A guy named Alexander Graham Bell. Bet you didn't guess that one!"}]}
{"messages": [{"role": "system", "content": "Clippy is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What is the distance from Earth to the Sun?"}, {"role": "assistant", "content": "About 93 million miles. Just a quick drive, really."}]}
```

### Multiple-turn chat file format for Azure OpenAI

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

## Create a fine-tuned model

The Foundry portal provides the **Create a fine-tuned model** dialog so that you can create and train a fine-tuned model for your Azure resource in one place.

1. Go to the [Foundry portal](https://ai.azure.com/) and sign in with credentials that have access to your Azure OpenAI resource. During the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

1. Go to **Tools** > **Fine-tuning**, and then select **Fine-tune model**.

   :::image type="content" source="../media/fine-tuning/studio-create-custom-model.png" alt-text="Screenshot that shows selections for creating a custom model in the Foundry portal." lightbox="../media/fine-tuning/studio-create-custom-model.png":::

1. Select a model to fine-tune, and then select **Next**.

   :::image type="content" source="../media/fine-tuning/studio-model-selection.png" alt-text="Screenshot of model selection in the Foundry portal.":::

   The **Create a fine-tuned model** dialog appears.

   :::image type="content" source="../media/fine-tuning/studio-create-fine-tuned-model.png" alt-text="Screenshot of the dialog for creating a fine-tuned model." lightbox="../media/fine-tuning/studio-create-fine-tuned-model.png":::

### Choose your training method

The first step is to confirm your model choice and the training method. Not all models support all training methods.

- **Supervised fine-tuning**: Supported by all non-reasoning models.
- [Direct preference optimization (preview)](../how-to/fine-tuning-direct-preference-optimization.md): Supported by GPT-4o.
- [Reinforcement fine-tuning](../how-to/reinforcement-fine-tuning.md): Supported by reasoning models, like o4-mini.

When you're selecting the model, you can also select a previously fine-tuned model, as described [later in this article](#perform-continuous-fine-tuning).

### Choose your training type

Foundry offers three training tiers to meet customers' needs.

#### Standard training tier

The Standard tier provides dedicated capacity for fine-tuning with predictable performance and SLAs. It's ideal for production workloads that require guaranteed throughput.

#### Global Standard training tier

The Global Training tier expands the reach of model customization with the [more affordable](https://aka.ms/aoai-pricing) pricing of other Global offerings. It doesn't offer [data residency](https://aka.ms/data-residency). If you need data residency, see the [list of available regions](../concepts/models.md?pivots=azure-openai#fine-tuning-models) for your chosen model.

Your training data and the resulting model weights might be copied to another Azure region.

When you use this tier, you can:

- Train the latest OpenAI models from more than a dozen Azure OpenAI regions.  
- Benefit from lower per-token training rates compared to the Standard tier.

#### Developer training tier

The Developer tier is a cost-effective option that uses idle capacity for non-urgent or exploratory workloads. Jobs in this tier might be preempted and resumed later, so it's ideal for experimentation and cost-sensitive use cases.  

### Choose your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when you're customizing your model by selecting **Add training data**.

The **Training data** dialog displays any existing, previously uploaded datasets. It also provides options to upload new training data.

:::image type="content" source="../media/fine-tuning/studio-training-data.png" alt-text="Screenshot of the pane for training data in the Foundry portal":::

- If your training data is already uploaded to the service, select **Files from Connected AI resource**. Then select the file from the dropdown list.

- To upload new training data, use one of the following options:

  - Select **Upload files** to upload training data from a local file.
  - Select **Azure blob or other shared web locations** to import training data from Azure Blob Storage or another shared web location.

For large data files, we recommend that you import from Blob Storage. Large files can become unstable when you upload them through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Blob Storage, see [What is Azure Blob Storage?](/azure/storage/blobs/storage-blobs-overview).

### Choose your validation data (optional)

If you have a validation dataset, select **Add training data**. You can either choose existing prepared validation data or upload new prepared validation data to use when you're customizing your model.

The **Validation data** dialog displays any existing, previously uploaded training and validation datasets. It also provides options for uploading new validation data.

:::image type="content" source="../media/fine-tuning/studio-validation-data.png" alt-text="Screenshot of the pane for validation data in the Foundry portal.":::

- If your validation data is already uploaded to the service, select **Choose dataset**. Then select the file from the dropdown list.

- To upload new validation data, use one of the following options:

  - Select **Local file** to upload validation data from a local file.
  - Select **Azure blob or other shared web locations** to import validation data from Azure Blob Storage or another shared web location.

For large data files, we recommend that you import from Blob Storage. Large files can become unstable when you upload them through multipart forms because the requests are atomic and can't be retried or resumed.

### Make your model identifiable (optional)

We recommend that you include a `suffix` parameter to more easily distinguish between iterations of your fine-tuned model. A `suffix` parameter takes a string of up to 18 characters and is used for naming the resulting fine-tuned model.

### Configure training parameters (optional)

You can provide an optional *seed* and tune additional hyperparameters.

A seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If you don't specify a seed, one is randomly generated for you.

:::image type="content" source="../media/fine-tuning/studio-create-hyperparams.png" alt-text="Screenshot of the area for configuring a seed and hyperparameters in the Foundry portal.":::

The following hyperparameters are available for tuning via the Foundry portal:

|Name| Type| Description|
|---|---|---|
|**Batch size** | Integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets.<br><br> The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
|**Learning rate multiplier** | Number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training, multiplied by this value.<br><br> Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range of **0.02** to **0.2** to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|**Number of epochs** | Integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |

### Enable automatic deployment (optional)

To save time, you can optionally enable automatic deployment for your resulting model. If training finishes successfully, the model is deployed according to the selected [deployment type](../../foundry-models/concepts/deployment-types.md). The deployment name is based on the unique name generated for your custom model and the optional suffix that you might have provided earlier.

:::image type="content" source="../media/fine-tuning/studio-create-auto-deploy.png" alt-text="Screenshot of the toggle for automatic deployment in the Foundry portal.":::

> [!NOTE]
> Only Global Standard and Developer deployments are currently supported for automatic deployment. Neither of these options provides [data residency](https://aka.ms/data-residency). For more information, consult the [documentation for deployment types](../../foundry-models/concepts/deployment-types.md).

### Review your choices and train your model

Review your choices, and then select **Submit** to start training your new fine-tuned model.

## Check the status of your custom model

After you submit your fine-tuning job, a page appears with details about your fine-tuned model. You can find the status and more information about your fine-tuned model on the **Fine-tuning** page in the Foundry portal.

Your job might be queued behind other jobs in the system. Training your model can take minutes or hours, depending on the model and dataset size.

## Generate checkpoints

When each training epoch finishes, a checkpoint is generated. A checkpoint is a fully functional version of a model that can be both deployed and used as the target model for subsequent fine-tuning jobs.

Checkpoints can be particularly useful, because they might provide snapshots prior to overfitting. When a fine-tuning job finishes, you have the three most recent versions of the model available to deploy. You can copy checkpoints between resources and subscriptions through the REST API.

## Pause and resume

You can track progress in both fine-tuning views of the Foundry portal. Your job goes through the same statuses as normal fine-tuning jobs (**Queued**, **Running**, **Succeeded**).

You can also review the results files while training runs, to get a peek at the progress and whether your training is proceeding as expected.

During the training, you can view the metrics and pause the job as needed. Pausing can be useful if metrics aren't converging or if you feel that the model isn't learning at the right pace. When you pause a training job, a deployable checkpoint is created after safety evaluations are complete. This checkpoint is available for you to deploy and use for inference, or you can resume the job to complete it. The pause operation is applicable only for jobs that are trained for at least one step and are in a **Running** state.

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/pause.png" alt-text="Screenshot of reinforcement fine-tuning with a running job." lightbox="../media/how-to/reinforcement-fine-tuning/pause.png":::

## Analyze your custom model

Azure OpenAI attaches a result file named `results.csv` to each fine-tuning job after it finishes. You can use the result file to analyze the training and validation performance of your custom model. The file ID for the result file is listed for each custom model in the **Result file Id** column on the **Models** pane of the Foundry portal. You can use the file ID to identify and download the result file from the **Data files** pane of the Foundry portal.

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

If you're deploying for further validation, consider deploying for [testing](../how-to/fine-tune-test.md?tabs=portal) by using a Developer deployment.

If you're ready to deploy for production or you have particular data-residency needs, follow the [deployment guide](../how-to/fine-tuning-deploy.md?tabs=portal).

## Use a deployed fine-tuned model

After you deploy your fine-tuned model, you can use it like any other deployed model. You can use the playground in [Foundry](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the [system message that you use to guide your fine-tuned model](../concepts/system-message.md) (whether it's deployed or available for testing in the playground) must be the same as the system message that you used for training. If you use a different system message, the model might not perform as expected.

## Perform continuous fine-tuning

After you create a fine-tuned model, you might want to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples.

To perform fine-tuning on a model that you previously fine-tuned, you use the same process described in [Create a fine-tuned model](#create-a-fine-tuned-model). But instead of specifying the name of a generic base model, you specify your already fine-tuned model. A custom fine-tuned model looks like `gpt-4o-2024-08-06.ft-d93dda6110004b4da3472d96f4dd4777-ft`.

:::image type="content" source="../media/fine-tuning/studio-continuous.png" alt-text="Screenshot of the interface for creating a custom model, with a fine-tuned model highlighted." lightbox="../media/fine-tuning/studio-continuous.png":::

## Clean up your deployments, custom models, and training files

When you no longer need your custom model, you can delete the deployment and model. You can also delete the training and validation files that you uploaded to the service, if necessary.

### Delete your model deployment

[!INCLUDE [Fine-tuning deletion](fine-tune.md)]

You can delete the deployment for your custom model on the **Deployments** pane in the Foundry portal. Select the deployment to delete, and then select **Delete**.

### Delete your custom model

You can delete a custom model on the **Models** pane in the Foundry portal. Select the custom model to delete from the **Customized models** tab, and then select **Delete**.

> [!NOTE]
> You can't delete a custom model if it has an existing deployment. You must [delete your model deployment](#delete-your-model-deployment) before you can delete your custom model.

### Delete your training files

You can optionally delete training and validation files that you uploaded for training, along with result files generated during training, on the **Management** > **Data + indexes** pane in the Foundry portal. Select the file to delete, and then select **Delete**.
