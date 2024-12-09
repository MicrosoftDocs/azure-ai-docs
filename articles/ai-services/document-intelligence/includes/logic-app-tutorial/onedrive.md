---
author: laujan
ms.service: azure-ai-document-intelligence
ms.topic: include
ms.date: 07/24/2023
ms.author: lajanuar
monikerRange: '<=doc-intel-4.0.0'
---

<!-- markdownlint-disable MD041 -->
<!-- markdownlint-disable MD029 -->

## Prerequisites

To complete this tutorial, you need the following resources:

* **An Azure subscription**. You can [create a free Azure subscription](https://azure.microsoft.com/free/cognitive-services/)

* A free [**OneDrive**](https://onedrive.live.com/signup) or [**OneDrive for Business**](https://www.microsoft.com/microsoft-365/onedrive/onedrive-for-business) cloud storage account.

    > [!NOTE]
    >
    > * OneDrive is intended for personal storage.
    > * OneDrive for Business is part of Office 365 and is designed for organizations. It provides cloud storage where you can store, share, and sync all work files.
    >

* A free [**Outlook online**](https://signup.live.com/signup.aspx?lic=1&mkt=en-ca) or [**Office 365**](https://www.microsoft.com/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook) email account**.

* **A sample invoice to test your Logic App**. You can download and use our [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/invoice-logic-apps-tutorial.pdf) for this tutorial.

* **A Document Intelligence resource**.  Once you have your Azure subscription, [create a Document Intelligence resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal to get your key and endpoint. If you have an existing Document Intelligence resource, navigate directly to your resource page. You can use the free pricing tier (F0) to try the service, and upgrade later to a paid tier for production.

  * After the resource deploys, select **Go to resource**. Copy the **Keys and Endpoint** values from your resource in the Azure portal and paste them in a convenient location, such as *Microsoft Notepad*. You need the key and endpoint values to connect your application to the Document Intelligence API. For more information, *see* [**create a Document Intelligence resource**](../../how-to-guides/create-document-intelligence-resource.md).

      :::image border="true" type="content" source="../../media/containers/keys-and-endpoint.png" alt-text="Screenshot showing how to access resource key and endpoint URL.":::

## Create a OneDrive folder

Before we jump into creating the Logic App, we have to set up a OneDrive folder.

1. Sign in to your [OneDrive](https://onedrive.live.com/) or [**OneDrive for Business**](https://www.microsoft.com/microsoft-365/onedrive/onedrive-for-business) home page.

1. Select the **➕ Add New** button in the upper-left corner sidebar and select **Folder**.

    :::image type="content" source="../../media/logic-apps-tutorial/add-new-folder.png" alt-text="Screenshot of add-new button.":::

1. Enter a name for your new folder and select **Create**.

    :::image type="content" source="../../media/logic-apps-tutorial/create-folder.png" alt-text="Screenshot of create and name folder window.":::

1. You see the new folder in your files.

    :::image type="content" source="../../media/logic-apps-tutorial/new-folder.png" alt-text="Screenshot of the new folder.":::

1. We're done with OneDrive for now.

## Create a Logic App resource

At this point, you should have a Document Intelligence resource and a OneDrive folder all set. Now, it's time to create a Logic App resource.

1. Navigate to the [Azure portal](https://ms.portal.azure.com/#home).

1. Select **➕ Create a resource** from the Azure home page.

    :::image type="content" source="../../media/logic-apps-tutorial/azure-create-resource.png" alt-text="Screenshot of create a resource in the Azure portal.":::

1. Search for and choose **Logic App** from the search bar.

1. Select the create button

    :::image type="content" source="../../media/logic-apps-tutorial/create-logic-app.png" alt-text="Screenshot of the Create Logic App page.":::

1. Next, you're going to fill out the **Create Logic App** fields with the following values:

   * **Subscription**. Select your current subscription.
   * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. Choose the same resource group you have for your Document Intelligence resource.
   * **Type**. Select **Consumption**. The Consumption resource type runs in global, multi-tenant Azure Logic Apps and uses the [Consumption billing model](/azure/logic-apps/logic-apps-pricing#consumption-pricing).
   * **Logic App name**. Enter a name for your resource. We recommend using a descriptive name, for example *YourNameLogicApp*.
   * **Publish**. Select **Workflow**.
   * **Region**. Select your local region.
   * **Enable log analytics**. For this project, select **No**.
   * **Plan Type**. Select **Consumption**. The Consumption resource type runs in global, multi-tenant Azure Logic Apps and uses the [Consumption billing model](/azure/logic-apps/logic-apps-pricing#consumption-pricing).
   * **Zone Redundancy**. Select **disabled**.

1. When you're done, you have something similar to the following image (Resource group, Logic App name, and Region may be different). After checking these values, select **Review + create** in the bottom-left corner.

    :::image border="true" type="content" source="../../media/logic-apps-tutorial/create-logic-app-fields.png" alt-text="Screenshot showing field values to create a Logic App resource.":::

1. A short validation check runs. After it completes successfully, select **Create** in the bottom-left corner.

1. Next, you're redirected to a screen that says **Deployment in progress**. Give Azure some time to deploy; it can take a few minutes. After the deployment is complete, you see a banner that says, **Your deployment is complete**. When you reach this screen, select **Go to resource**.

1. Finally, you're redirected to the **Logic Apps Designer** page. There's a short video for a quick introduction to Logic Apps available on the home screen. When you're ready to begin designing your Logic App, select the **Blank Logic App** button from the **Templates** section.

    :::image border="true" type="content" source="../../media/logic-apps-tutorial/logic-app-designer-templates.png" alt-text="Screenshot showing how to enter the Logic App Designer.":::

1. You see a screen that looks similar to the following image. Now, you're ready to start designing and implementing your Logic App.

    :::image border="true" type="content" source="../../media/logic-apps-tutorial/logic-app-designer.png" alt-text="Screenshot of the Logic App Designer start page.":::

## Create an automation flow

Now that you have the Logic App connector resource set up and configured, let's create the automation flow and test it out!

1. Search for and select **OneDrive** or **OneDrive for Business** in the search bar. Then, select the **When a file is created** trigger.

    :::image type="content" source="../../media/logic-apps-tutorial/one-drive-setup.png" alt-text="Screenshot of the OneDrive connector and trigger selection page.":::

1. Next, a pop-up window appears, prompting you to log into your OneDrive account. Select **Sign in** and follow the prompts to connect your account.

    > [!TIP]
    > If you try to sign into the OneDrive connector using an Office 365 account, you may receive the following error: ***Sorry, we can't sign you in here with your @MICROSOFT.COM account.***
    >
    > * This error happens because OneDrive is a cloud-based storage for personal use that can be accessed with an Outlook.com or Microsoft Live account not with Office 365 account.
    > * You can use the OneDrive for Business connector if you want to use an Office 365 account. Make sure that you have [created a OneDrive Folder](#create-a-onedrive-folder) for this project in your OneDrive for Business account.

1. After your account is connected, select the folder you created earlier in your **OneDrive** or **OneDrive for Business** account. Leave the other default values in place.

    :::image type="content" source="../../media/logic-apps-tutorial/when-file-created.png" alt-text="Screenshot of the When a file is created window.":::

 :::moniker range=">=doc-intel-3.0.0"

4. Next, we're going to add a new step to the workflow. Select the **➕ New step** button underneath the newly created OneDrive node.

    :::image type="content" source="../../media/logic-apps-tutorial/one-drive-trigger-setup.png" alt-text="Screenshot of the OneDrive trigger setup.":::

1. A new node is added to the Logic App designer view. Search for **Form Recognizer** (Document Intelligence forthcoming) in the **Choose an operation** search bar and select **Analyze Document for Prebuilt or Custom models (v3.0 API)** from the list.

    :::image type="content" source="../../media/logic-apps-tutorial/analyze-prebuilt-document-action.png" alt-text="Screenshot of the Analyze Document for Prebuilt or Custom models (v3.0 API) selection button.":::

1. Now, you see a window to create your connection. Specifically, you're going to connect your Document Intelligence resource to the Logic Apps Designer Studio:

    * Enter a **Connection name**. It should be something easy to remember.
    * Enter the Document Intelligence resource **Endpoint URL** and **Account Key** that you copied previously. If you skipped this step earlier or lost the strings, you can navigate back to your Document Intelligence resource and copy them again. When you're done, select **Create**.

      :::image type="content" source="../../media/logic-apps-tutorial/create-logic-app-connector.png" alt-text="Screenshot of the logic app connector dialog window":::

    > [!NOTE]
    > If you already logged in with your credentials, the prior step is skipped.

1. Next, you see the selection parameters window for the **Analyze Document for Prebuilt or Custom Models (v3.0 API)** connector.

      :::image type="content" source="../../media/logic-apps-tutorial/prebuilt-model-select-window.png" alt-text="Screenshot of the prebuilt model selection window.":::

1. Complete the fields as follows:

    * **Model Identifier**.  Specify which model you want to call, in this case we're calling the prebuilt invoice model, so enter **prebuilt-invoice**.
    * **Document/Image File Content**. Select this field. A dynamic content pop-up appears. If it doesn't, select the **Add dynamic content** button below the field and choose **File content**. This step is essentially sending the file(s) to be analyzed to the Document Intelligence prebuilt-invoice model. Once you see the **File content** badge show in the **Document /Image file content** field, you've completed this step correctly.
    * **Document/Image URL**. Skip this field for this project because we're already pointing to the file content directly from the OneDrive folder.
    * **Add new parameter**. Skip this field for this project.

      :::image type="content" source="../../media/logic-apps-tutorial/add-file-content.png" alt-text="Screenshot of add file content window.":::

1. We need to add a few more steps. Once again, select the **➕ New step** button to add another action.

1. In the **Choose an operation** search bar, enter *Control* and select the **Control** tile.

    :::image type="content" source="../../media/logic-apps-tutorial/select-control-tile.png" alt-text="Screenshot of the control tile from the Choose an Operation menu.":::

1. Scroll down and select the **For each Control** tile from the **Control** list.

    :::image type="content" source="../../media/logic-apps-tutorial/for-each-tile.png" alt-text="Screenshot of the For Each Control tile from the Control menu. ":::

1. In the **For each** step window, there's a field labeled **Select an output from previous steps**. Select this field. A dynamic content pop-up appears. If it doesn't, select the **Add dynamic content** button below the field and choose **documents**.

    :::image type="content" source="../../media/logic-apps-tutorial/dynamic-content-documents.png" alt-text="Screenshot of the dynamic content list.":::

1. Now, select **Add an Action** from within the **For each** step window.

1. In the **Choose an operation** search bar, enter *Outlook* and select **Outlook.com** (personal) or **Office 365 Outlook** (work).

1. In the actions list, scroll down until you find **Send an email (V2)** and select this action.

    :::image type="content" source="../../media/logic-apps-tutorial/send-email.png" alt-text="Screenshot of Send an email (V2) action button.":::

1. Just like with OneDrive, you're asked to sign into your Outlook or Office 365 Outlook account. After you sign in, you see a window where we're going to format the email with dynamic content that Document Intelligence extracts from the invoice.

1. We're going to use the following expression to complete some of the fields:

```powerappsfl
     
       items('For_each')?['fields']?['FIELD-NAME']?['content']
```

1. In order to access a specific field, we select the **add the dynamic content** button and select the **Expression** tab.

    :::image type="content" source="../../media/logic-apps-tutorial/function-expression-field.png" alt-text="Screenshot of the expression function field.":::

1. In  the **ƒx** box, copy and paste the above formula and replace **FIELD-NAME** with the name of the field we want to extract. For the full list of available fields, refer to the concept page for the given API. In this case, we use the [prebuilt-invoice model field extraction values](../../prebuilt/invoice.md#field-extraction).

1. We're almost done! Make the following changes to the following fields:

    * **To**. Enter your personal or business email address or any other email address you have access to.

    * **Subject**. Enter ***Invoice received from:*** and then add the following expression:

     ```powerappsfl
    
              items('For_each')?['fields']?['VendorName']?['content']
     ```

    * **Body**. We're going to add specific information about the invoice:

      * Type ***Invoice ID:*** and, using the same method as before, append the following expression:

       ```powerappsfl
     
              items('For_each')?['fields']?['InvoiceId']?['content']
       ```

      * On a new line type ***Invoice due date:*** and append the following expression:

      ```powerappsfl
     
               items('For_each')?['fields']?['DueDate']?['content']
      ```

      * Type ***Amount due:*** and append the following expression:

      ```powerappsfl
     
               items('For_each')?['fields']?['AmountDue']?['content']
      ```

      * Lastly, because the amount due is an important number, we also want to send the confidence score for this extraction in the email. To do this type ***Amount due (confidence):***  and append the following expression:

      ```powerappsfl
     
               items('For_each')?['fields']?['AmountDue']?['confidence']
      ```

    * When you're done, the window looks similar to the following image:

      :::image type="content" source="../../media/logic-apps-tutorial/send-email-functions.png" alt-text="Screenshot of the Send an email (V2) window with completed fields.":::

1. **Select Save in the upper left corner**.

    :::image type="content" source="../../media/logic-apps-tutorial/logic-app-designer-save.png" alt-text="Screenshot of the Logic Apps Designer save button.":::

> [!NOTE]
>
> * This current version only returns a single invoice per PDF.
> * The "For each loop" is required around the send email action to enable an output format that may return more than one invoice from PDFs in the future.

:::moniker-end

 :::moniker range="doc-intel-2.1.0"

4. Next, we're going to add a new step to the workflow. Select the **➕ New step** button underneath the newly created OneDrive node.

1. A new node is added to the Logic App designer view. Search for "Form Recognizer (Document Intelligence forthcoming)" in the **Choose an operation** search bar and select **Analyze Invoice** from the list.

    :::image type="content" source="../../media/logic-apps-tutorial/analyze-invoice-v-2.png" alt-text="Screenshot of Analyze Invoice action.":::

1. Now, you see a window where you can create your connection. Specifically, you're going to connect your Form Recognizer resource to the Logic Apps Designer Studio:

    * Enter a **Connection name**. It should be something easy to remember.
    * Enter the Form Recognizer resource **Endpoint URL** and **Account Key** that you copied previously. If you skipped this step earlier or lost the strings, you can navigate back to your Form Recognizer resource and copy them again. When you're done, select **Create**.

    :::image type="content" source="../../media/logic-apps-tutorial/create-logic-app-connector.png" alt-text="Screenshot of the logic app connector dialog window.":::

    > [!NOTE]
    > If you already logged in with your credentials, the prior step is skipped.
    > Continue by completing the **Analyze Invoice** parameters.

1. Next, you see the selection parameters window for the **Analyze Invoice** connector.

    :::image type="content" source="../../media/logic-apps-tutorial/analyze-invoice-parameters.png" alt-text="Screenshot showing the analyze invoice window fields.":::

1. Complete the fields as follows:

    * **Document/Image File Content**. Select this field. A dynamic content pop-up appears. If it doesn't, select the **Add dynamic content** button below the field and choose **File content**. This step is essentially sending the file(s) to be analyzed to the Document Intelligence prebuilt-invoice model. Once you see the **File content** badge show in the **Document /Image file content** field, you've completed this step correctly.
    * **Document/Image URL**. Skip this field for this project because we're already pointing to the file content directly from the OneDrive folder.
    * **Include Text Details**. Select **Yes**.
    * **Add new parameter**. Skip this field for this project.

1. We need to add the last step. Once again, select the **➕ New step** button to add another action.

1. In the **Choose an operation** search bar, enter *Outlook* and select **Outlook.com** (personal) or **Office 365 Outlook** (work).

1. In the actions list, scroll down until you find **Send an email (V2)** and select this action.

1. Sign into your **Outlook** or **Office 365 Outlook** account. After doing so, you see a window where we're going to format the email to be sent with dynamic content extracted from the invoice.

    :::image type="content" source="../../media/logic-apps-tutorial/send-email.png" alt-text="Screenshot of Send an email (V2) action button.":::

1. We're almost done! Type the following entries in the fields:

    * **To**. Enter your personal or business email address or any other email address you have access to.

    * **Subject**. Enter ***Invoice received from:*** and then append dynamic content **Vendor name field Vendor name**.

    * **Body**. We're going to add specific information about the invoice:

      * Type ***Invoice ID:*** and append the dynamic content **Invoice ID field Invoice ID**.

      * On a new line type ***Invoice due date:*** and append the dynamic content **Invoice date field invoice date (date)**.

      * Type ***Amount due:*** and append the dynamic content **Amount due field Amount due (number)**.

      * Lastly, because the amount due is an important number we also want to send the confidence score for this extraction in the email. To do this type ***Amount due (confidence):***  and add the dynamic content **Amount due field confidence of amount due**. When you're done, the window looks similar to the following image.

      :::image border="true" type="content" source="../../media/logic-apps-tutorial/send-email-fields-complete.png" alt-text="Screenshot of the completed Outlook fields.":::

      > [!TIP]
      > If you don't see the dynamic content display automatically, use the **Search dynamic content** bar to find field entries.

1. **Select Save in the upper left corner**.

     :::image type="content" source="../../media/logic-apps-tutorial/logic-app-designer-save.png" alt-text="Screenshot of the Logic Apps Designer save button.":::

    > [!NOTE]
    >
    > * This current version only returns a single invoice per PDF.
    > * The "For each loop" around the send email action enables an output format that may return more than one invoice from PDFs in the future.

:::moniker-end
