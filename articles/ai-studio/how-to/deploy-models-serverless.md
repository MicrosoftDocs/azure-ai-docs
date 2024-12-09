---
title: Deploy models as serverless APIs
titleSuffix: Azure AI Foundry
description: Learn to deploy models as serverless APIs, using Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 07/18/2024
ms.author: mopeakande
author: msakande
ms.reviewer: fasantia
reviewer: santiagxf
ms.custom: build-2024, serverless, devx-track-azurecli, ignite-2024
---

# Deploy models as serverless APIs

In this article, you learn how to deploy a model from the model catalog as a serverless API with pay-as-you-go token based billing.

[!INCLUDE [models-preview](../includes/models-preview.md)]

[Certain models in the model catalog](deploy-models-serverless-availability.md) can be deployed as a serverless API with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription.

This article uses a Meta Llama model deployment for illustration. However, you can use the same steps to deploy any of the [models in the model catalog that are available for serverless API deployment](deploy-models-serverless-availability.md).

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry hub](create-azure-ai-resource.md).

- An [Azure AI Foundry project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).

- You need to install the following software to work with Azure AI Foundry:

    # [AI Foundry portal](#tab/azure-ai-studio)

    You can use any compatible web browser to navigate [Azure AI Foundry](https://ai.azure.com).

    # [Azure CLI](#tab/cli)

    The [Azure CLI](/cli/azure/) and the [ml extension for Azure Machine Learning](/azure/machine-learning/how-to-configure-cli).

    ```azurecli
    az extension add -n ml
    ```

    If you already have the extension installed, ensure the latest version is installed.

    ```azurecli
    az extension update -n ml
    ```

    Once the extension is installed, configure it:

    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<project-name> group=<resource-group> location=<location>
    ```

    # [Python SDK](#tab/python)

    Install the [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install).

    ```python
    pip install -U azure-ai-ml
    ```

    Once installed, import necessary namespaces and create a client connected to your project:

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import InteractiveBrowserCredential
    from azure.ai.ml.entities import MarketplaceSubscription, ServerlessEndpoint

    client = MLClient(
        credential=InteractiveBrowserCredential(tenant_id="<tenant-id>"),
        subscription_id="<subscription-id>",
        resource_group_name="<resource-group>",
        workspace_name="<project-name>",
    )
    ```

    # [Bicep](#tab/bicep)

    Install the Azure CLI as described at [Azure CLI](/cli/azure/).

    Configure the following environment variables according to your settings:

    ```azurecli
    RESOURCE_GROUP="serverless-models-dev"
    LOCATION="eastus2" 
    ```  

    # [ARM](#tab/arm)

    You can use any compatible web browser to [deploy ARM templates](/azure/azure-resource-manager/templates/deploy-portal) in the Microsoft Azure portal or use any of the deployment tools. This tutorial uses the [Azure CLI](/cli/azure/).


## Find your model and model ID in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

> [!NOTE]
> For models offered through the Azure Marketplace, ensure that your account has the **Azure AI Developer** role permissions on the resource group, or that you meet the [permissions required to subscribe to model offerings](#permissions-required-to-subscribe-to-model-offerings).
>
> Models that are offered by non-Microsoft providers (for example, Llama and Mistral models) are billed through the Azure Marketplace. For such models, you're required to subscribe your project to the particular model offering. Models that are offered by Microsoft (for example, Phi-3 models) don't have this requirement, as billing is done differently. For details about billing for serverless deployment of models in the model catalog, see [Billing for serverless APIs](model-catalog-overview.md#billing).

4. Select the model card of the model you want to deploy. In this article, you select a **Meta-Llama-3-8B-Instruct** model.
    
    1. If you're deploying the model using Azure CLI, Python, or ARM, copy the **Model ID**.

        > [!IMPORTANT]
        > Do not include the version when copying the **Model ID**. Serverless API endpoints always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct/versions/3`, copy `azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct`.

    :::image type="content" source="../media/deploy-monitor/serverless/model-card.png" alt-text="A screenshot showing a model's details page." lightbox="../media/deploy-monitor/serverless/model-card.png":::


The next section covers the steps for subscribing your project to a model offering. You can skip this section and go to [Deploy the model to a serverless API endpoint](#deploy-the-model-to-a-serverless-api-endpoint), if you're deploying a Microsoft model.

## Subscribe your project to the model offering

Serverless API endpoints can deploy both Microsoft and non-Microsoft offered models. For Microsoft models (such as Phi-3 models), you don't need to create an Azure Marketplace subscription and you can [deploy them to serverless API endpoints directly](#deploy-the-model-to-a-serverless-api-endpoint) to consume their predictions. For non-Microsoft models, you need to create the subscription first. If it's your first time deploying the model in the project, you have to subscribe your project for the particular model offering from the Azure Marketplace. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending.

> [!TIP]
> Skip this step if you are deploying models from the Phi-3 family of models. Directly [deploy the model to a serverless API endpoint](#deploy-the-model-to-a-serverless-api-endpoint).

> [!NOTE]
> Models offered through the Azure Marketplace are available for deployment to serverless API endpoints in specific regions. Check [Model and region availability for Serverless API deployments](deploy-models-serverless-availability.md) to verify which models and regions are available. If the one you need is not listed, you can deploy to a workspace in a supported region and then [consume serverless API endpoints from a different workspace](deploy-models-serverless-connect.md).

1. Create the model's marketplace subscription. When you create a subscription, you accept the terms and conditions associated with the model offer.

    # [AI Foundry portal](#tab/azure-ai-studio)

    1. On the model's **Details** page, select **Deploy**. A **Deployment options** window opens up, giving you the choice between serverless API deployment and deployment using a managed compute.

        > [!NOTE]
        > For models that can be deployed only via serverless API deployment, the serverless API deployment wizard opens up right after you select **Deploy** from the model's details page.

    1. Select **Serverless API with Azure AI Content Safety (preview)** to open the serverless API deployment wizard.
    1. Select the project in which you want to deploy your models. To use the serverless API model deployment offering, your project must belong to one of the [regions that are supported for serverless deployment](deploy-models-serverless-availability.md) for the particular model.

        :::image type="content" source="../media/deploy-monitor/serverless/deploy-pay-as-you-go.png" alt-text="A screenshot showing how to deploy a model with the serverless API option." lightbox="../media/deploy-monitor/serverless/deploy-pay-as-you-go.png"::: 

    1. If you see the note *You already have an Azure Marketplace subscription for this project*, you don't need to create the subscription since you already have one. You can proceed to [Deploy the model to a serverless API endpoint](#deploy-the-model-to-a-serverless-api-endpoint).

    1. In the deployment wizard, select the link to **Azure Marketplace Terms** to learn more about the terms of use. You can also select the **Pricing and terms** tab to learn about pricing for the selected model.

    1. Select **Subscribe and Deploy**.

    # [Azure CLI](#tab/cli)

    __subscription.yml__

    ```yml
    name: meta-llama3-8b-qwerty
    model_id: azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct
    ```

    Use the previous file to create the subscription:

    ```azurecli
    az ml marketplace-subscription create -f subscription.yml
    ```

    # [Python SDK](#tab/python)

    ```python
    model_id="azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct"
    subscription_name="Meta-Llama-3-8B-Instruct"

    marketplace_subscription = MarketplaceSubscription(
        model_id=model_id,
        name=subscription_name,
    )

    marketplace_subscription = client.marketplace_subscriptions.begin_create_or_update(
        marketplace_subscription
    ).result()
    ```

    # [Bicep](#tab/bicep)

    Use the following bicep configuration to create a model subscription:

    __model-subscription.bicep__
    
    ```bicep
    param projectName string = 'my-project'
    param modelId string = 'azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct'
    
    var modelName = substring(modelId, (lastIndexOf(modelId, '/') + 1))
    var subscriptionName = '${modelName}-subscription'
    
    resource projectName_subscription 'Microsoft.MachineLearningServices/workspaces/marketplaceSubscriptions@2024-04-01-preview' = if (!startsWith(
      modelId,
      'azureml://registries/azureml/'
    )) {
      name: '${projectName}/${subscriptionName}'
      properties: {
        modelId: modelId
      }
    }
    ```

    Then create the resource as follows:

    ```azurecli
    az deployment group create --resource-group $RESOURCE_GROUP --template-file model-subscription.bicep
    ```

    # [ARM](#tab/arm)

    Use the following template to create a model subscription:

    __model-subscription.json__

    ```json
    {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "project_name": {
                "defaultValue": "my-project",
                "type": "String"
            },
            "subscription_name": {
                "defaultValue": "Meta-Llama-3-8B-Instruct",
                "type": "String"
            },
            "model_id": {
                "defaultValue": "azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct",
                "type": "String"
            }
        },
        "variables": {},
        "resources": [
            {
                "type": "Microsoft.MachineLearningServices/workspaces/marketplaceSubscriptions",
                "apiVersion": "2024-04-01",
                "name": "[concat(parameters('project_name'), '/', parameters('subscription_name'))]",
                "properties": {
                    "modelId": "[parameters('model_id')]"
                }
            }
        ]
    }
    ```

    Use the Azure portal or the Azure CLI to create the deployment.

    ```azurecli
    az deployment group create --resource-group $RESOURCE_GROUP --template-file model-subscription.json
    ```

1. Once you subscribe the project for the particular Azure Marketplace offering, subsequent deployments of the same offering in the same project don't require subscribing again.

1. At any point, you can see the model offers to which your project is currently subscribed:

    # [AI Foundry portal](#tab/azure-ai-studio)

    1. Go to the [Azure portal](https://portal.azure.com).

    1. Navigate to the resource group where the project belongs.

    1. On the **Type** filter, select **SaaS**.

    1. You see all the offerings to which you're currently subscribed.

    1. Select any resource to see the details.

    # [Azure CLI](#tab/cli)

    ```azurecli
    az ml marketplace-subscription list
    ```

    # [Python SDK](#tab/python)

    ```python
    marketplace_sub_list = client.marketplace_subscriptions.list()

    for sub in marketplace_sub_list:
        print(sub.as_dict())
    ```

    # [Bicep](#tab/bicep)

    You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.SaaS']"
    ```

    # [ARM](#tab/arm)

    You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.SaaS']"
    ```

## Deploy the model to a serverless API endpoint

Once you've created a subscription for a non-Microsoft model, you can deploy the associated model to a serverless API endpoint. For Microsoft models (such as Phi-3 models), you don't need to create a subscription.

The serverless API endpoint provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance organizations need. This deployment option doesn't require quota from your subscription.

In this section, you create an endpoint with the name **meta-llama3-8b-qwerty**.

1. Create the serverless endpoint

    # [AI Foundry portal](#tab/azure-ai-studio)

    1. To deploy a Microsoft model that doesn't require subscribing to a model offering:
        1. Select **Deploy** and then select **Serverless API with Azure AI Content Safety (preview)** to open the deployment wizard.
        1. Select the project in which you want to deploy your model. Notice that not all the regions are supported.

    1. Alternatively, for a non-Microsoft model that requires a model subscription, if you've just subscribed your project to the model offer in the previous section, continue to select **Deploy**. Alternatively, select **Continue to deploy** (if your deployment wizard had the note *You already have an Azure Marketplace subscription for this project*).

        :::image type="content" source="../media/deploy-monitor/serverless/deploy-pay-as-you-go-subscribed-project.png" alt-text="A screenshot showing a project that is already subscribed to the offering." lightbox="../media/deploy-monitor/serverless/deploy-pay-as-you-go-subscribed-project.png":::

    1. Give the deployment a name. This name becomes part of the deployment API URL. This URL must be unique in each Azure region.

        :::image type="content" source="../media/deploy-monitor/serverless/deployment-name.png" alt-text="A screenshot showing how to specify the name of the deployment you want to create." lightbox="../media/deploy-monitor/serverless/deployment-name.png":::
       > [!TIP]
       > The **Content filter (preview)** option is enabled by default. Leave the default setting for the service to detect harmful content such as hate, self-harm, sexual, and violent content. For more information about content filtering (preview), see [Content filtering in Azure AI Foundry portal](../concepts/content-filtering.md).

    1. Select **Deploy**. Wait until the deployment is ready and you're redirected to the Deployments page.

    # [Azure CLI](#tab/cli)

    __endpoint.yml__

    ```yml
    name: meta-llama3-8b-qwerty
    model_id: azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct
    ```

    Use the _endpoint.yml_ file to create the endpoint:

    ```azurecli
    az ml serverless-endpoint create -f endpoint.yml
    ```

    # [Python SDK](#tab/python)

    ```python
    endpoint_name="meta-llama3-8b-qwerty"
    
    serverless_endpoint = ServerlessEndpoint(
        name=endpoint_name,
        model_id=model_id
    )

    created_endpoint = client.serverless_endpoints.begin_create_or_update(
        serverless_endpoint
    ).result()
    ```

    # [Bicep](#tab/bicep)

    Use the following template to create an endpoint:

    __serverless-endpoint.bicep__

    ```bicep
    param projectName string = 'my-project'
    param endpointName string = 'myserverless-text-1234ss'
    param location string = resourceGroup().location
    param modelId string = 'azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct'
    
    var modelName = substring(modelId, (lastIndexOf(modelId, '/') + 1))
    var subscriptionName = '${modelName}-subscription'
    
    resource projectName_endpoint 'Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-04-01-preview' = {
      name: '${projectName}/${endpointName}'
      location: location
      sku: {
        name: 'Consumption'
      }
      properties: {
        modelSettings: {
          modelId: modelId
        }
      }
      dependsOn: [
        projectName_subscription
      ]
    }
    
    output endpointUri string = projectName_endpoint.properties.inferenceEndpoint.uri
    ```

    Create the deployment as follows:

    ```azurecli
    az deployment group create --resource-group $RESOURCE_GROUP --template-file model-subscription.bicep
    ```

    # [ARM](#tab/arm)

    Use the following template to create an endpoint:

    __template.json__

    ```json
    {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "project_name": {
                "defaultValue": "my-project",
                "type": "String"
            },
            "endpoint_name": {
                "defaultValue": "meta-llama3-8b-qwerty",
                "type": "String"
            },
            "location": {
                "defaultValue": "eastus2",
                "type": "String"
            },
            "model_id": {
                "defaultValue": "azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct",
                "type": "String"
            }
        },
        "variables": {},
        "resources": [
            {
                "type": "Microsoft.MachineLearningServices/workspaces/serverlessEndpoints",
                "apiVersion": "2024-04-01",
                "name": "[concat(parameters('project_name'), '/', parameters('endpoint_name'))]",
                "location": "[parameters('location')]",
                "sku": {
                    "name": "Consumption"
                },
                "properties": {
                    "modelSettings": {
                        "modelId": "[parameters('model_id')]"
                    }
                }
            }
        ]
    }
    ```

    Then create the deployment:

    ```azurecli
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file template.json
    ```

    The Azure deployment template can take a few minutes to complete. When it finishes, you see a message that includes the result:

    ```output
    "provisioningState": "Succeeded",
    ```

1. At any point, you can see the endpoints deployed to your project:

    # [AI Foundry portal](#tab/azure-ai-studio)

    1. Go to your project.

    1. In the **My assets** section, select **Models + endpoints**.

    1. Serverless API endpoints are displayed.

    # [Azure CLI](#tab/cli)

    ```azurecli
    az ml serverless-endpoint list
    ```

    # [Python SDK](#tab/python)

    ```python
    endpoint_name="meta-llama3-8b-qwerty"
    
    serverless_endpoint = ServerlessEndpoint(
        name=endpoint_name,
        model_id=model_id
    )

    created_endpoint = client.serverless_endpoints.begin_create_or_update(
        serverless_endpoint
    ).result()
    ```

    # [Bicep](#tab/bicep)

    You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.MachineLearningServices/workspaces/serverlessEndpoints']"
    ```

    # [ARM](#tab/arm)

    You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.MachineLearningServices/workspaces/serverlessEndpoints']"
    ```

1. The created endpoint uses key authentication for authorization. Use the following steps to get the keys associated with a given endpoint.

    # [AI Foundry portal](#tab/azure-ai-studio)

    You can select the deployment, and note the endpoint's _Target URI_ and _Key_. Use them to call the deployment and generate predictions.

    > [!NOTE]
    > When using the [Azure portal](https://portal.azure.com), serverless API endpoints aren't displayed by default on the resource group. Use the **Show hidden types** option to display them on the resource group.

    # [Azure CLI](#tab/cli)

    ```azurecli
    az ml serverless-endpoint get-credentials -n meta-llama3-8b-qwerty
    ```

    # [Python SDK](#tab/python)

    ```python
    endpoint_keys = client.serverless_endpoints.get_keys(endpoint_name)
    print(endpoint_keys.primary_key)
    print(endpoint_keys.secondary_key)
    ```

    # [Bicep](#tab/bicep)

    Use REST APIs to query this information.

    # [ARM](#tab/arm)

    Use REST APIs to query this information.

1. At this point, your endpoint is ready to be used.

1. If you need to consume this deployment from a different project or hub, or you plan to use prompt flow to build intelligent applications, you need to create a connection to the serverless API deployment. To learn how to configure an existing serverless API endpoint on a new project or hub, see [Consume deployed serverless API endpoints from a different project or from Prompt flow](deploy-models-serverless-connect.md).

    > [!TIP]
    > If you're using prompt flow in the same project or hub where the deployment was deployed, you still need to create the connection.

## Use the serverless API endpoint

Models deployed in Azure Machine Learning and Azure AI Foundry in Serverless API endpoints support the [Azure AI Model Inference API](../reference/reference-model-inference-api.md) that exposes a common set of capabilities for foundational models and that can be used by developers to consume predictions from a diverse set of models in a uniform and consistent way. 

Read more about the [capabilities of this API](../reference/reference-model-inference-api.md#capabilities) and how [you can use it when building applications](../reference/reference-model-inference-api.md#getting-started). 

## Network isolation

Endpoints for models deployed as Serverless APIs follow the public network access (PNA) flag setting of the AI Foundry portal Hub that has the project in which the deployment exists. To secure your MaaS endpoint, disable the PNA flag on your AI Foundry Hub. You can secure inbound communication from a client to your endpoint by using a private endpoint for the hub.

To set the PNA flag for the Azure AI Foundry hub:

1. Go to the [Azure portal](https://portal.azure.com).
2. Search for the Resource group to which the hub belongs, and select the **Azure AI hub** from the resources listed for this resource group.
3. From the hub **Overview** page on the left menu, select **Settings** > **Networking**.
4. Under the **Public access** tab, you can configure settings for the public network access flag.
5. Save your changes. Your changes might take up to five minutes to propagate.

## Delete endpoints and subscriptions

You can delete model subscriptions and endpoints. Deleting a model subscription makes any associated endpoint become *Unhealthy* and unusable.

# [AI Foundry portal](#tab/azure-ai-studio)

To delete a serverless API endpoint:

1. Go to the [Azure AI Foundry](https://ai.azure.com).

1. Go to your project.

1. In the **My assets** section, select **Models + endpoints**.

1. Open the deployment you want to delete.

1. Select **Delete**.


To delete the associated model subscription:

1. Go to the [Azure portal](https://portal.azure.com)

1. Navigate to the resource group where the project belongs.

1. On the **Type** filter, select **SaaS**.

1. Select the subscription you want to delete.

1. Select **Delete**.

# [Azure CLI](#tab/cli)

To delete a serverless API endpoint:

```azurecli
az ml serverless-endpoint delete \
    --name "meta-llama3-8b-qwerty"
```

To delete the associated model subscription:

```azurecli
az ml marketplace-subscription delete \
    --name "Meta-Llama-3-8B-Instruct"
```

# [Python SDK](#tab/python)

To delete a serverless API endpoint:

```python
client.serverless_endpoints.begin_delete(endpoint_name).wait()
```

To delete the associated model subscription:

```python
client.marketplace_subscriptions.begin_delete(subscription_name).wait()
```

# [Bicep](#tab/bicep)

You can use the resource management tools to manage the resources. The following code uses Azure CLI:

```azurecli
az resource delete --name <resource-name>
```


# [ARM](#tab/arm)

You can use the resource management tools to manage the resources. The following code uses Azure CLI:

```azurecli
az resource delete --name <resource-name>
```

---

## Cost and quota considerations for models deployed as serverless API endpoints

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

#### Cost for Microsoft models

You can find the pricing information on the __Pricing and terms__ tab of the deployment wizard when deploying Microsoft models (such as Phi-3 models) as serverless API endpoints.

#### Cost for non-Microsoft models

Non-Microsoft models deployed as serverless API endpoints are offered through the Azure Marketplace and integrated with Azure AI Foundry for use. You can find the Azure Marketplace pricing when deploying or fine-tuning these models.

Each time a project subscribes to a given offer from the Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

:::image type="content" source="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/deploy-monitor/serverless/costs-model-as-service-cost-details.png":::


## Permissions required to subscribe to model offerings

Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Owner__, __Contributor__, or __Azure AI Developer__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

- On the Azure subscription—to subscribe the workspace to the Azure Marketplace offering, once for each workspace, per offering:
  - `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
  - `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
  - `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
  - `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
  - `Microsoft.SaaS/register/action`

- On the resource group—to create and use the SaaS resource:
  - `Microsoft.SaaS/resources/read`
  - `Microsoft.SaaS/resources/write`

- On the workspace—to deploy endpoints (the Azure Machine Learning data scientist role contains these permissions already):
  - `Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*`  
  - `Microsoft.MachineLearningServices/workspaces/serverlessEndpoints/*`

For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).

## Related content

* [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md)
* [Fine-tune a Meta Llama 2 model in Azure AI Foundry portal](fine-tune-model-llama.md)
