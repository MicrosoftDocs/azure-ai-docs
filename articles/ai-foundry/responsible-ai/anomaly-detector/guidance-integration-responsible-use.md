---
title: Guidance for integration and responsible use with Anomaly Detector and Metrics Advisor
titleSuffix: Foundry Tools
description: Guidance for how to deploy the Anomaly Detector and Metrics Advisor responsibly, based on the knowledge and understanding from the team that created this product.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.service: azure-ai-anomaly-detector
ms.topic: best-practice
ms.date: 02/21/2024
---

# Guidance for integration and responsible use with Anomaly Detector

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft works to help customers responsibly develop and deploy solutions that use Anomaly Detector. Our principled approach upholds personal agency and dignity by considering the AI system's fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations reflect our commitment to developing responsible AI.

> [!NOTE]
> While the information in this article only refers to Anomaly Detector, most of the concepts described apply to both Anomaly Detector and Azure AI Metrics Advisor. Metrics Advisor is built on top of the core technology from Anomaly Detector.

## Recommendations for customers and deployers at the pre-development phase

These recommendations are intended for customers when they've started piloting or are planning to integrate the service into their solutions.

### Understand the service capability

Anomaly Detector is a service that provides time series anomaly detection. It doesn't process data that hasn't been formatted in time series.

### Human review

Anomaly Detector doesn't accept labeled data from customers, but you can use two parameters – sensitivity and [maxAnomalyRatio](/azure/ai-foundry/responsible-ai/anomaly-detector/transparency-note#introduction-to-anomaly-detector) – to fine-tune detection results according to your specific needs.
Humans can check the detection results and ensure the service is generating expected results. This human review would be important in some critical cases to ensure valid decisions are made.

## Recommendations for integration

Anomaly Detector is a core API service. We recommend it for integration with data processing or analysis solutions within a company. We expect customers to have a basic sense of what metrics are and be able to prepare the metrics data for the format that's expected by Anomaly Detector.

Customers might have their own preferences for viewing the anomaly results. If so, they would need to develop additional interface elements to display the results according to their preference.

Anomaly Detector deals with various metrics. Some of these metrics might be sensitive and shouldn't be accessed publicly. When you plan to implement a solution that uses Anomaly Detector, consider access control on different metrics data. Ensure that your solution is secure and has adequate controls to preserve the integrity of your content and prevent unauthorized access.

## Recommendations for preserving privacy

A successful privacy approach empowers individuals with information and provides controls and protection to preserve their privacy. We recommend that you:

* Include dimensions with the metrics to help monitor at a finer granularity. Limit the scope of the dimensions to only those that are necessary. Exclude user identifiers to avoid invading user privacy.
* Store data for the shortest amount of time to derive the insights necessary to satisfy monitoring requirements.
* Implement strict data retention plans per existing policies and regulation. Historical data has lower weight compared to recent data and has limited impact on recent detection results. Retention plans should be automated to follow policy requirements.
* Provide appropriate safeguards to secure the data, which includes de-identification. Data encryption should be in place to protect data from harmful exposure and hacking attempts.
* Don't share data without explicit consent from affected stakeholders or data owners, and minimize the data that is shared.

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)
