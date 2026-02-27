---
title: Characteristics and limitations for using custom text classification
titleSuffix: Foundry Tools
description: Learn about characteristics and limitations for using custom text classification.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 04/26/2023
---

# Characteristics and limitations for using custom text classification

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Performance of custom text classification models will vary based on the scenario and input data. The following sections are designed to help you understand key concepts about performance and evaluation of custom text classification models.

## Performance evaluation metrics

Reviewing model evaluation is an important step in the custom text classification model's development life cycle. It helps you determine how well your model is performing and to gauge the expected performance when the model is used in production.

In the process of building a model, training and testing sets are either defined during tagging or chosen at random during training. Either way, the training and testing sets are essential for training and evaluating custom text classification models. The training set is used to train the custom machine learning model. The test set is used as a blind set to evaluate model performance.

The model evaluation process is triggered after training is completed successfully. The evaluation process takes place by using the trained model to predict user-defined classes for files in the test set and compare the predictions with the provided data tags (ground truth). The results are returned to you to review the model's performance.

The first step in calculating the model's evaluation is categorizing the predicted labels in one of the following categories: true positives, false positives, or false negatives. The following table further explains these terms.

| Term | Correct/Incorrect | Definition | Example |
|----|----|----|----|
| True positive | Correct | The model predicts a class, and it's the same as the text has been tagged. | For a `comedy` movie script, the class `comedy` is predicted. |
| False positive | Incorrect | The model predicts the wrong class for a specific text. | For a `comedy` movie script, the class `drama` is predicted.  |
| False negative | Incorrect | The system doesn't return a result when a human judge would return a correct result. | For a `drama` movie script, the class `comedy` is predicted. In multiclassification only, for a `romance` and `comedy` movie script, the class `comedy` is predicted, but the class `romance` is not predicted. |

For single-label classification, it is not possible to have a false negative, because single-label classification models will always predict one class for each file. For a multi-label classification it is counted as both a false negative and false positive, false negative for the tagged class and false positive for the predicted class.

The preceding categories are then used to calculate *precision*, *recall* and an *F1 score*. These metrics are provided as part of the service's model evaluation. Here are the metric definitions and how they're calculated:<br>

**Precision**: The measure of the model's ability to predict actual positive classes. It's the ratio between the predicted true positives and the actually tagged positives. Recall returns how many predicted classes are correct.

**Recall**: The measure of the model's ability to predict actual positive classes. It's the ratio between the predicted true positives and the actually tagged positives. Recall returns how many predicted classes are correct.

**F1 score**: A function of precision and recall. An F1 score is needed when you are seeking a balance between precision and recall.

> [!NOTE] 
> For single classification, because the count of false positives and false negatives is always equal, it follows that precision, recall, and the F1 score are always equal to each other.

Model evaluation scores might not always be comprehensive, especially if a specific class is missing or underrepresented in the training data. This can occur if an insufficient number of tagged files were provided in the training phase. This situation would affect the quantity and quality of the testing split, which may affect the quality of the evaluation.

Any custom text classification model is expected to experience both false negative and false positive errors. You need to consider how each type of error affects the overall system and carefully think through scenarios where true events won't be recognized and incorrect events will be recognized. Depending on your scenario, precision or recall could be a more suitable metric for evaluating your model's performance.
For example, if your scenario is about ticket triaging, predicting the wrong class would cause it to be forwarded to the wrong team, which costs time and effort. In this case, your system should be more sensitive to false positives and precision would then be a more relevant metric for evaluation.

If your scenario is about categorizing email as important or spam, failing to predict that a certain email is important would cause you to miss it. But if spam email was mistakenly marked important, you would simply disregard it. In this case, the system should be more sensitive to false negatives and recall would then be a more relevant evaluation metric.

If you want to optimize for general purpose scenarios or when precision and recall are equally important, the F1 score would be the most relevant metric. Evaluation scores are dependent on your scenario and acceptance criteria. There's no absolute metric that will work for all scenarios.

## System limitations and best practices for enhancing system performance

* **Understand service limitations:** There are some limits enforced on the user, such as the number of files and classes contained in your data or entity length. Learn more about [system limitations](/azure/ai-services/language-service/custom-text-classification/service-limits).

* **Plan your schema:** Identify the categories that you want to classify your data into. You need to plan your schema to avoid ambiguity and to take the complexity of classes into consideration. Learn more about [recommended practices](/azure/ai-services/language-service/custom-text-classification/how-to/design-schema).

