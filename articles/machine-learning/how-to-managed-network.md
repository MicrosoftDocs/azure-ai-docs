---
title: Managed virtual network isolation
titleSuffix: Azure Machine Learning
description: Use managed virtual network isolation for network security with Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.reviewer: shshubhe
ms.author: scottpolly
author: s-polly
ms.date: 05/23/2025
ms.topic: how-to
zone_pivot_groups: azureml-portal-cli-python
ms.custom:
  - build-2023
  - devx-track-azurecli
  - ignite-2023
  - build-2024
  - ignite-2024
  - sfi-image-nochange
---

# Workspace Managed Virtual Network Isolation

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning provides support for managed virtual network (managed virtual network) isolation. Managed virtual network isolation streamlines and automates your network isolation configuration with a built-in, workspace-level Azure Machine Learning managed virtual network. The managed virtual network secures your managed Azure Machine Learning resources, such as compute instances, compute clusters, serverless compute, and managed online endpoints. 

Securing your workspace with a *managed network* provides network isolation for __outbound__ access from the workspace and managed computes. An *Azure Virtual Network that you create and manage* is used to provide network isolation __inbound__ access to the workspace. For example, a private endpoint for the workspace is created in your Azure Virtual Network. Any clients connecting to the virtual network can access the workspace through the private endpoint. When running jobs on managed computes, the managed network restricts what the compute can access.

## Managed Virtual Network Architecture

When you enable managed virtual network isolation, a managed virtual network is created for the workspace. Managed compute resources you create for the workspace automatically use this managed virtual network. The managed virtual network can use private endpoints for Azure resources that are used by your workspace, such as Azure Storage, Azure Key Vault, and Azure Container Registry. 

There are two different configuration modes for outbound traffic from the managed virtual network:

> [!TIP]
> Regardless of the outbound mode you use, traffic to Azure resources can be configured to use a private endpoint. For example, you might allow all outbound traffic to the internet, but restrict communication with Azure resources by adding outbound rules for the resources.

| Outbound mode | Description | Scenarios |
| ----- | ----- | ----- |
| Allow internet outbound | Allow all internet outbound traffic from the managed virtual network. | You want unrestricted access to machine learning resources on the internet, such as python packages or pretrained models.<sup>1</sup> |
| Allow only approved outbound | Outbound traffic is allowed by specifying service tags. | * You want to minimize the risk of data exfiltration, but you need to prepare all required machine learning artifacts in your private environment.</br>* You want to configure outbound access to an approved list of services, service tags, or FQDNs. |
| Disabled | Inbound and outbound traffic isn't restricted or you're using your own Azure Virtual Network to protect resources. | You want public inbound and outbound from the workspace, or you're handling network isolation with your own Azure virtual network. |

1. You can use outbound rules with _allow only approved outbound_ mode to achieve the same result as using allow internet outbound. The differences are:

