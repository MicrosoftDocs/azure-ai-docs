---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/03/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD041 -->
## Prerequisites

> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource, you can continue to use those existing Language resources within the Microsoft Foundry portal via a Foundry Hub project.
> * For more information, see [How to use Foundry Tools in the Foundry portal](../../../../connect-services-foundry-portal.md)
> * We highly recommended that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.

<!-- markdownlint-disable MD032 -->
[!INCLUDE [Foundry prerequisites](../../../includes/microsoft-foundry/prerequisites.md)]
* A [**Conversational language understanding (CQA)**](../../../conversational-language-understanding/overview.md) or [**Custom question answering (CQA)**](../../../question-answering/overview.md) project created in the Foundry.

## Migrate an existing orchestration workflow from Language Studio

If you have an existing orchestration workflow in Language Studio that you want to use in Foundry, you have two migration options:

### Option 1: Connect your Language resource to a Foundry Hub (recommended)

Connect your existing Language resource to a Foundry Hub project. This approach automatically preserves all task linkages between your orchestration workflow and its associated CLU and CQA tasks.

### Option 2: Import projects into a new Foundry resource

If you want to use a new Foundry resource, import your projects individually. To preserve task linkages, import in the following order:

1. Import your CLU and CQA tasks first.
1. Import the orchestration workflow only after the dependent tasks are available in the Foundry resource.

> [!IMPORTANT]
> The import order matters. If you import the orchestration workflow before its dependent CLU and CQA tasks, the task linkages aren't preserved. You must then manually relink the tasks in the **Configure orchestration** section.

For detailed migration steps, see [Migrate from Language Studio to Microsoft Foundry](../../../migration-studio-to-foundry.md).

## Get started

