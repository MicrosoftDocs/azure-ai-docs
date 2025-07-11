---
title: Train and deploy a TensorFlow model (SDK v2)
titleSuffix: Azure Machine Learning
description: Learn how Azure Machine Learning SDK (v2) enables you to scale out a TensorFlow training job using elastic cloud compute resources.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.author: scottpolly
author: s-polly
ms.reviewer: balapv
ms.date: 04/03/2024
ms.topic: how-to
ms.custom: sdkv2, update-code
#Customer intent: As a TensorFlow developer, I need to combine open-source with a cloud platform to train, evaluate, and deploy my deep learning models at scale.
---

# Train TensorFlow models at scale with Azure Machine Learning

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

In this article, learn how to run your [TensorFlow](https://www.tensorflow.org/overview) training scripts at scale using Azure Machine Learning Python SDK v2.

The example code in this article train a TensorFlow model to classify handwritten digits, using a deep neural network (DNN); register the model; and deploy it to an online endpoint.

Whether you're developing a TensorFlow model from the ground-up or you're bringing an existing model into the cloud, you can use Azure Machine Learning to scale out open-source training jobs using elastic cloud compute resources. You can build, deploy, version, and monitor production-grade models with Azure Machine Learning.

## Prerequisites

To benefit from this article, you need to:

- Access an Azure subscription. If you don't have one already, [create a free account](https://azure.microsoft.com/free/).
- Run the code in this article using either an Azure Machine Learning compute instance or your own Jupyter notebook.
    - Azure Machine Learning compute instance—no downloads or installation necessary
        - Complete the [Create resources to get started](quickstart-create-resources.md) tutorial to create a dedicated notebook server preloaded with the SDK and the sample repository.
        - In the samples deep learning folder on the notebook server, find a completed and expanded notebook by navigating to this directory: **v2  > sdk > python > jobs > single-step > tensorflow > train-hyperparameter-tune-deploy-with-tensorflow**.
    - Your Jupyter notebook server
        - [Install the Azure Machine Learning SDK (v2)](https://aka.ms/sdk-v2-install).
- Download the following files:
    - training script [tf_mnist.py](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/src/tf_mnist.py) 
    - scoring script [score.py](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/src/score.py)
    - sample request file [sample-request.json](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/request/sample-request.json)

You can also find a completed [Jupyter Notebook version](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb) of this guide on the GitHub samples page.


[!INCLUDE [gpu quota](includes/machine-learning-gpu-quota-prereq.md)]

## Set up the job

This section sets up the job for training by loading the required Python packages, connecting to a workspace, creating a compute resource to run a command job, and creating an environment to run the job.

### Connect to the workspace

First, you need to connect to your Azure Machine Learning workspace. The [Azure Machine Learning workspace](concept-workspace.md) is the top-level resource for the service. It provides you with a centralized place to work with all the artifacts you create when you use Azure Machine Learning.

We're using `DefaultAzureCredential` to get access to the workspace. This credential should be capable of handling most Azure SDK authentication scenarios.

If `DefaultAzureCredential` doesn't work for you, see [`azure-identity reference documentation`](/python/api/azure-identity/azure.identity) or [`Set up authentication`](how-to-setup-authentication.md?tabs=sdk) for more available credentials.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=credential)]

If you prefer to use a browser to sign in and authenticate, you should uncomment the following code and use it instead.

```python
# Handle to the workspace
# from azure.ai.ml import MLClient

# Authentication package
# from azure.identity import InteractiveBrowserCredential
# credential = InteractiveBrowserCredential()
```

Next, get a handle to the workspace by providing your Subscription ID, Resource Group name, and workspace name. To find these parameters:

1. Look for your workspace name in the upper-right corner of the Azure Machine Learning studio toolbar.
2. Select your workspace name to show your Resource Group and Subscription ID.
3. Copy the values for Resource Group and Subscription ID into the code.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=ml_client)]

The result of running this script is a workspace handle that you use to manage other resources and jobs.

> [!NOTE]
> - Creating `MLClient` will not connect the client to the workspace. The client initialization is lazy and will wait for the first time it needs to make a call. In this article, this will happen during compute creation.

### Create a compute resource

Azure Machine Learning needs a compute resource to run a job. This resource can be single or multi-node machines with Linux or Windows OS, or a specific compute fabric like Spark.

