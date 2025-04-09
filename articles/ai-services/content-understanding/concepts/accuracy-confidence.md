---
title: Understand and improve confidence scores in Azure AI Content Understanding.
titleSuffix: Azure AI services
description: Tips for interpreting and improving Azure AI Content Understanding accuracy and confidence scores.
author: laujan
ms.author: admaheshwari
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: reference
ms.date: 04/09/2025
---

# Interpret and improve confidence and accuracy scores

> [!NOTE]
>
> * Azure AI Content Understanding is currently available in preview.
>
> * While the service is in active development, confidence scores are only available for the document modality.

Confidence scores quantify the probability that a result is accurately detected, by gauging the degree of statistical certainty. The estimated accuracy is derived from evaluating various combinations of the training data to forecast the labeled values. In this article, we share how to interpret accuracy and confidence scores and best practices for using those scores to improve both accuracy and confidence results.

Confidence scores are essential as they indicate the model's level of certainty in its predictions. These scores enable users to assess the reliability of extracted data, guiding whether a human review is necessary. Additionally, confidence scores are instrumental in streamlining workflows and enhancing efficiency by minimizing the need for manual validation.

## Supported fields 

Confidence scores are supported for extractive various fields, including text, tables, and images. The specific fields supported may vary depending on the model and the use case. 

## Confidence scores

Confidence scores are listed for every field as part of the field extraction output:

  :::image type="content" source="../media/confidence-accuracy/field-extraction-score.png" alt-text="Screenshot of field extraction scores from Azure AI Foundry.":::

Confidence scores are also part of extraction output JSON file:

  :::image type="content" source="../media/confidence-accuracy/json-output.png" alt-text="Screenshot of field extraction JSON output.":::
 
## Improving accuracy results

Common challenges with confidence scores include the quality of input documents, diversity in document types, complexity of the documents, and limitations of the model to recognize certain types of content or features. These limitations underscore the need for continuous improvements and adaptations in the modeling process to enhance reliability and accuracy. Here are some tips:

* **Establish appropriate thresholds**. Setting thresholds can enhance the accuracy and reliability of predictions. These thresholds are predefined values that determine whether a prediction is considered reliable or requires further review. Establishing the right thresholds ensures that only high-confidence predictions are automated, while low-confidence predictions are flagged for human review. This approach helps increases the overall accuracy and reliability of predictions.

* **Incorporate human review into workflows**. Human in the Loop (`HITL`) is a process where human intervention is introduced to validate and correct the  model's predictions. Utilizing human expertise and judgment enhances the accuracy and reliability of predictions. `HITL` allows for the identification and correction of errors, improves the model's performance, and elevates the overall quality of predictions by involving human experts only when confidence scores fall below a specified threshold.

* **Include diverse input values for the schema you aim to extract**. To enrich the dataset and account for different variations and templates the model might encounter, use forms with unique values in each field and add labeled samples.

* **Improve the quality of your input documents**. Clear, well-structured forms with consistent formatting typically result in higher confidence scores.

## Related content

* [Best practices for Content Understanding](best-practices.md)

* [Document Intelligence accuracy and confidence scores](../../document-intelligence/concept/accuracy-confidence.md)


