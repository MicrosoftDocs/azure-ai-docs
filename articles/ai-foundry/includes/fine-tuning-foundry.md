## Prerequisites

- Read the [guide on when to use Foundry fine-tuning](../openai/concepts/fine-tuning-considerations.md).
- You need an Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- You need a Foundry project resource. To create one, sign in to the [Foundry portal](https://ai.azure.com).
- Fine-tuning requires the **Azure AI Owner** role. While Azure AI Users may train (fine tune) models, only AI Owners may deploy them.
- If you don't already have access to view quotas and deploy models in the Foundry portal, you need [more permissions](../openai/how-to/role-based-access-control.md).

### Supported models

To check which regions currently support fine-tuning, consult the [article about models](../foundry-models/concepts/models-sold-directly-by-azure.md#fine-tuning-models).

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.

## Prepare your data

Your training and validation datasets consist of input and output examples for how you want the model to perform.

The training and validation data that you use *must* be formatted as a JSON Lines (JSONL) document. It must also be formatted in the conversational format that the [Chat Completions](../openai/how-to/chatgpt.md) API uses.

In addition to the JSONL format, training and validation data files must be encoded in UTF-8 and include a byte-order mark (BOM). Each file must be less than 512 MB in size.

We recommend that you use the instructions and prompts that you found worked best in every training example. This approach helps you get the best results, especially if you have fewer than a hundred examples.

If you don't have an existing dataset prepared, you can use the [data generation](../default/fine-tuning/data-generation.md) capabilities to create a new one.

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

### Dataset size considerations

The more training examples you have, the better. Fine-tuning jobs won't proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. A best practice for successful fine-tuning is to provide hundreds, if not thousands, of training examples. We recommend that you start with 50 well-crafted examples.

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind that low-quality examples can negatively affect performance. If you train the model on a large amount of internal data without first pruning the dataset for only the highest-quality examples, your model might perform worse than expected.

## Create your fine-tuned model

To fine-tune a model in an existing Foundry project, follow these steps:

1. Sign in to [Foundry](https://ai.azure.com/) and select your project. If you don't have a project already, first [create a project](../how-to/create-projects.md).

1. Go to the **Build** > **Fine-tune** page, and then select the **Fine-tune** button at the upper right.

1. You should now see the **Fine-tune a model** experience for creating a new fine-tuning job. Use the following sections to help with configuring the job, and then select **Submit** to start training your new fine-tuned model.

### Base model selection

The project region might limit the available models. Your choice of model influences both the performance and the cost of your model.

You can also select a previously fine-tuned model.

### Customization method

The supported customization methods depend on the selected model:

- **Supervised fine-tuning (SFT)**: Trains the model on labeled input/output pairs. Best for most scenarios, including task specialization.

- **Direct preference optimization (DPO)**: Aligns the model with human-preferred responses. Ideal for improving response quality.

- **Reinforcement fine-tuning (RFT)**: Uses reward signals from model graders to optimize complex behaviors.

> [!NOTE]
> The rest of this article covers steps for the SFT method. For instructions specific to other customization methods, see the [guide for DPO](../openai/how-to/fine-tuning-direct-preference-optimization.md) and the [guide for RFT](../openai/how-to/reinforcement-fine-tuning.md).

### Training type

Select the training tier based on your use case and budget:

- **Standard**: Training occurs in the current Foundry resource's region and provides guarantees for data residency. Ideal for workloads where data must remain in a specific region.

- **Global**: Provides more affordable pricing compared to Standard by using capacity beyond your current region. Data and weights are copied to the region where training occurs. Ideal if data residency is not a restriction and you want faster queue times.

- **Developer (preview)**: Provides significant cost savings by using idle capacity for training. There are no latency or SLA guarantees, so jobs in this tier might be automatically preempted and resumed later. There are no guarantees for data residency either. Ideal for experimentation and price-sensitive workloads.

### Training and validation data

If you have existing datasets in the Foundry project, select **Existing dataset** for **Data source**, and then select your dataset.

To upload newly prepared datasets, select **Upload new dataset** for **Data source**, and then upload your JSONL file.

After you select or upload your data files, validation checks automatically occur to confirm that the files are formatted as JSONL, are encoded in UTF-8 with a BOM, and are less than 512 MB in size.

### Optional parameters

#### Suffix

We recommend that you provide a **Suffix** value to make it easier to distinguish between different iterations of your fine-tuned model. A suffix takes a string of up to 18 characters and is used in naming the resulting fine-tuned model.

#### Seed

A seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If you don't specify a seed, one is randomly generated for you.

#### Hyperparameters

You can manually configure hyperparameters for your fine-tuning job or leave them as defaults.

The following hyperparameters are available:

|Name| Type| Description|
|---|---|---|
|`batch_size` |Integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets.<br><br> The default value and the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. When the value is set to `-1`, the batch size is calculated as 0.2% of examples in the training set. The maximum is `256`. |
| `learning_rate_multiplier` | Number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training, multiplied by this value.<br><br> Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range of `0.02` to `0.2` to see what produces the best results. A smaller learning rate can be useful to avoid overfitting. |
|`n_epochs` | Integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. If the value is set to `-1`, the number of epochs is determined dynamically based on the input data. |

#### Automatic deployment

> [!IMPROTANT]
> For automatic deployment, you need to be assigned as `Azure AI owner` role or any role with `Microsfot.CognitiveServices/accounts/deployments/write" action.

To save time, you can enable automatic deployment for your resulting model. If training finishes successfully, the model is deployed according to the selected deployment type. The deployment name is based on the unique name generated for your custom model and the optional suffix that you might have provided earlier.

Automatic deployment is supported only for OpenAI models.

## Monitor and analyze the results

After you submit your fine-tuning job, a table view lists all of your fine-tuning job submissions. To see more information about the individual results, open the **Job details** page.

Your job might be queued behind other jobs in the system. Training your model can take minutes to hours, depending on the model and the dataset size.

### Metrics

You can monitor the following metrics by going to the **Monitor** pivot:

- `train_loss`: The loss for the training batch. Each training step on the x-axis represents a single pass, forward and backward, on a batch of training data.
- `full_valid_loss`: The validation loss calculated at the end of each epoch. When training goes well, loss should decrease.
- `train_mean_token_accuracy`: The percentage of tokens in the training batch that the model correctly predicted.

  For example, if the batch size is set to `3` and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to `0.83` (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`.
- `full_valid_mean_token_accuracy`: The valid mean token accuracy calculated at the end of each epoch. When training is going well, token accuracy should increase.

Look for your loss to decrease over time, and your accuracy to increase. If your training and validation data diverge, you might be overfitting. Try training with fewer epochs or a smaller learning-rate multiplier.

### Checkpoints

When each training epoch finishes, a checkpoint is generated. You can view checkpoints by going to the **Checkpoints** pivot.

A checkpoint is a fully functional version of a model that can be both deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, because they might provide snapshots prior to overfitting. When a fine-tuning job finishes, you have the three most recent versions of the model available to deploy. You can copy checkpoints between resources and subscriptions through the REST API.

> [!NOTE]
> During the training, you can view the metrics and pause the job as needed. Pausing can be useful if metrics aren't converging or if you feel that the model isn't learning at the right pace. When you pause a training job, a deployable checkpoint is created after safety evaluations are complete. This checkpoint is available for you to deploy and use for inference, or you can resume the job to complete it.
>
> The pause operation is applicable only for jobs that are trained for at least one step and are in a **Running** state. Pausing is supported only for OpenAI models.

## Deploy the fine-tuned model

> [!IMPROTANT]
> To deploy models, you need to be assigned as `Azure AI owner` role or any role with `Microsfot.CognitiveServices/accounts/deployments/write" action.

When you're satisfied with the metrics from your fine-tuning job, you can deploy the model by selecting the **Deploy** button on the details page and then configuring your deployment settings.

For more information, see the [fine-tuning deployment guide](../openai/how-to/fine-tuning-deploy.md?tabs=portal).

## Use a deployed fine-tuned model

After you deploy your fine-tuned model, you can use it like any other deployed model. You can use the playground in [Foundry](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the system message that you use to guide your fine-tuned model (whether it's deployed or available for testing in the playground) must be the same as the system message that you used for training. If you use a different system message, the model might not perform as expected.

## Perform continuous fine-tuning

After you create a fine-tuned model, you might want to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples.

To perform fine-tuning on a model that you previously fine-tuned, you use the same process described in [Create your fine-tuned model](#create-your-fine-tuned-model). But instead of specifying the name of a generic base model, you specify your already fine-tuned model. A custom fine-tuned model looks like `gpt-4o-2024-08-06.ft-d93dda6110004b4da3472d96f4dd4777-ft`.

Continuous fine-tuning is supported only for OpenAI models.

## Clean up your resources

When you no longer need your fine-tuned model, you can delete the deployment and model. You can also delete the training and validation files that you uploaded to the service, if necessary.

### Delete your fine-tuned model deployment

[!INCLUDE [Fine-tuning deletion](../openai/includes/fine-tune.md)]

You can delete the deployment for your fine-tuned model on the **Build** > **Models** page in the Foundry portal.

### Delete your fine-tuned model

You can delete a fine-tuned model on the **Fine-tuning** page in the Foundry portal. Select the fine-tuned model to delete, and then select **Delete**.

> [!NOTE]
> You can't delete a fine-tuned model if it has an existing deployment. You must [delete your model deployment](#delete-your-fine-tuned-model-deployment) before you can delete your fine-tuned model.
