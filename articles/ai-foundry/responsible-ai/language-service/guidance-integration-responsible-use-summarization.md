---
title: Guidance for integration and responsible use with summarization
titleSuffix: Foundry Tools
description: Guidance for integration and responsible use with summarization 
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: best-practice
ms.date: 04/09/2022
---

# Guidance for integration and responsible use with summarization

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft wants to help you develop and deploy solutions that use the summarization feature in a responsible manner. Microsoft takes a principled approach to uphold personal agency and dignity, by considering the following aspects of an AI system: fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations reflect our [commitment to developing Responsible AI](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1%3aprimaryr6).

## General guidelines

When you're getting ready to integrate and responsibly use AI-powered products or features, the following activities help to set you up for success. Although each guideline is unlikely to apply to all scenarios, consider them as a starting point for mitigating possible risks:

* **Understand what it can do, and how it might be misused.** Fully assess the capabilities of any AI system you're using to understand its capabilities and limitations. The particular testing that Microsoft conducts might not reflect your scenario. Understand how it will perform in your particular scenario, by thoroughly testing it with real-life conditions and diverse data that reflect your context. Include fairness considerations.

* **Test with real, diverse data.** Understand how your system will perform in your scenario. Test it thoroughly with real-life conditions, and data that reflects the diversity in your users, geography, and deployment contexts. Small datasets, synthetic data, and tests that don't reflect your end-to-end scenario are unlikely to sufficiently represent your production performance.

* **Evaluate the system.** Consider using adversarial testing, where trusted testers attempt to find system failures, poor performance, or undesirable behaviors. This information helps you to understand risks and how to mitigate them. Communicate the capabilities and limitations to stakeholders. To help you evaluate your system, you might find some of these resources useful: [Checklist on GitHub](https://github.com/marcotcr/checklist), [Stereotyping Norwegian Salmon: An Inventory of Pitfalls in Fairness Benchmark Datasets](https://www.microsoft.com/research/uploads/prod/2021/06/The_Salmon_paper.pdf) (Blodgett et al., 2021), and [On the Dangers of Stochastic Parrots: Ca Language Models Be Too Big?](https://dl.acm.org/doi/10.1145/3442188.3445922) (Bender et al., 2021).

* **Learn about fairness.** AI systems can behave unfairly for a variety of reasons. Some are social, some are technical, and some are a combination of the two. There are seldom clear-cut solutions. Mitigation methods are usually context dependent. Learning about fairness can help you learn what to expect and how you might mitigate potential harms. To learn more about the approach that Microsoft uses, see [Responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources?activetab=pivot1%3aprimaryr4), the [AI fairness checklist](https://www.microsoft.com/research/publication/co-designing-checklists-to-understand-organizational-challenges-and-opportunities-around-fairness-in-ai/), and resources from [Microsoft Research](https://www.microsoft.com/research/theme/fate/#!publications).

* **Respect an individual's right to privacy.** Only collect data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use for this purpose.

* **Conduct user testing during development, and solicit feedback after deployment.** Consider using value-sensitive design to identify stakeholders. Work with them to identify their values to design systems that support those values. Seek feedback from a diverse group of people during the development and evaluation process. Use strategies like [Community Jury](/azure/architecture/guide/responsible-innovation/community-jury/).
  
  Undertake user testing with diverse stakeholders. Then analyze the results broken down by stakeholder groups. Include stakeholders from different demographic groups. Consider conducting online experiments, ring testing, dogfooding, field trials, or pilots in deployment contexts.

* **Limit the length, structure, rate, and source of inputs and outputs.** Restricting input and output length can reduce the likelihood of risks. Such risks include producing undesirable content, misuse for an overly general-purpose beyond the intended application use cases, or other harmful, disallowed, or unintended scenarios.

* **Consider requiring prompts to be structured a certain way.** They can be confined to a particular topic, or drawn from validated sources, like a dropdown field. Consider structuring the output so it isn't overly open-ended. Consider returning outputs from validated, reliable source materials (such as existing support articles), rather than connecting to the internet. This restriction can help your application stay on task and mitigate unfair, unreliable, or offensive behavior. Putting rate limits in place can further reduce misuse.

* **Implement blocklists and content moderation. Keep your application on topic.** Consider blocklists and content moderation strategies to check inputs and outputs for undesirable content. The definition of *undesired content* depends on your scenario, and can change over time. It might include hate speech, text that contains profane words or phrases, misinformation, and text that relates to sensitive or emotionally charged topics. Checking inputs can help keep your application on topic, even if a malicious user tries to produce undesired content. Checking API outputs allows you to detect undesired content produced by the system. You can then replace it, report it, ask the user to enter different input, or provide input examples.

* **Authenticate users.** To make misuse more difficult, consider requiring that customers sign in and, if appropriate, link a valid payment method. Consider working only with known, trusted customers in the early stages of development.

* **Ensure human oversight.** Especially in higher-stakes scenarios, maintain the role of humans in decision making. Disclose what the AI has done versus what a human has done.

  Based on your scenario, there are various stages in the lifecycle in which you can add human oversight. Ensure you can have real-time human intervention in the solution to prevent harm. For example, when generating summaries, editors should review the summaries before publication. Ideally, assess the effectiveness of human oversight prior to deployment, through user testing, and after deployment.

* **Have a customer feedback loop.** Provide a feedback channel that allows users and individuals to report issues with the service after deployment. Issues might include unfair or undesirable behaviors. After you've deployed an AI-powered product or feature, it requires ongoing monitoring and improvement. Establish channels to collect questions and concerns from stakeholders who might be directly or indirectly affected by the system, such as employees, visitors, and the general public. Examples include:
    - Feedback features built into app experiences.
    - An easy-to-remember email address for feedback.

* **Conduct a legal review.** Obtain appropriate legal advice to review your solution, particularly if you'll use it in sensitive or high-risk applications. Know what restrictions you might need to work within. Understand your responsibility to resolve any issues that might come up in the future. Ensure the appropriate use of datasets.

* **Conduct a system review.** You might plan to integrate and responsibly use an AI-powered product or feature into an existing system of software, customers, and organizational processes. If so, take the time to understand how each part of your system will be affected. Consider how your AI solution aligns with the principles of responsible AI that Microsoft uses.

* **Security.** Ensure that your solution is secure, and has adequate controls to preserve the integrity of your content and prevent any unauthorized access.

## Recommended content

* **Assess your application for alignment with [Responsible AI principles](https://www.microsoft.com/ai/responsible-ai-resources).**

* **Use the [Microsoft HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/).** The toolkit recommends best practices for how AI systems should behave on initial interaction, during regular interaction, when they're inevitably wrong, and over time.

* **Follow the [Microsoft guidelines for responsible development of conversational AI systems](https://www.microsoft.com/research/publication/responsible-bots/).** Use the guidelines when you develop and deploy language models that power chat bots, or other conversational AI systems.

* **Use Microsoft [Inclusive Design Guidelines](https://www.microsoft.com/design/inclusive/)** to build inclusive solutions.
