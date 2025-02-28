---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Azure AI Services resource name.

  * The resource group where the Azure AI Services resource is deployed.

  * The model name, provider, version, and SKU you would like to deploy. You can use the Azure AI Foundry portal or the Azure CLI to identify it. In this example we deploy the following model:

    * **Model name:**: `Phi-3.5-vision-instruct`
    * **Provider**: `Microsoft`
    * **Version**: `2`
    * **Deployment type**: Global standard

## Add a model deployment with custom content filtering

1. Use the template `ai-services-content-filter-template.bicep` to describe the content filter policy:

    __ai-services-content-filter-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-content-filter-template.bicep":::

2. Use the template `ai-services-deployment-template.bicep` to describe model deployments:

    __ai-services-deployment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-deployment-template.bicep":::

3. Create the main deployment definition:

    __main.bicep__

    ```bicep
    param accountName string
    param modelName string
    param modelVersion string
    param modelPublisherFormat string
    param contentFilterPolicyName string

    module raiPolicy 'ai-services-content-filter-template.bicep' = {
      name: 'raiPolicy'
      scope: resourceGroup(resourceGroupName)
      params: {
        accountName: accountName
        policyName: contentFilterPolicyName
      }
    }

    module modelDeployment 'ai-services-deployment-template.bicep' = {
        name: 'modelDeployment'
        scope: resourceGroup(resourceGroupName)
        params: {
            accountName: accountName
            modelName: modelName
            modelVersion: modelVersion
            modelPublisherFormat: modelPublisherFormat
            contentFilterPolicyName: contentFilterPolicyName
        }
        dependsOn: [
            raiPolicy
        ]
    }
    ```

4. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    ACCOUNT_NAME="<azure-ai-model-inference-name>" 
    MODEL_NAME="Phi-3.5-vision-instruct"
    PROVIDER="Microsoft"
    VERSION=2
    RAI_POLICY_NAME="custom-policy"
    
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file main.bicep \
        --parameters accountName=$ACCOUNT_NAME raiPolicyName=$RAI_POLICY_NAME modelName=$MODEL_NAME modelVersion=$VERSION modelPublisherFormat=$PROVIDER
    ```

[!INCLUDE [code](code.md)]