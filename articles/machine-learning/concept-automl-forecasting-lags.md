---
title: Lag features for time-series forecasting in AutoML
titleSuffix: Azure Machine Learning
description: Explore how automated machine learning (AutoML) in Azure Machine Learning creates lag and rolling window aggregation to forecast time-series regression models.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: concept-article
ms.custom: automl, sdkv1
ms.date: 02/26/2025
show_latex: true

#customer intent: As a developer, I want to use AutoML methods in Azure Machine Learning for creating lag and rolling window aggregation, so I can forecast time-series regression models.
---

# Lag features for time-series forecasting in AutoML

This article describes how automated machine learning (AutoML) in Azure Machine Learning creates lag and rolling window aggregation features to help you forecast time-series regression models. The AutoML features use historical model data that can significantly increase model accuracy by helping the model learn correlational patterns in time. 

If you're interested in learning more about the forecasting methodology in AutoML, see [Overview of forecasting methods in AutoML](concept-automl-forecasting-methods.md). To explore training examples for forecasting models in AutoML, see [Set up AutoML to train a time-series forecasting model with the SDK and CLI](how-to-auto-train-forecast.md).

## Lag featurization in AutoML

AutoML generates lag features that correspond to the forecast horizon. This section explores lag featurization in AutoML for a model with a forecast horizon of three and target lag order of one. The following tables present the model data and lag features for a monthly time series.

**Table 1**: Original time series

| Date     | $y_t$ | 
| :---     | :---  |
| 1/1/2001 | 0     |
| 2/1/2001 | 10    |
| 3/1/2001 | 20    |
| 4/1/2001 | 30    |
| 5/1/2001 | 40    | 
| 6/1/2001 | 50    |

The first step generates the lag feature for the horizon $h=1$ only. The subsequent tables demonstrate why the process uses individual horizons to complete the lag featurization.

**Table 2**: Lag featurization for horizon $h=1$

| Date       | $y_t$ | Origin    | $y_{t-1}$ | $h$  |
| :---       | :---  | :---      | :---      | :--- | 
| 1/1/2001   | 0     | 12/1/2000 | -         | 1    |
| 2/1/2001   | 10    | 1/1/2001  | 0         | 1    |
| 3/1/2001   | 20    | 2/1/2001  | 10        | 1    |
| 4/1/2001   | 30    | 3/1/2001  | 20        | 1    |
| 5/1/2001   | 40    | 4/1/2001  | 30        | 1    |
| 6/1/2001   | 50    | 5/1/2001  | 40        | 1    |

AutoML generates the data in Table 2 from the data in Table 1 by shifting the $y_t$ column down by a single observation. Tables 2 through 5 include the **Origin** column to show the dates from which the lag features originate.

The next step generates the lag feature for the forecast horizon $h=2$ only.

**Table 3**: Lag featurization for forecast horizon $h=2$

| Date       | $y_t$ | Origin    | $y_{t-2}$ | $h$  |
| :---       | :---  | :---      | :---      | :--- | 
| 1/1/2001   | 0     | 11/1/2000 | -         | 2    |
| 2/1/2001   | 10    | 12/1/2000 | -         | 2    |
| 3/1/2001   | 20    | 1/1/2001  | 0         | 2    |
| 4/1/2001   | 30    | 2/1/2001  | 10        | 2    |
| 5/1/2001   | 40    | 3/1/2001  | 20        | 2    |
| 6/1/2001   | 50    | 4/1/2001  | 30        | 2    |

AutoML generates the data in Table 3 from the data in Table 1 by shifting the $y_t$ column down by two observations.

The next step generates the lag feature for the forecast horizon $h=3$ only.

**Table 4**: Lag featurization for forecast horizon $h=3$

