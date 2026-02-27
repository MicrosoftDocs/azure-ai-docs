---
title: Consume serverless APIs from a different project or hub
titleSuffix: Microsoft Foundry
description: Learn how to consume serverless APIs from a different project or hub.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/15/2025
manager: nitinme
author: ssalgadodev
ms.author: ssalgado
ms.reviewer: fasantia
reviewer: santiagxf
ms.custom:
  - build-2024
  - serverless
  - ignite-2024
---

# Consume serverless APIs from a different Microsoft Foundry project or hub

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this article, you learn how to configure an existing serverless APIs in a different project or hub than the one that was used to create the deployment.

[!INCLUDE [models-preview](../includes/models-preview.md)]

[Certain models in the model catalog](deploy-models-serverless-availability.md) can be deployed as serverless APIs. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription.

The need to consume a serverless APIs endpoint in a different project or hub than the one that was used to create the deployment might arise in situations such as these:

- You want to centralize your deployments in a given project or hub and consume them from different projects or hubs in your organization.
- You need to deploy a model in a hub in a particular Azure region where serverless deployment for that model is available. However, you need to consume it from another region, where serverless deployment isn't available for the particular models.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- A [Microsoft Foundry hub](create-azure-ai-resource.md), if you're using a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. A **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** does not use a hub. For more information, see [Project types](../what-is-foundry.md#types-of-projects).

- If you don't have one, [create a [!INCLUDE [hub](../includes/hub-project-name.md)]](hub-create-projects.md).

- A model [deployed to a serverless APIs](deploy-models-serverless.md). This article assumes that you previously deployed the **Meta-Llama-3-8B-Instruct** model. To learn how to deploy this model as a serverless API, see [Deploy models as serverless APIs](deploy-models-serverless.md).

- You need to install the following software to work with Foundry:

    # [Foundry portal](#tab/azure-ai-studio)

    You can use any compatible web browser to navigate [Foundry](https://ai.azure.com/?cid=learnDocs).

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

    Once installed, import necessary namespaces:

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import InteractiveBrowserCredential
    from azure.ai.ml.entities import ServerlessEndpoint, ServerlessConnection
    ```

## Create a serverless API endpoint connection

Follow these steps to create a connection:

1. Connect to the project or hub where the endpoint is deployed:

    # [Foundry portal](#tab/azure-ai-studio)

    [!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

    Go to [Foundry](https://ai.azure.com/?cid=learnDocs) and navigate to the project where the endpoint you want to connect to is deployed.

    # [Azure CLI](#tab/cli)

    Configure the CLI to point to the project:

    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<project-name> group=<resource-group> location=<location>
    ```

    # [Python SDK](#tab/python)

    Create a client connected to your project:

    ```python
    client = MLClient(
        credential=InteractiveBrowserCredential(tenant_id="<tenant-id>"),
        subscription_id="<subscription-id>",
        resource_group_name="<resource-group>",
        workspace_name="<project-name>",
    )
    ```

1. Get the endpoint's URL and credentials for the endpoint you want to connect to. In this example, you get the details for an endpoint name **meta-llama3-8b-qwerty**.

    # [Foundry portal](#tab/azure-ai-studio)

    1. From the left sidebar of your project in Foundry portal, go to **My assets** > **Models + endpoints** to see the list of deployments in the project.

    1. Select the deployment you want to connect to.

    1. Copy the values for **Target URI** and **Key**.

    # [Azure CLI](#tab/cli)

    ```azurecli
    az ml serverless-endpoint get-credentials -n meta-llama3-8b-qwerty
    ```

    # [Python SDK](#tab/python)

    ```python
    endpoint_name = "meta-llama3-8b-qwerty"
    endpoint_keys = client.serverless_endpoints.get_keys(endpoint_name)
    print(endpoint_keys.primary_key)
    print(endpoint_keys.secondary_key)
    ```

1. Now, connect to the project or hub **where you want to create the connection**:

    # [Foundry portal](#tab/azure-ai-studio)

    Go to the project where the connection needs to be created to.

    # [Azure CLI](#tab/cli)

    Configure the CLI to point to the project:

    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<project-name> group=<resource-group> location=<location>
    ```

    # [Python SDK](#tab/python)

    Create a client connected to your project:

    ```python
    client = MLClient(
        credential=InteractiveBrowserCredential(tenant_id="<tenant-id>"),
        subscription_id="<subscription-id>",
        resource_group_name="<resource-group>",
        workspace_name="<project-name>",
    )
    ```

1. Create the connection in the project:

    # [Foundry portal](#tab/azure-ai-studio)

    1. From your project in Foundry portal, go to the bottom part of the left sidebar and select **Management center**.

    1. From the left sidebar of the management center, select **Connected resources**.
    
    1. Select **New connection**.

    1. Select **Serverless Model**.

    1. For the **Target URI**, paste the value you copied previously.

    1. For the **Key**, paste the value you copied previously.

    1. Give the connection a name, in this case **meta-llama3-8b-connection**.

    1. Select **Add connection**.

    # [Azure CLI](#tab/cli)

    Create a connection definition:

    __connection.yml__
    
    ```yml
    name: meta-llama3-8b-connection
    type: serverless
    endpoint: https://meta-llama3-8b-qwerty-serverless.inference.ai.azure.com
    api_key: 1234567890qwertyuiop
    ```

    ```azurecli
    az ml connection create -f connection.yml
    ```

    # [Python SDK](#tab/python)

    ```python
    client.connections.create_or_update(ServerlessConnection(
        name="meta-llama3-8b-connection",
        endpoint="https://meta-llama3-8b-qwerty-serverless.inference.ai.azure.com",
        api_key="1234567890qwertyuiop"
    ))
    ```

1. At this point, the connection is available for consumption.

1. To validate that the connection is working:

    1. Return to your project in Foundry portal.

    1. From the left sidebar of your project, go to **Build and customize** > **Prompt flow**.

    1. Select **Create** to create a new flow.

    1. Select **Create** in the **Chat flow** box.

    1. Give your *Prompt flow* a name and select **Create**.

    1. Select the **chat** node from the graph to go to the _chat_ section.

    1. For **Connection**, open the dropdown list to select the connection you just created, in this case **meta-llama3-8b-connection**.

    1. Select **Start compute session** from the top navigation bar, to start a prompt flow automatic runtime.

    1. Select the **Chat** option. You can now send messages and get responses.


## Related content

- [What is Foundry?](../what-is-foundry.md)
- [Azure AI FAQ article](../faq.yml)
