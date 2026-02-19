---
title: Deploy models as serverless API deployments
titleSuffix: Microsoft Foundry
description: Learn to deploy models as serverless API deployments, using Microsoft Foundry.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 1/26/2026
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.reviewer: fasantia
reviewer: santiagxf
ms.custom: build-2024, serverless, devx-track-azurecli, ignite-2024
zone_pivot_groups: azure-ai-serverless-deployment
---

# Deploy models as serverless API deployments

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to deploy a Microsoft Foundry Model as a serverless API deployment. [Certain models in the model catalog](deploy-models-serverless-availability.md) can be deployed as a serverless API deployment. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription. 

Although serverless API deployment is one option for deploying Foundry Models, we recommend that you deploy Foundry Models to **Foundry resources**.

[!INCLUDE [deploy-models-to-foundry-resources](../includes/deploy-models-to-foundry-resources.md)]

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../includes/hub-project-name.md)]](hub-create-projects.md).

- Ensure that the **Deploy models to Foundry resources** (preview) feature is turned off in the Foundry portal. When this feature is on, serverless API deployments aren't available from the portal.

    :::image type="content" source="../media/deploy-models-serverless/foundry-resources-deployment-disabled.png" alt-text="A screenshot of the Foundry portal showing where to disable deployment to Foundry resources." lightbox="../media/deploy-models-serverless/foundry-resources-deployment-disabled.png":::

- Foundry [Models from Partners and Community](../foundry-models/concepts/models-sold-directly-by-azure.md) require access to Azure Marketplace, while Foundry [Models Sold Directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) don't have this requirement. Ensure you have the permissions required to subscribe to model offerings in Azure Marketplace.

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).

::: zone pivot="ai-foundry-portal"