* **Select training data:** The quality of training data is an important factor in model quality. Using diverse and real-life data similar to the data you expect during production will make the model more robust and better able to handle real-life scenarios. Make sure to include all layouts and formats of text that will be used in production. If the model isn't exposed to a certain scenario or class during training, it won't be able to recognize it in production. Learn more about [recommended practices](/azure/ai-services/language-service/custom-text-classification/how-to/design-schema#data-selection).

* **Tag data accurately:** The quality of your tagged data is a key factor in model performance, and it's considered the ground truth from which the model learns. Tag precisely and consistently. When you tag a specific file, make sure you assign it to the most relevant class. Make sure similar files in your data are always tagged with the same class. Make sure all classes are well represented and that you have a balanced data distribution across all entities. [Examine data distribution](/azure/ai-services/language-service/custom-text-classification/how-to/view-model-evaluation) to make sure all your classes are adequately represented. If a certain class is tagged less frequently than the others, this class may be underrepresented and may not be recognized properly by the model during production. In this case, consider adding more files from the underrepresented class to your training data and then train a new model.

* **Review evaluation and improve model:** After the model is successfully trained, check the model evaluation and confusion matrix. This review helps you understand where your model went wrong and learn about classes that aren't performing well. It's also considered a best practice to [review the test set](/azure/ai-services/language-service/custom-text-classification/how-to/view-model-evaluation?tabs=language-studio%2Ctest-set%2CLanguage-studio#model-details) and view the predicted and tagged classes side by side. It gives you a better idea of the model's performance and helps you decide if any changes in the schema or the tags are necessary. You can also review the [confusion matrix](/azure/ai-services/language-service/custom-text-classification/concepts/evaluation-metrics#confusion-matrix) to identify classes that are often mistakenly predicted to see if anything can be done to improve model performance.

## General guidelines to understand and improve performance

The following guidelines will help you to understand and improve performance in custom text classification.

### Understand confidence scores

After you've tagged data and trained your model, you'll need to deploy it to be consumed in a production environment. Deploying a model means making it available for use via the [runtime API](https://aka.ms/ct-runtime-swagger) to predict classes for a submitted text. The API returns a JSON object that contains the predicted class or classes and the confidence score. 
The confidence score is a decimal number between zero (0) and one (1). It serves as an indicator of how confident the system is with its prediction. A higher value indicates higher confidence in the accuracy of that result. The returned score is directly affected by the data you tagged when you built the custom model. If the user's input is similar to the data used in training, higher scores and more accurate predictions can be expected.
If a certain class is consistently predicted with a low confidence score, you might want to examine the tagged data and add more instances for this class, and then retrain the model.

### Set confidence score thresholds

The confidence score threshold can be adjusted based on your scenario. You can automate decisions in your scenario based on the confidence score the system returns. You can also set a certain threshold so that predicted classes with confidence scores higher or lower than this threshold are treated differently. For example, if a prediction is returned with a confidence score below the threshold, the file can be flagged for additional review.

Different scenarios call for different approaches. If the actions based on the predicted class will have high-impacts, you might decide to set a higher threshold to ensure accuracy of classification. In this case, you would expect fewer false positives but more false negatives resulting in higher precision. If no high-impact decision based on the predicted class will be made in your scenario, you might accept a lower threshold because you would want to predict all possible classes that might apply to the submitted text (in multi-label classification cases). In this case, you would expect more false positives but fewer false negatives. The result is a higher recall.

It's very important to evaluate your system with the set thresholds by using real data that the system will process in production to determine the effects on precision and recall.

### Different training sessions and changes in evaluation

Retraining the same model without any changes in tagged data will result in the same model output, and as a result, the same evaluation scores. If you add or remove tags, the model performance changes accordingly. Provided that no new files were added during tagging, the evaluation scores can be compared with the previous version of the model because both have the same files in the training and testing sets.

Adding new files or training a different model with random set splits leads to different files in training and testing sets. Although changes in evaluation scores might occur, they can't be directly compared to other models because performance is calculated on different splits for test sets.

### Review incorrect predictions to improve performance

After you've trained your model, you can [review model evaluation details](/azure/ai-services/language-service/custom-text-classification/how-to/view-model-evaluation) to identify areas for improvement. The model-level metrics provide information on the overall model performance. By observing the class-level performance metrics, you can identify if there are any issues within a specific class.

If you notice that a specific class has low performance, it means the model is having trouble predicting it. This issue could be due to an ambiguous schema, which means the class can't be differentiated from other classes. It could also be caused by a data imbalance, which means this class is underrepresented. In this instance you will need to add more tagged examples for the model to better predict this class.

You can also review the [confusion matrix](/azure/ai-services/language-service/custom-text-classification/concepts/evaluation-metrics#confusion-matrix) to identify classes that are often mistakenly predicted to see if anything can be done to improve model performance. If you notice that a specific class is often predicted as another class, it's a strong indicator that these two classes are similar to each other. You might need to rethink your schema. Or you can add more tagged examples to your dataset to help the model differentiate these classes.

After you've viewed evaluation details for your model, you can [improve your model](/azure/ai-services/language-service/custom-text-classification/how-to/view-model-evaluation). This process enables you to view the predicted and tagged classes side by side to determine what went wrong during model evaluation. If you find that some classes are interchangeably repeated, consider adding them all to a higher order which represents multiple classes for better prediction.

### Performance varies across features and languages

Custom text classification gives you the option to use data in multiple languages. You can have multiple files in your dataset of different languages. Also, you can train your model in one language and use it to query text in other languages. If you want to use the multilingual option, you have to enable this option during [project creation](/azure/ai-services/language-service/custom-text-classification/quickstart?#create-a-custom-classification-project).

If you notice low scores in a certain language, consider adding more data in this language to your dataset. To learn more about supported languages, see [this website/azure/ai-services/language-service/custom-text-classification/language-support).

## Next steps

* [Introduction to custom text classification](/azure/ai-services/language-service/custom-text-classification/overview)

* [Custom text classification Transparency Note](custom-text-classification-transparency-note.md)
* [Data privacy and security](custom-text-classification-data-privacy-security.md)
* [Guidance for integration and responsible use](custom-text-classification-guidance-integration-responsible-use.md)
* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
