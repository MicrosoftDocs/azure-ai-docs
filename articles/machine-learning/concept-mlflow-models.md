---
title: Artifacts and models in MLflow
titleSuffix: Azure Machine Learning
description: Learn how MLflow uses the concept of models instead of artifacts to represent trained models and enable a streamlined path to deployment.
services: machine-learning
author: msakande
ms.author: mopeakande
ms.reviewer: fasantia
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 09/27/2024
ms.topic: conceptual
ms.custom: cliv2, sdkv2, FY25Q1-Linter
#Customer intent: As a data scientist, I want to understand artifacts and models in MLflow so that I can enable a streamlined path to deployment.
---

# From artifacts to models in MLflow

This article explains the differences between an MLflow *artifact* and an MLflow *model*, and how to transition from one to the other. The article also explains how Azure Machine Learning uses the concept of an MLflow model to enable streamlined deployment workflows.

## Artifacts and models

There are fundamental differences between logging MLflow artifacts and files vs. logging MLflow models.

### Artifact

An artifact is any file that's generated and captured from an experiment's run or job. An artifact could be a model serialized as a pickle file, the weights of a PyTorch or TensorFlow model, or a text file containing the coefficients of a linear regression. Some artifacts have nothing to do with the model itself but contain run configurations, preprocessing information, or sample data. Artifacts can have various formats.

You can log artifacts as follows:

```python
filename = 'model.pkl'
with open(filename, 'wb') as f:
  pickle.dump(model, f)

mlflow.log_artifact(filename)
```

### Model

An MLflow model is an artifact, but you make stronger assumptions about this type of artifact that provide a clear *contract* between the saved files and what they mean.

You can log MLflow models by using the MLflow SDK as follows:

```python
import mlflow
mlflow.sklearn.log_model(sklearn_estimator, "classifier")
```

Logging MLflow models in Azure Machine Learning has the following advantages:

- You can deploy MLflow models to real-time or batch endpoints without providing a scoring script or an environment.
- When you deploy MLflow models, the deployments automatically generate a swagger file, so you can use the **Test** feature in Azure Machine Learning studio.
- You can use MLflow models directly as pipeline inputs.
- You can use the [Responsible AI dashboard](how-to-responsible-ai-dashboard.md) with MLflow models.

## The MLmodel format

When you log models as simple artifact files, you need to know how the model builder intended to use each of the files to load the model for inference. For MLflow models, the *MLmodel format* specifies the contract between the artifacts and what they represent. You load MLflow models by using the contract specified in the MLflow format.

The MLmodel format stores assets in a folder that has no specific naming requirement. Among the assets is a file named *MLmodel* that's the single source of truth for how to load and use the model.

The following example shows an MLflow model folder called *credit_defaults_model* in Azure Machine Learning studio. The folder contains the *MLmodel* file among other model artifacts.

:::image type="content" source="media/concept-mlflow-models/mlflow-mlmodel.png" alt-text="A screenshot showing assets of a sample MLflow model, including the MLmodel file." lightbox="media/concept-mlflow-models/mlflow-mlmodel.png":::

The following example shows an *MLmodel* file for a computer vision model trained with `fastai`:

```yaml
artifact_path: classifier
flavors:
  fastai:
    data: model.fastai
    fastai_version: 2.4.1
  python_function:
    data: model.fastai
    env: conda.yaml
    loader_module: mlflow.fastai
    python_version: 3.8.12
model_uuid: e694c68eba484299976b06ab9058f636
run_id: e13da8ac-b1e6-45d4-a9b2-6a0a5cfac537
signature:
  inputs: '[{"type": "tensor",
             "tensor-spec": 
                 {"dtype": "uint8", "shape": [-1, 300, 300, 3]}
           }]'
  outputs: '[{"type": "tensor", 
              "tensor-spec": 
                 {"dtype": "float32", "shape": [-1,2]}
            }]'
```

### Model flavor

Considering the large number of machine learning frameworks available, MLflow introduced the concept of *flavor* as a way to provide a unique contract for all machine learning frameworks. A flavor indicates what to expect for a given model that's created with a specific framework. For instance, TensorFlow has its own flavor, which specifies how to persist and load a TensorFlow model.

Because each model flavor indicates how to persist and load the model for a given framework, the MLmodel format doesn't enforce a single serialization mechanism that all models must support. Therefore, each flavor can use the methods that provide the best performance or best support according to their best practices, without compromising compatibility with the MLmodel standard.

The following example shows the `flavors` section for an `fastai` model.

```yaml
flavors:
  fastai:
    data: model.fastai
    fastai_version: 2.4.1
  python_function:
    data: model.fastai
    env: conda.yaml
    loader_module: mlflow.fastai
    python_version: 3.8.12
```

### Model signature

