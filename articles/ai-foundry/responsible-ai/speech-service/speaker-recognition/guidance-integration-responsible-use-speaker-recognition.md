---
title: Guidance for integration and responsible use with Speaker Recognition
titleSuffix: Azure AI services
description: Guidance for how to deploy the Speaker Recognition feature responsibly, based on the knowledge and understanding from the team that created this product.
author: HeidiHanZhang
ms.author: heidizh
manager: nitinme
ms.service: azure-ai-speech
ms.topic: article
ms.date: 10/08/2021
---

# Guidance for integration and responsible use with Speaker Recognition

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

Microsoft wants to help you responsibly develop and deploy solutions that use the Speaker Recognition feature. We're taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations reflect our commitment to developing Responsible AI.

## General guidelines

When you're getting ready to deploy Speaker Recognition, the following activities help to set you up for success:

* **Understand what it can do:** Fully assess the capabilities of any AI system you're using to understand its capabilities and limitations. Understand how it will perform in your particular scenario by testing it with real life conditions and diverse user data that reflect your context, including fairness considerations.

* **Respect an individual’s right to privacy:** Only collect biometric data and information from individuals for lawful and justifiable purposes. Obtain meaningful consent for your collection and intended uses.

* **Legal review:** Obtain appropriate legal advice to review your biometric solution, particularly if you'll use it in sensitive or high-risk applications. In some jurisdictions, there are specific legal requirements that govern the collection, use, storage, and security of biometric data. You're responsible for compliance with all applicable laws and regulations that apply to your solution deployment.

* **Build trust with affected stakeholders:** Communicate the expected benefits and potential risks to affected stakeholders. Help people understand why the data is needed and how the use of the data will lead to their benefit. Describe data handling in an understandable way.

* **Customer feedback loop:** Provide a feedback channel that allows users and individuals to report issues with Speaker Recognition after it’s been deployed. This mechanism should also allow for feedback about fairness. Monitor and improve the AI-powered product or feature on an ongoing basis. Be ready to implement any feedback and suggestions for improvement. Establish channels to collect questions and concerns from affected stakeholders (people who might be directly or indirectly impacted by the system, including employees, speakers, and the general public). Potential feedback channels include features built into application experiences, or an easy-to-remember email address for feedback.

* **Train and support end users:** The people who use the output of your solution, or who decide whether the output is correct, might not have experience collaborating with AI systems. This can result in mismatched judgments or the introduction of unfair bias. You can empower these users by evaluating where mismatches might occur, and providing training and ongoing support.

## Recommendations for preserving privacy

A successful privacy approach empowers individuals with information and provides controls and protection to preserve their privacy.  

* Ensure that you've received the appropriate permissions from users to conduct speaker recognition, and be clear about your intended scope of use and its duration. Don't share data without explicit consent from affected stakeholders and data owners, and minimize the data that you do share.
* Text-dependent verification requires the speaker’s active participation by picking and reading a specific passphrase at enrollment. Text-independent verification or identification allows everyday language for enrollment and recognition, so the speaker’s active participation isn't ensured. Ask the speaker to read a specific text in the enrollment to ensure active participation by the speaker and increase their awareness of using Speaker Recognition.
* Speaker Recognition doesn't store primary identifiers (for example, customer IDs) alongside voice signatures or audio of a speaker sent to the Speech service for enrollment or recognition. Microsoft associates this data with random GUIDs (globally unique identifiers).  It's up to you to manage the user identity mapping between these GUIDs and your users. You're responsible for ensuring that this data is securely stored and managed.  
* Provide a mechanism to allow the affected stakeholders and data owners to unenroll from Speaker Recognition and delete their data at any time. Implement a data retention strategy and plan that only retains enrollment data from your users for as long as needed to provide the services. Delete user data after some period of time, such as upon user termination or a specified period inactivity.

## Next steps

* [Speaker Recognition overview](/azure/ai-services/speech-service/speaker-recognition-overview)
* [Limited access for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/limited-access-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
* [Transparency Note for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/transparency-note-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
