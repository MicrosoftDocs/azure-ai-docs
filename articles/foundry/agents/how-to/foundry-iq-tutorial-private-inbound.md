---
title: "Set Up Private Inbound Connectivity"
titleSuffix: Foundry IQ
description: Set up and verify private inbound connectivity between Foundry Agent Service and Azure AI Search for private agentic retrieval with Foundry IQ.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: tutorial
ms.date: 06/26/2026
author: haileytap
ms.author: haileytapia
ms.reviewer: magottei
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#customer intent: As a platform engineer, I want to deploy Microsoft Foundry and Azure AI Search in private mode so that my agents can retrieve from private knowledge bases over secure network paths.
---

# Set up private inbound connectivity

> [!IMPORTANT]
> This tutorial series uses the 2026-05-01-preview REST API for agentic retrieval. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

This article is part one of a three-part tutorial series. In this part of the tutorial, you set up inbound private connectivity from Microsoft Foundry to Azure AI Search. By establishing this private request path, you ensure that later retrieval and dependency validation occur inside the intended network boundary.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) where your account has `Contributor` or `Owner` access at the subscription or resource group scope used for this tutorial.

- The following resource providers [registered in your subscription](/azure/azure-resource-manager/management/resource-providers-and-types):
  - `Microsoft.CognitiveServices`
  - `Microsoft.MachineLearningServices`
  - `Microsoft.App`
  - `Microsoft.ContainerService`
  - `Microsoft.ContainerRegistry`
  - `Microsoft.Network`
  - `Microsoft.Search`
  - `Microsoft.Storage`
  - `Microsoft.DocumentDB`

