---
title: Understanding Confidence Scores in Azure AI Content Understanding.
titleSuffix: Azure AI services
description: Best practices to interpret and improve Azure AI Content Understanding accuracy and confidence scores.
author: laujan
ms.author: admaheshwari
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 02/20/2025
---

# Interpret and improve accuracy and confidence scores

A confidence score indicates probability by measuring the degree of statistical certainty that the extracted result is detected correctly. The estimated accuracy is calculated by running a few different combinations of the training data to predict the labeled values. In this article, we share how to interpret accuracy and confidence scores and best practices for using those scores to improve accuracy and confidence results.


Understanding Confidence Scores
What are confidence scores?
Confidence scores represent the probability that the extracted result is correct. For example, a confidence score of 0.95 (95%) suggests that the prediction is likely correct 19 out of 20 times. These scores are derived from various factors, including the quality of the input document, the similarity between the training data and the document being analyzed, and the model's ability to recognize patterns and features in the document.
Why are confidence scores important?
Confidence scores are important because they provide a measure of the model's certainty in its predictions. They help users make informed decisions about the reliability of the extracted data and determine whether human review is necessary. Confidence scores also play a crucial role in automating workflows and improving efficiency by reducing the need for manual validation.
Supported fields
Confidence scores are supported for extractive fields, including text, tables for documents and speech transcription. The specific fields supported may vary depending on the model and the use case.

JSON output for documents
"fields": {
                    "ClientProjectManager": {
                        "type": "string",
                        "valueString": "Nestor Wilke",
                        "spans": [
                            {
                                "offset": 4345,
                                "length": 12
                            }
                        ],
                        "confidence": 0.964,
                        "source": "D(2,3.5486,8.3139,4.2943,8.3139,4.2943,8.4479,3.5486,8.4479)"
                    },
What are thresholds for confidence scores?
Thresholds for confidence scores are predefined values that determine whether a prediction is considered reliable or requires further review. These thresholds can be set across different modalities to ensure consistent and accurate results. Setting appropriate thresholds is important because it helps balance the trade-off between automation and accuracy. By setting the right thresholds, users can ensure that only high-confidence predictions are automated, while low-confidence predictions are flagged for human review. This helps improve the overall accuracy and reliability of the predictions

Improving Confidence Scores
What are some common challenges with confidence scores?
Common challenges with confidence scores include low-quality input documents, variability in document types, complexity of the documents, and limitations of the model in recognizing certain types of content or features. 
Human in the Loop (HITL)
What is Human in the Loop (HITL)?
Human in the Loop (HITL) is a process that involves human intervention in the model's predictions to validate and correct the results. HITL helps improve the accuracy and reliability of the predictions by incorporating human expertise and judgment. HITL helps identify and correct errors, improve the model's performance, and enhance the overall quality of the predictions by human experts intervening only when the confidence scores are below a certain threshold.
It can improved accuracy and reliability of the predictions, reduced errors, and enhanced overall quality of the results. 

How can customers access confidence score in CU?
For every field extraction, confidence score is listed as part of the field extraction output. You can also check confidence score as part of your JSON output under "confidence"
 
 Tips to improve confidence score
1.    Correcting an expected output so that the model can understand the definition better.  Example: Here we can see the confidence score is 12%, to improve confidence score, we can go to label data, select auto label which will give us predicted field labels. Now we can correct our definition and it will show corrected field label. Test the analyzer again for better confidence score. Here it jumped to 98%. Confidence improvement will vary as per the complexity and nature of document. 

2.    Adding more samples and label them for different variation and templates the model may expect. 
3.    Add documents that contains various input values for the schema you want to extract. 
4.    Improve the quality of your input documents. 
5.    Incorporate human in the loop for lower confidence results. 
Note: Confidence score is only available for document modality in the preview. For other modalities it will be added soon. 
