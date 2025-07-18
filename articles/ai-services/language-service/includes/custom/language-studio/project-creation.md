---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---

1. Sign into the [Language Studio](https://aka.ms/languageStudio). A window will appear to let you select your subscription and Language resource. Select the Language resource you created in the above step. 

2. Under the sections at the top of the page, section of Language Studio, find this service and select the box that represents it.

    :::image type="content" source="../../../media/custom/language-studio/select-custom-service.png" alt-text="A screenshot showing the location of services in the Language Studio landing page."../../../media/custom/language-studio/select-custom-service.png":::

3. Select **Create new project** from the top menu in your projects page. Creating a project will let you tag data, train, evaluate, improve, and deploy your models. 

    :::image type="content" source="/../../../media/custom/language-studio/create-project.png" alt-text="A screenshot of the project creation page." lightbox="/../../../media/custom/language-studio/create-project.png":::

4.  After you click, **Create new project**, a window will appear to let you connect your storage account. If you've already connected a storage account, you will see the storage accounted connected. If not, choose your storage account from the dropdown that appears and select **Connect storage account**; this will set the required roles for your storage account. This step will possibly return an error if you are not assigned as **owner** on the storage account.

    >[!NOTE]
    > * You only need to do this step once for each new resource you use. 
    > * This process is irreversible, if you connect a storage account to your Language resource you cannot disconnect it later.
    > * You can only connect your Language resource to one storage account.
    
    :::image type="content" source="../../../media/custom/language-studio/connect-storage.png" alt-text="A screenshot showing the storage connection screen." lightbox="../../../media/custom/language-studio/connect-storage.png":::

5. Enter the project information, including a name, description, and the language of the files in your project. for example, **English**. You won’t be able to change the name of your project later. Select **Next**

    > [!TIP]
    > Your dataset doesn't have to be entirely in the same language. You can have multiple documents, each with different supported languages. If your dataset contains documents of different languages or if you expect text from different languages during runtime, select **enable multi-lingual dataset** option when you enter the basic information for your project. This option can be enabled later from the **Project settings** page.

6. Select the container where you have uploaded your dataset. 
If you have already labeled data make sure it follows the supported format and select the relevant data format confirmation, then select the labels file from the drop-down menu. Select **Next**.

7. Review the data you entered and select **Create Project**.
