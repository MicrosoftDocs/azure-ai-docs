---
title: Deploy models with managed compute
titleSuffix: Microsoft Foundry
description: "Learn how to deploy large language models using managed compute in Microsoft Foundry. Perform real-time inference for production generative AI applications."
#customer intent: As an Azure AI developer, I want to deploy large language models on managed compute in Microsoft Foundry so that I can enable real-time generative AI applications in production.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - build-2024
  - dev-focus
ms.topic: how-to
ms.date: 01/22/2026
ms.author: mopeakande
ms.reviewer: mopeakande
manager: nitinme
author: msakande
zone_pivot_groups: azure-ai-managed-compute-deployment
ai-usage: ai-assisted

#CustomerIntent: As an Azure AI developer, I want to deploy and perform inference on large language models using managed compute in Microsoft Foundry so that I can make models available for real-time generative AI applications in production environments.
---

# How to deploy and infer with a managed compute deployment

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The Microsoft Foundry portal model catalog offers over 1,600 models that you can deploy using managed compute (also called managed online deployment) for real-time inference in production environments. With managed compute deployments, you get scalable, production-ready infrastructure for your large language models.

In this article, you learn how to deploy models with the managed compute deployment option and perform inference on the deployed model.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).

- If you don't have one, create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. For more information, see [Create a project](hub-create-projects.md).

- Foundry [Models from Partners and Community](../foundry-models/concepts/models-sold-directly-by-azure.md) require access to Azure Marketplace, while Foundry [Models Sold Directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) don't have this requirement. Ensure your Azure subscription has the permissions required to subscribe to model offerings in Azure Marketplace. For more information, see [Enable Azure Marketplace purchases](/azure/cost-management-billing/manage/enable-marketplace-purchases).

- Azure role-based access controls (Azure RBAC) grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).

