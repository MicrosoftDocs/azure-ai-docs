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

## About this tutorial

The example in this article is based on code samples contained in the [Azure-Samples/azureai-model-inference-bicep](https://github.com/Azure-Samples/azureai-model-inference-bicep) repository. To run the commands locally without having to copy or paste file content, use the following commands to clone the repository and go to the folder for your coding language:

```azurecli
git clone https://github.com/Azure-Samples/azureai-model-inference-bicep
```

The files for this example are in:

```azurecli
cd azureai-model-inference-bicep/infra
```

## Understand the resources

The tutorial helps you create:

> [!div class="checklist"]
> * An Azure AI Foundry (formerly known Azure AI Services) resource with key access disabled. For simplicity, this template doesn't deploy models.
> * A role-assignment for a given security principal with the role **Cognitive Services User**.

You are using the following assets to create those resources:

1. Use the template `modules/ai-services-template.bicep` to describe your Azure AI Foundry (formerly known Azure AI Services) resource:

    __modules/ai-services-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-template.bicep":::

    > [!TIP]
    > Notice that this template can take the parameter `allowKeys` which, when `false` will disable the use of keys in the resource. This configuration is optional.

2. Use the template `modules/role-assignment-template.bicep` to describe a role assignment in Azure:

    __modules/role-assignment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/role-assignment-template.bicep":::

## Create the resources

In your console, follow these steps:

1. Define the main deployment:

    __deploy-entra-id.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/deploy-entra-id.bicep":::

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
    SECURITY_PRINCIPAL_ID="<your-security-principal-id>"
    
    az deployment group create \
      --resource-group $RESOURCE_GROUP \
      --securityPrincipalId $SECURITY_PRINCIPAL_ID
      --template-file deploy-entra-id.bicep
    ```

7. The template outputs the Azure AI Foundry Models endpoint that you can use to consume any of the model deployments you have created.


## Use Microsoft Entra ID in your code

Once you configured Microsoft Entra ID in your resource, you need to update your code to use it when consuming the inference endpoint. The following example shows how to use a chat completions model:

[!INCLUDE [code](../code-create-chat-client-entra.md)]

[!INCLUDE [about-credentials](about-credentials.md)]

## Troubleshooting

[!INCLUDE [troubleshooting](troubleshooting.md)]

## Disable key-based authentication in the resource

Disabling key-based authentication is advisable when you implemented Microsoft Entra ID and fully addressed compatibility or fallback concerns in all the applications that consume the service. You can achieve it by changing the property `disableLocalAuth`:

__modules/ai-services-template.bicep__

:::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-template.bicep" highlight="10-11,42":::
