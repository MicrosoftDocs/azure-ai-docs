---
title: Secure an Azure Machine Learning workspace with virtual networks
titleSuffix: Azure Machine Learning
description: Use an isolated Azure Virtual Network to secure your Azure Machine Learning workspace and associated resources.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.reviewer: None
ms.author: larryfr
author: Blackmist
ms.date: 07/08/2024
ms.topic: how-to
ms.custom: tracking-python, security, cliv2, sdkv2, engagement-fy23, build-2023
---

# Secure an Azure Machine Learning workspace with virtual networks

[!INCLUDE [sdk/cli v2](includes/machine-learning-dev-v2.md)]

[!INCLUDE [managed-vnet-note](includes/managed-vnet-note.md)]

In this article, you learn how to secure an Azure Machine Learning workspace and its associated resources in an Azure Virtual Network.

This article is part of a series on securing an Azure Machine Learning workflow. See the other articles in this series:

* [Virtual network overview](how-to-network-security-overview.md)
* [Secure the training environment](how-to-secure-training-vnet.md)
* [Secure the inference environment](how-to-secure-inferencing-vnet.md)
* [Enable studio functionality](how-to-enable-studio-virtual-network.md)
* [Use custom DNS](how-to-custom-dns.md)
* [Use a firewall](how-to-access-azureml-behind-firewall.md)
* [API platform network isolation](how-to-configure-network-isolation-with-v2.md)

