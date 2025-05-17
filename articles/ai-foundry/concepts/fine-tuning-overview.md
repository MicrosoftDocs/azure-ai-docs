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

Consider fine-tuning GenAI models to: 

- Scale and adapt to specific enterprise needs
- Reduce false positives as tailored models are less likely to produce inaccurate or irrelevant responses
- Enhance the model's accuracy for domain-specific tasks
- Save time and resources with faster and more precise results
- Get more relevant and context-aware outcomes as models are fine-tuned for specific use cases

[Azure AI Foundry](https://ai.azure.com) offers several models across model providers enabling you to get access to the latest and greatest in the market. [View this list for more details](#supported-models-for-fine-tuning). 

:::image type="content" source="../media/concepts/model-catalog-fine-tuning.png" alt-text="Screenshot of Azure AI Foundry model catalog and filtering by Fine-tuning tasks." lightbox="../media/concepts/model-catalog-fine-tuning.png":::

## Getting started with fine-tuning

When starting out on your generative AI journey, we recommend you begin with prompt engineering and RAG to familiarize yourself with base models and its capabilities. 
- [Prompt engineering](../../ai-services/openai/concepts/prompt-engineering.md) is a technique that involves designing prompts using tone and style details, example responses, and intent mapping for natural language processing models. This process improves accuracy and relevancy in responses, to optimize the performance of the model.
- [Retrieval-augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) improves LLM performance by retrieving data from external sources and incorporating it into a prompt. RAG can help businesses achieve customized solutions while maintaining data relevance and optimizing costs.

As you get comfortable and begin building your solution, it's important to understand where prompt engineering falls short and when you should try fine-tuning.

- Is the base model failing on edge cases or exceptions? 
- Is the base model not consistently providing output in the right format?
- Is it difficult to fit enough examples in the context window to steer the model?
- Is there high latency?

Examples of failure with the base model and prompt engineering can help you identify the data to collect for fine-tuning and establish a performance baseline that you can evaluate and compare your fine-tuned model against. Having a baseline for performance without fine-tuning is essential for knowing whether or not fine-tuning improves model performance. 

Here's an example: 

_A customer wants to use GPT-4o-Mini to turn natural language questions into queries in a specific, nonstandard query language. The customer provides guidance in the prompt ("Always return GQL") and uses RAG to retrieve the database schema. However, the syntax isn't always correct and often fails for edge cases. The customer collects thousands of examples of natural language questions and the equivalent queries for the database, including cases where the model failed before. The customer then uses that data to fine-tune the model. Combining the newly fine-tuned model with the engineered prompt and retrieval brings the accuracy of the model outputs up to acceptable standards for use._

## Use cases

Base models are already pretrained on vast amounts of data. Most times you add instructions and examples to the prompt to get the quality responses that you're looking for - this process is called "few-shot learning." Fine-tuning allows you to train a model with many more examples that you can tailor to meet your specific use-case, thus improving on few-shot learning. Fine-tuning can reduce the number of tokens in the prompt leading to potential cost savings and requests with lower latency. 

Turning natural language into a query language is just one use case where you can "show not tell" the model how to behave. Here are some other use cases: 

- Improve the model's handling of retrieved data
- Steer model to output content in a specific style, tone, or format
- Improve the accuracy when you look up information
- Reduce the length of your prompt
- Teach new skills (that is, natural language to code)

If you identify cost as your primary motivator, proceed with caution. Fine-tuning might reduce costs for certain use cases by shortening prompts or allowing you to use a smaller model. But there might be a higher upfront cost to training, and you have to pay for hosting your own custom model.  

## Steps to fine-tune a model

At a high level, finetuning requires you to:

- Prepare and upload training data, 
- Train a new fine-tuned model, 
- Evaluate your newly trained model, 
- Deploy that model for inferencing, and 
 - Use the fine-tuned model in your application 

It's important to call out that fine-tuning is heavily dependent on the quality of data that you can provide. It's best practice to provide hundreds, if not thousands, of training examples to be successful and get your desired results. 

:::image type="content" source="../media/concepts/data-pipeline.png" alt-text="Screenshot of the fine-tuning data pipeline for adapting pre-trained models to a specific task." lightbox="../media/concepts/data-pipeline.png":::

## Data preparation

### What data are you going to use for fine-tuning? 

The fine-tuning process begins by selecting a pretrained model and preparing a relevant dataset tailored to the target task. This dataset should reflect the kind of inputs the model will see in deployment. 

Follow this link to view and download [example datasets](https://github.com/Azure-Samples/AIFoundry-Customization-Datasets) to try out fine-tuning.

For example, if the goal is to fine-tune a model for sentiment analysis, the dataset would include labeled text examples categorized by sentiment (positive, negative, neutral). The model is then retrained on this dataset, adjusting its parameters to better align with the new task. This retraining process usually requires fewer computational resources compared to training a model from scratch, as it builds upon the existing capabilities. 

Even with a great use case, fine-tuning is only as good as the quality of the data that you're able to provide. Different models will require different data volumes, but you often need to provide fairly large quantities of high-quality curated data in the correct formats. You can use this samples repository to understand formatting conditions and data preparation. 

To fine-tune a model for chat or question answering, your training dataset should reflect the types of interactions the model will handle. Here are some key elements to include in your dataset: 

- **Prompts and responses**: Each entry should contain a prompt (e.g., a user question) and a corresponding response (e.g., the model’s reply). 
- **Contextual information**: For multi-turn conversations, include previous exchanges to help the model understand context and maintain coherence. 
- **Diverse examples**: Cover a range of topics and scenarios to improve generalization and robustness. 
- **Human-generated responses**: Use responses written by humans to teach the model how to generate natural and accurate replies. 
- **Formatting**: Use a clear structure to separate prompts and responses. For example, `\n\n###\n\n` and ensure the delimiter doesn't appear in the content. 

### Best Practices for data preparation 

The more training examples you have, the better. Fine tuning jobs will not proceed without at least 10 training examples, but such a small number isn't enough to noticeably influence model responses. It is best practice to provide hundreds, if not thousands, of training examples to be successful. 100 good-quality examples are better than 1000 poor examples. 

In general, doubling the dataset size can lead to a linear increase in model quality. But keep in mind, low quality examples can negatively impact performance. If you train the model on a large amount of internal data, without first pruning the dataset for only the highest quality examples you could end up with a model that performs much worse than expected. 

### Best practices for data labelling 

Accurate and consistent labelling is crucial for training the model. Follow these best practices: 

- **Ensure data diversity**: Include all the typical variations such as document formats (digital vs. scanned), layout differences, varying table sizes, and optional fields. 
- **Define fields clearly**: Use semantically meaningful field names (e.g., effective_date), especially for custom models, and follow consistent naming conventions like Pascal or camel case. 
- **Maintain label consistency**: Ensure uniform labelling across documents, particularly for repeated values. 
- **Split your data**: Separate training and validation sets to evaluate the model on unseen data and avoid overfitting. 
- **Label at scale**: Aim for at least 50 labelled documents per class, where applicable.  
- **Combine automation and review**: Use AI-generated labels to accelerate the process, focusing manual effort on complex or critical fields.

## Model selection

Selecting the right model for fine-tuning is a critical decision that impacts performance, efficiency, and cost. Before making a choice, it is essential to clearly define the task and establish the desired performance metrics. A well-defined task ensures that the selected model aligns with specific requirements, optimizing effort and resources. 

### Best practices for model selection 

- **Choose models based on domain specificity and use case**: Start by evaluating industry-standard models for general capabilities, then assess models fine-tuned for your specific use case. If your task requires deep domain expertise, selecting a model tailored to your industry can improve accuracy and efficiency while reducing the need for extensive fine-tuning. 
- **Assess model performance on leaderboards**: Review benchmark leaderboards to evaluate how pre-trained models perform on relevant tasks. Focus on key metrics such as accuracy, coherence, latency, and domain-specific benchmarks to identify a strong foundation for fine-tuning. 
- **Experiment with model playgrounds**: Utilize interactive testing environments to assess the base model’s performance on real-world use cases. By adjusting prompts, temperature, and other parameters, you can identify performance gaps before investing in fine-tuning. 
- **Weigh trade-offs between model size, complexity, cost, and performance**: Larger models may offer superior accuracy but come with higher computational costs and latency. Consider the balance between efficiency and precision based on your deployment needs.

## Training and evaluation

Fine-tuning isn't merely a matter of retraining on a new dataset; it also involves careful consideration of various hyperparameters and techniques to balance accuracy and generalization. A key risk is overfitting, where a model becomes too narrowly adapted to training data, reducing its effectiveness on unseen inputs. To mitigate overfitting and optimize performance, fine-tuning requires adjusting parameters such as learning rate, regularization, batch size, number of epochs, and seed settings. 

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

For details about Azure OpenAI in Azure AI Foundry Models that are available for fine-tuning, see the [Azure OpenAI in Foundry Models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models) or the [Azure OpenAI models table](#fine-tuning-azure-openai-models) later in this guide.

For the Azure OpenAI models that you can fine tune, supported regions for fine-tuning include North Central US, Sweden Central, and more.

### Fine-tuning Azure OpenAI models

[!INCLUDE [Fine-tune models](../../ai-services/openai/includes/fine-tune-models.md)]

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

