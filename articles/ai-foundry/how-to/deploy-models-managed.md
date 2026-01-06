---
title: How to deploy and inference a managed compute deployment
titleSuffix: Microsoft Foundry
description: Learn how to deploy large language models on managed compute in Microsoft Foundry and perform real-time inference for generative AI applications.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 09/15/2025
ms.reviewer: fasantia 
reviewer: santiagxf
ms.author: mopeakande
manager: nitinme
author: msakande
zone_pivot_groups: azure-ai-managed-compute-deployment
ai-usage: ai-assisted

#CustomerIntent: As an Azure AI developer, I want to deploy and perform inference on large language models using managed compute in Microsoft Foundry so that I can make models available for real-time generative AI applications in production environments.
---

# How to deploy and infer with a managed compute deployment

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The Microsoft Foundry portal [model catalog](../how-to/model-catalog-overview.md) offers over 1,600 models. A common way to deploy these models is to use the managed compute deployment option. This option is also sometimes referred to as a managed online deployment. 

When you deploy a large language model (LLM), you make it available for use in a website, an application, or other production environment. Deployment typically involves hosting the model on a server or in the cloud and creating an API or other interface for users to interact with the model. You can invoke the deployment for real-time inference of generative AI applications such as chat and copilot.

In this article, you learn to deploy models with the managed compute deployment option and to perform inference on the deployed model.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]](hub-create-projects.md).

- Foundry [Models from Partners and Community](../model-inference/concepts/models.md#models-from-partners-and-community) require access to Azure Marketplace, while Foundry [Models Sold Directly by Azure](../model-inference/concepts/models.md#models-sold-directly-by-azure) don't have this requirement. Ensure your Azure subscription has the permissions required to subscribe to model offerings in Azure Marketplace. See [Enable Azure Marketplace purchases](/azure/cost-management-billing/manage/enable-marketplace-purchases) to learn more.

- Azure role-based access controls (Azure RBAC) grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).


## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. In the **Deployment options** filter, select **Managed compute**.

    [!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

    :::image type="content" source="../media/deploy-models-managed/catalog-filter-managed-compute.png" alt-text="A screenshot of the model catalog showing how to filter for models that can be deployed via managed compute." lightbox="../media/deploy-models-managed/catalog-filter-managed-compute.png"::: 

1. Select a model to open its model card. In this article, use the model `deepset-roberta-base-squad2`.


::: zone pivot="ai-foundry-portal"

## Deploy the model

1. From the model's page, select **Use this model** to open the deployment window. 
1. The deployment window is pre-filled with some selections and parameter values. You can either keep them or change them as desired. You can also select an existing endpoint for the deployment or create a new one. For this example, specify an instance count of `1` and create a new endpoint for the deployment.

    :::image type="content" source="../media/deploy-models-managed/deployment-configuration.png" alt-text="Screenshot of the deployment configuration screen for managed compute deployment in Foundry." lightbox="../media/deploy-models-managed/deployment-configuration.png":::

1. Select **Deploy** to create your deployment. The creation process might take a few minutes to complete. When it's complete, the portal opens the model deployment page.

    > [!TIP]
    > To see endpoints deployed to your project, go to the **My assets** section of the left pane and select **Models + endpoints**.

1. The created endpoint uses key authentication for authorization. To get the keys associated with a given endpoint, follow these steps:

    1. Select the deployment, and note the endpoint's Target URI and Key.
    1. Use these credentials to call the deployment and generate predictions.
 

## Consume deployments

After you create your deployment, follow these steps to consume it:

1. Select **Models + endpoints** under the **My assets** section in your Foundry project.
1. Select your deployment from the **Model deployments** tab.
1. Go to the **Test** tab for sample inference to the endpoint.
1. Return to the **Details** tab to copy the deployment's "Target URI", which you can use to run inference with code.
1. Go to the **Consume** tab of the deployment to find code samples for consumption.

::: zone-end


::: zone pivot="python-sdk"
6. Copy the model ID from the details page of the model you selected. It looks like this for the selected model: `azureml://registries/azureml/models/deepset-roberta-base-squad2/versions/17`.


## Deploy the model

1.  Install the Azure Machine Learning SDK.

    ```python
    pip install azure-ai-ml
    pip install azure-identity
    ```

1. Authenticate with Azure Machine Learning and create a client object. Replace the placeholders with your subscription ID, resource group name, and Foundry project name.

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import InteractiveBrowserCredential
    
    workspace_ml_client = MLClient(
        credential=InteractiveBrowserCredential,
        subscription_id="your subscription ID goes here",
        resource_group_name="your resource group name goes here",
        workspace_name="your project name goes here",
    )
    ```

1. Create an endpoint. For the managed compute deployment option, you need to create an endpoint before a model deployment. Think of an endpoint as a container that can house multiple model deployments. The endpoint names need to be unique in a region, so in this example use the timestamp to create a unique endpoint name.

    ```python
    import time, sys
    from azure.ai.ml.entities import (
        ManagedOnlineEndpoint,
        ManagedOnlineDeployment,
        ProbeSettings,
    )
    
    # Make the endpoint name unique
    timestamp = int(time.time())
    online_endpoint_name = "customize your endpoint name here" + str(timestamp)
    
    # Create an online endpoint
    endpoint = ManagedOnlineEndpoint(
        name=online_endpoint_name,
        auth_mode="key",
    )
    workspace_ml_client.online_endpoints.begin_create_or_update(endpoint).wait()
    ```

1. Create a deployment. Replace the model ID in the next code with the model ID that you copied from the details page of the model you selected in the [Find your model in the model catalog](#find-your-model-in-the-model-catalog) section.

    ```python
    model_name = "azureml://registries/azureml/models/deepset-roberta-base-squad2/versions/17" 
    
    demo_deployment = ManagedOnlineDeployment(
        name="demo",
        endpoint_name=online_endpoint_name,
        model=model_name,
        instance_type="Standard_DS3_v2",
        instance_count=2,
        liveness_probe=ProbeSettings(
            failure_threshold=30,
            success_threshold=1,
            timeout=2,
            period=10,
            initial_delay=1000,
        ),
        readiness_probe=ProbeSettings(
            failure_threshold=10,
            success_threshold=1,
            timeout=10,
            period=10,
            initial_delay=1000,
        ),
    )
    workspace_ml_client.online_deployments.begin_create_or_update(demo_deployment).wait()
    endpoint.traffic = {"demo": 100}
    workspace_ml_client.online_endpoints.begin_create_or_update(endpoint).result()
    ```

## Inference the deployment

1. You need a sample json data to test inferencing. Create `sample_score.json` with the following example. 

    ```python
    {
      "inputs": {
        "question": [
          "Where do I live?",
          "Where do I live?",
          "What's my name?",
          "Which name is also used to describe the Amazon rainforest in English?"
        ],
        "context": [
          "My name is Wolfgang and I live in Berlin",
          "My name is Sarah and I live in London",
          "My name is Clara and I live in Berkeley.",
          "The Amazon rainforest (Portuguese: Floresta Amaz\u00f4nica or Amaz\u00f4nia; Spanish: Selva Amaz\u00f3nica, Amazon\u00eda or usually Amazonia; French: For\u00eat amazonienne; Dutch: Amazoneregenwoud), also known in English as Amazonia or the Amazon Jungle, is a moist broadleaf forest that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi), of which 5,500,000 square kilometres (2,100,000 sq mi) are covered by the rainforest. This region includes territory belonging to nine nations. The majority of the forest is contained within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with minor amounts in Venezuela, Ecuador, Bolivia, Guyana, Suriname and French Guiana. States or departments in four nations contain \"Amazonas\" in their names. The Amazon represents over half of the planet's remaining rainforests, and comprises the largest and most biodiverse tract of tropical rainforest in the world, with an estimated 390 billion individual trees divided into 16,000 species."
        ]
      }
    }
    ```

1. Inference with `sample_score.json`. Change the location of the scoring file in the next code, based on where you saved your sample json file.

    ```python
    scoring_file = "./sample_score.json" 
    response = workspace_ml_client.online_endpoints.invoke(
        endpoint_name=online_endpoint_name,
        deployment_name="demo",
        request_file=scoring_file,
    )
    response_json = json.loads(response)
    print(json.dumps(response_json, indent=2))
    ```


::: zone-end

## Configure autoscaling

To configure autoscaling for deployments, follow these steps:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Locate the Azure resource type `Machine learning online deployment` for the model you just deployed in the resource group of the AI project.
1. Select **Settings** > **Scaling** from the left pane.
1. Select **Custom autoscale** and configure autoscale settings. For more information on autoscaling, see [Autoscale online endpoints](/azure/machine-learning/how-to-autoscale-endpoints) in the Azure Machine Learning documentation. 


## Delete the deployment

To delete deployments in the Foundry portal, select **Delete deployment** on the top panel of the deployment details page.

## Quota considerations

To deploy and perform inferencing with real-time endpoints, you consume Virtual Machine (VM) core quota that Azure assigns to your subscription on a per-region basis. When you sign up for Foundry, you receive a default VM quota for several VM families available in the region. You can continue to create deployments until you reach your quota limit. Once that happens, you can request a quota increase.  

## Related content

- Learn more about what you can do in [Foundry](../what-is-foundry.md)
- Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml)
