---
title: Transparency Note for Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: The Transparency note discusses Azure Language in Foundry Tools and the key considerations for making use of this technology responsibly.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 04/26/2023
---

# Transparency Note for Azure Language in Foundry Tools

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).


## The basics of Azure Language in Foundry Tools

### Introduction
Language is a cloud-based service that provides Natural Language Processing (NLP) features for text mining and text analysis, including the following features:

* [Named Entity Recognition (NER), Personally Identifying Information (PII)](/azure/ai-services/language-service/named-entity-recognition/overview)
* [Text analytics for health](/azure/ai-services/language-service/text-analytics-for-health/overview)
* [Key phrase extraction](/azure/ai-services/language-service/key-phrase-extraction/overview)
* [Language detection](/azure/ai-services/language-service/language-detection/overview)
* [Sentiment analysis and opinion mining](/azure/ai-services/language-service/sentiment-opinion-mining/overview)
* [Question answering](/azure/ai-services/language-service/question-answering/overview)
* [Summarization](/azure/ai-services/language-service/summarization/overview)
* [Custom Named Entity Recognition (Custom NER)](/azure/ai-services/language-service/custom-named-entity-recognition/overview)
* [Custom text classification](/azure/ai-services/language-service/custom-text-classification/overview)
* [Conversational language understanding](/azure/ai-services/language-service/conversational-language-understanding/overview)

Read the overview to get an introduction to each feature and review the example use cases. See the How-to guides and the API reference to understand more details about what each feature does and what gets returned by the system.

This article contains basic guidelines for how to use Language features responsibly. Read the general information first and then jump to the specific article if you're using one of the features below.

