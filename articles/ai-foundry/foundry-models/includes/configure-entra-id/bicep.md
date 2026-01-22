---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 01/22/2026
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

* Install the [Azure CLI](/cli/azure/)

* Identify the following information:

  * Your Azure subscription ID

## About this tutorial

The example in this article is based on code samples in the [Azure-Samples/azureai-model-inference-bicep](https://github.com/Azure-Samples/azureai-model-inference-bicep) repository. To run the commands locally without copying or pasting file content, clone the repository with these commands and go to the folder for your coding language:

```azurecli
git clone https://github.com/Azure-Samples/azureai-model-inference-bicep
```

The files for this example are in the following directory:

```azurecli
cd azureai-model-inference-bicep/infra
```

## Understand the resources

In this tutorial, you create the following resources:


* A Microsoft Foundry resource with key access disabled. For simplicity, this template doesn't deploy models.
* A role assignment for a given security principal with the role **Cognitive Services User**.

To create these resources, use the following assets:

1. Use the template `modules/ai-services-template.bicep` to describe your Foundry resource.

    __modules/ai-services-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-template.bicep":::

    > [!TIP]
    > This template accepts the `allowKeys` parameter. Set it to `false` to disable key access in the resource.

1. Use the template `modules/role-assignment-template.bicep` to describe a role assignment in Azure:

    __modules/role-assignment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/role-assignment-template.bicep":::

## Create the resources

In your console, follow these steps:

1. Define the main deployment:

    __deploy-entra-id.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/deploy-entra-id.bicep":::

1. Sign in to Azure:

    ```azurecli
    az login
    ```

1. Make sure you're in the right subscription:

    ```azurecli
    az account set --subscription "<subscription-id>"
    ```

1. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    SECURITY_PRINCIPAL_ID="<your-security-principal-id>"
    
    az deployment group create \
      --resource-group $RESOURCE_GROUP \
      --parameters securityPrincipalId=$SECURITY_PRINCIPAL_ID \
      --template-file deploy-entra-id.bicep
    ```

1. The template outputs the Foundry Models endpoint that you can use to consume any of the model deployments you created.

1. Verify the deployment and role assignment:

    ```azurecli
    # Get the endpoint from deployment output
    ENDPOINT=$(az deployment group show --resource-group $RESOURCE_GROUP --name deploy-entra-id --query properties.outputs.endpoint.value --output tsv)
    
    # Verify role assignment
    RESOURCE_ID=$(az deployment group show --resource-group $RESOURCE_GROUP --name deploy-entra-id --query properties.outputs.resourceId.value --output tsv)
    az role assignment list --scope $RESOURCE_ID --assignee $SECURITY_PRINCIPAL_ID --query "[?roleDefinitionName=='Cognitive Services User'].roleDefinitionName" --output tsv
    
    # Test authentication by getting an access token
    az account get-access-token --resource https://cognitiveservices.azure.com --query "accessToken" --output tsv
    ```

    If successful, you see **Cognitive Services User** from the role assignment check and an access token from the authentication test. You can now use this endpoint and Microsoft Entra ID authentication in your code.


## Use Microsoft Entra ID in your code

After you configure Microsoft Entra ID in your resource, update your code to use it when you consume the inference endpoint. The following example shows how to use a chat completions model.

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Disable key-based authentication in the resource

Disable key-based authentication when you implement Microsoft Entra ID and fully address compatibility or fallback concerns in all applications that consume the service. Change the `disableLocalAuth` property to disable key-based authentication.

For more information about how to disable local authentication when you're using a Bicep or ARM template, see [How to disable local authentication](../../../../ai-services/disable-local-auth.md#how-to-disable-local-authentication).

__modules/ai-services-template.bicep__

:::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-template.bicep" highlight="10-11,42":::
