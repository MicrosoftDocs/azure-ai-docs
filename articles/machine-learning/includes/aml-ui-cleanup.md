---
title: "include file"
description: "include file"
services: machine-learning
ms.service: azure-machine-learning
ms.topic: "include"
author: sgilley
ms.author: scottpolly
ms.date: 11/06/2019
ms.custom:
  - include file
  - sfi-image-nochange
---

>[!IMPORTANT]
>You can use the resources that you created as prerequisites for other Azure Machine Learning tutorials and how-to articles.

### Delete everything

If you don't plan to use anything that you created, delete the entire resource group so you don't incur any charges.

1. In the [Azure portal](https://portal.azure.com), select **Resource groups** under **Azure services**.
 
1. Select the resource group that you created.

1. Select **Delete resource group**.

   :::image type="content" source="./media/aml-ui-cleanup/delete-resources.png" alt-text="Screenshot that shows the button to delete resource group in the Azure portal.":::

Deleting the resource group also deletes all resources that you created in the designer.

### Delete individual assets

In the designer where you created your experiment, delete individual assets by selecting them and then selecting the **Delete** button.

The compute target that you created here *automatically autoscales* to zero nodes when it's not being used. This action is taken to minimize charges. If you want to delete the compute target, take these steps:

:::image type="content" source="./media/aml-ui-cleanup/delete-asset.png" alt-text="Screenshot that shows how to delete assets.":::

To delete a dataset, go to the storage account by using the Azure portal or Azure Storage Explorer and manually delete those assets.
