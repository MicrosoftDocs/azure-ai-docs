---
title: "Tutorial: Model Development on a Cloud Workstation"
titleSuffix: Azure Machine Learning
description: Learn how to get started with prototyping and developing machine learning models on an Azure Machine Learning cloud workstation. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.reviewer: lebaro
ms.date: 10/16/2025
ms.custom:
  - devx-track-python
  - sfi-image-nochange
#Customer intent: As a data scientist, I want to know how to prototype and develop machine learning models on a cloud workstation.
---

# Tutorial: model development on a cloud workstation

This article describes how to develop a training script by using a notebook on an Azure Machine Learning cloud workstation. The tutorial covers the basic steps that you need to get started:

> [!div class="checklist"]
> * Set up and configure the cloud workstation. Your cloud workstation is powered by an Azure Machine Learning compute instance, which is pre-configured with environments to support your model development needs.
> * Use cloud-based development environments.
> * Use MLflow to track your model metrics.

## Prerequisites

[!INCLUDE [workspace](includes/prereq-workspace.md)]

## Create or start compute

You can create compute resources in the **Compute** section in your workspace. A compute instance is a cloud-based workstation that's fully managed by Azure Machine Learning. This tutorial series uses a compute instance. You can also use it to run your own code, and to develop and test models.

1. Sign in to [Azure Machine Learning studio](https://ml.azure.com).
1. Select your workspace, if it isn't already open.
1. In the left pane, select **Compute**.
1. If you don't have a compute instance, you see **New** in the middle of the page. Select **New** and fill out the form. You can use all the defaults.
1. If you have a compute instance, select it from the list. If it's stopped, select **Start**.

## Open Visual Studio Code (VS Code)

After you have a running compute instance, you can access it in various ways. This tutorial describes how to use the compute instance from Visual Studio Code. Visual Studio Code provides a full integrated development environment (IDE) for creating compute instances.

In the compute instance list, select the **VS Code (Web)** or **VS Code (Desktop)** link for the compute instance you want to use. If you choose **VS Code (Desktop)**, you might see a message asking if you want to open the application.

:::image type="content" source="media/tutorial-cloud-workstation/launch-vs-code.png" alt-text="Screenshot that shows links for starting Visual Studio Code (Web or Desktop)." lightbox="media/tutorial-cloud-workstation/launch-vs-code.png":::

This Visual Studio Code instance is attached to your compute instance and your workspace file system. Even if you open it on your desktop, the files you see are files in your workspace.

## Set up a new environment for prototyping  

In order for your script to run, you need to be working in an environment that's configured with the dependencies and libraries the code expects. This section helps you create an environment that's tailored to your code. To create the new Jupyter kernel your notebook connects to, you use a YAML file that defines the dependencies.

* **Upload a file.**

    Files that you upload are stored in an Azure file share, and these files are mounted to each compute instance and shared within the workspace.

    1. Go to [azureml-examples/tutorials/get-started-notebooks/workstation_env.yml](https://github.com/Azure/azureml-examples/blob/main/tutorials/get-started-notebooks/workstation_env.yml).
    1. Download the Conda environment file *workstation_env.yml* to your computer by selecting the ellipsis button (**...**) in the top-right corner of the page and then selecting **Download**.
    1. Drag the file from your computer to the Visual Studio Code window. The file is uploaded to your workspace.
    1. Move the file into your username folder.

        :::image type="content" source="media/tutorial-cloud-workstation/upload-file.png" alt-text="Screenshot that shows the workstation_env.yml file in the username folder.":::

    1. Select the file to preview it. Review the dependencies that it specifies. You should see something like this:

    ::: code language="yml" source="~/azureml-examples-main/tutorials/get-started-notebooks/workstation_env.yml" :::

* **Create a kernel.**

    Now use the terminal to create a new Jupyter kernel that's based on the *workstation_env.yml* file.

    1. In the menu at the top of Visual Studio Code, select **Terminal > New Terminal**.

    :::image type="content" source="media/tutorial-cloud-workstation/open-terminal.png" alt-text="Screenshot of open terminal tool in notebook toolbar.":::

    1. View your current Conda environments. The active environment is marked with an asterisk (*).

        ```bash
        conda env list
        ```

    1. Use `cd` to navigate to the folder where you uploaded the *workstation_env.yml* file. For example, if you uploaded it to your user folder, use this command:

        ```bash
        cd Users/myusername
        ```

    1. Make sure workstation_env.yml is in the folder.

        ```bash
        ls
        ```

    1. Create the environment based on the Conda file provided. It takes a few minutes to build the environment.

        ```bash
        conda env create -f workstation_env.yml
        ```

    1. Activate the new environment.

        ```bash
        conda activate workstation_env
        ```

        > [!NOTE]
        > If you see CommandNotFoundError, follow instructions to run `conda init bash`, close the terminal, and then open a new one. Then try the `conda activate workstation_env` command again.

    1. Verify that the correct environment is active, again looking for the environment marked with a *.

        ```bash
        conda env list
        ```

    1. Create a new Jupyter kernel that's based on your active environment.

        ```bash
        python -m ipykernel install --user --name workstation_env --display-name "Tutorial Workstation Env" 
        ```

    1. Close the terminal window.

You now have a new kernel. Next, you'll open a notebook and use this kernel.

## Create a notebook

1. In the menu at the top of Visual Studio Code, select **File > New File**.
1. Name your new file **develop-tutorial.ipynb** (or use another name). Be sure to use the **.ipynb** extension.

## Set the kernel

1. In the top-right corner of the new file, select **Select Kernel**.
1. Select **Azure ML compute instance (computeinstance-name)**.
1. Select the kernel you created: **Tutorial Workstation Env**. If you don't see the kernel, select the refresh button above the list.

## Develop a training script

In this section, you develop a Python training script that predicts credit card default payments by using the prepared test and training datasets from the [UCI dataset](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients).

This code uses `sklearn` for training and MLflow for logging metrics.

1. Start with code that imports the packages and libraries that you'll use in the training script.

    [!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=import)]

1. Next, load and process the data for the experiment. In this tutorial, you read the data from a file on the internet.

    [!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=load)]

