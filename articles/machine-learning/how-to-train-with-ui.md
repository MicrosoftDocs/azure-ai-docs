---
title: Create a Training Job with the Job Creation UI
titleSuffix: Azure Machine Learning
description: Learn how to submit a training job in the Azure Machine Learning studio by using the job creation UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.topic: how-to
ms.custom: devplatv2
author: ssalgadodev
ms.author: ssalgado
ms.date: 04/02/2025
ms.reviewer: amipatel
---

# Submit a training job in the Azure Machine Learning studio

There are many ways to create a training job with Azure Machine Learning. You can train models by using the [Azure CLI](how-to-train-model.md), the [REST API](how-to-train-with-rest.md), or you can use the studio UI to directly create a training job.

In this article, you learn how to use your own data and code to train a machine learning model with a guided experience for submitting training jobs in the Azure Machine Learning studio.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/free/machine-learning/search/) before you begin.

* An Azure Machine Learning workspace. To learn how, see [Create workspace resources](quickstart-create-resources.md).

* An understanding of what a training job is in Azure Machine Learning. To learn more, see [how to train models](how-to-train-model.md).

## Get started

1. Sign in to the [Azure Machine Learning studio](https://ml.azure.com), then select your subscription and workspace.

1. Enter the job creation UI from the homepage. Select **+ New** and choose **Training job**.

    :::image type="content" source="media/how-to-train-with-ui/unified-job-submission-home.png" alt-text="Screenshot that shows the Azure Machine Learning studio homepage." lightbox="media/how-to-train-with-ui/unified-job-submission-home.png":::

1. Select your method of training, then choose **Start configuring job** to open the submission form.

    :::image type="content" source="media/how-to-train-with-ui/training-method.png" alt-text="Screenshot that shows the training method options on the Azure Machine Learning studio training form." lightbox="media/how-to-train-with-ui/training-method.png":::

    In the next section, we walk through the form with the steps for running a custom training script (command job).

## Configure basic settings

Configure the basic information about your training job. You can proceed to the next page if you're satisfied with the defaults we chose for you, or make changes based on your desired preference.

:::image type="content" source="media/how-to-train-with-ui/basic-settings.png" alt-text="Screenshot that shows the basic settings form for training jobs." lightbox="media/how-to-train-with-ui/basic-settings.png":::

The following fields are available:

|Field| Description|
|------| ------|
|Job name| The job name is used to uniquely identify your job. It's also used as the display name for your job.|
|Experiment name| This helps organize the job in Azure Machine Learning studio. Each job's run record is organized under the corresponding experiment in the studio's **Experiment** tab. By default, Azure puts the job in the **Default** experiment.|
|Description| Add some text describing your job, if desired.|
|Timeout| Specify the number of hours the entire training job is allowed to run. After this limit is reached, the system cancels the job including any child jobs.|
|Tags| Add tags to help organize your jobs.|

## Upload training script

On the next page, upload your source code. Configure any inputs or outputs required to execute the training job, and specify the command to execute your training script.  

You can use a code file or a folder from your local machine or workspace's default blob storage. Azure shows the files to be uploaded after you make the selection.

|Field| Description|
|------| ------|
|Code| A file or a folder from your local machine or workspace's default blob storage as your training script. Studio shows the files to be uploaded after you make the selection.|
|Inputs| Specify as many inputs as needed of the following types data: integer, number, boolean, string. |
|Command| The command to execute. Command-line arguments can be explicitly written into the command or inferred from other sections, specifically **inputs** using curly braces notation, as discussed in the next section.|

### Code

The command is run from the root directory of the uploaded code folder. After you select your code file or folder, you can see the files to be uploaded. Copy the relative path to the code containing your entry point and paste it into the box labeled **Enter the command to start the job**.

If the code is in the root directory, you can directly refer to it in the command. For instance, `python main.py`.

If the code isn't in the root directory, you should use the relative path. For example, the structure of the [word language model](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/single-step/pytorch/word-language-model) is:

```tree
.
├── job.yml
├── data
└── src
    └── main.py
```

Here, the source code is in the `src` subdirectory. The command would be `python ./src/main.py` (plus other command-line arguments).

:::image type="content" source="media/how-to-train-with-ui/training-script-code.png" alt-text="Screenshot of the files to be uploaded in the training job submission form." lightbox="media/how-to-train-with-ui/training-script-code.png":::

### Inputs

When you use an input in the command, you need to specify the input name. To indicate an input variable, use the form `${{inputs.input_name}}`. For instance, `${{inputs.wiki}}`. You can then refer to it in the command, for instance, `--data ${{inputs.wiki}}`.

:::image type="content" source="media/how-to-train-with-ui/training-script-inputs.png" alt-text="Screenshot that shows the input variables in the training job submission form." lightbox="media/how-to-train-with-ui/training-script-inputs.png":::

## Select compute resources

On the next page, select the compute target on which you'd like your job to run. The job creation UI supports several compute types:

| Compute type | Introduction |
| --- | --- |
| Compute instance | [What is an Azure Machine Learning compute instance?](concept-compute-instance.md) |
| Compute cluster | [What is a compute cluster?](how-to-create-attach-compute-cluster.md#what-is-a-compute-cluster) |
| Attached Kubernetes cluster | [Configure and attach Kubernetes cluster anywhere](how-to-attach-kubernetes-anywhere.md) |

1. Select a compute type.

1. Select an existing compute resource. The dropdown shows the node information and SKU type to help your choice.

1. For a compute cluster or a Kubernetes cluster, you can also specify how many nodes you want for the job in **Instance count**. The default number of instances is *1*.

1. When you're satisfied with your choices, choose **Next**.

If you're using Azure Machine Learning for the first time, you see an empty list and a link to create a new compute. For more information on creating the various types, see:

| Compute type | How to |
| --- | --- |
| Compute instance | [Create an Azure Machine Learning compute instance](how-to-create-compute-instance.md) |
| Compute cluster | [Create an Azure Machine Learning compute cluster](how-to-create-attach-compute-cluster.md) |
| Attached Kubernetes cluster | [Attach an Azure Arc-enabled Kubernetes cluster](how-to-attach-kubernetes-anywhere.md) |

## Specify the necessary environment

After selecting a compute target, you need to specify the runtime environment for your job. The job creation UI supports three types of environment:

* Curated environments
* Custom environments
* Container registry image

### Curated environments

Curated environments are Azure-defined collections of Python packages used in common ML workloads. Curated environments are available in your workspace by default. These environments are backed by cached Docker images, which reduce the job preparation overhead. The cards displayed in the **Curated environments** page show details of each environment. To learn more, see [Azure Machine Learning Curated Environments](resource-curated-environments.md).

:::image type="content" source="media/how-to-train-with-ui/curated-environments.png" alt-text="Screenshot of the curated environments selector page showing various environment cards." lightbox="media/how-to-train-with-ui/curated-environments.png":::

### Custom environments

Custom environments are environments that you specify. You can specify an environment or reuse an environment that you already created. To learn more, see [Manage software environments in Azure Machine Learning studio](how-to-manage-environments-in-studio.md).

### Container registry image

If you don't want to use the Azure Machine Learning curated environments or specify your own custom environment, you can use a docker image from a public container registry such as [Docker Hub](https://hub.docker.com).

## Review and create

After you configure the job, choose **Next** to go to the **Review** page. To modify a setting, choose the pencil icon and make the change.

:::image type="content" source="media/how-to-train-with-ui/review.png" alt-text="Screenshot that shows the review pane to validate your selections before submission." lightbox="media/how-to-train-with-ui/review.png":::

To launch the job, choose **Submit training job**. After the job is created, Azure shows you the job details page, where you can monitor and manage your training job.

[!INCLUDE [Email Notification Include](includes/machine-learning-email-notifications.md)]

## Related content

* [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
* [Train models with Azure Machine Learning CLI, SDK, and REST API](how-to-train-model.md)
