---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal. 
> * For more information, see [How to use Foundry Tools in the Foundry portal](/azure/ai-services/connect-services-foundry-portal).
> * We highly recommended that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.

## Prerequisites

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).
*  [Foundry resource](/azure/ai-services/multi-service-resource). For more information, *see* [Configure a Foundry resource](../../../concepts/configure-azure-resources.md). Alternately, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project created in the Foundry**. For more information, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).

## Get started with Foundry

To complete this quickstart, you need a Conversational Language Understanding (CLU) fine-tuning task project that includes a [defined schema](../../how-to/build-schema.md) and [labeled utterances](../../how-to/tag-utterances.md). 

You can download our [**sample project file**](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/language-service/CLU/EmailAppDemo.json), which comes preconfigured with both a schema and labeled utterances. This project enables the prediction of user intent for commands such as reading emails, deleting emails, and attaching documents to emails.

Let's begin:

1. Navigate to the [Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Foundry.
1. If you're not already at your project for this task, select it.
1. On the left side navigation pane, select **Playgrounds**, navigate to the **Language playground tile**, and then choose the **Try Azure Language playground** button.

  :::image type="content" source="../../media/quickstarts/try-playground.png" alt-text="Screenshot of the Try Language Playground selection in Foundry.":::

## Try Azure Language playground

The top section of Azure Language playground is where you can view and select the available Languages. 

1. Select the **Conversational language understanding** tile.

    :::image type="content" source="../../media/quickstarts/language-playground.png" alt-text="Screenshot of the language playground homepage in Foundry.":::

1. Next, scroll to and select the **Fine-tune** button.

   :::image type="content" source="../../media/quickstarts/fine-tune-button.png" alt-text="Screenshot of the fine-tune button on the language playground homepage in Foundry.":::

1. From **Create service fine-tuning** window, choose the **Conversational language understanding** card. Then select **Next**.

    :::image type="content" source="../../media/quickstarts/select-project.png" alt-text="Screenshot of conversational language understanding selection tile in the Foundry.":::

1. In **Create CLU fine tuning task** window, select **Import an existing project**, then choose your **Connected service** from the drop-down menu and complete the **Name** field.

    :::image type="content" source="../../media/quickstarts/select-import-existing-project.png" alt-text="Screenshot of the import an existing project selection in Foundry.":::

1. Next, add the [sample project file](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/language-service/CLU/EmailAppDemo.json) that you downloaded earlier to the upload area.

1. Select the  **Create** button. It can take a few minutes for the *creating* operation to complete.

1. Once your fine-tuning task project is created, the **Getting started with fine-tuning** page opens.

   :::image type="content" source="../../media/create-project/getting-started-fine-tuning.png" alt-text="Screenshot of the getting started with fine-tuning page in the Foundry." lightbox="../../media/create-project/getting-started-fine-tuning.png":::

## Train your model

After project creation, the next steps are [schema construction](../../how-to/build-schema.md) and [utterance labeling](../../how-to/tag-utterances.md). For this quickstart, these steps are preconfigured in the sample project. Therefore, you can go ahead and initiate a training job by selecting **Train model** from the **Getting Started** menu to generate your model.

  :::image type="content" source="../../media/quickstarts/getting-started-menu.png" alt-text="Screenshot of the getting started with fine-tuning menu in the Foundry.":::

1. Select the **➕Train model button** from the **Train your model** window.

    :::image type="content" source="../../media/quickstarts/train-your-model-button.png" alt-text="Screenshot of the train your model button in the Foundry.":::

1. Complete the **Select a mode** form by completing the **Model name** field and selecting a **Training mode**. For this quickstart, select the free **Standard training** mode. For more information, *see* [Training modes](../../how-to/train-model.md#training-modes).

1. Choose a **Training version** from the drop-down menu, then select the **Next** button.

1. Check your selections in the **Review** window, then select the **Create** button

    :::image type="content" source="../../media/quickstarts/review-selections.png" alt-text="Screenshot of the review selections window in the Foundry.":::

## Deploy your model

Typically, after training a model, you review its evaluation details. For this quickstart, you can just deploy your model and make it available to test in Azure Language playground, or by calling the [prediction API](https://aka.ms/clu-apis). However, if you wish, you can take a moment to select **Evaluate your model** from the left-side menu and explore the in-depth telemetry for your model. Complete the following steps to deploy your model within Foundry:

1. Select **Deploy model** from the left-side menu.
1. Next, select **➕Deploy a trained model** from the **Deploy your model** window.

    :::image type="content" source="../../media/quickstarts/deploy-trained-model.png" alt-text="Screenshot of the deploy your model window in Foundry.":::

1. Make sure the **Create a new deployment** button is selected.

1. Complete the **Deploy a trained model** window fields:

   * Create a deployment name. 
   * Select your trained model from the **Assign a model** drop-down menu.
   * Select a subscription from the **Subscription** drop-down menu.
   * Select a region from the **Region** drop-down menu.
   * Select a resource from the **Resource** drop-down menu. The resource must be in the same deployment region.


       :::image type="content" source="../../media/quickstarts/deploy-model-configuration.png" alt-text="Screenshot of the deploy your model configuration in Foundry.":::

1. Finally, select the **Create** button. It may take a few minutes for your model to deploy.

1. After successful deployment, you can view your model's deployment status on the **Deploy your model** page. The expiration date that appears marks the date when your deployed model becomes unavailable for prediction tasks. This date is usually 18 months after a training configuration is deployed.

    :::image type="content" source="../../media/quickstarts/deployed-model-succeeded.png" alt-text="Screenshot of your successfully deployed model status page in Foundry.":::

1. From the far-left menu, navigate to Azure Language playground.<br>
   **Playgrounds** → **Language playground (Try Azure Language playground)**.
1. Select the **Conversational language understanding** card.
1. A **Configuration** window with your deployed model should appear in the main/center window.
1. In the text box, enter an utterance to test. For example, if you used our [sample project](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/language-service/CLU/EmailAppDemo.json) application for email-related utterances you could enter ***Check email***.
1. After you enter your test text, select the **Run** button.

    :::image type="content" source="../../media/quickstarts/deployed-model-succeeded.png" alt-text="Screenshot of your successfully deployed model status page in Foundry.":::
1. After you run the test, you should see the response of the model in the result. 

    :::image type="content" source="../../media/quickstarts/language-playground-test.png" alt-text="Screenshot of deployed model testing in Foundry language playground.":::

1. You can view the results in a text or JSON format view.

    :::image type="content" source="../../media/quickstarts/language-playground-test-results.png" alt-text="Screenshot of deployed model test results in Foundry language playground.":::

That's it, congratulations!

In this quickstart, you deployed a CLU model and tested it in the Foundry Language playground. Next, learn how to [Create your own fine-tuning task project ](../../how-to/create-project.md) for your applications and workflows.

## Clean up resources

If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Foundry**
1. Select **Management center**.
1. Select **Delete project**.

   :::image type="content" source="../../media/create-project/delete-project.png" alt-text="Screenshot of the Delete project button in the Foundry.":::

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.

   :::image type="content" source="../../media/create-project/hub-details.png" alt-text="Screenshot of the hub details list in the Foundry.":::

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub there.

   :::image type="content" source="../../media/create-project/delete-hub.png" alt-text="Screenshot of the Delete hub button in the Foundry.":::

