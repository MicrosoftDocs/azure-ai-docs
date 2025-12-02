## Prerequisites

- Read the [When to use Foundry fine-tuning guide](../openai/concepts/fine-tuning-considerations.md).
- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project resource. Sign in to the [Foundry portal](https://ai.azure.com) to create one.
- Fine-tuning access requires the **Azure AI User** role.
- If you do not already have access to view quota, and deploy models in Microsoft Foundry portal you require [more permissions](../openai/how-to/role-based-access-control.md).

### Supported models

Consult the [models page](../foundry-models/concepts/models-sold-directly-by-azure.md#fine-tuning-models) to check which regions currently support fine-tuning.

Or you can fine tune a previously fine-tuned model, formatted as base-model.ft-{jobid}.

## Prepare your data

Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document and must be formatted in the conversational format that is used by the [Chat completions](../openai/how-to/chatgpt.md) API.

It's recommended to use the instructions and prompts that you found worked best in every training example. This helps you get the best results, especially if you have fewer than a hundred examples.

If you don't have an existing dataset prepared, you can use the [data generation](../default/fine-tuning/data-generation.md) capabilities create a new one.

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
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the biggest city in France?"}, {"role": "assistant", "content": "Paris", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", "weight": 1}]}
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

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs worse than expected.

## Create your fine-tuned model

To fine-tune a model in an existing Foundry project, follow these steps:

