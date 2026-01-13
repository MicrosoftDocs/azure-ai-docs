---
title: Network isolation in prompt flow
titleSuffix: Azure Machine Learning
description: Learn how to secure prompt flow with virtual network.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: sooryar 
ms.date: 7/10/2025
ms.custom:
  - ignite-2023
  - sfi-image-nochange
ms.update-cycle: 365-days
---

# Network isolation in prompt flow 

You can secure prompt flow using private networks. This article explains the requirements to use prompt flow in an environment secured by private networks.

## Involved services

When you develop AI applications using prompt flow, you need a secured environment. You can configure network isolation for the following services:

### Core Azure Machine Learning services

- **Workspace**: Configure the Azure Machine Learning workspace as private and restrict its inbound and outbound traffic.
- **Compute resource**: Apply inbound and outbound rules to limit compute resource access within the workspace.
- **Storage account**: Restrict storage account accessibility to a specific virtual network.
- **Container registry**: Secure your container registry using virtual network configuration.
- **Endpoint**: Control which Azure services or IP addresses can access your deployed endpoints.

### Foundry Tools

- **Azure OpenAI**: Use network configuration to make Azure OpenAI private, then use private endpoints for Azure Machine Learning communication.
- **Azure Content Safety**: Configure private network access and establish private endpoints for secure communication.
- **Azure AI Search**: Enable private network settings and use private endpoints for secure integration.

### External resources

- **Non-Azure resources**: For external APIs like SerpAPI, add FQDN rules to your outbound traffic restrictions to maintain access.

## Options in different network setups

In Azure Machine Learning, we have two options to secure network isolation: bring your own network or use a workspace-managed virtual network. Learn more about [Secure workspace resources](../how-to-network-isolation-planning.md).

Here's a table to illustrate the options in different network setups for prompt flow.

| Ingress | Egress  | Compute type in authoring                      | Compute type in inference           | Network options for workspace |
|---------|---------|------------------------------------------------|-------------------------------------|-------------------------------|
| Public  | Public  | Serverless (recommended), Compute instance     | Managed online endpoint (recommended) | Managed (recommended)         |
| Public  | Public  | Serverless (recommended), Compute instance     | K8s online endpoint                 | Bring your own                |
| Private | Public  | Serverless (recommended), Compute instance     | Managed online endpoint (recommended) | Managed (recommended)         |
| Private | Public  | Serverless (recommended), Compute instance     | K8s online endpoint                 | Bring your own                |
| Public  | Private | Serverless (recommended), Compute instance     | Managed online endpoint             | Managed                       |
| Private | Private | Serverless (recommended), Compute instance     | Managed online endpoint             | Managed                       |

- In private virtual network scenarios, we recommend using a workspace-enabled managed virtual network. It's the easiest way to secure your workspace and related resources. 
- The use of managed vNet and bring your own virtual network in a single workspace isn't supported. Additionally, since managed online endpoint is supported only with a managed virtual network, you can't deploy prompt flow to managed online endpoint in a workspace with an enabled bring your own virtual network.
- You can have one workspace for prompt flow authoring with your own virtual network,  and another workspace for prompt flow deployment using a  managed online endpoint with a workspace-managed virtual network.

## Secure prompt flow with workspace-managed virtual network

A workspace-managed virtual network is the recommended way to support network isolation in prompt flow. It provides an easy configuration to secure your workspace. After you enable managed vNet at the workspace level, resources related to the workspace in the same virtual network will use the same network settings at the workspace level. You can also configure the workspace to use private endpoints to access other Azure resources such as Azure OpenAI, Azure content safety, and Azure AI Search. You can also configure FQDN rules to approve outbound connections to non-Azure resources used by your prompt flow such as SerpAPI.

1. Follow [workspace-managed network isolation](../how-to-managed-network.md) to enable workspace-managed virtual network.

    > [!IMPORTANT]
    > The creation of the managed virtual network is deferred until a compute resource is created or provisioning is manually started. You can use the following command to manually trigger network provisioning.
    ```bash
    az ml workspace provision-network --subscription <sub_id> -g <resource_group_name> -n <workspace_name>
    ```

