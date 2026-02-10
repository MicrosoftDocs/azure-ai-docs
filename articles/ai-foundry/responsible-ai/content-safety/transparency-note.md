---
title: Transparency Note and use cases for AI Content Safety
titleSuffix: Foundry Tools
description: This article explains Azure AI Content Safety responsible AI basics, use cases, and terms.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 05/15/2023
---

# Transparency note: Azure AI Content Safety

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see the [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Azure AI Content Safety

### Introduction

Azure AI Content Safety detects harmful user-generated and AI-generated content in applications and services. Azure AI Content Safety includes text, image, and multimodal APIs that allow you to detect material that is harmful, and an Interactive Studio that allows you to view, explore and try out sample code for detecting harmful content across different modalities. 

Custom categories is a feature that allows users to define and detect categories tailored to their specific content moderation needs. Custom categories empower users with greater flexibility and control over their content safety measures.

### Key terms

**Default categories**

The categories below describe the types of harmful content which Azure AI Content Safety detects.

| **Category** | **Description** |
| --- | --- |
| Hate | The hate category describes language attacks or uses that include pejorative or discriminatory language with reference to a person or identity group on the basis of certain differentiating attributes of these groups including but not limited to race, ethnicity, nationality, gender identity and expression, sexual orientation, religion, immigration status, ability status, personal appearance, and body size. |
| Sexual | The sexual category describes language related to anatomical organs and genitals, romantic relationships, acts portrayed in erotic or affectionate terms, physical sexual acts, including those portrayed as an assault or a forced sexual violent act against one's will, prostitution, pornography, and abuse. |
| Violence | The violence category describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, etc. |
| Self-Harm | The self-harm category describes language related to physical actions intended to purposely hurt, injure, or damage one's body, or kill oneself. |

**Severity levels**

Content flags applied by the service assign a severity level rating, which indicates the severity of displaying the flagged content.

| Severity Level 0 – Safe | Content may be related to violence, self-harm, sexual or hate categories but the terms are used in general, journalistic, scientific, medical, and similar professional contexts that are appropriate for most audiences. |
| --- | --- |
| Severity Level 2 – Low | Content that expresses prejudiced, judgmental, or opinionated views, includes offensive use of language, stereotyping, use cases exploring a fictional world (for example, gaming, literature) and depictions at low intensity. |
| Severity Level 4 – Medium | Content that uses offensive, insulting, mocking, intimidating, or demeaning language towards specific identity groups, includes depictions of seeking and executing harmful instructions, fantasies, glorification, promotion of harm at medium intensity. |
| Severity Level 6 – High | Content that displays explicit and severe harmful instructions, actions, damage, or abuse, includes endorsement, glorification, promotion of severe harmful acts, extreme or illegal forms of harm, radicalization, and non-consensual power exchange or abuse. |

**Custom categories**

With custom categories, Azure AI Content Safety extends its capabilities beyond predefined content categories. Users can now create custom definitions that are unique to their environment, enabling a more personalized and relevant content moderation experience. This feature supports a wide range of use cases, from brand protection to community guidelines enforcement. 

## Capabilities

### System behavior

Azure AI Content Safety uses artificial intelligence to analyze user-generated and AI-generated content and flag any harmful content (for a given severity level) such as hate speech, sexual, violent and self-harm activities. Clear and understandable explanations are provided, allowing users to understand why content was flagged or removed.

Different types of analysis are available in Azure AI Content Safety:

| **Type** | **Functionality** |
| --- | --- |
| Text Detection API | Scans text for hate, sexual, violence, and self-harm content, with multi-severity risk levels. |
| Image Detection API | Scans images for hate, sexual, violence, and self-harm content, with multi-severity risk levels. |
| Multimodal Detection API | Scans both images and text (including separate text or text extracted from an image using optical character recognition) for hate content, with multi-severity risk levels. |
| Azure AI Content Safety Studio | Azure AI Content Safety Studio is an online tool that customers can use to visually explore, understand, and evaluate the Azure AI Content Safety service. The studio provides a platform for customers to experiment with the different Azure AI Content Safety classifications and to interactively sample returned data without writing any code. |

### Use cases

#### Intended uses

Azure AI Content Safety can be used in multiple scenarios. The system's intended uses include:

- **Social media platforms:** Customers can use Azure AI Content Safety on their social media platforms to help prevent the spread of harmful content, such as hate speech, cyberbullying, and pornography.
- **E-commerce websites:** E-commerce customers can use Azure AI Content Safety to help screen product listings and reviews for harmful content, such as fake reviews and offensive language.
- **Gaming platforms:** Gaming platforms can use Azure AI Content Safety to help detect misconduct, as well as to prevent inappropriate behavior in chats and forums.
- **News websites:** News websites can use Azure AI Content Safety to ensure that user comments remain civil and respectful, and to help prevent the spread of misinformation and hate speech.
- **Video-sharing platforms** : Video-sharing platforms can use Azure AI Content Safety to detect and remove inappropriate content, such as violence, hate speech, and pornography.

#### Considerations when choosing other use cases

We encourage customers to leverage Azure AI Content Safety in their innovative solutions or applications. However, here are some considerations when choosing a use case:

- **Customization:** Different applications and solutions might have different requirements when it comes to content safety. It's important to experiment with severity levels for Azure AI Content Safety and set them to meet the needs of your specific use case. Custom categories are intended to enhance content moderation by allowing users to define what is important for their specific context. It is not intended to replace the existing content categories but to complement them, providing a more granular level of content safety.
- **Transparency:** Some end users might want to understand how your application or solution moderates content. When you choose to use Azure AI Content Safety, it's important to ensure that the service provides transparency and clear communication with your users about how content is moderated and why certain content might be flagged or removed.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Limitations

### Technical limitations, operational factors, and ranges

Azure AI Content Safety has some technical limitations that can affect performance. Some of these limitations are:

**Accuracy:** Azure AI Content Safety might not be perfectly accurate in detecting inappropriate content. This is because the system relies on algorithms and machine learning, which can have biases and errors.

**Unsupported languages:** Azure AI Content Safety might not be able to detect inappropriate content in languages that it has not been trained or tested to process. Currently, Azure AI Content Safety is available in English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese.

**Image recognition:** Azure AI Content Safety might not be able to detect inappropriate content in images that are not clearly discernible or that have been edited.

**Evolving nature of content:** Azure AI Content Safety might not keep up with the evolving nature of online content. As new types of inappropriate content emerge (for example, new language or usage patterns), there may be a delay in Azure AI Content Safety's ability to detect these new types of content.

Azure AI Content Safety also has some operational factors that need to be considered for its effectiveness. Some of these factors are:

**Volume of content:** Azure AI Content Safety might struggle to handle large volumes of content. This can lead to delays in detecting inappropriate content.

**Time sensitivity:** Some types of inappropriate content require immediate action. Azure AI Content Safety might be unable to identify these types of content quickly in order to alert moderators.

**Contextual analysis:** Azure AI Content Safety might be unable to analyze content in context to determine whether it is inappropriate. For example, certain words might be appropriate in some contexts but not in others.

**Improve your custom categories:** While custom categories offer increased customization, they may require additional setup and tuning. Users should be aware of the potential need for iterative adjustments to achieve optimal performance. 

It is important to rigorously evaluate Azure AI Content Safety on real data before deploying and to continue monitoring the system once deployed to ensure appropriate performance.

## System performance

In this section, we'll review what performance means for Azure AI Content Safety, best practices for improving performance, and limitations as they relate to Azure AI Content Safety.

**General performance guidelines**

Because Azure AI Content Safety serves various uses, there's no universally applicable estimate of accuracy. The performance of Azure AI Content Safety is affected by the customer use case and data. In the following sections we describe how to understand accuracy for Azure AI Content Safety at a high level.

**Accuracy**

The performance of Azure AI Content Safety is measured by examining how well the system detects harmful content. For example, one might count the true prevalence of harmful content in some text based on human judgment, and then compare with the output of the system from processing the same text. Comparing human judgment with the system recognized entities would allow you to classify the events into two kinds of correct (or "true") events and two kinds of incorrect (or "false") events.

| **Error Type** | **Definition** | **Example** |
| --- | --- | --- |
| True Positive | The model correctly identifies harmful content. | When harmful content such as "you are an idiot" is flagged as hate, the system returns a severity level of 2. The system correctly rejects the harmful content. |
| False Positive | The model incorrectly identifies harmless content as harmful. | When harmless content such as "you are a good person" is flagged as hate and returns a severity level of 4. The system incorrectly blocks the content. |
| True Negative | The model correctly identifies harmless content. | When harmless content such as "you are a good person", the system returns a severity level of 0. The system correctly accepts the content. |
| False Negative | The model fails to identify harmful content. | When harmful content such as "you are an idiot", the system returns a severity level of 0. The system incorrectly accepts the content. |

The consequences of a false positive or a false negative will vary depending upon how you use the Azure AI Content Safety system.

**Severity levels, match severity levels, and matched conditions**

System configuration influences system accuracy. Azure AI Content Safety detects harmful content by comparing the model output severity levels for a given input and uses a match severity level to accept or reject the input as a match.

| **Term** | **Definition** |
| --- | --- |
| Severity levels | The higher the severity of input content, the larger this value is. The values are: 0, 2, 4, or 6. |
| Match Severity Levels (Only Studio has this feature) | Match severity is a configurable value that determines the match severity level required to be considered a positive match. If the match severity level is set to 0, then the system will accept any match severity levels; if the match severity level is set to 6, then it will only accept inputs with a 6 (100%) match severity level. Studio has a default match severity level that you can change to suit your application. |

With your evaluation results, you can adjust the match severity levels for your specific use case and validate your results by testing with your data (only Azure AI Content Safety Studio has this feature). For example, games for children typically have higher content safety requirements than games available for adults only. For children's games, you might set the match severity level lower than the default match severity level. In contrast, for adults the match severity level could be higher than the default. Based on each evaluation result, you can iteratively adjust the match severity level until the trade-off between false positives and false negatives matches the needs in your use case.



### Best practices to improve accuracy

Below are some recommendations to obtain the best results.

**Meet specifications**

The following specifications are important to be aware of:

- **Text and image format:**  The current system only supports text and image inputs.
- Maximum length of text: In Azure AI Content Safety API, the text input limit is 1000 characters per text API call. The fewer characters, the more accurate the result will be.

**Design the system to support human judgment**

We recommend using Azure AI Content Safety to support people making accurate and efficient judgments, rather than fully automating a process. Meaningful human review is important to:

- Detect and resolve cases of misidentification or other failures.
- Provide support to people who believe their content was incorrectly flagged.

For example, in gaming scenarios, legitimate content can be rejected due to having a false positive. In this case, a human reviewer can intervene and help the customer verify the results.

**Use AI features responsibly** 

Use of Azure AI Content Safety is subject to the requirements of the Azure OpenAI Service Code of Conduct. If you will enable end users to create or deploy custom categories using Azure AI Content Safety, those users should be informed of those requirements and bound to adhere to them when using the system. 

### Best practices for improving system performance

Do:

- Monitor the system's performance regularly to ensure that the tradeoff is appropriate for your use case.
- Adjust the severity levels for blocking based on user feedback and observed trends in content safety.
- Consider the impact of the system's performance on different user populations and adjust accordingly. For example, certain words or images may be considered offensive in one culture but not in another, and the system should be trained to detect this and adjust its risk levels accordingly.
- Take steps to mitigate any unintended consequences of adjusting the risk levels for blocking, such as over-removal of content or the spread of harmful content.
- To maximize the effectiveness of custom categories, we recommend: 
    - Clearly defining your custom category. The services will use the definition to augment the training dataset. 
    - Preparing a high quality dataset to cover both positive and negative samples, so the model has more accurate results. 
    - Regularly reviewing and updating the categories based on content trends. 
    - Utilizing user feedback to update category definitions and training samples. 

Don't:

- Set the severity levels too low: If the severity levels for blocking are set too low, the system might flag a lot of content even if it is not harmful. This can negatively affect the user experience by making it difficult for users to post legitimate content without being flagged.
- Set the severity levels too high: Conversely, if the severity levels for blocking are set too high, the content safety system might not flag content as harmful. This can harm users and communities by allowing inappropriate content to be disseminated.
- Ignore feedback from users and communities: Content safety systems are designed to serve the needs of users and communities, and it is important to listen to their feedback about the system's performance. For example, if users are consistently reporting false positives or false negatives, the system should be adjusted accordingly.
- Over-relying on automated decision-making: Content safety systems often rely on automated decision-making to flag inappropriate content, but it is important to ensure appropriate human oversight and intervention to avoid errors and biases. For example, if the system flags content as inappropriate, a human moderator should review the decision to ensure that it is accurate and fair.

## Evaluating and integrating Azure AI Content Safety for your use

### Evaluation methods

Before a large-scale deployment or rollout of any Azure AI Content Safety, system owners should conduct an evaluation phase. The methods used to evaluate a system for content safety considerations typically involve analyzing large datasets of harmful content and evaluating the system's ability to accurately identify and flag potentially harmful or inappropriate content.

It's important to evaluate how the system performs across different demographic groups and geographic areas. The groups of people that are included in the evaluation depend on the type of content that is being evaluated and the intended audience of the system. For example, if the system is designed to monitor social media posts, the dataset might include a diverse range of users from various geographic locations, backgrounds, and age groups. However, if the system is designed for use in a specific industry or niche market, the dataset might be limited to users who are in that specific group.

The evaluation itself might involve a combination of automated testing and manual review by content safety experts to ensure that the system is effectively identifying potentially harmful or inappropriate content. The results of the evaluation are then used to improve the system and to optimize its performance for real-world use.

This evaluation should be conducted in the context where you'll use the system, and with people who will interact with the system. Some best practices for evaluating Azure AI Content Safety include:

- Work with your analytics and research teams to collect ground truth evaluation data.
- Establish baseline accuracy, false positive and false negative rates.
- Choose an appropriate match severity level for your use case.
- Determine whether the error distribution is skewed towards specific groups of data or categories.
- Evaluation is likely to be an iterative process. For example, you can start with 50 rows or images for each category and then assess the false positive and false negative results.
- In addition to analyzing accuracy data, you can also analyze feedback from the people making judgments based on the system output.

> [!WARNING]
> **Content warning: Sample Content in Content Safety Studio.**
>
> Content Safety Studio includes prepopulated data sets to enable you to test the system and tailor it to your requirements. These data sets contain objectionable content to enable this feature to function. This content should be reviewed with discretion. In some cases, image content will be blurred by default, and you can select a toggle to unblur the content.

### Best practices for evaluating and integrating Azure AI Content Safety

- **Appropriate human oversight for the system is critical to ensure that it is being used effectively and responsibly.** This includes ensuring that the people who are responsible for oversight understand the system's intended uses, how to interact with the system effectively, how to interpret system behavior, and when and how to intervene in or override the system. Considerations such as UX and UI design and the use of severity levels can inform human oversight strategies and help prevent over-reliance on system outputs. For example, for a product like a content safety system, it is important to provide content moderators with the training and resources that they need to effectively oversee the system. This might involve providing access to training materials and documentation, as well as ongoing support from content safety experts.
- **Establish feedback channels for users and affected groups.**  AI-powered products and features require ongoing monitoring and improvement. Establish channels to collect questions and concerns from users as well as from people who are affected by the system. For example, build feedback features into the user experience. Invite feedback on the usefulness and accuracy of outputs and give users a separate and clear path to report outputs that are problematic.

## Learn more about responsible AI

[Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

[Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

[Microsoft Azure Learning courses on responsible AI](/learn/paths/responsible-ai-business-principles/)
