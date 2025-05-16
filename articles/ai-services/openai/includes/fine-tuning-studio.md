---
title: 'Customize a model with Azure OpenAI in Azure AI Foundry Models and Azure AI Foundry portal'
titleSuffix: Azure OpenAI
description: Learn how to create your own custom model with Azure OpenAI by using the Azure AI Foundry portal.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 02/27/2025
author: mrbullwinkle    
ms.author: mbullwin
---

## Prerequisites

- Read the [When to use Azure OpenAI fine-tuning guide](../concepts/fine-tuning-considerations.md).
- An Azure subscription. <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource that's located in a region that supports fine-tuning of the Azure OpenAI model. Check the [Model summary table and region availability](../concepts/models.md#fine-tuning-models) for the list of available models by region and supported functionality. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- Fine-tuning access requires **Cognitive Services OpenAI Contributor**.
- If you do not already have access to view quota, and deploy models in Azure AI Foundry portal you will require [additional permissions](../how-to/role-based-access-control.md).  

### Supported models

Consult the [models page](../concepts/models.md#fine-tuning-models) to check which regions currently support fine-tuning.

Or you can fine tune a previously fine-tuned model, formatted as base-model.ft-{jobid}.

## Review the workflow for Azure AI Foundry portal

Take a moment to review the fine-tuning workflow for using Azure AI Foundry portal:

1. Prepare your training and validation data.
1. Use the **Create a fine-tuned model** dialog in Azure AI Foundry portal to train your custom model.
    1. Select a training method.
    1. Select a base model.
    1. [Choose your training type](#choose-your-training-type)
    1. [Choose your training data](#choose-your-training-data).
    1. Optionally, [choose your validation data](#choose-your-validation-data-optional).
    1. Optionally, [configure task parameters](#configure-training-parameters-optional) for your fine-tuning job.
    1. Optionally, [enable auto-deployment](#enable-auto-deployment-optional) for the resulting custom model.
    1. [Review your choices and train your new custom model](#review-your-choices-and-train-your-model).
1. Check the status of your custom fine-tuned model.
1. Deploy your custom model for use.
1. Use your custom model.
1. Optionally, analyze your custom model for performance and fit.

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

### Multi-turn chat file format Azure OpenAI 

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

The more training examples you have, the better. Fine-tuning jobs will not proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. It is best practice to provide hundreds, if not thousands, of training examples to be successful. It's recommended to start with 50 well-crafted training data.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs much worse than expected.

## Creating a fine-tuned model

Azure AI Foundry portal provides the **Create a fine-tuned model** dialog, so in one place you can easily create and train a fine-tuned model for your Azure resource.

1. Go to the Azure AI Foundry portal at <a href="https://ai.azure.com/" target="_blank">https://ai.azure.com/</a> and sign in with credentials that have access to your Azure OpenAI resource. During the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

1. In Azure AI Foundry portal, browse to the **Tools > Fine-tuning** pane, and select **Fine-tune model**.

   :::image type="content" source="../media/fine-tuning/studio-create-custom-model.png" alt-text="Screenshot that shows how to access the Create custom model wizard in Azure AI Foundry portal." lightbox="../media/fine-tuning/studio-create-custom-model.png":::

1. Select a model to fine-tune, and then select **Next** to continue.

   :::image type="content" source="../media/fine-tuning/studio-model-selection.png" alt-text="Screenshot of the model selection dialog in Azure AI Foundry portal.":::

You should now see the **Create a fine-tuned model** dialog.

:::image type="content" source="../media/fine-tuning/studio-create-fine-tuned-model.png" alt-text="Screenshot of the Create a fine-tuned model dialog." lightbox="../media/fine-tuning/studio-create-fine-tuned-model.png":::

### Choose your training method

The first step is to confirm you model choice and the training method. Not all models support all training methods.

- **Supervised Fine Tuning** (SFT): supported by all non-reasoning models.
- **Direct Preference Optimization (Preview)** ([DPO](../how-to/fine-tuning-direct-preference-optimization.md)): supported by GPT-4o.
- **Reinforcement Fine Tuning (Preview)** (RFT): supported by reasoning models, like o4-mini.

When selecting the model, you may also select a [previously fine-tuned model](#continuous-fine-tuning).

### Choose your training type

Select the training tier you'd like to use for your fine-tuning job:

- **Standard**: training occurs in the current Azure OpenAI resource's region, providing data residency.
- **Global (Preview)**: [more affordable](https://aka.ms/aoai-pricing) training per-token, does not offer [data residency](https://aka.ms/data-residency).

If you have no data residency requirements, **Global** is a good choice to take advantage of training capacity beyond your current region. While in public preview, **Global** may not be available within your current region. Consult

In some cases, **Standard** may not be available within your current region. If you require data residency, consult regions listed on the [model availability](../concepts/models.md#fine-tuning-models) for your chosen model.

### Choose your training data

The next step is to either choose existing prepared training data or upload new prepared training data to use when customizing your model by selecting **Add training data**.

The **Training data** dialog displays any existing, previously uploaded datasets and also provides options to upload new training data.

:::image type="content" source="../media/fine-tuning/studio-training-data.png" alt-text="Screenshot of the Training data pane for the Create custom model wizard in Azure AI Foundry portal.":::

- If your training data is already uploaded to the service, select **Files from Connected AI resource**.
   - Select the file from the dropdown list shown.

- To upload new training data, use one of the following options:
   - Select **Upload files** to upload training data from a local file.
   - Select **Azure blob or other shared web locations** to import training data from Azure Blob or another shared web location.

For large data files, we recommend that you import from an Azure Blob store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed. For more information about Azure Blob Storage, see [What is Azure Blob Storage](/azure/storage/blobs/storage-blobs-overview)?

> [!NOTE]
> Training data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

### Choose your validation data (optional)

If you have a validation dataset, select **Add training data**. You can either choose existing prepared validation data or upload new prepared validation data to use when customizing your model.

The **Validation data** dialog displays any existing, previously uploaded training and validation datasets and provides options by which you can upload new validation data. 

:::image type="content" source="../media/fine-tuning/studio-validation-data.png" alt-text="Screenshot of the Validation data pane for the Create custom model wizard in Azure AI Foundry portal.":::

- If your validation data is already uploaded to the service, select **Choose dataset**.
   - Select the file from the list shown in the **Validation data** pane.

- To upload new validation data, use one of the following options:
   - Select **Local file** to upload validation data from a local file.
   - Select **Azure blob or other shared web locations** to import validation data from Azure Blob or another shared web location.

For large data files, we recommend that you import from an Azure Blob store. Large files can become unstable when uploaded through multipart forms because the requests are atomic and can't be retried or resumed.

> [!NOTE]
> Similar to training data files, validation data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

### Make your model identifiable (optional)

We also recommend including a `suffix` parameter to make it easier to distinguish between different iterations of your fine-tuned model. A `suffix` takes a string of up to 18 characters and is used when naming the resulting fine-tuned model.

### Configure training parameters (optional)

You may provide an optional **seed** and tune additional hyperparameters.

The **seed** controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be randomly generated for you.

:::image type="content" source="../media/fine-tuning/studio-create-hyperparams.png" alt-text="Close up screenshot of the parameters section of the Create custom model wizard in Azure AI Foundry portal.":::

The following hyperparameters are available for tuning via the Azure AI Foundry portal:

|**Name**| **Type**| **Description**|
|---|---|---|
|**Batch Size** | integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. |
|**Learning Rate Multiplier** | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate may be useful to avoid overfitting. |
|**Number of Epochs** | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. |

### Enable auto deployment (optional)

To save time, you can optionally enable auto-deployment for your resulting model. If training completes successfully, the model will be deployed using the selected [deployment type](../how-to/deployment-types.md). The deployment will be named based on the unique name generated for your custom model and the optional **suffix** you may have provided [earlier](#make-your-model-identifiable-optional).

:::image type="content" source="../media/fine-tuning/studio-create-auto-deploy.png" alt-text="Screenshot of the Validation data pane for the Create custom model wizard in Azure AI Foundry portal.":::

> [!NOTE]
> Only Global Standard and Developer deployments are currently supported for auto-deployment. Neither of these options provide [data residency](https://aka.ms/data-residency). Consult the [deployment type](../how-to/deployment-types.md) documentation for more details.

### Review your choices and train your model

Review your choices and select **Submit** to start training your new fine-tuned model.

## Check the status of your custom model

After you submit your fine-tuning job, you will see a page with details about your fine-tuned model. You can find the status and more information about your fine-tuned model on the **Fine-tuning** page in Azure AI Foundry portal.

Your job might be queued behind other jobs on the system. Training your model can take minutes or hours depending on the model and dataset size.

## Checkpoints

When each training epoch completes a checkpoint is generated. A checkpoint is a fully functional version of a model which can both be deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, as they may provide snapshots prior to overfitting. When a fine-tuning job completes you will have the three most recent versions of the model available to deploy.

## Analyze your custom model

Azure OpenAI attaches a result file named _results.csv_ to each fine-tuning job after it completes. You can use the result file to analyze the training and validation performance of your custom model. The file ID for the result file is listed for each custom model in the **Result file Id** column on the **Models** pane for Azure AI Foundry portal. You can use the file ID to identify and download the result file from the **Data files** pane of Azure AI Foundry portal.

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

Look for your loss to decrease over time, and your accuracy to increase. If you see a divergence between your training and validation data, that may indicate that you are overfitting. Try training with fewer epochs, or a smaller learning rate multiplier. 

## Deploy a fine-tuned model

Once you're satisified with the metrics from your fine-tuning job, or you just want to move onto inference, you must deploy the model.

If you're deploying for further validation, consider deploying for [testing](../how-to/fine-tune-test.md?tabs=portal) using a Developer deployment.

If you're ready to deploy for production or have particular data residency needs, follow our [deployment guide](../how-to/fine-tuning-deploy.md?tabs=portal).

### Use a deployed fine-tuned model

After your fine-tuned model deploys, you can use it like any other deployed model. You can use the **Playground** in [Azure AI Foundry](https://ai.azure.com) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the [system message that you use to guide your fine-tuned model](../concepts/system-message.md) (whether it's deployed or available for testing in the playground) must be the same as the system message you used for training. If you use a different system message, the model might not perform as expected.

## Continuous fine-tuning

Once you have created a fine-tuned model you may wish to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples.

To perform fine-tuning on a model that you have previously fine-tuned you would use the same process as described in [creating a fine-tuned model](#creating-a-fine-tuned-model) but instead of specifying the name of a generic base model you would specify your already fine-tuned model. A custom fine-tuned model would look like `gpt-4o-2024-08-06.ft-d93dda6110004b4da3472d96f4dd4777-ft`

:::image type="content" source="../media/fine-tuning/studio-continuous.png" alt-text="Screenshot of the Create a custom model UI with a fine-tuned model highlighted." lightbox="../media/fine-tuning/studio-continuous.png":::

## Clean up your deployments, custom models, and training files

When you're done with your custom model, you can delete the deployment and model. You can also delete the training and validation files you uploaded to the service, if needed.

### Delete your model deployment

[!INCLUDE [Fine-tuning deletion](fine-tune.md)]

You can delete the deployment for your custom model on the **Deployments** pane in Azure AI Foundry portal. Select the deployment to delete, and then select **Delete** to delete the deployment.

### Delete your custom model

You can delete a custom model on the **Models** pane in Azure AI Foundry portal. Select the custom model to delete from the **Customized models** tab, and then select **Delete** to delete the custom model.

> [!NOTE]
> You can't delete a custom model if it has an existing deployment. You must first [delete your model deployment](#delete-your-model-deployment) before you can delete your custom model.

### Delete your training files

You can optionally delete training and validation files that you uploaded for training, and result files generated during training, on the **Management** > **Data + indexes** pane in Azure AI Foundry portal. Select the file to delete, and then select **Delete** to delete the file.

