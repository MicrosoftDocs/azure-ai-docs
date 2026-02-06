---
title: Log MLflow models
titleSuffix: Azure Machine Learning
description: See how to use the MLflow SDK to log MLflow models as models, not artifacts, in Azure Machine Learning. Find out how to log custom models and use automatic logging.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 02/06/2026
ms.topic: how-to
ms.custom: cliv2, sdkv2, dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to see how to log MLflow models so that I can use automatic logging or custom models.
---

# Log MLflow models

This article describes how to log your trained machine learning models, or artifacts, as MLflow models. MLflow is an open-source framework for managing machine learning workflows. This article explores various options for customizing the way that MLflow packages and runs models.

## Prerequisites

* The MLflow SDK `mlflow` package (version 2.16.x or earlier)
* The Azure Machine Learning MLflow plugin `azureml-mlflow`
* The `xgboost` package (version 2.1.1 or earlier)
* The `scikit-learn` package

> [!IMPORTANT]
> Azure Machine Learning is compatible with MLflow 2.16 and earlier. MLflow 2.17 and later introduces artifact repository and LoggedModels API changes that the `azureml-mlflow` plugin doesn't currently support. Pin your MLflow and XGBoost versions to avoid compatibility issues.

```bash
pip install "mlflow<=2.16.2" azureml-mlflow "xgboost<=2.1.1" scikit-learn
```

## Use automatic logging to log models

Use MLflow `autolog` functionality to automatically log models. When you use automatic logging, MLflow captures all relevant metrics, parameters, artifacts, and models in your framework. The data that's logged depends on the framework. By default, if you turn on automatic logging, most models are logged. In some situations, some flavors don't log models. For instance, the PySpark flavor doesn't log models that exceed a certain size.

Use either `mlflow.autolog` or `mlflow.<flavor>.autolog` to activate automatic logging. The following code uses `autolog` to log a classifier model that's trained with XGBoost:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load sample data and split into train/test sets.
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.autolog()

model = XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
```

**Reference:** [`mlflow.autolog`](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.autolog) | [`XGBClassifier`](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier) | [`accuracy_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)

> [!NOTE]
> The remaining code examples in this article reuse the `X_train`, `X_test`, `y_train`, and `y_test` variables from the preceding sample data setup.

> [!TIP]
> If you use machine learning pipelines, such as [scikit-learn pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), use the `autolog` functionality of that pipeline flavor to log models. Model logging automatically runs when you call the `fit` method on the pipeline object. For a notebook that logs a model, includes preprocessing, and uses pipelines, see [Training and tracking an XGBoost classifier with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_classification_mlflow.ipynb).

## Why log models instead of artifacts?

Logging models rather than raw artifacts provides a structured contract between model creators and consumers. For a detailed comparison, see [Artifacts and models in MLflow](concept-mlflow-models.md).

Model logging offers the following advantages:

* You can use `mlflow.<flavor>.load_model` to directly load models for inference, and you can use the `predict` function.
* Pipeline inputs can use models directly.
* You can deploy models without specifying a scoring script or an environment.
* Swagger is automatically turned on in deployed endpoints. As a result, you can use the test feature in Azure Machine Learning studio to test models.
* You can use the Responsible AI dashboard. For more information, see [Use the Responsible AI dashboard in Azure Machine Learning studio](how-to-responsible-ai-dashboard.md).

## Log models that use a custom signature, environment, or samples

Use the MLflow `mlflow.<flavor>.log_model` method to manually log models. This workflow gives you control over various aspects of model logging.

Use this method when:

* You want to specify a Conda environment or pip packages that differ from the automatically detected packages or environment.
* You want to include input examples.
* You want to include specific artifacts in the package.
* The `autolog` method doesn't correctly infer your signature. This problem can occur when you work with tensor inputs, which require the signature to have a specific shape.
* The `autolog` method doesn't meet all your needs.

The following code logs an XGBoost classifier model:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.autolog(log_models=False)

model = XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

# Infer the signature.
signature = infer_signature(X_test, y_test)

# Sample the data.
input_example = X_train.sample(n=1)

# Log the model manually.
mlflow.xgboost.log_model(model, 
                         artifact_path="classifier", 
                         pip_requirements=["xgboost>=2.0"],
                         signature=signature,
                         input_example=input_example)