An MLflow [model signature](https://www.mlflow.org/docs/latest/models.html#model-signature) is an important part of the model specification, because it serves as a data contract between the model and the server running the model. A model signature is also important for parsing and enforcing a model's input types at deployment time.

If a signature is available, MLflow enforces the input types when data is submitted to your model. For more information, see [MLflow signature enforcement](https://www.mlflow.org/docs/latest/models.html#signature-enforcement).

Signatures are indicated when models get logged, and are persisted in the `signature` section of the *MLmodel* file. The **Autolog** feature in MLflow automatically makes a best effort to infer signatures. However, you can log models manually if the inferred signatures aren't the ones you need. For more information, see [How to log models with signatures](https://www.mlflow.org/docs/latest/models.html#how-to-log-models-with-signatures). 

There are two types of signatures:

- **Column-based signatures**  operate on tabular data. For models with this type of signature, MLflow supplies `pandas.DataFrame` objects as inputs.
- **Tensor-based signatures** operate with n-dimensional arrays or tensors. For models with this signature, MLflow supplies `numpy.ndarray` as inputs, or a dictionary of `numpy.ndarray` for named tensors.

The following *MLmodel* example shows a computer vision model trained with `fastai`. This model receives a batch of images represented as tensors of shape `(300, 300, 3)` with their RGB representation as unsigned integers. The model outputs batches of predictions as probabilities for two classes.

```yaml
signature:
  inputs: '[{"type": "tensor",
             "tensor-spec": 
                 {"dtype": "uint8", "shape": [-1, 300, 300, 3]}
           }]'
  outputs: '[{"type": "tensor", 
              "tensor-spec": 
                 {"dtype": "float32", "shape": [-1,2]}
            }]'
```

> [!TIP]
> Azure Machine Learning generates a swagger file for a deployment of an MLflow model that has an available signature. This file makes it easier to test deployments using Azure Machine Learning studio.

### Model environment

Requirements for the model to run are specified in the *conda.yaml* file. MLflow can automatically detect dependencies, or you can manually indicate them by calling the `mlflow.<flavor>.log_model()` method. Calling the method can be useful if the libraries that MLflow included in your environment aren't the ones you intended to use.

The following *conda.yaml* example shows an environment used for a model that's created with the `fastai` framework:

```yaml
channels:
- conda-forge
dependencies:
- python=3.8.5
- pip
- pip:
  - mlflow
  - astunparse==1.6.3
  - cffi==1.15.0
  - configparser==3.7.4
  - defusedxml==0.7.1
  - fastai==2.4.1
  - google-api-core==2.7.1
  - ipython==8.2.0
  - psutil==5.9.0
name: mlflow-env
```

While an MLflow environment operates at the level of the model, an Azure Machine Learning environment operates at the workspace level for registered environments or the jobs/deployments level for anonymous environments. When you deploy MLflow models, Azure Machine Learning builds the model's environment and uses it for deployment. You can use the [Azure Machine Learning CLI](concept-v2.md) to override this behavior and deploy MLflow models using a specific Azure Machine Learning environment.

### Predict function

All MLflow models contain a `predict` function that is called when the model is deployed by using a no-code deployment. What the `predict` function returns, such as classes, probabilities, or a forecast, depends on the framework or flavor used for training. The documentation of each flavor describes what it returns.

In same cases, you might need to customize the `predict` function to change the way inference is executed. In such cases, you need to [log models with a different behavior in the predict method](how-to-log-mlflow-models.md#logging-models-with-a-different-behavior-in-the-predict-method) or [log a custom model's flavor](how-to-log-mlflow-models.md#logging-custom-models).

## Workflows for loading MLflow models

You can load MLflow models from the following locations:

- Directly from the run where the models were logged
- From the file system where they models are saved
- From the model registry where the models are registered

MLflow provides a consistent way to load these models regardless of the location.

There are two workflows for loading models:

- **Load back the same object and types that were logged.** You can load models using the MLflow SDK and obtain an instance of the model with types belonging to the training library. For example, an ONNX model returns a `ModelProto`, while a decision tree model trained with `scikit-learn` returns a `DecisionTreeClassifier` object. Use `mlflow.<flavor>.load_model()` to load back the same model object and types that were logged.

- **Load back a model for running inference.** You can load models using the MLflow SDK and get a wrapper that has a guaranteed `predict` function. It doesn't matter which flavor you use, because every MLflow model has a `predict` function. MLflow guarantees that you can call this function by using arguments of type `pandas.DataFrame`, `numpy.ndarray`, or `dict[string, numpyndarray]`, depending on the model signature. MLflow handles the type conversion to the input type that the model expects. Use `mlflow.pyfunc.load_model()` to load back a model for running inference.

## Related content

- [Configure MLflow for Azure Machine Learning](how-to-use-mlflow-configure-tracking.md)
- [How to log MLFlow models](how-to-log-mlflow-models.md) 
- [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md)
