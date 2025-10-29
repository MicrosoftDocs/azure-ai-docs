---
title: Inference data collection from models in production
titleSuffix: Azure Machine Learning
description: Collect inference data from models deployed on Azure Machine Learning to monitor their performance in production.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: mlops
ms.reviewer: alehughes
ms.topic: concept-article 
ms.date: 04/15/2024
ms.custom: devplatv2, event-tier1-build-2023, build-2023
---

# Data collection from models in production

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn about data collection from models that are deployed to Azure Machine Learning online endpoints.

Azure Machine Learning **Data collector** provides real-time logging of input and output data from models that are deployed to managed online endpoints or Kubernetes online endpoints. Azure Machine Learning stores the logged inference data in Azure blob storage. This data can then be seamlessly used for model monitoring, debugging, or auditing, thereby, providing observability into the performance of your deployed models.

Data collector provides:
- Logging of inference data to a central location (Azure Blob Storage)
- Support for managed online endpoints and Kubernetes online endpoints
- Definition at the deployment level, allowing maximum changes to its configuration
- Support for both payload and custom logging


## Logging modes

Data collector provides two logging modes: _payload logging_ and _custom logging_. Payload logging allows you to collect the HTTP request and response payload data from your deployed models. With custom logging, Azure Machine Learning provides you with a Python SDK for logging pandas DataFrames directly from your scoring script. Using the custom logging Python SDK, you can log model input and output data, in addition to data before, during, and after any data transformations (or preprocessing).

## Data collector configuration

Data collector can be configured at the deployment level, and the configuration is specified at deployment time. You can configure the Azure Blob storage destination that will receive the collected data. You can also configure the sampling rate (ranging from 0 – 100%) of the data to collect.

## Limitations

Data collector has the following limitations:
- Data collector only supports logging for online (or real-time) Azure Machine Learning endpoints (Managed or Kubernetes).
- The Data collector Python SDK only supports logging tabular data via pandas DataFrames.

## Related content

- [How to collect data from models in production](how-to-collect-production-data.md)
- [What are Azure Machine Learning endpoints?](concept-endpoints.md)