```

**Reference:** [`mlflow.xgboost.log_model`](https://mlflow.org/docs/latest/python_api/mlflow.xgboost.html#mlflow.xgboost.log_model) | [`infer_signature`](https://mlflow.org/docs/latest/python_api/mlflow.models.html#mlflow.models.infer_signature)

> [!NOTE]
> * The call to `autolog` uses a configuration of `log_models=False`. This setting turns off automatic MLflow model logging. The `log_model` method is used later to manually log the model.
> * The `infer_signature` method tries to infer the signature directly from inputs and outputs.
> * The `pip_requirements` parameter specifies the packages required for the model. As an alternative, you can use the `conda_env` parameter with a dictionary or YAML file.

## Log models that use modified prediction behavior

When you use `mlflow.autolog` or `mlflow.<flavor>.log_model` to log a model, the model flavor determines how the inference is performed. The flavor also determines what the model returns. MLflow doesn't enforce specific behavior about the generation of `predict` results. In some scenarios, you might want to preprocess or post-process your data.

In this situation, you can implement machine learning pipelines that directly move from inputs to outputs. Although this type of implementation can sometimes improve performance, it can be challenging to achieve. In such cases, it can be helpful to customize how your model handles inference. For more information, see the next section, [Log custom models](#log-custom-models).

## Log custom models

MLflow supports many machine learning frameworks, including CatBoost, Keras, LightGBM, ONNX, PyTorch, scikit-learn, Spark MLlib, TensorFlow, XGBoost, and others. For a complete list, see [Built-In Model Flavors](https://mlflow.org/docs/latest/models.html#built-in-model-flavors).

However, you might need to change the way a flavor works or log a model that MLflow doesn't natively support. Or you might need to log a model that uses multiple elements from various frameworks. In these cases, you can create a custom model flavor.

To solve the problem, MLflow offers the PyFunc flavor, a default model interface for Python models. This flavor can log any object as a model as long as that object satisfies two conditions:

* You implement at least the `predict` method.
* The Python object inherits from the `mlflow.pyfunc.PythonModel` class.

> [!TIP]
> Serializable models that implement the scikit-learn API can use the scikit-learn flavor to log the model, regardless of whether the model was built with scikit-learn. If you can persist your model in Pickle format, and the object has at least the `predict` and `predict_proba` methods, use `mlflow.sklearn.log_model` to log the model inside an MLflow run.

# [Use a model wrapper](#tab/wrapper)

The easiest way to create a flavor for your custom model is to create a wrapper around your existing model object. MLflow serializes and packages your model for you. Python objects are serializable when the object can be stored in the file system as a file, generally in Pickle format. At runtime, the object can be loaded from that file. Loading restores all the values, properties, and methods that are available when it's saved.

Use this method when:

* You can serialize your model in Pickle format.
* You want to retain the state of the model just after training.
* You want to customize how the `predict` function works.

The following code wraps a model created with XGBoost so that it behaves differently than the XGBoost flavor default implementation. It returns probabilities instead of classes.

```python
from mlflow.pyfunc import PythonModel, PythonModelContext

class ModelWrapper(PythonModel):
    def __init__(self, model):
        self._model = model

    def predict(self, context: PythonModelContext, data, params=None):
        # The next line uses a prediction function. However, you could also use model.recommend(), model.forecast(), or a similar function instead.
        return self._model.predict_proba(data)

    # You can add extra functions if you need to. Because the model is serialized,
    # all of them are available when you load your model.
    def predict_batch(self, data):
        pass
```

Use the following code to log a custom model during a run:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.xgboost.autolog(log_models=False)

model = XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

signature = infer_signature(X_test, y_probs)
mlflow.pyfunc.log_model(artifact_path="classifier", 
                        python_model=ModelWrapper(model),
                        signature=signature)
```

