---
title: Train deep learning Keras models (SDK v2)
titleSuffix: Azure Machine Learning
description: Learn how to train and register a Keras deep neural network classification model running on TensorFlow using Azure Machine Learning SDK (v2).
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.author: scottpolly
author: s-polly
ms.reviewer: sooryar
ms.date: 03/26/2026
ms.topic: how-to
ms.custom: sdkv2, update-code
#Customer intent: As a Python Keras developer, I need to combine open-source with a cloud platform to train, evaluate, and deploy my deep learning models at scale.
---

# Train Keras models at scale with Azure Machine Learning

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

In this article, you learn how to run your Keras training scripts by using the Azure Machine Learning Python SDK v2.

The example code in this article uses Azure Machine Learning to train, register, and deploy a Keras model that uses the TensorFlow backend. The model is a deep neural network (DNN) built with the [Keras Python library](https://keras.io) and the [TensorFlow](https://www.tensorflow.org/overview) backend. It classifies handwritten digits from the popular [MNIST dataset](https://www.tensorflow.org/datasets/catalog/mnist).

Keras is a high-level neural network API that supports multiple backends - including TensorFlow, JAX, and PyTorch - to simplify deep learning development. By using Azure Machine Learning, you can rapidly scale out training jobs by using elastic cloud compute resources. You can also track your training runs, version models, deploy models, and much more.

Whether you're developing a Keras model from the ground up or bringing an existing model into the cloud, Azure Machine Learning can help you build production-ready models.

> [!NOTE]
> This article uses the standalone `keras` package (Keras 3) with the TensorFlow backend. By using TensorFlow 2.16 and later, `from tensorflow import keras` also uses Keras 3. If you're using TensorFlow 2.15 or earlier, where `tf.keras` refers to Keras 2, see [Train TensorFlow models](how-to-train-tensorflow.md) instead.

## Prerequisites

To benefit from this article, you need to:

- Access an Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Run the code in this article by using either an Azure Machine Learning compute instance or your own Jupyter notebook.
    - Azure Machine Learning compute instance – no downloads or installation necessary
        - Complete [Create resources to get started](quickstart-create-resources.md) to create a dedicated notebook server preloaded with the SDK and the sample repository.
        - In the samples deep learning folder on the notebook server, find a completed and expanded notebook by going to this directory: **v2  > sdk > python > jobs > single-step > tensorflow > train-hyperparameter-tune-deploy-with-keras**.
    - Your Jupyter notebook server
        - [Install the Azure Machine Learning SDK (v2)](https://aka.ms/sdk-v2-install).
- Download the training scripts [keras_mnist.py](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/src/keras_mnist.py) and [utils.py](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/src/utils.py).

You can also find a completed [Jupyter Notebook version](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb) of this guide on the GitHub samples page.

[!INCLUDE [gpu quota](includes/machine-learning-gpu-quota-prereq.md)]

## Set up the job

This section sets up the job for training by loading the required Python packages, connecting to a workspace, creating a compute resource to run a command job, and creating an environment to run the job.

### Connect to the workspace

First, you need to connect to your Azure Machine Learning workspace. The [Azure Machine Learning workspace](concept-workspace.md) is the top-level resource for the service. It provides you with a centralized place to work with all the artifacts you create when you use Azure Machine Learning.

Use `DefaultAzureCredential` to access the workspace. This credential can handle most Azure SDK authentication scenarios.

If `DefaultAzureCredential` doesn't work for you, see [`azure-identity` reference documentation](/python/api/azure-identity/azure.identity) or [`Set up authentication`](how-to-setup-authentication.md?tabs=sdk) for more available credentials.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=credential)]

If you prefer to use a browser to sign in and authenticate, uncomment the following code and use it instead.

```python
# Handle to the workspace
# from azure.ai.ml import MLClient

# Authentication package
# from azure.identity import InteractiveBrowserCredential
# credential = InteractiveBrowserCredential()
```

Next, get a handle to the workspace by providing your Subscription ID, Resource Group name, and workspace name. To find these parameters:

1. Look for your workspace name in the upper-right corner of the Azure Machine Learning studio toolbar.
1. Select your workspace name to show your Resource Group and Subscription ID.
1. Copy the values for Resource Group and Subscription ID into the code.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=ml_client)]

The result of running this script is a workspace handle that you use to manage other resources and jobs.

> [!NOTE]
> - Creating `MLClient` won't connect the client to the workspace. The client initialization is lazy and will wait for the first time it needs to make a call. In this article, this happens during compute creation.

### Create a compute resource to run the job

Azure Machine Learning needs a compute resource to run a job. This resource can be single-node or multinode machines with Linux or Windows OS, or a specific compute fabric like Spark.

