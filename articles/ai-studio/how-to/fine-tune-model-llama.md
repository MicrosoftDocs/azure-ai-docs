---
title: Fine-tune Llama models in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to fine-tune Meta Llama models in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 7/23/2024
ms.reviewer: rasavage
reviewer: shubhirajMsft
ms.author: ssalgado
author: ssalgadodev
ms.custom: references_regions, build-2024
---

# Fine-tune Meta Llama models in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Azure AI Foundry lets you tailor large language models to your personal datasets by using a process known as *fine-tuning*. 

Fine-tuning provides significant value by enabling customization and optimization for specific tasks and applications. It leads to improved performance, cost efficiency, reduced latency, and tailored outputs.

In this article, you learn how to fine-tune Meta Llama models in [Azure AI Foundry](https://ai.azure.com).

The [Meta Llama family of large language models (LLMs)](./deploy-models-llama.md) is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. The model family also includes fine-tuned versions optimized for dialogue use cases with Reinforcement Learning from Human Feedback (RLHF), called Llama-Instruct.

[!INCLUDE [models-preview](../includes/models-preview.md)]

## Models
# [Meta Llama 3.1](#tab/llama-three)

The following models are available in Azure Marketplace for Llama 3.1 when fine-tuning as a service with pay-as-you-go billing:

- `Meta-Llama-3.1-70B-Instruct` (preview)
- `Meta-LLama-3.1-8b-Instruct` (preview)
  
Fine-tuning of Llama 3.1 models is currently supported in projects located in West US 3.

> [!IMPORTANT]
> At this time we are not able to do fine-tuning for Llama 3.1 with sequence length of 128K. 

# [Meta Llama 2](#tab/llama-two)

The following models are available in Azure Marketplace for Llama 2 when fine-tuning as a service with pay-as-you-go billing:

- `Meta Llama-2-70b` (preview)
- `Meta Llama-2-13b` (preview)
- `Meta Llama-2-7b` (preview)

Fine-tuning of Llama 2 models is currently supported in projects located in West US 3.

---

## Prerequisites

# [Meta Llama 3.1](#tab/llama-three)


 An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- An [Azure AI Foundry hub](../how-to/create-azure-ai-resource.md).

    > [!IMPORTANT]
    > For Meta Llama 3.1 models, the pay-as-you-go model fine-tune offering is only available with hubs created in **West US 3** regions.

- An [Azure AI Foundry project](../how-to/create-projects.md) in Azure AI Foundry portal.
- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

    - On the Azure subscription—to subscribe the AI Foundry project to the Azure Marketplace offering, once for each project, per offering:
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
      - `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.SaaS/register/action`
 
    - On the resource group—to create and use the SaaS resource:
      - `Microsoft.SaaS/resources/read`
      - `Microsoft.SaaS/resources/write`
 
    - On the AI Foundry project—to deploy endpoints (the Azure AI Developer role contains these permissions already):
      - `Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*`  
      - `Microsoft.MachineLearningServices/workspaces/serverlessEndpoints/*`

    For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).


# [Meta Llama 2](#tab/llama-two)

 An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- An [AI Foundry hub](../how-to/create-azure-ai-resource.md).

    > [!IMPORTANT]
    > For Meta Llama 2 models, the pay-as-you-go model fine-tune offering is only available with hubs created in the **West US 3** region.

- An [AI Foundry project](../how-to/create-projects.md) in Azure AI Foundry portal.
- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

    - On the Azure subscription—to subscribe the AI Foundry project to the Azure Marketplace offering, once for each project, per offering:
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
      - `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.SaaS/register/action`
 
    - On the resource group—to create and use the SaaS resource:
      - `Microsoft.SaaS/resources/read`
      - `Microsoft.SaaS/resources/write`
 
    - On the AI Foundry project—to deploy endpoints (the Azure AI Developer role contains these permissions already):
      - `Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*`  
      - `Microsoft.MachineLearningServices/workspaces/serverlessEndpoints/*`

    For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).
---

### Subscription provider registration

