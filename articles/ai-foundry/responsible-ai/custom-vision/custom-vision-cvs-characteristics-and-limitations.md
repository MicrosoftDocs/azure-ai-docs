---
title: Characteristics and limitations for Custom Vision
titleSuffix: Foundry Tools
description: Learn general guidelines for using this image recognition service from Azure.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-custom-vision
ms.topic: concept-article
ms.date: 07/07/2021
---

# Characteristics and Limitations of Custom Vision

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

The quality of your classifier or object detector model built with Azure AI Custom Vision depends on the amount, quality, and variety of the labeled data you provide when training the model. The quality also depends on how balanced the overall dataset is between classes.

After you've trained your model, you can see the estimate of the project's performance [customvision.ai](http://customvision.ai). Custom Vision uses the images that you submitted for training to estimate precision, recall, and mean average precision. These three measurements of an image classifier’s effectiveness are defined as follows:

* *Precision* is the percentage of identified classifications that were correct. For example, if the model identified 100 images as dogs, and 99 of them were actually of dogs, then the precision is 99 percent.
* *Recall* is the percentage of actual classifications that were correctly identified. For example, if there were actually 100 images of apples, and the model identified 80 as apples, the recall is 80 percent.
* *Mean average precision* (mAP) is the average value of the average precision (AP). AP is the area under the precision/recall curve (precision plotted against recall for each prediction made).

*Probability threshold* is the desired level of confidence that a prediction needs to have in order to be considered correct. 
When you interpret prediction calls with a high probability threshold, they  tend to return results with high precision at the expense of recall. That is, the detected classifications are correct, but many remain undetected. A low probability threshold does the opposite: most of the actual classifications are detected, but there are more false positives within that set. With this in mind, you should set the probability threshold according to the specific needs of your project. By default, the probability threshold is 50% and can be set between 0% and 100%. To adjust the probability threshold go to [customvision.ai](http://customvision.ai) on the **Performance** tab, find the **Probability Threshold** slider, and adjust it to your needs.

## Evaluating and integrating Custom Vision for your use

### Best practices to improve model accuracy

The process of building a Custom Vision model is iterative. Each time you train your model, you create a new iteration with its own, updated performance metrics. You can view all of your iterations in the left pane of the **Performance** tab for your project at [customvision.ai](http://customvision.ai). 

A model will learn to make predictions based on arbitrary characteristics that your images have in common. To prevent overfitting, see [How to improve your Custom Vision model](/azure/ai-services/custom-vision-service/getting-started-improving-your-classifier).

We suggest that you test the model for an iteration with additional data. You can decide which iteration of the model to publish or export, and to use for inference.

Based on the model's performance, you need to decide if the model is appropriate for your use case and business needs. Here's an approach that you might take. You can deploy a Custom Vision model in an isolated environment, test the performance of the model relative to your use case, and then use the predictions to further train the model until it reaches the level of performance you want. 

For more information, see [Quickstart: Build a classifier with the Custom Vision website](/azure/ai-services/custom-vision-service/getting-started-build-a-classifier), and [Quickstart: Build an object detector with the Custom Vision website](/azure/ai-services/custom-vision-service/get-started-build-detector).

## Next steps

* [Compliance, privacy, and security for Custom Vision ](custom-vision-cvs-data-privacy-security.md)