In the following example script, you create a Linux [`compute cluster`](./how-to-create-attach-compute-cluster.md?tabs=python). For the full list of VM sizes and prices, see the [`Azure Machine Learning pricing`](https://azure.microsoft.com/pricing/details/machine-learning/) page. Since you need a GPU cluster for this example, select the *Standard_NC4as_T4_v3* version and create an Azure Machine Learning compute.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=cpu_compute_target)]

### Create a job environment

To run an Azure Machine Learning job, you need an environment. An Azure Machine Learning [environment](concept-environments.md) encapsulates the dependencies (such as software runtime and libraries) needed to run your machine learning training script on your compute resource. This environment is similar to a Python environment on your local machine.

Azure Machine Learning allows you to either use a curated (or ready-made) environment or create a custom environment using a Docker image or a Conda configuration. In this article, you create a custom Conda environment for your jobs, using a Conda YAML file.

#### Create a custom environment

To create your custom environment, you define your Conda dependencies in a YAML file. First, create a directory for storing the file. In this example, we've named the directory `dependencies`.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=dependencies_folder)]
Then, create the file in the dependencies directory. In this example, the file is named `conda.yml`.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=conda_file)]

The specification contains some common packages, such as numpy and pip, that you use in your job.

> [!NOTE]
> If your environment installs Keras 3 (`keras >= 3.0`), set the `KERAS_BACKEND` environment variable to `tensorflow` before importing Keras. Add `KERAS_BACKEND=tensorflow` to your Conda environment YAML under `variables`, or set it at the top of your training script with `import os; os.environ['KERAS_BACKEND'] = 'tensorflow'` before any Keras import.

Next, use the YAML file to create and register this custom environment in your workspace. The environment is packaged into a Docker container at runtime.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=custom_environment)]

For more information on creating and using environments, see [Create and use software environments in Azure Machine Learning](how-to-use-environments.md).

## Configure and submit your training job

In this section, we begin by introducing the data for training. We'll then cover how to run a training job, using a training script that we've provided. You learn to build the training job by configuring the command for running the training script. Then, you submit the training job to run in Azure Machine Learning.

### Obtain the training data
You use data from the Modified National Institute of Standards and Technology (MNIST) database of handwritten digits. This data is stored in an Azure storage account.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=data_url)]

For more information about the MNIST dataset, see the [MNIST dataset page](https://www.tensorflow.org/datasets/catalog/mnist).

### Prepare the training script

In this article, the training script *keras_mnist.py* is provided. In practice, you should be able to take any custom training script as is and run it with Azure Machine Learning without having to modify your code.

The provided training script does the following steps:
 - Handles the data preprocessing, splitting the data into test and train data.
 - Trains a model by using the data.
 - Returns the output model.

During the pipeline run, you use MLFlow to log the parameters and metrics. To learn how to enable MLFlow tracking, see [Track ML experiments and models with MLflow](how-to-use-mlflow-cli-runs.md).

In the training script `keras_mnist.py`, you create a simple deep neural network (DNN). This DNN has:

- An input layer with 28 * 28 = 784 neurons. Each neuron represents an image pixel.
- Two hidden layers. The first hidden layer has 300 neurons and the second hidden layer has 100 neurons.
- An output layer with 10 neurons. Each neuron represents a targeted label from 0 to 9.

:::image type="content" source="media/how-to-train-tensorflow/neural-network.png" alt-text="Diagram showing a deep neural network with 784 neurons at the input layer, two hidden layers, and 10 neurons at the output layer.":::

### Build the training job

Now that you have all the assets required to run your job, it's time to build it using the Azure Machine Learning Python SDK v2. For this example, we are creating a `command`.

An Azure Machine Learning `command` is a resource that specifies all the details needed to execute your training code in the cloud. These details include the inputs and outputs, type of hardware to use, software to install, and how to run your code. The `command` contains information to execute a single command.


#### Configure the command

You use the general purpose `command` to run the training script and perform your desired tasks. Create a `Command` object to specify the configuration details of your training job.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=job)]

- The inputs for this command include the data location, batch size, number of neurons in the first and second layer, and learning rate. Notice that you pass in the web path directly as an input.

- For the parameter values:
    - provide the compute cluster `gpu_compute_target = "gpu-cluster"` that you created for running this command;
    - provide the custom environment `keras-env` that you created for running the Azure Machine Learning job;
    - configure the command line action itself - in this case, the command is `python keras_mnist.py`. You can access the inputs and outputs in the command via the `${{ ... }}` notation; and
    - configure metadata such as the display name and experiment name. An experiment is a container for all the iterations one does on a certain project. All the jobs submitted under the same experiment name appear next to each other in Azure Machine Learning studio.
 
- In this example, you use the `UserIdentity` to run the command. Using a user identity means that the command uses your identity to run the job and access the data from the blob.

### Submit the job

It's now time to submit the job to run in Azure Machine Learning. This time, you use `create_or_update` on `ml_client.jobs`.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=create_job)]

Once completed, the job registers a model in your workspace (as a result of training) and output a link for viewing the job in Azure Machine Learning studio.

> [!WARNING]
> Azure Machine Learning runs training scripts by copying the entire source directory. If you have sensitive data that you don't want to upload, use a [.ignore file](concept-train-machine-learning-model.md#understand-what-happens-when-you-submit-a-training-job) or don't include it in the source directory.

### What happens during job execution
As the job executes, it goes through the following stages:

