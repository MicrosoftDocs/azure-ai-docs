---
title: Guidance for integration and responsible use with Custom Vision
titleSuffix: Foundry Tools
description: Guidance for how to deploy Custom Vision responsibly, based on the knowledge and understanding from the team that created this product.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-custom-vision
ms.topic: article
ms.date: 07/07/2021
---

# Guidance for integration and responsible use with Custom Vision

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft wants to help you responsibly develop and deploy solutions that use Azure AI Custom Vision. We're taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations represent our commitment to developing Responsible AI.

## General guidance

When you're getting ready to deploy Custom Vision, the following activities help to set you up for success:

* **Understand what it can do:** Fully assess Custom Vision to understand its capabilities and limitations. Understand how it will perform in your particular deployment scenario and operational context by thoroughly testing it with production‑like images, representative lighting conditions, and target camera hardware.
<!-- Comment: Scoped ambiguous terms by adding concrete deployment and testing context. -->

* **Respect an individual's right to privacy:** Only collect image data from individuals for lawful and justifiable purposes, and only use training or inference images for which you have explicit, documented consent for the stated use. For example, evaluate camera locations and positions. Adjust camera angles and regions of interest so they exclude protected areas (for example, bathrooms) and non‑consented public spaces (for example, external streets or mall concourses).
<!-- Comment: Clarified data type, consent scope, and tightened camera usage guidance with explicit constraints. -->

* **Legal review:** Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within, and your responsibility to resolve any issues that might come up in the future. Do not provide any legal advice or guidance.

* **Human in the loop:** Keep a human in the loop by requiring human review for high‑impact predictions and maintaining real‑time human override for production inference workflows. This means ensuring constant human oversight of the AI-powered product or feature, and maintaining the role of humans in decision-making. Ensure that you can have real-time human intervention in the solution to prevent harm. This enables you to manage situations when the AI system does not perform as required.
<!-- Comment: Clarified human-in-the-loop expectations with operational qualifiers. -->

* **Security:** Ensure your solution is secure by implementing controls such as encrypted storage for training images, role‑based access control for project resources, and restricted access to prediction endpoints.
<!-- Comment: Strengthened security guidance with explicit control examples. -->

* **Build trust with affected stakeholders**: Communicate the expected benefits and potential risks of image collection and automated classification to affected stakeholders, including employees, visitors, or customers. Help people understand why the data is needed and how the use of the data will lead to their benefit. Describe data handling in an understandable way.
<!-- Comment: Clarified stakeholder communication scope and affected parties. -->

* **Customer feedback loop:** Provide at least one persistent feedback channel (for example, an in‑app form or monitored email address) that allows users and affected individuals to report issues after deployment. Monitor and improve the AI-powered product or feature on an ongoing basis. Be ready to implement any feedback and suggestions for improvement. Establish channels to collect questions and concerns from affected stakeholders (people who might be directly or indirectly impacted by the system, including employees, visitors, and the general public). For example:
<!-- Comment: Tightened feedback loop guidance with explicit, actionable channels. -->

  * Feedback features built into app experiences.
  * An easy-to-remember email address for feedback.
  * Anonymous feedback boxes placed in semi-private spaces.
  * Knowledgeable representatives in the lobby.

* **Feedback:** Seek out feedback from a diverse sampling of the community during the development and evaluation process (for example, historically marginalized groups, people with disabilities, and service workers). For more information, see [Community jury](/azure/architecture/guide/responsible-innovation/community-jury/).

* **User Study:** Any consent or disclosure recommendations should be framed in a user study. Evaluate the first and continuous-use experience with a representative sample of the community to validate that the design choices lead to effective disclosure. Conduct user research with 10-20 community members (affected stakeholders) to evaluate their comprehension of the information and to determine if their expectations are met.

## Next steps

* [Build a classifier model](/azure/ai-services/custom-vision-service/getting-started-build-a-classifier)
* [Build an object detector model](/azure/ai-services/custom-vision-service/get-started-build-detector)