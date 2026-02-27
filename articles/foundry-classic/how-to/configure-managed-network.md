---
title: How to configure a managed network for a hub
titleSuffix: Microsoft Foundry
description: Learn how to configure a managed network for Microsoft Foundry hubs. A managed network secures your computing resources.
ms.service: azure-ai-foundry
ms.custom: 
  - ignite-2023
  - build-2024
  - devx-track-azurecli
  - ignite-2024
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 02/02/2026
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
zone_pivot_groups: azure-ai-studio-sdk-cli
ai.usage: ai-assisted
#Customer intent: As an administrator, I want to configure a managed network for Microsoft Foundry hubs so that my computing resources are protected.
---

# How to set up a managed network for Microsoft Foundry hubs

[!include [hub](../includes/uses-hub-only.md)]

Network isolation for a [!INCLUDE [hub-based](../includes/hub-project-name.md)] has two parts: accessing a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) hub, and isolating the computing resources in your hub and project (like compute instances, serverless, and managed online endpoints). This article covers the latter. The diagram highlights it. Use the hub's built-in network isolation to protect your computing resources.

:::image type="content" source="../media/how-to/network/azure-ai-network-outbound.svg" alt-text="Diagram that shows Foundry hub network isolation for outbound traffic and managed network configuration." lightbox="../media/how-to/network/azure-ai-network-outbound.png":::

Set up the following network isolation settings:

