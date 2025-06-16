---
title: Log Metrics in Designer Pipelines
titleSuffix: Azure Machine Learning
description: Monitor your Azure Machine Learning designer experiments. Enable logging using the Execute Python Script component and view the logged results in the studio.
services: machine-learning
author: lgayhardt
ms.author: lagayhar
ms.reviewer: keli19
ms.service: azure-machine-learning
ms.subservice: core
ms.date: 06/12/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, designer, sdkv1, devx-track-python
---

# Enable log metrics in Azure Machine Learning designer pipelines

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In this article, you learn how to add code to designer pipelines to enable log metrics. You also learn how to view those logs using the Azure Machine Learning studio web portal.

For more information on logging metrics using the SDK authoring experience, see [Log & view metrics and log files](../how-to-log-view-metrics.md).

## Enable logging with Execute Python Script

Use the [Execute Python Script](../algorithm-module-reference/execute-python-script.md) component to enable logging in designer pipelines. Although you can log any value with this workflow, it's especially useful to log metrics from the **Evaluate Model** component to track model performance across runs.

The following example shows how to log the mean squared error of two trained models using the **Evaluate Model** and **Execute Python Script** components.

1. Connect an **Execute Python Script** component to the output of the **Evaluate Model** component.

    :::image type="content" source="../media/how-to-log-view-metrics/designer-logging-pipeline.png" alt-text="Screenshot that shows how to connect the Execute Python Script component to the Evaluate Model component." lightbox="../media/how-to-log-view-metrics/designer-logging-pipeline.png":::

1. Paste the following code into the **Execute Python Script** code editor to log the mean absolute error for your trained model. You can use a similar pattern to log any other value in the designer:

    [!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

    ```python
    # dataframe1 contains the values from Evaluate Model
    def azureml_main(dataframe1=None, dataframe2=None):
        print(f'Input pandas.DataFrame #1: {dataframe1}')
    
        from azureml.core import Run
    
        run = Run.get_context()
    
        # Log the mean absolute error to the parent run to see the metric in the run details page.
        # Note: 'run.parent.log()' should not be called multiple times because of performance issues.
        # If repeated calls are necessary, cache 'run.parent' as a local variable and call 'log()' on that variable.
        parent_run = Run.get_context().parent
        
        # Log left output port result of Evaluate Model. This also works when evaluate only 1 model.
        parent_run.log(name='Mean_Absolute_Error (left port)', value=dataframe1['Mean_Absolute_Error'][0])
        # Log right output port result of Evaluate Model. The following line should be deleted if you only connect one Score component to the` left port of Evaluate Model component.
        parent_run.log(name='Mean_Absolute_Error (right port)', value=dataframe1['Mean_Absolute_Error'][1])

        return dataframe1,
    ```

This code uses the Azure Machine Learning Python SDK to log values. It uses `Run.get_context()` to get the context of the current run. It then logs values to that context with the `run.parent.log()` method. It uses `parent` to log values to the parent pipeline run rather than the component run.

For more information on how to use the Python SDK to log values, see [Log & view metrics and log files](../how-to-log-view-metrics.md).

## View logs

After the pipeline run completes, you can see the *Mean_Absolute_Error* in the Experiments page.

1. Navigate to the **Jobs** section.

1. Select your experiment.

1. Select the job in your experiment that you want to view.

1. Select **Metrics**.

    :::image type="content" source="../media/how-to-log-view-metrics/experiment-page-metrics-across-runs.png" alt-text="Screenshot that shows job metrics in the studio." lightbox="../media/how-to-log-view-metrics/experiment-page-metrics-across-runs.png":::

## Related content

* [Troubleshooting machine learning pipelines](how-to-debug-pipelines.md#azure-machine-learning-designer)
* [Log & view metrics and log files v1](how-to-log-view-metrics.md)
* [Execute Python Script component](../algorithm-module-reference/execute-python-script.md)
