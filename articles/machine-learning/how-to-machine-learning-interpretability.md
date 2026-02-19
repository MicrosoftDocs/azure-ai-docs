---
title: Model interpretability
titleSuffix: Azure Machine Learning
description: Learn how your machine learning model makes predictions during training and inferencing by using the Azure Machine Learning CLI and Python SDK.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.topic: how-to
ms.author: lagayhar
ms.reviewer: lagayhar
author: lgayhardt
ms.custom: responsible-ml, mktng-kw-nov2021, build-2023, devx-track-python, dev-focus
ms.date: 02/10/2026
ai-usage: ai-assisted
---

# Model interpretability

This article describes methods you can use for model interpretability in Azure Machine Learning.

## Why model interpretability is important to model debugging

When you use machine learning models in ways that affect people's lives, it's critically important to understand what influences the behavior of models. Interpretability helps answer questions in scenarios such as:
* Model debugging: Why did my model make this mistake? How can I improve my model?
* Human-AI collaboration: How can I understand and trust the model's decisions?
* Regulatory compliance: Does my model satisfy legal requirements?  

The interpretability component of the [Responsible AI dashboard](concept-responsible-ai-dashboard.md) contributes to the "diagnose" stage of the model lifecycle workflow by generating human-understandable descriptions of the predictions of a machine learning model. It provides multiple views into a model's behavior: 
* Global explanations: For example, what features affect the overall behavior of a loan allocation model?
* Local explanations: For example, why was a customer's loan application approved or rejected? 

You can also observe model explanations for a selected cohort as a subgroup of data points. This approach is valuable when, for example, you're assessing fairness in model predictions for individuals in a particular demographic group. The **Local explanation** tab of this component also represents a full data visualization, which is great for general eyeballing of the data and looking at differences between correct and incorrect predictions of each cohort.

