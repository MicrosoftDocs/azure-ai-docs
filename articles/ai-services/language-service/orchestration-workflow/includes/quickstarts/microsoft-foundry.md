---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 01/09/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD041 -->
[!INCLUDE [Foundry introduction](../../../includes/microsoft-foundry/introduction.md)]

[!INCLUDE [Foundry prerequisites](../../../includes/microsoft-foundry/prerequisites.md)]

* A [**Conversational language understanding (CQA)**](../../../conversational-language-understanding/overview.md) or [**Custom question answering (CQA)**](../../../question-answering/overview.md) project created in the Foundry.

## Get started

After you create your Language resource, you can initiate an orchestration workflow project in the [Microsoft Foundry](https://ai.azure.com/). This project serves as a dedicated workspace for developing custom machine learning models using your data. Access to the project is restricted to you and others who have permissions for the associated Azure Language resource.

For this quickstart, you can complete the [**Conversational Language Understanding quickstart**](../../../conversational-language-understanding/quickstart.md) or [**Custom question answering (CQA)**](../../../question-answering/quickstart/sdk.md) to establish a project for use in our subsequent orchestration workflow quickstart steps.

Let's begin:

1. Navigate to the Foundry.

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, you can create or access your existing projects within Foundry.

1. If you're not already in your `CLU` or `CQA` project, select it now.

   :::image type="content" source="../../media/select-fine-tuning.png" alt-text="Screenshot of fine-tuning selector in the Foundry.":::

## Create an orchestration workflow project

1. Select **Fine-tuning** from the left navigation pane.

1. From the window that appears, select the AI Service fine-tuning tab and then the + Fine-tune button.

   :::image type="content" source="../../media/select-fine-tuning.png" alt-text="Screenshot of create fine-tuning button in the Foundry.":::


1. From the window that appears, select **Conversational Orchestration Workflow** as the task type, then select **Next**.

   :::image type="content" source="../../media/select-orchestration-workflow.png" alt-text="Screenshot of selecting orchestration workflow in the Foundry.":::

1. In the **Create service fine-tuning window**, you can choose to create a new task or import an existing one. Complete all required fields, then  select **Create**:

* **Name**: Provide a unique name for your orchestration workflow project.
* **Language**: Select the language for your project.
* **Description**: Optionally, provide a description for your project.

1. After creating the orchestration workflow project, you'll be directed to the project overview page. Here, you can manage your project settings, monitor training progress, and access various tools to enhance your model.

## Link tasks

1. To add existing `CLU` or `CQA` models to your orchestration workflow, navigate to the **Link tasks** button within your project. Here, you can add intents and entities from your existing models to the orchestration workflow.

   :::image type="content" source="../../media/orchestration-workflow-overview.png" alt-text="Screenshot of orchestration workflow overview in the Foundry.":::

1. Link your tasks by selecting from the **Task type** and **Fine-tuning task name** dropdown menus. The **Intent name** field automatically populates with the same name as the **fine-tuning task name** field. Once everything is set, select **Add** to continue.

   :::image type="content" source="../../media/orchestration-link-tasks.png" alt-text="Screenshot of linking tasks in orchestration workflow in the Foundry.":::

## Add training data

1. Navigate to the Manage Data tab and add your utterances file. For this project, you can download our [**sample utterances file**](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/language-service/CLU/clu_utterances.json) which comes preconfigured with labeled utterances.

1. After uploading your utterances file, select the **unlinked intents** from the Insights pane. This action allows you to map these intents to the appropriate linked tasks within your orchestration workflow.

   :::image type="content" source="../../media/select-unlinked-intents.png" alt-text="Screenshot of unlinked intents in orchestration workflow in the Foundry.":::

## Train your model

1. Next, navigate to the **Train model** sections and select the **Train model** button to start training your orchestration workflow with the linked tasks and uploaded utterances. This process may take some time depending on the size of your dataset and the complexity of your model.

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