* You must add rules for each outbound connection you need to allow.
* Adding FQDN outbound rules __increase your costs__ as this rule type uses Azure Firewall. For more information, see [Pricing](#pricing)
* The default rules for _allow only approved outbound_ are designed to minimize the risk of data exfiltration. Any outbound rules you add might increase your risk.

The managed virtual network is preconfigured with [required default rules](#list-of-required-rules). It's also configured for private endpoint connections to your workspace, workspace's default storage, container registry, and key vault __if they're configured as private__ or __the workspace isolation mode is set to allow only approved outbound__. After choosing the isolation mode, you only need to consider other outbound requirements you might need to add.

The following diagram shows a managed virtual network configured to __allow internet outbound__:

:::image type="content" source="./media/how-to-managed-network/internet-outbound.svg" alt-text="Diagram of managed virtual network isolation configured for internet outbound." lightbox="./media/how-to-managed-network/internet-outbound.svg":::

The following diagram shows a managed virtual network configured to __allow only approved outbound__:

> [!NOTE]
> In this configuration, the storage, key vault, and container registry used by the workspace are flagged as private. Since they're flagged as private, a private endpoint is used to communicate with them.

:::image type="content" source="./media/how-to-managed-network/only-approved-outbound.svg" alt-text="Diagram of managed virtual network isolation configured for allow only approved outbound." lightbox="./media/how-to-managed-network/only-approved-outbound.svg":::

> [!NOTE]
> Once a managed VNet workspace is configured to __allow internet outbound__, the workspace can't be reconfigured to __disabled__. Similarly, once a managed VNet workspace is configured to __allow only approved outbound__, the workspace can't be reconfigured to __allow internet outbound__.


### Azure Machine Learning studio

If you want to use the integrated notebook or create datasets in the default storage account from studio, your client needs access to the default storage account. Create a _private endpoint_ or _service endpoint_ for the default storage account in the Azure Virtual Network that the clients use.

Part of Azure Machine Learning studio runs locally in the client's web browser, and communicates directly with the default storage for the workspace. Creating a private endpoint or service endpoint (for the default storage account) in the client's virtual network ensures that the client can communicate with the storage account.

If the workspace associated Azure storage account has public network access disabled, ensure the private endpoint created in the client virtual network is granted the Reader role to your workspace managed identity. This applies to both blog and file storage private endpoints. The role isn't required for the private endpoint created by the managed virtual network. 

For more information on creating a private endpoint or service endpoint, see the [Connect privately to a storage account](/azure/storage/common/storage-private-endpoints) and [Service Endpoints](/azure/virtual-network/virtual-network-service-endpoints-overview) articles.

### Secured associated resources

If you add the following services to the virtual network by using either a service endpoint or a private endpoint (disabling the public access), allow trusted Microsoft services to access these services:

| Service | Endpoint information | Allow trusted information |
| ----- | ----- | ----- |
| __Azure Key Vault__| [Service endpoint](/azure/key-vault/general/overview-vnet-service-endpoints)</br>[Private endpoint](/azure/key-vault/general/private-link-service) | [Allow trusted Microsoft services to bypass this firewall](how-to-secure-workspace-vnet.md#secure-azure-key-vault) |
| __Azure Storage Account__ | [Service and private endpoint](how-to-secure-workspace-vnet.md?tabs=se#secure-azure-storage-accounts)</br>[Private endpoint](how-to-secure-workspace-vnet.md?tabs=pe#secure-azure-storage-accounts) | [Grant access from Azure resource instances](/azure/storage/common/storage-network-security#grant-access-from-azure-resource-instances)</br>__or__</br>[Grant access to trusted Azure services](/azure/storage/common/storage-network-security#grant-access-to-trusted-azure-services) |
| __Azure Container Registry__ | [Private endpoint](/azure/container-registry/container-registry-private-link) | [Allow trusted services](/azure/container-registry/allow-access-trusted-services) |

## Prerequisites

Before following the steps in this article, make sure you have the following prerequisites:

::: zone pivot="cli"

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* The __Microsoft.Network__ resource provider must be registered for your Azure subscription. This resource provider is used by the workspace when creating private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* The Azure identity you use when deploying a managed network requires the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints:

    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read`
    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write`

* The [Azure CLI](/cli/azure/) and the `ml` extension to the Azure CLI. For more information, see [Install, set up, and use the CLI (v2)](how-to-configure-cli.md).

    >[!TIP]
    > Azure Machine Learning managed VNet was introduced on May 23rd, 2023. If you have an older version of the ml extension, you might need to update it for the examples in this article work. To update the extension, use the following Azure CLI command:
    >
    > ```azurecli
    > az extension update -n ml
    > ```

* The CLI examples in this article assume that you're using the Bash (or compatible) shell. For example, from a Linux system or [Windows Subsystem for Linux](/windows/wsl/about).

* The Azure CLI examples in this article use `ws` to represent the name of the workspace, and `rg` to represent the name of the resource group. Change these values as needed when using the commands with your Azure subscription.

::: zone-end
::: zone pivot="python-sdk"

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* The __Microsoft.Network__ resource provider must be registered for your Azure subscription. This resource provider is used by the workspace when creating private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* The Azure identity you use when deploying a managed network requires the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints:

    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read`
    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write`

* The Azure Machine Learning Python SDK v2. For more information on the SDK, see [Install the Python SDK v2 for Azure Machine Learning](/python/api/overview/azure/ai-ml-readme).

    > [!TIP]
    > Azure Machine Learning managed VNet was introduced on May 23rd, 2023. If you have an older version of the SDK installed, you might need to update it for the examples in this article to work. To update the SDK, use the following command:
    >
    > ```bash
    > pip install --upgrade azure-ai-ml azure-identity
    > ```

* The examples in this article assume that your code begins with the following Python. This code imports the classes required when creating a workspace with managed virtual network, sets variables for your Azure subscription and resource group, and creates the `ml_client`:

    ```python
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import (
        Workspace,
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
    ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group)
    ```

::: zone-end

::: zone pivot="azure-portal"

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* The __Microsoft.Network__ resource provider must be registered for your Azure subscription. This resource provider is used by the workspace when creating private endpoints for the managed virtual network.

    For information on registering resource providers, see [Resolve errors for resource provider registration](/azure/azure-resource-manager/templates/error-register-resource-provider).

* The Azure identity you use when deploying a managed network requires the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions to create private endpoints:

    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read`
    * `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write`

::: zone-end

To establish private endpoint connections in managed virtual networks using Azure Machine Learning, the workspace managed identity, whether system-assigned or user-assigned, and the user identity that initiates the creation of the private endpoint, must have permissions to approve the Private Endpoint connections on the target resources. After April 30th, 2025, permissions aren't automatically granted to the managed identity and must be assigned manually.

Microsoft recommends assigning the _Azure AI Enterprise Network Connection Approver_ role to the managed identity. The following list contains the private endpoint target resource types covered by the __Azure AI Enterprise Network Connection Approver__ role:

* Azure Application Gateway
* Azure Monitor
* Azure AI Search
* Event Hubs
* Azure SQL Database
* Azure Storage
* Azure Machine Learning workspace
* Azure Machine Learning registry
* Microsoft Foundry
* Azure Key Vault
* Azure Cosmos DB
* Azure Database for MySQL
* Azure Database for PostgreSQL
* Foundry Tools
* Azure Managed Redis
* Container Registry
* API Management

If you would like to create a custom role instead, see [Azure AI Enterprise Network Connection Approver role](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-enterprise-network-connection-approver) to add the specific actions for each resource type.

To create private endpoint outbound rules to target resource types not covered by the _Azure AI Enterprise Network Connection Approver_ role, a custom scoped-down role is recommended. The role should be defined with the actions necessary to approve private endpoint connections on the target resource types. Examples of such resource types are Azure Data Factory, Azure Databricks, and Azure Function Apps.

To create Private Endpoint outbound rules to default workspace resources, the required permissions are automatically covered by the role assignments granted during workspace creation, so no other action is needed.

## Configure a managed virtual network to allow internet outbound

> [!TIP]
> The creation of the managed VNet is deferred until a compute resource is created or provisioning is manually started. When you allow automatic creation, it can take around __30 minutes__ to create the first compute resource as it is also provisioning the network. For more information, see [Manually provision the network](#manually-provision-a-managed-vnet).

> [!IMPORTANT]
> __If you plan to submit serverless Spark jobs__, you must manually start provisioning. For more information, see the [configure for serverless Spark jobs](#configure-for-serverless-spark-jobs) section.

::: zone pivot="cli"

To configure a managed virtual network that allows internet outbound communications, you can use either the `--managed-network allow_internet_outbound` parameter or a YAML configuration file that contains the following entries:

```yml
managed_network:
  isolation_mode: allow_internet_outbound
```

You can also define _outbound rules_ to other Azure services that the workspace relies on. These rules define _private endpoints_ that allow an Azure resource to securely communicate with the managed virtual network. The following rule demonstrates adding a private endpoint to an Azure Blob resource.

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

You can configure a managed virtual network using either the `az ml workspace create` or `az ml workspace update` commands:

# [Create a new workspace](#tab/new-workspace)

The following example creates a new workspace. The `--managed-network allow_internet_outbound` parameter configures a managed virtual network for the workspace:

```azurecli
az ml workspace create --name ws --resource-group rg --managed-network allow_internet_outbound
```

To create a workspace using a YAML file instead, use the `--file` parameter and specify the YAML file that contains the configuration settings:

```azurecli
az ml workspace create --file workspace.yaml --resource-group rg --name ws
```

The following YAML example defines a workspace with a managed virtual network:

```yml
name: myworkspace
location: EastUS
managed_network:
    isolation_mode: allow_internet_outbound
```

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

The following example updates an existing workspace. The `--managed-network allow_internet_outbound` parameter configures a managed virtual network for the workspace:

```azurecli
az ml workspace update --name ws --resource-group rg --managed-network allow_internet_outbound
```

To update an existing workspace using the YAML file, use the `--file` parameter and specify the YAML file that contains the configuration settings:

```azurecli
az ml workspace update --file workspace.yaml --name ws --resource-group MyGroup
```

The following YAML example defines a managed virtual network for the workspace. It also demonstrates how to add a private endpoint connection to a resource used by the workspace; in this example, a private endpoint for a blob store:

```yml
name: myworkspace
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

---

::: zone-end

::: zone pivot="python-sdk"

To configure a managed virtual network that allows internet outbound communications, use the `ManagedNetwork` class to define a network with `IsolationMode.ALLOW_INTERNET_OUTBOUND`. You can then use the `ManagedNetwork` object to create a new workspace or update an existing one. To define _outbound rules_ to Azure services that the workspace relies on, use the `PrivateEndpointDestination` class to define a new private endpoint to the service.

# [Create a new workspace](#tab/new-workspace)

The following example creates a new workspace named `myworkspace`, with an outbound rule named `myrule` that adds a private endpoint for an Azure Blob store:

```python
# Basic managed VNet configuration
network = ManagedNetwork(IsolationMode.ALLOW_INTERNET_OUTBOUND)

# Workspace configuration
ws = Workspace(
    name="myworkspace",
    location="eastus",
    managed_network=network
)

# Example private endpoint outbound to a blob
rule_name = "myrule"
service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
subresource_target = "blob"
spark_enabled = True

# Add the outbound 
ws.managed_network.outbound_rules = [PrivateEndpointDestination(
    name=rule_name, 
    service_resource_id=service_resource_id, 
    subresource_target=subresource_target, 
    spark_enabled=spark_enabled)]

# Create the workspace
ws = ml_client.workspaces.begin_create(ws).result()
```

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

The following example demonstrates how to create a managed virtual network for an existing Azure Machine Learning workspace named `myworkspace`:

```python
# Get the existing workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name="myworkspace")
ws = ml_client.workspaces.get()

# Basic managed VNet configuration
ws.managed_network = ManagedNetwork(IsolationMode.ALLOW_INTERNET_OUTBOUND)

# Example private endpoint outbound to a blob
rule_name = "myrule"
service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
subresource_target = "blob"
spark_enabled = True

# Add the outbound 
ws.managed_network.outbound_rules = [PrivateEndpointDestination(
    name=rule_name, 
    service_resource_id=service_resource_id, 
    subresource_target=subresource_target, 
    spark_enabled=spark_enabled)]

# Create the workspace
ml_client.workspaces.begin_update(ws)
```

---

::: zone-end

::: zone pivot="azure-portal"

# [Create a new workspace](#tab/new-workspace)

1. Sign in to the [Azure portal](https://portal.azure.com), and choose Azure Machine Learning from Create a resource menu.
1. Provide the required information on the __Basics__ tab.
1. From the __Networking__ tab, select __Private with Internet Outbound__.

    :::image type="content" source="./media/how-to-managed-network/use-managed-network-internet-outbound.png" alt-text="Screenshot of creating a workspace with an internet outbound managed virtual network." lightbox="./media/how-to-managed-network/use-managed-network-internet-outbound.png":::

1. To add an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Workspace outbound rules__ sidebar, provide the following information:

    * __Rule name__: A name for the rule. The name must be unique for this workspace.
    * __Destination type__: Private Endpoint is the only option when the network isolation is private with internet outbound. Azure Machine Learning managed virtual network doesn't support creating a private endpoint to all Azure resource types. For a list of supported resources, see the [Private endpoints](#private-endpoints) section.
    * __Subscription__: The subscription that contains the Azure resource you want to add a private endpoint for.
    * __Resource group__: The resource group that contains the Azure resource you want to add a private endpoint for.
    * __Resource type__: The type of the Azure resource.
    * __Resource name__: The name of the Azure resource.
    * __Sub Resource__: The sub resource of the Azure resource type.
    * __Spark enabled__: Select this option if you want to enable serverless Spark jobs for the workspace. This option is only available if the resource type is Azure Storage.

    :::image type="content" source="./media/how-to-managed-network/outbound-rule-private-endpoint.png" alt-text="Screenshot of adding an outbound rule for a private endpoint." lightbox="./media/how-to-managed-network/outbound-rule-private-endpoint.png":::

    Select __Save__ to save the rule. You can continue using __Add user-defined outbound rules__ to add rules.

1. Continue creating the workspace as normal.

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

1. Sign in to the [Azure portal](https://portal.azure.com), and select the Azure Machine Learning workspace that you want to enable managed virtual network isolation for.
1. Select __Networking__, __Workspace managed outbound access__, and then __Allow Internet Outbound__.

    :::image type="content" source="./media/how-to-managed-network/update-managed-network-internet-outbound.png" alt-text="Screenshot of updating a workspace to managed virtual network with internet outbound." lightbox="./media/how-to-managed-network/update-managed-network-internet-outbound.png":::

    * To _add_ an _outbound rule_, select __Add user-defined outbound rules__. From the __Workspace outbound rules__ sidebar, provide the same information as used when creating a workspace in the 'Create a new workspace' section.

        :::image type="content" source="./media/how-to-managed-network/outbound-rule-private-endpoint.png" alt-text="Screenshot of updating a managed virtual network by adding a private endpoint." lightbox="./media/how-to-managed-network/outbound-rule-private-endpoint.png":::

    * To __delete__ an outbound rule, select __delete__ for the rule.

        :::image type="content" source="./media/how-to-managed-network/delete-outbound-rule.png" alt-text="Screenshot of the delete rule icon for an approved outbound managed virtual network.":::

1. Select __Save__ at the top of the page to save the changes to the managed virtual network.

---

::: zone-end

## Configure a managed virtual network to allow only approved outbound

> [!TIP]
> The managed VNet is automatically provisioned when you create a compute resource. When you allow automatic creation, it can take around __30 minutes__ to create the first compute resource as it is also provisioning the network. If you configured FQDN outbound rules, the first FQDN rule adds around __10 minutes__ to the provisioning time. For more information, see [Manually provision the network](#manually-provision-a-managed-vnet).

> [!IMPORTANT]
> __If you plan to submit serverless Spark jobs__, you must manually start provisioning. For more information, see the [configure for serverless Spark jobs](#configure-for-serverless-spark-jobs) section.

::: zone pivot="cli"

To configure a managed virtual network that allows only approved outbound communications, you can use either the `--managed-network allow_only_approved_outbound` parameter or a YAML configuration file that contains the following entries:

```yml
managed_network:
  isolation_mode: allow_only_approved_outbound
```

You can also define _outbound rules_ to define approved outbound communication. An outbound rule can be created for a type of `service_tag`, `fqdn`, and `private_endpoint`. The following rule demonstrates adding a private endpoint to an Azure Blob resource, a service tag to Azure Data Factory, and an FQDN to `pypi.org`:

> [!IMPORTANT]
> * Adding an outbound for a service tag or FQDN is only valid when the managed VNet is configured to `allow_only_approved_outbound`.
> * If you add outbound rules, Microsoft can't guarantee data exfiltration.

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

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

You can configure a managed virtual network using either the `az ml workspace create` or `az ml workspace update` commands:

# [Create a new workspace](#tab/new-workspace)

The following example uses the `--managed-network allow_only_approved_outbound` parameter to configure the managed virtual network:

```azurecli
az ml workspace create --name ws --resource-group rg --managed-network allow_only_approved_outbound
```

The following YAML file defines a workspace with a managed virtual network:

```yml
name: myworkspace
location: EastUS
managed_network:
    isolation_mode: allow_only_approved_outbound
```

To create a workspace using the YAML file, use the `--file` parameter:

```azurecli
az ml workspace create --file workspace.yaml --resource-group rg --name ws
```

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

The following example uses the `--managed-network allow_only_approved_outbound` parameter to configure the managed virtual network for an existing workspace:

```azurecli
az ml workspace update --name ws --resource-group rg --managed-network allow_only_approved_outbound
```

The following YAML file defines a managed virtual network for the workspace. It also demonstrates how to add an approved outbound to the managed virtual network. In this example, an outbound rule is added for both a service tag:

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

```yaml
name: myworkspace_dep
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

---

::: zone-end

::: zone pivot="python-sdk"

To configure a managed virtual network that allows only approved outbound communications, use the `ManagedNetwork` class to define a network with `IsolationMode.ALLOw_ONLY_APPROVED_OUTBOUND`. You can then use the `ManagedNetwork` object to create a new workspace or update an existing one. To define _outbound rules_, use the following classes:

| Destination | Class |
| ----------- | ----- |
| __Azure service that the workspace relies on__ | `PrivateEndpointDestination` |
| __Azure service tag__ | `ServiceTagDestination` |
| __Fully qualified domain name (FQDN)__ | `FqdnDestination` |

# [Create a new workspace](#tab/new-workspace)

The following example creates a new workspace named `myworkspace`, with several outbound rules:

* `myrule` - Adds a private endpoint for an Azure Blob store.
* `datafactory` - Adds a service tag rule to communicate with Azure Data Factory.

> [!IMPORTANT]
> * Adding an outbound for a service tag or FQDN is only valid when the managed VNet is configured to `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`.
> * If you add outbound rules, Microsoft can't guarantee data exfiltration.

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

```python
# Basic managed VNet configuration
network = ManagedNetwork(IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND)

# Workspace configuration
ws = Workspace(
    name="myworkspace",
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

# Create the workspace
ws = ml_client.workspaces.begin_create(ws).result()
```

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

The following example demonstrates how to create a managed virtual network for an existing Azure Machine Learning workspace named `myworkspace`. The example also adds several outbound rules for the managed virtual network:

* `myrule` - Adds a private endpoint for an Azure Blob store.
* `datafactory` - Adds a service tag rule to communicate with Azure Data Factory.

> [!TIP]
> Adding an outbound for a service tag or FQDN is only valid when the managed VNet is configured to `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`.

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

```python
# Get the existing workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name="myworkspace")
ws = ml_client.workspaces.get()

# Basic managed VNet configuration
ws.managed_network = ManagedNetwork(IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND)

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

# Update the workspace
ml_client.workspaces.begin_update(ws)
```

---

::: zone-end
::: zone pivot="azure-portal"

# [Create a new workspace](#tab/new-workspace)

1. Sign in to the [Azure portal](https://portal.azure.com), and choose Azure Machine Learning from Create a resource menu.
1. Provide the required information on the __Basics__ tab.
1. From the __Networking__ tab, select __Private with Approved Outbound__.

    :::image type="content" source="./media/how-to-managed-network/use-managed-network-approved-outbound.png" alt-text="Screenshot of creating a workspace with an approved outbound managed virtual network." lightbox="./media/how-to-managed-network/use-managed-network-approved-outbound.png":::

1. To add an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Workspace outbound rules__ sidebar, provide the following information:

    * __Rule name__: A name for the rule. The name must be unique for this workspace.
    * __Destination type__: Private Endpoint, Service Tag, or FQDN. Service Tag and FQDN are only available when the network isolation is private with approved outbound.

    If the destination type is __Private Endpoint__, provide the following information:

    * __Subscription__: The subscription that contains the Azure resource you want to add a private endpoint for.
    * __Resource group__: The resource group that contains the Azure resource you want to add a private endpoint for.
    * __Resource type__: The type of the Azure resource.
    * __Resource name__: The name of the Azure resource.
    * __Sub Resource__: The sub resource of the Azure resource type.
    * __Spark enabled__: Select this option if you want to enable serverless Spark jobs for the workspace. This option is only available if the resource type is Azure Storage.

    > [!TIP]
    > Azure Machine Learning managed VNet doesn't support creating a private endpoint to all Azure resource types. For a list of supported resources, see the [Private endpoints](#private-endpoints) section.

    :::image type="content" source="./media/how-to-managed-network/outbound-rule-private-endpoint.png" alt-text="Screenshot of updating an approved outbound network by adding a private endpoint." lightbox="./media/how-to-managed-network/outbound-rule-private-endpoint.png":::

    If the destination type is __Service Tag__, provide the following information:

    * __Service tag__: The service tag to add to the approved outbound rules.
    * __Protocol__: The protocol to allow for the service tag.
    * __Port ranges__: The port ranges to allow for the service tag.

    :::image type="content" source="./media/how-to-managed-network/outbound-rule-service-tag.png" alt-text="Screenshot of updating an approved outbound network by adding a service tag." lightbox="./media/how-to-managed-network/outbound-rule-service-tag.png" :::

    If the destination type is __FQDN__, provide the following information:

    > [!WARNING]
    > FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

    * __FQDN destination__: The fully qualified domain name to add to the approved outbound rules.

    :::image type="content" source="./media/how-to-managed-network/outbound-rule-fqdn.png" alt-text="Screenshot of updating an approved outbound network by adding an FQDN rule for an approved outbound managed virtual network." lightbox="./media/how-to-managed-network/outbound-rule-fqdn.png":::

    Select __Save__ to save the rule. You can continue using __Add user-defined outbound rules__ to add rules.

1. Continue creating the workspace as normal.

# [Update an existing workspace](#tab/update-workspace)

[!INCLUDE [managed-vnet-update](~/reusable-content/ce-skilling/azure/includes/machine-learning/includes/managed-vnet-update.md)]

1. Sign in to the [Azure portal](https://portal.azure.com), and select the Azure Machine Learning workspace that you want to enable managed virtual network isolation for.
1. Select __Networking__, __Workspace managed outbound access__, and then select __Private with Approved Outbound__.

    :::image type="content" source="./media/how-to-managed-network/update-managed-network-approved-outbound.png" alt-text="Screenshot of updating a workspace to managed virtual network with approved outbound." lightbox="./media/how-to-managed-network/update-managed-network-approved-outbound.png":::

    * To _add_ an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Workspace outbound rules__ sidebar, provide the same information as when creating a workspace in the previous 'Create a new workspace' section.

    * To __delete__ an outbound rule, select __delete__ for the rule.

        :::image type="content" source="./media/how-to-managed-network/delete-outbound-rule.png" alt-text="Screenshot of the delete rule icon for an approved outbound managed virtual network.":::

1. Select __Save__ at the top of the page to save the changes to the managed virtual network.

---

::: zone-end


## Configure for serverless Spark jobs

> [!TIP]
> The steps in this section are only needed if you plan to submit __serverless Spark jobs__. If you aren't going to be submitting serverless Spark jobs, you can skip this section.

To enable the [serverless Spark jobs](how-to-submit-spark-jobs.md) for the managed virtual network, you must perform the following actions:

* Configure a managed virtual network for the workspace and add an outbound private endpoint for the Azure Storage Account.
* After you configure the managed virtual network, provision it and flag it to allow Spark jobs.

1. Configure an outbound private endpoint.

    ::: zone pivot="cli"

    Use a YAML file to define the managed virtual network configuration and add a private endpoint for the Azure Storage Account. Also set `spark_enabled: true`:

    > [!TIP]
    > This example is for a managed VNet configured using `isolation_mode: allow_internet_outbound` to allow internet traffic.  If you want to allow only approved outbound traffic, use `isolation_mode: allow_only_approved_outbound`.

    ```yml
    name: myworkspace
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

    You can use a YAML configuration file with the `az ml workspace update` command by specifying the `--file` parameter and the name of the YAML file. For example, the following command updates an existing workspace using a YAML file named `workspace_pe.yml`:

    ```azurecli
    az ml workspace update --file workspace_pe.yml --resource_group rg --name ws
    ```

    > [!NOTE]
    > When **Allow Only Approved Outbound** is enabled (`isolation_mode: allow_only_approved_outbound`), conda package dependencies defined in Spark session configuration fails to install. To resolve this problem, upload a self-contained Python package wheel with no external dependencies to an Azure storage account and create private endpoint to this storage account. Use the path to Python package wheel as `py_files` parameter in your Spark job. Setting an FQDN outbound rule won't bypass this issue as FQDN rule propagation isn't supported by Spark. 

    ::: zone-end
    ::: zone pivot="python-sdk"

    The following example demonstrates how to create a managed virtual network for an existing Azure Machine Learning workspace named `myworkspace`. It also adds a private endpoint for the Azure Storage Account and sets `spark_enabled=true`:

    > [!TIP]
    > The following example is for a managed VNet configured using `IsolationMode.ALLOW_INTERNET_OUTBOUND` to allow internet traffic. If you want to allow only approved outbound traffic, use `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`.  
        
    ```python
    # Get the existing workspace
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, "myworkspace")
    ws = ml_client.workspaces.get()

    # Basic managed VNet configuration
    ws.managed_network = ManagedNetwork(IsolationMode.ALLOW_INTERNET_OUTBOUND)

    # Example private endpoint outbound to a blob
    rule_name = "myrule"
    service_resource_id = "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
    subresource_target = "blob"
    spark_enabled = True

    # Add the outbound 
    ws.managed_network.outbound_rules = [PrivateEndpointDestination(
        name=rule_name, 
        service_resource_id=service_resource_id, 
        subresource_target=subresource_target, 
        spark_enabled=spark_enabled)]

    # Create the workspace
    ml_client.workspaces.begin_update(ws)
    ```
    > [!NOTE]
    > - When **Allow Only Approved Outbound** is enabled (`isolation_mode: allow_only_approved_outbound`), conda package dependencies defined in Spark session configuration fails to install. To resolve this problem, upload a self-contained Python package wheel with no external dependencies to an Azure storage account and create private endpoint to this storage account. Use the path to Python package wheel as `py_files` parameter in the Spark job.
    > - If the workspace was created with `IsolationMode.ALLOW_INTERNET_OUTBOUND`, it can’t be updated later to use `IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND`. 


    ::: zone-end
    ::: zone pivot="azure-portal"

    1. Sign in to the [Azure portal](https://portal.azure.com), and select the Azure Machine Learning workspace.
    2. Select __Networking__, then select __Add user-defined outbound rules__. Add a rule for the Azure Storage Account, and make sure that __Spark enabled__ is selected.
    
        :::image type="content" source="./media/how-to-managed-network/add-outbound-spark-enabled.png" alt-text="Screenshot of an endpoint rule with Spark enabled selected." lightbox="./media/how-to-managed-network/add-outbound-spark-enabled.png":::

    3. Select __Save__ to save the rule, then select __Save__ from the top of __Networking__ to save the changes to the managed virtual network.

    ::: zone-end

2. Provision the managed virtual network.

    > [!NOTE]
    > If your workspace has [public network access enabled](/azure/machine-learning/how-to-configure-private-link#enable-public-access), you must disable it before provisioning the managed VNet. If you don't disable public network access when provisioning the managed VNet, the private endpoints for the workspace might not be created automatically in the managed VNet. Otherwise, you would have to manually configure the private endpoint outbound rule for the workspace after the provisioning.

    ::: zone pivot="cli"

    The following example shows how to provision a managed virtual network for serverless Spark jobs by using the `--include-spark` parameter.

    ```azurecli
    az ml workspace provision-network -g my_resource_group -n my_workspace_name --include-spark
    ```

    ::: zone-end
    ::: zone pivot="python-sdk"

    The following example shows how to provision a managed virtual network for serverless Spark jobs:

    ```python
    # Connect to a workspace named "myworkspace"
    ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name="myworkspace")

    # whether to provision Spark vnet as well
    include_spark = True

    provision_network_result = ml_client.workspaces.begin_provision_network(workspace_name=ws_name, include_spark=include_spark).result()
    ```

    ::: zone-end
    ::: zone pivot="azure-portal"

    From the Azure portal, you can only select to provision the managed network during workspace creation. To do so, select __Provision managed virtual network__ from the __Outbound access__ tab. To provision the managed network for serverless Spark jobs for an existing workspace, you must use the [Azure CLI](how-to-managed-network.md?pivots=cli#configure-for-serverless-spark-jobs) or [Python SDK](how-to-managed-network.md?pivots=python-sdk#configure-for-serverless-spark-jobs).

    ::: zone-end

## Manually provision a managed VNet

The managed virtual network is automatically provisioned when you create a compute instance. When you rely on automatic provisioning, it can take around __30 minutes__ to create the first compute instance as it is also provisioning the network. If you configured FQDN outbound rules (only available with allow only approved mode), the first FQDN rule adds around __10 minutes__ to the provisioning time. If you have a large set of outbound rules to be provisioned in the managed network, it can take longer for provisioning to complete. The increased provisioning time can cause your first compute instance creation to time out.

To reduce the wait time and avoid potential timeout errors, we recommend manually provisioning the managed network. Then wait until the provisioning completes before you create a compute instance.

Alternatively, you can use the `provision_network_now` flag to provision the managed network as part of workspace creation.

> [!NOTE]
> To create an online deployment, you must manually provision the managed network, or create a compute instance first which will automatically provision it. 

::: zone pivot="cli"

The following example shows how to provision a managed virtual network during workspace creation.
    
```azurecli
az ml workspace create -n myworkspace -g my_resource_group --managed-network AllowInternetOutbound --provision-network-now
```

The following example shows how to manually provision a managed virtual network.

> [!TIP]
> If you plan to submit serverless Spark jobs, add the `--include-spark` parameter.

```azurecli
az ml workspace provision-network -g my_resource_group -n my_workspace_name
```

To verify that the provisioning completed, use the following command:

```azurecli
az ml workspace show -n my_workspace_name -g my_resource_group --query managed_network
```

::: zone-end
::: zone pivot="python-sdk"

To provision the managed network during workspace creation, set the `provision_network_now` flag to `True`.

```python
provision_network_now: True
```

The following example shows how to provision a managed virtual network:

```python
# Connect to a workspace named "myworkspace"
ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name="myworkspace")

# whether to provision Spark vnet as well
include_spark = True

provision_network_result = ml_client.workspaces.begin_provision_network(workspace_name=ws_name, include_spark=include_spark).result()
```

To verify that the workspace has been provisioned, use `ml_client.workspaces.get()` to get the workspace information. The `managed_network` property contains the status of the managed network.

```python
ws = ml_client.workspaces.get()
print(ws.managed_network.status)
```

::: zone-end

::: zone pivot="azure-portal"

During workspace creation, select __Provision managed network proactively at creation__ to provision the managed network. Charges are incurred from network resources, such as private endpoints, once the virtual network is provisioned. This configuration option is only available during workspace creation.

::: zone-end

## Configure image builds

When the Azure Container Registry for your workspace is behind a virtual network, it can't be used to directly build Docker images. Instead, configure your workspace to use a compute cluster or compute instance to build images.

> [!IMPORTANT]
> The compute resource used to build Docker images needs to be able to access the package repositories that are used to train and deploy your models. If you're using a network configured to allow only approved outbound, you might need to add [rules that allow access to public repos](#scenario-access-public-machine-learning-packages) or [use private Python packages](concept-vulnerability-management.md#using-a-private-package-repository).

::: zone pivot="cli"

To update a workspace to use a compute cluster or compute instance to build Docker images, use the `az ml workspace update` command with the `--image-build-compute` parameter:

```azurecli
az ml workspace update --name ws --resource-group rg --image-build-compute mycompute
```

::: zone-end

::: zone pivot="python-sdk"

The following example demonstrates how to update a workspace to use a compute cluster to build images:

```python
# import required libraries
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

subscription_id = "<your subscription ID>"
resource_group = "<your resource group name>"
workspace = "<your workspace name>"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name=workspace
)

# Get workspace info
ws=ml_client.workspaces.get(name=workspace)
# Update to use cpu-cluster for image builds
ws.image_build_compute="mycompute"
ml_client.workspaces.begin_update(ws)
# To switch back to using ACR to build (if ACR is not in the virtual network):
# ws.image_build_compute = ''
# ml_client.workspaces.begin_update(ws)
```

::: zone-end

::: zone pivot="azure-portal"

There isn't a way to set the image build compute from the Azure portal. Instead, use the [Azure CLI](how-to-managed-network.md?pivots=cli#configure-image-builds) or [Python SDK](how-to-managed-network.md?pivots=python-sdk#configure-image-builds).

::: zone-end

## Manage outbound rules

::: zone pivot="cli"

To list the managed virtual network outbound rules for a workspace, use the following command:

```azurecli
az ml workspace outbound-rule list --workspace-name ws --resource-group rg
```

To view the details of a managed virtual network outbound rule, use the following command:

```azurecli
az ml workspace outbound-rule show --rule rule-name --workspace-name ws --resource-group rg
```

To remove an outbound rule from the managed virtual network, use the following command:

```azurecli
az ml workspace outbound-rule remove --rule rule-name --workspace-name ws --resource-group rg
```

::: zone-end

::: zone pivot="python-sdk"

The following example demonstrates how to manage outbound rules for a workspace named `myworkspace`:

```python
# Connect to the workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id=subscription_id, resource_group_name=resource_group, workspace_name="myworkspace")

# Specify the rule name
rule_name = "<some-rule-name>"

# Get a rule by name
rule = ml_client._workspace_outbound_rules.get(resource_group, ws_name, rule_name)

# List rules for a workspace
rule_list = ml_client._workspace_outbound_rules.list(resource_group, ws_name)

# Delete a rule from a workspace
ml_client._workspace_outbound_rules.begin_remove(resource_group, ws_name, rule_name).result()
```

::: zone-end

::: zone pivot="azure-portal"

1. Sign in to the [Azure portal](https://portal.azure.com), and select the Azure Machine Learning workspace that you want to enable managed virtual network isolation for.
1. Select __Networking__. The __Workspace Outbound access__ section allows you to manage outbound rules.

    :::image type="content" source="./media/how-to-managed-network/manage-outbound-rules.png" alt-text="Screenshot of the outbound rules section." lightbox="./media/how-to-managed-network/manage-outbound-rules.png":::

* To _add_ an _outbound rule_, select __Add user-defined outbound rules__ from the __Networking__ tab. From the __Workspace outbound rules__ sidebar, provide the following information:

* To __enable__ or __disable__ a rule, use the toggle in the __Active__ column.

* To __delete__ an outbound rule, select __delete__ for the rule.

::: zone-end

## List of required rules

__Private endpoints__:
* When the isolation mode for the managed virtual network is `Allow internet outbound`, private endpoint outbound rules are automatically created as required rules from the managed virtual network for the workspace and associated resources __with public network access disabled__ (Key Vault, Storage Account, Container Registry, Azure Machine Learning workspace).
* When the isolation mode for the managed virtual network is `Allow only approved outbound`, private endpoint outbound rules are automatically created as required rules from the managed virtual network for the workspace and associated resources __regardless of public network access mode for those resources__ (Key Vault, Storage Account, Container Registry, Azure Machine Learning workspace).
* These rules are automatically added to the managed virtual network. 

For Azure Machine Learning to run normally, there are a set of required service tags, required in either a managed or custom virtual network set-up. There are no alternatives to replacing certain required service tags. The following table describes each required service tag and its purpose within Azure Machine Learning.

| Service tag rule | Inbound or Outbound | Purpose |
| ----------- | ----- | ----- |
| `AzureMachineLearning` | Inbound | Create, update, and delete of Azure Machine Learning compute instance/cluster. |  
| `AzureMachineLearning`| Outbound | Using Azure Machine Learning services. Python intellisense in notebooks uses port 18881. Creating, updating, and deleting an Azure Machine Learning compute instance uses port 5831. |
| `AzureActiveDirectory` | Outbound | Authentication using Microsoft Entra ID. |
| `BatchNodeManagement.region` | Outbound | Communication with Azure Batch back-end for Azure Machine Learning compute instances/clusters. |
| `AzureResourceManager` | Outbound | Creation of Azure resources with Azure Machine Learning, Azure CLI, and Azure Machine Learning SDK. |
| `AzureFrontDoor.FirstParty` | Outbound | Access docker images provided by Microsoft. |
| `MicrosoftContainerRegistry` | Outbound | Access docker images provided by Microsoft. Setup of the Azure Machine Learning router for Azure Kubernetes Service. |		
| `AzureMonitor` | Outbound | Used to log monitoring and metrics to Azure Monitor. Only needed if the Azure Monitor for the workspace isn't secured. This outbound is also used to log information for support incidents. |
| `VirtualNetwork` | Outbound | Required when private endpoints are present in the virtual network or peered virtual networks. |

> [!NOTE]
> Service tags as the ONLY security boundary isn't sufficient. For tenant level isolation, use private endpoints when possible.

## List of scenario specific outbound rules

### Scenario: Access public machine learning packages

To allow installation of __Python packages for training and deployment__, add outbound _FQDN_ rules to allow traffic to the following host names:

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

[!INCLUDE [recommended outbound](includes/recommended-network-outbound.md)]

### Scenario: Use Visual Studio Code desktop or web with compute instance

If you plan to use __Visual Studio Code__ with Azure Machine Learning, add outbound _FQDN_ rules to allow traffic to the following hosts:

> [!NOTE]
> The following list isn't a complete list of the hosts required for all Visual Studio Code resources on the internet, only the most commonly used. For example, if you need access to a GitHub repository or other host, you must identify and add the required hosts for that scenario. For a complete list of host names, see [Network Connections in Visual Studio Code](https://code.visualstudio.com/docs/setup/network).

| __Host name__ | __Purpose__ |
| ---- | ---- |
| `*.vscode.dev`<br>`*.vscode-unpkg.net`<br>`*.vscode-cdn.net`<br>`*.vscodeexperiments.azureedge.net`<br>`default.exp-tas.com` | Required to access vscode.dev (Visual Studio Code for the Web) |
| `code.visualstudio.com` | Required to download and install VS Code desktop. This host isn't required for VS Code Web. |
| `update.code.visualstudio.com`<br>`*.vo.msecnd.net` | Used to retrieve VS Code server bits that are installed on the compute instance through a setup script. |
| `marketplace.visualstudio.com`<br>`vscode.blob.core.windows.net`<br>`*.gallerycdn.vsassets.io` | Required to download and install VS Code extensions. These hosts enable the remote connection to compute instances. For more information, see [Manage Azure Machine Learning resources in VS Code](how-to-manage-resources-vscode.md). |
| `vscode.download.prss.microsoft.com` | Used for Visual Studio Code download CDN |

### Scenario: Use batch endpoints or ParallelRunStep

If you plan to use __Azure Machine Learning batch endpoints__ for deployment or __ParallelRunStep__, add outbound _private endpoint_ rules to allow traffic to the following sub resources for the default storage account:

* `queue`
* `table`

### Scenario: Use prompt flow with Azure OpenAI, content safety, and Azure AI Search

* Private endpoint to Foundry Tools
* Private endpoint to Azure AI Search

### Scenario: Use HuggingFace models

If you plan to use __HuggingFace models__ with Azure Machine Learning, add outbound _FQDN_ rules to allow traffic to the following hosts:

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. For more information, see [Pricing](#pricing).

* `docker.io`
* `*.docker.io`
* `*.docker.com`
* `production.cloudflare.docker.com`
* `cdn.auth0.com`
* `cdn-lfs.huggingface.co`

### Scenario: Enable access from selected IP Addresses

If you want to enable access from specific IP addresses, use the following actions:

1. Add an outbound _private endpoint_ rule to allow traffic to the Azure Machine Learning workspace. This rule allows compute instances created in the managed virtual network to access the workspace.

    > [!TIP]
    > You can't add this rule during workspace creation, as the workspace doesn't exist yet.

1. Enable public network access to the workspace. For more information, see [public network access enabled](how-to-configure-private-link.md#enable-public-access).
1. Add your IP addresses to the firewall for Azure Machine Learning. For more information, see [enable access only from IP ranges](how-to-configure-private-link.md#enable-public-access-only-from-internet-ip-ranges).

    > [!NOTE]
    > Only IPv4 addresses are supported.

For more information, see [Configure private link](how-to-configure-private-link.md#enable-public-access-only-from-internet-ip-ranges).

## Private endpoints

Private endpoints are currently supported for the following Azure services:

* Azure Machine Learning
* Azure Machine Learning registries
* Azure Storage (all sub resource types)
* Azure Container Registry
* Azure Key Vault
* Foundry Tools
* Azure AI Search (formerly Cognitive Search)
* Azure SQL Server
* Azure Data Factory
* Azure Cosmos DB (all sub resource types)
* Azure Event Hubs
* Azure Redis Cache
* Azure Databricks
* Azure Database for MariaDB
* Azure Database for PostgreSQL Single Server
* Azure Database for PostgreSQL Flexible Server
* Azure Database for MySQL
* Azure API Management
  * Supporting only Classic tier without VNET injection and Standard V2 tier with virtual network integration. For more on API Management virtual networks, see [Virtual Network Concepts](/azure/api-management/virtual-network-concepts)
* Application Insights (Through [PrivateLinkScopes](/azure/azure-monitor/logs/private-link-configure#create-azure-monitor-private-link-scope-ampls))

When you create a private endpoint, you provide the _resource type_ and _subresource_ that the endpoint connects to. Some resources have multiple types and subresources. For more information, see [what is a private endpoint](/azure/private-link/private-endpoint-overview).

When you create a private endpoint for Azure Machine Learning dependency resources, such as Azure Storage, Azure Container Registry, and Azure Key Vault, the resource can be in a different Azure subscription. However, the resource must be in the same tenant as the Azure Machine Learning workspace.

Private endpoints for the workspace aren't created automatically. They're only created when the first _compute is created_ or when managed virtual network provisioning is forced. For more information on forcing the managed virtual network provisioning, see [Manually provision the network](#manually-provision-a-managed-vnet).

### Approval of private endpoints

To establish Private Endpoint connections in managed virtual networks using Azure Machine Learning, the workspace managed identity, whether system-assigned or user-assigned, must have permissions to approve the Private Endpoint connections on the target resources. Previously, this assignment was done through automatic role assignments by the Azure Machine Learning service. However, there are security concerns about the automatic role assignment. To improve security, starting April 30th, 2025, this role assignment isn't automatic. 

We recommend assigning the Azure AI Enterprise Network Connection Approver role, or a custom role with the necessary Private Endpoint connection permissions, on the target resource types. To allow Azure Machine Learning services to approve Private Endpoint connections to the target Azure resources, grant this role to the Azure Machine Learning workspace's managed identity.
 
Here's the list of private endpoint target resource types covered by the Azure AI Enterprise Network Connection Approver role:
* Azure Application Gateway
* Azure Monitor
* Azure AI Search
* Event Hubs
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
* Container Registry
* API Management
  
To create Private Endpoint outbound rules to target resource types not covered by the Azure AI Enterprise Network Connection Approver role, a custom scoped-down role is recommended. The rule should define the actions necessary to approve private endpoint connections on the target resource types. Examples of such resource types are Azure Data Factory, Azure Databricks, and Azure Function Apps.
 
To create Private Endpoint outbound rules to default workspace resources, the required permissions are automatically covered by the role assignments granted during workspace creation, so no other action is needed.

## Select an Azure Firewall version for allowed only approved outbound

An Azure Firewall is deployed if an FQDN outbound rule is created while in the _allow only approved outbound_ mode. Charges for the Azure Firewall are included in your billing. By default, a __Standard__ version of AzureFirewall is created. Optionally, you can select to use a __Basic__ version. You can change the firewall version used as needed. To figure out which version is best for you, visit [Choose the right Azure Firewall version](/azure/firewall/choose-firewall-sku).

> [!IMPORTANT]
> The firewall isn't created until you add an outbound FQDN rule. For more information on pricing, see [Azure Firewall pricing](https://azure.microsoft.com/pricing/details/azure-firewall/) and view prices for the _standard_ version.
> URL-based filtering is only supported with Premium SKU Azure Firewall, not Basic or Standard SKU Azure Firewall. Managed virtual network doesn't support Premium SKU Azure Firewall.

::: zone pivot="azure-portal"

After selecting the allow only approved outbound mode, an option to select the Azure Firewall version (SKU) appears. Select __Standard__ to use the standard version or __Basic__ to use the basic version. Select __Save__ to save your configuration.

::: zone-end
::: zone pivot="cli"

To configure the firewall version from the CLI, use a YAML file and specify the `firewall_sku`. The following example demonstrates a YAML file that sets the firewall SKU to `basic`:

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

::: zone-end

::: zone pivot="python-sdk"

To configure the firewall version from the Python SDK, set the `firewall_sku` property of the `ManagedNetwork` object. The following example demonstrates how to set the firewall SKU to `basic`:

```python
network = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_INTERNET_OUTBOUND,
                         firewall_sku='basic')
```

::: zone-end

## Pricing

The Azure Machine Learning managed virtual network feature is free. However, you're charged for the following resources that are used by the managed virtual network:

* Azure Private Link - Private endpoints used to secure communications between the managed virtual network and Azure resources relies on Azure Private Link. For more information on pricing, see [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link/).
* FQDN outbound rules - FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are added to your billing. A standard version of Azure Firewall is used by default. For information on selecting the basic version, see [Select an Azure Firewall version](#select-an-azure-firewall-version-for-allowed-only-approved-outbound).

    > [!IMPORTANT]
    > The firewall isn't created until you add an outbound FQDN rule. For more information on pricing, see [Azure Firewall pricing](https://azure.microsoft.com/pricing/details/azure-firewall/) and view prices for the _standard_ version.

## Limitations

* Once you enable managed virtual network isolation of your workspace (either allow internet outbound or allow only approved outbound), you can't disable it.
* Managed virtual network uses private endpoint connection to access your private resources. You can't have a private endpoint and a service endpoint at the same time for your Azure resources, such as a storage account. We recommend using private endpoints in all scenarios.
* The managed virtual network is deleted when the workspace is deleted.
* Make sure there are no __scope locks__ on the Azure Machine Learning resources and resource group. Internal operations related to managed virtual network might be blocked.
* Data exfiltration protection is automatically enabled for the only approved outbound mode. If you add other outbound rules, such as to FQDNs, Microsoft can't guarantee that you're protected from data exfiltration to those outbound destinations.
* Creating a compute cluster in a different region than the workspace isn't supported when using a managed virtual network.
* Kubernetes and attached VMs aren't supported in an Azure Machine Learning managed virtual network.
* Using FQDN outbound rules increases the cost of the managed virtual network because FQDN rules use Azure Firewall. For more information, see [Pricing](#pricing).
* FQDN outbound rules only support ports 80 and 443.
* If your compute instance is in a managed network and is configured for no public IP, use the `az ml compute connect-ssh` command to connect to it using SSH.
* When using Managed virtual network, you can't deploy compute resources inside your custom virtual network. Compute resources can only be created inside the managed virtual network.
* If your managed network is configured to __allow only approved outbound__, you can't use an FQDN rule to access Azure Storage Accounts. You must use a private endpoint instead.
* Ensure to allowlist Microsoft-managed private endpoints created for the managed virtual network in your custom policy.

### Migration of compute resources

If you have an existing workspace and want to enable managed virtual network for it, there's currently no supported migration path for existing managed compute resources. You'll need to delete all existing managed compute resources and recreate them after enabling the managed virtual network. The following list contains the compute resources that must be deleted and recreated:

* Compute cluster
* Compute instance
* Managed online endpoints

## Next steps

* [Troubleshoot managed virtual network](how-to-troubleshoot-managed-network.md)
* [Configure managed computes in a managed virtual network](how-to-managed-network-compute.md)
