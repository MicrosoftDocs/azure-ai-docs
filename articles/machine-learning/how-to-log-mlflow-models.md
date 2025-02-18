---
title: Log MLflow models
titleSuffix: Azure Machine Learning
description: Logging MLflow models, instead of artifacts, with MLflow SDK in Azure Machine Learning
services: machine-learning
author: msakande
ms.author: mopeakande
ms.reviewer: fasantia
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 02/16/2024
ms.topic: conceptual
ms.custom: cliv2, sdkv2
---

# Log MLflow models

This article describes how to log your trained models (or artifacts) as MLflow models. It explores various ways of customizing how MLflow packages and runs models.

## Why log models instead of artifacts?

An MLflow model is a type of artifact. However, a model has a specific structure that serves as a contract between the person that creates the model and the person that intends to use it. This contract helps build a bridge between the artifacts themselves and their meanings.

For the difference between logging artifacts, or files, and logging MLflow models, see [Artifacts and models in MLflow](concept-mlflow-models.md). 

You can log your model's files as artifacts, but model logging offers the following advantages:

* You can use `mlflow.<flavor>.load_model` to directly load models for inference, and you can use the `predict` function.
* Pipeline inputs can use models directly.
* You can deploy models without specifying a scoring script or an environment.
* Swagger is automatically turned on in deployed endpoints. As a result, you can use the Azure Machine Learning studio test feature.
* You can use the Responsible AI dashboard. For more information, see [Use the Responsible AI dashboard in Azure Machine Learning studio](how-to-responsible-ai-dashboard.md).

## Use automatic logging to log models

You can use MLflow `autolog` functionality to automatically log models. When you use automatic logging, MLflow instructs the framework that's in use to log all the metrics, parameters, artifacts, and models that the framework considers relevant. By default, if automatic logging is turned on, most models are logged. In some situations, some flavors don't log models. For instance, the PySpark flavor doesn't log models that exceed a certain size.

Use either `mlflow.autolog` or `mlflow.<flavor>.autolog` to activate automatic logging. The following code uses `autolog` to log a classifier model that's trained with XGBoost:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

mlflow.autolog()

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
```

> [!TIP]
> If you use machine learning pipelines, for example [Scikit-Learn pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), use the `autolog` functionality of that pipeline flavor to log models. Model logging automatically happens when the `fit` method is called on the pipeline object. For a notebook that logs a model and that includes preprocessing and uses pipelines, see [Training and tracking an XGBoost classifier with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_classification_mlflow.ipynb).

## Log models that use a custom signature, environment, or samples

You can use the MLflow `mlflow.<flavor>.log_model` method to manually log models. This workflow can control various aspects of model logging.

Use this method when:

* You want to indicate pip packages or a Conda environment that differs from the automatically detected packages or environment.
* You want to include input examples.
* You want to include specific artifacts in the package that you need.
* The `autolog` method doesn't correctly infer your signature. This case comes up when you work with tensor inputs, which require the signature to have a specific shape.
* The `autolog` method doesn't meet all your needs.

The following code logs an XGBoost classifier model:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature
from mlflow.utils.environment import _mlflow_conda_env

mlflow.autolog(log_models=False)

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

# Infer the signature.
signature = infer_signature(X_test, y_test)

# Set up a Conda environment.
custom_env =_mlflow_conda_env(
    additional_conda_deps=None,
    additional_pip_deps=["xgboost==1.5.2"],
    additional_conda_channels=None,
)

# Sample the data.
input_example = X_train.sample(n=1)

# Log the model manually.
mlflow.xgboost.log_model(model, 
                         artifact_path="classifier", 
                         conda_env=custom_env,
                         signature=signature,
                         input_example=input_example)
```

> [!NOTE]
> * The call to `autolog` uses a configuration of `log_models=False`. This setting turns off automatic MLflow model logging. The `log_model` method is used later to manually log the model.
> * The `infer_signature` method is used to try to infer the signature directly from inputs and outputs.
> * The `mlflow.utils.environment._mlflow_conda_env` method is a private method in the MLflow SDK. In this example, it streamlines the code. But use this method with caution, because it might change in the future. As an alternative, you can generate the YAML definition manually as a Python dictionary.

## Log models with a different behavior in the predict method

