---
title: Create a secure workspace with Azure Virtual Network
titleSuffix: Azure Machine Learning
description: Create an Azure Machine Learning workspace and required Azure services inside an Azure Virtual Network.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.reviewer: shshubhe
ms.author: scottpolly
author: s-polly
ms.date: 03/12/2026
ms.topic: how-to
monikerRange: 'azureml-api-2 || azureml-api-1'
ms.custom:
  - subject-rbac-steps
  - cliv2
  - build-2023
  - sfi-image-nochange
---
# Tutorial: How to create a secure workspace with an Azure Virtual Network

In this article, learn how to create and connect to a secure Azure Machine Learning workspace. The steps in this article use an Azure Virtual Network to create a security boundary around resources used by Azure Machine Learning. 

> [!IMPORTANT]
> Use the Azure Machine Learning managed virtual network instead of an Azure Virtual Network. For a version of this tutorial that uses a managed virtual network, see [Tutorial: Create a secure workspace with a managed virtual network](tutorial-create-secure-workspace.md).

In this tutorial, you accomplish the following tasks:

> [!div class="checklist"]
> * Create an Azure Virtual Network (VNet) to secure communications between services in the virtual network.
> * Create an Azure Storage Account (blob and file) behind the VNet. Use this service as the default storage for the workspace.
> * Create an Azure Key Vault behind the VNet. Use this service to store secrets used by the workspace, such as the security information needed to access the storage account.
> * Create an Azure Container Registry (ACR). Use this service as a repository for Docker images. Docker images provide the compute environments needed when training a machine learning model or deploying a trained model as an endpoint.
> * Create an Azure Machine Learning workspace.
> * Create a jump box. A jump box is an Azure Virtual Machine that is behind the VNet. Since the VNet restricts access from the public internet, use the jump box as a way to connect to resources behind the VNet.
> * Configure Azure Machine Learning studio to work behind a VNet. The studio provides a web interface for Azure Machine Learning.
> * Create an Azure Machine Learning compute cluster. Use a compute cluster when training machine learning models in the cloud. In configurations where Azure Container Registry is behind the VNet, it also builds Docker images.
> * Connect to the jump box and use the Azure Machine Learning studio.

