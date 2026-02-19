---
title: Entry scripts for advanced scenarios
titleSuffix: Azure Machine Learning
description: See how to write Azure Machine Learning entry scripts for advanced scenarios like schema generation, accepting raw data, and loading registered models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
ms.date: 03/11/2025
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: UpdateFrequency5, deploy, sdkv1
# customer intent: As a developer, I want to see how to use advanced entry scripts in Azure Machine Learning so that I can implement schema generation, accept raw data, and load registered models.
---

# Advanced entry scripts

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article explains how to write entry scripts for specialized use cases in Azure Machine Learning. An entry script, which is also called a scoring script, accepts requests, uses a model to score data, and returns a response.

## Prerequisites

A trained machine learning model that you intend to deploy with Azure Machine Learning. For more information about model deployment, see [Deploy machine learning models to Azure](how-to-deploy-and-where.md).

## Automatically generate a Swagger schema

To automatically generate a schema for your web service, provide a sample of the input or output in the constructor for one of the defined type objects. The type and sample are used to automatically create the schema. Azure Machine Learning then creates an [OpenAPI specification](https://swagger.io/docs/specification/about/) (formerly, a Swagger specification) for the web service during deployment.

> [!WARNING]
> Don't use sensitive or private data for the sample input or output. In Azure Machine Learning, the Swagger page for inferencing exposes the sample data.

The following types are currently supported:

* `pandas`
* `numpy`
* `pyspark`
* Standard Python object

To use schema generation, include the open-source `inference-schema` package version 1.1.0 or later in your dependencies file. For more information about this package, see [InferenceSchema on GitHub](https://github.com/Azure/InferenceSchema). In order to generate conforming Swagger for automated web service consumption, the `run` function in your scoring script must meet the following conditions:

* The first parameter must have the type `StandardPythonParameterType`, be named `Inputs`, and be nested.
* There must be an optional second parameter of type `StandardPythonParameterType` that's named `GlobalParameters`.
* The function must return a dictionary of type `StandardPythonParameterType` that's named `Results` and is nested.

Define the input and output sample formats in the `sample_input` and `sample_output` variables, which represent the request and response formats for the web service. Use these samples in the input and output function decorators on the `run` function. The `scikit-learn` example in the following section uses schema generation.

## Power BI-compatible endpoint

The following example demonstrates how to define the `run` function according to the instructions in the preceding section. You can use this script when you consume your deployed web service from Power BI.

```python
import os
import json
import pickle
import numpy as np
import pandas as pd
import azureml.train.automl
import joblib
from sklearn.linear_model import Ridge

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


def init():
    global model
    # Replace the file name if needed.
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'sklearn_regression_model.pkl')
    # Deserialize the model file back into a sklearn model.
    model = joblib.load(model_path)


# Provide three sample inputs for schema generation.
numpy_sample_input = NumpyParameterType(np.array([[1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1]],dtype='float64'))
pandas_sample_input = PandasParameterType(pd.DataFrame({'name': ['Sarah', 'John'], 'age': [25, 26]}))
standard_sample_input = StandardPythonParameterType(0.0)

# The following sample is a nested input sample. Any item wrapped by `ParameterType` is described by the schema.
sample_input = StandardPythonParameterType({'input1': numpy_sample_input, 
                                        'input2': pandas_sample_input, 
                                        'input3': standard_sample_input})

sample_global_parameters = StandardPythonParameterType(1.0) # This line is optional.
sample_output = StandardPythonParameterType([1.0, 1.0])
outputs = StandardPythonParameterType({'Results':sample_output}) # "Results" is case sensitive.

@input_schema('Inputs', sample_input) 
# "Inputs" is case sensitive.

@input_schema('GlobalParameters', sample_global_parameters) 
# The preceding line is optional. "GlobalParameters" is case sensitive.

@output_schema(outputs)

def run(Inputs, GlobalParameters): 
    # The parameters in the preceding line have to match those in the decorator. "Inputs" and 
    # "GlobalParameters" are case sensitive.
    try:
        data = Inputs['input1']
        # The data gets converted to the target format.
        assert isinstance(data, np.ndarray)
        result = model.predict(data)
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
```

> [!TIP]
> The return value from the script can be any Python object that's serializable to JSON. For example, if your model returns a Pandas dataframe that contains multiple columns, you can use an output decorator that's similar to the following code:
> 
> ```python
> output_sample = pd.DataFrame(data=[{"a1": 5, "a2": 6}])
> @output_schema(PandasParameterType(output_sample))
> ...
> result = model.predict(data)
> return result
> ```

## <a id="binary-data"></a> Binary (image) data

If your model accepts binary data, like an image, you must modify the score.py file that your deployment uses so that it accepts raw HTTP requests. To accept raw data, use the `AMLRequest` class in your entry script and add the `@rawhttp` decorator to the `run` function.

The following score.py script accepts binary data:

```python
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse
from PIL import Image
import json

def init():
    print("This is init()")

@rawhttp
def run(request):
    print("This is run()")
    
    if request.method == 'GET':
        # For this example, return the URL for GET requests.
        respBody = str.encode(request.full_path)
        return AMLResponse(respBody, 200)
    elif request.method == 'POST':
        file_bytes = request.files["image"]
        image = Image.open(file_bytes).convert('RGB')
        # For a real-world solution, load the data from the request body
        # and send it to the model. Then return the response.

        # For demonstration purposes, this example returns the size of the image as the response.
        return AMLResponse(json.dumps(image.size), 200)
    else:
        return AMLResponse("bad request", 500)
```

> [!IMPORTANT]
> The `AMLRequest` class is in the `azureml.contrib` namespace. Entities in this namespace are in preview. They change frequently while the service undergoes improvements. Microsoft doesn't offer full support for these entities.
>
> If you need to test code that uses this class in your local development environment, you can install the components by using the following command:
>
> ```shell
> pip install azureml-contrib-services
> ```

> [!NOTE]
> We don't recommend using `500` as a custom status code. On the Azure Machine Learning inference router (`azureml-fe`) side, the status code is rewritten to `502`.
> 
> * The status code is passed through `azureml-fe` and then sent to the client.
> * The `azureml-fe` code rewrites the `500` that's returned from the model side as `502`. The client receives a code of `502`.
> * If the `azureml-fe` code itself returns `500`, the client side still receives a code of `500`.

When you use the `AMLRequest` class, you can access only the raw posted data in the score.py file. There's no client-side component. From a client, you can post data as usual. For example, the following Python code reads an image file and posts the data:

```python
import requests

uri = service.scoring_uri
image_path = 'test.jpg'
files = {'image': open(image_path, 'rb').read()}
response = requests.post(uri, files=files)

print(response.json)
```

<a id="cors"></a>

## Cross-origin resource sharing

Cross-origin resource sharing (CORS) provides a way for resources on a webpage to be requested from another domain. CORS works via HTTP headers that are sent with the client request and returned with the service response. For more information about CORS and valid headers, see [Cross-origin resource sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing).

To configure your model deployment to support CORS, use the `AMLResponse` class in your entry script. When you use this class, you can set the headers on the response object.

The following example sets the `Access-Control-Allow-Origin` header for the response from the entry script:

```python
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse


def init():
    print("This is init()")

@rawhttp
def run(request):
    print("This is run()")
    print("Request: [{0}]".format(request))
    if request.method == 'GET':
        # For this example, just return the URL for GET.
        # For a real-world solution, you would load the data from URL params or headers
        # and send it to the model. Then return the response.
        respBody = str.encode(request.full_path)
        resp = AMLResponse(respBody, 200)
        resp.headers["Allow"] = "OPTIONS, GET, POST"
        resp.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = "http://www.example.com"
        resp.headers['Access-Control-Allow-Headers'] = "*"
        return resp
    elif request.method == 'POST':
        reqBody = request.get_data(False)
        # For a real-world solution, you would load the data from reqBody
        # and send it to the model. Then return the response.
        resp = AMLResponse(reqBody, 200)
        resp.headers["Allow"] = "OPTIONS, GET, POST"
        resp.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = "http://www.example.com"
        resp.headers['Access-Control-Allow-Headers'] = "*"
        return resp
    elif request.method == 'OPTIONS':
        resp = AMLResponse("", 200)
        resp.headers["Allow"] = "OPTIONS, GET, POST"
        resp.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
        resp.headers['Access-Control-Allow-Origin'] = "http://www.example.com"
        resp.headers['Access-Control-Allow-Headers'] = "*"
        return resp
    else:
        return AMLResponse("bad request", 400)
```

> [!IMPORTANT]
> The `AMLRequest` class is in the `azureml.contrib` namespace. Entities in this namespace are in preview. They change frequently while the service undergoes improvements. Microsoft doesn't offer full support for these entities.
>
> If you need to test code that uses this class in your local development environment, you can install the components by using the following command:
>
> ```shell
> pip install azureml-contrib-services
> ```

> [!WARNING]
> Azure Machine Learning routes only POST and GET requests to the containers that run the scoring service. Errors can result if browsers use OPTIONS requests to issue preflight requests.

## Load registered models

There are two ways to locate models in your entry script:

* `AZUREML_MODEL_DIR`: An environment variable that contains the path to the model location
* `Model.get_model_path`: An API that returns the path to the model file by using the registered model name

#### AZUREML_MODEL_DIR

`AZUREML_MODEL_DIR` is an environment variable that's created during service deployment. You can use this environment variable to find the location of deployed models.

The following table describes possible values of `AZUREML_MODEL_DIR` for a varying number of deployed models:

| Deployment | Environment variable value |
| ----- | ----- |
| Single model | The path to the folder that contains the model. |
| Multiple models | The path to the folder that contains all models. Models are located by name and version in this folder in the format `<model-name>/<version>`. |

During model registration and deployment, models are placed in the `AZUREML_MODEL_DIR` path, and their original file names are preserved.

To get the path to a model file in your entry script, combine the environment variable with the file path you're looking for.

##### Single model

The following example shows you how to find the path when you have a single model:

```python
import os

# In the following example, the model is a file.
model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'sklearn_regression_model.pkl')

# In the following example, the model is a folder that contains a file.
file_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'my_model_folder', 'sklearn_regression_model.pkl')
```

##### Multiple models

The following example shows you how to find the path when you have multiple models. In this scenario, two models are registered with the workspace:

* `my_first_model`: This model contains one file, my_first_model.pkl, and has one version, `1`.
* `my_second_model`: This model contains one file, my_second_model.pkl, and has two versions, `1` and `2`.

When you deploy the service, you provide both models in the deploy operation:

```python
from azureml.core import Workspace, Model

# Get a handle to the workspace.
ws = Workspace.from_config()

first_model = Model(ws, name="my_first_model", version=1)
second_model = Model(ws, name="my_second_model", version=2)
service = Model.deploy(ws, "myservice", [first_model, second_model], inference_config, deployment_config)
```

In the Docker image that hosts the service, the `AZUREML_MODEL_DIR` environment variable contains the folder where the models are located. In this folder, each model is located in a folder path of `<model-name>/<version>`. In this path, `<model-name>` is the name of the registered model, and `<version>` is the version of the model. The files that make up the registered model are stored in these folders.

In this example, the path of the first model is `$AZUREML_MODEL_DIR/my_first_model/1/my_first_model.pkl`. The path of the second model is `$AZUREML_MODEL_DIR/my_second_model/2/my_second_model.pkl`.

```python
# In the following example, the model is a file, and the deployment contains multiple models.
first_model_name = 'my_first_model'
first_model_version = '1'
first_model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), first_model_name, first_model_version, 'my_first_model.pkl')
second_model_name = 'my_second_model'
second_model_version = '2'
second_model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), second_model_name, second_model_version, 'my_second_model.pkl')
```

### get_model_path

When you register a model, you provide a model name that's used for managing the model in the registry. You use this name with the [`Model.get_model_path`](/python/api/azureml-core/azureml.core.model.model#azureml-core-model-model-get-model-path) method to retrieve the path of the model file or files on the local file system. If you register a folder or a collection of files, this API returns the path of the folder that contains those files.

When you register a model, you give it a name. The name corresponds to where the model is placed, either locally or during service deployment.

## Framework-specific examples

For more entry script examples for specific machine learning use cases, see the following articles:

* [PyTorch](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/ml-frameworks/pytorch)
* [TensorFlow](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/ml-frameworks/tensorflow)
* [Keras](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/ml-frameworks/keras/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb)
* [Automated machine learning](https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/automated-machine-learning/classification-bank-marketing-all-features)

## Related content

* [Troubleshooting remote model deployment](how-to-troubleshoot-deployment.md)
* [Consume an Azure Machine Learning model deployed as a web service](how-to-consume-web-service.md)
* [Update a deployed web service (v1)](how-to-deploy-update-web-service.md)