1. Prepare the data for training.

    [!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=extract)]

1. Add code to start autologging with MLflow so that you can track the metrics and results. With the iterative nature of model development, MLflow helps you log model parameters and results. Refer to different runs to compare and understand how your model performs. The logs also provide context for when you're ready to move from the development phase to the training phase of your workflows within Azure Machine Learning.

    [!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=mlflow)]

1. Train a model.

    [!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=gbt)]

    > [!NOTE]
    > You can ignore the MLflow warnings. The results you need will still be tracked.
1. Select **Run All** above the code. 

## Iterate 

Now that you have model results, change something and run the model again. For example, try a different classification technique:

[!notebook-python[] (~/azureml-examples-main/tutorials/get-started-notebooks/cloud-workstation.ipynb?name=ada)]

> [!NOTE]
> You can ignore the MLflow warnings. The results you need will still be tracked.

Select **Run All** to run the model.

## Examine the results

Now that you've tried two different models, use the results tracked by MLFfow to decide which model is better. You can reference metrics like accuracy, or other indicators that matter the most for your scenarios. You can review these results in more detail by looking at the jobs created by MLflow.

1. Return to your workspace in the [Azure Machine Learning studio](https://ml.azure.com).
1. In the left pane, select **Jobs**.

    :::image type="content" source="media/tutorial-cloud-workstation/jobs.png" alt-text="Screenshot that shows the Jobs item in the left pane.":::

1. Select **Develop on cloud tutorial**.
1. There are two jobs shown, one for each of the models you tried. The names are autogenerated. If you want to rename the job, hover over the name and select the pencil button next to it. 
1. Select the link for the first job. The name appears at the top of the page. You can also rename it here by using the pencil button.
1. The page shows job details, like properties, outputs, tags, and parameters. Under **Tags**, you see the **estimator_name**, which describes the type of model.
1. Select the **Metrics** tab to view the metrics that were logged by MLflow. (Your results will be different because you have a different training set.)

    :::image type="content" source="media/tutorial-cloud-workstation/metrics.png" alt-text="Screenshot that shows metrics for a job." lightbox="media/tutorial-cloud-workstation/metrics.png":::

1. Select the **Images** tab to view the images generated by MLflow. 

    :::image type="content" source="media/tutorial-cloud-workstation/images.png" alt-text="Screenshot that shows images for a job.":::

1. Go back and review the metrics and images for the other model.

## Create a Python script

You'll now create a Python script from your notebook for model training.

1. In Visual Studio Code, right-click the notebook file name and select **Import Notebook to Script**.
1. Select **File > Save** to save the new script file. Call it **train.py**.
1. Look through the file and delete code that you don't want in the training script. For example, keep the code for the model you want to use, and delete code for the model you don't want to use.
    * Be sure you keep the code that starts autologging (`mlflow.sklearn.autolog()`).
    * When you run the Python script interactively (as you're doing here), you can keep the line that defines the experiment name (`mlflow.set_experiment("Develop on cloud tutorial")`). Or you can give it a different name to see it as a different entry in the **Jobs** section. But when you prepare the script for a training job, that line doesn't apply and should be omitted: the job definition includes the experiment name.
    * When you train a single model, the lines for starting and ending a run (`mlflow.start_run()` and `mlflow.end_run()`) aren't necessary (they have no effect), but you can leave them in.

1. When you're finished with your edits, save the file.

You now have a Python script to use for training your preferred model.

## Run the Python script

For now, you're running this code on your compute instance, which is your Azure Machine Learning development environment. [Tutorial: Train a model](tutorial-train-model.md) shows how to run a training script in a more scalable way on more powerful compute resources. 

1. Select the environment you created earlier in this tutorial as your Python version (workstations_env). In the lower-right corner of the notebook, you'll see the environment name. Select it, and then select the environment at the top of Visual Studio Code.

    :::image type="content" source="media/tutorial-cloud-workstation/select-python.png" alt-text="Screenshot that shows selecting the new environment." lightbox="media/tutorial-cloud-workstation/select-python.png":::

1. Run the Python script by selecting the **Run All** button above the code.

    :::image type="content" source="media/tutorial-cloud-workstation/run-python.png" alt-text="Screenshot that shows the Run button." lightbox="media/tutorial-cloud-workstation/run-python.png":::

> [!NOTE]
> You can ignore the MLflow warnings. You'll still get all the metrics and images from autologging.

## Examine the script results

Go back to **Jobs** in your workspace in Azure Machine Learning studio to see the results of your training script. Keep in mind that the training data changes with each split, so the results differ between runs.

## Clean up resources

If you plan to continue on to other tutorials, skip to [Next steps](#next-steps).

### Stop the compute instance

If you're not going to use it now, stop the compute instance:

1. In the studio, in the left pane, select **Compute**.
1. At the top of the page, select **Compute instances**.
1. In the list, select the compute instance.
1. At the top of the page, select **Stop**.

### Delete all resources

[!INCLUDE [aml-delete-resource-group](includes/aml-delete-resource-group.md)]

## Next steps

See these resources to learn more:

* [Artifacts and models in MLflow](concept-mlflow-models.md)
* [Using Git with Azure Machine Learning](concept-train-model-git-integration.md)
* [Running Jupyter notebooks in your workspace](how-to-run-jupyter-notebooks.md)
* [Working with a compute instance terminal in your workspace](how-to-access-terminal.md)
* [Manage notebook and terminal sessions](how-to-manage-compute-sessions.md)

This tutorial shows the early steps of creating a model, prototyping on the same machine where the code resides. For your production training, learn how to use that training script on more powerful remote compute resources:

> [!div class="nextstepaction"]
> [Train a model](tutorial-train-model.md)
>