> [!TIP]
> For a template that demonstrates how to create a secure workspace, see [Bicep template](/samples/azure/azure-quickstart-templates/machine-learning-end-to-end-secure/) or [Terraform template](https://github.com/Azure/terraform/tree/master/quickstart/201-machine-learning-moderately-secure).

After completing this tutorial, you have the following architecture:

* An Azure Virtual Network, which contains three subnets:
    * **Training**: Contains the Azure Machine Learning workspace, dependency services, and resources used for training models.
    * **Scoring**: For the steps in this tutorial, it isn't used. However if you continue using this workspace for other tutorials, use this subnet when deploying models to [endpoints](concept-endpoints.md).
    * **AzureBastionSubnet**: Used by the Azure Bastion service to securely connect clients to Azure Virtual Machines.
* An Azure Machine Learning workspace that uses a private endpoint to communicate by using the virtual network.
* An Azure Storage Account that uses private endpoints to allow storage services such as blob and file to communicate by using the virtual network.
* An Azure Container Registry that uses a private endpoint to communicate by using the virtual network.
* Azure Bastion, which you use your browser to securely communicate with the jump box VM inside the virtual network.
* An Azure Virtual Machine that you can remotely connect to and access resources secured inside the virtual network.
* An Azure Machine Learning compute instance and compute cluster.

> [!TIP]
> The Azure Batch Service listed on the diagram is a back-end service required by the compute clusters and compute instances.

:::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-secure-vnet-end-state.svg" alt-text="Diagram of the final architecture created through this tutorial." lightbox="./media/tutorial-create-secure-workspace-vnet/create-secure-vnet-end-state.png":::

## Prerequisites

* Familiarity with Azure Virtual Networks and IP networking. If you're not familiar, try the [Fundamentals of computer networking](/training/modules/network-fundamentals/) module.
* While most of the steps in this article use the Azure portal or the Azure Machine Learning studio, some steps use the Azure CLI extension for Machine Learning v2.

## Create a virtual network

To create a virtual network, use the following steps:

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Virtual Network** in the search field. Select the **Virtual Network** entry, and then select **Create**.


    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-resource-search-vnet.png" alt-text="Screenshot of the resource search form with virtual network selected.":::

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-resource-vnet.png" alt-text="Screenshot of the virtual network create form.":::

1. From the **Basics** tab, select the Azure **subscription** to use for this resource and then select or create a new **resource group**. Under **Instance details**, enter a friendly **name** for your virtual network and select the **region** to create it in.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-vnet-basics.png" alt-text="Screenshot of the basic virtual network configuration form.":::

1. Select **Security**. Select to **Enable Azure Bastion**. [Azure Bastion](/azure/bastion/bastion-overview) provides a secure way to access the VM jump box you create inside the virtual network in a later step. Use the following values for the remaining fields:

    * **Bastion name**: A unique name for this Bastion instance
    * **Public IP address**: Create a new public IP address.

    Leave the other fields at the default values.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-bastion.png" alt-text="Screenshot of Bastion config.":::

1. Select **IP Addresses**. The default settings should be similar to the following image:

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-vnet-ip-address-default.png" alt-text="Screenshot of the default IP Address form.":::

    Use the following steps to configure the IP address and configure a subnet for training and scoring resources:

    > [!TIP]
    > While you can use a single subnet for all Azure Machine Learning resources, the steps in this article show how to create two subnets to separate the training and scoring resources.
    >
    > The workspace and other dependency services go into the training subnet. They can still be used by resources in other subnets, such as the scoring subnet.

    1. Look at the default **IPv4 address space** value. In the screenshot, the value is **172.16.0.0/16**. **The value might be different for you**. While you can use a different value, the rest of the steps in this tutorial are based on the **172.16.0.0/16 value**.
    
        > [!WARNING]
        > Don't use the 172.17.0.0/16 IP address range for your virtual network. This range is the default subnet range used by the Docker bridge network, and it results in errors if you use it for your virtual network. Other ranges might also conflict depending on what you want to connect to the virtual network. For example, if you plan to connect your on-premises network to the virtual network, and your on-premises network also uses the 172.16.0.0/16 range. Ultimately, you need to plan your network infrastructure.

    1. Select the **Default** subnet and then select the **edit icon**.
    
        :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/edit-default-subnet.png" alt-text="Screenshot of selecting the edit icon of default subnet.":::

    1. Change the subnet **Name** to **Training**. Leave the other values at the default settings, and then select **Save** to save the changes.

    1. To create a subnet for compute resources used to _score_ your models, select **+ Add subnet** and set the name and address range:
        * **Subnet name**: Scoring
        * **Starting address**: 172.16.2.0
        * **Subnet size**: /24 (256 addresses)

        :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/vnet-add-scoring-subnet.png" alt-text="Screenshot of Scoring subnet.":::

    1. Select **Add** to add the subnet.

1. Select **Review + create**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-vnet-ip-address-final.png" alt-text="Screenshot of the review + create button.":::

1. Verify that the information is correct, and then select **Create**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-vnet-review.png" alt-text="Screenshot of the virtual network review and create page.":::

## Create a storage account

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Storage account**. Select the **Storage Account** entry, and then select **Create**.
1. From the **Basics** tab, select the **subscription**, **resource group**, and **region** you previously used for the virtual network. Enter a unique **Storage account name**, and set **Redundancy** to **Locally-redundant storage (LRS)**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-storage.png" alt-text="Screenshot of storage account basic config.":::

1. From the **Networking** tab, select **Disable public access** and then select **+ Add private endpoint**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-enable-private-endpoint.png" alt-text="Screenshot of the form to add the blob private network.":::

1. On the **Create private endpoint** form, use the following values:
    * **Subscription**: The same Azure subscription that contains the previous resources.
    * **Resource group**: The same Azure resource group that contains the previous resources.
    * **Location**: The same Azure region that contains the previous resources.
    * **Name**: A unique name for this private endpoint.
    * **Target sub-resource**: blob
    * **Virtual network**: The virtual network you created earlier.
    * **Subnet**: Training (172.16.0.0/24)
    * **Private DNS integration**: Yes
    * **Private DNS Zone**: privatelink.blob.core.windows.net

    Select **Add** to create the private endpoint.

1. Select **Review + create**. Verify that the information is correct, and then select **Create**.

1. Once the storage account is created, select **Go to resource**:

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-go-to-resource.png" alt-text="Screenshot of the go to new storage resource button.":::

1. From the left navigation, select **Networking**. Select the **Private endpoint connections** tab, and then select **+ Private endpoint**:

    > [!NOTE]
    > While you created a private endpoint for Blob storage in the previous steps, you must also create one for File storage.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-file-networking.png" alt-text="Screenshot of the storage account networking form.":::

1. On the **Create a private endpoint** form, use the same **subscription**, **resource group**, and **Region** that you used for previous resources. Enter a unique **Name**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-file-private-endpoint.png" alt-text="Screenshot of the basics form when adding the file private endpoint.":::

1. Select **Next : Resource**, and then set **Target sub-resource** to **file**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-file-private-endpoint-resource.png" alt-text="Screenshot of the resource form when selecting a subresource of 'file'.":::

1. Select **Next : Virtual Network**, and then use the following values:
    * **Virtual network**: The network you created previously
    * **Subnet**: Training

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-file-private-endpoint-config.png" alt-text="Screenshot of the configuration form when adding the file private endpoint.":::

1. Continue through the tabs selecting defaults until you reach **Review + Create**. Verify that the information is correct, and then select **Create**.

> [!TIP]
> If you plan to use a [batch endpoint](concept-endpoints.md) or an Azure Machine Learning pipeline that uses a [ParallelRunStep](./tutorial-pipeline-batch-scoring-classification.md), you also need to configure private endpoints that target **queue** and **table** subresources. `ParallelRunStep` internally uses queue and table for task scheduling and dispatching.

## Create a key vault

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Key Vault**. Select the **Key Vault** entry, and then select **Create**.
1. From the **Basics** tab, select the **subscription**, **resource group**, and **region** you previously used for the virtual network. Enter a unique **Key vault name**. Leave the other fields at the default value.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-key-vault.png" alt-text="Screenshot of the basics form when creating a new key vault.":::

1. From the **Networking** tab, deselect **Enable public access** and then select **+ create a private endpoint**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/key-vault-networking.png" alt-text="Screenshot of the networking form when adding a private endpoint for the key vault.":::

1. On the **Create private endpoint** form, use the following values:
    * **Subscription**: The same Azure subscription that contains the previous resources.
    * **Resource group**: The same Azure resource group that contains the previous resources.
    * **Location**: The same Azure region that contains the previous resources.
    * **Name**: A unique name for this private endpoint.
    * **Target sub-resource**: Vault
    * **Virtual network**: The virtual network you created earlier.
    * **Subnet**: Training (172.16.0.0/24)
    * **Enable Private DNS integration**: Yes
    * **Private DNS Zone**: Select the resource group that contains the virtual network and key vault.

    Select **Add** to create the private endpoint.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/key-vault-private-endpoint.png" alt-text="Screenshot of the key vault private endpoint configuration form.":::

1. Select **Review + create**. Verify that the information is correct, and then select **Create**.

1. When the key vault is created, select **Go to resource**.

1. From the left navigation, select **Networking**. On the **Firewalls and virtual networks** tab, select the checkbox for **Allow trusted Microsoft services to bypass this firewall** and select **Apply**.

## Create a container registry

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Container Registry**. Select the **Container Registry** entry, and then select **Create**.
1. From the **Basics** tab, select the **subscription**, **resource group**, and **location** you previously used for the virtual network. Enter a unique **Registry name** and set the **SKU** to **Premium**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-container-registry.png" alt-text="Screenshot of the basics form when creating a container registry.":::

1. From the **Networking** tab, select **Private endpoint** and then select **+ Add**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/container-registry-networking.png" alt-text="Screenshot of the networking form when adding a container registry private endpoint.":::

1. On the **Create private endpoint** form, use the following values:
    * **Subscription**: The same Azure subscription that contains the previous resources.
    * **Resource group**: The same Azure resource group that contains the previous resources.
    * **Location**: The same Azure region that contains the previous resources.
    * **Name**: A unique name for this private endpoint.
    * **Target sub-resource**: registry
    * **Virtual network**: The virtual network you created earlier.
    * **Subnet**: Training (172.16.0.0/24)
    * **Private DNS integration**: Yes
    * **Resource group**: Select the resource group that contains the virtual network and container registry.

    Select **Add** to create the private endpoint.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/container-registry-private-endpoint.png" alt-text="Screenshot of the configuration form for the container registry private endpoint.":::

1. Select **Review + create**. Verify that the information is correct, and then select **Create**.

1. After the container registry is created, select **Go to resource**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/container-registry-go-to-resource.png" alt-text="Screenshot of the go to resource button.":::

1. From the left of the page, select **Access keys**, and then enable **Admin user**. You need this setting when you use Azure Container Registry inside a virtual network with Azure Machine Learning.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/container-registry-admin-user.png" alt-text="Screenshot of the container registry access keys form, with the admin user option enabled.":::

## Create a workspace

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Machine Learning**. Select the **Machine Learning** entry, and then select **Create**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/machine-learning-create.png" alt-text="Screenshot of the create page for Azure Machine Learning.":::

1. From the **Basics** tab, select the **subscription**, **resource group**, and **Region** you previously used for the virtual network. Use the following values for the other fields:
    * **Name**: A unique name for your workspace.
    * **Storage account**: Select the storage account you created previously.
    * **Key vault**: Select the key vault you created previously.
    * **Application insights**: Use the default value.
    * **Container registry**: Use the container registry you created previously.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-machine-learning-workspace.png" alt-text="Screenshot of the basic workspace configuration form.":::

1. From the **Networking** tab, select **Private with Internet Outbound**. In the **Workspace inbound access** section, select **+ Add**.

1. On the **Create private endpoint** form, use the following values: 
    * **Subscription**: The same Azure subscription that contains the previous resources.
    * **Resource group**: The same Azure resource group that contains the previous resources.
    * **Location**: The same Azure region that contains the previous resources.
    * **Name**: A unique name for this private endpoint.
    * **Target sub-resource**: amlworkspace
    * **Virtual network**: The virtual network you created earlier.
    * **Subnet**: Training (172.16.0.0/24)
    * **Private DNS integration**: Yes
    * **Private DNS Zone**: Leave the two private DNS zones at the default values of **privatelink.api.azureml.ms** and **privatelink.notebooks.azure.net**.

    Select **OK** to create the private endpoint.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/machine-learning-workspace-private-endpoint.png" alt-text="Screenshot of the workspace private network configuration form.":::

1. From the **Networking** tab, in the **Workspace outbound access** section, select **Use my own virtual network**.
1. Select **Review + create**. Verify that the information is correct, and then select **Create**.
1. Once the workspace is created, select **Go to resource**.
1. From the **Settings** section on the left, select **Networking**, **Private endpoint connections**, and then select the link in the **Private endpoint** column:

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/workspace-private-endpoint-connections.png" alt-text="Screenshot of the private endpoint connections for the workspace.":::

1. Once the private endpoint information appears, select **DNS configuration** from the left of the page. Save the IP address and fully qualified domain name (FQDN) information on this page.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/workspace-private-endpoint-dns.png" alt-text="screenshot of the IP and FQDN entries for the workspace.":::

> [!IMPORTANT]
> There are still some configuration steps needed before you can fully use the workspace. However, these steps require you to connect to the workspace.

## Enable studio

Azure Machine Learning studio is a web-based application that you use to manage your workspace. However, it needs some extra configuration before you can use it with resources secured inside a virtual network. Use the following steps to enable studio:

1. When you use an Azure Storage Account that has a private endpoint, add the service principal for the workspace as a __Reader__ for the storage private endpoints. From the Azure portal, select your storage account and then select __Networking__. Next, select __Private endpoint connections__.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-private-endpoint-select.png" alt-text="Screenshot of storage private endpoint connections.":::

1. For __each private endpoint listed__, use the following steps:

    1. Select the link in the __Private endpoint__ column.
    
        :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/storage-private-endpoint-selected.png" alt-text="Screenshot of the endpoint links in the private endpoint column.":::

    1. Select __Access control (IAM)__ from the left side.
    1. Select __+ Add__, and then select __Add role assignment (Preview)__.

        ![Access control (IAM) page with Add role assignment menu open.](~/reusable-content/ce-skilling/azure/media/role-based-access-control/add-role-assignment-menu-generic.png)

    1. On the __Role__ tab, select the __Reader__ role.

        ![Add role assignment page with Role tab selected.](~/reusable-content/ce-skilling/azure/media/role-based-access-control/add-role-assignment-role-generic.png)

    1. On the __Members__ tab, select __User, group, or service principal__ in the __Assign access to__ area and then select __+ Select members__. In the __Select members__ dialog, enter the name as your Azure Machine Learning workspace. Select the service principal for the workspace, and then use the __Select__ button.

    1. On the **Review + assign** tab, select **Review + assign** to assign the role.

## Secure Azure Monitor and Application Insights

> [!NOTE]
> For more information on securing Azure Monitor and Application Insights, see the following links:
> * [Migrate to workspace-based Application Insights resources](/azure/azure-monitor/app/convert-classic-resource).
> * [Configure your Azure Monitor private link](/azure/azure-monitor/logs/private-link-configure).

1. In the [Azure portal](https://portal.azure.com), select **Home**, and then search for **Private link**. Select the **Azure Monitor Private Link Scope** result and then select **Create**.
1. From the **Basics** tab, select the same **Subscription**, **Resource Group**, and **Resource group region** as your Azure Machine Learning workspace. Enter a **Name** for the instance, and then select **Review + Create**. To create the instance, select **Create**.
1. After you create the Azure Monitor Private Link Scope instance, select the instance in the Azure portal. From the **Configure** section, select **Azure Monitor Resources** and then select **+ Add**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/add-monitor-resources.png" alt-text="Screenshot of the add button.":::

1. From **Select a scope**, use the filters to select the Application Insights instance for your Azure Machine Learning workspace. Select **Apply** to add the instance.
1. From the **Configure** section, select **Private Endpoint connections** and then select **+ Private Endpoint**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/private-endpoint-connections.png" alt-text="Screenshot of the add private endpoint button.":::

1. Select the same **Subscription**, **Resource Group**, and **Region** that contains your virtual network. Select **Next: Resource**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/monitor-private-endpoint-basics.png" alt-text="Screenshot of the Azure Monitor private endpoint basics.":::

1. Select `Microsoft.insights/privateLinkScopes` as the **Resource type**. Select the Private Link Scope you created earlier as the **Resource**. Select `azuremonitor` as the **Target sub-resource**. Select **Next: Virtual Network** to continue.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/monitor-private-endpoint-resource.png" alt-text="Screenshot of the Azure Monitor private endpoint resources.":::

1. Select the **Virtual network** you created earlier, and the **Training** subnet. Select **Next** until you arrive at **Review + Create**. Select **Create** to create the private endpoint.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/monitor-private-endpoint-network.png" alt-text="Screenshot of the Azure Monitor private endpoint network.":::

1. After you create the private endpoint, return to the **Azure Monitor Private Link Scope** resource in the portal. From the **Configure** section, select **Access modes**. Select **Private only** for **Ingestion access mode** and **Query access mode**, and then select **Save**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/access-modes.png" alt-text="Screenshot of the private link scope access modes.":::

## Connect to the workspace

You can connect to the secured workspace in several ways. The steps in this article use a **jump box**, which is a virtual machine in the virtual network. You can connect to it by using your web browser and Azure Bastion. The following table lists several other ways that you might connect to the secure workspace:

| Method | Description |
| ----- | ----- |
| [Azure VPN gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) | Connects on-premises networks to the virtual network over a private connection. Connection is made over the public internet. |
| [ExpressRoute](https://azure.microsoft.com/services/expressroute/) | Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider. |

> [!IMPORTANT]
> When you use a **VPN gateway** or **ExpressRoute**, you need to plan how name resolution works between your on-premises resources and those in the virtual network. For more information, see [Use a custom DNS server](how-to-custom-dns.md).

### Create a jump box (VM)

Use the following steps to create an Azure Virtual Machine to use as a jump box. By using Azure Bastion, you can connect to the VM desktop through your browser. From the VM desktop, you can use the browser on the VM to connect to resources inside the virtual network, such as Azure Machine Learning studio. Or you can install development tools on the VM. 

> [!TIP]
> The following steps create a Windows 11 enterprise VM. Depending on your requirements, you might want to select a different VM image. The Windows 11 (or 10) enterprise image is useful if you need to join the VM to your organization's domain.

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Virtual Machine**. Select the **Virtual Machine** entry, and then select **Create**.

1. From the **Basics** tab, select the **subscription**, **resource group**, and **Region** you previously used for the virtual network. Provide values for the following fields:

    * **Virtual machine name**: A unique name for the VM.
    * **Username**: The username you use to sign in to the VM.
    * **Password**: The password for the username.
    * **Security type**: Standard.
    * **Image**: Windows 11 Enterprise.

        > [!TIP]
        > If Windows 11 Enterprise isn't in the list for image selection, use **See all images**. Find the **Windows 11** entry from Microsoft, and use the **Select** drop-down to select the enterprise image.


    You can leave other fields at the default values.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-virtual-machine-basic.png" alt-text="Screenshot of the virtual machine basics configuration.":::

1. Select **Networking**, and then select the **Virtual network** you created earlier. Use the following information to set the remaining fields:

    * Select the **Training** subnet.
    * Set the **Public IP** to **None**.
    * Leave the other fields at the default value.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-virtual-machine-network.png" alt-text="Screenshot of the virtual machine network configuration.":::

1. Select **Review + create**. Verify that the information is correct, and then select **Create**.


### Connect to the jump box

1. After the virtual machine is created, select **Go to resource**.
1. From the top of the page, select **Connect** and then **Connect via Bastion**.

    > [!TIP]
    > Azure Bastion uses port 443 for inbound communication. If you have a firewall that restricts outbound traffic, make sure it allows traffic on port 443 to the Azure Bastion service. For more information, see [Working with NSGs and Azure Bastion](/azure/bastion/bastion-nsg).

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/virtual-machine-connect.png" alt-text="Screenshot of the connect list, with Bastion selected.":::

1. Enter your authentication information for the virtual machine. A connection is established in your browser.

## Create a compute cluster and instance

A compute instance provides a Jupyter Notebook experience on a shared compute resource attached to your workspace.

1. From an Azure Bastion connection to the jump box, open the **Microsoft Edge** browser on the remote desktop.
1. In the remote browser session, go to **https://ml.azure.com**. When prompted, authenticate by using your Microsoft Entra account.
1. From the **Welcome to studio!** screen, select the **Machine Learning workspace** you created earlier and then select **Get started**.

    > [!TIP]
    > If your Microsoft Entra account has access to multiple subscriptions or directories, use the **Directory and Subscription** dropdown to select the one that contains the workspace.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/studio-select-workspace.png" alt-text="Screenshot of the select Machine Learning workspace form.":::

1. From studio, select **Compute**, **Compute clusters**, and then **+ New**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/studio-new-compute-cluster.png" alt-text="Screenshot of the compute clusters page, with the new button selected.":::

1. From the Virtual Machine dialog, select **Next** to accept the default virtual machine configuration.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/studio-new-compute-vm.png" alt-text="Screenshot of the compute cluster virtual machine configuration.":::

1. From the Configure Settings dialog, enter `cpu-cluster` as the Compute name. Set the Subnet to `Training` and then select **Create** to create the cluster.

    > [!TIP]
    > Compute clusters dynamically scale the nodes in the cluster as needed. Leave the minimum number of nodes at 0 to reduce costs when the cluster isn't in use.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/studio-new-compute-settings.png" alt-text="Screenshot of the configure settings form.":::

1. From studio, select **Compute**, **Compute instance**, and then **+ New**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-compute-instance.png" alt-text="Screenshot of the compute instances page, with the new button selected.":::

1. From **Required settings**, enter a unique **Computer name** and select **Next**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-compute-instance-vm.png" alt-text="Screenshot of compute instance virtual machine configuration.":::

1. Continue selecting **Next** until you arrive at **Security** dialog, select the **Virtual network** and set the **Subnet** to **Training**. Select **Review + Create** and then select **Create**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/create-compute-instance-settings.png" alt-text="Screenshot of the advanced settings.":::

> [!TIP]
> When you create a compute cluster or compute instance, Azure Machine Learning dynamically adds a Network Security Group (NSG). This NSG contains the following rules, which are specific to compute cluster and compute instance:
> 
> * Allow inbound TCP traffic on ports 29876-29877 from the `BatchNodeManagement` service tag.
> * Allow inbound TCP traffic on port 44224 from the `AzureMachineLearning` service tag.
>
> The following screenshot shows an example of these rules:
>
> :::image type="content" source="./media/how-to-secure-training-vnet/compute-instance-cluster-network-security-group.png" alt-text="Screenshot of NSG":::

For more information on creating a compute cluster and compute instance, including how to do so with Python and the CLI, see the following articles:

* [Create a compute cluster](how-to-create-attach-compute-cluster.md)
* [Create a compute instance](how-to-create-compute-instance.md)

## Configure image builds

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

When Azure Container Registry is behind the virtual network, Azure Machine Learning can't use it to directly build Docker images (used for training and deployment). Instead, configure the workspace to use the compute cluster you created earlier. Use the following steps to create a compute cluster and configure the workspace to use it to build images:

1. Go to [https://shell.azure.com/](https://shell.azure.com/) to open the Azure Cloud Shell.
1. From the Cloud Shell, use the following command to install the 2.0 CLI for Azure Machine Learning:
 
    ```azurecli-interactive
    az extension add -n ml
    ```

1. Update the workspace to use the compute cluster to build Docker images. Replace `docs-ml-rg` with your resource group. Replace `docs-ml-ws` with your workspace. Replace `cpu-cluster` with the compute cluster name:
    
    ```azurecli-interactive
    az ml workspace update \
      -n docs-ml-ws \
      -g docs-ml-rg \
      -i cpu-cluster
    ```

    > [!NOTE]
    > You can use the same compute cluster to train models and build Docker images for the workspace.

## Use the workspace

> [!IMPORTANT]
> The steps in this article put Azure Container Registry behind the virtual network. In this configuration, you can't deploy a model to Azure Container Instances inside the virtual network. Don't use Azure Container Instances with Azure Machine Learning in a virtual network. For more information, see [Secure the inference environment (SDK/CLI v1)](./v1/how-to-secure-inferencing-vnet.md).
>
> As an alternative to Azure Container Instances, try Azure Machine Learning managed online endpoints. For more information, see [Enable network isolation for managed online endpoints](how-to-secure-online-endpoint.md).

At this point, you can use the studio to interactively work with notebooks on the compute instance and run training jobs on the compute cluster. For a tutorial on using the compute instance and compute cluster, see [Tutorial: Azure Machine Learning in a day](tutorial-azure-ml-in-a-day.md).

## Stop compute instance and jump box

> [!WARNING]
> While it's running (started), the compute instance and jump box continue charging your subscription. To avoid excess cost, __stop__ them when they're not in use.

The compute cluster dynamically scales between the minimum and maximum node count set when you create it. If you accept the defaults, the minimum is 0, which effectively turns off the cluster when not in use.
### Stop the compute instance

From studio, select **Compute**, **Compute clusters**, and then select the compute instance. Finally, select **Stop** from the top of the page.

:::image type="content" source="./media/tutorial-create-secure-workspace-vnet/compute-instance-stop.png" alt-text="Screenshot of the stop button for the compute instance.":::

### Stop the jump box

After you create the jump box, select the virtual machine in the Azure portal and then use the **Stop** button. When you're ready to use it again, use the **Start** button to start it.

:::image type="content" source="./media/tutorial-create-secure-workspace-vnet/virtual-machine-stop.png" alt-text="Screenshot of the stop button for the jump box virtual machine.":::

You can also configure the jump box to automatically shut down at a specific time. To do so, select **Auto-shutdown**, **Enable**, set a time, and then select **Save**.

:::image type="content" source="./media/tutorial-create-secure-workspace-vnet/virtual-machine-auto-shutdown.png" alt-text="Screenshot of the autoshutdown option.":::

## Clean up resources

If you plan to keep using the secured workspace and other resources, skip this section.

To delete all resources created in this tutorial, use the following steps:

1. In the Azure portal, select **Resource groups** on the far left.
1. From the list, select the resource group that you created in this tutorial.
1. Select **Delete resource group**.

    :::image type="content" source="./media/tutorial-create-secure-workspace-vnet/delete-resources.png" alt-text="Screenshot of the delete resource group link.":::

1. Enter the resource group name, and then select **Delete**.
## Next steps

:::moniker range="azureml-api-2"
Now that you have a secure workspace and can access studio, learn how to [deploy a model to an online endpoint with network isolation](how-to-secure-online-endpoint.md).
:::moniker-end
:::moniker range="azureml-api-1"
Now that you have a secure workspace, learn how to [deploy a model](./v1/how-to-deploy-and-where.md).
:::moniker-end
