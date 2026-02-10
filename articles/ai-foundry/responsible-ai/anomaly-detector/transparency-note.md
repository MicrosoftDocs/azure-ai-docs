---
title: Use cases for Anomaly Detector and Metrics Advisor
titleSuffix: Foundry Tools
description: Understanding the use cases of Anomaly Detector and Metrics Advisor
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.service: azure-ai-anomaly-detector
ms.topic: concept-article
ms.date: 02/21/2024
---

# Transparency Note for Anomaly Detector

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *Transparency Notes* to help you understand how our AI technology works. This includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft's AI Principles](https://www.microsoft.com/ai/responsible-ai).

> [!NOTE]
> While the information in this article only refers to Anomaly Detector, most of the concepts described apply to both Anomaly Detector and Azure AI Metrics Advisor. Metrics Advisor is built on top of the core technology from Anomaly Detector.

## Introduction to Anomaly Detector

Here are some key terms to help you get started with Anomaly Detector.

| Term | Definition |
|----|----|
| Time series | A time series is a series of data points indexed (or listed or graphed) in chronological order. Most commonly, a time series is a sequence taken at successive, equally spaced points in time. It is a sequence of discrete-time data and usually contains timestamps, dimensions (optional), and measures. |
| Dimension | A dimension is one or more categorical values. The combination of those values identifies a particular univariate time series, for example: country, language, tenant, and so on. |
| Measure | A measure is a fundamental or unit-specific term and a quantifiable value of the metric.|
| Granularity | Time series input data needs to be at equally spaced points in time. This means the data needs to be pre-aggregated to a specific granularity, like by year, month, week, day, hour, minute or second. |
| Sensitivity | A system parameter indicated by a numerical value that adjusts the tolerance of the anomaly detection. Lowering the sensitivity increases the range identified as normal which leads to fewer anomalies detected.  |
| MaxAnomalyRatio | The max ratio of anomalies to be detected from a time series. For example, if it's set to 0.25, for a time series with 100 points, the max anomaly points would be 25. |

Anomaly Detector is an AI service that enables you to monitor and detect abnormalities in your time series data with machine learning. The Anomaly Detector API adapts by automatically identifying and applying the best-fitting models to your data, regardless of industry, scenario, or data volume. Using your time series data, the API determines boundaries for anomaly detection, expected values, and abnormalities in time series data using machine learning.

### The basics of Anomaly Detector

Using Anomaly Detector doesn't require any prior experience in machine learning. The [RESTful API](https://westus2.dev.cognitive.microsoft.com/docs/services/AnomalyDetector/operations/post-timeseries-last-detect) enables you to easily integrate the service into your applications and processes. Anomaly Detector API can be deployed using the cloud or the intelligent edge with containers.

The Anomaly Detector RESTful API takes time series data as its input, the key parts of which are timestamps and the numerical values of metrics to be analyzed. The output of the API contains the anomalous status of each data point.

Anomaly Detector v1.0 supports three different operations:

- The /last operation detects anomalies for the latest data points in streaming data monitoring scenarios. 
- The /entire operation detects anomalies through your entire times series data. One single statistical model is created and applied to each point in the time series.
- The /changepoint operation finds trend change points from the entire time series data in a batch.

In addition to the observed anomalies, these calls also return other information about the data, including expected values, anomaly boundaries, and positions. [Read more](/azure/ai-services/anomaly-detector/concepts/anomaly-detection-best-practices#when-to-use-batch-entire-or-latest-last-point-anomaly-detection) to get the best practice on which operation to choose.

## Example use cases

Anomaly Detector can be used in multiple scenarios across a variety of industries. Some examples include:

* **Monitoring business metrics**: Track the performance of business metrics in real time to identify substantive or sudden changes. An example is an unexpected numerical pattern with daily active users of a website, stock inventory, or revenue. 
* **Monitoring IT operations metrics**: Analyze and monitor telemetry data like performance counters from IT operations to detect anomalies that could impact the health and performance of an IT system. Examples include the CPU usage of VMs, the throughput of databases, or even the number of sign-ins and signups of a website. 
* **Monitoring IoT data from sensors and predictive maintenance**: Sensor data read from IoT sensors that are deployed on factory floors, production lines, oil rigs, and pipelines, or even cars and drones could be analyzed and monitored with Anomaly Detector. Anomalies detected from the data might indicate an anomalous state of the machinery. The application you build can inform human reviewers, allowing them to take potential maintenance actions before a bigger problem arises.

## Considerations when choosing a use case

- In use cases with potential to impact the physical safety of human beings, include human review of outputs prior to any decision regarding operations. Examples of such use cases include monitoring and detecting an anomalous state in the performance of machinery on factory floors or in production lines.
- Don’t use Anomaly Detector for decisions that may have serious adverse impacts: Examples of such use cases include health care scenarios like monitoring heartbeat or blood glucose levels. Decisions based on incorrect output could have serious adverse impacts. Additionally, it is advisable to include human review of decisions that have the potential for serious impacts on individuals.
- Don't use Anomaly Detector in workspace monitoring on individuals. Because Anomaly Detector has no qualitative assessment capabilities, it is not suitable for monitoring or evaluating human activity, such as in the workplace. We do not recommend that it be used in such a way. In addition, workplace monitoring may not be legal within your jurisdiction.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)
