---
title: Create and run component-based ML pipelines (UI)
titleSuffix: Azure Machine Learning
description: Learn how to create and run machine learning pipelines using the Azure Machine Learning studio and components.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.author: lagayhar
author: lgayhardt
ms.reviewer: keli19
ms.date: 01/27/2026
ms.topic: how-to
ms.custom: devplatv2, designer
ai-usage: ai-assisted
#customer intent: As a Machine Learning data scientist, I want to learn how to use Azure Machine Learning studio to create and run pipelines so that I can do ML experiments and reuse components.
---

# Create and run machine learning pipelines by using components in Azure Machine Learning studio

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

In this article, you learn how to create and run [machine learning pipelines](concept-ml-pipelines.md) by using the Azure Machine Learning studio and [components](concept-component.md). You can create pipelines without using components, but components offer better flexibility and reuse. Azure Machine Learning Pipelines can be defined in YAML and [run from the Azure CLI](how-to-create-component-pipelines-cli.md), [authored in Python](how-to-create-component-pipeline-python.md), or composed in Azure Machine Learning studio Designer with a drag-and-drop UI. This article focuses on the Azure Machine Learning studio Designer UI.

## Prerequisites

- If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An Azure Machine Learning workspace. [Create workspace resources](quickstart-create-resources.md).

- [Install and set up the Azure CLI extension for Machine Learning](how-to-configure-cli.md).

- Clone the examples repository:

  ```azurecli-interactive
  git clone https://github.com/Azure/azureml-examples --depth 1
  cd azureml-examples/cli/jobs/pipelines-with-components/
  ```

> [!NOTE]
> Designer supports two types of components, classic prebuilt components（v1） and custom components (v2). These two types of components are NOT compatible.
>
> Classic prebuilt components provide prebuilt components mainly for data processing and traditional machine learning tasks like regression and classification. Classic prebuilt components continue to be supported but won't have any new components added. Also, deployment of classic prebuilt (v1) components doesn't support managed online endpoints (v2).
>
> Custom components allow you to wrap your own code as a component. It supports sharing components across workspaces and seamless authoring across studio, CLI v2, and SDK v2 interfaces.
>
> For new projects, we highly recommend that you use custom components, which is compatible with Azure Machine Learning V2 and receives new updates.
>
> This article applies to custom components.

## Register a component in your workspace

To build a pipeline using components in the Designer UI, you need to first register components to your workspace. You can use the UI, Azure CLI, or the SDK to register components to your workspace, so that you can share and reuse the component in the workspace. Registered components support automatic versioning so you can update the component but assure that pipelines that require an older version continue to work.