- The [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated with `az login`.

- An in-VNet client, such as a jumpbox, VM, dev box, or Azure Bastion-connected workstation, connected to the private network path used in your deployment and able to reach your private endpoints. You use this same client in part three to run data plane REST calls over private endpoints.

## Create a private network

Create the virtual network boundaries that carry private traffic between Foundry and Azure AI Search. This section defines subnets for runtime, private endpoints, and optional in-VNet test clients.

To create the private network:

1. Create the resource group and VNet.

   ```bash
   az group create \
     --name rg-private-retrieval \
     --location westus3

   az network vnet create \
     --resource-group rg-private-retrieval \
     --name vnet-private-retrieval \
     --location westus3 \
     --address-prefixes 10.42.0.0/16
   ```

1. Create two subnets: `agent-subnet` for agent runtime and `pe-subnet` for private endpoints.

   > [!IMPORTANT]
   > The deployment requires `agent-subnet` to be dedicated to this environment. If the subnet is already used by another environment or service, deployment can fail. Use a new VNet or a new, unused subnet range for each isolated tutorial deployment.

   ```bash
   # Agent runtime subnet
   az network vnet subnet create \
     --resource-group rg-private-retrieval \
     --vnet-name vnet-private-retrieval \
     --name agent-subnet \
     --address-prefixes 10.42.0.0/24

   # Private endpoint subnet
   az network vnet subnet create \
     --resource-group rg-private-retrieval \
     --vnet-name vnet-private-retrieval \
     --name pe-subnet \
     --address-prefixes 10.42.1.0/24
   ```

1. (Optional) Create an in-VNet subnet named `mcp-subnet` if you need to place workloads inside the VNet, such as jumpboxes, validation VMs, or MCP hosts. If you don't need in-VNet components, skip this step.

   ```bash
   # In-VNet test subnet
   az network vnet subnet create \
     --resource-group rg-private-retrieval \
     --vnet-name vnet-private-retrieval \
     --name mcp-subnet \
     --address-prefixes 10.42.2.0/24
   ```

## Deploy private infrastructure

With the network in place, use the [foundry-samples](https://github.com/microsoft-foundry/foundry-samples) deployment artifact to create the private infrastructure (private services, private endpoints, and private DNS zones) for this tutorial series.

To deploy the private infrastructure:

1. Get your subscription ID to use as `<subscription-id>` throughout the tutorial series.

   ```azurecli
   az account show --query id -o tsv
   ```

1. Set the deployment template URL and the existing VNet resource ID used by the deployment.

   ```bash
   templateUri='https://raw.githubusercontent.com/microsoft-foundry/foundry-samples/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup/azuredeploy.json'
   vnetId='/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Network/virtualNetworks/vnet-private-retrieval'
   ```

1. Validate the deployment configuration.

   ```bash
   az deployment group validate \
     --resource-group rg-private-retrieval \
     --template-uri "$templateUri" \
     --parameters \
       location='westus3' \
       aiServices='private-retrieval' \
       firstProjectName='project-private-retrieval' \
       displayName='private foundry project' \
       projectDescription='Private Foundry plus private Azure AI Search' \
       vnetName='vnet-private-retrieval' \
       existingVnetResourceId="$vnetId" \
       agentSubnetName='agent-subnet' \
       peSubnetName='pe-subnet' \
       agentSubnetPrefix='10.42.0.0/24' \
       peSubnetPrefix='10.42.1.0/24'
   ```

   If your subscription enforces a policy that requires Azure AI Search to disable local authentication, this sample deployment can be denied during validation or deployment. In that case, precreate a compliant Azure AI Search service and reuse it by supplying the optional `aiSearchResourceId` template parameter.

   A compliant bring-your-own Search service for this tutorial should meet the following requirements before you pass its resource ID to the template:

   - A supported region and SKU for agentic retrieval.
   - A system-assigned managed identity.
   - Role-based access enabled for the data plane.
   - Local authentication disabled if required by policy.
   - Public network access disabled if required by policy.

   For example:

   ```azurecli
   az search service create \
     --name <search-service-name> \
     --resource-group rg-private-retrieval \
     --location westus3 \
     --sku standard \
     --identity-type SystemAssigned \
     --disable-local-auth true \
     --public-access disabled
   ```

1. Deploy the private services, endpoints, and DNS zones.

   The deployment typically takes 10 to 20 minutes to finish, and the command doesn't return until it completes.

   ```bash
   az deployment group create \
     --name dg-private-retrieval \
     --resource-group rg-private-retrieval \
     --template-uri "$templateUri" \
     --parameters \
       location='westus3' \
       aiServices='private-retrieval' \
       firstProjectName='project-private-retrieval' \
       displayName='private foundry project' \
       projectDescription='Private Foundry plus private Azure AI Search' \
       vnetName='vnet-private-retrieval' \
       existingVnetResourceId="$vnetId" \
       agentSubnetName='agent-subnet' \
       peSubnetName='pe-subnet' \
       agentSubnetPrefix='10.42.0.0/24' \
       peSubnetPrefix='10.42.1.0/24'
   ```

   If you reuse an existing Azure AI Search service to satisfy a subscription policy, append `aiSearchResourceId='<search-resource-id>'` to the deployment parameters.

1. Confirm that the deployment created the following resources:

   - Foundry resource and project
   - Azure AI Search service
   - Azure Storage account
   - Azure Cosmos DB account
   - Azure Container Registry that supports the standard agent environment
   - Private endpoints for the deployed resources
   - Private DNS zones with virtual network links required by the deployment

   ```azurecli
   az deployment group show \
     --resource-group rg-private-retrieval \
     --name dg-private-retrieval \
     --query properties.provisioningState \
     -o tsv
   ```

   The command should return `Succeeded`. The exact number of private endpoints and DNS zones can change as the sample deployment evolves, so use the deployment output as the source of truth.

1. Record the generated resource names.

   The deployment appends a unique suffix to globally unique resources to avoid naming collisions, so the deployed names differ from the input names. Record the actual names now. Throughout this tutorial series, substitute them for the placeholders `<foundry-resource-name>`, `<search-service-name>`, `<storage-account-name>`, and `<cosmos-account-name>`.

   ```azurecli
   # Foundry resource name
   az cognitiveservices account list \
     --resource-group rg-private-retrieval \
     --query "[?kind=='AIServices'].name | [0]" \
     -o tsv

   # Azure AI Search service name
   az search service list \
     --resource-group rg-private-retrieval \
     --query "[0].name" \
     -o tsv

   # Azure Storage account name
   az storage account list \
     --resource-group rg-private-retrieval \
     --query "[0].name" \
     -o tsv

   # Azure Cosmos DB account name
   az cosmosdb list \
     --resource-group rg-private-retrieval \
     --query "[0].name" \
     -o tsv
   ```

## Verify private infrastructure

Inbound private connectivity depends on three controls working together: network exposure settings, private endpoint attachment state, and private DNS resolution paths. In this section, you validate each control so you can trust that requests are constrained to private network routes.

To verify the private infrastructure:

1. Check that public access is disabled for all four services.

    ```bash
    # Foundry resource
    az cognitiveservices account show \
      --name <foundry-resource-name> \
      --resource-group rg-private-retrieval \
      --query 'properties.publicNetworkAccess'

    # Azure AI Search
    az search service show \
      --name <search-service-name> \
      --resource-group rg-private-retrieval \
      --query 'publicNetworkAccess'

    # Azure Storage
    az storage account show \
      --name <storage-account-name> \
      --resource-group rg-private-retrieval \
      --query 'publicNetworkAccess'

    # Azure Cosmos DB
    az cosmosdb show \
      --name <cosmos-account-name> \
      --resource-group rg-private-retrieval \
      --query 'publicNetworkAccess'
    ```

    Each service should return `Disabled`.

1. Check that the private endpoint connections are approved for the four core services.

    ```bash
    # Foundry resource
    az network private-endpoint-connection list \
      --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name> \
      --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
      -o table

    # Azure AI Search
    az network private-endpoint-connection list \
      --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Search/searchServices/<search-service-name> \
      --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
      -o table

    # Azure Storage
    az network private-endpoint-connection list \
      --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name> \
      --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
      -o table

    # Azure Cosmos DB
    az network private-endpoint-connection list \
      --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.DocumentDB/databaseAccounts/<cosmos-account-name> \
      --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
      -o table
    ```

    Each private endpoint connection should show an `Approved` status.

1. Check that the required private DNS zones exist and are linked to the VNet.

    ```bash
    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.cognitiveservices.azure.com \
      --query "[].name" \
      -o table

    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.openai.azure.com \
      --query "[].name" \
      -o table

    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.services.ai.azure.com \
      --query "[].name" \
      -o table

    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.search.windows.net \
      --query "[].name" \
      -o table

    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.blob.core.windows.net \
      --query "[].name" \
      -o table

    az network private-dns link vnet list \
      --resource-group rg-private-retrieval \
      --zone-name privatelink.documents.azure.com \
      --query "[].name" \
      -o table
    ```

    Each command should return a VNet link, which confirms that the private DNS zone is linked to your virtual network.
    
## Validate private connectivity

With networking configured, validate reachability by confirming private DNS resolution and TCP 443 connectivity. You must run these checks from inside the virtual network, such as from an Azure Bastion-connected VM, jumpbox, dev box, or another private access path.

If you don't have an in-VNet client yet, create one in [(Optional) Add a Linux jumpbox and Azure Bastion](#optional-add-a-linux-jumpbox-and-azure-bastion) or [(Optional) Add a Windows VM and Azure Bastion](#optional-add-a-windows-vm-and-azure-bastion), and then return to this section.

To validate the private connectivity:

1. Verify that DNS resolves to private IP addresses.

   ```bash
   getent hosts <search-service-name>.search.windows.net
   getent hosts <foundry-resource-name>.services.ai.azure.com
   getent hosts <foundry-resource-name>.openai.azure.com
   getent hosts <storage-account-name>.blob.core.windows.net
   ```

   These endpoints should resolve to private IP addresses in the `10.x.x.x` range.

1. Verify TCP 443 connectivity to the endpoints used in later parts of the tutorial.

   ```bash
   timeout 10 bash -c '</dev/tcp/<search-service-name>.search.windows.net/443' && \
     echo 'Azure AI Search: OK' || echo 'Azure AI Search: FAILED'

   timeout 10 bash -c '</dev/tcp/<foundry-resource-name>.services.ai.azure.com/443' && \
     echo 'Foundry: OK' || echo 'Foundry: FAILED'

   timeout 10 bash -c '</dev/tcp/<foundry-resource-name>.openai.azure.com/443' && \
     echo 'Foundry OpenAI endpoint: OK' || echo 'Foundry OpenAI endpoint: FAILED'

   timeout 10 bash -c '</dev/tcp/<storage-account-name>.blob.core.windows.net/443' && \
     echo 'Azure Blob Storage: OK' || echo 'Azure Blob Storage: FAILED'
   ```

   Each endpoint should return `OK`.

## (Optional) Add a Linux jumpbox and Azure Bastion

If you need a repeatable in-VNet client for CLI and REST validation over private endpoints, provision a Linux jumpbox behind Azure Bastion.

To configure this setup:

1. Ensure `mcp-subnet` exists. If you didn't create this subnet yet, complete the optional `mcp-subnet` step in [Create the private network](#create-a-private-network).

1. Create the Linux VM network interface and VM.

    ```bash
    az network nic create \
      --resource-group rg-private-retrieval \
      --name vm-linux-nic \
      --vnet-name vnet-private-retrieval \
      --subnet mcp-subnet
    
    az vm create \
      --resource-group rg-private-retrieval \
      --name vm-linux \
      --computer-name vm-linux \
      --nics vm-linux-nic \
      --image Ubuntu2204 \
      --authentication-type password \
      --admin-username azureuser \
      --admin-password <admin-password> \
      --size Standard_B2s \
      --storage-sku Premium_LRS
    ```

1. Create the Azure Bastion subnet and public IP.

    ```bash
    az network vnet subnet create \
      --resource-group rg-private-retrieval \
      --vnet-name vnet-private-retrieval \
      --name AzureBastionSubnet \
      --address-prefixes 10.42.3.0/26

    az network public-ip create \
      --resource-group rg-private-retrieval \
      --name bastion-pip \
      --sku Standard \
      --allocation-method Static
    ```
    
1. Deploy Azure Bastion.

    ```bash
    az network bastion create \
      --resource-group rg-private-retrieval \
      --name bastion-private-retrieval \
      --public-ip-address bastion-pip \
      --vnet-name vnet-private-retrieval
    ```

### Recommended workflow

After you set up the Linux jumpbox and Azure Bastion:

1. Connect to the VM through Azure Bastion by using an interactive shell session.

1. From the Linux VM, run the DNS resolution and TCP 443 connectivity checks from [Validate private connectivity](#validate-private-connectivity) to confirm the inbound path is working.

1. Use `az vm run-command invoke` for repeatable, noninteractive validation when you automate testing workflows.

1. Save the VM connection details if you plan to validate commands from inside the VNet in later parts of the tutorial.
    
## (Optional) Add a Windows VM and Azure Bastion

If you want to test the browser-based Foundry portal or agent playground over the private path, provision a Windows VM behind Azure Bastion.

To configure this setup:

1. Ensure `mcp-subnet` exists. If you didn't create this subnet yet, complete the optional `mcp-subnet` step in [Create the private network](#create-a-private-network).

1. Create the Windows VM network interface and VM.

    ```bash
    az network nic create \
      --resource-group rg-private-retrieval \
      --name vm-windows-nic \
      --vnet-name vnet-private-retrieval \
      --subnet mcp-subnet
    
    az vm create \
      --resource-group rg-private-retrieval \
      --name vm-windows \
      --computer-name vm-windows \
      --nics vm-windows-nic \
      --image MicrosoftWindowsServer:WindowsServer:2022-datacenter-azure-edition:latest \
      --authentication-type password \
      --admin-username azureuser \
      --admin-password <admin-password> \
      --size Standard_B2s \
      --public-ip-address "" \
      --storage-sku Premium_LRS
    ```

1. Create the Azure Bastion subnet and public IP.

    ```bash
    az network vnet subnet create \
      --resource-group rg-private-retrieval \
      --vnet-name vnet-private-retrieval \
      --name AzureBastionSubnet \
      --address-prefixes 10.42.3.0/26

    az network public-ip create \
      --resource-group rg-private-retrieval \
      --name bastion-pip \
      --sku Standard \
      --allocation-method Static
    ```

1. Deploy Azure Bastion.

    ```bash
    az network bastion create \
      --resource-group rg-private-retrieval \
      --name bastion-private-retrieval \
      --public-ip-address bastion-pip \
      --vnet-name vnet-private-retrieval
    ```

### Recommended workflow

After you set up the Windows VM and Azure Bastion:

1. Open Azure Bastion in the [Azure portal](https://portal.azure.com) and connect to the Windows VM by using the username and password you set during VM creation.

1. From within the VM, launch Edge or Chrome and verify you can access the [Foundry portal](https://ai.azure.com?cid=learnDocs) over the private network path. This confirms browser connectivity through the inbound private endpoint.

1. Save the VM connection details if you plan to validate commands from inside the VNet in later parts of the tutorial.

> [!TIP]
> For Azure Bastion username and password sign-ins, use strong passwords to avoid errors when copying and pasting.

## Troubleshooting

When the inbound private path between Foundry and Azure AI Search doesn't behave as expected, start by confirming DNS resolution, private endpoint approval, and TCP 443 reachability from an in-VNet client.

| Check or symptom | Likely issue | What to do next |
| --- | --- | --- |
| `403 Forbidden` | Request isn't reaching Azure AI Search over the intended private path. | Validate the private path from the client to Azure AI Search by checking DNS resolution, TCP 443 connectivity, and private endpoint approval. A restricted search service can return `403 Forbidden` when the request doesn't arrive over an allowed network path. |
| Connection timeout | Client is not on the private path or private endpoints are not reachable. | From the test VM, run the DNS and TCP checks from [Validate private connectivity](#validate-private-connectivity) to confirm you can reach the services over the private path. |

## Learn more

For more information about the topics covered in this part of the tutorial, see the following articles:

- [Add, change, or delete a subnet](/azure/virtual-network/virtual-network-manage-subnet)
- [Create a private endpoint for a secure connection to Azure AI Search](/azure/search/service-create-private-endpoint)
- [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint)
- [Azure Private Endpoint private DNS zone values](/azure/private-link/private-endpoint-dns)
- [Connect to a Linux VM using SSH with Azure Bastion](/azure/bastion/bastion-connect-vm-ssh-linux)
- [Connect to a Windows VM using RDP with Azure Bastion](/azure/bastion/bastion-connect-vm-rdp-windows)

## Next step

> [!div class="nextstepaction"]
> [Set up private outbound connectivity](foundry-iq-tutorial-private-outbound.md)
