---
title: Data and privacy for Anomaly Detector and Metrics Advisor
titleSuffix: Foundry Tools
description: This document details issues for data, privacy, and security for Anomaly Detector and Metrics Advisor.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.service: azure-ai-anomaly-detector
ms.topic: concept-article
ms.date: 02/21/2024
---

# Data and privacy for Anomaly Detector

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

> [!NOTE]
> While the information in this article only refers to Anomaly Detector, most of the concepts described apply to both Anomaly Detector and Azure AI Metrics Advisor. Metrics Advisor is built on top of the core technology from Anomaly Detector.

## What data does Anomaly Detector process?

The Anomaly Detector API can receive input and process data based on two detection modes: univariate (containing measures of one type) and multivariate (containing measures of multiple types).

### Univariate detection mode

In univariate detection mode, Anomaly Detector processes the following types of data:

- **Single time series data**: Customers call the Anomaly Detector API to send time series data to perform anomaly detection. The time series data contains timestamps, dimensions (optional), and measures for one variable (for example, temperature).
- **Configuration data**: Together with time series data that's sent to the service, some configuration data is sent along with it, like **granularity** of the metrics, **maxAnomalyRatio**, and **sensitivity**. This data could help Anomaly Detector perform expected detection results. 

### Multivariate detection mode

In multivariate detection mode, Anomaly Detector processes the following types of data:

- **Multiple time series data**:
    - **Time series data used for training**:
    
      The request must include a source parameter to indicate an externally accessible Azure Storage URI (preferably a shared access signature URI). All time series used in generating the model must be zipped into a single file and stored to the Azure Storage URI that provided. Each time series is in a single CSV file, in which the first column is timestamp and the second column is value (Here's [one example](https://multiadsample.blob.core.windows.net/data/sample_data_5_3000.zip?sp=r&st=2021-03-05T12:02:17Z&se=2021-10-05T20:02:17Z&spr=https&sv=2020-02-10&sr=c&sig=t6xHqwRmr98li6ApWoZ04Gi%2BaZNPnVMXRp07t7r11xs%3D)). 

      To train a model according to a group of time series data, the service requires some historical data to be ingested. Anomaly Detector doesn't retain the training data. It is only used for training the model, and then the data is discarded.

    - **Time series data to perform anomaly detection**:
    
      The time series data contains timestamps, dimensions (optional), and measures for multiple variables (for example, temperature and humidity). Time series data requirements are the same as when the data is used for training. However, to perform anomaly detection based on the trained model, Anomaly Detector only requires the recent data for which the customer wants to get anomaly results.

- Metrics metadata, like **slidingWindow**, **alignPolicy**, **startTime**, and **endTime**, helps to set up the detection. 

## How does Anomaly Detector process data?
### Univariate detection mode

The univariate APIs receive time series data from the customer. Anomaly Detector then processes data in memory, performing univariate anomaly detection and returning the detection results to customers. Anomaly Detector doesn't store any customer data or any generated data.

### Multivariate detection mode
The multivariate APIs include training and detection functions. Customers prepare the training data (time series data of multiple variables) in a zip file and upload it to a [blob container](https://azure.microsoft.com/services/storage/blobs/) . Then they generate a shared access signature URI and provide it to the training API. The training data is fully owned by customers and can be updated at any time.

The training API aligns the multiple time series into a consistent time dimension with **alignPolicy** defined by the customer. Then a multivariate anomaly detection model is trained with the customer's data. The multivariate training process doesn't store any customer data. It generates metadata to represent model status. Customers can delete the model including metadata at any time. The metadata of each model includes the following items:

- **Status**：Model status can be Ready, Running, or Failed.
- **SetupInfo**：Training request for this model.
- **DiagnoseInfo**：Training latency, loss, and variable states. The variable state can be used to know the NA ratio of this variable.

The detection API accepts similar requests and performs similar data processing to the training API. Because the detection process is asynchronous, customers first get a result ID. This result ID is used to get detection results with a multivariate result API. The detection result is stored in a blob temporarily and automatically removed in **seven days**. Detection results include the following items:

- **Status**: Detection status can be Ready, Running, or Failed.
- **VariableStates**: The variable state can be used to analyze the [NA ratio](/azure/ai-services/anomaly-detector/concepts/best-practices-multivariate#fill-not-available-na) of each variable.
- **SetupInfo**: Request body of the corresponding multivariate anomaly detection task.
- **Results**: Anomaly status, score, and severity of each timestamp.

Detection results and the metadata in the blob will be stored by default with a Microsoft managed key. Customers can enable a customer-managed key with their own key vault in the Azure portal to encrypt the data.

## How is data retained and what customer controls are available?

Anomaly Detector API receives customer's input data including time series data, related metadata, and configuration data then processes it to return results. The service does not retain the input data after the processing. Similarly, any training data sent by the customer is used to train models for use only by the customer. The underlying training data is not retained after training is complete. 

Customers may delete trained models at any time by using the [Delete Multivariate Model API](https://westus2.dev.cognitive.microsoft.com/docs/services/AnomalyDetector-v1-1-preview/operations/DeleteMultivariateModel).

To learn more about Microsoft privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/trust-center).

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)
