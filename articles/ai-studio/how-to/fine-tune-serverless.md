---
title: Fine-tune models using serverless APIs in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to fine-tune models deployed via serverless APIs in Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/31/2025
ms.reviewer: rasavage
reviewer: RSavage2
ms.author: ssalgado
author: ssalgadodev
ms.custom: references_regions
---

# Fine-tune models using serverless APIs in Azure AI Foundry

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

Azure AI Foundry lets you tailor large language models to your personal datasets by using a process known as *fine-tuning*. 

Fine-tuning provides significant value by enabling customization and optimization for specific tasks and applications. It leads to improved performance, cost efficiency, reduced latency, and tailored outputs.

In this article, you learn how to fine-tune models that are deployed via serverless APIs in [Azure AI Foundry](https://ai.azure.com).


## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- Access to the [Azure portal](https://portal.azure.com).

- An [Azure AI Foundry project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).


## Find models with fine-tuning support

The AI Foundry model catalog offers fine-tuning support for multiple types of models, including chat completions and text generation. For a list of models that support fine-tuning and the Azure regions of support for fine-tuning, see [region availability for models in serverless API endpoints.](deploy-models-serverless-availability.md).


You can also go to the Azure AI Foundry portal to view all models that contain fine-tuning support:

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. If you're not already in your project, select it. 
1. Navigate to the model catalog.
1. Select the **Fine-tuning tasks** filter. 
    
    :::image type="content" source="../media/how-to/fine-tune/fine-tune-filters.png" alt-text="Screenshot of model catalog finetuning filter options." lightbox="../media/how-to/fine-tune/fine-tune-filters.png":::

1. Select **All** or select a specific task. 



## Verify registration of subscription provider

Verify the subscription is registered to the `Microsoft.Network` resource provider.
1. Sign in to the [Azure portal](https://portal.azure.com).
1. Select **Subscriptions** from the left menu.
1. Select the subscription you want to use.
1. Select **Settings** > **Resource providers** from the left menu.
1. Confirm that **Microsoft.Network** is in the list of resource providers. Otherwise add it.

    

### Prepare data for fine-tuning

Prepare your training and validation data to fine-tune your model. Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a balanced and diverse dataset by maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations. These actions ultimately lead to more accurate and balanced model responses.

> [!TIP]
> Different model types require a different format of training data.

# [Chat completion](#tab/chat-completion)

### Example file format

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

```json
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```

# [Text generation](#tab/text-generation)

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document in which each line represents a single prompt-completion pair.

### Example file format

```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

Here are some example datasets on Hugging Face that you can use to fine-tune your model:
- [dair-ai/emotion](https://huggingface.co/datasets/dair-ai/emotion)

    :::image type="content" source="../media/how-to/fine-tune/dataset-dair-ai-emotion.png" alt-text="Screenshot of example emotion data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-dair-ai-emotion.png":::

- [SetFit/mrpc](https://huggingface.co/datasets/SetFit/mrpc)

    :::image type="content" source="../media/how-to/fine-tune/dataset-setfit-mrpc.png" alt-text="Screenshot of example Microsoft Research Paraphrase Corpus (MRPC) data on Hugging Face." lightbox="../media/how-to/fine-tune/dataset-setfit-mrpc.png":::

Single text classification requires the training data to include at least two fields such as `text1` and `label`. Text pair classification requires the training data to include at least three fields such as `text1`, `text2`, and `label`. 

The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

---

## Fine-tune a model

1. Choose the model you want to fine-tune from the Azure AI Foundry [model catalog](https://ai.azure.com/explore/models). 

1. On the model's **Details** page, select **fine-tune**. Some foundation models support both __Serverless API__ and __Managed compute__, while others support one or the other.

1. If you're presented the options for __Serverless API__ and __Managed compute__, select __Serverless API__ for fine-tuning. This action opens up a wizard that shows information about __pay-as-you-go__ fine-tuning for your model.

    > [!NOTE]
    > To use a serverless API to fine-tune your model, your project must belong to an available region. Each model has specific region availability. These regions are listed in the fine-tune wizard that opens up. You can also check [region availability](deploy-models-serverless-availability.md) for your chosen model.

1. Select the **Pricing and terms** tab to learn about pricing for the selected model.
1. If you're using a model that's offered through Azure Marketplace, select the link to **Azure Marketplace Terms** from the __Overview__ tab to learn more about the terms of use.

    1. If it's your first time fine-tuning the model (for example, Mistral-large-2407) in the project, you must subscribe your project for the particular offering from Azure AI Foundry. This step requires that your account has the Azure subscription permissions and resource group permissions listed in the prerequisites. Each project has its own subscription to the particular Azure AI Studio offering, which allows you to control and monitor spending. Select **Subscribe and fine-tune**.

    > [!NOTE]
    > Subscribing a project to a particular Azure AI Foundry offering requires that your account has **Contributor** or **Owner** access at the subscription level where the project is created. Alternatively, your user account can be assigned a custom role that has the Azure subscription permissions and resource group permissions listed in the [prerequisites](#prerequisites).

    2. Once you sign up the project for the particular Azure AI Foundry offering, subsequent fine-tuning of the _same_ offering in the _same_ project don't require subscribing again. Therefore, you don't need to have the subscription-level permissions for subsequent fine-tune jobs. If this scenario applies to you, select **Continue to fine-tune**.

1. If you're using a Microsoft model (for example, Phi-3.5-mini-instruct),  you don't  create an Azure Marketplace subscription. Select __Fine-tune__.

1. Enter a name for your fine-tuned model and the optional tags and description.
1. Select training data to fine-tune your model. See [prepare data for fine-tuning](#prepare-data-for-fine-tuning) for more information.

    > [!NOTE]
    > If you have your training/validation files in a credential-less datastore, you need to allow workspace managed identity access to your datastore in order to proceed with Serverless API fine-tuning with a credential-less storage. On the __Datastore__ page, after selecting __Update authentication__, select the option to use workspace managed identity. 
    
    ![Use workspace managed identity for data preview and profiling in Azure Machine Learning Foundry.](../media/how-to/fine-tune/phi-3/credentials.png)

1. Select validation data.
1. Specify (optional) task parameters. Task parameters are an optional step and an advanced option. Tuning hyperparameters is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. You can choose to keep he default settings or customize parameters like epochs or learning rate.

    - __Batch size multiplier__: The batch size to use for training. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256.
    - __Learning rate__: The fine-tuning learning rate is the original learning rate used for pretraining multiplied by this multiplier. We recommend experimenting with values between 0.5 and 2. Empirically, we've found that larger learning rates often perform better with larger batch sizes. Must be between 0.0 and 5.0.
    - __Epochs__: Number of training epochs. An epoch refers to one full cycle through the data set.

1. Review your selections and select __Submit__ to train your model.

Once your model is fine-tuned, you can deploy it and use it in your own application, in the playground, or in prompt flow. For more information on how to use deployed models, see [How to use Mistral premium chat models](./deploy-models-mistral.md).

---
## Supported Enterprise Scenarios for Finetuning

Several enterprise scenarios are supported for MaaS finetuning. The table below outlines the supported configurations for user storage networking and authentication to ensure smooth operation within enterprise scenarios:

**Note:**  
- Data connections auth can be changed via AI Studio by clicking on the datastore connection which your dataset is stored in, and navigating to the "Access details" > "Authentication Method" setting.  
- Storage auth can be changed in Azure Storage > "Settings" > "Configurations" page > "Allow storage account key access"  
- Storage networking can be changed in Azure Storage > "Networking" page

| **Storage Networking**                                       | **Storage Auth**               | **Data Connection Auth**               | **Support**           |
| ------------------------------------------------------------ | ------------------------------ | --------------------------------- | ----------------------- |
| Public Network Access = Enabled                               | Account key enabled            | SAS/Account Key                  | Yes, UX and SDK         |
| Public Network Access = Enabled                               | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK <br><br> *Note:* for UX, you may need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token |                               |                                   |                         |
| Enabled from selected virtual networks and IP addresses      | Account key enabled            | Account key                      | Yes, UX and SDK <br><br> *Note:*: for UX, the IP of the compute running the browser must be in the selected list        |
| Enabled from selected virtual networks and IP addresses      | Account key enabled            | SAS                               | Yes, UX and SDK  <br><br> *Note:*: for UX, the IP of the compute running the browser must be in the selected list       |
| Enabled from selected virtual networks and IP addresses      | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK. <br><br>*Note:* for UX, you may need to add Storage Blob Data Reader or Storage Blob Data Contributor for your user ID on the storage account, or change the connection's authentication to use Account key/SAS token. Also ensure the IP of the compute running the browser must be in the selected list |                               |                                   |                         |
| Public Network Access = Disabled                              | Account key enabled            | SAS/Account Key                  | Yes, UX and SDK. <br><br> *Note:*  for UX data upload and submission to work, the workspace _needs to be accessed from within the Vnet_ that has appropriate access to the storage           |
| Public Network Access = Disabled                              | Account key disabled           | Entra-Based Auth (Credentialless) | Yes, UX and SDK. <br><br> *Note:* for UX data upload and submission to work, the workspace _needs to be accessed from within the Vnet_ that has appropriate access to the storage                |


The scenarios above should work in a Managed Vnet workspace as well. See setup of Managed Vnet AI Studio hub here: [How to configure a managed network for Azure AI Foundry hubs](./configure-managed-network.md)

Customer-Managed Keys (CMKs) is **not** a supported enterprise scenario with MaaS finetuning.

Issues finetuning with unique network setups on the workspace and storage usually points to a networking setup issue.

---

## Clean up your fine-tuned models 

You can delete a fine-tuned model from the fine-tuning model list in [Azure AI Foundry](https://ai.azure.com) or from the model details page. To delete the fine-tuned model from the Fine-tuning page,

1. Select __Fine-tuning__ from the left navigation in your Azure AI Foundry project.
1. Select the __Delete__ button to delete the fine-tuned model.

>[!NOTE]
> You can't delete a custom model if it has an existing deployment. You must first delete your model deployment before you delete your custom model.

## Cost and quota considerations for models deployed as serverless API endpoints

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

#### Cost for Microsoft models

You can find the pricing information on the __Pricing and terms__ tab of the deployment wizard when deploying Microsoft models (such as Phi-3 models) as serverless API endpoints.

#### Cost for non-Microsoft models

Non-Microsoft models deployed as serverless API endpoints are offered through Azure Marketplace and integrated with Azure AI Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning these models.

Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

:::image type="content" source="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png":::

## Sample Notebook

You can use this [sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/chat-completion/chat_completion_with_model_as_service.ipynb)  to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using the Samsum dataset. The training data utilized is the ultrachat_200k dataset, which is divided into four splits suitable for supervised fine-tuning (sft) and generation ranking (gen). The notebook employs the available Azure AI models for the chat-completion task (If you would like to use a different model than what's used in the notebook, you can replace the model name). The notebook includes setting up prerequisites, selecting a model to fine-tune, creating training and validation datasets, configuring and submitting the fine-tuning job, and finally, creating a serverless deployment using the fine-tuned model for sample inference.

## Sample CLI

Additionally, you can use this sample CLI to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using a dataset. 

```yaml
type: finetuning

name: "Phi-3-mini-4k-instruct-with-amlcompute"
experiment_name: "Phi-3-mini-4k-instruct-finetuning-experiment"
display_name: "Phi-3-mini-4k-instruct-display-name"
task: chat_completion
model_provider: custom
model: 
  path: "azureml://registries/azureml/models/Phi-3-mini-4k-instruct/versions/14"
  type: mlflow_model
training_data: train.jsonl
validation_data:
  path: validation.jsonl
  type: uri_file
hyperparameters:
  num_train_epochs: "1"
  per_device_train_batch_size: "1"
  learning_rate: "0.00002"
properties:
  my_property: "my_value"
tags:
  foo_tag: "bar"
outputs:
  registered_model:
    name: "Phi-3-mini-4k-instruct-finetuned-model"
    type: mlflow_model 
```

The training data used is the same as demonstrated in the SDK notebook. The CLI employs the available Azure AI models for the chat-completion task. If you prefer to use a different model than the one in the CLI sample, you can update the arguments, such as 'model path,' accordingly

## Content filtering

Models deployed as a service with pay-as-you-go billing are protected by Azure AI Content Safety. When deployed to real-time endpoints, you can opt out of this capability. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](../concepts/content-filtering.md).


## Next steps
- [What is Azure AI Foundry?](../what-is-ai-studio.md)
- [Learn more about deploying Mistral models](./deploy-models-mistral.md)
- [Azure AI FAQ article](../faq.yml)