In the following example script, we provision a Linux [`compute cluster`](./how-to-create-attach-compute-cluster.md?tabs=python). You can see the [`Azure Machine Learning pricing`](https://azure.microsoft.com/pricing/details/machine-learning/) page for the full list of VM sizes and prices. Since we need a GPU cluster for this example, let's pick a *STANDARD_NC6* model and create an Azure Machine Learning compute.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=cpu_compute_target)]

### Create a job environment

To run an Azure Machine Learning job, you need an environment. An Azure Machine Learning [environment](concept-environments.md) encapsulates the dependencies (such as software runtime and libraries) needed to run your machine learning training script on your compute resource. This environment is similar to a Python environment on your local machine.

Azure Machine Learning allows you to either use a curated (or ready-made) environment—useful for common training and inference scenarios—or create a custom environment using a Docker image or a Conda configuration. 

In this article, you reuse the curated Azure Machine Learning environment `AzureML-tensorflow-2.7-ubuntu20.04-py38-cuda11-gpu`. You use the latest version of this environment using the `@latest` directive.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=curated_env_name)]

## Configure and submit your training job

In this section, we begin by introducing the data for training. We then cover how to run a training job, using a training script that we've provided. You learn to build the training job by configuring the command for running the training script. Then, you submit the training job to run in Azure Machine Learning.

### Obtain the training data
You'll use data from the Modified National Institute of Standards and Technology (MNIST) database of handwritten digits. This data is sourced from Yan LeCun's website and stored in an Azure storage account.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=data_url)]

For more information about the MNIST dataset, visit [Yan LeCun's website](http://yann.lecun.com/exdb/mnist/).

### Prepare the training script

In this article, we've provided the training script *tf_mnist.py*. In practice, you should be able to take any custom training script as is and run it with Azure Machine Learning without having to modify your code.

The provided training script does the following:
- handles the data preprocessing, splitting the data into test and train data;
- trains a model, using the data; and 
- returns the output model.

During the pipeline run, you use MLFlow to log the parameters and metrics. To learn how to enable MLFlow tracking, see [Track ML experiments and models with MLflow](how-to-use-mlflow-cli-runs.md).

In the training script `tf_mnist.py`, we create a simple deep neural network (DNN). This DNN has:

- An input layer with 28 * 28 = 784 neurons. Each neuron represents an image pixel.
- Two hidden layers. The first hidden layer has 300 neurons and the second hidden layer has 100 neurons.
- An output layer with 10 neurons. Each neuron represents a targeted label from 0 to 9.

:::image type="content" source="media/how-to-train-tensorflow/neural-network.png" alt-text="Diagram showing a deep neural network with 784 neurons at the input layer, two hidden layers, and 10 neurons at the output layer.":::

### Build the training job

Now that you have all the assets required to run your job, it's time to build it using the Azure Machine Learning Python SDK v2. For this example, we are creating a `command`.

An Azure Machine Learning `command` is a resource that specifies all the details needed to execute your training code in the cloud. These details include the inputs and outputs, type of hardware to use, software to install, and how to run your code. The `command` contains information to execute a single command.


#### Configure the command

You use the general purpose `command` to run the training script and perform your desired tasks. Create a `Command` object to specify the configuration details of your training job.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=job)]

- The inputs for this command include the data location, batch size, number of neurons in the first and second layer, and learning rate. Notice that we've passed in the web path directly as an input.

- For the parameter values:
    - provide the compute cluster `gpu_compute_target = "gpu-cluster"` that you created for running this command;
    - provide the curated environment `curated_env_name` that you declared earlier;
    - configure the command line action itself—in this case, the command is `python tf_mnist.py`. You can access the inputs and outputs in the command via the `${{ ... }}` notation; and
    - configure metadata such as the display name and experiment name; where an experiment is a container for all the iterations one does on a certain project. All the jobs submitted under the same experiment name would be listed next to each other in Azure Machine Learning studio.
 
- In this example, you'll use the `UserIdentity` to run the command. Using a user identity means that the command will use your identity to run the job and access the data from the blob.

### Submit the job

It's now time to submit the job to run in Azure Machine Learning. This time, you'll use `create_or_update` on `ml_client.jobs`.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=create_job)]

Once completed, the job will register a model in your workspace (as a result of training) and output a link for viewing the job in Azure Machine Learning studio.

> [!WARNING]
> Azure Machine Learning runs training scripts by copying the entire source directory. If you have sensitive data that you don't want to upload, use a [.ignore file](concept-train-machine-learning-model.md#understand-what-happens-when-you-submit-a-training-job) or don't include it in the source directory.

### What happens during job execution
As the job is executed, it goes through the following stages:

- **Preparing**: A docker image is created according to the environment defined. The image is uploaded to the workspace's container registry and cached for later runs. Logs are also streamed to the job history and can be viewed to monitor progress. If a curated environment is specified, the cached image backing that curated environment will be used.

- **Scaling**: The cluster attempts to scale up if it requires more nodes to execute the run than are currently available.

- **Running**: All scripts in the script folder *src* are uploaded to the compute target, data stores are mounted or copied, and the script is executed. Outputs from *stdout* and the *./logs* folder are streamed to the job history and can be used to monitor the job.

