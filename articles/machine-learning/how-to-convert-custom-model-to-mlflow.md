---
title: Convert custom models to MLflow
titleSuffix: Azure Machine Learning
description: Convert custom models to MLflow model format for no code deployment with endpoints in Azure Machine Learning.
services: machine-learning
author: msakande
ms.author: mopeakande
ms.reviewer: fasantia
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 08/16/2024
ms.topic: how-to
ms.custom: devx-track-python, mlflow
#customer intent: As a data scientist, I want to convert a model to an MLflow format to use the benefits of MLflow.
---

# Convert custom ML models to MLflow formatted models

In this article, learn how to convert your custom ML model into MLflow format. [MLflow](https://www.mlflow.org) is an open-source library for managing the lifecycle of your machine learning experiments. In some cases, you might use a machine learning framework without its built-in MLflow model flavor support. Due to this lack of built-in MLflow model flavor, you can't log or register the model with MLflow model fluent APIs. To resolve this issue, you can convert your model to an MLflow format where you can apply the following benefits of Azure Machine Learning and MLflow models.

With Azure Machine Learning, MLflow models get the added benefits of:

- No code deployment
- Portability as an open source standard format
- Ability to deploy both locally and on cloud

MLflow provides support for various [machine learning frameworks](https://mlflow.org/docs/latest/models.html#built-in-model-flavors), such as scikit-learn, Keras, and PyTorch. MLflow might not cover every use case. For example, you might want to create an MLflow model with a framework that MLflow doesn't natively support. You might want to change the way your model does preprocessing or post-processing when running jobs. To learn more about MLflow models, see [From artifacts to models in MLflow](concept-mlflow-models.md).

If you didn't train your model with MLFlow and want to use Azure Machine Learning's MLflow no-code deployment offering, you need to convert your custom model to MLFLow. For more information, see [Custom Python Models](https://mlflow.org/docs/latest/models.html#custom-python-models).

## Prerequisites

- Install the `mlflow` package

## Create a Python wrapper for your model

Before you can convert your model to an MLflow supported format, you need to create a Python wrapper for your model. The following code demonstrates how to create a Python wrapper for an `sklearn` model.

```python

# Load training and test datasets
from sys import version_info
import sklearn
import mlflow.pyfunc


PYTHON_VERSION = "{major}.{minor}.{micro}".format(major=version_info.major,
                                                  minor=version_info.minor,
                                                  micro=version_info.micro)

# Train and save an SKLearn model
sklearn_model_path = "model.pkl"

artifacts = {
    "sklearn_model": sklearn_model_path
}

# create wrapper
class SKLearnWrapper(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        import pickle
        self.sklearn_model = pickle.load(open(context.artifacts["sklearn_model"], 'rb'))
    
    def predict(self, model, data):
        return self.sklearn_model.predict(data)
```

## Create a Conda environment

Next, create Conda environment for the new MLflow Model that contains all necessary dependencies. If not indicated, the environment is inferred from the current installation. If not, it can be specified.

```python

import cloudpickle
conda_env = {
    'channels': ['defaults'],
    'dependencies': [
      'python={}'.format(PYTHON_VERSION),
      'pip',
      {
        'pip': [
          'mlflow',
          'scikit-learn=={}'.format(sklearn.__version__),
          'cloudpickle=={}'.format(cloudpickle.__version__),
        ],
      },
    ],
    'name': 'sklearn_env'
}
```

## Load the MLflow formatted model and test predictions

After your environment is ready, pass the `SKlearnWrapper`, the Conda environment, and your newly created artifacts dictionary to the `mlflow.pyfunc.save_model()` method. Doing so saves the model to your disk.

```python
mlflow_pyfunc_model_path = "sklearn_mlflow_pyfunc_custom"
mlflow.pyfunc.save_model(path=mlflow_pyfunc_model_path, python_model=SKLearnWrapper(), conda_env=conda_env, artifacts=artifacts)
```

To ensure that your newly saved MLflow formatted model didn't change during the save, load your model and print a test prediction to compare your original model.

The following code prints a test prediction from the mlflow formatted model and a test prediction from the sklearn model. It saves the test predictions to your disk for comparison.

```python
loaded_model = mlflow.pyfunc.load_model(mlflow_pyfunc_model_path)

input_data = "<insert test data>"
# Evaluate the model
import pandas as pd
test_predictions = loaded_model.predict(input_data)
print(test_predictions)

# load the model from disk
import pickle
loaded_model = pickle.load(open(sklearn_model_path, 'rb'))
result = loaded_model.predict(input_data)
print(result)
```

## Register the MLflow formatted model

After you confirm that your model saved correctly, you can create a test run. Register and save your MLflow formatted model to your model registry.

```python

mlflow.start_run()

mlflow.pyfunc.log_model(artifact_path=mlflow_pyfunc_model_path, 
                        loader_module=None, 
                        data_path=None, 
                        code_path=None,
                        python_model=SKLearnWrapper(),
                        registered_model_name="Custom_mlflow_model", 
                        conda_env=conda_env,
                        artifacts=artifacts)
mlflow.end_run()
```

> [!IMPORTANT]
> In some cases, you might use a machine learning framework without its built-in MLflow model flavor support. For instance, the `vaderSentiment` library is a standard natural language processing (NLP) library used for sentiment analysis. Since it lacks a built-in MLflow model flavor, you cannot log or register the model with MLflow model fluent APIs. For an example on how to save, log and register a model that doesn't have a supported built-in MLflow model flavor, see [Registering an Unsupported Machine Learning Model](https://mlflow.org/docs/latest/model-registry.html#registering-an-unsupported-machine-learning-model).

## Related content

- [Deploy MLflow models to online endpoints](how-to-deploy-mlflow-models-online-endpoints.md)
- [MLflow and Azure Machine Learning](concept-mlflow.md)