- Virtual machine (VM) quota in your Azure subscription for the specific VM SKUs needed to run your model. Each deployment consumes VM core quota on a per-region basis. For more information, see [Quota considerations](#quota-considerations), including quota requirements and how to request increases.

- For deployments with Python SDK: Python 3.8 or later installed, including the Azure Machine Learning SDK (`azure-ai-ml`) and Azure Identity library (`azure-identity`).


## Find your model in the model catalog

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. In the **Deployment options** filter, select **Managed compute**.

    [!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

    :::image type="content" source="../media/deploy-models-managed/catalog-filter-managed-compute.png" alt-text="Screenshot of the model catalog interface with the Deployment options filter panel open, on the left showing Managed compute selected, and a grid of available model cards displayed on the right." lightbox="../media/deploy-models-managed/catalog-filter-managed-compute.png"::: 

1. Select a model to open its model card. In this article, you use the model `Phi-4`.


::: zone pivot="ai-foundry-portal"

## Deploy the model

1. On the model's page, select **Use this model**. This action opens the deployment window if the selected model can be deployed to a managed compute only. 

1. Alternatively, if you've selected a model that also supports another deployment option, you land on the "Purchase options" window. Select the **Managed Compute** purchase option to open the deployment window. 

    -  Select the checkbox in the deployment window to use the temporary shared quota. For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

1. The deployment window is pre-filled with some selections and parameter values. You can either keep them or change them as desired. You can also select an existing endpoint for the deployment or create a new one. For this example, specify an instance count of `1` and create a new endpoint for the deployment.

    :::image type="content" source="../media/deploy-models-managed/deployment-configuration.png" alt-text="Screenshot of the deployment configuration dialog showing fields for deployment name, endpoint selection, virtual machine selection, and instance count set to 1, with a Deploy button at the bottom." lightbox="../media/deploy-models-managed/deployment-configuration.png":::

1. Select **Deploy** to create your deployment. The creation process might take a few minutes to complete. When it's complete, the portal opens the model deployment page.

    > [!TIP]
    > To see endpoints deployed to your project, go to the **My assets** section of the left pane and select **Models + endpoints**.

1. Verify your deployment succeeded. On the deployment details page, check that the **Provisioning state** shows **Succeeded** and the **Deployment state** shows **Healthy**. If you see any errors, refer to the [Troubleshooting](#troubleshooting) section.

1. The created endpoint uses key authentication for authorization. To get the keys associated with a given endpoint, follow these steps:

    1. Select the deployment and note the endpoint's Target URI and Key.
    1. Use these credentials to call the deployment and generate predictions.

    The Target URI follows this format: `https://<endpoint-name>.<region>.inference.ml.azure.com/score`
 

## Consume deployments

After you create your deployment, follow these steps to consume it:

1. Select **Models + endpoints** under the **My assets** section in your Foundry project.
1. Select your deployment from the **Model deployments** tab.
1. Go to the **Test** tab for sample inference to the endpoint.
1. Return to the **Details** tab to copy the deployment's "Target URI", which you can use to run inference with code.
1. Go to the **Consume** tab of the deployment to find code samples for consumption.

::: zone-end


::: zone pivot="python-sdk"
6. Copy the model ID from the details page of the model you selected. It looks like this for the selected model: `azureml://registries/azureml/models/Phi-4/versions/8`.


## Deploy the model

1.  Install the Azure Machine Learning SDK.

    ```bash
    pip install azure-ai-ml
    pip install azure-identity
    ```

1. Authenticate with Azure Machine Learning and create a client object. Replace the placeholders with your subscription ID, resource group name, and Foundry project name.

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import InteractiveBrowserCredential
    
    workspace_ml_client = MLClient(
        credential=InteractiveBrowserCredential(),
        subscription_id="your subscription ID goes here",
        resource_group_name="your resource group name goes here",
        workspace_name="your project name goes here",
    )
    ```

    This code authenticates with Azure using interactive browser credentials and creates a client to interact with your Foundry project. When you run this code, a browser window opens for authentication.

    **Reference:** [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient), [InteractiveBrowserCredential](/python/api/azure-identity/azure.identity.interactivebrowsercredential)

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

    This code creates a managed online endpoint with key-based authentication. The operation typically takes 2-3 minutes. When complete, you'll have an endpoint URL where you can deploy models.

    **Reference:** [ManagedOnlineEndpoint](/python/api/azure-ai-ml/azure.ai.ml.entities.managedonlineendpoint), [online_endpoints.begin_create_or_update](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-begin-create-or-update)

1. Create a deployment. Replace the model ID in the next code with the model ID that you copied from the details page of the model you selected in the [Find your model in the model catalog](#find-your-model-in-the-model-catalog) section.

    ```python
    model_name = "azureml://registries/azureml/models/Phi-4/versions/8" 
    
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

    This code deploys the model to your endpoint with 2 Standard_DS3_v2 VM instances. The deployment includes liveness and readiness probes for health monitoring. Traffic is set to 100% for this deployment. The operation takes several minutes to complete. When finished, your model is ready to accept inference requests.

    **Reference:** [ManagedOnlineDeployment](/python/api/azure-ai-ml/azure.ai.ml.entities.managedonlinedeployment), [ProbeSettings](/python/api/azure-ai-ml/azure.ai.ml.entities.probesettings), [online_deployments.begin_create_or_update](/python/api/azure-ai-ml/azure.ai.ml.operations.onlinedeploymentoperations#azure-ai-ml-operations-onlinedeploymentoperations-begin-create-or-update)

## Perform inference on the deployment

1. You need sample JSON data to test inferencing. Create a file named `sample_score.json` in your working directory with the following content: 

    ```json
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

1. Inference with `sample_score.json`. Change the location of the scoring file in the next code, based on where you saved your sample JSON file.

    ```python
    import json
    
    scoring_file = "./sample_score.json" 
    response = workspace_ml_client.online_endpoints.invoke(
        endpoint_name=online_endpoint_name,
        deployment_name="demo",
        request_file=scoring_file,
    )
    response_json = json.loads(response)
    print(json.dumps(response_json, indent=2))
    ```

    This code sends the sample questions and context to your deployed model and prints the answers. The model performs question-answering by extracting relevant text from the provided context. Expected output includes answer text and confidence scores for each question.

    **Reference:** [online_endpoints.invoke](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-invoke)


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

## Troubleshooting

This section provides solutions to common issues you might encounter when deploying models with managed compute.

### Deployment fails with quota exceeded error

**Issue:** You receive an error indicating insufficient quota when creating a deployment.

**Solution:** 
- Check your current quota usage in the Azure portal under your subscription's quota settings
- Request a quota increase through the Azure portal for the specific VM SKU you need
- Consider using a different VM SKU that has available quota
- See [Manage and increase quotas for resources with Azure Machine Learning](/azure/machine-learning/how-to-manage-quotas) for detailed guidance

### Authentication errors when invoking the endpoint

**Issue:** You receive authentication errors (401 Unauthorized) when calling the deployed endpoint.

**Solution:**
- Verify you're using the correct endpoint URI and authentication key from the deployment details page
- Check that the key hasn't been regenerated since you copied it
- Ensure your Azure RBAC permissions haven't changed
- For SDK calls, confirm your credential object is properly initialized

### Deployment provisioning fails or times out

**Issue:** The deployment stays in a provisioning state for an extended period or fails with a timeout error.

**Solution:**
- Check the deployment logs in the Foundry portal for specific error messages
- Verify that your hub's managed network settings allow access to required resources
- Ensure the model ID is correct and the model is still available in the catalog
- Try deploying with a different VM SKU or reducing the instance count

### Model returns unexpected or incorrect responses

**Issue:** The deployed model responds but returns unexpected results.

**Solution:**
- Verify your input data format matches the model's expected schema
- Check the model card documentation for input/output specifications
- Test with the sample data provided in the model's documentation
- Review the request and response in the Test tab of the Foundry portal

For additional troubleshooting assistance, see [Troubleshoot online endpoint deployment](/azure/machine-learning/how-to-troubleshoot-online-endpoints).

## Related content

- Learn more about what you can do in [Foundry](../what-is-foundry.md)
- Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml)