The following example uses the UI to register components. The [component source files](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components) are in the `cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components` directory of the [`azureml-examples` repository](https://github.com/Azure/azureml-examples). You need to clone the repository.

1. In your Azure Machine Learning workspace, navigate to **Components** page and select **New Component**. The **Components** page appearance differs depending on whether you previously created components.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/register-component-entry-button-2.png" alt-text="Screenshot showing register entry button in component page." lightbox="./media/how-to-create-component-pipelines-ui/register-component-entry-button-2.png":::

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/register-component-entry-button.png" alt-text="Screenshot showing register entry button in component page with can include archive." lightbox="./media/how-to-create-component-pipelines-ui/register-component-entry-button.png":::

   This example uses `train.yml` [in the 1b_e2e_registered_components directory](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components). The YAML file defines the name, type, interface including inputs and outputs, code, environment, and command of this component. The code of this component (`train.py`) is in `./train_src` folder. That code describes the execution logic of this component. To learn more about the component schema, see the [command component YAML schema reference](reference-yaml-component-command.md).

   > [!NOTE]
   > For register components in the UI, `code` defined in the component YAML file can only point to the current folder where YAML file locates or the subfolders. Because the UI can't recognize the parent directory, you can't specify `../`.
   >
   > `additional_includes` can only point to the current folder or subfolder.
   >
   > Currently, the UI only supports registering components with `command` type.

1. Select **Folder**, then browse to the `1b_e2e_registered_components` folder to upload.

1. Select `train.yml` from the **Yaml file name**.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/upload-from-local-folder.png" alt-text="Screenshot showing upload from local folder." lightbox="./media/how-to-create-component-pipelines-ui/upload-from-local-folder.png":::

1. Select **Next**, then confirm the details of this component. After you confirm, select **Create** to finish the registration process.

1. Repeat the previous steps to register Score and Eval component using `score.yml` and `eval.yml`.

1. After registering the three components successfully, you can see your components in the studio UI.

:::image type="content" source="./media/how-to-create-component-pipelines-ui/component-page.png" alt-text="Screenshot showing registered component in component page." lightbox="./media/how-to-create-component-pipelines-ui/component-page.png":::

## Create pipeline by using registered component

1. Create a new pipeline in Designer. Select the **Custom** option.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/new-pipeline.png" alt-text="Screenshot showing creating new pipeline in the Designer homepage." lightbox="./media/how-to-create-component-pipelines-ui/new-pipeline.png":::

1. Select the pencil icon to give the pipeline a meaningful name.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/rename-pipeline.png" alt-text="Screenshot showing rename the pipeline." lightbox="./media/how-to-create-component-pipelines-ui/rename-pipeline.png":::

1. In the Designer asset library, you can see **Data**, **Model**, and **Components** tabs. Select **Components**. You can see the components registered from previous section. If there are too many components, you can search with the component name.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/asset-library.png" alt-text="Screenshot showing registered component in asset library." lightbox="./media/how-to-create-component-pipelines-ui/asset-library.png":::

   Find the *train*, *score*, and *eval* components registered in previous section then drag them to the canvas. By default, Designer uses the default version of the component. To change to a specific version, double-click the component to open the component pane.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/change-component-version.png" alt-text="Screenshot showing changing version of component." lightbox="./media/how-to-create-component-pipelines-ui/change-component-version.png":::

1. In this example, use [the sample data in the data folder](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/data). To register the data into your workspace, select the add icon in the asset library, then follow the wizard to register the data. The data type needs to be `uri_folder` to align with the [train component definition](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/train.yml).

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/add-data.png" alt-text="Screenshot showing add data." lightbox="./media/how-to-create-component-pipelines-ui/add-data.png":::

1. Drag the data into the canvas. Your pipeline should look like the following screenshot.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/pipeline-with-all-boxes.png" alt-text="Screenshot showing the pipeline draft." lightbox="./media/how-to-create-component-pipelines-ui/pipeline-with-all-boxes.png":::

1. Connect the data and components by dragging connections in the canvas.
  
   :::image type="content" source="./media/how-to-create-component-pipelines-ui/connect.gif" alt-text="Animation showing connecting the pipeline." lightbox="./media/how-to-create-component-pipelines-ui/connect.gif":::


5. Double click one component, you'll see a right pane where you can configure the component.

     :::image type="content" source="./media/how-to-create-component-pipelines-ui/component-parameter.png" alt-text="Screenshot showing component parameter settings." lightbox ="./media/how-to-create-component-pipelines-ui/component-parameter.png":::

   For components with primitive type inputs like number, integer, string, and boolean, you can change values of such inputs in the component detailed pane, under **Inputs** section.

   You can also change the output settings (where to store the component's output) and run settings (compute target to run this component) in the right pane.

1. Promote the *max_epocs* input of the *train* component to pipeline level input. By doing so, you can assign a different value to this input every time before submitting the pipeline.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/promote-pipeline-input.png" alt-text="Screenshot showing how to promote component input to pipeline input." lightbox="./media/how-to-create-component-pipelines-ui/promote-pipeline-input.png":::

> [!NOTE]
> Custom components and the Designer classic prebuilt components can't be used together.

## Submit pipeline

1. To submit the pipeline, select **Configure & Submit**.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/configure-submit.png" alt-text="Screenshot showing configure and submit button." border="false":::

1. Then you'll see a step-by-step wizard. Follow the wizard to submit the pipeline job.

  :::image type="content" source="./media/how-to-create-component-pipelines-ui/submission-wizard.png" alt-text="Screenshot showing submission wizard." lightbox ="./media/how-to-create-component-pipelines-ui/submission-wizard.png":::

In **Basics** step, you can configure the experiment, job display name, job description etc.

In **Inputs & Outputs** step, you can configure the Inputs/Outputs that are promoted to pipeline level. In previous step, we promoted the *max_epocs* of *train* component to pipeline input, so you should be able to see and assign value to *max_epocs* here.

In **Runtime settings**, you can configure the default datastore and default compute of the pipeline. It's the default datastore/compute for all components in the pipeline. But note if you set a different compute or datastore for a component explicitly, the system respects the component level setting. Otherwise, it uses the pipeline default value. 

The **Review + Submit** step is the last step to review all configurations before submit. The wizard remembers your last time's configuration if you ever submit the pipeline.

After submitting the pipeline job, there will be a message on the top with a link to the job detail. You can select this link to review the job details.

   :::image type="content" source="./media/how-to-create-component-pipelines-ui/submit-message.png" alt-text="Screenshot showing submission message." lightbox="./media/how-to-create-component-pipelines-ui/submit-message.png":::

## Specify identity in pipeline job

When you submit a pipeline job, you can specify the identity to access the data under `Run settings`. The default identity is `AMLToken`, which doesn't use any identity. A pipeline can also support `UserIdentity` and `Managed`. For `UserIdentity`, the identity of job submitter is used to access input data and write the result to the output folder. If you specify `Managed`, the system uses the managed identity to access the input data and write the result to the output folder.

:::image type="content" source="./media/how-to-create-component-pipelines-ui/identity-in-pipeline.png" alt-text="Screenshot showing how to set identity in pipeline job." lightbox="./media/how-to-create-component-pipelines-ui/identity-in-pipeline.png":::

## Related content

- Use [these Jupyter notebooks on GitHub](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components) to explore machine learning pipelines further.
- Learn [how to use CLI v2 to create pipeline using components](how-to-create-component-pipelines-cli.md).
- Learn [how to use SDK v2 to create pipeline using components](how-to-create-component-pipeline-python.md).