The capabilities of this component are founded by the [InterpretML](https://interpret.ml/) package, which generates model explanations.

Use interpretability when you need to:

* Determine how trustworthy your AI system's predictions are by understanding what features are most important for the predictions.
* Approach the debugging of your model by understanding it first and identifying whether the model is using healthy features or merely false correlations.
* Uncover potential sources of unfairness by understanding whether the model is basing predictions on sensitive features or on features that are highly correlated with them.
* Build user trust in your model's decisions by generating local explanations to illustrate their outcomes.
* Complete a regulatory audit of an AI system to validate models and monitor the impact of model decisions on humans.

## How to interpret your model

In machine learning, *features* are the data fields you use to predict a target data point. For example, to predict credit risk, you might use data fields for age, account size, and account age. Here, age, account size, and account age are features. Feature importance tells you how each data field affects the model's predictions. For example, although you might use age heavily in the prediction, account size and account age might not affect the prediction values significantly. Through this process, data scientists can explain resulting predictions in ways that give stakeholders visibility into the model's most important features.

By using the classes and methods in the Responsible AI dashboard and by using SDK v2 and CLI v2, you can:

* Explain model prediction by generating feature-importance values for the entire model (global explanation) or individual data points (local explanation).
* Achieve model interpretability on real-world datasets at scale.
* Use an interactive visualization dashboard to discover patterns in your data and its explanations at training time.

## Supported model interpretability techniques

The Responsible AI dashboard uses the interpretability techniques that were developed in [Interpret-Community](https://github.com/interpretml/interpret-community/), an open-source Python package for training interpretable models and helping to explain opaque-box AI systems. Opaque-box models are those models for which you have no information about their internal workings. 

Interpret-Community serves as the host for the following supported explainers, and currently supports the interpretability techniques presented in the next sections.

### Supported in Responsible AI dashboard in Python SDK v2 and CLI v2

|Interpretability technique|Description|Type|
|--|--|--|
|Mimic Explainer (Global Surrogate) + SHAP tree|Mimic Explainer is based on the idea of training global surrogate models to mimic opaque-box models. A global surrogate model is an intrinsically interpretable model that's trained to approximate the predictions of any opaque-box model as accurately as possible.<br><br> Data scientists can interpret the surrogate model to draw conclusions about the opaque-box model. The Responsible AI dashboard uses LightGBM (LGBMExplainableModel), paired with the SHAP (SHapley Additive exPlanations) Tree Explainer, which is a specific explainer to trees and ensembles of trees. The combination of LightGBM and SHAP tree provides model-agnostic global and local explanations of your machine learning models.|Model-agnostic|

### Supported model interpretability techniques for text models  

| Interpretability technique | Description | Type | Text Task |
|----------------------------|-------------|------|-----------|
| SHAP text  | SHAP (SHapley Additive exPlanations) is a popular explanation method for deep neural networks that provides insights into the contribution of each input feature to a given prediction. It's based on the concept of Shapley values, which is a method for assigning credit to individual players in a cooperative game. SHAP applies this concept to the input features of a neural network by computing the average contribution of each feature to the model's output across all possible combinations of features.  For text specifically, SHAP splits on words in a hierarchical manner, treating each word or token as a feature. This process produces a set of attribution values that quantify the importance of each word or token for the given prediction. The final attribution map is generated by visualizing these values as a heatmap over the original text document. SHAP is a model-agnostic method and can be used to explain a wide range of deep learning models, including CNNs, RNNs, and transformers. Additionally, it provides several desirable properties, such as consistency, accuracy, and fairness, making it a reliable and interpretable technique for understanding the decision-making process of a model. | Model Agnostic  | Text Multi-class Classification, Text Multi-label Classification |

### Supported model interpretability techniques for image models 

| Interpretability technique | Description | Type | Vision Task |
|----------------------------|-------------|------|-------------|
|SHAP vision  | SHAP (SHapley Additive exPlanations) is a popular explanation method for deep neural networks that provides insights into the contribution of each input feature to a given prediction. It's based on the concept of Shapley values, which is a method for assigning credit to individual players in a cooperative game. SHAP applies this concept to the input features of a neural network by computing the average contribution of each feature to the model's output across all possible combinations of features.  For vision specifically, SHAP splits on the image in a hierarchical manner, treating superpixel areas of the image as each feature. This process produces a set of attribution values that quantify the importance of each superpixel or image area for the given prediction. The final attribution map is generated by visualizing these values as a heatmap. SHAP is a model-agnostic method and can be used to explain a wide range of deep learning models, including CNNs, RNNs, and transformers. Additionally, it provides several desirable properties, such as consistency, accuracy, and fairness, making it a reliable and interpretable technique for understanding the decision-making process of a model. | Model Agnostic | Image Multi-class Classification, Image Multi-label Classification |
| Guided Backprop | Guided-backprop is a popular explanation method for deep neural networks that provides insights into the learned representations of the model. It generates a visualization of the input features that activate a particular neuron in the model, by computing the gradient of the output with respect to the input image. Unlike other gradient-based methods, guided-backprop only backpropagates through positive gradients and uses a modified ReLU activation function to ensure that negative gradients don't influence the visualization. This approach results in a more interpretable and high-resolution saliency map that highlights the most important features in the input image for a given prediction. Guided-backprop can be used to explain a wide range of deep learning models, including convolutional neural networks (CNNs), recurrent neural networks (RNNs), and transformers. | AutoML | Image Multi-class Classification, Image Multi-label Classification |
| Guided gradCAM | Guided GradCAM is a popular explanation method for deep neural networks that provides insights into the learned representations of the model. It generates a visualization of the input features that contribute most to a particular output class, by combining the gradient-based approach of guided backpropagation with the localization approach of GradCAM. Specifically, it computes the gradients of the output class with respect to the feature maps of the last convolutional layer in the network, and then weights each feature map according to the importance of its activation for that class. This process produces a high-resolution heatmap that highlights the most discriminative regions of the input image for the given output class. Guided GradCAM can be used to explain a wide range of deep learning models, including CNNs, RNNs, and transformers. Additionally, by incorporating guided backpropagation, it ensures that the visualization is meaningful and interpretable, avoiding spurious activations and negative contributions. | AutoML | Image Multi-class Classification, Image Multi-label Classification |
| Integrated Gradients | Integrated Gradients is a popular explanation method for deep neural networks that provides insights into the contribution of each input feature to a given prediction. It computes the integral of the gradient of the output class with respect to the input image, along a straight path between a baseline image and the actual input image. This path is typically chosen to be a linear interpolation between the two images, with the baseline being a neutral image that has no salient features. By integrating the gradient along this path, Integrated Gradients provides a measure of how each input feature contributes to the prediction, allowing for an attribution map to be generated. This map highlights the most influential input features, and can be used to gain insights into the model's decision-making process. Integrated Gradients can be used to explain a wide range of deep learning models, including CNNs, RNNs, and transformers. Additionally, it's a theoretically grounded technique that satisfies a set of desirable properties, such as sensitivity, implementation invariance, and completeness. | AutoML | Image Multi-class Classification, Image Multi-label Classification |
| XRAI | [XRAI](https://arxiv.org/abs/1906.02825) is a novel region-based saliency method based on Integrated Gradients (IG). It over-segments the image and iteratively tests the importance of each region, coalescing smaller regions into larger segments based on attribution scores. This strategy yields high quality, tightly bounded saliency regions that outperform existing saliency techniques. XRAI can be used with any DNN-based model as long as there's a way to cluster the input features into segments through some similarity metric. | AutoML | Image Multi-class Classification, Image Multi-label Classification |
| D-RISE  | D-RISE is a model agnostic method for creating visual explanations for the predictions of object detection models. By accounting for both the localization and categorization aspects of object detection, D-RISE can produce saliency maps that highlight parts of an image that most contribute to the prediction of the detector. Unlike gradient-based methods, D-RISE is more general and doesn't need access to the inner workings of the object detector. It only requires access to the inputs and outputs of the model. The method can be applied to one-stage detectors (for example, YOLOv3), two-stage detectors (for example, Faster-RCNN), and Vision Transformers (for example, DETR, OWL-ViT). <br> D-Rise provides the saliency map by creating random masks of the input image and sends them to the object detector. By assessing the change of the object detector's score, it aggregates all the detections with each mask and produces a final saliency map. | Model Agnostic | Object Detection |

## Next steps

* Learn how to generate the Responsible AI dashboard via [CLI v2 and SDK v2](how-to-responsible-ai-insights-sdk-cli.md) or the [Azure Machine Learning studio UI](how-to-responsible-ai-insights-ui.md).
* Explore the [supported interpretability visualizations](how-to-responsible-ai-dashboard.md#feature-importances-model-explanations) of the Responsible AI dashboard.
* Learn how to generate a [Responsible AI scorecard](how-to-responsible-ai-scorecard.md) based on the insights observed in the Responsible AI dashboard.