## Tune model hyperparameters

Now that you've seen how to do a TensorFlow training run using the SDK, let's see if you can further improve the accuracy of your model. You can tune and optimize your model's hyperparameters using Azure Machine Learning's [`sweep`](/python/api/azure-ai-ml/azure.ai.ml.sweep) capabilities.

To tune the model's hyperparameters, define the parameter space in which to search during training. You'll do this by replacing some of the parameters (`batch_size`, `first_layer_neurons`, `second_layer_neurons`, and `learning_rate`) passed to the training job with special inputs from the `azure.ml.sweep` package.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=job_for_sweep)]

Then, you configure sweep on the command job, using some sweep-specific parameters, such as the primary metric to watch and the sampling algorithm to use.

In the following code, we use random sampling to try different configuration sets of hyperparameters in an attempt to maximize our primary metric, `validation_acc`.

We also define an early termination policy—the `BanditPolicy`. This policy operates by checking the job every two iterations. If the primary metric, `validation_acc`, falls outside the top 10 percent range, Azure Machine Learning terminates the job. This saves the model from continuing to explore hyperparameters that show no promise of helping to reach the target metric.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=sweep_job)]

Now, you can submit this job as before. This time, you'll be running a sweep job that sweeps over your train job.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=create_sweep_job)]

You can monitor the job by using the studio user interface link that is presented during the job run.

## Find and register the best model

Once all the runs complete, you can find the run that produced the model with the highest accuracy.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=model)]

You can then register this model.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=register_model)]


## Deploy the model as an online endpoint

After you register your model, you can deploy it as an [online endpoint](concept-endpoints.md)—that is, as a web service in the Azure cloud.

To deploy a machine learning service, you typically need:
- The model assets that you want to deploy. These assets include the model's file and metadata that you already registered in your training job.
- Some code to run as a service. The code executes the model on a given input request (an entry script). This entry script receives data submitted to a deployed web service and passes it to the model. After the model processes the data, the script returns the model's response to the client. The script is specific to your model and must understand the data that the model expects and returns. When you use an MLFlow model, Azure Machine Learning automatically creates this script for you.

For more information about deployment, see [Deploy and score a machine learning model with managed online endpoint using Python SDK v2](how-to-deploy-managed-online-endpoint-sdk-v2.md).

### Create a new online endpoint

As a first step to deploying your model, you need to create your online endpoint. The endpoint name must be unique in the entire Azure region. For this article, you create a unique name using a universally unique identifier (UUID).

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=online_endpoint_name)]

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=endpoint)]

Once you create the endpoint, you can retrieve it as follows:

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=get_endpoint)]

### Deploy the model to the endpoint

After you've created the endpoint, you can deploy the model with the entry script. An endpoint can have multiple deployments. Using rules, the endpoint can then direct traffic to these deployments.

In the following code, you create a single deployment that handles 100% of the incoming traffic. We use an arbitrary color name (*tff-blue*) for the deployment. You could also use any other name such as *tff-green* or *tff-red* for the deployment.
The code to deploy the model to the endpoint does the following:

- deploys the best version of the model that you registered earlier;
- scores the model, using the `score.py` file; and
- uses the same curated environment (that you declared earlier) to perform inferencing.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=blue_deployment)]

> [!NOTE]
> Expect this deployment to take a bit of time to finish.

### Test the deployment with a sample query

After you deploy the model to the endpoint, you can predict the output of the deployed model, using the `invoke` method on the endpoint. To run the inference, use the sample request file `sample-request.json` from the *request* folder.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=invoke)]

You can then print the returned predictions and plot them along with the input images. Use red font color and inverted image (white on black) to highlight the misclassified samples.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=test_invoke)]

> [!NOTE]
> Because the model accuracy is high, you might have to run the cell a few times before seeing a misclassified sample.

### Clean up resources

If you won't be using the endpoint, delete it to stop using the resource. Make sure no other deployments are using the endpoint before you delete it.

[!notebook-python[](~/azureml-examples-main/sdk/python/jobs/single-step/tensorflow/train-hyperparameter-tune-deploy-with-tensorflow/train-hyperparameter-tune-deploy-with-tensorflow.ipynb?name=delete_endpoint)]

> [!NOTE]
> Expect this cleanup to take a bit of time to finish.


## Next steps

In this article, you trained and registered a TensorFlow model. You also deployed the model to an online endpoint. See these other articles to learn more about Azure Machine Learning.

- [Track run metrics during training](how-to-log-view-metrics.md)
- [Tune hyperparameters](how-to-tune-hyperparameters.md)
- [Reference architecture for distributed deep learning training in Azure](/azure/architecture/reference-architectures/ai/training-deep-learning)