| Date       | $y_t$ | Origin    | $y_{t-3}$ | $h$  |
| :---       | :---  | :---      | :---      | :--- | 
| 1/1/2001   | 0     | 10/1/2000 | -         | 3    |
| 2/1/2001   | 10    | 11/1/2000 | -         | 3    |
| 3/1/2001   | 20    | 12/1/2000 | -         | 3    |
| 4/1/2001   | 30    | 1/1/2001  | 0         | 3    |
| 5/1/2001   | 40    | 2/1/2001  | 10        | 3    |
| 6/1/2001   | 50    | 3/1/2001  | 20        | 3    |

The final step concatenates the data in Tables 1, 2, and 3, and rearranges the rows.

**Table 5**: Lag featurization complete

| Date       | $y_t$ | Origin    | $y_{t-1}^{(h)}$ | $h$  |
| :---       | :---  | :---      | :---            | :--- | 
| 1/1/2001   | 0     | 12/1/2000 | -               | 1    |
| 1/1/2001   | 0     | 11/1/2000 | -               | 2    |
| 1/1/2001   | 0     | 10/1/2000 | -               | 3    |
| 2/1/2001   | 10    | 1/1/2001  | 0               | 1    |
| 2/1/2001   | 10    | 12/1/2000 | -               | 2    |
| 2/1/2001   | 10    | 11/1/2000 | -               | 3    |
| 3/1/2001   | 20    | 2/1/2001  | 10              | 1    |
| 3/1/2001   | 20    | 1/1/2001  | 0               | 2    |
| 3/1/2001   | 20    | 12/1/2000 | -               | 3    |
| 4/1/2001   | 30    | 3/1/2001  | 20              | 1    |
| 4/1/2001   | 30    | 2/1/2001  | 10              | 2    |
| 4/1/2001   | 30    | 1/1/2001  | 0               | 3    |
| 5/1/2001   | 40    | 4/1/2001  | 30              | 1    |
| 5/1/2001   | 40    | 3/1/2001  | 20              | 2    |
| 5/1/2001   | 40    | 2/1/2001  | 10              | 3    |
| 6/1/2001   | 50    | 4/1/2001  | 40              | 1    |
| 6/1/2001   | 50    | 4/1/2001  | 30              | 2    |
| 6/1/2001   | 50    | 3/1/2001  | 20              | 3    |

In Table 5, the lag column is renamed to **$y_{t-1}^{(h)}$** to reflect that the lag is generated with respect to a specific horizon. Table 5 shows how lags generated with respect to the horizon can be mapped to the conventional ways of generating lags in the previous tables.

Table 5 is an example of the data augmentation that AutoML applies to training data to enable direct forecasting from regression models. When the configuration includes lag features, AutoML creates horizon-dependent lags along with an integer-valued horizon feature. AutoML forecasting regression models can make a prediction at horizon $h$ without regard to the prediction at $h-1$, in contrast to recursively defined models like ARIMA.

## Considerations for lag featurization

There are a few considerations related to lag featurization for a model. Review the following sections to identify potential actions for your scenario.

### Dataset-size growth

When AutoML generates horizon-dependent lag features, it adds new _rows_ to the model dataset. The number of new rows is proportional to the forecast horizon.

The growth in the dataset-size can lead to out-of-memory errors on smaller compute nodes or when the dataset size is already large. You can find solutions to address this issue in the [Frequently Asked Questions (FAQ) for AutoML forecasting](how-to-automl-forecasting-faq.md#how-do-i-fix-an-out-of-memory-error).       

### Decoupling of lag order and forecast horizon

The AutoML lagging strategy decouples lag order and forecast horizon. Suppose your forecast horizon is seven, and you want AutoML to use lag features. In this scenario, you don't have to set the lag order to seven to ensure prediction over a full forecast horizon. Because AutoML generates lags with respect to horizon, you can set the lag order to one. AutoML augments the data so lags of any order are valid up to the forecast horizon.

## Related content

- [Train time-series forecasting models with AutoML](how-to-auto-train-forecast.md)
- Browse [FAQ for AutoML forecasting](how-to-automl-forecasting-faq.md)
- Explore [how AutoML uses machine learning to build forecasting models](concept-automl-forecasting-methods.md)
