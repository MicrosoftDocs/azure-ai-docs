---
title: Azure OpenAI in Azure AI Foundry Models fine-tuning considerations
description: Learn more about what you should take into consideration before fine-tuning with Azure OpenAI 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 03/26/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom:
---

# Azure OpenAI in Azure AI Foundry Models fine-tuning considerations

Fine-tuning is the process of taking a pretrained language model and adapting it to perform a specific task or improve its performance on a particular dataset. This involves training the model on a smaller, task-specific dataset while adjusting the model's weights slightly. Fine-tuning leverages the knowledge the model acquired during its initial training on a large, diverse dataset, allowing it to specialize without starting from scratch. This approach is often more efficient and effective than training a new model from scratch, especially for specialized tasks. 

## Key benefits of fine-tuning

### Enhanced accuracy and relevance

Fine-tuning improves the model's performance on particular tasks by training it with task-specific data. This often results in more accurate and relevant high-quality outputs compared to using general prompts. 

Unlike few-shot learning, where only a limited number of examples can be included in a prompt, fine-tuning allows you to train the model on an additional dataset. Fine-tuning helps the model learn more nuanced patterns and improves task performance. 

### Efficiency and potential cost savings

Fine-tuned models require shorter prompts because they are trained on relevant examples. This process reduces the number of tokens needed in each request, which can lead to cost savings depending on the use case. 

Since fine-tuned models need fewer examples in the prompt, they process requests faster, resulting in quicker response times. 

### Scalability and specialization

Fine-tuning applies the extensive pretraining of language models and hones their capabilities for specific applications, making them more efficient and effective for targeted use cases. 

Fine-tuning smaller models can achieve performance levels comparable to larger, more expensive models for specific tasks. This approach reduces computational costs and increases speed, making it a cost-effective scalable solution for deploying AI in resource-constrained environments. 

## When to fine-tune

Fine-tuning is suited for times when you have a small amount of data and want to improve the performance of your model. Fine-tuning can be for different kinds of use cases - but they often fall into broader categories. 

* **Reducing prompt engineering overhead**: Many users begin with few-shot learning, appending examples of desired outputs to their system message. Over time, this process can lead to increasingly long prompts, driving up token counts and latency. Fine-tuning lets you embed these examples into the model by training on the expected outputs, which is valuable in scenarios with numerous edge cases.

* **Modifying style and tone**: Fine-tuning helps align model outputs with a desired style or tone, ensuring consistency in applications like customer service chatbots and brand-specific communication.

* **Generating outputs in specific formats or schemas**: Models can be fine-tuned to produce outputs in specific formats or schemas, making them ideal for structured data generation, reports, or formatted responses.

* **Enhancing tool usage**: While the chat completions API supports tool calling, listing many tools increases token usage and may lead to hallucinations. Fine-tuning with tool examples enhances accuracy and consistency, even without full tool definitions.

* **Enhancing retrieval-based performance**: Combining fine-tuning with retrieval methods improves a model’s ability to integrate external knowledge, perform complex tasks, and provide more accurate, context-aware responses. Fine-tuning trains the model to effectively use retrieved data while filtering out irrelevant information.

* **Optimizing for efficiency**: Fine-tuning can also be used to transfer knowledge from a larger model to a smaller one, allowing the smaller model to achieve similar task performance with lower cost and latency. For example, production data from a high-performing model can be used to fine-tune a smaller, more efficient model. This approach helps scale AI solutions while maintaining quality and reducing computational overhead.

* **Distillation**: Model Distillation uses a large model's outputs to fine-tune a smaller model, allowing it to perform similarly on a specific task, for example collecting production traffic from an o1 deployment and using that as training data to fine tune 4o-mini. This process can cut cost and latency since smaller models can be more efficient. 

## Types of fine-tuning

Azure AI Foundry offers multiple types of fine -tuning techniques:

* **Supervised fine-tuning**: This allows you to provide custom data (prompt/completion or conversational chat, depending on the model) to teach the base model new skills. This process involves further training the model on a high-quality labeled dataset, where each data point is associated with the correct output or answer. The goal is to enhance the model's performance on a particular task by adjusting its parameters based on the labeled data. This technique works best when there are finite ways of solving a problem and you want to teach the model a particular task and improve its accuracy and conciseness.

* **Reinforcement fine-tuning**: This is a model customization technique, beneficial for optimizing model behavior in highly complex or dynamic environments, enabling the model to learn and adapt through iterative feedback and decision-making. For example, financial services providers can optimize the model for faster, more accurate risk assessments or personalized investment advice. In healthcare and pharmaceuticals, o3-mini can be tailored to accelerate drug discovery, enabling more efficient data analysis, hypothesis generation, and identification of promising compounds. RFT is a great way to fine-tune when there are infinite or high number of ways to solve a problem. The grader rewards the model incrementally and makes reasoning better.

* **Direct Preference Optimization (DPO)**: This is another new alignment technique for large language models, designed to adjust model weights based on human preferences. Unlike Reinforcement Learning from Human Feedback (RLHF), DPO doesn't require fitting a reward model and uses binary preferences for training. This method is computationally lighter and faster, making it equally effective at alignment while being more efficient. You share thenon-preferred and preferred response to the training set and use the DPO technique.

You can also stack techniques: first using SFT to create a customized model – optimized for your use case – then using preference fine tuning to align the responses to your specific preferences. During the SFT step, you focus on data quality and representativeness of the tasks, while the DPO step adjusts responses with specific comparisons. 

## Challenges and limitations of fine-tuning

Fine-tuning large language models scan be a powerful technique to adapt them to specific domains and tasks. However, fine-tuning also comes with some challenges and disadvantages that need to be considered before applying it to a real-world problem. Below are a few of these challenges and disadvantages. 

- Fine-tuning requires high-quality, sufficiently large, and representative training data matching the target domain and task. Quality data is relevant, accurate, consistent, and diverse enough to cover the possible scenarios and variations the model will encounter in the real world. Poor-quality or unrepresentative data leads to over-fitting, under-fitting, or bias in the fine-tuned model, which harms its generalization and robustness.
- Fine-tuning large language models means extra costs associated with training and hosting the custom model.
- Formatting input/output pairs used to fine-tune a large language model can be crucial to its performance and usability.
- Fine-tuning may need to be repeated whenever the data is updated, or when an updated base model is released. This involves monitoring and updating regularly.
- Fine-tuning is a repetitive task (trial and error) so, the hyperparameters need to be carefully set. Fine-tuning requires much experimentation and testing to find the best combination of hyperparameters and settings to achieve desired performance and quality.

## Next steps

- Watch the [Azure AI Show episode: "To fine-tune or not to fine-tune, that is the question"](https://www.youtube.com/watch?v=0Jo-z-MFxJs)
- Learn more about [Azure OpenAI fine-tuning](../how-to/fine-tuning.md)
- Explore our [fine-tuning tutorial](../tutorials/fine-tune.md)
