---
title: Use Model Catalog collections with workspace managed virtual network
titleSuffix: Azure Machine Learning
description: Learn how to use the Model Catalog in an isolated network.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.topic: how-to
author: ssalgadodev
ms.author: ssalgado
ms.reviewer: timanghn
ms.date: 12/15/2023
ms.collection: ce-skilling-ai-copilot
---

# Use Model Catalog collections with workspace managed virtual network

In this article, you learn how to use the various collections in the Model Catalog within an isolated network. 

Workspace [managed virtual network](./how-to-network-isolation-planning.md) is the only way to support network isolation with the Model Catalog. It provides easily configuration to secure your workspace. After you enable managed virtual network in the workspace level, resources related to workspace in the same virtual network, will use the same network setting in the workspace level. You can also configure the workspace to use private endpoint to access other Azure resources such as Azure OpenAI. Furthermore, you can configure FQDN rule to approve outbound to non-Azure resources, which is required to use some of the collections in the Model Catalog. See [how to Workspace managed network isolation](./how-to-managed-network.md) to enable workspace managed virtual network.

The creation of the managed virtual network is deferred until a compute resource is created or provisioning is manually started. You can use following command to manually trigger network provisioning.
```bash
az ml workspace provision-network --subscription <sub_id> -g <resource_group_name> -n <workspace_name>
```

## Workspace managed virtual network to allow internet outbound

1. Configure a workspace with managed virtual network to allow internet outbound by following the steps listed [here](./how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-internet-outbound).
2. If you choose to set the public network access to the workspace to disabled, you can connect to the workspace using one of the following methods:

     * [Azure VPN gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) - Connects on-premises networks to the virtual network over a private connection. Connection is made over the public internet. There are two types of VPN gateways that you might use: 

        * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network. 
        * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network. 

    * [ExpressRoute](https://azure.microsoft.com/products/expressroute/) - Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider. 

    * [Azure Bastion](/azure/bastion/bastion-overview) - In this scenario, you create an Azure Virtual Machine (sometimes called a jump box) inside the virtual network. You then connect to the VM using Azure Bastion. Bastion allows you to connect to the VM using either an RDP or SSH session from your local web browser. You then use the jump box as your development environment. Since it is inside the virtual network, it can directly access the workspace.

Since the workspace managed virtual network can access internet in this configuration, you can work with all the Collections in the Model Catalog from within the workspace. 

## Workspace managed virtual network to allow only approved outbound

1. Configure a workspace by following [Workspace managed network isolation](./how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-only-approved-outbound). In step 3 of the tutorial when selecting **Workspace managed outbound access**, select **Allow Only Approved Outbound**.  
2. If you set the public network access to the workspace to disabled, you can connect to the workspace using one of the methods as listed [in step 2 of the allow internet outbound section of this tutorial](#workspace-managed-virtual-network-to-allow-internet-outbound).
3. The workspace manages virtual network is set to an allow only configuration. You must add a corresponding user-defined outbound rule to allow all the relevant FQDNs.
    1. Follow this link for a list of FQDNs required for the [Curated by Azure AI collection](#language-models-in-curated-by-azure-ai-collection).
    2. Follow this link for a list of FQDNs required for the [Hugging Face collection](#work-with-hugging-face-collection). 

## Work with open source models curated by Azure Machine Learning

Workspace managed virtual network to allow only approved outbound uses a Service Endpoint Policy to Azure Machine Learning managed storage accounts, to help access the models in the collections curated by Azure Machine Learning in an out-of-the-box manner. This mode of workspace configuration also has default outbound to the Microsoft Container Registry that contains the docker image used to deploy the models. 

### Language models in 'Curated by Azure AI' collection

These models involve dynamic installation of dependencies at runtime. To add a user defined outbound rule, follow step four of 
To use the Curated by Azure AI collection, users should add user defined outbound rules for the following FQDNs at the workspace level:

  * `*.anaconda.org`
  * `*.anaconda.com`
  * `anaconda.com`
  * `pypi.org`
  * `*.pythonhosted.org`
  * `*.pytorch.org`
  * `pytorch.org`

Follow Step 4 in the [managed virtual network tutorial](./how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-only-approved-outbound) to add the corresponding user-defined outbound rules. 

> [!WARNING]
> FQDN outbound rules are implemented using Azure Firewall. If you use outbound FQDN rules, charges for Azure Firewall are included in your billing. For more information, see [Pricing](./how-to-managed-network.md#pricing).
  
### Meta collection 

Users can work with this collection in network isolated workspaces with no other user defined outbound rules required. 

> [!NOTE]
> New curated collections are added to the Model Catalog frequently. We will update this documentation to reflect the support in private networks for various collections.

## Work with Hugging Face collection 

The model weights aren't hosted on Azure if you're using the Hugging Face registry. The model weights are downloaded directly from Hugging Face hub to the online endpoints in your workspace during deployment.
Users need to add the following outbound FQDNs rules for Hugging Face Hub, Docker Hub and their CDNs to allow traffic to the following hosts: 

  * `docker.io`
  * `huggingface.co`
  * `production.cloudflare.docker.com`
  * `cdn-lfs.huggingface.co`
  * `cdn.auth0.com`

Follow Step 4 in the [managed virtual network tutorial](./how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-only-approved-outbound) to add the corresponding user-defined outbound rules. 

## Next steps 

* Learn how-to [troubleshoot managed virtual network](./how-to-troubleshoot-managed-network.md)
  
