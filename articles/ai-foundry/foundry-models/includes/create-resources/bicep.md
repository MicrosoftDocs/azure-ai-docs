---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

## About this tutorial

The example in this article is based on code samples contained in the [Azure-Samples/azureai-model-inference-bicep](https://github.com/Azure-Samples/azureai-model-inference-bicep) repository. To run the commands locally without having to copy or paste file content, use the following commands to clone the repository and go to the folder for your coding language:

```azurecli
git clone https://github.com/Azure-Samples/azureai-model-inference-bicep
```

The files for this example are in:

```azurecli
cd azureai-model-inference-bicep/infra
```

[!INCLUDE [marketplace-rbac](../configure-marketplace/rbac.md)]

## Create the resources

Follow these steps:

1. Use the template `modules/ai-services-template.bicep` to describe your Foundry Tools resource:

    __modules/ai-services-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-template.bicep":::

2. Use the template `modules/ai-services-deployment-template.bicep` to describe model deployments:

    __modules/ai-services-deployment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-deployment-template.bicep":::

3. For convenience, we define the model we want to have available in the service using a JSON file. The file [__infra/models.json__](https://github.com/Azure-Samples/azureai-model-inference-bicep/blob/main/infra/models.json) contains a list of JSON object with keys `name`,`version`, `provider`, and `sku`, which defines the models the deployment will provision. Since the models support serverless API deployments, adding model deployments doesn't incur on extra cost. Modify the file by **removing/adding the model entries you want to have available**. The following example **shows only the first 7 lines** of the JSON file:

    __models.json__

    :::code language="json" source="~/azureai-model-inference-bicep/infra/models.json" range="1-7":::

4. If you plan to use projects (recommended), you need the templates for creating a project, hub, and a connection to the Foundry Tools resource:

    __modules/project-hub-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/project-hub-template.bicep":::

    __modules/ai-services-connection-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-connection-template.bicep":::

1. Define the main deployment:

    __deploy-with-project.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/deploy-with-project.bicep":::

2. Log into Azure:

    ```azurecli
    az login
    ```

3. Ensure you are in the right subscription:

    ```azurecli
    az account set --subscription "<subscription-id>"
    ```

4. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    
    az deployment group create \
      --resource-group $RESOURCE_GROUP \
      --template-file deploy-with-project.bicep
    ```

5. If you want to deploy only the Foundry Tools resource and the model deployments, use the following deployment file:

    __deploy.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/deploy.bicep":::

6. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    
    az deployment group create \
      --resource-group $RESOURCE_GROUP \
      --template-file deploy.bicep
    ```

7. The template outputs the Microsoft Foundry Models endpoint that you can use to consume any of the model deployments you have created.

## Next steps

> [!div class="nextstepaction"]
> [Use the inference endpoint](../../how-to/inference.md)
