---
title: Characteristics and limitations for using Anomaly Detector and Metrics Advisor
titleSuffix: Foundry Tools
description: Characteristics and limitations of using Anomaly Detector and Metrics Advisor
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.service: azure-ai-anomaly-detector
ms.topic: concept-article
ms.date: 02/21/2024
---

# Characteristics and limitations of Anomaly Detector

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

In this section, we'll review what accuracy means for Anomaly Detector and how to assess it for your context.

> [!NOTE]
> While the information in this article only refers to Anomaly Detector, most of the concepts described apply to both Anomaly Detector and Azure AI Metrics Advisor. Metrics Advisor is built on top of the core technology from Anomaly Detector.

## Language of accuracy

The accuracy of anomaly detection can be measured by evaluating how well the system-detected anomalies correspond to actual anomalous events. An example is when an anomaly is captured by Anomaly Detector and at the same time an actual service outage is reported by a customer. To measure accuracy, the customer might pass in a set of historical data and let Anomaly Detector perform detection results. The customer could then compare that information with the record of real events and classify the detection results into two kinds of correct (or "true") anomalies and two kinds of incorrect (or "false") anomalies.

| Term | Definition | Example |
|----|----|----|
| True positive (TP)| The system-detected anomaly correctly corresponds to an actual anomalous event. | The system identifies an anomaly that corresponds to a real service outage. |
| True negative (TN)| The system correctly doesn't detect any anomaly when metrics data follows a historical pattern that is within the range of normal operations. | The system doesn't find any anomaly at a time when there was no service outage.|
| False positive (FP)| The system incorrectly detects an anomaly when there's no anomalous event. | The system detects an anomaly when there was no service outage. |
| False negative (FN)| The system fails to detect an anomaly when an anomalous event has occurred. | The system fails to capture an anomaly when a service outage occurred. |

### Precision and recall

**Precision** is the proportion of true positives among all the positive results returned, regardless of their correctness (true positives and false positives). It indicates how many detected anomalies correspond to actual abnormal events. It can be calculated as follows:

`Precision = TP / (TP + FP)`

A precision score of 1.0 means that every anomaly detected corresponds to an actual abnormal event.

**Recall** is the proportion of true positives among all actual positives (both true positives and false negatives). It indicates how many of the actual abnormal events were detected. It can be calculated as follows:

`Recall = TP / (TP + FN)`

A recall score of 1.0 means that every actual abnormal event is detected.

## Best practices for improving accuracy

It can sometimes be hard to optimize for both precision and recall at the same time. Depending on the specific scenario, customers might want to prioritize one over the other. Stakeholders who monitor specific KPIs might need a high recall rate so that no issues are missed. In contrast, stakeholders at the executive level might want to be notified only when something serious happens, then they prefer a high precision rate.

Several factors need to be balanced to get the best accuracy to meet business requirements.

### Sensitivity

The **sensitivity** parameter (check [API reference](https://aka.ms/anomaly-detector-rest-api-ref) for more parameter descriptions) is the key to tuning the detection results. In general, a high sensitivity value means the model is more sensitive to outliers and is likely to identify more anomalies. A low sensitivity value usually means the model will tolerate minor outliers.

### Choose the right mode

There are two different detection modes offered by Anomaly Detector: /last mode and /entire mode. These two API operations look similar in terms of input parameters and output format. But there's one key difference regarding the detection behavior which should be considered when choosing the mode to be used. The /entire operation uses all the data points from the request to create a single statistical model. The /last operation only looks at the window of data points that you've passed to the API, which is usually a subset of the entire dataset. In practice, the /entire operation is more likely to ignore random and small noise as it looks at the global statistical pattern. The /last operation only looks at the local window you indicated and is more likely to call out those noise points as anomalies.

Please refer to [this example](/azure/ai-services/anomaly-detector/concepts/anomaly-detection-best-practices#when-to-use-batch-entire-or-latest-last-point-anomaly-detection) for more information.

### Data granularity

When the raw data is at low granularity – like one data point per second or even sub-second – a common practice is to aggregate (sum/average/sample) it to a higher granularity. The benefits of aggregation include:

1. Easier alignment to even distribution on time, which is a protocol of the API input.
1. Increased tolerance of random noise.
1. Fewer data points and fewer API transactions.

The downside of aggregation is that subtle changes within lower granularity are not considered, which might lead to missing important anomalies.

Other factors can also be used to improve the accuracy of the model, such as specifying a known seasonal pattern. For more information on improving accuracy for Anomaly Detector, see [Best practices for using the Anomaly Detector API](/azure/ai-services/anomaly-detector/concepts/anomaly-detection-best-practices).

## Limitations

There are several limitations of Anomaly Detector to be aware of:

- Anomaly Detector v1.0 is stateless and doesn't store any customer data or model updates. That means every API call is completely independent. Multiple API calls with a lot of data won't change the accuracy of the service. To achieve better accuracy, tune within single API calls.
- The minimum number of data points to trigger anomaly detection is 12, and the maximum is 8640 points. If there's a seasonal pattern in your metrics data, send at least 4 cycles of the pattern. 
- Anomaly Detector doesn't automatically tune the parameters for customers. When customers want to rely on the anomaly detection results from the service to trigger automated actions, we highly recommend that you perform an evaluation with real world data before you apply the settings to your scenario.
- Anomaly Detector only takes in time series data by using timestamps and numbers. The service has no knowledge of the context and surroundings where the data is collected. In production use, decision makers might need to consider knowledge beyond those measures.

## Evaluating Anomaly Detector in your applications

Anomaly Detector's performance will vary depending on the real-world uses that customers implement. In order to ensure optimal performance in their scenarios, customers should conduct their own evaluations of the solutions they implement using Anomaly Detector. As you do so, consider the following:

- Will this product or feature benefit my scenario? Before deploying AI into your scenario, test how it performs using real-life data and make sure it can serve the goal you are trying to achieve.
- Will this product or feature generate accurate results as expected? Validate accuracy of the results generated by the service, do some fine-tune according to [Best practices for improving accuracy](#best-practices-for-improving-accuracy) and make sure it delivers the accuracy you need.
- Are we equipped to identify and respond to errors? AI-powered products and features will not be 100% accurate, so consider how you will identify and respond to any errors that may occur.

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)