2. Add workspace MSI as `Storage File Data Privileged Contributor` to the storage account linked with the workspace.

    2.1 Go to Azure portal and find the workspace.

    :::image type="content" source="./media/how-to-secure-prompt-flow/go-to-azure-portal.png" alt-text="Diagram showing how to go from Azure Machine Learning portal to Azure portal." lightbox = "./media/how-to-secure-prompt-flow/go-to-azure-portal.png":::

    2.2 Find the storage account linked with the workspace.

    :::image type="content" source="./media/how-to-secure-prompt-flow/linked-storage.png" alt-text="Diagram showing how to find workspace linked storage account in Azure portal." lightbox = "./media/how-to-secure-prompt-flow/linked-storage.png":::

    2.3 Navigate to the role assignment page of the storage account.

    :::image type="content" source="./media/how-to-secure-prompt-flow/add-role-storage.png" alt-text="Diagram showing how to jump to role assignment of storage account." lightbox = "./media/how-to-secure-prompt-flow/add-role-storage.png":::

    2.4 Find the storage file data privileged contributor role.

    :::image type="content" source="./media/how-to-secure-prompt-flow/storage-file-data-privileged-contributor.png" alt-text="Diagram showing how to find storage file data privileged contributor role." lightbox = "./media/how-to-secure-prompt-flow/storage-file-data-privileged-contributor.png":::
    
    2.5 Assign the storage file data privileged contributor role to the workspace managed identity.

    :::image type="content" source="./media/how-to-secure-prompt-flow/managed-identity-workspace.png" alt-text="Diagram showing how to assign storage file data privileged contributor role to workspace managed identity." lightbox = "./media/how-to-secure-prompt-flow/managed-identity-workspace.png":::

    > [!NOTE]
    > This operation might take several minutes to take effect.

3. If you want to communicate with [private Foundry Tools](/azure/ai-services/cognitive-services-virtual-networks), you need to add related user-defined outbound rules to the related resource. The Azure Machine Learning workspace creates a private endpoint in the related resource with autoapproval. If the status is stuck in pending, go to the related resource to approve the private endpoint manually.

    :::image type="content" source="./media/how-to-secure-prompt-flow/outbound-rule-cognitive-services.png" alt-text="Screenshot of user defined outbound rule for Foundry Tools." lightbox = "./media/how-to-secure-prompt-flow/outbound-rule-cognitive-services.png":::

    :::image type="content" source="./media/how-to-secure-prompt-flow/outbound-private-endpoint-approve.png" alt-text="Screenshot of user approve private endpoint." lightbox = "./media/how-to-secure-prompt-flow/outbound-private-endpoint-approve.png":::

4. If you're restricting outbound traffic to only allow specific destinations, you must add a corresponding user-defined outbound rule to allow the relevant FQDN.

    :::image type="content" source="./media/how-to-secure-prompt-flow/outbound-rule-non-azure-resources.png" alt-text="Screenshot of user defined outbound rule for non Azure resource." lightbox = "./media/how-to-secure-prompt-flow/outbound-rule-non-azure-resources.png":::

5. In workspaces that enable managed VNet, you can only deploy prompt flow to managed online endpoints. You can follow [Secure your managed online endpoints with network isolation](../how-to-secure-kubernetes-inferencing-environment.md) to secure your managed online endpoint.

## Secure prompt flow using your own virtual network

- To set up Azure Machine Learning related resources as private, see [Secure workspace resources](../how-to-secure-workspace-vnet.md).
- If you have strict outbound rules, make sure you have opened the [Required public internet access](../how-to-secure-workspace-vnet.md#required-public-internet-access).
- Add workspace MSI as `Storage File Data Privileged Contributor` to the storage account linked with the workspace. Follow step 2 in [Secure prompt flow with workspace managed vNet](#secure-prompt-flow-with-workspace-managed-virtual-network).
- If you're using serverless compute type in flow authoring, you need to set the custom virtual network at the workspace level. Learn more about [Secure an Azure Machine Learning training environment with virtual networks](../how-to-secure-training-vnet.md)

    ```yaml
    serverless_compute:
      custom_subnet: /subscriptions/<sub id>/resourceGroups/<resource group>/providers/Microsoft.Network/virtualNetworks/<vnet name>/subnets/<subnet name>
      no_public_ip: false # Set to true if you don't want to assign public IP to the compute
    ```

- Meanwhile, you can follow [private Foundry Tools](/azure/ai-services/cognitive-services-virtual-networks) to make them private.
- If you want to deploy prompt flow in a workspace that is secured by your own virtual network, you can deploy it to an AKS cluster that is in the same virtual network. You can follow [Secure Azure Kubernetes Service inferencing environment](../how-to-secure-kubernetes-inferencing-environment.md) to secure your AKS cluster. Learn more about [How to deploy prompt flow to AKS cluster via code](./how-to-deploy-to-code.md).
- You can either create a private endpoint to the same virtual network or use virtual network peering to make them communicate with each other.

## Known limitations

- Managed online endpoints with selected egress require a workspace with managed vNet. If you're using your own virtual network, consider this two-workspace approach:
      - Use one workspace with your virtual network for prompt flow authoring
      - Use a separate workspace with managed vNet for prompt flow deployment via managed online endpoint

## Next steps

- [Secure workspace resources](../how-to-secure-workspace-vnet.md)
- [Workspace managed network isolation](../how-to-managed-network.md)
- [Secure Azure Kubernetes Service inferencing environment](../how-to-secure-kubernetes-inferencing-environment.md)
- [Secure your managed online endpoints with network isolation](../how-to-secure-online-endpoint.md)
- [Secure your RAG workflows with network isolation](../how-to-secure-rag-workflows.md)
