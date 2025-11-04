## Prerequisites

- Read the [When to use AI Foundry fine-tuning guide](../openai/concepts/fine-tuning-considerations.md).
- An Azure subscription. <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An AI Foundry project resource. Sign in to the [AI Foundry portal](https://ai.azure.com) to create one.
- Fine-tuning access requires the **Azure AI User** role.
- If you do not already have access to view quota, and deploy models in Azure AI Foundry portal you will require [additional permissions](../openai/how-to/role-based-access-control.md).


## Prepare your data

Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document and must be formatted in the conversational format that is used by the [Chat completions](../openai/how-to/chatgpt.md) API.

It's generally recommended to use the instructions and prompts that you found worked best in every training example. This will help you get the best results, especially if you have fewer than a hundred examples.

If you don't have an existing dataset prepared, you can leverage the [data generation](../default/fine-tuning/data-generation.md) capabilities create a new one.

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
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital/major city of France?"}, {"role": "assistant", "content": "Paris", "weight": 0}, {"role": "user", "content": "Can you be more sarcastic?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already.", "weight": 1}]}
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

To fine-tune an model in an existing Azure AI Foundry project, follow these steps:

1. Sign in to [Azure AI Foundry](https://ai.azure.com/) and select your project. If you don't have a project already, first [create a project](../how-to/create-projects.md).

1. From the top navigation, select **Build** followed by **Fine-tune** on the left navigation.

1. Select the **Fine-tune** button on the top right of the page. You should now see the **Fine-tune a model** experience.

### Base model selection

Available models may be limited by the project region. Your choice of model will influence both the performance and the cost of your model. 

When selecting the model, you may also select a previously fine-tuned model.

### Customization method

Different customization methods may be supported based on the selected model:

- **Supervised (SFT)**: Trains the model on labeled input-output pairs. Best for most scenarios, including task specialization. This is supported by all non-reasoning models.

- **Direct Preference Optimization (DPO)**: Aligns model with human-preferred responses. Ideal for improving response quality. This is supported only by GPT-4o.

- **Reinforcement (RFT)**: Uses reward signals from model graders to optimize complex behaviors. This is supported only by GPT-5 and o4-mini.

### Training type

Select the training tier based on your use case and budget.

- **Standard**: Training occurs in the current Foundry resource's region, providing data residency guarantees. Ideal for workloads where data must remain in a specific region.

- **Global**: Provides more affordable pricing compared to Standard by leverage capacity beyond your current region. Data and weights are copied to the region where training occurs. Ideal if data residency is not a restriction and you want faster queue times.

- **Developer (preview)**: Provides significant cost savings by leveraging idle capacity for training. There are no latency or SLA guarantees, so jobs in this tier may be automatically preempted and resumed later. There are no data residency guarantees either. Ideal for experimentation and price-sensitive workloads.

### Training and validation data

If you have an existing datasets in the Foundry project, choose **Existing dataset** for the **data source** and then select your dataset.

To upload a newly prepared datasets, choose **Upload new dataset** for the **data source** and then upload your *.jsonl* file.

On your data files are selected or uploaded, validation check will automatically occur to confirm they are in the right format.

> [!NOTE]
> Training data files must be formatted as JSONL files, encoded in UTF-8 with a byte-order mark (BOM). The file must be less than 512 MB in size.

### Optional parameters 

#### Suffix

It is recommended to fill in the **suffix** field to make it easier to distinguish between different iterations of your fine-tuned model. A suffix takes a string of up to 18 characters and is used when naming the resulting fine-tuned model.

#### Seed

Controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be randomly generated for you.

#### Hyperparameters

Hyperparameters for your fine-tuning job can be manually configured or left as defaults.

The following hyper parameters are available:

|**Name**| **Type**| **Description**|
|---|---|---|
|`batch_size` |integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. A larger batch size means that model parameters are updated less frequently, but with lower variance. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256. |
| `learning_rate_multiplier` | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. A smaller learning rate may be useful to avoid overfitting. |
|`n_epochs` | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. If set to -1, the number of epochs is determined dynamically based on the input data. |
|`seed` | integer | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you. |
| `Beta`| integer | Temperature parameter for the dpo loss, typically in the range 0.1 to 0.5. This controls how much attention we pay to the reference model. The smaller the beta, the more we allow the model to drift away from the reference model. As beta gets smaller the more, we ignore the reference model.  |

#### Enable auto-deployment

To save time, you can enable auto-deployment for your resulting model. If training completes successfully, the model will be deployed using the selected deployment type. The deployment will be named based on the unique name generated for your custom model and the optional suffix you may have provided earlier.