1. Sign in to [Foundry](https://ai.azure.com/) and select your project. If you don't have a project already, first [create a project](../how-to/create-projects.md).

1. Navigate to **Build > Fine-tune** page and select the **Fine-tune** button at the top right.

1. You should now see the **Fine-tune a model** experience for creating a new fine-tuning job. Use the sections below to help with configuring the job and select **Submit** to start training your new fine-tuned model.

### Base model selection

Available models might be limited by the project region. Your choice of model influences both the performance and the cost of your model. 

When selecting the model, you can also select a previously fine-tuned model.

### Customization method

Different customization methods may be supported based on the selected model:

- **Supervised (SFT)**: Trains the model on labeled input-output pairs. Best for most scenarios, including task specialization.

- **Direct Preference Optimization (DPO)**: Aligns model with human-preferred responses. Ideal for improving response quality. 

- **Reinforcement (RFT)**: Uses reward signals from model graders to optimize complex behaviors. 

> [!NOTE]
> This rest of this document will cover steps for supervised fine-tuning method. For instructions specific to other customization methods, see articles for [DPO](../openai/how-to/fine-tuning-direct-preference-optimization.md) or [RFT](../openai/how-to/reinforcement-fine-tuning.md).


### Training type

Select the training tier based on your use case and budget.

- **Standard**: Training occurs in the current Foundry resource's region, providing data residency guarantees. Ideal for workloads where data must remain in a specific region.

- **Global**: Provides more affordable pricing compared to Standard by leveraging capacity beyond your current region. Data and weights are copied to the region where training occurs. Ideal if data residency is not a restriction and you want faster queue times.

- **Developer (preview)**: Provides significant cost savings by leveraging idle capacity for training. There are no latency or SLA guarantees, so jobs in this tier may be automatically preempted and resumed later. There are no data residency guarantees either. Ideal for experimentation and price-sensitive workloads.

```python
import openai
from openai import AzureOpenAI

base_uri = "https://<ACCOUNT-NAME>.services.ai.azure.com"
api_key = "<API-KEY>"
api_version = "2025-04-01-preview"
client = AzureOpenAI(
azure_endpoint=base_uri,
api_key=api_key,
api_version=api_version
)
try:
    client.fine_tuning.jobs.create(
    model="gpt-4.1-mini",
    training_file="<FILE-ID>",
    extra_body={"trainingType": "developerTier"}
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__) # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
    print(e.body)
``` 

### Training and validation data

If you have existing datasets in the Foundry project, choose **Existing dataset** for the **data source** and then select your dataset.

To upload newly prepared datasets, choose **Upload new dataset** for the **data source** and then upload your JSONL file.

Once your data files are selected or uploaded, validation checks automatically occur to confirm they are in the right format.

> [!NOTE]
> Training data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size. While 10 is the minimum number of required samples in a dataset, at least 100s of training samples are recommended to teach the model a new skill.

### Optional parameters 

#### Suffix

It is recommended to fill in the **suffix** field to make it easier to distinguish between different iterations of your fine-tuned model. A suffix takes a string of up to 18 characters and is used when naming the resulting fine-tuned model.

#### Seed

Controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results but might differ in rare cases. If a seed isn't specified, one is randomly generated for you.

#### Hyperparameters

Hyperparameters for your fine-tuning job can be manually configured or left as defaults.

The following hyperparameters are available:

|**Name**| **Type**| **Description**|
|---|---|---|
|`batch_size` |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we find that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256. |
| `learning_rate_multiplier` | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate might be useful to avoid overfitting. |
|`n_epochs` | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. If set to -1, the number of epochs is determined dynamically based on the input data. |

#### Enable auto-deployment

To save time, you can enable auto-deployment for your resulting model. If training finishes successfully, the model is deployed by using the selected deployment type. The deployment name is based on the unique name generated for your custom model and the optional suffix you might have provided earlier.

## Monitor and analyze the results

After you submit your fine-tuning job, you will see a table view listing all of your fine-tuning job submissions. Click into the **job details** page to see more information about the individual results.

Your job might be queued behind other jobs on the system. Training your model can take minutes to hours depending on the model and dataset size.

### Metrics

You can monitor the following metrics by navigating to the **Monitor** pivot:

- **train_loss**: The loss for the training batch. Each training step on the x-axis represents a single pass, forward and backward, on a batch of training data.
- **full_valid_loss**: The validation loss calculated at the end of each epoch. When training goes well, loss should decrease.
- **train_mean_token_accuracy**: The percentage of tokens in the training batch correctly predicted by the model.<br>For example, if the batch size is set to 3 and your data contains completions `[[1, 2], [0, 5], [4, 2]]`, this value is set to 0.83 (5 of 6) if the model predicted `[[1, 1], [0, 5], [4, 2]]`.
- **full_valid_mean_token_accuracy**: The valid mean token accuracy calculated at the end of each epoch. When training is going well, token accuracy should increase.

Look for your loss to decrease over time, and your accuracy to increase. If you see a divergence between your training and validation data, that may indicate that you are overfitting. Try training with fewer epochs, or a smaller learning rate multiplier. 

### Checkpoints

When each training epoch completes a checkpoint is generated. Checkpoints can be viewed by navigating to the **Checkpoints** pivot.

A checkpoint is a fully functional version of a model which can both be deployed and used as the target model for subsequent fine-tuning jobs. Checkpoints can be particularly useful, as they may provide snapshots prior to overfitting. When a fine-tuning job completes you will have the three most recent versions of the model available to deploy. You can copy checkpoints between resources and subscriptions through REST API.

> [!NOTE]
> During the training you can view the metrics and pause the job as needed. Pausing can be useful, if metrics aren't converging or if you feel the model isn't learning at the right pace. Once the training job is paused, a deployable checkpoint will be created once safety evaluations are complete. This checkpoint available for you to deploy and use for inference or resume the job further to completion. Pause operation is only applicable for jobs which have been trained for at least one step and are in *Running* state.

## Deploy the fine-tuned model

Once you're satisfied with the metrics from your fine-tuning job, you can deploy the model by clicking on the **Deploy** button at the top right of the details page and configuring your deployment settings.

See the [fine-tune deployment guide](../openai/how-to/fine-tuning-deploy.md?tabs=portal) for more details.

### Use a deployed fine-tuned model

After your fine-tuned model deploys, you can use it like any other deployed model. You can use the **Playground** in [Foundry](https://ai.azure.com/?cid=learnDocs) to experiment with your new deployment. You can also use the REST API to call your fine-tuned model from your own application. You can even begin to use this new fine-tuned model in your prompt flow to build your generative AI application.

> [!NOTE]
> For chat models, the system message that you use to guide your fine-tuned model (whether it's deployed or available for testing in the playground) must be the same as the system message you used for training. If you use a different system message, the model might not perform as expected.

## Continuous fine-tuning

Once you have created a fine-tuned model you may wish to continue to refine the model over time through further fine-tuning. Continuous fine-tuning is the iterative process of selecting an already fine-tuned model as a base model and fine-tuning it further on new sets of training examples.

To perform fine-tuning on a model that you have previously fine-tuned you would use the same process as described in [creating a fine-tuned model](#creating-a-fine-tuned-model) but instead of specifying the name of a generic base model you would specify your already fine-tuned model. A custom fine-tuned model would look like `gpt-4o-2024-08-06.ft-d93dda6110004b4da3472d96f4dd4777-ft`.

## Clean up your resources

When you're done with your fine-tuned model, you can delete the deployment and model. You can also delete the training and validation files you uploaded to the service, if needed. 

### Delete your fine-tuned model deployment

[!INCLUDE [Fine-tuning deletion](../openai/includes/fine-tune.md)]

You can delete the deployment for your fine-tuned model on the **Build > Models** page in Foundry portal.

### Delete your fine-tuned model

You can delete a fine-tuned model on the **Fine-tuning** page in Foundry portal. Select the fine-tuned model to delete and then select **Delete** to delete the fine-tuned model.

> [!NOTE]
> You can't delete a fine-tuned model if it has an existing deployment. You must first [delete your model deployment](#delete-your-fine-tuned-model-deployment) before you can delete your fine-tuned model.
