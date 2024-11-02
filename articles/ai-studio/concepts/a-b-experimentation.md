---
title: A/B experiments for AI applications
description: Learn about conducting A/B experiments for AI applications.
author: s-polly
ms.author: scottpolly
ms.reviewer: skohlmeier
ms.service: azure-ai-studio
ms.topic: concept-article 
ms.date: 11/22/2024

#CustomerIntent: As an AI application developer, I want to learn about A/B experiments so that I can evaluate and improve my applications.
---

# A/B Experiments for AI applications

In the rapidly evolving field of AI application development, A/B experimentation has emerged as a critical practice. Given trade-offs between business impact, risk and cost, you need to be able to continuously evaluate your AI applications and run A/B experiments at scale. Offline and online evaluation only gets you limited mileage and needs to be complimented by A/B experimentation to ensure that you are using the right metrics to measure success. A/B experimentation, which involves comparing two versions of a feature, prompt or model using feature flags or dynamics configuration to determine which performs better, is essential for several reasons:

- **Enhancing Model Performance** - A/B experimentation allows developers to systematically test different versions of AI models, algorithms, or features to identify the most effective version. By running controlled experiments, developers can measure the impact of changes on key performance metrics, such as accuracy, user engagement, and response time. This iterative process enables you to identify the best model, assists in fine-tuning and ensures that your models deliver the best possible results.
- **Reducing Bias and Improving Fairness** - AI models can inadvertently introduce biases, leading to unfair outcomes. A/B experimentation helps in identifying and mitigating these biases by comparing the performance of different model versions across diverse user groups. This ensures that the AI applications are fair and equitable, providing consistent performance for all users.
- **Accelerating Innovation** - A/B experimentation fosters a culture of innovation by encouraging continuous experimentation and learning. Developers can quickly validate new ideas and features, reducing the time and resources spent on unproductive approaches. This accelerates the development cycle and allows teams to bring innovative AI solutions to market faster.
- **Optimizing User Experience** - User experience is paramount in AI applications. A/B experimentation enables developers to experiment with different user interface designs, interaction patterns, and personalization strategies. By analyzing user feedback and behavior, developers can optimize the user experience, making AI applications more intuitive and engaging.
- **Data-Driven Decision Making** - A/B experimentation provides a robust framework for data-driven decision making. Instead of relying on intuition or assumptions, developers can base their decisions on empirical evidence. This leads to more informed and effective strategies for improving AI applications.


## How does A/B experimentation fit into the AI application lifecycle?


A/B experimentation and offline evaluation are both essential components in the development of AI applications, each serving unique purposes that complement each other.
Offline evaluation involves testing AI models using test datasets to measure their performance on various metrics such as fluency and coherence. After selecting a model in the GitHub Model marketplace, offline pre-production evaluation is crucial for initial model validation during integration testing, allowing developers to identify potential issues and make improvements before deploying the model or application to production.

However, offline evaluation has its limitations. It cannot fully capture the dynamic and complex interactions that occur in real-world scenarios. This is where A/B experimentation comes into play. By deploying different versions of the AI model or UX features to live users, A/B experimentation provides insights into how the model and application performs in real-world conditions. This helps you understand user behavior, identify unforeseen issues, and measure the impact of changes on model evaluation metrics, operational metrics (e.g., latency) and business metrics (e.g. account sign-ups, conversions, etc.).

As shown in the diagram below, while offline evaluation is essential for initial model validation and refinement, A/B experimentation provides the real-world testing needed to ensure the AI application performs effectively and fairly in practice. Together, they form a comprehensive approach to developing robust, safe and user-friendly AI applications.

:::image type="content" source="../media/concepts/experimentation-overview.png" alt-text="A diagram depicting a typical workflow for A/B experimentation":::

## Scale AI applications with Azure AI evaluations and online A/B experimentation using CI/CD workflows 

We are significantly simplifying the evaluation and A/B experimentation process with GitHub Actions that can be integrated seamlessly into existing CI/CD workflows in GitHub. In your CI workflows, you can now use our Azure AI Evaluation GitHub Action to run manual or automated evaluations after changes are committed leveraging the [Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md) to compute metrics such as coherence and fluency. 

We also have an online experimentation feature in private preview that enables you to integrate A/B experimentation into your CD workflows. Leveraging our Online Experimentation GitHub Action, A/B experiments can be automatically created and analyzed using out of the box AI model metrics and custom metrics as part of your CD workflows following successful deployment. Along the way you can also engage with a GitHub Copilot for Azure plugin that assists with experimentation, creates metrics, powers decisions and more. 

Azure AI evaluation is already publicly available, but if you are interested in trying out our online experimentation feature please sign up for our private preview to learn more! 

<!--> Need to revise the section above to make private preview content appropriate. <-->

## Additional A/B experimentation solutions available in the Azure Marketplace


You are also welcome to leverage your own A/B experimentation provider to run experiments on your AI applications. There are several solutions to choose from available in the Azure Marketplace:

### Statsig

[Statsig](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/statsiginc1610354169520.statsig?tab=Overview) is an Azure AI partner and an experimentation platform for Product, Engineering, and Data Science teams that connects the features you build to the business metrics you care about. Statsig powers automatic A/B tests and experiments for web and mobile applications, giving teams a comprehensive view of which features are driving impact (and which aren't). To simplify experimentation with Azure AI, Statsig has published a wrapper SDK built on top of the Azure AI SDK that makes it easier for Statsig customers to run experiments.

### Split.io
[Split.io](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/splitio1614896174525.split_azure?tab=Overview) enables you to set up feature flags and safely deploy to production, controlling who sees which features and when. You can also connect every flag to contextual data, so you know if your features are making things better or worse, and act without hesitation. With Split's Microsoft integrations, we are helping development teams manage feature flags, monitor release performance, experiment, and surface data to make ongoing, data-driven decisions.

### LaunchDarkly
[LaunchDarkly](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/aad.launchdarkly?tab=Overview) is a feature management and experimentation platform built with software developers in mind. It enables you to manage feature flags on a large scale, run A/B tests and experiments, and progressively deliver software to ship with confidence.



## Related content


- [Azure AI Evaluation SDK](../how-to/develop/evaluate-sdk.md)