- You can use any compatible web browser to navigate [Foundry](https://ai.azure.com/?cid=learnDocs).

## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

# [Models sold directly by Azure](#tab/azure-direct)

4. Select the model card of the model you want to deploy. In this article, you select a **DeepSeek-R1** model.

1. Select **Use this model** to open the _Serverless API deployment_ window where you can view the *Pricing and terms* tab.

1. In the deployment wizard, name the deployment. The **Content filter (preview)** option is enabled by default. Leave the default setting for the service to detect harmful content such as hate, self-harm, sexual, and violent content. For more information about content filtering, see [Content filtering in Foundry portal](../concepts/content-filtering.md).
    
    :::image type="content" source="../media/deploy-models-serverless/deepseek-deployment-wizard.png" alt-text="Screenshot showing the deployment wizard for a model sold directly by Azure." lightbox="../media/deploy-models-serverless/deepseek-deployment-wizard.png":::
    
   
# [Models from Partners and Community](#tab/partner-models)

4. Select the model card of the model you want to deploy. In this article, you select **Cohere-command-r-08-2024**.

> [!NOTE]
> [Models from Partners and Community](../concepts/foundry-models-overview.md#models-from-partners-and-community) are offered through Azure Marketplace. For these models, ensure that your account has the **Azure AI Developer** role permissions on the resource group, or that you meet the [permissions required to subscribe to model offerings](#permissions-required-to-subscribe-to-model-offerings), as you're required to subscribe your project to the particular model offering.
    

### Subscribe your project to the model offering

For models from partners and community, for example, _Cohere-command-r-08-2024_, you must create a subscription before you can deploy them. If it's your first time deploying the model in the project, you have to subscribe your project for the particular model offering from Azure Marketplace. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending. Once you subscribe a project for the particular Azure Marketplace offering, subsequent deployments of the same offering in the same project don't require subscribing again.

Furthermore, models offered through Azure Marketplace are available for deployment to serverless API deployment in specific regions. Check [regions that are supported for serverless deployment](deploy-models-serverless-availability.md) to verify available regions for the particular model. If the region in which your project is located isn't listed, you can deploy to a project in a supported region and then [consume serverless API deployment from a different project](deploy-models-serverless-connect.md).


1. On the model's **Details** page, select **Use this model** to open the Serverless API deployment window. In the Serverless API deployment window, the **Azure Marketplace Terms** link provides more information about the terms of use. The **Pricing and terms** tab also provides pricing details for the selected model.

    > [!TIP]
    > For models that can be deployed via serverless API deployment or [managed compute](deploy-models-managed.md), a **Deployment options** window opens up, giving you the choice between serverless API deployment and deployment using a managed compute. From there, you can select the serverless API deployment option.
    
1. If you've never deployed the model in your project before, you first have to subscribe to the model's offering in Azure Marketplace. Select **Subscribe and Deploy** to open the deployment wizard. 
    
    :::image type="content" source="../media/deploy-models-serverless/model-marketplace-subscription.png" alt-text="Screenshot showing where to subscribe a model to Azure Marketplace before deployment." lightbox="../media/deploy-models-serverless/model-marketplace-subscription.png":::

1. Alternatively, if you see the note *You already have an Azure Marketplace subscription for this project*, you don't need to create the subscription since you already have one. Select **Continue to deploy** to open the deployment wizard. 
    
    :::image type="content" source="../media/deploy-models-serverless/model-subscribed-to-marketplace.png" alt-text="Screenshot of the deployment page for a model that is already subscribed to Azure Marketplace." lightbox="../media/deploy-models-serverless/model-subscribed-to-marketplace.png":::    

1. (Optional) At any point, you can see the model offers to which your project is currently subscribed:
    
    1. Go to the [Azure portal](https://portal.azure.com).
    1. Navigate to the resource group where the project belongs.
    1. On the **Type** filter, select **SaaS**.
    1. You see all the offerings to which you're currently subscribed.
    1. Select any resource to see the details.

1. In the deployment wizard, name the deployment. The **Content filter (preview)** option is enabled by default. Leave the default setting for the service to detect harmful content such as hate, self-harm, sexual, and violent content. For more information about content filtering, see [Content filtering in Foundry portal](../concepts/content-filtering.md).
    :::image type="content" source="../media/deploy-models-serverless/deploy-with-content-filter.png" alt-text="Screenshot of the deployment wizard showing the content filter enabled." lightbox="../media/deploy-models-serverless/deploy-with-content-filter.png":::

---

## Deploy the model to a serverless API

In this section, you create an endpoint for your model.

1. In the deployment wizard, select **Deploy**. Wait until the deployment is ready and you're redirected to the Deployments page.

1. To see the endpoints deployed to your project, in the **My assets** section of the left pane, select **Models + endpoints**.

1. The created endpoint uses key authentication for authorization. To get the keys associated with a given endpoint, follow these steps:

    1. Select the deployment, and note the endpoint's Target URI and Key. 
    
    1. Use these credentials to call the deployment and generate predictions.

1. If you need to consume this deployment from a different project or hub, or you plan to use Prompt flow to build intelligent applications, you need to create a connection to the serverless API deployment. To learn how to configure an existing serverless API deployment on a new project or hub, see [Consume deployed serverless API deployment from a different project or from Prompt flow](deploy-models-serverless-connect.md).

    > [!TIP]
    > If you're using Prompt flow in the same project or hub where the deployment was deployed, you still need to create the connection.

## Use the serverless API deployment

Models deployed in Azure Machine Learning and Foundry in serverless API deployments support the [Azure AI Model Inference API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md) that exposes a common set of capabilities for foundational models and that can be used by developers to consume predictions from a diverse set of models in a uniform and consistent way. 

Read more about the [capabilities of this API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#capabilities) and how [you can use it when building applications](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#getting-started). 


## Delete endpoints and subscriptions

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

You can delete model subscriptions and endpoints. Deleting a model subscription makes any associated endpoint become *Unhealthy* and unusable.

To delete a serverless API deployment:

1. Go to the [Foundry](https://ai.azure.com/?cid=learnDocs).
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

::: zone-end

::: zone pivot="programming-language-cli"

- To work with Foundry, install the [Azure CLI](/cli/azure/) and the [ml extension for Azure Machine Learning](/azure/machine-learning/how-to-configure-cli).

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

## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

# [Models sold directly by Azure](#tab/azure-direct)

4. Select the model card of the model you want to deploy. In this article, you select a **DeepSeek-R1** model.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-deepseek/models/DeepSeek-R1/versions/1`, copy `azureml://registries/azureml-deepseek/models/DeepSeek-R1`.

    :::image type="content" source="../media/deploy-models-serverless/model-card.png" alt-text="A screenshot showing a model's details page for a model sold directly by Azure." lightbox="../media/deploy-models-serverless/model-card.png":::
    
   
# [Models from Partners and Community](#tab/partner-models)

4. Select the model card of the model you want to deploy. In this article, you select **Cohere-command-r-08-2024**.

    > [!NOTE]
    > [Models from Partners and Community](../concepts/foundry-models-overview.md#models-from-partners-and-community) are offered through Azure Marketplace. For these models, ensure that your account has the **Azure AI Developer** role permissions on the resource group, or that you meet the [permissions required to subscribe to model offerings](#permissions-required-to-subscribe-to-model-offerings), as you're required to subscribe your project to the particular model offering.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024/versions/1`, copy `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024`.

    :::image type="content" source="../media/deploy-models-serverless/partner-model-card.png" alt-text="A screenshot showing a model's details page for a partner model." lightbox="../media/deploy-models-serverless/partner-model-card.png":::

### Subscribe your project to the model offering

For models from partners and community, for example, _Cohere-command-r-08-2024_, you must create a subscription before you can deploy them. If it's your first time deploying the model in the project, you have to subscribe your project for the particular model offering from Azure Marketplace. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending. Once you subscribe a project for the particular Azure Marketplace offering, subsequent deployments of the same offering in the same project don't require subscribing again.

Furthermore, models offered through Azure Marketplace are available for deployment to serverless API deployment in specific regions. Check [regions that are supported for serverless deployment](deploy-models-serverless-availability.md) to verify available regions for the particular model. If the region in which your project is located isn't listed, you can deploy to a project in a supported region and then [consume serverless API deployment from a different project](deploy-models-serverless-connect.md).

1. Create the model's marketplace subscription. When you create a subscription, you accept the terms and conditions associated with the model offer.

    __subscription.yml__
    
    ```yml
    name: Cohere-command-r-08-2024-qwerty
    model_id: azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024
    ```
    
    Use the previous file to create the subscription:
    
    ```azurecli
    az ml marketplace-subscription create -f subscription.yml
    ```

1. (Optional) At any point, you can see the model offers to which your project is currently subscribed:

    ```azurecli
    az ml marketplace-subscription list
    ```

---

The steps in this section of the article use the _DeepSeek-R1_ model for illustration. The steps are the same, whether you're using Foundry Models sold directly by Azure or Foundry Models from partners and community. For example, if you choose to deploy the _Cohere-command-r-08-2024_
model instead, you can replace the model credentials in the code snippets with the credentials for Cohere.

## Deploy the model to a serverless API

In this section, you create an endpoint for your model. Name the endpoint **DeepSeek-R1-qwerty**.

1. Create the serverless endpoint.

    __endpoint.yml__

    ```yml
    name: DeepSeek-R1-qwerty
    model_id: azureml://registries/azureml-deepseek/models/DeepSeek-R1
    ```

    Use the _endpoint.yml_ file to create the endpoint:

    ```azurecli
    az ml serverless-endpoint create -f endpoint.yml
    ```

1. At any point, you can see the endpoints deployed to your project:

    ```azurecli
    az ml serverless-endpoint list
    ```

1. The created endpoint uses key authentication for authorization. Use the following steps to get the keys associated with a given endpoint.

    ```azurecli
    az ml serverless-endpoint get-credentials -n DeepSeek-R1-qwerty
    ```

1. If you need to consume this deployment from a different project or hub, or you plan to use Prompt flow to build intelligent applications, you need to create a connection to the serverless API deployment. To learn how to configure an existing serverless API deployment on a new project or hub, see [Consume deployed serverless API deployment from a different project or from Prompt flow](deploy-models-serverless-connect.md).

    > [!TIP]
    > If you're using Prompt flow in the same project or hub where the deployment was deployed, you still need to create the connection. 

## Use the serverless API deployment

Models deployed in Azure Machine Learning and Foundry in serverless API deployments support the [Azure AI Model Inference API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md) that exposes a common set of capabilities for foundational models and that can be used by developers to consume predictions from a diverse set of models in a uniform and consistent way. 

Read more about the [capabilities of this API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#capabilities) and how [you can use it when building applications](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#getting-started). 


## Delete endpoints and subscriptions

You can delete model subscriptions and endpoints. Deleting a model subscription makes any associated endpoint become *Unhealthy* and unusable.

To delete a serverless API deployment:

```azurecli
az ml serverless-endpoint delete \
    --name "DeepSeek-R1-qwerty"
```

To delete the associated model subscription:

```azurecli
az ml marketplace-subscription delete \
    --name "DeepSeek-R1"
```

::: zone-end


::: zone pivot="python-sdk"

- To work with Foundry, install the [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install).

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

## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

# [Models sold directly by Azure](#tab/azure-direct)

4. Select the model card of the model you want to deploy. In this article, you select a **DeepSeek-R1** model.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-deepseek/models/DeepSeek-R1/versions/1`, copy `azureml://registries/azureml-deepseek/models/DeepSeek-R1`.

    :::image type="content" source="../media/deploy-models-serverless/model-card.png" alt-text="A screenshot showing a model's details page for a model sold directly by Azure." lightbox="../media/deploy-models-serverless/model-card.png":::
    
   
# [Models from Partners and Community](#tab/partner-models)

4. Select the model card of the model you want to deploy. In this article, you select **Cohere-command-r-08-2024**.

    > [!NOTE]
    > [Models from Partners and Community](../concepts/foundry-models-overview.md#models-from-partners-and-community) are offered through Azure Marketplace. For these models, ensure that your account has the **Azure AI Developer** role permissions on the resource group, or that you meet the [permissions required to subscribe to model offerings](#permissions-required-to-subscribe-to-model-offerings), as you're required to subscribe your project to the particular model offering.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024/versions/1`, copy `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024`.

    :::image type="content" source="../media/deploy-models-serverless/partner-model-card.png" alt-text="A screenshot showing a model's details page for a partner model." lightbox="../media/deploy-models-serverless/partner-model-card.png":::

### Subscribe your project to the model offering

For models from partners and community, for example, _Cohere-command-r-08-2024_, you must create a subscription before you can deploy them. If it's your first time deploying the model in the project, you have to subscribe your project for the particular model offering from Azure Marketplace. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending. Once you subscribe a project for the particular Azure Marketplace offering, subsequent deployments of the same offering in the same project don't require subscribing again.

Furthermore, models offered through Azure Marketplace are available for deployment to serverless API deployment in specific regions. Check [regions that are supported for serverless deployment](deploy-models-serverless-availability.md) to verify available regions for the particular model. If the region in which your project is located isn't listed, you can deploy to a project in a supported region and then [consume serverless API deployment from a different project](deploy-models-serverless-connect.md).

1. Create the model's marketplace subscription. When you create a subscription, you accept the terms and conditions associated with the model offer.

    ```python
    model_id="azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024"
    subscription_name="Cohere-command-r-08-2024"

    marketplace_subscription = MarketplaceSubscription(
        model_id=model_id,
        name=subscription_name,
    )

    marketplace_subscription = client.marketplace_subscriptions.begin_create_or_update(
        marketplace_subscription
    ).result()
    ```

1. (Optional) At any point, you can see the model offers to which your project is currently subscribed:

    ```python
    marketplace_sub_list = client.marketplace_subscriptions.list()

    for sub in marketplace_sub_list:
        print(sub.as_dict())
    ```

---

The steps in this section of the article use the _DeepSeek-R1_ model for illustration. The steps are the same, whether you're using Foundry Models sold directly by Azure or Foundry Models from partners and community. For example, if you choose to deploy the _Cohere-command-r-08-2024_
model instead, you can replace the model credentials in the code snippets with the credentials for Cohere.

## Deploy the model to a serverless API

In this section, you create an endpoint for your model. Name the endpoint **DeepSeek-R1-qwerty**.

1. Create the serverless endpoint.

    ```python
    endpoint_name="DeepSeek-R1-qwerty"
    
    serverless_endpoint = ServerlessEndpoint(
        name=endpoint_name,
        model_id=model_id
    )

    created_endpoint = client.serverless_endpoints.begin_create_or_update(
        serverless_endpoint
    ).result()
    ```

1. At any point, you can see the endpoints deployed to your project:

    ```python
    endpoint_name="DeepSeek-R1-qwerty"
    
    serverless_endpoint = ServerlessEndpoint(
        name=endpoint_name,
        model_id=model_id
    )

    created_endpoint = client.serverless_endpoints.begin_create_or_update(
        serverless_endpoint
    ).result()
    ```

1. The created endpoint uses key authentication for authorization. Use the following steps to get the keys associated with a given endpoint.

    ```python
    endpoint_keys = client.serverless_endpoints.get_keys(endpoint_name)
    print(endpoint_keys.primary_key)
    print(endpoint_keys.secondary_key)
    ```

1. If you need to consume this deployment from a different project or hub, or you plan to use Prompt flow to build intelligent applications, you need to create a connection to the serverless API deployment. To learn how to configure an existing serverless API deployment on a new project or hub, see [Consume deployed serverless API deployment from a different project or from Prompt flow](deploy-models-serverless-connect.md).

    > [!TIP]
    > If you're using Prompt flow in the same project or hub where the deployment was deployed, you still need to create the connection. 


## Use the serverless API deployment

Models deployed in Azure Machine Learning and Foundry in serverless API deployments support the [Azure AI Model Inference API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md) that exposes a common set of capabilities for foundational models and that can be used by developers to consume predictions from a diverse set of models in a uniform and consistent way. 

Read more about the [capabilities of this API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#capabilities) and how [you can use it when building applications](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#getting-started). 


## Delete endpoints and subscriptions

You can delete model subscriptions and endpoints. Deleting a model subscription makes any associated endpoint become *Unhealthy* and unusable.

```python
client.serverless_endpoints.begin_delete(endpoint_name).wait()
```

To delete the associated model subscription:

```python
client.marketplace_subscriptions.begin_delete(subscription_name).wait()
```

::: zone-end


::: zone pivot="programming-language-bicep"

- To work with Foundry, install the Azure CLI as described at [Azure CLI](/cli/azure/).

    Configure the following environment variables according to your settings:

    ```azurecli
    RESOURCE_GROUP="serverless-models-dev"
    LOCATION="eastus2" 
    ```  


## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

# [Models sold directly by Azure](#tab/azure-direct)

4. Select the model card of the model you want to deploy. In this article, you select a **DeepSeek-R1** model.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-deepseek/models/DeepSeek-R1/versions/1`, copy `azureml://registries/azureml-deepseek/models/DeepSeek-R1`.

    :::image type="content" source="../media/deploy-models-serverless/model-card.png" alt-text="A screenshot showing a model's details page for a model sold directly by Azure." lightbox="../media/deploy-models-serverless/model-card.png":::
    
   
# [Models from Partners and Community](#tab/partner-models)

4. Select the model card of the model you want to deploy. In this article, you select **Cohere-command-r-08-2024**.

    > [!NOTE]
    > [Models from Partners and Community](../concepts/foundry-models-overview.md#models-from-partners-and-community) are offered through Azure Marketplace. For these models, ensure that your account has the **Azure AI Developer** role permissions on the resource group, or that you meet the [permissions required to subscribe to model offerings](#permissions-required-to-subscribe-to-model-offerings), as you're required to subscribe your project to the particular model offering.

1. Copy the **Model ID** without including the model version, since serverless API deployments always deploy the model's latest version available. For example, for the model ID `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024/versions/1`, copy `azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024`.

    :::image type="content" source="../media/deploy-models-serverless/partner-model-card.png" alt-text="A screenshot showing a model's details page for a partner model." lightbox="../media/deploy-models-serverless/partner-model-card.png":::

### Subscribe your project to the model offering

For models from partners and community, for example, _Cohere-command-r-08-2024_, you must create a subscription before you can deploy them. If it's your first time deploying the model in the project, you have to subscribe your project for the particular model offering from Azure Marketplace. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending. Once you subscribe a project for the particular Azure Marketplace offering, subsequent deployments of the same offering in the same project don't require subscribing again.

Furthermore, models offered through Azure Marketplace are available for deployment to serverless API deployment in specific regions. Check [regions that are supported for serverless deployment](deploy-models-serverless-availability.md) to verify available regions for the particular model. If the region in which your project is located isn't listed, you can deploy to a project in a supported region and then [consume serverless API deployment from a different project](deploy-models-serverless-connect.md).

1. Use the following bicep configuration to create a model subscription. When you create a subscription, you accept the terms and conditions associated with the model offer.

    __model-subscription.bicep__
    
    ```bicep
    param projectName string = 'my-project'
    param modelId string = 'azureml://registries/azureml-cohere/models/Cohere-command-r-08-2024'
    
    var modelName = substring(modelId, (lastIndexOf(modelId, '/') + 1))
    // Replace period character which is used in some model names (and is not valid in the subscription name)
    var sanitizedModelName = replace(modelName, '.', '')
    var subscriptionName = '${sanitizedModelName}-subscription'
    
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

1. (Optional) At any point, you can see the model offers to which your project is currently subscribed. You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.SaaS']"
    ```

---

The steps in this section of the article use the _DeepSeek-R1_ model for illustration. The steps are the same, whether you're using Foundry Models sold directly by Azure or Foundry Models from partners and community. For example, if you choose to deploy the _Cohere-command-r-08-2024_
model instead, you can replace the model credentials in the code snippets with the credentials for Cohere.

## Deploy the model to a serverless API

In this section, you create an endpoint for your model. Name the endpoint **myserverless-text-1234ss**.

1. Create the serverless endpoint. Use the following template to create an endpoint:

    __serverless-endpoint.bicep__

    ```bicep
    param projectName string = 'my-project'
    param endpointName string = 'myserverless-text-1234ss'
    param location string = resourceGroup().location
    param modelId string = 'azureml://registries/azureml-deepseek/models/DeepSeek-R1'
    
    var modelName = substring(modelId, (lastIndexOf(modelId, '/') + 1))
    // Replace period character which is used in some model names (and is not valid in the subscription name)
    var sanitizedModelName = replace(modelName, '.', '')
    var subscriptionName = '${sanitizedModelName}-subscription'
    
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
    
1. At any point, you can see the endpoints deployed to your project:

    You can use the resource management tools to query the resources. The following code uses Azure CLI:

    ```azurecli
    az resource list \
        --query "[?type=='Microsoft.MachineLearningServices/workspaces/serverlessEndpoints']"
    ```

1. The created endpoint uses key authentication for authorization. Get the keys associated with the given endpoint by using REST APIs to query this information.

1. If you need to consume this deployment from a different project or hub, or you plan to use Prompt flow to build intelligent applications, you need to create a connection to the serverless API deployment. To learn how to configure an existing serverless API deployment on a new project or hub, see [Consume deployed serverless API deployment from a different project or from Prompt flow](deploy-models-serverless-connect.md).

    > [!TIP]
    > If you're using Prompt flow in the same project or hub where the deployment was deployed, you still need to create the connection. 


## Use the serverless API deployment

Models deployed in Azure Machine Learning and Foundry in serverless API deployments support the [Azure AI Model Inference API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md) that exposes a common set of capabilities for foundational models and that can be used by developers to consume predictions from a diverse set of models in a uniform and consistent way. 

Read more about the [capabilities of this API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#capabilities) and how [you can use it when building applications](../../ai-foundry/model-inference/reference/reference-model-inference-api.md#getting-started). 


## Delete endpoints and subscriptions

You can delete model subscriptions and endpoints. Deleting a model subscription makes any associated endpoint become *Unhealthy* and unusable.

You can use the resource management tools to manage the resources. The following code uses Azure CLI:

```azurecli
az resource delete --name <resource-name>
```

::: zone-end


## Cost and quota considerations for Foundry Models deployed as a serverless API deployment

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. Additionally, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

- You can find pricing information for [Models Sold Directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md), on the *Pricing and terms* tab of the _Serverless API deployment_ window.

- [Models from Partners and Community](../foundry-models/concepts/models-sold-directly-by-azure.md) are offered through Azure Marketplace and integrated with Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning these models. Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently. For more information on how to track costs, see [Monitor costs for models offered through Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).


## Permissions required to subscribe to model offerings

Azure role-based access controls (Azure RBAC) are used to grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __Owner__, __Contributor__, or __Azure AI Developer__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

- On the Azure subscription—to subscribe the workspace to Azure Marketplace offering, once for each workspace, per offering:
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

For more information on permissions, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).



## Related content

* [Region availability for models as serverless API deployments](deploy-models-serverless-availability.md)
* [Fine-tune models using serverless API deployment](../how-to/fine-tune-serverless.md)
