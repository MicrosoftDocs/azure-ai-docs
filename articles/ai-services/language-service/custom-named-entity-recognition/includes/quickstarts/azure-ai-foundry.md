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
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal. For more information, see [How to use Foundry Tools in the Foundry portal](/azure/ai-services/connect-services-foundry-portal).

## Prerequisites

* An **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* The **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control).

*  An [**Language resource with a storage account**](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics). On the **select additional features** page, select the **Custom text classification, Custom named entity recognition, Custom sentiment analysis & Custom Text Analytics for health** box to link a required storage account to this resource:

    :::image type="content" source="../../media/foundry-next/select-additional-features.png" alt-text="Screenshot of the select additional features option in the Foundry.":::

  > [!NOTE]
  >  * You need to have an **owner** role assigned on the resource group to create a Language resource.
  >  * If you're connecting a preexisting storage account, you should have an owner role assigned to it.
  >  * Don't move the storage account to a different resource group or subscription once linked with Azure Language resource.


* **A Foundry project created in the Foundry**. For more information, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).

* **A custom NER dataset uploaded to your storage container**. A custom named entity recognition (NER) dataset is the collection of labeled text documents used to train your custom NER model. You can [download our sample dataset](https://go.microsoft.com/fwlink/?linkid=2175226) for this quickstart. The source language is English.

## Step 1: Configure required roles, permissions, and settings

Let's begin by configuring your resources.

### Enable custom named entity recognition feature

Make sure the **Custom text classification / Custom Named Entity Recognition** feature is enabled in the [Azure portal](https://portal.azure.com/).

1. Navigate to your Language resource in the [Azure portal](https://portal.azure.com).
1. From the left side menu, under **Resource Management** section, select **Features**.
1. Make sure the **Custom text classification / Custom Named Entity Recognition** feature is enabled.
1. If your storage account isn't assigned, select and connect your storage account.
1. Select **Apply**.

### Add required roles for your Language resource

1. From the Language resource page in the [Azure portal](https://portal.azure.com/), select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and add **Cognitive Services Language Owner** or **Cognitive Services Contributor** role assignment for your Language resource.
1. Within **Assign access to**, select **User, group, or service principal**.
1. Select **Select members**.
1. Select ***your user name***. You can search for user names in the **Select** field. Repeat this step for all roles.
1. Repeat these steps for all the user accounts that need access to this resource.


### Add required roles for your storage account

1. Go to your storage account page in the [Azure portal](https://portal.azure.com/).
1. Select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and choose the **Storage blob data contributor** role on the storage account.
1. Within **Assign access to**, select **Managed identity**.
1. Select **Select members**.
1. Select your subscription, and **Language** as the managed identity. You can search for your language resource in the **Select** field.

### Add required user roles

> [!IMPORTANT]
> If you skip this step, you get a 403 error when you try to connect to your custom project. It's important that your current user has this role to access storage account blob data, even if you're the owner of the storage account.
>

1. Go to your storage account page in the [Azure portal](https://portal.azure.com/).
1. Select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and choose the **Storage blob data contributor** role on the storage account.
1. Within **Assign access to**, select **User, group, or service principal**.
1. Select **Select members**.
1. Select your User. You can search for user names in the **Select** field.

> [!IMPORTANT]
> If you have a Firewall or virtual network or private endpoint, be sure to select **Allow Azure services on the trusted services list to access this storage account** under the **Networking tab** in the Azure portal.

   :::image type="content" source="../../media/foundry-next/allow-azure-services.png" alt-text="Screenshot of allow Azure services enabled in Foundry.":::

## Step 2: Upload your dataset to your storage container

Next, let's add a container and upload your dataset files directly to the root directory of your storage container. These documents are used to train your model.

1. Add a container to the storage account associated with your language resource. For more information, *see* [create a container](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container).

1. [Download the sample dataset](https://go.microsoft.com/fwlink/?linkid=2175226) from GitHub. The provided sample dataset contains 20 loan agreements:

    * Each agreement includes two parties: a lender and a borrower.
    * You extract relevant information for: both parties, agreement date, loan amount, and interest rate.

1. Open the .zip file, and extract the folder containing the documents.

1. Navigate to the Foundry.

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, access your existing Foundry project for this quickstart.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. Next choose the workspace blob storage that was set up for you as a connected resource.

1. On the workspace blob storage, select **View in Azure portal**.


1. On the **AzurePortal** page for your blob storage, select **Upload** from the top menu. Next, choose the `.txt` and `.json` files you downloaded earlier. Finally, select the **Upload** button to add the file to your container.

    :::image type="content" source="../../media/foundry-next/upload-blob-files.png" alt-text="A screenshot showing the button for uploading files to the storage account.":::


Now that the required Azure resources are provisioned and configured within the Azure portal,  let's use these resources in the Foundry to create a fine-tuned custom Named Entity Recognition (NER) model.

## Step 3: Connect your Language resource

Next we create a connection to your Language resource so Foundry can access it securely. This connection provides secure identity management and authentication, as well as controlled and isolated access to data.

1. Return to the [Foundry](https://ai.azure.com/).

1. Access your existing Foundry project for this quickstart.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. In the main  window, select the **+ New connection** button.

1. Select **Language** from the **Add a connection to external assets** window.

1. Select **Add connection**, then select **Close.**

    :::image type="content" source="../../media/foundry-next/add-connection.png" alt-text="Screenshot of the connection window in Foundry.":::

## Step 4: Fine tune your custom NER model

Now, we're ready to create a  custom NER fine-tune model.

1. From the **Project** section of the **Management center** menu, select **Go to project**.

1. From the **Overview** menu, select **Fine-tuning**.

1. From the main window, select **the AI Service fine-tuning** tab and then the **+ Fine-tune** button.

1. From the **Create service fine-tuning** window, choose the **Custom named entity recognition** tab, and then select **Next**.

    :::image type="content" source="../../media/foundry-next/create-fine-tuning.png" alt-text="Screenshot of the fine-tuning selection tile in Foundry." lightbox="../../media/foundry-next/create-fine-tuning.png":::

1. In the **Create service fine-tuning task** window, complete the fields as follows:

    * **Connected service**. The name of your Language resource should already appear in this field by default. if not, add it from the drop-down menu.

    * **Name**. Give your fine-tuning task project a name.

    * **Language**. English is set as the default and already appears in the field.

    * **Description**. You can optionally provide a description or leave this field empty.

     * **Blob store container**. Select the workspace blob storage container from [Step 2](#step-2-upload-your-dataset-to-your-storage-container) and choose the **Connect** button.

1. Finally, select the  **Create** button. It can take a few minutes for the *creating* operation to complete.

## Step 5: Train your model

   :::image type="content" source="../../media/foundry-next/workflow.png" alt-text="Screenshot of fine-tuning workflow in Foundry.":::


1. From the **Getting Started** menu, choose **Manage data**. In the **Add data for training and testing** window, you see the sample data that you previously uploaded to your Azure Blob Storage container.
1. Next, from the **Getting Started** menu, select **Train model**.
1. Select the **+ Train model button**. When the **Train a new model** window appears, enter a name for your new model and keep the default values. Select the **Next** button.
1. In the **Train a new model** window, keep the default **Automatically split the testing set from training data** enabled with the recommended percentage set at 80% for training data and 20% for testing data.
1. Review your model configuration then select the **Create** button.
1. After training a model, you can select **Evaluate model** from the **Getting started** menu. You can select your model from the **Evaluate you model** window and make improvements if necessary.

## Step 6: Deploy your model

Typically, after training a model, you review its evaluation details. For this quickstart, you can just deploy your model and make it available to test in Azure Language playground, or by calling the [prediction API](https://aka.ms/clu-apis). However, if you wish, you can take a moment to select **Evaluate your model** from the left-side menu and explore the in-depth telemetry for your model. Complete the following steps to deploy your model within Foundry.

1. Select **Deploy model** from the left-side menu.
1. Next, select **➕Deploy a trained model** from the **Deploy your model** window.

    :::image type="content" source="../../media/foundry-next/deploy-trained-model.png" alt-text="Screenshot of the deploy your model window in Foundry.":::

1. Make sure the **Create a new deployment** button is selected.

1. Complete the **Deploy a trained model** window fields:

   * **Deployment name**. Name your model.
   * **Assign a model**. Select your trained model from the drop-down menu.
   * **Region**. Select a region from the drop-down menu.

1. Finally, select the **Create** button. It may take a few minutes for your model to deploy.

1. After successful deployment, you can view your model's deployment status on the **Deploy your model** page. The expiration date that appears marks the date when your deployed model becomes unavailable for prediction tasks. This date is usually 18 months after a training configuration is deployed.

    :::image type="content" source="../../media/foundry-next/deployed-model.png" alt-text="Screenshot of the deploy your model status window in Foundry.":::

## Step 7: Try Azure Language playground

The Language playground provides a sandbox to test and configure your fine-tuned model before deploying it to production, all without writing code.

1. From the top menu bar, select **Try in playground**.
1. In Azure Language Playground window, select the **Custom named entity recognition** tile.
1. In the **Configuration** section, select your **Project name** and **Deployment name** from the drop-down menus.
1. Enter an entity and select **Run**.
1. You can evaluate the results in the **Details** window.


That's it, congratulations!

In this quickstart, you created a fine-tuned custom NER model, deployed it in Foundry, and tested your model in Azure Language playground.

## Clean up resources

If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Foundry**.
1. Select **Management center**.
1. Select **Delete project**.

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab in the **Hub** section.

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub there.
