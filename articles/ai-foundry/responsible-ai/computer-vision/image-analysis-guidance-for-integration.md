---
title: Guidance for integration and responsible use with Image Analysis
titleSuffix: Foundry Tools
description: Guidance for how to deploy Image Analysis responsibly, based on the knowledge and understanding from the team that created this product.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: article
ms.date: 10/15/2025
---

# Guidance for integration and responsible use with Image Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft works to help customers responsibly develop and deploy solutions that use Azure Vision in Foundry Tools. We're taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations are in line with our commitment to developing Responsible AI.

## General guidelines for integration and responsible use 

This article discusses Azure Vision and the key considerations for making use of this technology responsibly. The following are general recommendations for the responsible deployment and use of Azure Vision. Your context might require you to prioritize and apply these recommendations according to the needs of your specific deployment scenario. But in general, the following activities will assist you:

* **Understand what it can do:** Fully assess the potential of any AI system you are using to understand its capabilities and limitations. Understand how it will perform in your particular scenario and context, by thoroughly testing it with real-life conditions and data (for example, test with production-like images captured across expected lighting conditions, camera angles, and representative object classes).
<!-- Added a concrete testing example to clarify how to assess performance in real-world conditions. -->

* **Respect an individual's right to privacy:** Only collect data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use, and only for the purpose(s) for which consent was given (for example, explicit user consent stating “Images will be analyzed for object detection to improve product safety”).
<!-- Added sample consent wording to make privacy guidance more concrete. -->

* **Legal review:** Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within, and your responsibility to resolve any issues that might come up in the future.

* **Human-in-the-loop:** Keep a human in the loop, and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of Azure Vision, and maintaining the role of humans in decision-making. Ensure that you can have real-time human intervention in the solution to prevent harm (for example, route low-confidence or safety-sensitive detections to a human reviewer before acting on results). This enables you to manage situations where Azure Vision does not perform as expected.
<!-- Added a concrete example of human intervention for safety-sensitive or low-confidence results. -->

* **Security:** Ensure your solution is secure, and that it has adequate controls to preserve the integrity of your content and prevent unauthorized access.

* **Have a blocklist or an allow list:** Instead of enabling all tags with Azure Vision tag feature, focus on the specific ones most appropriate for your use case (for example, allow only “vehicle,” “road,” and “traffic sign” tags for a traffic analysis scenario, and disable person-related tags if not required).
<!-- Added an example allow list to illustrate selective tag enablement. -->

## Recommendations for preserving privacy  

A successful privacy approach empowers individuals with information, and provides controls and protection to preserve their privacy.  

* If the service is part of a solution designed to incorporate health-related data, think carefully about whether and how to record that data. Follow applicable state and federal privacy and health regulations.

* Privacy managers should carefully consider what the retention policies should be for the extracted image metadata and insights, as well as the underlying images. The retention policies should be reflective of the intended use of the applications (for example, retain extracted metadata for 30 days for debugging, and delete underlying images immediately after analysis unless legally required).
<!-- Added a sample retention duration to clarify how retention policies can be applied in practice. -->

* Don't share any data without explicit consent from affected stakeholders or data owners, and minimize the data that is shared.

## Next steps
* [Transparency Note](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-transparency-note)
* [Characteristics and limitations](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-characteristics-and-limitations)
* [Responsible deployment of Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-guidance-for-integration)
* [QuickStart your Image Analysis use case development](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library)
* [Data, privacy, and security for Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security)