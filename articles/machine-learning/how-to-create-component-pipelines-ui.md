---
title: Create and run component-based ML pipelines (UI)
titleSuffix: Azure Machine Learning
description: Create and run machine learning pipelines using the Azure Machine Learning studio UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.author: lagayhar
author: lgayhardt
ms.reviewer: keli19
ms.date: 01/08/2026
ms.topic: how-to
ms.custom: devplatv2, designer
ai-usage: ai-assisted
---

# Create and run machine learning pipelines by using components in Azure Machine Learning studio

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

In this article, you learn how to create and run [machine learning pipelines](concept-ml-pipelines.md) by using the Azure Machine Learning studio and [Components](concept-component.md). You can create pipelines without using components, but components offer more flexibility and reuse. You can define Azure Machine Learning Pipelines in YAML and [run them from the CLI](how-to-create-component-pipelines-cli.md), [author them in Python](how-to-create-component-pipeline-python.md), or compose them in Azure Machine Learning studio Designer with a drag-and-drop UI. This article focuses on the Azure Machine Learning studio designer UI.

## Prerequisites

- If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An Azure Machine Learning workspace. [Create workspace resources](quickstart-create-resources.md).

- [Install and set up the Azure CLI extension for Machine Learning](how-to-configure-cli.md).

- Clone the examples repository:

    ```azurecli-interactive
    git clone https://github.com/Azure/azureml-examples --depth 1
    cd azureml-examples/cli/jobs/pipelines-with-components/
    ```

>[!Note]
> Designer supports two types of components: classic prebuilt components (v1) and custom components (v2). These two types of components aren't compatible.
>
> Classic prebuilt components mainly provide prebuilt components for data processing and traditional machine learning tasks like regression and classification. Classic prebuilt components continue to be supported but don't receive new components. Also, deployment of classic prebuilt (v1) components doesn't support managed online endpoints (v2).
>
> Custom components allow you to wrap your own code as a component. They support sharing components across workspaces and seamless authoring across studio, CLI v2, and SDK v2 interfaces.
>
> For new projects, use custom components, which are compatible with AzureML V2 and receive new updates.
>
> This article applies to custom components.

## Register a component in your workspace

To build a pipeline by using components in the UI, first register components to your workspace. Use the UI, CLI, or SDK to register components to your workspace, so you can share and reuse the component within the workspace. Registered components support automatic versioning, so you can update the component but assure that pipelines that require an older version continue to work.  

