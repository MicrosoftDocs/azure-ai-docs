---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/26/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]  

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Microsoft Foundry resource (formerly known as Azure AI Services resource) name.

  * The resource group where you deployed the Foundry resource.


## Configure Microsoft Entra ID for inference

Follow these steps to configure Microsoft Entra ID for inference:


1. Sign in to your Azure subscription.

    ```azurecli
    az login
    ```

1. If you have more than one subscription, select the subscription where your resource is located.

    ```azurecli
    az account set --subscription "<subscription-id>"
    ```

1. Set the following environment variables with the name of the Foundry resource you plan to use and resource group.

    ```azurecli
    ACCOUNT_NAME="<ai-services-resource-name>"
    RESOURCE_GROUP="<resource-group>"
    ```

1. Get the full name of your resource.

    ```azurecli
    RESOURCE_ID=$(az resource show -g $RESOURCE_GROUP -n $ACCOUNT_NAME --resource-type "Microsoft.CognitiveServices/accounts" --query id --output tsv)
    ```

1. Get the object ID of the security principal you want to assign permissions to. The following example shows how to get the object ID associated with:
    
    **Your own signed in account:**

    ```azurecli
    OBJECT_ID=$(az ad signed-in-user show --query id --output tsv)
    ```

    **A security group:**

    ```azurecli
    OBJECT_ID=$(az ad group show --group "<group-name>" --query id --output tsv)
    ```

    **A service principal:**

    ```azurecli
    OBJECT_ID=$(az ad sp show --id "<service-principal-guid>" --query id --output tsv)
    ```
    
1. Assign the **Cognitive Services User** role to the service principal (scoped to the resource). By assigning a role, you grant the service principal access to this resource.

    ```azurecli
    az role assignment create --assignee-object-id $OBJECT_ID --role "Cognitive Services User" --scope $RESOURCE_ID
    ```

1. The selected user can now use Microsoft Entra ID for inference.

    > [!TIP]
    > Keep in mind that Azure role assignments can take up to five minutes to propagate. Adding or removing users from a security group propagates immediately.


## Use Microsoft Entra ID in your code

After you configure Microsoft Entra ID in your resource, update your code to use it when consuming the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Troubleshooting

[!INCLUDE [troubleshooting](troubleshooting.md)]
