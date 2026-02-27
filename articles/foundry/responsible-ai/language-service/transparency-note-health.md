---
title: Transparency note - Health feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Foundry Tool for language includes a feature that uses natural language processing techniques to find and label valuable health information, such as diagnosis, symptoms, medications and treatments in unstructured text documents.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 02/01/2023
---

# Transparency note for Text Analytics for health

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> Text Analytics for health is a capability provided “AS IS” and “WITH ALL FAULTS.” Text Analytics for health is not intended or made available for use as a medical device, clinical support, diagnostic tool, or other technology intended to be used in the diagnosis, cure, mitigation, treatment, or prevention of disease or other conditions, and no license or right is granted by Microsoft to use this capability for such purposes. This capability is not designed or intended to be implemented or deployed as a substitute for professional medical advice or healthcare opinion, diagnosis, treatment, or the clinical judgment of a healthcare professional, and should not be used as such. The customer is solely responsible for any use of Text Analytics for health. The customer must separately license any and all source vocabularies it intends to use under the terms set for that UMLS Metathesaurus License Agreement Appendix or any future equivalent link. The customer is responsible for ensuring compliance with those license terms, including any geographic or other applicable restrictions.
>
> Text Analytics for health now allows extraction of Social Determinants of Health (SDOH) and ethnicity mentions in text. This capability may not cover all potential SDOH and does not derive inferences based on SDOH or ethnicity (for example, substance use information is surfaced, but substance abuse is not inferred). All decisions leveraging outputs of the Text Analytics for health that impact individuals or resource allocation (including, but not limited to, those related to billing, human resources, or treatment managing care) should be made with human oversight and not be based solely on the findings of the model. The purpose of the SDOH and ethnicity extraction capability is to help providers improve health outcomes and it should not be used to stigmatize or draw negative inferences about the users or consumers of SDOH data, or patient populations beyond the stated purpose of helping providers improving health outcomes.

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft’s Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system. 

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Responsible AI principles](https://www.microsoft.com/en-gb/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6) from Microsoft.

## The basics of Text Analytics for health

### Introduction

The Text Analytics for health feature of Azure Language in Foundry Tools uses natural language processing techniques to find and label valuable health information such as diagnoses, symptoms, medications, and treatments in unstructured text. The service can be used for diverse types of unstructured medical documents, including discharge summaries, clinical notes, clinical trial protocols, medical publications, and more. Text Analytics for health performs Named Entity Recognition (NER), extracts relations between identified entities, surfaces assertions such as negation and conditionality, and links detected entities to common vocabularies.

Text Analytics for health can receive unstructured text in English as part of its general availability offering. Additional languages are currently supported in a preview offering. For more information, see [Language support](/azure/ai-services/language-service/text-analytics-for-health/language-support).

You can [read an overview](/azure/ai-services/language-service/text-analytics-for-health/overview) of the API and its capabilities. Also, see [supported entities and relations](/azure/ai-services/language-service/text-analytics-for-health/concepts/health-entity-categories). 

Additionally, customization is now offered for Text Analytics for health under the new preview feature, custom Text Analytics for health. [Custom Text Analytics for health](/azure/ai-services/language-service/custom-text-analytics-for-health/overview) allows customers to use their own data train a custom NER model, designed for healthcare, to extract their domain specific categories, extending the existing Text Analytics for health entity map. Customers can also define lexicon or specific vocabulary for the newly defined custom entities as well as existing Text Analytics for health entities such as Medication Name. Therefore, custom Text Analytics for health offers the same capabilities offered by Text Analytics for health along with the ability to extend the existing entity map by adding new ML entities and adding custom vocabulary to existing entities.  

### Key terms

Text Analytics for health currently performs Named Entity Recognition (NER), relation extraction, assertion detection, and entity linking for biomedical text. It can also be supplemented with additional custom entity extraction using entity learned and list components, now available using custom Text Analytics for health.

|Term  |Definition |
|--|--|
|Named Entity Recognition |Detects words and phrases that are mentioned in unstructured text that can be associated with one or more semantic types, such as diagnosis, medication name, symptom or sign, or age. |
|Relation extraction | Identifies meaningful connections between concepts that are mentioned in text. For example, a "time of condition" relation is found by associating a condition name with a time.|
|Assertion detection | Surfaces entity modifiers that are mentioned in text, such as negation or conditionality. The meaning of medical content might be highly affected by these modifiers.|
|Entity linking |Disambiguates distinct entities by associating named entities that are mentioned in text with concepts that are found in a predefined database of concepts, such as in the Unified Medical Language System (UMLS). |
|Entity Learned Component | Allows the definition of new custom entities such as treatment, facility, or medical instrument through training a custom model with labeled data.|
|Entity List Component|Allows the extraction of new custom entities or existing Text Analytics for health entities using a lexicon recognizer by defining a list of synonyms or vocabulary corresponding to the entities of choice. For example, “Medication A” can be defined as a new list value under the medication name entity. |


## Capabilities

### System Behavior 

To use Text Analytics for health, you input raw, unstructured text for analysis, and the API output is handled in your application. Four key functions are performed in a single API call: entity recognition, relation extraction, entity linking, and assertion detection. Analysis is performed as-is, with no additional customization of the pretrained model. 
You can use Text Analytics for health either through a hosted API or by deploying it in a container in your on-premises environment. For more information, see [how to call Text Analytics for health](/azure/ai-services/language-service/text-analytics-for-health/how-to/call-api).

To customize Text Analytics for health, use custom Text Analytics for health’s authoring experience to create new entities that will extend the existing prebuilt entity map. You can also define new vocabulary to be recognized using exact matching for new custom entities as well as existing prebuilt entity categories such as Medication Name. After defining your project’s entity map, you can train and deploy the custom model to make predictions. The deployed custom model, by default, supports all the capabilities already included in Text Analytics for health for the prebuilt entity categories. Additionally, the custom model features custom NER for the new entity categories as well as any dictionary defined for the prebuilt entities. Therefore, predictions to the custom model performs named entity recognition, relation extraction, entity linking, and assertion detection for the Text Analytics for health entities and custom named entity recognition to extract customer defined entity categories along with defined vocabulary for new and existing entity categories. All the data used to train your custom model will be stored in your private blob storage. Additionally, calling your custom model requires your APIM subscription key, which means that your custom model is available only to users with whom you have shared your secret key.      



### Intended use cases

Text Analytics for health can be used in multiple scenarios across a variety of industries that this type of system supports. Some common customer motivations for using Text Analytics for health include:

* Assist and automate the processing of medical documents for proper coding to improve accuracy of care and billing.
* Increase efficiency of analyzing healthcare data to help drive success of value-based care models (for example, Medicare).
* Improve the aggregation of key data for tracking trends of patient care and history without adding overhead to healthcare providers.
* Make progress toward adopting HL7 standards, which is the framework for the exchange, integration, sharing, and retrieval of electronic health information in support of the daily clinical practice and management and overall delivery and evaluation of health services.

The same use cases and considerations apply to custom Text Analytics for health,  but custom Text Analytics for health is better suited for scenarios where the customer has data and would like to extend the existing prebuilt entity map by creating their own entity categories or defining vocabulary for new and existing entity categories. 


### Example use cases

The following use cases are popular examples for applications of the Text Analytics for health and custom Text Analytics for health features:

* **Insights and statistics extraction.** Identify medical entities such as symptoms, medications, and diagnoses in clinical notes and diverse clinical documents. Use this information to produce insights and statistics about patient populations, to search clinical documents, and to research documents and publications.
* **Creation of predictive analytics and predictive models from historic data.** Enables the development of solutions for planning, decision support, risk analysis, and more based on prediction models created by using historic data.
* **Assisted annotation and curation.** Support solutions for clinical data annotation and curation. For example, to support clinical coding, digitization of data that was manually created, and automation of registry reporting.
* **Support solutions for displaying or analyzing health-related information.** Support solutions to display or analyze health-related information. For example, for reporting purposes, support quality assurance processes or flag possible errors to be reviewed by a human.

### Considerations when choosing a use case

Text Analytics for health is a valuable tool when you manage and extract knowledge from unstructured medical text. However, given the sensitive nature of health-related data, it's important to consider your use cases carefully. In all cases, a human should be making decisions assisted by the information the system returns, and in all cases, you should have a way to review the source data and correct errors. Here are some additional considerations when choosing a use case:

* **Avoid scenarios that use this service as a medical device, to provide clinical support, or as a diagnostic tool to be used in the diagnosis, cure, mitigation, treatment, or prevention of disease or other conditions without human intervention.** A qualified medical professional should always do due diligence and verify source data that might influence patient care decisions.
* **Avoid scenarios related to automatically granting or denying medical services or health insurance without human intervention.** Because decisions that affect coverage levels are extremely impactful, source data should always be verified in these scenarios. 
* **Avoid scenarios that use personal health information for a purpose not permitted by patient consent or applicable law.** Health information has special protections regarding privacy and consent. Make sure that all data you use has patient consent for the way you use the data in your system or you are otherwise compliant with applicable law as it relates to the use of health information.
* **Carefully consider using detected entities to automatically update patient records without human intervention.** Make sure that there is always a way to report, trace, and correct any errors to avoid propagating incorrect data to other systems. Ensure that any updates to patient records are reviewed and approved by qualified professionals. 
* **Carefully consider using detected entities in patient billing without human intervention.** Make sure that providers and patients always have a way to report, trace, and correct data that generates incorrect billing.
* **Carefully consider scenarios that make use of the detected Social Determinants of Health and ethnicity entities.** Always make sure that there is a way to report, trace, and correct any errors to avoid erroneous substance use inference or offering an incorrect form of care based on social and demographic factors.
* **Carefully consider scenarios that use an automated feedback loop in finetuning the custom Text Analytics for health model.** Always make sure to test and evaluate the model prior to deploying to a production environment to avoid model quality regression because custom model training is an iterative process that is very sensitive to the input training data.    
* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Social Determinants of Health and Ethnicity 

Text Analytics for health allows extraction of Social Determinants of Health (SDOH) and ethnicity mentions in text. Using social and demographics entities might help you unlock mentions of an array of factors besides direct medical care that can drive health outcomes, such as underlying genetics, health behaviors, and social and environmental factors. By leveraging the Text Analytics for health SDOH entity extraction capability, you might be able to reduce health disparities that are often rooted in social and economic disadvantages, improve care, assess health inequity issues, and incorporate underrepresented groups into clinical trials and research. For more information, see [Social determinants of health](https://www.who.int/health-topics/social-determinants-of-health#tab=tab_1), [FDA Takes Important Steps to Increase Racial and Ethnic Diversity in Clinical Trials | FDA and County Health Rankings: Relationships Between Determinant Factors and Health Outcomes](https://www.sciencedirect.com/science/article/abs/pii/S0749379715005140).

This capability doesn’t derive inferences based on SDOH or ethnicity (for example, substance use information is surfaced from the input text, but substance abuse is not inferred based on extracted entities). All decisions that rely on the outputs of Text Analytics for health and that impact individuals or resource allocation (including but not limited to decisions related to billing, human resources, or managing care) should be made with human oversight and not be based solely on the findings of the model. The purpose of the SDOH and ethnicity extraction capabilities is to help providers improve health outcomes. They should not be used to stigmatize or draw negative inferences about the users or consumers of SDOH data or of patient populations beyond the stated purpose of helping providers improve health outcomes.
As with other extracted entities, the Text Analytics for health response also returns a confidence score for living status, employment, substance use, and ethnicity entities. Carefully consider the confidence score in the context of an entity’s intended use.

## Custom Text Analytics for health

Text Analytics for health enables developers to process and extract insights from unstructured medical data. Although the health feature is capable of processing and extracting a broad range of data types and entity categories, there are still cases where the customer might like to add a new entity type specific to their data or even define additional medical vocabulary in an existing entity category. 

Therefore, the purpose of Custom Text Analytics for health is to provide a means of customizing on top of Text Analytics for health by giving customers the ability to extend the entity map with completely new entity categories specific to their data, as well as the ability to add custom vocabulary to the existing entity categories.

Custom Text Analytics for health allows customers to train a custom healthcare entity extraction ML model using their labeled data and custom dictionaries/vocabularies. This will allow customers to define new medical entities that are specific to their data. The service will also internally call Text Analytics for health, providing all the features and entity map already given in Text Analytics for health. As an added level of customization, customers will be able to add their own vocabulary to existing Text Analytics for health entities in order to supplement the prebuilt response with their data. 

The customer is responsible for providing sufficient labelled data and vocabulary to train the custom model; therefore, performance of the model may vary depending on the quality and comprehensiveness of the labeled training data used by the customer relative to the new entity categories to be defined. It is recommended to always test and evaluate the model prior to deploying to a production environment to avoid model quality regression because custom model training is an iterative process that is very sensitive to the input training data.  



## Limitations

* **Coverage**: SDOH extraction capability might not cover all potential SDOH. Recognition is limited to ethnicity and the entity types listed here Entity categories recognized by Text Analytics for health - Foundry Tools | Microsoft Learn.
* **Languages**: Currently, SDOH and ethnicity extraction capabilities are enabled for English text only. Text Analytics for health can receive unstructured text in English as part of its general availability offering. Additional languages are currently supported in a preview offering.
* **Spelling**: Incorrect spelling might affect the output. Specifically, entity linking looks for terms and synonyms based only on a specific, correct spelling. If a drug name, for example, is misspelled, the system might have enough information to recognize that the text is a drug name, but it might not identify the link as it would for the correctly spelled drug name.
* **Performance**: Potential error types have been outlined in the System performance section below.
* **Custom Text Analytics for health (in preview)**: Supports all the languages supported by Text Analytics for health. To train a custom model you need to supply the training service with a minimum of 10 labels for each newly defined custom entity category. In order to train a custom model, the customer must add a minimum of 10 documents to the project’s dataset. Lexicon recognizers used for extracting customer defined vocabulary rely on exact case matching in the specified language, meaning that the customer must add all variants of the specific word and include it for all the input languages for their project. When using custom Text Analytics for health, entity linking, relationship extraction, and assertion detection will be supported for Text Analytics for health entities but will not be returned for any newly defined custom entity categories.

## System Performance

Text Analytics for health and custom Text Analytics for health in general might have both false positive errors and false negative errors for each capability supported by the health feature. Several examples of the potential error types are described in the next sections.


### Named Entity Recognition (NER)

**False positive**

In NER, a false positive occurs when the system incorrectly identifies an entity as belonging in a category. In the following example, COVID-19 is mislabeled as EXAMINATION_NAME. In fact, COVID-19 is a diagnosis, not the name of an examination. So, this is a false positive for EXAMINATION_NAME.

In the second example, vodka is a false positive for MEDICATION_NAME. Instead, it should be classified as SUBSTANCE_USE.

:::image type="content" source="./media/named-entity-resolution-false-positive.png" alt-text="A screenshot of Named Entity Recognition False Positive."::: 

:::image type="content" source="./media/substance-use-misclassification.png" alt-text="A screenshot of Substance Use Misclassification."::: 

**False negative**

A false negative in NER occurs when an entity should have been identified as belonging in a category, but it wasn't. In the following example, the entity ER should have been identified as CARE_ENVIRONMENT, but it wasn’t. If an entity isn’t properly recognized, the linked code won’t be recognized either.

:::image type="content" source="./media/named-entity-resolution-false-negative.png" alt-text="A screenshot of Named Entity Recognition False Negative.":::

In the next two examples, a second mention of ETHNICITY and information about previous employment aren’t properly recognized.

:::image type="content" source="./media/ethnicity-misclassification.png" alt-text="A screenshot of Ethnicity Misclassification.":::

:::image type="content" source="./media/employment-misclassification.png" alt-text="A screenshot of Employment Misclassification.":::


### Relation Extraction

**False positive**

In relation extraction, a false positive occurs when a relation should not have been identified, but it was. In the next example, the value of the AST examination was incorrectly attributed to the ALT examination, which already has a measurement value assigned to it.

:::image type="content" source="./media/relation-extraction-false-negative.png" alt-text="A screenshot of Relation Extraction False Negative.":::

**False negative**

A false negative in relation extraction occurs when a relation should have been recognized, but it wasn't. In the preceding example, the measurement value of 45 was not assigned to the AST examination, and it should have been.


### Entity Linking 

**False positive**

Entity linking is achieved by looking for an exact match between concepts in common vocabularies and the recognized entity. A false positive for entity linking would happen in the rare cases when an entity is captured while it shouldn’t have been (false positive NER) and a matching concept appears to exist in the vocabulary. A false positive for entity linking might also happen for ambiguous terms having several distinct matching concepts in the common vocabularies.

**False negative**

Because entity linking is an exact match with the original text, you can get a false negative if there's enough signal to properly recognize the entity but the spelling of that entity is not correct in the text. For example, in the following text where therapies is misspelled, you would not get the appropriate linked entity UMLS: C0087111.

:::image type="content" source="./media/entity-linking-false-negative.png" alt-text="A screenshot of Entity Linking False Negative.":::

### Assertion Detection

**False positive**

In assertion detection, a false positive occurs when the system identifies an assertion that should not exist in the text. In the following example, the entity respiratory disease is incorrectly negated as a DIAGNOSIS for COVID-19.

:::image type="content" source="./media/negation-detection-resolution-false-positive.png" alt-text="A screenshot of Negation Detection False Positive.":::

**False negative**

A false negative in assertion detection occurs when an assertion is not captured. In the following example, the symptom “respond” should be negated because there was no response to the mentioned medication.

:::image type="content" source="./media/negation-detection-resolution-false-negative.png" alt-text="A screenshot of Negation Detection False Negative.":::

### Best practices for improving system performance

* Custom Text Analytics for health’s custom vocabulary uses exact word matching; therefore, incorrect spelling may affect entity extraction. 
* To improve the quality of custom Text Analytics for health’s ML-based entity extraction using Learned entity components, it is recommended to include an equal distribution of labels for each custom entity as well as a minimum of 15 labels for each entity of examples that are representative of the input data.

## Evaluation of Text Analytics for Health

### Evaluation methods

Text Analytics for health is trained and evaluated on diverse types of unstructured medical documents, including discharge summaries, clinical notes, clinical trial protocols, medical publications, and more. The SDOH model, which surfaces living status, employment, and substance use entities, is trained and evaluated on a manually annotated dataset that comes from two independent sources: approximately 750 randomly sampled proprietary clinical notes and about 1,500 clinical notes randomly sampled from a corpus provided by a US medical center and focused mostly on adult patients. The original corpus covers more than 10 years of collected data and thousands of patient admissions. It provides almost equal representation of male and female patients. It should be noted that no further analysis of the training data representativeness (for example, geographic, demographic, or ethnographic representation) has been performed. Even though internal tests demonstrate the model’s potential to generalize to different populations and geographies, you should carefully consider how the training and evaluation data is representative in the context of your intended use.
To evaluate the system in relation to potential fairness harms, the evaluation dataset was split into subgroups of documents by social and demographic factors, such as gender, age, ethnicity, employment, and living status. Targeted minimum performance levels for each group were evaluated, as were relative performance differences between groups. 

### Evaluation of custom Text Analytics for Health

Custom Text Analytics for health leverages a custom healthcare base model that gets finetuned by customer- provided data in addition to the prebuilt Text Analytics for health model. The healthcare base model used is the same base model that the Text Analytics for health entity map is built on.

Custom Text Analytics for health features an internal evaluation as part of the authoring experience; this enables the customer to create a testing dataset and review the F1, precision, and recall scores for the defined custom entity categories. Text Analytics for health prebuilt entities are not included in the internal evaluation. The experience also features model guidance to provide the customer with ways of improving the resulting scores from the testing such as recommending additional labels for entities that are not performing well.


### Evaluating and integrating Text Analytics for health for your use

Microsoft wants to help you responsibly develop and deploy solutions that use Language. These considerations are in line with our commitment to developing responsible AI.
When you decide how to use and implement products and solutions powered by Language features, consider the following factors.

## General guidelines

When you're getting ready to deploy Text Analytics for health, the following activities help set you up for success:

* **Understand what it can do**: Fully assess the capabilities of Text Analytics for health to understand its capabilities and limitations. Understand how it will perform in your scenario and context.
* **Test with real, diverse data**: Understand Text Analytics for health will perform in your scenario by thoroughly testing it by using real-life conditions and data that reflect the diversity in your users, geography, and deployment contexts. Small datasets, synthetic data, and tests that don't reflect your end-to-end scenario are unlikely to sufficiently represent your production performance.
* **Respect an individual's right to privacy**: Only collect or use data and information from individuals for lawful and justifiable purposes. Use only the data and information that you have consent to use or are legally permitted to use.
* **Legal review**: Obtain appropriate legal review of your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and any risks that need to be mitigated prior to use. It is your responsibility to mitigate such risks and resolve any issues that might come up. 
* **System review**: If you plan to integrate and responsibly use an AI-powered product or feature into an existing system for software or customer or organizational processes, take time to understand how each part of your system will be affected. Consider how your AI solution aligns with Microsoft Responsible AI principles.
* **Human in the loop**: Keep a human in the loop and include human oversight as a consistent pattern area to explore. This means constant human oversight of the AI-powered product or feature and ensuring the role of humans in making any decisions that are based on the model’s output. To prevent harm and to manage how the AI model performs, ensure that humans have a way to intervene in the solution in real time.
* **Security**: Ensure that your solution is secure and that it has adequate controls to preserve the integrity of your content and prevent unauthorized access.
* **Customer feedback loop**: Provide a feedback channel that users and individuals can use to report issues with the service after it's deployed. After you deploy an AI-powered product or feature, it requires ongoing monitoring and improvement. Have a plan and be ready to implement feedback and suggestions for improvement.


## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Data Privacy and Security for  Language](data-privacy.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