* [Transparency note for Named Entity Recognition](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition)
* [Transparency note for Personally Identifying Information](/azure/ai-foundry/responsible-ai/language-service/transparency-note-personally-identifiable-information
* [Transparency note for text analytics for health](/azure/ai-foundry/responsible-ai/language-service/transparency-note-health
* [Transparency note for key phrase extraction](/azure/ai-foundry/responsible-ai/language-service/transparency-note-key-phrase-extraction)
* [Transparency note for language detection](/azure/ai-foundry/responsible-ai/language-service/transparency-note-language-detection)
* [Transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis)
* [Transparency note for question answering](/azure/ai-foundry/responsible-ai/language-service/transparency-note-question-answering)
* [Transparency note for summarization](/azure/ai-foundry/responsible-ai/language-service/transparency-note-extractive-summarization)
* [Transparency note for custom Named Entity Recognition (custom NER)](/azure/ai-foundry/responsible-ai/language-service/custom-named-entity-recognition-transparency-note)
* [Transparency note for custom text classification](/azure/ai-foundry/responsible-ai/language-service/custom-text-classification-transparency-note)
* [Transparency note for conversational language understanding](/azure/ai-foundry/responsible-ai/clu/clu-transparency-note)

## Capabilities 

### Use cases 
Language services can be used in multiple scenarios across a variety of industries. Some examples listed by feature are:

* **Use Custom Named Entity Recognition for knowledge mining to enhance semantic search.** Search is foundational to any app that surfaces text content to users. Common scenarios include catalog or document search, retail product search, or knowledge mining for data science. Many enterprises across various industries want to build a rich search experience over private, heterogeneous content, which includes both structured and unstructured documents. As a part of their pipeline, developers can use custom NER for extracting entities from the text that are relevant to their industry. These entities can be used to enrich the indexing of the file for a more customized search experience. 


* **Use Named Entity Recognition to enhance or automate business processes.** For example, when reviewing insurance claims, recognized entities like name and location could be highlighted to facilitate the review. Or a support ticket could be generated with a customer's name and company automatically from an email.

* **Use Personally Identifiable Information to redact some categories of personal information from documents to protect privacy.**  For example, if customer contact records are accessible to first line support representatives, the company may want to redact unnecessary customer's personal information from customer history to preserve the customer's privacy.

* **Use Language Detection to detect languages for business workflow.** For example, if a company receives email in various languages from customers, they could use language detection to route the emails by language to native speakers for ease of communication with those customers.

* **Use Sentiment Analysis to monitor for positive and negative feedback trends in aggregate.** After the introduction of a new product, a retailer could use the sentiment service to monitor multiple social media outlets for mentions of the product with their sentiment. They could review the trending sentiment in their weekly product meetings.

* **Use Summarization to extract key information from public news articles.** To produce insights such as trends and news spotlights.

* **Use Key Phrase Extraction to view aggregate trends in text data.** For example, a word cloud can be generated with key phrases to help visualize key concepts in text comments or feedback. For example, a hotel could generate a word cloud based on key phrases identified in their comments and might see that people are commenting most frequently about the location, cleanliness and helpful staff.

* **Use Text Analytics for Health for insights and statistics extraction.** Identify medical entities such as symptoms, medications, and diagnoses in clinical notes and diverse clinical documents. Use this information for producing insights and statistics on patient populations, searching clinical documents, research documents and publications.

* **Use Custom Text Classification for automatic email or ticket triaging.** Support centers of all types receive a high volume of emails or tickets containing unstructured, freeform text and attachments. Timely review, acknowledgment, and routing to subject matter experts within internal teams is critical. Email triage at this scale requires people to review and route to the right departments, which takes time and resources. Custom text classification can be used to analyze incoming text, and triage and categorize the content to be automatically routed to the relevant departments for further action.

* **Use Conversational Language Understanding to build end-to-end conversational bots.** Use CLU to build and train a custom natural language understanding model based on a specific domain and the expected users' utterances. Integrate it with any end-to-end conversational bot so that it can process and analyze incoming text in real time to identify the intention of the text and extract important information from it. Have the bot perform the desired action based on the intention and extracted information. An example would be a customized retail bot for online shopping or food ordering.

* **Use Question Answering for customer support.** In most customer support scenarios, common questions are asked frequently. Question Answering lets you instantly create a chat bot from existing support content, and this bot can act as the front-line system for handling customer queries. If the questions can't be answered by the bot, then additional components can help identify and flag the question for human intervention.

## Limitations 

### The quality of the incoming text to the system will affect your results.

Language features only process text. The fidelity and formatting of the incoming text will affect the performance of the system. Make sure you consider the following:

* Speech transcription quality may affect the quality of the results. If your source data is voice, make sure you use the highest quality combination of automatic and human transcription to ensure the best performance. Consider using custom speech models for better quality results.

* Lack of standard punctuation or casing may affect the quality of your results. If you are using a speech system, like Azure Speech in Foundry Tools to Text, be sure to select the option to include punctuation.

* Optical character recognition (OCR) quality may affect the quality of the system. If your source data is images and you use OCR technology to generate the text, incorrectly generated text may affect the performance of the system. Consider using custom OCR models to help improve the quality of results.

* If your data includes frequent misspellings, consider using Bing Spell Check to correct misspellings.

* Tabular data may not be identified correctly depending on how you send the table text to the system. Assess how you send text from tables in source documents to the service. For tables in documents, consider using Azure Document Intelligence in Foundry Tools or a similar service. This will allow you to get the appropriate keys and values to send to Language with contextual keys that are close enough to the values for the system to properly recognize the entities.

* Microsoft trained its Language feature models (with the exception of language detection) using natural language text data that is comprised primarily of fully formed sentences and paragraphs. Therefore, using this service for data that most closely resembles this type of text will yield the best performance. We recommend avoiding use of this service to evaluate incomplete sentences and phrases where possible, as the performance may be reduced.

* The service only supports single language text. If your text includes multiple languages for example "the sandwich was bueno", the output may not be accurate.

* The language code must match the input text language to get accurate results. If you are  unsure about the input language you can use the language detection feature.

### Best practices for improving system performance

Some features of Language return confidence scores and can be evaluated using the approach described in the following sections. Other features which do not return a confidence score (such as key word extraction and summarization) will need to be evaluated using different methods. 

### Understand confidence scores for sentiment analysis, named entity recognition, language detection, and health functions

The sentiment, named entity recognition, language detection and health functions all return a confidence score as a part of the system response. This is an indicator of how confident the service is with the system's response. A higher value indicates that the service is more confident that the result is accurate. For example, the system recognizes entity of category U.S. Driver's License Number on the text **555 555 555** when given the text "My NY driver's license number is 555 555 555" with a score of .75 and might recognize category U.S. Driver's License Number on the text **555 555 555** with a score of .65 when given the text "My NY DL number is 555 555 555". Given the more specific context in the first example, the system is more confident in its response.
In many cases, the system response can be used without examining the confidence score. In other cases, you can choose to use a response only if its confidence score is above a specified confidence score threshold.

### Understand and measuring performance

The performance of Language features is measured by examining how well the system recognizes the supported NLP concepts (at a given threshold value in comparison with a human judge.) For named entity extraction (NER), for example, one might count the true number of phone number entities in some text based on human judgement, and then compare with the output of the system from processing the same text. Comparing human judgement with the system recognized entities would allow you to classify the events into two kinds of correct (or "true") events and two kinds of incorrect (or "false") events.

| Outcome | Correct/Incorrect | Definition | Example |
|---------|-------------------|------------|---------|
| True Positive | Correct | The system returns the same result that would be expected from a  human judge. | The system correctly recognizes PII entity of category **Phone Number** on the text **1-234-567-8910** when given the text: "You can reach me at my office number 1-234-567-9810."  |
| True Negative | Correct | The system does not return a result, and this aligns with what would be expected from human judge. | The system does not recognize any PII entity when given the text: "You can reach me at my office number." |
| False Positive | Incorrect | The system returns a result where a human judge would not. | The system incorrectly recognizes PII entity of category **Phone Number** for the text office number when given the text: "You can reach me at my office number."  |
| False Negative | Incorrect | The system does not return a result when a human judge would. | The system incorrectly misses a **Phone Number** PII entity on the text **1-234-567-8910** when given the text: "You can reach me at my office number 1-234-567-9810." |

Language features will not always be correct. You'll likely experience both false negative and false positive errors. It's important to consider how each type of error will affect your system. Carefully think through scenarios where true events won't be recognized and where incorrect events will be recognized and what the downstream effects might be in your implementation. Make sure to build in ways to identify, report and respond to each type of error. Plan to periodically review the performance of your deployed system to ensure errors are being handled appropriately.

### How to set confidence score thresholds

You can choose to make decisions in your system based on the confidence score the system returns. You can adjust the confidence score threshold your system uses to meet your needs. If it is more important to identify all potential instances of the NLP concepts you want, you can use a lower threshold. This means that you may get more false positives but fewer false negatives. If it is more important for your system to recognize only true instances of the feature you're calling, you can use a higher threshold. If you use a higher threshold, you may get fewer false positives but more false negatives. Different scenarios call for different approaches. In addition, threshold values may not have consistent behavior across individual features of Language and categories of entities. For example, do not make assumptions that using a certain threshold for NER category Phone Number would be sufficient for another NER category, or that a threshold you use in NER would work similarly for Sentiment Analysis. Therefore, it is critical that you test your system with any thresholds you are considering using with real data to determine the effects of various threshold values of your system in the context that it will be used.

### Fairness

At Microsoft, we strive to empower every person on the planet to achieve more. An essential part of this goal is working to create technologies and products that are fair and inclusive. Fairness is a multi-dimensional, sociotechnical topic and impacts many different aspects of our product development. You can learn more about Microsoft’s approach to fairness [here](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1%3aprimaryr6). 

One dimension we need to consider is how well the system performs for different groups of people. This may include looking at the accuracy of the model as well as measuring the performance of the complete system. Research has shown that without conscious effort focused on improving performance for all groups, it is often possible for the performance of an AI system to vary across groups based on factors such as race, ethnicity, language, gender, and age.

Each service and feature is different, and our testing may not perfectly match your context or cover all scenarios required for your use case. We encourage developers to thoroughly evaluate error rates for the service with real-world data that reflects your use case, including testing with users from different demographic groups. 

For Language, certain dialects and language varieties within our supported languages and text from some demographic groups may not yet have enough representation in our current training datasets. We encourage you to review our [responsible use guidelines](guidance-integration-responsible-use.md), and if you encounter performance differences, we encourage you to let us know.

## Performance varies across features and languages

Various languages are supported for each Language feature. You may find that performance for a particular feature is not consistent with another feature. Also, you may find that for a particular feature that performance is not consistent across various languages.

## Next steps

If you are using any of the features below, be sure to review the specific information for that feature.

## See also

* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for text analytics for health](transparency-note-health.md)
* [Transparency note for key phrase extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for language detection](transparency-note-language-detection.md)
* [Transparency note for question answering](transparency-note-question-answering.md)
* [Transparency note for summarization](transparency-note-extractive-summarization.md)
* [Transparency note for sentiment analysis](transparency-note-sentiment-analysis.md)
* [Transparency note for custom Named Entity Recognition (NER)](custom-named-entity-recognition-transparency-note.md)
* [Transparency note for custom text classification](custom-text-classification-transparency-note.md)
* [Transparency note for conversational language understanding](..\clu\clu-transparency-note.md)

Also, make sure to review:

* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
* [Data Privacy for Language](data-privacy.md)