For a tutorial on creating a secure workspace, see [Tutorial: Create a secure workspace](tutorial-create-secure-workspace.md), [Bicep template](/samples/azure/azure-quickstart-templates/machine-learning-end-to-end-secure/), or [Terraform template](https://github.com/Azure/terraform/tree/master/quickstart/201-machine-learning-moderately-secure).

In this article you learn how to enable the following workspaces resources in a virtual network:
> [!div class="checklist"]
> - Azure Machine Learning workspace
> - Azure Storage accounts
> - Azure Key Vault
> - Azure Container Registry

## Prerequisites

+ Read the [Network security overview](how-to-network-security-overview.md) article to understand common virtual network scenarios and overall virtual network architecture.

+ Read the [Azure Machine Learning best practices for enterprise security](/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-enterprise-security) article to learn about best practices.

+ An existing virtual network and subnet to use with your compute resources.

    > [!WARNING]
    > Do not use the 172.17.0.0/16 IP address range for your VNet. This is the default subnet range used by the Docker bridge network, and will result in errors if used for your VNet. Other ranges may also conflict depending on what you want to connect to the virtual network. For example, if you plan to connect your on premises network to the VNet, and your on-premises network also uses the 172.16.0.0/16 range. Ultimately, it is up to __you__ to plan your network infrastructure.

[!INCLUDE [network-rbac](includes/network-rbac.md)]

### Azure Container Registry

* Your Azure Container Registry must be Premium version. For more information on upgrading, see [Changing SKUs](/azure/container-registry/container-registry-skus#changing-tiers).

* If your Azure Container Registry uses a __private endpoint__, we _recommend_ that it be in the same _virtual network_ as the storage account and compute targets used for training or inference. However it can also be in a [peered](/azure/virtual-network/virtual-network-peering-overview) virtual network.

   If it uses a __service endpoint__, it must be in the same _virtual network_ and _subnet_ as the storage account and compute targets.

* Your Azure Machine Learning workspace must contain an [Azure Machine Learning compute cluster](how-to-create-attach-compute-cluster.md).

## Limitations

### Azure storage account

* If you plan to use Azure Machine Learning studio and the storage account is also in the virtual network, there are extra validation requirements:

    * If the storage account uses a __service endpoint__, the workspace private endpoint and storage service endpoint must be in the same subnet of the virtual network.
    * If the storage account uses a __private endpoint__, the workspace private endpoint and storage private endpoint must be in the same virtual network. In this case, they can be in different subnets.

### Azure Container Instances

When your Azure Machine Learning workspace is configured with a private endpoint, deploying to Azure Container Instances in a virtual network isn't supported. Instead, consider using a [Managed online endpoint with network isolation](how-to-secure-online-endpoint.md).

### Azure Container Registry

When your Azure Machine Learning workspace or any resource is configured with a private endpoint it may be required to setup a user managed compute cluster for AzureML Environment image builds. Default scenario is leveraging [serverless compute](how-to-use-serverless-compute.md) and currently intended for scenarios with no network restrictions on resources associated with AzureML Workspace.

> [!IMPORTANT]
> The compute cluster used to build Docker images needs to be able to access the package repositories that are used to train and deploy your models. You may need to add network security rules that allow access to public repos, [use private Python packages](concept-vulnerability-management.md#using-a-private-package-repository), or use [custom Docker images (SDK v1)](v1/how-to-train-with-custom-image.md?view=azureml-api-1&preserve-view=true) that already include the packages.

> [!WARNING]
> If your Azure Container Registry uses a private endpoint or service endpoint to communicate with the virtual network, you cannot use a managed identity with an Azure Machine Learning compute cluster.

### Azure Monitor

> [!WARNING]
> Azure Monitor supports using Azure Private Link to connect to a VNet. However, you must use the open Private Link mode in Azure Monitor. For more information, see [Private Link access modes: Private only vs. Open](/azure/azure-monitor/logs/private-link-security#private-link-access-modes-private-only-vs-open).

## Required public internet access

[!INCLUDE [machine-learning-required-public-internet-access](includes/machine-learning-public-internet-access.md)]

For information on using a firewall solution, see [Configure required input and output communication](how-to-access-azureml-behind-firewall.md).

## Secure the workspace with private endpoint

Azure Private Link lets you connect to your workspace using a private endpoint. The private endpoint is a set of private IP addresses within your virtual network. You can then limit access to your workspace to only occur over the private IP addresses. A private endpoint helps reduce the risk of data exfiltration.

For more information on configuring a private endpoint for your workspace, see [How to configure a private endpoint](how-to-configure-private-link.md).

> [!WARNING]
> Securing a workspace with private endpoints does not ensure end-to-end security by itself. You must follow the steps in the rest of this article, and the VNet series, to secure individual components of your solution. For example, if you use a private endpoint for the workspace, but your Azure Storage Account is not behind the VNet, traffic between the workspace and storage does not use the VNet for security.

## Secure Azure storage accounts

Azure Machine Learning supports storage accounts configured to use either a private endpoint or service endpoint. 

# [Private endpoint](#tab/pe)

1. In the Azure portal, select the Azure Storage Account.
1. Use the information in [Use private endpoints for Azure Storage](/azure/storage/common/storage-private-endpoints#creating-a-private-endpoint) to add private endpoints for the following storage resources:

    * **Blob**
    * **File**
    * **Queue** - Only needed if you plan to use [Batch endpoints](concept-endpoints-batch.md) or the [ParallelRunStep](./tutorial-pipeline-batch-scoring-classification.md) in an Azure Machine Learning pipeline.
    * **Table** - Only needed if you plan to use [Batch endpoints](concept-endpoints-batch.md) or the [ParallelRunStep](./tutorial-pipeline-batch-scoring-classification.md) in an Azure Machine Learning pipeline.

    :::image type="content" source="./media/how-to-enable-studio-virtual-network/configure-storage-private-endpoint.png" alt-text="Screenshot showing private endpoint configuration page with blob and file options":::

    > [!TIP]
    > When configuring a storage account that is **not** the default storage, select the **Target subresource** type that corresponds to the storage account you want to add.

1. After creating the private endpoints for the storage resources, select the __Firewalls and virtual networks__ tab under __Networking__ for the storage account.
1. Select __Selected networks__, and then under __Resource instances__, select `Microsoft.MachineLearningServices/Workspace` as the __Resource type__. Select your workspace using __Instance name__. For more information, see [Trusted access based on system-assigned managed identity](/azure/storage/common/storage-network-security#trusted-access-based-on-system-assigned-managed-identity).

    > [!TIP]
    > Alternatively, you can select __Allow Azure services on the trusted services list to access this storage account__ to more broadly allow access from trusted services. For more information, see [Configure Azure Storage firewalls and virtual networks](/azure/storage/common/storage-network-security#trusted-microsoft-services).

    :::image type="content" source="./media/how-to-enable-virtual-network/storage-firewalls-and-virtual-networks-no-vnet.png" alt-text="The networking area on the Azure Storage page in the Azure portal when using private endpoint":::

1. Select __Save__ to save the configuration.

> [!TIP]
> When using a private endpoint, you can also disable anonymous access. For more information, see [disallow anonymous access](/azure/storage/blobs/anonymous-read-access-configure#allow-or-disallow-anonymous-read-access-for-a-storage-account).

# [Service endpoint](#tab/se)

1. In the Azure portal, select the Azure Storage Account.

1. From the __Security + networking__ section on the left of the page, select __Networking__ and then select the __Firewalls and virtual networks__ tab.

1. Select __Selected networks__. Under __Virtual networks__, select the __Add existing virtual network__ link and select the virtual network that your workspace uses.

    > [!IMPORTANT]
    > The storage account must be in the same virtual network and subnet as the compute instances or clusters used for training or inference.

1. Under __Resource instances__, select `Microsoft.MachineLearningServices/Workspace` as the __Resource type__ and select your workspace using __Instance name__. For more information, see [Trusted access based on system-assigned managed identity](/azure/storage/common/storage-network-security#trusted-access-based-on-system-assigned-managed-identity).

    > [!TIP]
    > Alternatively, you can select __Allow Azure services on the trusted services list to access this storage account__ to more broadly allow access from trusted services. For more information, see [Configure Azure Storage firewalls and virtual networks](/azure/storage/common/storage-network-security#trusted-microsoft-services).

    :::image type="content" source="./media/how-to-enable-virtual-network/storage-firewalls-and-virtual-networks.png" alt-text="The networking area on the Azure Storage page in the Azure portal":::

1. Select __Save__ to save the configuration.

> [!TIP]
> When using a service endpoint, you can also disable anonymous access. For more information, see [disallow anonymous access](/azure/storage/blobs/anonymous-read-access-configure#allow-or-disallow-anonymous-read-access-for-a-storage-account).

---

## Secure Azure Key Vault

Azure Machine Learning uses an associated Key Vault instance to store the following credentials:
* The associated storage account connection string
* Passwords to Azure Container Repository instances
* Connection strings to data stores

Azure key vault can be configured to use either a private endpoint or service endpoint. To use Azure Machine Learning experimentation capabilities with Azure Key Vault behind a virtual network, use the following steps:

> [!TIP]
> We _recommend_ that the key vault be in the same VNet as the workspace, however it can be in a [peered](/azure/virtual-network/virtual-network-peering-overview) VNet.

# [Private endpoint](#tab/pe)

For information on using a private endpoint with Azure Key Vault, see [Integrate Key Vault with Azure Private Link](/azure/key-vault/general/private-link-service#establish-a-private-link-connection-to-key-vault-using-the-azure-portal).


# [Service endpoint](#tab/se)

1. Go to the Key Vault that's associated with the workspace.

1. On the __Key Vault__ page, in the left pane, select __Networking__.

1. On the __Firewalls and virtual networks__ tab, do the following actions:
    1. Under __Allow access from__, select __Allow public access from specific virtual networks and IP addresses__.
    1. Under __Virtual networks__, select __Add a virtual network__, __Add existing virtual networks__, and add the virtual network/subnet where your experimentation compute resides.
    1. Verify that __Allow trusted Microsoft services to bypass this firewall__ is checked, and then select __Apply__.

    :::image type="content" source="./media/how-to-enable-virtual-network/key-vault-firewalls-and-virtual-networks-page.png" alt-text="The Firewalls and virtual networks section in the Key Vault pane":::

For more information, see [Configure Azure Key Vault network settings](/azure/key-vault/general/how-to-azure-key-vault-network-security).

---

## Enable Azure Container Registry (ACR)

> [!TIP]
> If you did not use an existing Azure Container Registry when creating the workspace, one may not exist. By default, the workspace will not create an ACR instance until it needs one. To force the creation of one, train or deploy a model using your workspace before using the steps in this section.

Azure Container Registry can be configured to use a private endpoint. Use the following steps to configure your workspace to use ACR when it is in the virtual network:

1. Find the name of the Azure Container Registry for your workspace, using one of the following methods:

    # [Azure CLI](#tab/cli)

    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

    If you've [installed the Machine Learning extension v2 for Azure CLI](how-to-configure-cli.md), you can use the `az ml workspace show` command to show the workspace information. The v1 extension doesn't return this information.

    ```azurecli-interactive
    az ml workspace show -n yourworkspacename -g resourcegroupname --query 'container_registry'
    ```

    This command returns a value similar to `"/subscriptions/{GUID}/resourceGroups/{resourcegroupname}/providers/Microsoft.ContainerRegistry/registries/{ACRname}"`. The last part of the string is the name of the Azure Container Registry for the workspace.

    # [Python SDK](#tab/python)

    [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

    The following code snippet demonstrates how to get the container registry information using the [Azure Machine Learning SDK](/python/api/overview/azure/ai-ml-readme):

   ```python
    # import required libraries
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential

    subscription_id = "<your subscription ID>"
    resource_group = "<your resource group name>"
    workspace = "<your workspace name>"

    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace
    )
    
    # Get workspace info
    ws=ml_client.workspaces.get(name=workspace)
    print(ws.container_registry)
    ```

    This code returns a value similar to `"/subscriptions/{GUID}/resourceGroups/{resourcegroupname}/providers/Microsoft.ContainerRegistry/registries/{ACRname}"`. The last part of the string is the name of the Azure Container Registry for the workspace.

    # [Portal](#tab/portal)

    From the overview section of your workspace, the __Registry__ value links to the Azure Container Registry.

    :::image type="content" source="./media/how-to-enable-virtual-network/azure-machine-learning-container-registry.png" alt-text="Azure Container Registry for the workspace" border="true":::

    ---

1. Limit access to your virtual network using the steps in [Connect privately to an Azure Container Registry](/azure/container-registry/container-registry-private-link). When adding the virtual network, select the virtual network and subnet for your Azure Machine Learning resources.

1. Configure the ACR for the workspace to [Allow access by trusted services](/azure/container-registry/allow-access-trusted-services).

1. By default, Azure Machine Learning will try to use a [serverless compute](how-to-use-serverless-compute.md) to build the image. This works only when the workspace-dependent resources such as Storage Account or Container Registry are not under any network restriction (private endpoints). If your workspace-dependent resources are network restricted, use an image-build-compute instead.

1. To set up an image-build compute, create an Azure Machine Learning CPU SKU [compute cluster](how-to-create-attach-compute-cluster.md) in the same VNet as your workspace-dependent resources. This cluster can then be set as the default image-build compute and will be used to build every image in your workspace from that point onwards. Use one of the following methods to configure the workspace to build Docker images using the compute cluster.

    > [!IMPORTANT]
    > The following limitations apply When using a compute cluster for image builds:
    > * Only a CPU SKU is supported.
    > * If you use a compute cluster configured for no public IP address, you must provide some way for the cluster to access the public internet. Internet access is required when accessing images stored on the Microsoft Container Registry, packages installed on Pypi, Conda, etc. You need to configure User Defined Routing (UDR) to reach to a public IP to access the internet. For example, you can use the public IP of your firewall, or you can use [Virtual Network NAT](/azure/virtual-network/nat-gateway/nat-overview) with a public IP. For more information, see [How to securely train in a VNet](how-to-secure-training-vnet.md).

    # [Azure CLI](#tab/cli)

    You can use the `az ml workspace update` command to set a build compute. The command is the same for both the v1 and v2 Azure CLI extensions for machine learning. In the following command, replace `myworkspace` with your workspace name, `myresourcegroup` with the resource group that contains the workspace, and `mycomputecluster` with the compute cluster name:

    ```azurecli
    az ml workspace update --name myworkspace --resource-group myresourcegroup --image-build-compute mycomputecluster
    ```

    You can switch back to serverless compute by executing the same command and referencing the compute as an empty space: `--image-build-compute ''`.

    # [Python SDK](#tab/python)

    The following code snippet demonstrates how to update the workspace to set a build compute using the [Azure Machine Learning SDK](/python/api/overview/azure/ai-ml-readme). Replace `mycomputecluster` with the name of the cluster to use:

    [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

    ```python
    # import required libraries
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential

    subscription_id = "<your subscription ID>"
    resource_group = "<your resource group name>"
    workspace = "<your workspace name>"

    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace
    )
    
    # Get workspace info
    ws=ml_client.workspaces.get(name=workspace)
    # Update to use cpu-cluster for image builds
    ws.image_build_compute="cpu-cluster"
    ml_client.workspaces.begin_update(ws)
    
    # To switch back to serverless compute:
    # ws.image_build_compute = ''
    # ml_client.workspaces.begin_update(ws)
    ```

    
    For more information, see the [begin_update](/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations#azure-ai-ml-operations-workspaceoperations-begin-update) method reference.

    # [Portal](#tab/portal)

    Currently there isn't a way to set the image build compute from the Azure portal.

    ---

> [!TIP]
> When ACR is behind a VNet, you can also [disable public access](/azure/container-registry/container-registry-access-selected-networks#disable-public-network-access) to it.

## Secure Azure Monitor and Application Insights

To enable network isolation for Azure Monitor and the Application Insights instance for the workspace, use the following steps:

1. Open your Application Insights resource in the Azure portal. The __Overview__ tab may or may not have a Workspace property. If it _doesn't_ have the property, perform step 2. If it _does_, then you can proceed directly to step 3.

    > [!TIP]
    > New workspaces create a workspace-based Application Insights resource by default. If your workspace was recently created, then you would not need to perform step 2.
   
1. Upgrade the Application Insights instance for your workspace. For steps on how to upgrade, see [Migrate to workspace-based Application Insights resources](/azure/azure-monitor/app/convert-classic-resource).

1. Create an Azure Monitor Private Link Scope and add the Application Insights instance from step 1 to the scope. For more information, see [Configure your Azure Monitor private link](/azure/azure-monitor/logs/private-link-configure).

## Securely connect to your workspace

[!INCLUDE [machine-learning-connect-secure-workspace](includes/machine-learning-connect-secure-workspace.md)]

## Workspace diagnostics

[!INCLUDE [machine-learning-workspace-diagnostics](includes/machine-learning-workspace-diagnostics.md)]

## Public access to workspace

> [!IMPORTANT]
> While this is a supported configuration for Azure Machine Learning, Microsoft doesn't recommend it. You should verify this configuration with your security team before using it in production.

In some cases, you may need to allow access to the workspace from the public network (without connecting through the virtual network using the methods detailed the [Securely connect to your workspace](#securely-connect-to-your-workspace) section). Access over the public internet is secured using TLS.

To enable public network access to the workspace, use the following steps:

1. [Enable public access](how-to-configure-private-link.md#enable-public-access) to the workspace after configuring the workspace's private endpoint.
1. [Configure the Azure Storage firewall](/azure/storage/common/storage-network-security?toc=%2fazure%2fstorage%2fblobs%2ftoc.json#grant-access-from-an-internet-ip-range) to allow communication with the IP address of clients that connect over the public internet. You may need to change the allowed IP address if the clients don't have a static IP. For example, if one of your Data Scientists is working from home and can't establish a VPN connection to the virtual network.

## Next steps

This article is part of a series on securing an Azure Machine Learning workflow. See the other articles in this series:

* [Virtual network overview](how-to-network-security-overview.md)
* [Secure the training environment](how-to-secure-training-vnet.md)
* [Secure the inference environment](how-to-secure-inferencing-vnet.md)
* [Enable studio functionality](how-to-enable-studio-virtual-network.md)
* [Use custom DNS](how-to-custom-dns.md)
* [Use a firewall](how-to-access-azureml-behind-firewall.md)
* [Tutorial: Create a secure workspace](tutorial-create-secure-workspace.md)
* [Bicep template](/samples/azure/azure-quickstart-templates/machine-learning-end-to-end-secure/)
* [Terraform template](https://github.com/Azure/terraform/tree/master/quickstart/201-machine-learning-moderately-secure).
* [API platform network isolation](how-to-configure-network-isolation-with-v2.md)