**Reference:** [`mlflow.pyfunc.log_model`](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model) | [`PythonModel`](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#mlflow.pyfunc.PythonModel)

> [!TIP]
> In the preceding code, the `infer_signature` method uses `y_probs` to infer the signature. The target column contains the target class, but the model returns two probabilities for each class.

# [Use artifacts](#tab/artifacts)

Sometimes a model is composed of multiple pieces that you need to load. Sometimes, you can't serialize the model as a Pickle file. In these cases, use the `PythonModel` class. It supports an arbitrary list of artifacts. Package each artifact along with your model.

Use this technique when:

* You can't serialize your model in Pickle format, or you have a better serialization format available.
* Your model has one or more artifacts that must be referenced to load the model.
* You want to persist some inference configuration properties, such as the number of items to recommend.
* You want to customize the way the model is loaded and how the `predict` function works.

The following code shows how to log a custom model that uses artifacts:

```python
encoder_path = 'encoder.pkl'
joblib.dump(encoder, encoder_path)

model_path = 'xgb.model'
model.save_model(model_path)

mlflow.pyfunc.log_model(artifact_path="classifier", 
                        python_model=ModelWrapper(),
                        artifacts={ 
                            'encoder': encoder_path,
                            'model': model_path 
                        },
                        signature=signature)
```

> [!NOTE]
> * The model isn't saved in Pickle format. Instead, the code saves the model by using the save method of the framework that you use.
> * The `ModelWrapper` class wraps the model, but the model isn't passed as an argument to the `ModelWrapper` constructor.
> * The `log_model` method has a dictionary parameter, `artifacts`. Its keys hold artifact names. Each value contains the path in the local file system to an artifact.

The corresponding model wrapper looks similar to the following code:

```python
from mlflow.pyfunc import PythonModel, PythonModelContext

class ModelWrapper(PythonModel):
    def load_context(self, context: PythonModelContext):
        import pickle
        from xgboost import XGBClassifier
        from sklearn.preprocessing import OrdinalEncoder
        
        self._encoder = pickle.loads(context.artifacts["encoder"])
        self._model = XGBClassifier(eval_metric="logloss")
        self._model.load_model(context.artifacts["model"])

    def predict(self, context: PythonModelContext, data, params=None):
        return self._model.predict_proba(data)
```

The complete training routine looks similar to the following code:

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

model = XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

encoder_path = 'encoder.pkl'
joblib.dump(encoder, encoder_path)
model_path = "xgb.model"
model.save_model(model_path)

signature = infer_signature(X, y_probs)
mlflow.pyfunc.log_model(artifact_path="classifier", 
                        python_model=ModelWrapper(),
                        artifacts={ 
                            'encoder': encoder_path,
                            'model': model_path 
                        },
                        signature=signature)
```

# [Use a model loader](#tab/loader)

A model sometimes has complex logic, or it loads several source files at inference time. This situation occurs when you have a Python library for your model, for example. In this scenario, package the library along with your model so they function as a single piece.

Use this technique when:

* You can't serialize your model in Pickle format, or you have a better serialization format available.
* You can store your model artifacts in a folder that stores all required artifacts.
* Your model source code is complex, and it requires multiple Python files. Potentially, a library supports your model.
* You want to customize the way the model is loaded and how the `predict` function operates.

MLflow supports these types of models. When you use MLflow, you can specify arbitrary source code to package along with the model, as long as the source code has a *loader module*. You can specify loader modules in the call to `log_model` by using the `loader_module` parameter, which indicates the Python namespace that implements the loader. The `code_paths` parameter is also required. It provides the source files that define the loader module. In this namespace, you must implement a `_load_pyfunc(data_path: str)` function that receives the path of the artifacts and returns an object that implements at least a `predict` method.

```python
model_path = 'xgb.model'
model.save_model(model_path)

mlflow.pyfunc.log_model(artifact_path="classifier", 
                        data_path=model_path,
                        code_paths=['src'],
                        loader_module='loader_module',
                        signature=signature)
```

> [!NOTE]
> * The model isn't saved in Pickle format. Instead, the code saves the model by using the save method of the framework that you use.
> * The `log_model` method has a `data_path` parameter that points to the folder that holds the model artifacts. The artifacts can be in a folder or a file. The artifacts are packaged with the model.
> * The `log_model` method has a `code_paths` parameter that points to the location of the source code. The `code_paths` value can be a path or a single file. The source code is packaged with the model.
> * The `_load_pyfunc` function is stored in the `loader_module` Python module.

The src folder contains the `loader_module.py` file. That file serves as the loader module and contains the following lines:

```python
class MyModel():
    def __init__(self, model):
        self._model = model

    def predict(self, data):
        return self._model.predict_proba(data)

def _load_pyfunc(data_path: str):
    import os

    model = XGBClassifier(eval_metric='logloss')
    model.load_model(os.path.abspath(data_path))

    return MyModel(model)
```

> [!NOTE]
> * The `MyModel` class doesn't inherit from `PythonModel` as shown earlier. However, it has a `predict` function.
> * The model source code is in a file. Any source code is suitable. A folder named src is ideal in this situation.
> * A `_load_pyfunc` function returns an instance of the class of the model.

The complete training routine looks similar to the following code:

```python
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

mlflow.xgboost.autolog(log_models=False)

model = XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
y_probs = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_probs.argmax(axis=1))
mlflow.log_metric("accuracy", accuracy)

model_path = "xgb.model"
model.save_model(model_path)

signature = infer_signature(X_test, y_probs)
mlflow.pyfunc.log_model(artifact_path="classifier",
                        data_path=model_path,
                        code_paths=["loader_module.py"],
                        loader_module="loader_module",
                        signature=signature)
```

**Reference:** [`mlflow.pyfunc.log_model`](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model) | [`_load_pyfunc`](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#creating-custom-pyfunc-models)

---

## Next step

* [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md)