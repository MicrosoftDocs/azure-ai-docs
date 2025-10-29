---
title: "Tutorial: Create workspace resources"
titleSuffix: Azure Machine Learning
description: Create an Azure Machine Learning workspace and cloud resources that can be used to train machine learning models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.reviewer: sgilley
ms.date: 08/08/2025
adobe-target: true
ms.custom: mode-other
#Customer intent: As a data scientist, I want to create a workspace so that I can start to use Azure Machine Learning.
---

# Tutorial: Create resources you need to get started

In this tutorial, you create the resources you need to start working with Azure Machine Learning.

> [!div class="checklist"]
>* A *workspace*. To use Azure Machine Learning, you need a workspace. The workspace is the central place to view and manage all the artifacts and resources you create.
>* A *compute instance*. A compute instance is a preconfigured cloud-computing resource that you can use to train, automate, manage, and track machine learning models. A compute instance is the quickest way to start using the Azure Machine Learning SDKs and CLIs. You use it to run Jupyter notebooks and Python scripts in the rest of the tutorials.
>

In this tutorial, you create your resources in [Azure Machine Learning studio](https://ml.azure.com).

You can also create a workspace using the [Azure portal or SDK](how-to-manage-workspace.md), [the CLI](how-to-manage-workspace-cli.md), [Azure PowerShell](how-to-manage-workspace-powershell.md), or [the Visual Studio Code extension](how-to-setup-vs-code.md).

For other ways to create a compute instance, see [Create a compute instance](how-to-create-compute-instance.md).

This video shows you how to create a workspace and compute instance in Azure Machine Learning studio. The steps are also described in the sections below.
> [!VIDEO https://learn-video.azurefd.net/vod/player?id=9c6141c9-07f7-4661-ad77-6129297ddc0c]

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Create the workspace

The workspace is the top-level resource for your machine learning activities, providing a centralized place to view and manage the artifacts you create when you use Azure Machine Learning.

If you already have a workspace, skip this section and continue to [Create a compute instance](#create-a-compute-instance).

If you don't yet have a workspace, create one now:

1. Sign in to [Azure Machine Learning studio](https://ml.azure.com).
1. Select **Create workspace**.
1. Provide the following information to configure your new workspace:

   Field|Description 
   ---|---
    Workspace name | Enter a unique name that identifies your workspace. Names must be unique within the resource group. Use a name that's easy to recall and differentiate from workspaces created by others. The workspace name is case-insensitive.
    Friendly name | This name isn't restricted by Azure naming rules. You can use spaces and special characters in this name.
    Hub | A hub lets you group related workspaces and share resources. If you have access to a hub, select it here. If you don't have access to a hub, leave this blank.

1. If you didn't select a hub, provide the advanced settings. If you selected a hub, these values are taken from the hub.

    Field|Description
    ---|---
    Subscription | Select the Azure subscription that you want to use.
    Resource group | Use an existing resource group in your subscription or enter a name to create a new one. A resource group holds related resources for an Azure solution. You need the Contributor or Owner role to use an existing resource group. For more information about access, see [Manage access to an Azure Machine Learning workspace](how-to-assign-roles.md).
    Region | Select the Azure region closest to your users and data to create your workspace.

1. Select **Create** to create the workspace.

> [!NOTE]
> This creates a workspace along with all required resources. If you'd like more customization, use the [Azure portal](https://ms.portal.azure.com/#create/Microsoft.MachineLearningServices) instead. See [Create a workspace](how-to-manage-workspace.md) for more information.

## Create a compute instance

You use the *compute instance* to run Jupyter notebooks and Python scripts in the rest of the tutorials. If you don't yet have a compute instance, create one now:

1. Select your workspace.
1. On the top right, select **New**.
1. Select **Compute instance** in the list.

    :::image type="content" source="media/quickstart-create-resources/create-compute.png" alt-text="Screenshot shows create compute in the New list.":::

1. Supply a name.
1. Keep the default values for the rest of the page unless your organization's policy requires different settings.
1. Select **Review + Create**.
1. Select **Create**.

## Quick tour of the studio

The studio is your web portal for Azure Machine Learning. It combines no-code and code-first experiences for an inclusive data science platform.

Review the parts of the studio on the left-hand navigation bar:

* The **Authoring** section of the studio contains multiple ways to get started creating machine learning models. You can:

    * **Notebooks** lets you create Jupyter notebooks, copy sample notebooks, and run notebooks and Python scripts.
    * **Automated ML** guides you through creating a machine learning model without writing code.
    * **Designer** provides a drag-and-drop way to build models using prebuilt components.

* The **Assets** section helps you track the assets you create as you run jobs. In a new workspace, these sections are empty.

* The **Manage** section lets you create and manage compute and external services linked to your workspace. You can also create and manage a **Data labeling** project here.

:::image type="content" source="media/quickstart-create-resources/overview.png" alt-text="Screenshot of Azure Machine Learning studio." lightbox="media/quickstart-create-resources/overview.png":::

## Learn from sample notebooks

Use the sample notebooks available in the studio to learn how to train and deploy models. They're referenced in many of the other articles and tutorials.

1. On the left navigation, select **Notebooks**.
1. At the top, select **Samples**.

:::image type="content" source="media/quickstart-create-resources/samples.png" alt-text="Screenshot shows sample notebooks.":::

* Use notebooks in the **SDK v2** folder for examples that use the current SDK (v2).
* These notebooks are read-only and are updated periodically.
* When you open a notebook, select **Clone this notebook** at the top to add a copy and any associated files to your **Files**. A new folder is created for you in the **Files** section.

## Create a new notebook

When you clone a notebook from **Samples**, a copy is added to your files and you can start running or modifying it. Many of the tutorials mirror these sample notebooks.

You can also create a new, empty notebook and then copy and paste code from a tutorial into it. To do so:

1. Still in the **Notebooks** section, select **Files** to go back to your files.
1. Select **+** to add files.
1. Select **Create new file**.
    
    :::image type="content" source="media/quickstart-create-resources/create-new-file.png" alt-text="Screenshot shows how to create a new file.":::
    

## Clean up resources

If you plan to continue to other tutorials now, skip to [Next step](#next-step).

### Stop compute instance

If you're not going to use it now, stop the compute instance:

1. In the studio, on the left menu, select **Compute**.
1. On the top tabs, select **Compute instances**.
1. Select the compute instance in the list.
1. On the top toolbar, select **Stop**.

### Delete all resources

[!INCLUDE [aml-delete-resource-group](includes/aml-delete-resource-group.md)]

## Next step

You now have an Azure Machine Learning workspace that contains a compute instance for your development environment.

Continue to learn how to use the compute instance to run notebooks and scripts in Azure Machine Learning.

> [!div class="nextstepaction"]
> [Quickstart: Get to know Azure Machine Learning](tutorial-azure-ml-in-a-day.md) 

Use your compute instance with the following tutorials to train and deploy a model.

|Tutorial  |Description  |
|---------|---------|
| [Upload, access, and explore your data in Azure Machine Learning](tutorial-explore-data.md) | Store large data in the cloud and retrieve it from notebooks and scripts. |
| [Model development on a cloud workstation](tutorial-cloud-workstation.md) | Start prototyping and developing machine learning models. |
| [Train a model in Azure Machine Learning](tutorial-train-model.md) | Dive into the details of training a model. |
| [Deploy a model as an online endpoint](tutorial-deploy-model.md) | Dive into the details of deploying a model. |
| [Create production machine learning pipelines](tutorial-pipeline-python-sdk.md) | Split a complete machine learning task into a multistep workflow. |

Want to jump right in? [Browse code samples](/samples/browse/?expanded=azure&products=azure-machine-learning).
