---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 09/22/2025
ms.author: lajanuar
---

> [!NOTE]
>
> * This project requires that you have an **Azure AI Foundry hub-based project with an Azure storage account** (not a Foundry project). For more information, *see* [How to create and manage an Azure AI Foundry hub](/azure/ai-foundry/how-to/create-azure-ai-resource.)
> * If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. For more information, see [How to use Azure AI services in the Azure AI Foundry portal](/azure/ai-services/connect-services-ai-foundry-portal).

## Prerequisites

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).
*  An [**Azure AI Language resource with a storage account and *Cognitive Services Contributor* access**](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics) role granted to your hub-based project. For more information, *see* [Configure Azure resources](../../../concepts/configure-azure-resources.md#option-1-configure-an-azure-ai-foundry-resource) 
* **An Azure AI Foundry hub-based project with Azure storage**. For more information about Foundry hub-based project, *see* [Create a hub project for Azure AI Foundry](/azure/ai-foundry/how-to/hub-create-projects).
* **A custom NER dataset uploaded to your storage container**. A custom named entity recognition (NER) dataset is the collection of labeled text documents used to train your custom NER model. You can [download our sample dataset](https://go.microsoft.com/fwlink/?linkid=2175226) for this quickstart. The source language is English.

## Step 1: Upload your dataset to your storage container

Let's begin by adding a container and uploading your dataset files directly to the root directory of your storage container. These documents are used to train your model.

1. Add a container to the storage account associated with your language resource. For more information, *see* [create a container](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container).

1. [Download the sample dataset](https://go.microsoft.com/fwlink/?linkid=2175226) from GitHub. The provided sample dataset contains 20 loan agreements:

    * Each agreement includes two parties: a lender and a borrower.
    * You extract relevant information for: both parties, agreement date, loan amount, and interest rate.

1. Open the .zip file, and extract the folder containing the documents.

1. Navigate to the Azure AI Foundry.

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, access your existing Azure AI Foundry hub-based project for this quickstart.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. Next choose the workspace blob storage that was set up for you as a connected resource.

1. On the workspace blob storage, select **View in Azure Portal**.


1. On the **AzurePortal** page for your blob storage, select **Upload** from the top menu. Next, choose the `.txt` and `.json` files you downloaded earlier. Finally, select the **Upload** button to add the file to your container.

    :::image type="content" source="../../media/foundry-next/upload-blob-files.png" alt-text="A screenshot showing the button for uploading files to the storage account.":::

## Step 2: Configure your language resource

Next, configure your language resource.

1. Navigate to the [Azure portal](https://azure.microsoft.com/#home)

1. Go to your **Azure AI Language resource** (select **All resources** to locate your resource).

1. Next, select **Access Control (IAM)** on the left panel, then select **Add role assignment**.

1. Search and select the **Storage Blob Data Owner** role from the **Add role assignment** list and then select **Next**.

1. Navigate to the Members tab and then select **User, group, or service principal**.

1. Choose **Select members**, then in the right panel, search for and choose your **Azure AI Language resource** (the one you're using for this project), and choose **Select**.

1. Finally, select **Review + assign** to confirm your selection.

## Step 3: Connect your Azure AI Language resource


Now, let's create a connection to your Azure AI Language resource so Azure AI Foundry can access it securely. This connection provides secure identity management and authentication, as well as controlled and isolated access to data.

1. Return to the [Azure AI Foundry](https://ai.azure.com/).

1. Access your existing Azure AI Foundry hub-based project for this quickstart.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. In the main  window, select the **+ New connection** button.

1. Select **Azure AI Language** from the **Add a connection to external assets** window.

1. Select **Add connection**, then select **Close.**

    :::image type="content" source="../../media/foundry-next/add-connection.png" alt-text="Screenshot of the connection window in Azure AI Foundry.":::

## Step 4: Fine tune your custom NER model

Now, we're ready to create a  custom NER fine-tune model.

1. From the **Project** section of the **Management center** menu, select **Go to project** .

1. From the **Overview** menu, select **Fine-tuning**.

1. From the main window, select **the AI Service fine-tuning** tab and then the **+ Fine-tune** button.

1. From the **Create service fine-tuning** window, choose the **Custom named entity recognition** tab, and then select **Next**.

    :::image type="content" source="../../media/foundry-next/create-fine-tuning.png" alt-text="Screenshot of the fine-tuning selection tile in Azure AI Foundry." lightbox="../../media/foundry-next/create-fine-tuning.png":::

1. In the **Create service fine-tuning task** window, complete the fields as follows:

  * **Connected service**. The name of your language service resource should already appear in this field by default. if not, add it from the drop-down menu.

  * **Name**. Give your fine-tuning task project a name.

  * **Language**. English is set as the default and already appears in the field.

  * **Description**. You can optionally provide a description or leave this field empty.

   * **Blob store container**. Select the workspace blob storage container from [Step 1](#step-1-upload-your-dataset-to-your-storage-container) and choose the **Connect** button.

1. Finally, select the  **Create** button. It can take a few minutes for the *creating* operation to complete.

That's it, congratulations!


## Create solutions with your data

After project creation, the next steps are as follows:

1. **Train your model**. Determine the specific test cases to use, then proceed to train your custom model with the selected data.
1. **Evaluate your model**. Review the analysis of your model performance evaluation data.
1. **Deploy your model**. Launch you model in a supported region.
1. **Test your in the Language playground**. The Language playground provides a sandbox to test and configure a deployed custom model before deploying it to production, all without writing code.


   :::image type="content" source="../../media/foundry-next/workflow.png" alt-text="Screenshot of fine-tuning workflow in Azure AI Foundry.":::


## Next Steps

> [!div class="nextstepaction"]
> [Learn how to use autolabeling](../../how-to/use-autolabeling.md)