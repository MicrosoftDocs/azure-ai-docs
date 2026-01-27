---
title: Guidance for integration and responsible use with Face
titleSuffix: Foundry Tools Face
description: Guidance for how to deploy the Face responsibly, based on the knowledge and understanding from the team that created this product.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: best-practice
ms.date: 06/21/2022
---

# Guidance for integration and responsible use of Face

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

To help customers responsibly develop and integrate biometric solutions using Face, we are offering guidance for responsible use based on Microsoft’s AI principles of fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability.

> [!NOTE]
> This article is provided for informational purposes only and not for the purpose of providing legal advice. We strongly recommend seeking specialist legal advice when implementing Face.

## General guidelines for integration and responsible use

When getting ready to integrate and responsibly use AI-powered products or features, the following activities help to set you up for success: 

* **Understand what it can do**: Fully assess the potential of any AI system you are using to understand its capabilities and limitations. Understand how it will perform in your particular scenario and context by thoroughly testing it with real life conditions and data.

* **Respect an individual’s right to privacy**: Only collect biometric data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use for this purpose. 

* **Update privacy policies and communicate them to stakeholders**: Providing conspicuous notice to and securing meaningful consent from individuals before using their images for facial recognition technology is both an opportunity to build trust and in many cases a legal requirement. In some jurisdictions, there may be additional legal requirements. Customers are responsible for compliance with all applicable laws. See [Meaningful consent guidelines](/azure/ai-services/computer-vision/enrollment-overview).

* **Legal review**: Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and your responsibility to resolve any issues that might come up in the future. 

* **Human in the loop**: Keep a human in the loop and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of facial recognition results, and maintaining the role of humans in decision-making. Ensure you can have real-time human intervention in the solution to prevent harm. This enables you to manage situations when the AI system does not perform as required. 

* **Train and support your end users**: The people who use the output of your solution or who decide whether the output is correct might not have experience collaborating with AI systems, which might result in mismatched judgments or the introduction of unfair bias. You can empower these users by evaluating where mismatches might occur and providing training and ongoing evaluation and support.

* **Security**: Ensure your solution is secure and has adequate controls to preserve the integrity of your content and prevent unauthorized access, including: 
    - Implement (and, when possible, automate) strict data retention plans per existing policies/regulation, such as deleting raw data as soon as insights are derived.  
    - Provide appropriate safeguards to secure any data collected, including de-identification and encryption. 

* **Build trust with affected stakeholders**: Communicate the expected benefits and potential risks to affected stakeholders. Help people understand why the data is needed and how the use of the data will lead to their benefit. Describe data handling in an understandable way.  

* **Customer feedback loop**: Provide a feedback channel that allows users and individuals to report issues with the service once it’s been deployed. Once you’ve deployed an AI-powered product or feature it requires ongoing monitoring and improvement – be ready to implement any feedback and suggestions for improvement. Establish channels to collect questions and concerns from affected stakeholders (people who may be directly or indirectly impacted by the system, including employees, visitors, and the general public). Examples of such channels are:
    - Feedback features built into app experiences,
    - An easy-to-remember email address for feedback,
    - Anonymous feedback boxes placed in semi-private spaces, and
    - Knowledgeable representatives in the lobby.

* **Feedback**: Seek out feedback from a diverse sampling of the community during the development and evaluation process (for example, historically marginalized groups, people with disabilities, and service workers).  

* **User Study**: Any consent or disclosure recommendations should be framed in a user study. Evaluate the first and continuous-use experience with a representative sample of the community to validate that the design choices lead to effective disclosure. Conduct user research with 10-20 community members (affected stakeholders) to evaluate their comprehension of the information and to determine if their expectations are met.  

## Suggestions for touchless access control scenarios

This guidance has been developed based on Microsoft user research in the context of enrolling individuals in facial recognition for building access. Therefore, these suggestions might not apply to all facial recognition solutions. Responsible use for Face depends strongly on the specific context in which it’s integrated, so the prioritization and application of these suggestions should be adapted to your scenario.

Even with an enrollment experience that is mostly automated, it’s important to carefully consider how the technology will be integrated into people’s daily tasks and interactions with the system. We suggest that you  identify the people whose job responsibilities might change because of the technology as well as those who might be less likely to adopt the technology because of barriers to access and identify ways to improve their experience.

Based on a case study of scenarios that use facial recognition to grant building access, we offer suggestions for supporting two stakeholder groups: Security and receptionist personnel, and people with visual or mobility impairments. 

### Supporting security and reception personnel
Our research shows that you can support security and reception personnel by helping them be prepared to answer questions about the system, handle system failures, and have a forum to provide feedback about the system. You might:
* Ask for regular updates from security specialists and reception personnel on the system performance, challenges, and frustrations.
* Provide regular training that uses multiple channels such as webinars and Q&A sessions to reach people with different preferences for learning. Possible content for this training material can be found in the [Transparency Note](transparency-note.md).
* Provide role-specific training modules to address the diverse needs of security personnel (for example, security system monitoring specialists and ground operation teams).
* Provide clear talking points about what user data will be stored, for how long, and who has access to allow so that security specialists and reception personnel can be able to answer users' questions.

### Supporting people with visual and or mobility impairments
* Provide a self-enrollment option as well as a way to provide help when users need it.
* In building access scenarios, install facial recognition on doors that are automatic to address accessibility and hygiene concerns.
* If a QR code is used to initiate the enrollment process, place it in an easy-to-access location and provide clear instructions on how to locate it.
* Enable the camera to automatically capture faces when people are within a specific range to better serve the needs of people with visual impairments if they have consented to using the technology. 

## Next steps

* [Meaningful consent guidelines](/azure/ai-services/computer-vision/enrollment-overview).
* [Characteristics and limitations](/azure/ai-foundry/responsible-ai/face/characteristics-and-limitations)
* [Data, privacy, and security for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security)
* [Quickstart your Face use case development](/azure/ai-services/computer-vision/quickstarts-sdk/identity-client-library)
