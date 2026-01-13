---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* Install the [Azure CLI](/cli/azure/) and the `ml` extension for Microsoft Foundry:

    ```azurecli
    az extension add -n ml
    ```

* Identify the following information:

  * Your Azure subscription ID.

  * Your Foundry Tools resource name.

  * The resource group where the Foundry Tools resource is deployed.
    
    
### Add a connection

To add a model, you first need to identify the model that you want to deploy. You can query the available models as follows:

1. Log in into your Azure subscription:

    ```azurecli
    az login
    ```

2. Configure the CLI to point to the project:

    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<project-name> group=<resource-group> location=<location>
    ```

3. Create a connection definition:

    __connection.yml__

    ```yml
    name: <connection-name>
    type: aiservices
    endpoint: https://<ai-services-resourcename>.services.ai.azure.com
    api_key: <resource-api-key>
    ```
4. Create the connection:

    ```azurecli
    az ml connection create -f connection.yml
    ```
5. At this point, the connection is available for consumption.