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

  * Your Microsoft Foundry resource name

  * The resource group where you deployed the Foundry resource


## Configure Microsoft Entra ID for inference

To configure Microsoft Entra ID for inference, follow these steps:


1. Sign in to your Azure subscription.

    ```azurecli
    # Authenticate with Azure and sign in interactively
    az login
    ```

1. If you have more than one subscription, select the subscription where your resource is located.

    ```azurecli
    # Set the active subscription context
    az account set --subscription "<subscription-id>"
    ```

1. Set the following environment variables with the name of the resource and resource group you plan to use.

    ```azurecli
    # Store resource identifiers for reuse in subsequent commands
    ACCOUNT_NAME="<ai-services-resource-name>"
    RESOURCE_GROUP="<resource-group>"
    ```

1. Get the full name of your resource.

    ```azurecli
    # Retrieve the full Azure Resource Manager ID for role assignment scoping
    RESOURCE_ID=$(az resource show -g $RESOURCE_GROUP -n $ACCOUNT_NAME --resource-type "Microsoft.CognitiveServices/accounts" --query id --output tsv)
    ```

1. Get the object ID of the security principal you want to assign permissions to. The following examples show how to get the object ID associated with:
    
    **Your own signed in account:**

    ```azurecli
    # Get your user's Microsoft Entra ID object ID
    OBJECT_ID=$(az ad signed-in-user show --query id --output tsv)
    ```

    **A security group:**

    ```azurecli
    # Get the object ID for a security group (recommended for production)
    OBJECT_ID=$(az ad group show --group "<group-name>" --query id --output tsv)
    ```

    **A service principal:**

    ```azurecli
    # Get the object ID for a service principal (for app authentication)
    OBJECT_ID=$(az ad sp show --id "<service-principal-guid>" --query id --output tsv)
    ```
    
1. Assign the **Cognitive Services User** role to the service principal (scoped to the resource). By assigning a role, you grant the service principal access to this resource.

    ```azurecli
    # Grant inference access by assigning the Cognitive Services User role
    az role assignment create --assignee-object-id $OBJECT_ID --role "Cognitive Services User" --scope $RESOURCE_ID
    ```

1. The selected user can now use Microsoft Entra ID for inference.

    > [!TIP]
    > Keep in mind that Azure role assignments can take up to five minutes to propagate. Adding or removing users from a security group propagates immediately.

1. Verify the role assignment:

    ```azurecli
    az role assignment list --scope $RESOURCE_ID --assignee $OBJECT_ID --query "[?roleDefinitionName=='Cognitive Services User'].{principalName:principalName, roleDefinitionName:roleDefinitionName}" --output table
    ```

    The output should show the **Cognitive Services User** role assigned to your principal.


## Use Microsoft Entra ID in your code

After you configure Microsoft Entra ID in your resource, update your code to use it when you consume the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Disable key-based authentication in the resource

Disable key-based authentication when you implement Microsoft Entra ID and fully address compatibility or fallback concerns in all the applications that consume the service. 
Use PowerShell with the Azure CLI to disable local authentication for an individual resource. First sign in with the `Connect-AzAccount` command. Then use the `Set-AzCognitiveServicesAccount` cmdlet with the parameter `-DisableLocalAuth $true`, like the following example:

```powershell
Set-AzCognitiveServicesAccount -ResourceGroupName "my-resource-group" -Name "my-resource-name" -DisableLocalAuth $true
```

For more information about how to use the Azure CLI to disable or reenable local authentication and verify authentication status, see [Disable local authentication in Foundry Tools](../../../../ai-services/disable-local-auth.md).
