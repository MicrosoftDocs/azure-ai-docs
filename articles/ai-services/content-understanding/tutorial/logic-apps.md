---
title: Create a Content Understanding Logic Apps workflow
titleSuffix: Foundry Tools
description: Learn how to build an Azure Logic Apps workflow that automatically processes documents with Azure Content Understanding in Foundry Tools.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 05/07/2026
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ai-usage: ai-assisted
---

# Tutorial: Create a Content Understanding Logic Apps workflow

Azure Logic Apps is a cloud-based platform that automates workflows without writing code. When combined with Azure Content Understanding in Foundry Tools, Logic Apps can automatically process documents—extracting structured fields from invoices, receipts, contracts, and other document types.

In this tutorial, you build a Logic Apps workflow that:

- Detects when a document is added to a OneDrive folder.
- Processes the document using the Content Understanding `prebuilt-invoice` analyzer.
- Sends the extracted invoice data to a specified email address.

## Prerequisites

To complete this tutorial, you need the following resources:

- An Azure subscription. You can [create a free Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- A free [OneDrive](https://onedrive.live.com/signup) or [OneDrive for Business](https://www.microsoft.com/microsoft-365/onedrive/onedrive-for-business) cloud storage account.

  > [!NOTE]
  > - OneDrive is intended for personal storage and requires a Microsoft or Outlook.com account.
  > - OneDrive for Business is part of Microsoft 365 and is designed for organizations.

- A free [Outlook online](https://signup.live.com/signup.aspx?lic=1) or [Office 365](https://www.microsoft.com/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook) email account.
- A sample invoice to test your Logic App. You can download the [sample invoice](https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf) from the Content Understanding samples repository.
- A Microsoft Foundry resource with Content Understanding configured. See [Create a Microsoft Foundry resource](../how-to/create-multi-service-resource.md) for setup instructions. You can use the free pricing tier (F0) to try the service, then upgrade to a paid tier for production.

  > [!TIP]
  > After your resource deploys, select **Go to resource**. Under **Resource Management**, select **Keys and Endpoint** and copy the key and endpoint values to a temporary location. You need these values to connect your Logic App to Content Understanding.

## Create a OneDrive folder

Before you create the Logic App, set up a OneDrive folder to use as the document trigger source.

1. Sign in to your [OneDrive](https://onedrive.live.com/) or [OneDrive for Business](https://www.microsoft.com/microsoft-365/onedrive/onedrive-for-business) home page.
1. Select the **➕ Add New** button in the upper-left sidebar and select **Folder**.
1. Enter a name for your new folder and select **Create**.
1. Confirm the new folder appears in your file list. You're done with OneDrive for now.

## Create a Logic App resource

1. Navigate to the [Azure portal](https://portal.azure.com/#home).
1. Select **➕ Create a resource** from the Azure home page.
1. Search for and select **Logic App**, then select **Create**.
1. Fill out the **Create Logic App** form with the following values:

   - **Subscription**: Select your current subscription.
   - **Resource group**: Select the same resource group as your Microsoft Foundry resource.
   - **Type**: Select **Consumption**. This type runs in global, multi-tenant Azure Logic Apps and uses the [Consumption billing model](https://learn.microsoft.com/azure/logic-apps/logic-apps-pricing#consumption-pricing).
   - **Logic App name**: Enter a descriptive name.
   - **Region**: Select your region.
   - **Enable log analytics**: Select **No** for this tutorial.

1. Select **Review + create**. After validation completes, select **Create**.
1. When deployment finishes, select **Go to resource**.
1. On the Logic Apps Designer page, select **Blank Logic App** from the **Templates** section to open the workflow canvas.

## Create an automation flow

1. In the Logic Apps Designer, search for **OneDrive** or **OneDrive for Business** in the connector search bar. Select the **When a file is created** trigger.

   > [!TIP]
   > If you use an Office 365 account, use the **OneDrive for Business** connector. The **OneDrive** connector requires a Microsoft or Outlook.com personal account.

1. When prompted, sign in to your OneDrive account.
1. After connecting, select the folder you created earlier. Leave the other default values in place.

   > [!NOTE]
   > The **When a file is created** trigger uses polling to detect new files. The default polling interval is 3 minutes, so there can be a delay of up to 3 minutes between uploading a file and the workflow starting. You can change the interval in the trigger settings.

1. Select the **➕ New step** button to add the next step.
1. In the **Choose an operation** search bar, enter **Content Understanding**. Select **Analyze Content** from the results.

   > [!NOTE]
   > The connector might appear as **Azure Content Understanding** in the search results.

1. In the connection dialog, enter the following values and select **Create**:

   - **Connection name**: Enter a memorable name for this connection.
   - **Endpoint URL**: Paste the endpoint URL from your Microsoft Foundry resource.
   - **API Key**: Paste the API key from your Microsoft Foundry resource.

   > [!NOTE]
   > If you're already signed in with saved credentials, this step is skipped automatically.

1. In the **Analyze content** action parameters, complete the following fields:

   - **Analyzer ID**: Enter `prebuilt-invoice` (or one of the other [prebuilt analyzers](../concepts/prebuilt-analyzers.md))to use the built-in invoice analyzer.
   - **File Content**: Select this field. In the dynamic content pop-up that appears, choose **File content**. This sends the OneDrive file to the Content Understanding analyzer for processing. When the **File content** badge appears in the field, this step is complete.
   - **Input File URL**: Leave this field empty, because you're supplying the file content directly from OneDrive.

1. Select **➕ New step** to add another action.
1. In the **Choose an operation** search bar, enter **Control** and select the **Control** tile.
1. Select **For each** from the Control action list.
1. In the **For each** step, select the **Select an output from previous steps** field. In the dynamic content pop-up, choose **contents**. This iterates over each analyzed document in the response.
1. Select **Add an action** from inside the **For each** step.
1. Search for **Outlook** and select **Outlook.com** (personal) or **Office 365 Outlook** (work). In the actions list, select **Send an email (V2)**.
1. Sign in to your Outlook account when prompted.
1. Complete the **Send an email (V2)** fields as follows. For each expression, select **Add dynamic content**, choose the **Expression** tab, and enter the expression in the **fx** box. For a complete list of available fields, see [Prebuilt analyzers](../concepts/prebuilt-analyzers.md).

   1. In the **To** field, enter your email address.

   1. In the **Subject** field, type `Invoice received from: ` and append the following expression:

      ```
      items('For_each')?['fields']?['VendorName']?['valueString']
      ```

   1. In the **Body** field, add the following invoice details:

      - Type `Invoice ID: ` and append:
        ```
        items('For_each')?['fields']?['InvoiceId']?['valueString']
        ```

      - On a new line, type `Invoice due date: ` and append:
        ```
        items('For_each')?['fields']?['DueDate']?['valueDate']
        ```

      - Type `Amount due: ` and append:
        ```
        items('For_each')?['fields']?['AmountDue']?['valueObject']?['Amount']?['valueNumber']
        ```

      - Type `Amount due (confidence): ` and append:
        ```
        items('For_each')?['fields']?['AmountDue']?['valueObject']?['Amount']?['confidence']
        ```

1. Select **Publish** in the upper-left corner to save and publish the workflow.

> [!NOTE]
> The **For each** loop is required around the **Send email** action to support response formats that might return more than one document result per file.

## Test the automation flow

Before testing, review what the workflow does:

- A **trigger** activates when a file is created in your OneDrive folder.
- A **Content Understanding action** analyzes the file using the `prebuilt-invoice` analyzer.
- An **Outlook action** emails extracted invoice data to the address you specified.

1. Open a new browser tab and navigate to your OneDrive folder. Upload the [sample invoice](https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf) file.
1. Return to the Logic App designer and select **Run trigger** > **Run**.
1. A notification in the upper-right corner confirms the trigger ran successfully.
1. Navigate to your Logic App overview page by selecting the app name link in the upper-left corner.
1. Check the run status to see whether the run succeeded or failed. Select the status indicator to view details for each step.
1. If a step failed, select it to review the error details and verify your connection credentials or expression values.
1. After a successful run, check your inbox. You receive an email with the invoice fields you configured.
1. When you finish testing, [disable or delete your Logic App](/azure/logic-apps/manage-logic-apps-with-azure-portal?tabs=consumption#disable-enable-logic-apps) to stop usage charges.


## Next steps

- [Explore prebuilt analyzers](../concepts/prebuilt-analyzers.md)
- [Build a robotic process automation solution](robotic-process-automation.md)