When you use `mlflow.autolog` or `mlflow.<flavor>.log_model` to log a model, the model flavor determines how to perform the inference. The flavor also determines what the model returns. MLflow doesn't enforce any specific behavior about the generation of `predict` results. In some scenarios, you might want to do some preprocessing or post-processing before and after your model runs.

In this situation, you can implement machine learning pipelines that directly move from inputs to outputs. Although this type of implementation can sometimes improve performance, it can be challenging to achieve.

## Logging custom models

In cases that involve implementing pipelines that directly move from inputs to outputs, it can help to customize the way your model handles inference.

MLflow supports many machine learning frameworks, including the following flavors:

- CatBoost
- FastAI
- h2o
- Keras
- LightGBM
- MLeap
- MXNet Gluon
- ONNX
- Prophet
- PyTorch
- Scikit-Learn
- spaCy
- Spark MLLib
- statsmodels
- TensorFlow
- XGBoost

For a complete list, see [Built-In Model Flavors](https://mlflow.org/docs/latest/models.html#built-in-model-flavors).

However, you might need to change the way a flavor works or log a model that's not natively supported by MLflow. Or you might need to log a model that uses multiple elements from various frameworks. In these cases, you might need to create a custom model flavor.

To solve the problem, MLflow offers the `pyfunc` flavor, a default model interface for Python models. This flavor can log any object as a model, as long as that object satisfies two conditions:

* You implement at least the `predict` method.
* The Python object inherits from the `mlflow.pyfunc.PythonModel` class.

> [!TIP]
> Serializable models that implement the Scikit-learn API can use the `Scikit-learn` flavor to log the model, regardless of whether the model was built with `Scikit-learn`. If you can persist your model in Pickle format, and the object has at least the `predict` and `predict_proba` methods, you can use `mlflow.sklearn.log_model` to log the model inside an MLflow run.

# [Use a model wrapper](#tab/wrapper)

The easiest way to create a flavor for your custom model is to create a wrapper around your existing model object. MLflow serializes and packages it for you. Python objects are serializable when the object can be stored in the file system as a file, generally in Pickle format. At runtime, the object can materialize from that file. This restores all the values, properties, and methods available when it was saved.

Use this method when:

* You can serialize your model in Pickle format.
* You want to retain the state of the model just after training.
* You want to customize how the `predict` function works.

This code sample wraps a model created with XGBoost, to make it behave in a different from the XGBoost flavor default implementation. Instead, it returns the probabilities instead of the classes:

```python
from mlflow.pyfunc import PythonModel, PythonModelContext

class ModelWrapper(PythonModel):
    def __init__(self, model):
        self._model = model

    def predict(self, context: PythonModelContext, data):
        # You don't have to keep the semantic meaning of `predict`. You can use here model.recommend(), model.forecast(), etc
        return self._model.predict_proba(data)

    # You can even add extra functions if you need to. Since the model is serialized,
    # all of them will be available when you load your model back.
    def predict_batch(self, data):
        pass
```

Log a custom model in the run:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.xgboost.autolog(log_models=False)

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

signature = infer_signature(X_test, y_probs)
mlflow.pyfunc.log_model("classifier", 
                        python_model=ModelWrapper(model),
                        signature=signature)
```

> [!TIP]
> Here, the `infer_signature` method uses `y_probs` to infer the signature. Our target column has the target class, but our model now returns the two probabilities for each class.

# [Using artifacts](#tab/artifacts)

Your model might be composed of multiple pieces that need to be loaded. You might not have a way to serialize it as a Pickle file. In those cases, the `PythonModel` supports indication of an arbitrary list of **artifacts**. Each artifact is packaged along with your model.

Use this technique when:
> [!div class="checklist"]
> * You can't serialize your model in Pickle format, or you have a better serialization format available
> * Your model has one, or many, artifacts must be referenced to load the model
> * You might want to persist some inference configuration properties - for example, the number of items to recommend
> * You want to customize the way the model loads, and how the `predict` function works

This code sample shows how to log a custom model, using artifacts:

```python
encoder_path = 'encoder.pkl'
joblib.dump(encoder, encoder_path)

model_path = 'xgb.model'
model.save_model(model_path)

mlflow.pyfunc.log_model("classifier", 
                        python_model=ModelWrapper(),
                        artifacts={ 
                            'encoder': encoder_path,
                            'model': model_path 
                        },
                        signature=signature)
```

> [!NOTE]
> * The model is not saved as a pickle. Instead, the code saved the model with save method of the framework that you used
> * The model wrapper is `ModelWrapper()`, but the model is not passed as a parameter to the constructor
> A new dictionary parameter - `artifacts` - has keys as the artifact names, and values as the path in the local file system where the artifact is stored

The corresponding model wrapper then would look like this:

```python
from mlflow.pyfunc import PythonModel, PythonModelContext

class ModelWrapper(PythonModel):
    def load_context(self, context: PythonModelContext):
        import pickle
        from xgboost import XGBClassifier
        from sklearn.preprocessing import OrdinalEncoder
        
        self._encoder = pickle.loads(context.artifacts["encoder"])
        self._model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self._model.load_model(context.artifacts["model"])

    def predict(self, context: PythonModelContext, data):
        return self._model.predict_proba(data)
```

The complete training routine would look like this:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.xgboost.autolog(log_models=False)

encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan)
X_train['thal'] = encoder.fit_transform(X_train['thal'].to_frame())
X_test['thal'] = encoder.transform(X_test['thal'].to_frame())

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

encoder_path = 'encoder.pkl'
joblib.dump(encoder, encoder_path)
model_path = "xgb.model"
model.save_model(model_path)

signature = infer_signature(X, y_probs)
mlflow.pyfunc.log_model("classifier", 
                        python_model=ModelWrapper(),
                        artifacts={ 
                            'encoder': encoder_path,
                            'model': model_path 
                        },
                        signature=signature)
```

# [Using a model loader](#tab/loader)

A model might have complex logic, or it might load several source files at inference time. This happens if you have a Python library for your model, for example. In this scenario, you should package the library along with your model, so it can move as a single piece.

Use this technique when:
> [!div class="checklist"]
> * You can't serialize your model in Pickle format, or you have a better serialization format available
> * You can store your model artifacts in a folder which stores all the required artifacts
> * Your model source code has great complexity, and it requires multiple Python files. Potentially, a library supports your model
> * You want to customize the way the model loads, and how the `predict` function operates

MLflow supports these models. With MLflow, you can specify any arbitrary source code to package along with the model, as long as it has a *loader module*. You can specify loader modules in the `log_model()` instruction with the `loader_module` argument, which indicates the Python namespace that implements the loader. The `code_path` argument is also required, to indicate the source files that define the `loader_module`. In this namespace, you must implement a `_load_pyfunc(data_path: str)` function that receives the path of the artifacts, and returns an object with a method predict (at least).

```python
model_path = 'xgb.model'
model.save_model(model_path)

mlflow.pyfunc.log_model("classifier", 
                        data_path=model_path,
                        code_path=['src'],
                        loader_module='loader_module'
                        signature=signature)
```

> [!NOTE]
> * The model is not saved as a pickle. Instead, the code saved the model with save method of the framework that you used
> * A new parameter - `data_path` - points to the folder that holds the model artifacts. The artifacts can be a folder or a file. Those artifacts - either a folder or a file - will be packaged with the model
> * A new parameter - `code_path` - points to the source code location. This resource at this location can be a path or a single file. That resource - either a folder or a file - will be packaged with the model
> * The function `_load_pyfunc` function is stored in the `loader_module` Python module

The `src` folder contains the `loader_module.py` file. That file is the loader module:

__src/loader_module.py__

```python
class MyModel():
    def __init__(self, model):
        self._model = model

    def predict(self, data):
        return self._model.predict_proba(data)

def _load_pyfunc(data_path: str):
    import os

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.load_model(os.path.abspath(data_path))

    return MyModel(model)
```

> [!NOTE]
> * The `MyModel` class doesn't inherit from `PythonModel` as shown earlier. However, it has a `predict` function
> * The model source code is in a file. Any source code will work. A **src** folder is ideal for this
> * A `_load_pyfunc` function returns an instance of the class of the model

The complete training code looks like this:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.xgboost.autolog(log_models=False)

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

model_path = "xgb.model"
model.save_model(model_path)

signature = infer_signature(X_test, y_probs)
mlflow.pyfunc.log_model("classifier",
                        data_path=model_path,
                        code_path=["loader_module.py"],
                        loader_module="loader_module",
                        signature=signature)
```

---

## Next steps

* [Deploy MLflow models](how-to-deploy-mlflow-models.md)