- **Preparing**: The process creates a Docker image according to the environment you defined. It uploads the image to the workspace's container registry and caches it for later runs. The process also streams logs to the job history, so you can view them to monitor progress. If you specify a curated environment, the process uses the cached image that backs that curated environment.

- **Scaling**: The cluster attempts to scale up if it requires more nodes to execute the run than are currently available.

- **Running**: The process uploads all scripts in the *src* script folder to the compute target. It mounts or copies data stores. Then, it executes the script. The process streams outputs from *stdout* and the *./logs* folder to the job history. You can use these outputs to monitor the job.

## Tune model hyperparameters

You've trained the model with one set of parameters. Let's now see if you can further improve the accuracy of your model. You can tune and optimize your model's hyperparameters using Azure Machine Learning's [`sweep`](/python/api/azure-ai-ml/azure.ai.ml.sweep) capabilities.

To tune the model's hyperparameters, define the parameter space in which to search during training. You do this by replacing some of the parameters (`batch_size`, `first_layer_neurons`, `second_layer_neurons`, and `learning_rate`) passed to the training job with special inputs from the `azure.ml.sweep` package.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=job_for_sweep)]

Then, you configure sweep on the command job, using some sweep-specific parameters, such as the primary metric to watch and the sampling algorithm to use.

In the following code, random sampling tries different configuration sets of hyperparameters in an attempt to maximize the primary metric, `validation_acc`.

We also define an early termination policy—the `BanditPolicy`. This policy operates by checking the job every two iterations. If the primary metric, `validation_acc`, falls outside the top 10 percent range, Azure Machine Learning terminates the job. This saves the model from continuing to explore hyperparameters that show no promise of helping to reach the target metric.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=sweep_job)]

Now, you can submit this job as before. This time, you are running a sweep job that sweeps over your train job.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=create_sweep_job)]

You can monitor the job by using the studio user interface link that's presented during the job run.

## Find and register the best model

When all the runs finish, find the run that produces the model with the highest accuracy.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=model)]

Then, register this model.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=register_model)]


## Deploy the model as an online endpoint

After you register your model, deploy it as an [online endpoint](concept-endpoints.md)—that is, as a web service in the Azure cloud.

To deploy a machine learning service, you typically need:
- The model assets that you want to deploy. These assets include the model's file and metadata that you already registered in your training job.
- Some code to run as a service. The code executes the model on a given input request (an entry script). This entry script receives data submitted to a deployed web service and passes it to the model. After the model processes the data, the script returns the model's response to the client. The script is specific to your model and must understand the data that the model expects and returns. When you use an MLFlow model, Azure Machine Learning automatically creates this script for you.

For more information about deployment, see [Deploy and score a machine learning model with managed online endpoint using Python SDK v2](how-to-deploy-managed-online-endpoint-sdk-v2.md).

### Create a new online endpoint

As a first step to deploying your model, you need to create your online endpoint. The endpoint name must be unique in the entire Azure region. For this article, you create a unique name using a universally unique identifier (UUID).

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=online_endpoint_name)]

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=endpoint)]

After you create the endpoint, retrieve it as follows:

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=get_endpoint)]

### Deploy the model to the endpoint

After you create the endpoint, deploy the model by using the entry script. An endpoint can have multiple deployments. By using rules, the endpoint can direct traffic to these deployments.

In the following code, you create a single deployment that handles 100% of the incoming traffic. We've specified an arbitrary color name (*tff-blue*) for the deployment. You could also use any other name such as *tff-green* or *tff-red* for the deployment.
The following code deploys the model to the endpoint:

- deploys the best version of the model that you registered earlier;
- scores the model by using the `score.py` file; and
- uses the custom environment (that you created earlier) to perform inferencing.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=blue_deployment)]

> [!NOTE]
> Expect this deployment to take a bit of time to finish.

### Test the deployed model

Now that you deployed the model to the endpoint, you can predict the output of the deployed model by using the `invoke` method on the endpoint. 

To test the endpoint, you need some test data. Let us locally download the test data, which we used in our training script.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=download_test_data)]

Load these files into a test dataset.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=load_test_data)]

Pick 30 random samples from the test set and write them to a JSON file.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=generate_test_json)]

Invoke the endpoint, print the returned predictions, and plot them along with the input images. Use red font color and inverted image (white on black) to highlight the misclassified samples.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=invoke_and_test)]


> [!NOTE]
> Because the model accuracy is high, you might have to run the cell a few times before you see a misclassified sample.

### Clean up resources

If you don't plan to use the endpoint, delete it to stop using the resource. Make sure no other deployments are using the endpoint before you delete it.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-keras/train-hyperparameter-tune-deploy-with-keras.ipynb?name=delete_endpoint)]

> [!NOTE]
> The cleanup process can take some time.


## Next steps

In this article, you trained and registered a Keras model. You also deployed the model to an online endpoint. To learn more about Azure Machine Learning, see the following articles:

- [Track run metrics during training](how-to-log-view-metrics.md)
- [Tune hyperparameters](how-to-tune-hyperparameters.md)
- [Reference architecture for distributed deep learning training in Azure](/azure/architecture/reference-architectures/ai/training-deep-learning)
