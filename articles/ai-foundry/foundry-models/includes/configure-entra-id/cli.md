---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 12/15/2024
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]  

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Azure AI Foundry (formerly known Azure AI Services) resource name.

  * The resource group where the Azure AI Foundry (formerly known Azure AI Services) resource is deployed.


## Configure Microsoft Entra ID for inference

Follow these steps to configure Microsoft Entra ID for inference:


1. Log in into your Azure subscription:

    ```azurecli
    az login
    ```

2. If you have more than one subscription, select the subscription where your resource is located:

    ```azurecli
    az account set --subscription "<subscription-id>"
    ```

3. Set the following environment variables with the name of the Azure AI Foundry (formerly known Azure AI Services) resource you plan to use and resource group.

    ```azurecli
    ACCOUNT_NAME="<ai-services-resource-name>"
    RESOURCE_GROUP="<resource-group>"
    ```

4. Get the full name of your resource:

    ```azurecli
    RESOURCE_ID=$(az resource show -g $RESOURCE_GROUP -n $ACCOUNT_NAME --resource-type "Microsoft.CognitiveServices/accounts")
    ```

5. Get the object ID of the security principal you want to assign permissions to. The following example shows how to get the object ID associated with:
    
    __Your own logged in account:__

    ```azurecli
    OBJECT_ID=$(az ad signed-in-user show --query id --output tsv)
    ```

    __A security group:__

    ```azurecli
    OBJECT_ID=$(az ad group show --group "<group-name>" --query id --output tsv)
    ```

    __A service principal:__

    ```azurecli
    OBJECT_ID=$(az ad sp show --id "<service-principal-guid>" --query id --output tsv)
    ```
    
6. Assign the **Cognitive Services User** role to the service principal (scoped to the resource). By assigning a role, you're granting service principal access to this resource.

    ```azurecli
    az role assignment create --assignee-object-id $OBJECT_ID --role "Cognitive Services User" --scope $RESOURCE_ID
    ```

8.  The selected user can now use Microsoft Entra ID for inference.

    > [!TIP]
    > Keep in mind that Azure role assignments may take up to five minutes to propagate. Adding or removing users from a security group propagates immediately.


## Use Microsoft Entra ID in your code

Once Microsoft Entra ID is configured in your resource, you need to update your code to use it when consuming the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Troubleshooting

[!INCLUDE [troubleshooting](troubleshooting.md)]
