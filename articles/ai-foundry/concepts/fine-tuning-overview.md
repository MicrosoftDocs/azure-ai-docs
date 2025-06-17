---
title: Fine-tune models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article explains what fine-tuning is and under what circumstances you should consider doing it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - code01
ms.topic: concept-article
ms.date: 05/14/2025
ms.reviewer: keli19
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn what it means to fine-tune a model.
---

# Fine-tune models with Azure AI Foundry

Fine-tuning customizes a pretrained AI model with additional training on a specific task or dataset to improve performance, add new skills, or enhance accuracy. The result is a new, optimized GenAI model based on the provided examples. This article walks you through use-cases for fine-tuning and how it helps you in your GenAI journey.

[Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) offers several models across model providers enabling you to get access to the latest and greatest in the market. [View this list for more details](#supported-models-for-fine-tuning). 

:::image type="content" source="../media/concepts/model-catalog-fine-tuning.png" alt-text="Screenshot of Azure AI Foundry model catalog and filtering by Fine-tuning tasks." lightbox="../media/concepts/model-catalog-fine-tuning.png":::

## Getting started with fine-tuning

To find steps


## Steps to fine-tune a model

For steps on fine-tuning a model within AI Foundry, see foundry models for serverless API Steps and foundry models for managed compute steps. 

:::image type="content" source="../media/concepts/data-pipeline.png" alt-text="Screenshot of the fine-tuning data pipeline for adapting pre-trained models to a specific task." lightbox="../media/concepts/data-pipeline.png":::

## Data preparation

The fine-tuning process begins by selecting a pretrained model and preparing a relevant dataset tailored to the target task. This dataset should reflect the kind of inputs the model will see in deployment. 

Follow this link to view and download [example datasets](https://github.com/Azure-Samples/AIFoundry-Customization-Datasets) to try out fine-tuning.

To fine-tune a model for chat or question answering, your training dataset should reflect the types of interactions the model will handle. Here are some key elements to include in your dataset: 

- **Prompts and responses**: Each entry should contain a prompt (e.g., a user question) and a corresponding response (e.g., the model’s reply). 
- **Contextual information**: For multi-turn conversations, include previous exchanges to help the model understand context and maintain coherence. 
- **Diverse examples**: Cover a range of topics and scenarios to improve generalization and robustness. 
- **Human-generated responses**: Use responses written by humans to teach the model how to generate natural and accurate replies. 
- **Formatting**: Use a clear structure to separate prompts and responses. For example, `\n\n###\n\n` and ensure the delimiter doesn't appear in the content. 

## Model selection

Selecting the right model for fine-tuning is a critical decision that impacts performance, efficiency, and cost. Before making a choice, it is essential to clearly define the task and establish the desired performance metrics. A well-defined task ensures that the selected model aligns with specific requirements, optimizing effort and resources. 

## Use evaluations in fine-tuning

You should have clearly defined goals for what success with fine-tuning looks like. Ideally, these should go beyond qualitative measures and include quantitative metrics, such as using a holdout validation set, conducting user acceptance testing, or A/B tests comparing the fine-tuned model to the base model. 

Model training can be guided by metrics. For example, BLEU-4 was used to evaluate training when fine-tuning a model to generate chest X-Ray reports, as seen in this paper. Additionally you can also monitor metrics while you train. If the loss curves are not converging as expected, you can pause the jobs, analyze and resume. 

:::image type="content" source="../media/concepts/hyperparameter-tuning.png" alt-text="Screenshot of the fine-tuning data hyperparameter tuning and metrics used to guide model training." lightbox="../media/concepts/hyperparameter-tuning.png":::

**Use intermediate checkpoints for better model selection**. Save checkpoints at regular intervals (e.g., every few epochs) and evaluate their performance. In some cases, an intermediate checkpoint may outperform the final model, allowing you to select the best version rather than relying solely on the last trained iteration. 

## Deployment and monitoring

- Choose a suitable deployment infrastructure, such as cloud-based platforms or on-premises servers. 
- Continuously monitor the model's performance and make necessary adjustments to ensure optimal performance. 
- Consider regional deployment needs and latency requirements to meet enterprise SLAs. Implement security guardrails, such as private links, encryption, and access controls, to protect sensitive data and maintain compliance with organizational policies. 

## Supported models for fine-tuning

Now that you know when to use fine-tuning for your use case, you can go to Azure AI Foundry to find models available to fine-tune.
For some models in the model catalog, fine-tuning is available by using a standard deployment, or a managed compute (preview), or both.

Fine-tuning is available in specific Azure regions for some models that are deployed via standard deployments. To fine-tune such models, a user must have a hub/project in the region where the model is available for fine-tuning. See [Region availability for models in standard deployment](../how-to/deploy-models-serverless-availability.md) for detailed information.

For more information on fine-tuning using a managed compute (preview), see [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md).

For details about Azure OpenAI in Azure AI Foundry Models that are available for fine-tuning, see the [Azure OpenAI in Foundry Models documentation.](../../ai-services/openai/concepts/models.md#fine-tuning-models)


## Best practices for fine-tuning

Here are some best practices that can help improve the efficiency and effectiveness of fine-tuning LLMs for various applications: 

- **Start with a smaller model**: A common mistake is assuming that your application needs the newest, biggest, most expensive model. Especially for simpler tasks, start with smaller models and only try larger models if needed. 
- **Select models based on domain needs**: Start with industry-standard models before considering fine-tuned versions for specific use cases. Use benchmark leaderboards to assess performance and test real-world scenarios in model playgrounds. Balance accuracy, cost, and efficiency to ensure the best fit for your deployment. 
- **Collect a large, high-quality dataset**: LLMs are data-hungry and can benefit from having more diverse and representative data to fine-tune on. However, collecting and annotating large datasets can be costly and time-consuming. Therefore, you can also use synthetic data generation techniques to increase the size and variety of your dataset. However, you should also ensure that the synthetic data is relevant and consistent with your task and domain. Also ensure that it does not introduce noise or bias to the model. 
- **Try fine-tuning subsets first**: To assess the value of getting more data, you can fine-tune models on subsets of your current dataset to see how performance scales with dataset size. This fine-tuning can help you estimate the learning curve of your model and decide whether adding more data is worth the effort and cost. You can also compare the performance of your model with the pre-trained model or a baseline. This comparison shows how much improvement you can achieve with fine-tuning. 
- **Experiment with hyperparameters**: Iteratively adjust hyperparameters to optimize the model performance. Hyperparameters, such as the learning rate, the batch size and the number of epochs, can have significant effect on the model’s performance. Therefore, you should experiment with different values and combinations of hyperparameters to find the best ones for your task and dataset. 
- **Try different data formats**: Depending on the task, different data formats can have different impacts on the model’s performance. For example, for a classification task, you can use a format that separates the prompt and the completion with a special token, such as {"prompt": "Paris##\n", "completion": " city\n###\n"}. Be sure to use formats suitable for your application. 

## Related content

- [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md)
- [Fine-tune an Azure OpenAI model in Azure AI Foundry portal](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune models using standard deployment](../how-to/fine-tune-serverless.md)
