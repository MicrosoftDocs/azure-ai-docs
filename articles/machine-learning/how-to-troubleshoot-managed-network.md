---
title: Troubleshooting managed virtual networks
titleSuffix: Azure Machine Learning
description: Learn how to troubleshoot Azure Machine Learning managed virtual network.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.reviewer: shshubhe
ms.author: scottpolly
author: s-polly
ms.topic: troubleshooting
ms.date: 04/01/2025
ms.custom: build-2023
---

# Troubleshoot Azure Machine Learning managed virtual network

This article provides information on troubleshooting common issues with Azure Machine Learning managed virtual network.

## Can I still use an Azure Virtual Network?

Yes, you can still use an Azure Virtual Network for network isolation. If you're using the v2 __Azure CLI__ and __Python SDK__, the process is the same as before the introduction of the managed virtual network feature. The process through the Azure portal changed slightly.

To use an Azure Virtual Network when creating a workspace through the Azure portal, use the following steps:

1. When creating a workspace, select the __Networking__ tag.
1. Select __Private with Internet Outbound__.
1. In the __Workspace inbound access__ section, select __Add__ and add a private endpoint for the Azure Virtual Network to use for network isolation.
1. In the __Workspace Outbound access__ section, select __Use my own virtual network__.
1. Continue to create the workspace as normal.

## Doesn't have authorization to perform action 'Microsoft.MachineLearningServices<br/> /workspaces/privateEndpointConnections/read'

When you create a managed virtual network, the operation can fail with an error similar to the following text:

"The client '\<GUID\>' with object ID '\<GUID\>' doesn't have authorization to perform action 'Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read' over scope '/subscriptions/\<GUID\>/resourceGroups/\<resource-group-name\>/providers/Microsoft.MachineLearningServices/workspaces/\<workspace-name\>' or the scope is invalid."

This error occurs when the Azure identity used to create the managed virtual network doesn't have the following Azure role-based access control permissions:

* Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read
* Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write

## Troubleshoot configurations on connecting to storage

When you create a workspace, required outbound rules to Azure storage are autocreated for data upload scenarios and artifact storage. Ensure your Azure storage is set up correct by checked with the following steps:

1. In Azure portal, check the network settings of the storage account that is associated to your hub.
  * If public network access is set to __Enabled from selected virtual networks and IP addresses__, ensure the correct IP address ranges are added to access your storage account.
  * If public network access is set to __Disabled__, ensure you have a private endpoint configured from your Azure virtual network to your storage account with Target subresource as blob. In addition, you must grant the [Reader](/azure/role-based-access-control/built-in-roles#reader) role for the storage account private endpoint to the managed identity.
2. In Azure portal, navigate to your Azure Machine Learning workspace. Ensure the managed virtual network is provisioned and the outbound private endpoint to blob storage is Active.

## Next steps

For more information, see [Managed virtual networks](how-to-managed-network.md).
