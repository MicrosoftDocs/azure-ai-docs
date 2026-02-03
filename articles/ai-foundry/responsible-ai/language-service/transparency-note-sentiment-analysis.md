---
title: Transparency note - Sentiment Analysis feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: The Sentiment Analysis feature of Azure Language in Foundry Tools evaluates text and returns sentiment scores and labels for each sentence. This is useful for detecting positive, neutral and negative sentiment in social media, customer reviews, discussion forums and other product and service scenarios.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 08/12/2022
---

# Transparency note for Sentiment Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> This article assumes that you're familiar with guidelines and best practices for Azure Language in Foundry Tools. For more information, see [Transparency note for Language](transparency-note.md).

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI Principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Sentiment Analysis

### Introduction

The Sentiment Analysis feature of Language evaluates text and returns sentiment scores and labels for each sentence. This is useful for detecting positive, neutral and negative sentiment in social media, customer reviews, discussion forums and other product and service scenarios. 

## Capabilities

### System behavior 

Sentiment analysis provides sentiment labels (such as "negative", "neutral" and "positive") based on the highest confidence score found by the service at a sentence and document-level. This feature also returns confidence scores between 0 and 1 for each document and sentence for positive, neutral and negative sentiment. Scores closer to 1 indicate a higher confidence in the label's classification, while lower scores indicate lower confidence. By default, the overall sentiment label is the greatest of the three confidence scores, however, you can define a threshold for any or all of the individual sentiment confidence scores depending on what works best for your scenario. For each document or each sentence, the predicted scores associated with the labels (positive, negative and neutral) add up to 1. Read more details about [sentiment labels and scores](/azure/ai-services/language-service/sentiment-opinion-mining/how-to/call-api).

In addition, the optional opinion mining feature returns aspects (such as the attributes of products or services) and their associated opinion words. For each aspect an overall sentiment label is returned along with confidence scores for positive and negative sentiment. For example, the sentence "The restaurant had great food and our waiter was friendly" has two aspects, "food" and "waiter," and their corresponding opinion words are "great" and "friendly." The two aspects therefore receive sentiment classification `positive`, with confidence scores between 0 and 1.0. Read more details about [opinion mining](/azure/ai-services/language-service/sentiment-opinion-mining/how-to/call-api#opinion-mining).

[See the JSON response for this example](/azure/ai-services/language-service/sentiment-opinion-mining/quickstart?pivots=rest-api).

### Use cases

Sentiment Analysis can be used in multiple scenarios across a variety of industries. Some examples include:

* **Monitor for positive and negative feedback trends in aggregate**. After introducing a new product, a retailer can use the sentiment service to monitor multiple social media outlets for mentions of the product and its associated sentiment. The trending sentiment can be used in product meetings to make business decisions about the new product.
* **Run sentiment analysis on raw text results of surveys to gain insights for analysis and follow-up with participants (customers, employees, consumers, etc.)**. A store with a policy to follow up on customers' negative reviews within 24 hours and positive reviews within a week can use the sentiment service to categorize reviews for easy and timely follow up.
* **Help customer service staff improve customer engagement through insights captured from real-time analysis of interactions**. Extract insights from transcribed customer services calls to better understand customer-agent interactions and trends to improve customer engagements.

### Considerations when choosing a use case

* **Avoid automatic actions without human intervention for high impact scenarios**. For example, employee bonuses should not be automatically based on sentiment scores from their customer service interaction text. Source data should always be reviewed when a person's economic situation, health or safety is affected. 
* **Carefully consider scenarios outside of the product and service review domain**. Since the model is trained on product and service reviews, the system may not accurately recognize sentiment focused language in other domains. Always make sure to test the system on operational test datasets to ensure you get the performance you need. Your operational test dataset should reflect the real data your system will see in production with all the characteristics and variation you will have when your product is deployed. Synthetic data and tests that don't reflect your end-to-end scenario likely won't be sufficient.
* **Carefully consider scenarios that take automatic action to filter or remove content**. You can add a human review cycle and/or re-rank content (rather than filtering it completely) if your goal is to ensure content meets your community standards.
* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Limitations

Depending on your scenario and input data, you could experience different levels of performance. The following information is designed to help you understand system limitations and key concepts about performance as they apply to Sentiment Analysis.

Key limitations to consider:

* The machine learning model that is used to predict sentiment was trained on product and service reviews. That means the service will perform most accurately for similar scenarios and less accurately for scenarios outside the scope of the product and service reviews. For example, personnel reviews may use different language to describe sentiment and thus, you might not get the results or performance you would expect. A word like "strong" in the phrase "Shafali was a strong leader" may not obtain a positive sentiment because the word strong may not have a clear positive sentiment in product and service reviews.

* Since the model is trained on product and service reviews, dialects and language that are less represented in the dataset may have lower accuracy.

* The model has no understanding of the relative importance of various sentences that are sent together. Since the overall sentiment is a simple aggregate score of the sentences, the overall sentiment score may not agree with a human's interpretation which would take into account the fact that some sentences may have more importance in determining the overall sentiment.

* The model may not recognize sarcasm. Context, like tone of voice, facial expression, the author of the text, the audience for the text, or prior conversation are often important to understanding the sentiment. With sarcasm, additional context is often needed to recognize if a text input is positive or negative. Given that the service only sees the text input, classifying sarcastic sentiment may be less accurate. For example, that was awesome, could be either positive or negative depending on the context, tone of voice, facial expression, author and the audience.

* The confidence score magnitude does not reflect the intensity of the sentiment. It is based on the confidence of the model for a particular sentiment (positive, neutral, negative). Therefore, if your system depends on the intensity of the sentiment, consider using a human reviewer or post processing logic on the individual opinion scores or the original text to help rank the intensity of the sentiment. 

* While we’ve made efforts to reduce the bias exhibited by our models, the limitations that come with language models, including the potential for it to produce inaccurate, unreliable, and biased output, apply to the Language Sentiment Analysis model. We expect the model to have some false negatives and positives for now, but we are eager to collect user feedback to aid our ongoing work to improve this service.

### Best practices for improving system performance

Because sentiment is somewhat subjective, it is not possible to provide a universally applicable estimate of performance for the model. Ultimately, performance depends on a number of factors such as the subject domain, the characteristics of the text processed, the use case for the system, and how people interpret the system's output.

You may find confidence scores for positive, negative, and neutral sentiments differ according to your scenario. Instead of using the overall sentence level sentiment for the full document or sentence, you can define a threshold for any or all of the individual sentiment confidence scores that works best for your scenario. For example, if it is more important to identify all potential instances of negative sentiment, you can use a lower threshold on the negative sentiment instead of looking at the overall sentiment label. This means that you may get more false positives (neutral or positive text being recognized as negative sentiment), but fewer false negatives (negative text not recognized as negative sentiment). For example, you might want to read all product feedback that has some potential negative sentiment for ideas for product improvement. In that case, you could use the negative sentiment score only and set a lower threshold. This may lead to extra work because you'd end up reading some reviews that aren't negative, but you're more likely to identify opportunities for improvement. If it is more important for your system to recognize only true negative text, you can use a higher threshold or use the overall sentiment label. For example, you may want to respond to product reviews that are negative. If you want to minimize the work to read and respond to negative reviews, you could only use the overall sentiment prediction and ignore the individual sentiment scores. While there may be some negative sentiment predicted that you miss, you're likely to get most of the truly negative reviews. Threshold values may not have consistent behavior across scenarios. Therefore, it is critical that you test your system with real data that it will process in production.

## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for Health](transparency-note-health.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Data Privacy and Security for  Language](data-privacy.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