The following example uses the UI to register components. The [component source files](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components) are in the `cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components` directory of the [`azureml-examples` repository](https://github.com/Azure/azureml-examples). You need to clone the repo to your local computer first.

1. In your Azure Machine Learning workspace, navigate to the **Components** page and select **New Component**.
    One of the two style pages appears:

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/register-component-entry-button-2.png" alt-text="Screenshot showing register entry button in component page." lightbox="./media/how-to-create-component-pipelines-ui/register-component-entry-button-2.png":::

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/register-component-entry-button.png" alt-text="Screenshot showing register entry button in component page with can include archive." lightbox="./media/how-to-create-component-pipelines-ui/register-component-entry-button.png":::

This example uses `train.yml` [in the 1b_e2e_registered_components directory](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components). The YAML file defines the name, type, interface including inputs and outputs, code, environment, and command of this component. The code for this component, `train.py`, is under the `./train_src` folder. It describes the execution logic of this component. To learn more about the component schema, see the [command component YAML schema reference](reference-yaml-component-command.md).

>[!Note]
> When you register components in the UI, the `code` defined in the component YAML file can only point to the current folder where the YAML file is located or its subfolders. You can't specify `../` for `code` because the UI can't recognize the parent directory.
> `additional_includes` can only point to the current folder or a subfolder.
> Currently, the UI only supports registering components with the `command` type.

1. Select **Upload from Folder**, and select the `1b_e2e_registered_components` folder to upload. Select `train.yml` from the drop-down list.

:::image type="content" source="./media/how-to-create-component-pipelines-ui/upload-from-local-folder.png" alt-text="Screenshot showing upload from local folder." lightbox="./media/how-to-create-component-pipelines-ui/upload-from-local-folder.png":::

1. Select **Next** at the bottom. You can confirm the details of this component. Once you confirm, select **Create** to finish the registration process.

1. Repeat the previous steps to register the **Score** and **Eval** components by using `score.yml` and `eval.yml`.

1. After registering the three components successfully, you see your components in the studio UI.

:::image type="content" source="./media/how-to-create-component-pipelines-ui/component-page.png" alt-text="Screenshot showing registered component in component page." lightbox="./media/how-to-create-component-pipelines-ui/component-page.png":::

## Create pipeline by using registered component

1. Create a new pipeline in the designer. Select the **Custom** option.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/new-pipeline.png" alt-text="Screenshot showing creating new pipeline in designer homepage." lightbox ="./media/how-to-create-component-pipelines-ui/new-pipeline.png":::

1. Give the pipeline a meaningful name. Select the pencil icon next to the autogenerated name.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/rename-pipeline.png" alt-text="Screenshot showing rename the pipeline." lightbox ="./media/how-to-create-component-pipelines-ui/rename-pipeline.png":::

1. In the designer asset library, you see **Data**, **Model**, and **Components** tabs. Switch to the **Components** tab. You see the components registered from previous section. If there are too many components, you can search by component name.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/asset-library.png" alt-text="Screenshot showing registered component in asset library." lightbox ="./media/how-to-create-component-pipelines-ui/asset-library.png":::

    Find the *train*, *score*, and *eval* components registered in previous section. Drag and drop them on the canvas. By default, the pipeline uses the default version of the component. To change to a specific version, double-click the component to open the component pane.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/change-component-version.png" alt-text="Screenshot showing changing version of component." lightbox ="./media/how-to-create-component-pipelines-ui/change-component-version.png":::

    In this example, use [the sample data in the data folder](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/data). Register the data into your workspace by selecting the add icon in designer asset library -> data tab. Set Type = Folder(uri_folder) then follow the wizard to register the data. The data type needs to be uri_folder to align with the [train component definition](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/train.yml).

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/add-data.png" alt-text="Screenshot showing add data." lightbox ="./media/how-to-create-component-pipelines-ui/add-data.png":::

    Then drag and drop the data into the canvas. Your pipeline look should look like the following screenshot now.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/pipeline-with-all-boxes.png" alt-text="Screenshot showing the pipeline draft." lightbox ="./media/how-to-create-component-pipelines-ui/pipeline-with-all-boxes.png":::

1. Connect the data and components by dragging connections in the canvas.
  
     :::image type="content" source="./media/how-to-create-component-pipelines-ui/connect.gif" alt-text="Gif showing connecting the pipeline." lightbox ="./media/how-to-create-component-pipelines-ui/connect.gif":::


1. Double-click one component. You see a right pane where you can configure the component.

     :::image type="content" source="./media/how-to-create-component-pipelines-ui/component-parameter.png" alt-text="Screenshot showing component parameter settings." lightbox ="./media/how-to-create-component-pipelines-ui/component-parameter.png":::

    For components with primitive type inputs like number, integer, string, and boolean, change values of such inputs in the component detailed pane, under **Inputs** section.

    You can also change the output settings (where to store the component's output) and run settings (compute target to run this component) in the right pane.

    Now promote the *max_epocs* input of the *train* component to pipeline level input. By doing this step, you can assign a different value to this input every time before submitting the pipeline.

     :::image type="content" source="./media/how-to-create-component-pipelines-ui/promote-pipeline-input.png" alt-text="Screenshot showing how to promote component input to pipeline input." lightbox ="./media/how-to-create-component-pipelines-ui/promote-pipeline-input.png":::

> [!NOTE]
> You can't use custom components and the designer classic prebuilt components together.

## Submit pipeline

1. Select **Configure & Submit** to submit the pipeline.

    :::image type="content" source="./media/how-to-create-component-pipelines-ui/configure-submit.png" alt-text="Screenshot showing configure and submit button." border="false":::

1. A step-by-step wizard appears. Follow the wizard to submit the pipeline job.

  :::image type="content" source="./media/how-to-create-component-pipelines-ui/submission-wizard.png" alt-text="Screenshot showing submission wizard." lightbox ="./media/how-to-create-component-pipelines-ui/submission-wizard.png":::

In the **Basics** step, you can configure the experiment, job display name, job description, and other settings.

In the **Inputs & Outputs** step, you can configure the inputs and outputs that are promoted to the pipeline level. In the previous step, you promoted the *max_epocs* of the *train* component to a pipeline input, so you should see and assign a value to *max_epocs* here.

In the **Runtime settings**, you can configure the default datastore and default compute for the pipeline. These settings apply to all components in the pipeline. If you set a different compute or datastore for a component explicitly, the system uses the component level setting. Otherwise, it uses the pipeline default value. 

> [!NOTE]
> Designer pipelines don't support Spark compute (serverless Spark or attached Synapse Spark pools) or Spark components. Use CLI v2 or the Python SDK to run Spark components in pipelines. For standalone Spark jobs, select **+ New** > **Spark job (preview)** in Azure Machine Learning studio.

The **Review + Submit** step is the last step to review all configurations before submitting. The wizard remembers your last configuration if you ever submit the pipeline.

After submitting the pipeline job, a message appears at the top with a link to the job detail. Select this link to review the job details.

  :::image type="content" source="./media/how-to-create-component-pipelines-ui/submit-message.png" alt-text="Screenshot showing submission message." lightbox ="./media/how-to-create-component-pipelines-ui/submit-message.png":::

## Specify identity in pipeline job

When you submit a pipeline job, specify the identity to access the data under `Run settings`. The default identity is `AMLToken` which doesn't use any identity. Support both `UserIdentity` and `Managed`. For `UserIdentity`, the identity of job submitter is used to access input data and write the result to the output folder. If you specify `Managed`, the system uses the managed identity to access the input data and write the result to the output folder.

  :::image type="content" source="./media/how-to-create-component-pipelines-ui/identity-in-pipeline.png" alt-text="Screenshot showing how to set identity in pipeline job." lightbox ="./media/how-to-create-component-pipelines-ui/identity-in-pipeline.png":::

## Next steps

- Use [these Jupyter notebooks on GitHub](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components) to explore machine learning pipelines further.
- Learn [how to use CLI v2 to create pipeline using components](how-to-create-component-pipelines-cli.md).
- Learn [how to use SDK v2 to create pipeline using components](how-to-create-component-pipeline-python.md).