After you create your Foundry resource, you can initiate an orchestration workflow project in the [Microsoft Foundry](https://ai.azure.com/). This project serves as a dedicated workspace for developing custom machine learning models using your data. Access to the project is restricted to you and others who have permissions for the associated Foundry resource.

For this quickstart, you can complete the [**Conversational Language Understanding quickstart**](../../../conversational-language-understanding/quickstart.md) or [**Custom question answering (CQA)**](../../../question-answering/quickstart/sdk.md) to establish a project for use in our subsequent orchestration workflow quickstart steps.

Let's begin:

1. Navigate to the Foundry.

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, you can create or access your existing projects within Foundry.

1. If you're not already in your **`CLU`** or **`CQA`** project, select it now.

## Create an orchestration workflow project

1. Select **Fine-tuning** from the left navigation pane.

1. From the window that appears, select the AI Service fine-tuning tab and then the **+ Fine-tune** button.

   :::image type="content" source="../../media/select-fine-tuning.png" alt-text="Screenshot of create fine-tuning button in the Foundry.":::

1. From the window that appears, select **Conversational Orchestration Workflow** as the task type, then select **Next**. 

* If you don't have a CLU or CQA fine-tuning task in this Foundry resource, a warning appears indicating that no tasks are available to link. 

     :::image type="content" source="../../media/no-tasks-warning.png" alt-text="Screenshot of no tasks warning in orchestration workflow creation in the Foundry.":::

* Create a [Conversational Language Understanding](../../../conversational-language-understanding/quickstart.md) or [Custom Question Answering](../../../question-answering/quickstart/sdk.md) task first, then return to create your orchestration workflow.

1. In the **Create service fine-tuning window**, you can choose to create a new task or import an existing one. Complete all required fields, then select **Create**:

    * **Name**: Provide a unique name for your orchestration workflow project.
    * **Language**: Select the language for your project.
    * **Description**: Optionally, provide a description for your project.

1. After creating the orchestration workflow project, you'll be directed to the project overview page. Here, you can manage your project settings, monitor training progress, and access various tools to enhance your model.

## Configure orchestration

Connect your existing **Conversational Language Understanding** (CLU) and **Custom Question Answering** (CQA) fine-tuning tasks to create a unified orchestration layer that routes user inputs to the appropriate model. You can define more routing intents when user inputs are ambiguous and need extra logic to identify the correct task.

> [!NOTE]
> If the **Configure orchestration** page is empty, you don't have any CLU or CQA fine-tuning tasks in this Foundry resource. Create a [Conversational Language Understanding](../../../conversational-language-understanding/quickstart.md) or [Custom Question Answering](../../../question-answering/quickstart/sdk.md) task first, then return to this page and link it.

1. To add existing **`CLU`** or **`CQA`** models to your orchestration workflow, navigate to your fine-tuning project and select the **Configure orchestration** section from the **Getting started** menu. There, you can link your fine-tuning tasks and add intents from your existing models to the orchestration workflow.

   :::image type="content" source="../../media/orchestration-workflow-overview.png" alt-text="Screenshot of orchestration workflow overview in the Foundry." lightbox="../../media/orchestration-workflow-overview.png":::

1. Link your tasks by selecting the radio button next to the task you want to link, and then selecting the **Link fine-tuning task** from the top navigation bar. The **Orchestration intent name** field automatically populates with the same name as the **Fine-tuning task name** field.

   :::image type="content" source="../../media/orchestration-link-tasks.png" alt-text="Screenshot of linking tasks in orchestration workflow in the Foundry." lightbox="../../media/orchestration-link-tasks.png":::

1. Once this step is complete, the status for your linked tasks changes from **Unlinked** to **Linked** in the **Configure orchestration** section.

   :::image type="content" source="../../media/orchestration-linked-tasks.png" alt-text="Screenshot of linked tasks in orchestration workflow in the Foundry." lightbox="../../media/orchestration-linked-tasks.png":::

1. To link multiple fine-tuning tasks at once, select one or more unlinked tasks, then select **Link fine-tuning task** from the top navigation bar.

1. To unlink tasks, select one or more linked tasks, then select **Unlink fine-tuning task** from the top navigation bar.

1. To add routing intents, select the **Intents** tab from the top navigation bar. In the window that appears, select the **+ Add intent** button, provide a unique name for your intent in the **Intent name** field, then select **Add** to continue.

   :::image type="content" source="../../media/orchestration-add-intent.png" alt-text="Screenshot of adding intents in orchestration workflow in the Foundry." lightbox="../../media/orchestration-add-intent.png":::

## Add training data

1. Navigate to the Manage Data tab. For this project, use one of your existing **Conversational Language Understanding** (CLU) projects. If your existing project doesn't include labeled utterances, you can download our [**sample utterances file**](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/language-service/CLU/clu_utterances.json) which comes preconfigured with labeled utterances.

1. Select the **Upload utterances** button to upload your utterances file in JSON format.

   :::image type="content" source="../../media/upload-utterances.png" alt-text="Screenshot of uploading utterances in orchestration workflow in the Foundry.":::

1. After uploading your utterances file, select the **unlinked intents** from the Insights pane. This action allows you to map these intents to the appropriate linked tasks within your orchestration workflow.

   :::image type="content" source="../../media/select-unlinked-intents.png" alt-text="Screenshot of unlinked intents in orchestration workflow in the Foundry.":::

## Train your model

1. Navigate to the **Train model** section and select the **Train model** button to start training your orchestration workflow with the linked tasks and uploaded utterances. This process may take some time depending on the size of your dataset and the complexity of your model.

   :::image type="content" source="../../media/train-orchestration-model.png" alt-text="Screenshot of training orchestration button in the Foundry.":::

1. In the **Train a new model** window, provide a name for your model, keep the default standard training mode, and select **Next** to proceed.

   :::image type="content" source="../../media/train-new-model.png" alt-text="Screenshot of training orchestration model window in the Foundry.":::

1. In the data splitting window, you can choose to either use the default data split or customize it according to your needs. After making your selection, select **Next** to continue.

1. Review your selections in the summary window, and if everything looks correct, select **Create** to initiate the training process for your orchestration workflow model.

   :::image type="content" source="../../media/training-review.png" alt-text="Screenshot of orchestration model training summary in the Foundry.":::

1. After initiating the training process, you can monitor the progress and view detailed metrics on the training dashboard. Once the training is complete, your orchestration workflow model is ready for deployment and testing.

## Deploy your model

Deploy your trained model by navigating to the **Deploy model** section and selecting the **Deploy** button. Follow the prompts to complete the deployment process.

   :::image type="content" source="../../media/deploy-trained-model.png" alt-text="Screenshot of deploying orchestration model button in the Foundry.":::

## Test your model

After your model successfully deploys, you can test it directly within the Foundry interface. Navigate to the **Test in playground** section, input various utterances, and observe how your orchestration workflow routes requests to the appropriate linked tasks.

That's it, congratulations!

## Clean up resources

If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.

1. Select the project that you want to delete from the **Keep building with Foundry**

1. Select **Management center**.

1. Select **Delete project**.



