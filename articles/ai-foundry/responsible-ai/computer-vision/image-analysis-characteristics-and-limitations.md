---
title: Characteristics and limitations for Image Analysis
titleSuffix: Foundry Tools
description: Characteristics, accuracy, and limitations when using Image Analysis service.

author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 10/15/2025
---

# Characteristics and limitations for using Image Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Image Analysis service is part of Foundry Tools and provides pre-built AI features that are fundamental building blocks of image processing applications. In this section, you will learn about what accuracy means for Image Analysis, and how to assess accuracy for your specific use case and application.

## Accuracy for Image Analysis

The accuracy of Image Analysis feature is a measure of how well the AI generated outputs correspond to actual visual content present in the images. For example, the Image Tag feature should generate tags of the visual content present in the images. To measure accuracy, you might evaluate the image with your ground truth data and compare the output of the AI model. Comparing the ground truth with the AI generated results allows you to classify the events into two kinds of correct (or "true") results and two kinds of incorrect (or "false") results.

| **Term** | **Definition** |
|----------|----------------|
| True Positive | The system-generated output correctly corresponds to ground truth data. For example, the system correctly tags an image of a dog as a dog. |
| True Negative | The system correctly does not generate results that are not present in the ground truth data. For example, the system correctly does not tag an image as a dog when no dog is present in the image. | 
| False Positive | The system incorrectly generates an output not present in the ground truth data. For example, the system tags an image of a cat as a dog. | 
| False Negative | The system fails to generate results that are present in the ground truth data. For example, the system fails to tag an image of a dog that was present in the image.|

The above categories are then used to calculate precision and recall.

| **Term** | **Definition** |
|----------|----------------|
| Precision | Measure of the correctness of the extracted content. From an image containing multiple objects, you find out how many of those objects were correctly extracted. |
| Recall | Measure of the overall content extracted. From an image containing multiple objects, you find out how many objects were detected overall, without regard to their correctness. |

The precision and recall definitions imply that in certain cases, it can be hard to optimize for both at the same time. Depending on your specific scenario, you might need to prioritize one over the other. For example, if you're developing a solution to detect only the most accurate tags/labels in the content such as for displaying image search results, you'd need to optimize for higher precision. But if you're trying tag all possible visual content from the images for indexing or internal cataloging, you'd need to optimize for higher recall.

As an image processing system owner, it is recommended that you collect ground-truth evaluation data, which is data collected and tagged by human judges to evaluate a system. The pre-built AI models provided in Azure Vision in Foundry Tools might not satisfy the requirements of your use-case. With the use-case specific evaluation dataset, you can make an informed decision on whether the pre-built Image Analysis models are right for your use-case. You can also use the data to determine how the confidence threshold affects the achievement of your goals.

You can compare ground-truth labels to the output of the system to establish the overall accuracy and error rates, and the distribution of errors helps you set the right threshold for your scenario. Ground-truth evaluation data should include adequate sampling of representative images, so that you can understand performance differences and take corrective action. Based on the results of this evaluation, you can iteratively adjust the threshold until the trade-off between precision and recall meets your objectives.

## System performance implications based on scenarios

System performance implications can vary according to how you use it. For example, you can use the confidence value to calibrate custom thresholds for your content and scenarios to route the content for straight-through processing, or forwarding to a human-in-the-loop process. The resulting measurements determine the scenario-specific accuracy in terms of the precision and recall metrics, as illustrated in the following examples.

- **Photo-sharing app:** You can use Image Analysis to automatically generate tags for images shared and stored by application users. App users make use of this to search for specific photos shared by other users. In this use case the developer might prefer high-precision results, because the cost of incorrectly extracting tags would result in incorrect query results for app users.

- **Image processing:** For insurance and claim processing applications, as you do not want to miss any potential information you might prefer a high recall to maximize extractions. In this situation a human reviewer could flag incorrect or inappropriate tags.

## General guidelines

The following guidelines can help you understand and improve the performance of the Image Analysis APIs:


* Image Analysis supports images that meet the following requirements:
   * The image must be presented in JPEG, PNG, GIF, or BMP format
   * The file size of the image must be less than 4 megabytes (MB)
   * The dimensions of the image must be greater than 50 x 50 pixels
For information see [Image requirements](/azure/ai-services/computer-vision/overview-image-analysis#image-requirements).

* Although Image Analysis is resilient, factors such as resolution, light exposure, contrast, and image quality may affect the accuracy of your results. Refer to the product specifications and test Azure Vision on your images to validate the fit for your situation.

* Before a large-scale deployment or rollout of any Image Analysis system, system owners should conduct an evaluation phase in the context where the system will be used, and with the people who will interact with the system. This will ensure system accuracy and will help you to take actions to improve system accuracy if applicable.

* Build a feedback channel for people making decisions based on the system output, including satisfaction data from the people who will be relying on your Image Analysis features, and feedback from existing customer voice channels. This will help you to fine-tune the system and improve accuracy.

* The AI provides a confidence score for each predicted output. A confidence score represents the accuracy of a prediction as a percentage. For example, you might set a minimum confidence threshold for a system to automatically caption a photo. If a generated caption's confidence score is below the threshold, it would be forwarded for further review.

## Next steps

* [Transparency Note](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-transparency-note)
* [Responsible deployment of Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-guidance-for-integration)
* [Image Analysis Overview](/azure/ai-services/computer-vision/overview-image-analysis)
* [QuickStart your Image Analysis use case development](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library)
* [Data, privacy, and security for Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security)