- Choose a network isolation mode: allow internet outbound or allow only approved outbound.
- If you use Visual Studio Code integration in **allow only approved outbound** mode, create FQDN outbound rules as described in the [use Visual Studio Code](#scenario-use-visual-studio-code) section.
- If you use Hugging Face models in **allow only approved outbound** mode, create FQDN outbound rules as described in the [use Hugging Face models](#scenario-use-hugging-face-models) section.
- If you use one of the open source models in **allow only approved outbound** mode, create FQDN outbound rules as described in the [Models sold directly by Azure](#scenario-models-sold-directly-by-azure) section.

## Prerequisites

Before you start, make sure you have these prerequisites:

# [Azure portal](#tab/portal)

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.

* Register the `Microsoft.Network` resource provider for your Azure subscription. The hub uses this provider to create private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* Use an Azure identity with the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints for the managed virtual network:

    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read`
    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write`

    > [!TIP]
    > The [Azure AI Enterprise Network Connection Approver](/azure/role-based-access-control/built-in-roles/ai-machine-learning) built-in role includes these permissions. Assign this role to the hub's managed identity to approve private endpoint connections.

# [Azure CLI](#tab/azure-cli)

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.

* The __Microsoft.Network__ resource provider must be registered for your Azure subscription. The hub uses this resource provider when creating private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* Use an Azure identity with the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints for the managed virtual network:

    * Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read
    * Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write

    > [!TIP]
    > The [Azure AI Enterprise Network Connection Approver](/azure/role-based-access-control/built-in-roles/ai-machine-learning) built-in role includes these permissions. Assign this role to the hub's managed identity to approve private endpoint connections.

* Install the [Azure CLI](/cli/azure/) and the `ml` extension for the Azure CLI. For more information, see [Install, set up, and use the CLI (v2)](/azure/machine-learning/how-to-configure-cli).

* A Bash-compatible shell for running the CLI examples in this article. For example, use a Linux system or [Windows Subsystem for Linux](/windows/wsl/about).

* The Azure CLI examples in this article use `ws` for the hub name and `rg` for the resource group name. Change these values as needed when you run the commands in your Azure subscription.

# [Python SDK](#tab/python)

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* The __Microsoft.Network__ resource provider must be registered for your Azure subscription. The hub uses this resource provider when creating private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* The Azure identity you use when deploying a managed network requires the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints:

    * Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read
    * Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write

    > [!TIP]
    > The [Azure AI Enterprise Network Connection Approver](/azure/role-based-access-control/built-in-roles/ai-machine-learning) built-in role includes these permissions. Assign this role to the hub's managed identity to approve private endpoint connections.

* The Azure Machine Learning Python SDK v2. For more information on the SDK, see [Install the Python SDK v2 for Azure Machine Learning](/python/api/overview/azure/ai-ml-readme).

* The examples in this article assume that your code begins with the following Python code. It imports the classes required to create a hub with a managed virtual network, sets variables for your Azure subscription and resource group, and creates the `ml_client`. In the following example, replace the placeholder text *`<SUBSCRIPTION_ID>`* and *`<RESOURCE_GROUP>`* with your own values:

    ```python
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import (
        Hub,
        ManagedNetwork,
        IsolationMode,
        ServiceTagDestination,
        PrivateEndpointDestination,
        FqdnDestination
    )
    from azure.identity import DefaultAzureCredential

    # Replace with the values for your Azure subscription and resource group.
    subscription_id = "<SUBSCRIPTION_ID>"
    resource_group = "<RESOURCE_GROUP>"

    # get a handle to the subscription
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
    ```

---

## Configure a managed virtual network to allow internet outbound

> [!TIP]
> Foundry defers creating the managed virtual network until you create a compute resource or start provisioning manually. With automatic creation, it can take about __30 minutes__ to create the first compute resource because it also provisions the network.

# [Azure portal](#tab/portal)

* __Create a new hub__:

    1. Sign in to the [Azure portal](https://portal.azure.com), and select Foundry from the **Create a resource** menu.
    1. Select __+ New Azure AI__.
    1. Enter the required information on the __Basics__ tab.
    1. From the __Networking__ tab, select __Private with Internet Outbound__.
    1. To add an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Outbound rules__ sidebar, enter the following information:
    
        * __Rule name__: A name for the rule. The name must be unique for this hub.
        * __Destination type__: Private Endpoint is the only option when network isolation is Private with Internet Outbound. A hub-managed virtual network doesn't support creating private endpoints for all Azure resource types. For a list of supported resources, see the [Private endpoints](#private-endpoints) section.
        * __Subscription__: The subscription that contains the Azure resource you want to add a private endpoint for.
        * __Resource group__: The resource group that contains the Azure resource you want to add a private endpoint for.
        * __Resource type__: The type of the Azure resource.
        * __Resource name__: The name of the Azure resource.
        * __Sub Resource__: The subresource of the Azure resource type.

        Select __Save__. To add more rules, select __Add user-defined outbound rules__.

    1. Continue creating the hub.

* __Update an existing hub__:

    1. Sign in to the [Azure portal](https://portal.azure.com), and select the hub to enable managed virtual network isolation.
    1. Select __Networking__ > __Private with Internet Outbound__.

        * To _add_ an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Outbound rules__ sidebar, provide the same information as used when creating a hub in the 'Create a new hub' section.

        * To __delete__ an outbound rule, select __delete__ for the rule.

    1. Select __Save__ at the top of the page to apply the changes to the managed virtual network.

# [Azure CLI](#tab/azure-cli)

To configure a managed virtual network that allows internet outbound, use either the `--managed-network allow_internet_outbound` parameter or a YAML configuration file with the following entries:

```yaml
managed_network:
  isolation_mode: allow_internet_outbound
```

Define _outbound rules_ to other Azure services that the hub relies on. These rules define _private endpoints_ that allow an Azure resource to communicate securely with the managed virtual network. The following rule shows how to add a private endpoint to an Azure Blob Storage account. In the following example, replace the placeholder text *`<SUBSCRIPTION_ID>`*, *`<RESOURCE_GROUP>`*, and *`<STORAGE_ACCOUNT_NAME>`* with your own values.

```yml
managed_network:
  isolation_mode: allow_internet_outbound
  outbound_rules:
  - name: added-perule
    destination:
      service_resource_id: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>
      spark_enabled: true
      subresource_target: blob
    type: private_endpoint
```

Configure a managed virtual network by using either the `az ml workspace create` or `az ml workspace update` commands:

* __Create a new hub__:

    The following example creates a new hub. The `--managed-network allow_internet_outbound` parameter configures a managed virtual network for the hub:

    ```azurecli
    az ml workspace create --name ws --resource-group rg --kind hub --managed-network allow_internet_outbound
    ```

    To create a hub by using a YAML file, use the `--file` parameter and specify the YAML file that contains the configuration settings:

    ```azurecli
    az ml workspace create --file hub.yaml --resource-group rg --name ws --kind hub
    ```

    The following YAML example defines a hub with a managed virtual network:

    ```yml
    name: myhub
    location: EastUS
    managed_network:
      isolation_mode: allow_internet_outbound
    ```

* __Update an existing hub__:

    [!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

    The following example updates an existing hub. The `--managed-network allow_internet_outbound` parameter configures a managed virtual network for the hub:

    ```azurecli
    az ml workspace update --name ws --resource-group rg --kind hub --managed-network allow_internet_outbound
    ```

    To update an existing hub by using a YAML file, use the `--file` parameter and specify the YAML file that contains the configuration settings:

    ```azurecli
    az ml workspace update --file hub.yaml --name ws --kind hub --resource-group MyGroup
    ```

    The following YAML example defines a managed virtual network for the hub. It also shows how to add a private endpoint connection to a resource that the hub uses. In this example, it adds a private endpoint for an Azure Blob Storage account. In the following example, replace the placeholder text *`<SUBSCRIPTION_ID>`*, *`<RESOURCE_GROUP>`*, and *`<STORAGE_ACCOUNT_NAME>`* with your own values:

    ```yml
    name: myhub
    managed_network:
      isolation_mode: allow_internet_outbound
      outbound_rules:
      - name: added-perule
        destination:
          service_resource_id: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>
          spark_enabled: true
          subresource_target: blob
        type: private_endpoint
    ```

### References

* [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)
* [az ml workspace update](/cli/azure/ml/workspace#az-ml-workspace-update)

# [Python SDK](#tab/python)

To configure a managed virtual network that allows internet outbound, use the `ManagedNetwork` class with `IsolationMode.ALLOW_INTERNET_OUTBOUND`. Then use the `ManagedNetwork` object to create a new hub or update an existing one. To define _outbound rules_ to Azure services that the hub relies on, use the `PrivateEndpointDestination` class to define a new private endpoint to the service.

* __Create a new hub__:

    The following example creates a new hub named `myhub`, with an outbound rule named `myrule` that adds a private endpoint for an Azure Blob Storage account. In the following example, replace the placeholder text *`<SUBSCRIPTION_ID>`*, *`<RESOURCE_GROUP>`*, and *`<STORAGE_ACCOUNT_NAME>`* with your own values:

    ```python
    from azure.ai.ml.entities import ManagedNetwork, IsolationMode, Hub, PrivateEndpointDestination

    # Basic managed VNet configuration
    network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_INTERNET_OUTBOUND)

    # Hub configuration
    ws = Hub(
        name="myhub",
        location="eastus",
        managed_network=network
    )

    # Example private endpoint to Azure Blob Storage
    rule_name = "myrule"
    service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
    subresource_target = "blob"
    spark_enabled = True

    # Add the outbound rule
    ws.managed_network.outbound_rules = [PrivateEndpointDestination(
        name=rule_name, 
        service_resource_id=service_resource_id, 
        subresource_target=subresource_target, 
        spark_enabled=spark_enabled)]

    # Create the hub
    ws = ml_client.workspaces.begin_create(ws).result()
    ```

    ### References

    * [ManagedNetwork](/python/api/azure-ai-ml/azure.ai.ml.entities.managednetwork)
    * [IsolationMode](/python/api/azure-ai-ml/azure.ai.ml.entities.isolationmode)
    * [Hub](/python/api/azure-ai-ml/azure.ai.ml.entities.hub)
    * [PrivateEndpointDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination)

* __Update an existing hub__:

    The following example demonstrates how to create a managed virtual network for an existing hub named `myhub`:
    
    ```python
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml.entities import ManagedNetwork, IsolationMode, PrivateEndpointDestination

    # Get the existing hub
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, "myhub")
    ws = ml_client.workspaces.get(name="myhub")
    
    # Basic managed VNet configuration
    ws.managed_network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_INTERNET_OUTBOUND)

    # Example private endpoint outbound to a blob
    rule_name = "myrule"
    service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
    subresource_target = "blob"
    spark_enabled = True

    # Add the outbound rule
    ws.managed_network.outbound_rules = [PrivateEndpointDestination(
        name=rule_name, 
        service_resource_id=service_resource_id, 
        subresource_target=subresource_target, 
        spark_enabled=spark_enabled)]

    # Update the hub
    ml_client.workspaces.begin_update(ws)
    ```

    ### References

    * [ManagedNetwork](/python/api/azure-ai-ml/azure.ai.ml.entities.managednetwork)
    * [IsolationMode](/python/api/azure-ai-ml/azure.ai.ml.entities.isolationmode)
    * [PrivateEndpointDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination)
    * [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)
---

## Configure a managed virtual network to allow only approved outbound

> [!TIP]
> Azure automatically sets up the managed VNet when you create a compute resource. If you allow automatic creation, the first compute resource can take about 30 minutes to create because the network also needs to set up. If you configure FQDN outbound rules, the first FQDN rule adds about 10 minutes to the setup time.

# [Azure portal](#tab/portal)

* __Create a new hub__:

    1. Sign in to the [Azure portal](https://portal.azure.com), and choose Foundry from the Create a resource menu.
    1. Select __+ New Azure AI__.
    1. Provide the required information on the __Basics__ tab.
    1. From the __Networking__ tab, select __Private with Approved Outbound__.

    1. To add an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Outbound rules__ sidebar, provide the following information:
    
        * __Rule name__: A name for the rule. The name must be unique for this hub.
        * __Destination type__: Private Endpoint, Service Tag, or FQDN. Service Tag and FQDN are only available when the network isolation is private with approved outbound.

        If the destination type is __Private Endpoint__, enter the following information:

        * __Subscription__: The subscription that contains the Azure resource you want to add a private endpoint for.
        * __Resource group__: The resource group that contains the Azure resource you want to add a private endpoint for.
        * __Resource type__: The type of the Azure resource.
        * __Resource name__: The name of the Azure resource.
    * __Sub Resource__: The sub resource of the Azure resource type.

    > [!TIP]
    > The hub's managed VNet doesn't support private endpoints for all Azure resource types. For a list of supported resources, see the [Private endpoints](#private-endpoints) section.

    If the destination type is __Service Tag__, enter the following information:

    * __Service tag__: The service tag to add to the approved outbound rules.
    * __Protocol__: The protocol to allow for the service tag.
    * __Port ranges__: The port ranges to allow for the service tag.

    If the destination type is __FQDN__, enter the following information:

    * __FQDN destination__: The fully qualified domain name to add to the approved outbound rules.

        Select __Save__ to save the rule. To add more rules, select __Add user-defined outbound rules__ again.

    1. Continue creating the hub as usual.

* __Update an existing hub__:

    1. Sign in to the [Azure portal](https://portal.azure.com), and select the hub that you want to enable managed virtual network isolation for.
    1. Select __Networking__ > __Private with Approved Outbound__.

        * To _add_ an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Outbound rules__ sidebar, enter the same information as when creating a hub in the previous 'Create a new hub' section.

        * To __delete__ an outbound rule, select __delete__ for the rule.

    1. Select __Save__ at the top of the page to save the changes to the managed virtual network.

# [Azure CLI](#tab/azure-cli)

To configure a managed virtual network that allows only approved outbound communication, use either the `--managed-network allow_only_approved_outbound` parameter or a YAML configuration file that contains the following entries:

```yml
managed_network:
  isolation_mode: allow_only_approved_outbound
```

You can also define _outbound rules_ for approved outbound communication. Create an outbound rule of type `service_tag`, `fqdn`, or `private_endpoint`. The following example adds a private endpoint to an Azure Blob resource, a service tag for Azure Data Factory, and an FQDN for `pypi.org`. In the following example, replace the placeholder text *`<SUBSCRIPTION_ID>`*, *`<RESOURCE_GROUP>`*, and *`<STORAGE_ACCOUNT_NAME>`* with your values.

> [!IMPORTANT]
> * Adding an outbound rule for a service tag or FQDN is valid only when the managed VNet is configured to `allow_only_approved_outbound`.
> * If you add outbound rules, Microsoft can't guarantee protection against data exfiltration.

```yaml
managed_network:
  isolation_mode: allow_only_approved_outbound
  outbound_rules:
  - name: added-servicetagrule
    destination:
      port_ranges: 80, 8080
      protocol: TCP
      service_tag: DataFactory
    type: service_tag
  - name: add-fqdnrule
    destination: 'pypi.org'
    type: fqdn
  - name: added-perule
    destination:
      service_resource_id: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>
      spark_enabled: true
      subresource_target: blob
    type: private_endpoint
```

You can configure a managed virtual network by using either the `az ml workspace create` or `az ml workspace update` commands:

* __Create a new hub__:

    The following example uses the `--managed-network allow_only_approved_outbound` parameter to configure the managed virtual network:

    ```azurecli
    az ml workspace create --name ws --resource-group rg --kind hub --managed-network allow_only_approved_outbound
    ```

    The following YAML file defines a hub with a managed virtual network:

    ```yml
    name: myhub
    location: EastUS
    managed_network:
      isolation_mode: allow_only_approved_outbound
    ```

    To create a hub by using the YAML file, use the `--file` parameter:

    ```azurecli
    az ml workspace create --file hub.yaml --resource-group rg --name ws --kind hub
    ```

* __Update an existing hub__

    [!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

    The following example uses the `--managed-network allow_only_approved_outbound` parameter to configure the managed virtual network for an existing hub:

    ```azurecli
    az ml workspace update --name ws --resource-group rg --kind hub --managed-network allow_only_approved_outbound
    ```

    The following YAML file defines a managed virtual network for the hub and shows how to add approved outbound rules. In this example, outbound rules are added for a service tag, an FQDN, and a private endpoint:

    ```yaml
    name: myhub_dep
    managed_network:
      isolation_mode: allow_only_approved_outbound
      outbound_rules:
      - name: added-servicetagrule
        destination:
          port_ranges: 80, 8080
          protocol: TCP
          service_tag: DataFactory
        type: service_tag
      - name: add-fqdnrule
        destination: 'pypi.org'
        type: fqdn
      - name: added-perule
        destination:
          service_resource_id: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>
          spark_enabled: true
          subresource_target: blob
        type: private_endpoint
    ```

### References

* [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)
* [az ml workspace update](/cli/azure/ml/workspace#az-ml-workspace-update)

# [Python SDK](#tab/python)

To configure a managed virtual network that allows only approved outbound communication, use the `ManagedNetwork` class to define a network with `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`. Use the `ManagedNetwork` object to create a new hub or update an existing one. To define _outbound rules_, use the following classes:

| Destination | Class |
| ----------- | ----- |
| __Azure service that the hub relies on__ | `PrivateEndpointDestination` |
| __Azure service tag__ | `ServiceTagDestination` |
| __Fully qualified domain name (FQDN)__ | `FqdnDestination` |

* __Create a new hub__:

    The following example creates a new hub named `myhub`, with several outbound rules:

    * `myrule` - Adds a private endpoint for an Azure Blob store.
    * `datafactory` - Adds a service tag rule to communicate with Azure Data Factory.

    > [!IMPORTANT]
    > * Add an outbound rule for a service tag or FQDN only when you configure the managed VNet to `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`.
    > * If you add outbound rules, Microsoft can't guarantee protection against data exfiltration.

    ```python
    from azure.ai.ml.entities import ManagedNetwork, IsolationMode, Hub, PrivateEndpointDestination, ServiceTagDestination, FqdnDestination

    # Basic managed VNet configuration
    network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND)

    # Hub configuration
    ws = Hub(
        name="myhub",
        location="eastus",
        managed_network=network
    )

    # Append some rules
    ws.managed_network.outbound_rules = []
    # Example private endpoint outbound to a blob
    rule_name = "myrule"
    service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
    subresource_target = "blob"
    spark_enabled = True
    ws.managed_network.outbound_rules.append(
        PrivateEndpointDestination(
            name=rule_name, 
            service_resource_id=service_resource_id, 
            subresource_target=subresource_target, 
            spark_enabled=spark_enabled
        )
    )

    # Example service tag rule
    rule_name = "datafactory"
    service_tag = "DataFactory"
    protocol = "TCP"
    port_ranges = "80, 8080-8089"
    ws.managed_network.outbound_rules.append(
        ServiceTagDestination(
            name=rule_name, 
            service_tag=service_tag, 
            protocol=protocol, 
            port_ranges=port_ranges
        )
    )

    # Example FQDN rule
    ws.managed_network.outbound_rules.append(
        FqdnDestination(
            name="fqdnrule", 
            destination="pypi.org"
        )
    )

    # Create the hub
    ws = ml_client.workspaces.begin_create(ws).result()
    ```

    ### References

    * [ManagedNetwork](/python/api/azure-ai-ml/azure.ai.ml.entities.managednetwork)
    * [IsolationMode](/python/api/azure-ai-ml/azure.ai.ml.entities.isolationmode)
    * [Hub](/python/api/azure-ai-ml/azure.ai.ml.entities.hub)
    * [PrivateEndpointDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination)
    * [ServiceTagDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.servicetagdestination)
    * [FqdnDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.fqdndestination)

* __Update an existing hub__:

    The following example shows how to configure a managed virtual network for an existing hub named `myhub`. It also adds several outbound rules:

    * `myrule` - Adds a private endpoint for an Azure Blob store.
    * `datafactory` - Adds a service tag rule to communicate with Azure Data Factory.

    > [!TIP]
    > You can add an outbound rule for a service tag or FQDN only when you configure the managed VNet to use `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`.
    
    ```python
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml.entities import ManagedNetwork, IsolationMode, PrivateEndpointDestination, ServiceTagDestination, FqdnDestination

    # Get the existing hub
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, "myhub")
    ws = ml_client.workspaces.get()

    # Basic managed VNet configuration
    ws.managed_network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND)

    # Append some rules
    ws.managed_network.outbound_rules = []
    # Example private endpoint outbound to a blob
    rule_name = "myrule"
    service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
    subresource_target = "blob"
    spark_enabled = True
    ws.managed_network.outbound_rules.append(
        PrivateEndpointDestination(
            name=rule_name, 
            service_resource_id=service_resource_id, 
            subresource_target=subresource_target, 
            spark_enabled=spark_enabled
        )
    )

    # Example service tag rule
    rule_name = "datafactory"
    service_tag = "DataFactory"
    protocol = "TCP"
    port_ranges = "80, 8080-8089"
    ws.managed_network.outbound_rules.append(
        ServiceTagDestination(
            name=rule_name, 
            service_tag=service_tag, 
            protocol=protocol, 
            port_ranges=port_ranges
        )
    )

    # Example FQDN rule
    ws.managed_network.outbound_rules.append(
        FqdnDestination(
            name="fqdnrule", 
            destination="pypi.org"
        )
    )

    # Update the hub
    ml_client.workspaces.begin_update(ws)
    ```

    ### References

    * [ManagedNetwork](/python/api/azure-ai-ml/azure.ai.ml.entities.managednetwork)
    * [IsolationMode](/python/api/azure-ai-ml/azure.ai.ml.entities.isolationmode)
    * [PrivateEndpointDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination)
    * [ServiceTagDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.servicetagdestination)
    * [FqdnDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.fqdndestination)
    * [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)

---

## Manually provision a managed VNet

The managed virtual network is automatically provisioned when you create a compute instance. When you rely on automatic provisioning, it can take around **30 minutes** to create the first compute instance as it also provisions the network. If you configure FQDN outbound rules (only available with allow only approved mode), the first FQDN rule adds around **10 minutes** to the provisioning time. If you have a large set of outbound rules to be provisioned in the managed network, it can take longer for provisioning to complete. The increased provisioning time can cause your first compute instance creation to time out.

To reduce wait time and avoid timeouts, manually set up the managed network. Wait for provisioning to complete before you create a compute instance.

Alternatively, use the `provision_network_now` flag to set up the managed network during hub creation.

> [!NOTE]
> To deploy a model to managed compute, you must manually provision the managed network, or create a compute instance first. Creating a compute instance automatically provisions the managed network. 

# [Azure portal](#tab/portal)

During workspace creation, select __Provision managed network proactively at creation__ to set up the managed network. Billing starts for network resources, like private endpoints, after the virtual network is set up. This option is available only during workspace creation.

# [Azure CLI](#tab/azure-cli)

The following example shows how to provision a managed virtual network during hub creation. 
    
```azurecli
az ml workspace create -n my_ai_hub_name -g my_resource_group --kind hub --managed-network AllowInternetOutbound --provision-network-now true
```

The following example shows how to provision a managed virtual network.

```azurecli
az ml workspace provision-network -g my_resource_group -n my_ai_hub_name
```

To check that provisioning is complete, run the following command:

```azurecli
az ml workspace show -n my_ai_hub_name -g my_resource_group --query managed_network
```

### References

* [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)
* [az ml workspace provision-network](/cli/azure/ml/workspace#az-ml-workspace-provision-network)
* [az ml workspace show](/cli/azure/ml/workspace#az-ml-workspace-show)

# [Python SDK](#tab/python)

Use the SDK to provision a managed virtual network, and then check its status.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

subscription_id = "00000000-0000-0000-0000-000000000000"
resource_group = "my_resource_group"
workspace_name = "my_ai_hub_name"

ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace_name=workspace_name)

# Start provisioning the managed network for the workspace.
provision_result = ml_client.workspaces.begin_provision_network(workspace_name=workspace_name).result()

# Check the managed network status.
ws = ml_client.workspaces.get(name=workspace_name)
print(ws.managed_network.status)
```

### References

* [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)
* [begin_provision_network](/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations#azure-ai-ml-operations-workspaceoperations-begin-provision-network)

--- 

## Manage outbound rules

# [Azure portal](#tab/portal)

1. Sign in to the [Azure portal](https://portal.azure.com), and select the hub that you want to enable managed virtual network isolation for.
1. Select __Networking__. The __Foundry Outbound access__ section lets you manage outbound rules.

* To add an outbound rule, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Azure AI outbound rules__ sidebar, enter the required values.

* To __enable__ or __disable__ a rule, use the toggle in the __Active__ column.

* To __delete__ an outbound rule, select __delete__ for the rule.

# [Azure CLI](#tab/azure-cli)

In the following commands, replace the placeholder text *`<workspace-name>`*, *`<resource-group>`*, and *`<rule-name>`* with your values. To list managed virtual network outbound rules for a hub, run:

```azurecli
az ml workspace outbound-rule list --workspace-name <workspace-name> --resource-group <resource-group>
```

To view the details of a managed virtual network outbound rule, run:

```azurecli
az ml workspace outbound-rule show --rule <rule-name> --workspace-name <workspace-name> --resource-group <resource-group>
```

To remove an outbound rule from the managed virtual network, run:

```azurecli
az ml workspace outbound-rule remove --rule <rule-name> --workspace-name <workspace-name> --resource-group <resource-group>
```

### References

* [az ml workspace outbound-rule list](/cli/azure/ml/workspace/outbound-rule#az-ml-workspace-outbound-rule-list)
* [az ml workspace outbound-rule show](/cli/azure/ml/workspace/outbound-rule#az-ml-workspace-outbound-rule-show)
* [az ml workspace outbound-rule remove](/cli/azure/ml/workspace/outbound-rule#az-ml-workspace-outbound-rule-remove)

# [Python SDK](#tab/python)

The following example shows how to manage outbound rules for a hub named `myhub`. In the example, replace the placeholder text *`<some-rule-name>`* with your rule name:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Connect to the hub
ws_name = "myhub"
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace_name=ws_name)

# Specify the rule name
rule_name = "<some-rule-name>"

# Get a rule by name
rule = ml_client._workspace_outbound_rules.get(resource_group, ws_name, rule_name)

# List rules for a hub
rule_list = ml_client._workspace_outbound_rules.list(resource_group, ws_name)

# Delete a rule from a hub
ml_client._workspace_outbound_rules.begin_remove(resource_group, ws_name, rule_name).result()
```

### References

* [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)

---

## Network isolation architecture and isolation modes

When you enable managed virtual network isolation, you create a managed virtual network for the hub. Managed compute resources you create for the hub automatically use this managed virtual network. The managed virtual network can use private endpoints for Azure resources your hub uses, like Azure Storage, Azure Key Vault, and Azure Container Registry. 

Choose one of three outbound modes for the managed virtual network:

| Outbound mode | Description | Scenarios |
| ----- | ----- | ----- |
| Allow internet outbound | Allow all internet outbound traffic from the managed virtual network. | You want unrestricted access to machine learning resources on the internet, such as Python packages or pretrained models.<sup>1</sup> |
| Allow only approved outbound | Use service tags to allow outbound traffic. | * You want to minimize the risk of data exfiltration, but you need to prepare all required machine learning artifacts in your private environment.<br/>* You want to configure outbound access to an approved list of services, service tags, or fully qualified domain names (FQDNs). |
| Disabled | Inbound and outbound traffic isn't restricted. | You want public inbound and outbound from the hub. |

<sup>1</sup> You can use outbound rules with the _allow only approved outbound_ mode to achieve the same result as using _allow internet outbound_. The differences are:

* Always use private endpoints to access Azure resources. 
* You must add rules for each outbound connection you need to allow.
* Adding fully qualified domain name (FQDN) outbound rules increases your costs because this rule type uses Azure Firewall. If you use FQDN outbound rules, charges for Azure Firewall are included in your billing. For more information, see [Pricing](#pricing).
* The default rules for _allow only approved outbound_ are designed to minimize the risk of data exfiltration. Any outbound rules you add might increase your risk.

The managed virtual network is preconfigured with [required default rules](#list-of-required-rules). The hub also configures private endpoint connections to your hub, the hub's default storage account, container registry, and key vault when those resources are set to private or when the isolation mode is set to allow only approved outbound. After you choose an isolation mode, add any other outbound rules you need.

The following diagram shows a managed virtual network configured to _allow internet outbound_:

:::image type="content" source="../media/how-to/network/internet-outbound.svg" alt-text="Diagram that shows a managed virtual network configured to allow internet outbound traffic." lightbox="../media/how-to/network/internet-outbound.png":::

The following diagram shows a managed virtual network configured to _allow only approved outbound_:

> [!NOTE]
> In this configuration, the storage, key vault, and container registry that the hub uses are set to private. Because they're private, the hub uses private endpoints to reach them.

:::image type="content" source="../media/how-to/network/only-approved-outbound.svg" alt-text="Diagram that shows a managed virtual network configured to allow only approved outbound traffic." lightbox="../media/how-to/network/only-approved-outbound.png":::

> [!NOTE]
> To access a private storage account from a public Foundry hub, use Foundry from within your storage account's virtual network. Accessing Foundry from within the virtual network ensures that you can perform actions such as uploading files to the private storage account. The private storage account is independent of your Foundry hub's networking settings. See [Configure Azure Storage firewalls and virtual networks](/azure/storage/common/storage-network-security).

## List of required rules

> [!TIP]
> These rules are automatically added to the managed virtual network (VNet).

__Private endpoints__:
* When you set the isolation mode for the managed virtual network to `Allow internet outbound`, Foundry automatically creates required private endpoint outbound rules from the managed virtual network for the hub and associated resources with public network access disabled (Azure Key Vault, storage account, Azure Container Registry, and hub).
* When you set the isolation mode for the managed virtual network to `Allow only approved outbound`, Foundry automatically creates required private endpoint outbound rules from the managed virtual network for the hub and associated resources regardless of the public network access setting for those resources (Azure Key Vault, storage account, Azure Container Registry, and hub).

Foundry requires a set of service tags for private networking. Don't replace the required service tags. The following table describes each required service tag and its purpose within Foundry. 

| Service tag rule | Inbound or outbound | Purpose |
| ----------- | ----- | ----- |
| `AzureMachineLearning` | Inbound | Create, update, and delete Foundry compute instances and clusters. |  
| `AzureMachineLearning`| Outbound | Using Azure Machine Learning services. Python IntelliSense in notebooks uses port 18881. Creating, updating, and deleting an Azure Machine Learning compute instance uses port 5831. |
| `AzureActiveDirectory` | Outbound | Authentication using Microsoft Entra ID. |
| `BatchNodeManagement.region` | Outbound | Communication with the Azure Batch back end for Foundry compute instances and clusters. |
| `AzureResourceManager` | Outbound | Create Azure resources by using Foundry, Azure CLI, and the Microsoft Foundry SDK. |
| `AzureFrontDoor.FirstParty` | Outbound | Access Docker images provided by Microsoft. |
| `MicrosoftContainerRegistry` | Outbound | Access Docker images provided by Microsoft. Set up the Foundry router for Azure Kubernetes Service. |        
| `AzureMonitor` | Outbound | Send logs and metrics to Azure Monitor. Only needed if you haven't secured Azure Monitor for the workspace. This outbound rule also logs information for support incidents. |
| `VirtualNetwork` | Outbound | Required when private endpoints are present in the virtual network or peered virtual networks. |

## List of scenario-specific outbound rules

### Scenario: Access public machine learning packages

To install Python packages for training and deployment, add outbound FQDN rules to allow traffic to the following host names:

> [!NOTE]
> This list covers common hosts for Python resources on the internet. If you need access to a GitHub repository or another host, identify and add the hosts required for your scenario.

| __Host name__ | __Purpose__ |
| ---- | ---- |
| `anaconda.com`<br>`*.anaconda.com` | Used to install default packages. |
| `*.anaconda.org` | Used to get repo data. |
| `pypi.org` | Lists dependencies from the default index if user settings don't overwrite it. If you overwrite the index, also allow `*.pythonhosted.org`. |
| `pytorch.org`<br>`*.pytorch.org` | Used by some examples based on PyTorch. |
| `*.tensorflow.org` | Used by some examples based on TensorFlow. |

### Scenario: Use Visual Studio Code
Visual Studio Code relies on specific hosts and ports to establish a remote connection.

#### Hosts

Use these hosts to install Visual Studio Code packages and establish a remote connection to your project's compute instances.

> [!NOTE]
> This list doesn't include all the hosts required for all Visual Studio Code resources on the internet. For example, if you need access to a GitHub repository or other host, you must identify and add the required hosts for that scenario. For a complete list of host names, see [Network Connections in Visual Studio Code](https://code.visualstudio.com/docs/setup/network).

| __Host name__ | __Purpose__ |
| ---- | ---- |
| `*.vscode.dev`<br>`*.vscode-unpkg.net`<br>`*.vscode-cdn.net`<br>`*.vscodeexperiments.azureedge.net`<br>`default.exp-tas.com` | Required to access VS Code for the Web (vscode.dev). |
| `code.visualstudio.com` | Required to download and install VS Code desktop. This host isn't required for VS Code Web. |
| `update.code.visualstudio.com`<br>`*.vo.msecnd.net` | Downloads VS Code Server components to the compute instance during setup scripts. |
| `marketplace.visualstudio.com`<br>`vscode.blob.core.windows.net`<br>`*.gallerycdn.vsassets.io` | Required to download and install VS Code extensions. These hosts enable the remote connection to compute instances. For more information, see [Get started with Foundry projects in VS Code](./develop/get-started-projects-vs-code.md). |
| `vscode.download.prss.microsoft.com` | Serves as the Visual Studio Code download CDN. |

#### Ports
Allow network traffic to ports 8704 to 8710. The VS Code Server selects the first available port in this range.

### Scenario: Use Hugging Face models

To use Hugging Face models with the hub, add outbound FQDN rules to allow traffic to the following hosts:

* `docker.io`
* `*.docker.io`
* `*.docker.com`
* `production.cloudflare.docker.com`
* `cdn.auth0.com`
* `huggingface.co`
* `cas-bridge.xethub.hf.co`
* `cdn-lfs.huggingface.co`

### Scenario: Models sold directly by Azure

These models install dependencies at runtime. Add outbound FQDN rules to allow traffic to the following hosts:

* `*.anaconda.org`
* `*.anaconda.com`
* `anaconda.com`
* `pypi.org`
* `*.pythonhosted.org`
* `*.pytorch.org`
* `pytorch.org`

## Private endpoints

Azure services currently support private endpoints for the following services:

* Foundry hub
* Azure AI Search
* Foundry Tools
* Azure API Management
    * Supports only the Classic tier without VNet injection and the Standard V2 tier with virtual network integration. For more on API Management virtual networks, see [Virtual Network Concepts](/azure/api-management/virtual-network-concepts).
* Azure Container Registry
* Azure Cosmos DB (all subresource types)
* Azure Data Factory
* Azure Database for MariaDB
* Azure Database for MySQL
* Azure Database for PostgreSQL Single Server
* Azure Database for PostgreSQL Flexible Server
* Azure Databricks
* Azure Event Hubs
* Azure Key Vault
* Azure Machine Learning
* Azure Machine Learning registries
* Azure Cache for Redis
* Azure SQL Server
* Azure Storage (all subresource types)
* Application Insights (through [PrivateLinkScopes](/azure/azure-monitor/logs/private-link-configure#create-azure-monitor-private-link-scope-ampls))


When you create a private endpoint, you specify the _resource type_ and _subresource_ that the endpoint connects to. Some resources have multiple types and subresources. For more information, see [what is a private endpoint](/azure/private-link/private-endpoint-overview).

When you create a private endpoint for hub dependency resources, such as Azure Storage, Azure Container Registry, and Azure Key Vault, the resource can be in a different Azure subscription. However, the resource must be in the same tenant as the hub.

If you select one of the Azure resources listed earlier as the target resource, the service automatically creates a private endpoint for the connection. Provide a valid target ID for the private endpoint. For a connection, the target ID can be the Azure Resource Manager ID of a parent resource. Include the target ID in the connection's target or in `metadata.resourceid`. For more on connections, see [How to add a new connection in Foundry portal](connections-add.md).

### Approval of private endpoints

To establish private endpoint connections in managed virtual networks by using Foundry, the workspace managed identity (system-assigned or user-assigned) and the user identity that creates the private endpoint must have permission to approve the private endpoint connections on the target resources. Previously, the Foundry service granted this permission through automatic role assignments. Because of security concerns with automatic role assignments, starting April 30, 2025, the service discontinues this automatic permission grant logic. Assign the [Azure AI Enterprise Network Connection Approver role](/azure/role-based-access-control/built-in-roles/ai-machine-learning) or a custom role with the necessary private endpoint connection permissions on the target resource types, and grant this role to the Foundry hub's managed identity to let Foundry approve private endpoint connections to the target Azure resources.

Here's the list of private endpoint target resource types covered by the Azure AI Enterprise Network Connection Approver role:

* Azure Application Gateway
* Azure Monitor
* Azure AI Search
* Azure Event Hubs
* Azure SQL Database
* Azure Storage
* Azure Machine Learning workspace
* Azure Machine Learning registry
* Foundry
* Azure Key Vault
* Azure Cosmos DB
* Azure Database for MySQL
* Azure Database for PostgreSQL
* Foundry Tools
* Azure Cache for Redis
* Azure Container Registry
* Azure API Management

To create private endpoint outbound rules for target resource types not covered by the Azure AI Enterprise Network Connection Approver role, such as Azure Data Factory, Azure Databricks, and Azure Function Apps, use a custom, scoped-down role defined only by the actions necessary to approve private endpoint connections on the target resource types.

To create private endpoint outbound rules for default workspace resources, workspace creation grants the required permissions through role assignments, so you don't need to take any additional action.

## Select an Azure Firewall version to allow only approved outbound

Azure Firewall deploys when you add an outbound FQDN rule in the **allow only approved outbound** mode. Azure Firewall charges are added to your bill. By default, a __Standard__ version of Azure Firewall is created. Or select the __Basic__ version. Change the firewall version at any time. To learn which version fits your needs, go to [Choose the right Azure Firewall version](/azure/firewall/choose-firewall-sku).

> [!IMPORTANT]
> Azure Firewall isn't created until you add an outbound FQDN rule. For pricing details, see [Azure Firewall pricing](https://azure.microsoft.com/pricing/details/azure-firewall/) and view prices for the Standard version.

Use these tabs to see how to select the firewall version for your managed virtual network.

# [Azure portal](#tab/portal)

After you select the **allow only approved outbound** mode, the option to select the Azure Firewall version (SKU) appears. Select __Standard__ or __Basic__. Select **Save**.

# [Azure CLI](#tab/azure-cli)

To set the firewall version by using Azure CLI, use a YAML file and specify `firewall_sku`. The following example sets the firewall SKU to `basic`:

```yaml
name: test-ws
resource_group: test-rg
location: eastus2 
managed_network:
  isolation_mode: allow_only_approved_outbound
  outbound_rules:
  - category: required
    destination: 'contoso.com'
    name: contosofqdn
    type: fqdn
  firewall_sku: basic
tags: {}
```

# [Python SDK](#tab/python)

To set the firewall version by using the Python SDK, set the `firewall_sku` property of the `ManagedNetwork` object. The following example sets the firewall SKU to `basic`:

```python
from azure.ai.ml.entities import ManagedNetwork, IsolationMode

network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND,
                         firewall_sku='basic')
```

### References

* [ManagedNetwork](/python/api/azure-ai-ml/azure.ai.ml.entities.managednetwork)
* [IsolationMode](/python/api/azure-ai-ml/azure.ai.ml.entities.isolationmode)
---

## Pricing

The hub managed virtual network feature is free, but you pay for the following resources that the managed virtual network uses:

* Azure Private Link - Private endpoints that secure communication between the managed virtual network and Azure resources use Azure Private Link. For pricing, see [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link/).
* FQDN outbound rules - Azure Firewall enforces these rules. If you use outbound FQDN rules, Azure Firewall charges appear on your bill. The Standard version of Azure Firewall is used by default. To select the Basic version, see [Select an Azure Firewall version](#select-an-azure-firewall-version-to-allow-only-approved-outbound). Azure Firewall is provisioned per hub.

    > [!IMPORTANT]
    > Azure Firewall isn't created until you add an outbound FQDN rule. If you don't use FQDN rules, you aren't charged for Azure Firewall. For pricing, see [Azure Firewall pricing](https://azure.microsoft.com/pricing/details/azure-firewall/).

## Limitations

* Foundry supports managed virtual network isolation for compute resources. Foundry doesn't support bringing your own virtual network for compute isolation. This scenario differs from the Azure Virtual Network required to access Foundry from an on-premises network.
* After you enable managed virtual network isolation, you can't disable it.
* The managed virtual network uses a private endpoint to connect to private resources. You can't use a private endpoint and a service endpoint on the same Azure resource, like a storage account. Use private endpoints for all scenarios.
* When you delete Foundry, the service deletes the managed virtual network.
* With __allow only approved outbound__, Foundry enables data exfiltration protection automatically. If you add other outbound rules, like FQDNs, Microsoft can't guarantee protection against data exfiltration to those destinations.
* FQDN outbound rules increase managed virtual network cost because they use Azure Firewall. For more information, see [Pricing](#pricing).
* FQDN outbound rules support only ports 80 and 443.
* To disable a compute instance's public IP address, add a private endpoint to a hub.
* For a compute instance in a managed network, run `az ml compute connect-ssh` to connect over SSH.
* If your managed network is configured to __allow only approved outbound__, you can't use an FQDN rule to access Azure Storage accounts. Use a private endpoint instead.

## Related content

- [Create Foundry hub and project using the SDK](./develop/create-hub-project-sdk.md)
- [Access on-premises resources from Foundry](access-on-premises-resources.md)