Verify the subscription is registered to the `Microsoft.Network` resource provider.
1. Sign in to the [Azure portal](https://portal.azure.com).
1. Select **Subscriptions** from the left menu.
1. Select the subscription you want to use.
1. Select **Settings** > **Resource providers** from the left menu.
1. Confirm that **Microsoft.Network** is in the list of resource providers. Otherwise add it.

    :::image type="content" source="../media/how-to/fine-tune/llama/subscription-resource-providers.png" alt-text="Screenshot of subscription resource providers in Azure portal." lightbox="../media/how-to/fine-tune/llama/subscription-resource-providers.png":::

### Data preparation

Prepare your training and validation data to fine-tune your model. Your training data and validation data sets consist of input and output examples for how you would like the model to perform.

Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a balanced and diverse dataset.

This involves maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations, ultimately leading to more accurate and balanced model responses.

Different model types require a different format of training data.

# [Chat Completion](#tab/chatcompletion)

The training and validation data you use **must** be formatted as a JSON Lines (JSONL) document. For `Meta-Llama-3.1-70B-Instruct` the fine-tuning dataset must be formatted in the conversational format that is used by the Chat completions API.

### Example file format

```json
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Is Xbox better than PlayStation?"}, {"role": "assistant", "content": "I apologize, but I cannot provide personal opinions. My primary job is to assist you with any issues related to your Xbox device. Do you have any Xbox-related issues that need addressing?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "Can I play PC games on my Xbox?"}, {"role": "assistant", "content": "While Xbox consoles don't natively support PC games, they can play an array of Xbox games, many of which are also available on PC. Can I assist you with finding games compatible with your Xbox device?"}]}
    {"messages": [{"role": "system", "content": "You are an Xbox customer support agent whose primary goal is to help users with issues they are experiencing with their Xbox devices. You are friendly and concise. You only provide factual answers to queries, and do not provide answers that are not related to Xbox."}, {"role": "user", "content": "I'm having trouble connecting my Xbox to the Wi-Fi."}, {"role": "assistant", "content": "No worries, let's go through the network settings on your Xbox. Can you please tell me what happens when you try to connect it to the Wi-Fi?"}]}
```
The supported file type is JSON Lines. Files are uploaded to the default datastore and made available in your project.

# [Text Generation](#tab/textgeneration)

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

## Fine-tune a Meta Llama model

# [Meta Llama 3.1](#tab/llama-three)

To fine-tune a LLama 3.1 model:

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. Choose the model you want to fine-tune from the Azure AI Foundry portal [model catalog](https://ai.azure.com/explore/models). 

1. On the model's **Details** page, select **fine-tune**.

1. Select the project in which you want to fine-tune your models. To use the pay-as-you-go model fine-tune offering, your workspace must belong to the **West US 3** region.
1. On the fine-tune wizard, select the link to **Azure Marketplace Terms** to learn more about the terms of use. You can also select the **Marketplace offer details** tab to learn about pricing for the selected model.
1. If this is your first time fine-tuning the model in the project, you have to subscribe your project for the particular offering (for example, Meta-Llama-3.1-70B-Instruct) from Azure Marketplace. This step requires that your account has the Azure subscription permissions and resource group permissions listed in the prerequisites. Each project has its own subscription to the particular Azure Marketplace offering, which allows you to control and monitor spending. Select **Subscribe and fine-tune**.

    > [!NOTE]
    > Subscribing a project to a particular Azure Marketplace offering (in this case, Meta-Llama-3.1-70B-Instruct) requires that your account has **Contributor** or **Owner** access at the subscription level where the project is created. Alternatively, your user account can be assigned a custom role that has the Azure subscription permissions and resource group permissions listed in the [prerequisites](#prerequisites).

1. Once you sign up the project for the particular Azure Marketplace offering, subsequent fine-tuning of the _same_ offering in the _same_ project don't require subscribing again. Therefore, you don't need to have the subscription-level permissions for subsequent fine-tune jobs. If this scenario applies to you, select **Continue to fine-tune**.

1. Enter a name for your fine-tuned model and the optional tags and description.
1. Select training data to fine-tune your model. See [data preparation](#data-preparation) for more information.

    > [!NOTE]
    > If you have your training/validation files in a credential less datastore, you will need to allow workspace managed identity access to their datastore in order to proceed with MaaS finetuning with a credential less storage. On the "Datastore" page, after clicking "Update authentication" > Select the following option: 
    
    ![Use workspace managed identity for data preview and profiling in Azure Machine Learning studio.](../media/how-to/fine-tune/llama/credentials.png)

    Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a balanced and diverse dataset. This involves maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations, ultimately leading to more accurate and balanced model responses.
    - The batch size to use for training. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256.
    - The fine-tuning learning rate is the original learning rate used for pretraining multiplied by this multiplier. We recommend experimenting with values between 0.5 and 2. Empirically, we've found that larger learning rates often perform better with larger batch sizes. Must be between 0.0 and 5.0.
    - Number of training epochs. An epoch refers to one full cycle through the data set.

1. Task parameters are an optional step and an advanced option- Tuning hyperparameter is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. The default settings can be used or advanced users can customize parameters like epochs or learning rate.

1. Review your selections and proceed to train your model.

Once your model is fine-tuned, you can deploy the model and can use it in your own application, in the playground, or in prompt flow. For more information, see [How to deploy Llama 3.1 family of large language models with Azure AI Foundry](./deploy-models-llama.md).


# [Meta Llama 2](#tab/llama-two)

You can fine-tune a Llama 2 model in Azure AI Foundry portal via the [model catalog](./model-catalog-overview.md) or from your existing project. 

To fine-tune a Llama 2 model in an existing Azure AI Foundry project, follow these steps:

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
   
1. Choose the model you want to fine-tune from the Azure AI Foundry portal [model catalog](https://ai.azure.com/explore/models). 

1. On the model's **Details** page, select **fine-tune**.
   
1. If this is the first time you fine-tuned the model in the project, you have to sign up your project for the particular offering from the Azure Marketplace. Each project has its own connection to the marketplace's offering, which, allows you to control and monitor spending per project. Select **Continue to fine-tune**.

    > [!NOTE]
    > Subscribing a project to a particular offering from the Azure Marketplace requires **Contributor** or **Owner** access at the subscription level where the project is created. 

    :::image type="content" source="../media/how-to/fine-tune/llama/llama-pay-as-you-go-overview.png" alt-text="Screenshot of pay-as-you-go marketplace overview." lightbox="../media/how-to/fine-tune/llama/llama-pay-as-you-go-overview.png":::

1. Choose a base model to fine-tune and select **Confirm**. Your choice influences both the performance and [the cost of your model](./deploy-models-llama.md#cost-and-quota-considerations-for-meta-llama-models-deployed-as-serverless-api-endpoints).

    :::image type="content" source="../media/how-to/fine-tune/llama/fine-tune-select-model.png" alt-text="Screenshot of option to select a model to fine-tune." lightbox="../media/how-to/fine-tune/llama/fine-tune-select-model.png":::

1. Enter a name for your fine-tuned model and the optional tags and description.
1. Select training data to fine-tune your model. See [data preparation](#data-preparation) for more information.

    Make sure all your training examples follow the expected format for inference. To fine-tune models effectively, ensure a balanced and diverse dataset. This involves maintaining data balance, including various scenarios, and periodically refining training data to align with real-world expectations, ultimately leading to more accurate and balanced model responses.
    - The batch size to use for training. When set to -1, batch_size is calculated as 0.2% of examples in training set and the max is 256.
    - The fine-tuning learning rate is the original learning rate used for pretraining multiplied by this multiplier. We recommend experimenting with values between 0.5 and 2. Empirically, we've found that larger learning rates often perform better with larger batch sizes. Must be between 0.0 and 5.0.
    - Number of training epochs. An epoch refers to one full cycle through the data set. If set to -1, number of epochs will be determined dynamically based on the input data.

1. Task parameters are an optional step and an advanced option- Tuning hyperparameter is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. The default settings can be used or advanced users can customize parameters like epochs or learning rate.

1. Review your selections and proceed to train your model.

Once your model is fine-tuned, you can deploy the model and can use it in your own application, in the playground, or in prompt flow. For more information, see [How to deploy Llama 2 family of large language models with Azure AI Foundry](./deploy-models-llama.md).

---

## Cleaning up your fine-tuned models 

You can delete a fine-tuned model from the fine-tuning model list in [Azure AI Foundry](https://ai.azure.com) or from the model details page. Select the fine-tuned model to delete from the Fine-tuning page, and then select the Delete button to delete the fine-tuned model.

>[!NOTE]
> You can't delete a custom model if it has an existing deployment. You must first delete your model deployment before you can delete your custom model.

## Cost and quotas

### Cost and quota considerations for Meta Llama models fine-tuned as a service

Meta Llama models fine-tuned as a service are offered by Meta through the Azure Marketplace and integrated with Azure AI Foundry for use. You can find the Azure Marketplace pricing when [deploying](./deploy-models-llama.md) or fine-tuning the models.

Each time a project subscribes to a given offer from the Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [monitor costs for models offered throughout the Azure Marketplace](./costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

## Sample notebook

You can use this [sample notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/finetuning/standalone/chat-completion/chat_completion_with_model_as_service.ipynb)  to create a standalone fine-tuning job to enhance a model's ability to summarize dialogues between two people using the Samsum dataset. The training data utilized is the ultrachat_200k dataset, which is divided into four splits suitable for supervised fine-tuning (sft) and generation ranking (gen). The notebook employs the available Azure AI models for the chat-completion task (If you would like to use a different model than what's used in the notebook, you can replace the model name). The notebook includes setting up prerequisites, selecting a model to fine-tune, creating training and validation datasets, configuring and submitting the fine-tuning job, and finally, creating a serverless deployment using the fine-tuned model for sample inference.

## Content filtering

Models deployed as a service with pay-as-you-go billing are protected by Azure AI Content Safety. When deployed to real-time endpoints, you can opt out of this capability. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](../concepts/content-filtering.md).


## Next steps
- [What is Azure AI Foundry?](../what-is-ai-studio.md)
- [Learn more about deploying Meta Llama models](./deploy-models-llama.md)
- [Azure AI FAQ article](../faq.yml)
