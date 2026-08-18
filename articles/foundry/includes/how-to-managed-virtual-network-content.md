---
title: include file
description: include file
author: s-polly
ms.author: scottpolly
ms.reviewer: meerakurup
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/18/2026
ms.custom: include, classic-and-new, dev-focus
ai-usage: ai-assisted
---

This article explains how to set up a managed virtual network for your Foundry resource. A managed virtual network streamlines and automates network isolation by provisioning a Microsoft-managed virtual network that secures the Agents service underlying compute within your Foundry projects.

When you enable it, this managed network boundary secures Agents outbound network traffic, and the isolation mode you choose governs all the traffic. You can create the required private endpoints to dependent Azure services and apply the necessary network rules.

You get a secure default without requiring you to build or maintain your own virtual network. This managed network restricts what your Agents can access, helping prevent data exfiltration while still allowing connectivity to approved Azure resources. 

Managed virtual network now supports Prompt and Hosted Agent services with the new Responses API and in the new Foundry portal. The currently supported regions for managed virtual network with the new Agent service and new Foundry portal are the following: **East US, East US 2, Japan East, France Central, UAE North, Brazil South, Spain Central, Germany West Central, Italy North, South Central US, Australia East, Sweden Central, Canada East, South Africa North, West US, West US 3, South India, and UK South.** 

Before continuing, consider the [limitations](#limitations) of the offering and review the prerequisites. 

## Understand isolation modes

When you enable managed virtual network isolation, you create a managed virtual network for the Foundry account, created in the Microsoft tenant. Any new Agent you build in your projects automatically uses the managed virtual network for outbound traffic. The managed virtual network can use private endpoints for Azure resources that your Agents use, such as Azure Storage, Azure Cosmos DB, and Azure AI Search. 

:::image type="content" source="../how-to/media/managed-virtual-network/diagram-managed-network.png" alt-text="Diagram of managed virtual network configuration." lightbox="../how-to/media/managed-virtual-network/diagram-managed-network.png":::

> [!NOTE]
> The diagrams in this article represent logical connectivity only. Managed private endpoints in a Foundry managed virtual network don't create customer-visible network interfaces (NICs). Unlike standard VNet private endpoints that create a NIC with a private IP in your subnet, managed private endpoints are fully managed by Microsoft and abstracted from the customer's virtual network resources. You don't see these endpoints or associated NICs in your subscription.

Three configuration modes exist for outbound traffic from the managed virtual network:

| Outbound mode | Description | Scenarios |
| --- | --- | --- |
| Allow internet outbound | Allows all outbound traffic to the internet. | Unrestricted outbound access is acceptable; broad connectivity required. |
| Allow only approved outbound | Restricts outbound traffic by using service tags, private endpoints, and optional FQDN rules (ports 80, 443) enforced via Azure Firewall. | Minimize data exfiltration risk; require curated list of destinations. |
| Disabled | Managed virtual network isolation isn't enabled, unless custom virtual network is used. | Need public outbound or plan to supply your own virtual network. |

The following architecture diagram shows a managed network in `allow internet outbound` mode. 

:::image type="content" source="../how-to/media/managed-virtual-network/diagram-allow-internet-outbound-managed-network.png" alt-text="Diagram of managed virtual network configuration in allow internet outbound mode." lightbox="../how-to/media/managed-virtual-network/diagram-allow-internet-outbound-managed-network.png":::

The following architecture diagram shows a managed network in `allow only approved outbound` mode. 

:::image type="content" source="../how-to/media/managed-virtual-network/diagram-allow-only-approved-outbound-managed-network.png" alt-text="Diagram of managed virtual network configuration in allow only approved outbound mode." lightbox="../how-to/media/managed-virtual-network/diagram-allow-only-approved-outbound-managed-network.png":::

After you configure a managed virtual network Foundry to allow internet outbound, you can't reconfigure the resource to disabled. Similarly, after you configure a managed virtual network resource to allow only approved outbound, you can't reconfigure the resource to allow internet outbound.

## Prerequisites

Before following the steps in this article, make sure you have the following prerequisites:

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.
* Azure CLI version 2.86.0 or later. Required to create outbound rules from the managed network.

  > [!NOTE]
  > The `az cognitiveservices account managed-network` command group is in preview and might change.

* The `Microsoft.Network`, `Microsoft.KeyVault`, `Microsoft.CognitiveServices`, `Microsoft.Storage`, `Microsoft.Search`, and `Microsoft.ContainerService` resource providers registered for your Azure subscription. For more information, see [Register resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).
* Permissions to deploy a managed network resource. `Foundry Account Owner` on the Foundry resource scope is needed to create a Foundry account and project. `Owner` or `Role Based Access Administrator` is needed to assign RBAC to the required resources. `Foundry User` on project scope is required to create and build Agents. 

  [!INCLUDE [role-rename-note](./role-rename-note.md)]
* Sufficient quota for all resources in your target Azure region. If you don't pass any parameters, this template creates a Foundry resource, Foundry project, Azure Cosmos DB for NoSQL, Azure AI Search, and Azure Storage account. 

## Limitations

Consider the following limitations before enabling managed network isolation for your Foundry resource. 

1. You can deploy a managed network Foundry resource in three ways:
  1. Bicep template in the folder [18-managed-virtual-network in foundry-samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network)
  1. Terraform template in the folder [18-managed-virtual-network in foundry-samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform/18-managed-virtual-network)
  1. `az rest` and Azure CLI commands `az cognitiveservices`. More on Azure CLI support in this article below.  
1. The Azure portal UI doesn't currently support creating the managed network. Use the Azure CLI, `az rest`, or the Bicep or Terraform templates instead. 
1. After you create your Foundry resource, assign the Foundry resource's managed identity the built-in role of `Azure AI Enterprise Network Connection Approver` (role ID: `b556d68e-0be0-4f35-a333-ad7ee1ce17ea`) to ensure the required private endpoint to the Foundry resource is created and approved. 
1. You can't disable managed virtual network isolation after enabling it. There's no upgrade path from custom virtual network set-up to managed virtual network. A Foundry resource redeployment is required. Deleting your Foundry resource deletes the managed virtual network.
1. Support for managed virtual network is only in the following regions: **East US, East US 2, Japan East, France Central, UAE North, Brazil South, Spain Central, Germany West Central, Italy North, South Central US, Australia East, Sweden Central, Canada East, South Africa North, West US, West US 3, South India, and UK South.** Additional region support to follow soon.
1. If you require private access to on-premises resources for your Foundry resource, use [Application Gateway](/azure/application-gateway/overview) to configure on-premises access. The same set-up with a private endpoint to Application Gateway and setting up backend pools is supported. Both L4 and L7 traffic are now supported with the Application Gateway in GA.
1. If you create FQDN outbound rules when the managed virtual network is in **Allow Only Approved Outbound** mode, a managed Azure Firewall is created which comes with associated Firewall costs. For more on pricing, see [Pricing](#pricing). The FQDN outbound rules only support ports 80 and 443. 
1. You can't bring your own Azure Firewall to the managed virtual network. A managed firewall is automatically created for your Foundry account when you use **Allow Only Approved Outbound** mode.
1. You can't reuse the same managed firewall for multiple Foundry accounts. Each Foundry account creates its own managed firewall when you use **Allow Only Approved Outbound** mode.
1. If you create new projects within your Foundry resource that has managed virtual network enabled, you need to recreate the project capability host as well to ensure the project is using the BYO resources and the managed network. More instructions are in the README for managed network set-up in [foundry-samples repository](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup/README.md).

## Deploy managed virtual network isolation mode

To get started deploying a managed virtual network Foundry resource, follow the steps in the following section.

# [Azure CLI](#tab/azure-cli)

### Create the AI Services account with network injections

Create the account by setting `customSubDomainName`, `allowProjectManagement`, and `networkInjections` **at creation time**. You can't add these properties after creating the account.

> [!IMPORTANT]
> Use `az rest` commands to create the account with network injections. Azure CLI doesn't yet support creating a Foundry resource with network injection.

```azurecli
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}?api-version=2026-05-01" \
  --body '{
    "location": "{region}",
    "kind": "AIServices",
    "sku": { "name": "S0" },
    "identity": { "type": "SystemAssigned" },
    "properties": {
      "allowProjectManagement": true,
      "customSubDomainName": "{account-name}",
      "networkInjections": [
        {
          "scenario": "agent",
          "subnetArmId": "",
          "useMicrosoftManagedNetwork": true
        }
      ],
      "disableLocalAuth": false
    }
  }' \
  --headers "Content-Type=application/json"
```

Wait for `provisioningState` to reach `Succeeded` before proceeding:

```azurecli
az rest --method GET \
  --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}?api-version=2026-05-01" \
  --query "properties.provisioningState" -o tsv
```

### Get the managed identity principal ID

Retrieve the system-assigned managed identity principal ID from the account:

```azurecli
az cognitiveservices account show \
  --resource-group {resource-group} \
  --name {account-name} \
  --query identity.principalId -o tsv
```

### Assign the Network Connection Approver role

Assign the **Azure AI Enterprise Network Connection Approver** role (role ID: `b556d68e-0be0-4f35-a333-ad7ee1ce17ea`) to the Foundry account's managed identity. This role auto-approves managed network private endpoints.

```azurecli
az role assignment create \
  --assignee-object-id {principal-id} \
  --assignee-principal-type ServicePrincipal \
  --role "b556d68e-0be0-4f35-a333-ad7ee1ce17ea" \
  --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group}
```

> [!NOTE]
> If your target resources (Storage, Cosmos DB, AI Search) are in a different resource group, scope the role assignment to that resource group or to the subscription.

### Create the managed network

Create the managed network child resource on the account. This resource establishes the network isolation mode and provisions the network infrastructure.

To create a managed network with **Allow Internet Outbound**:

```azurecli
az cognitiveservices account managed-network create \
  --resource-group {resource-group} \
  --name {account-name} \
  --managed-network allow_internet_outbound
```

To create a managed network with **Allow Only Approved Outbound**:

```azurecli
az cognitiveservices account managed-network create \
  --resource-group {resource-group} \
  --name {account-name} \
  --managed-network allow_only_approved_outbound \
  --firewall-sku Standard
```

# [Bicep / Terraform](#tab/bicep)

You can deploy the solution by using either the Bicep or Terraform templates in the `foundry-samples` repository:

- **Bicep**: [`18-managed-virtual-network`](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network)
- **Terraform**: [`18-managed-virtual-network`](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform/18-managed-virtual-network)

**For Bicep:**

1. Clone or download the `foundry-samples` repository.
1. Open the `managed-network.bicep` template in the `modules-network-secured` folder.
1. Set the isolation mode parameter `IsolationMode` depending on your selected isolation mode: `AllowInternetOutbound` or `AllowOnlyApprovedOutbound`.
1. In the `README.md` file, select the **Deploy to Azure** button. This action opens the template in the Azure portal for a quick deploy.
1. Complete all of your parameters before deploying, such as region, resource group, virtual network name, and others. If you're bringing your own Cosmos DB, Storage, or Search, ensure the resource IDs are included as well.
1. Finally, deploy the template. Template deployment should take roughly 30 minutes.

**For Terraform:**

1. Clone or download the `foundry-samples` repository.
1. Navigate to the `infrastructure/infrastructure-setup-terraform/18-managed-virtual-network` folder.
1. Configure the required variables for your environment (region, resource group, isolation mode, and any existing resource IDs).
1. Run `terraform init`, `terraform plan`, and `terraform apply` to deploy.

After the template finishes, confirm the configuration by following the steps in [Verify managed virtual network deployment](#verify-managed-virtual-network-deployment).

---

For more details on the parameters required for managed virtual network deployment, see [Microsoft.CognitiveServices/accounts/managedNetworks](/azure/templates/microsoft.cognitiveservices/accounts/managednetworks).

## Verify managed virtual network deployment

After the deployment finishes, verify that the managed virtual network is configured correctly.

# [Azure CLI](#tab/azure-cli)

1. Confirm the Foundry resource exists and the managed network is enabled:

   ```azurecli
   az cognitiveservices account managed-network show \
     --resource-group {resource-group} \
     --name {account-name}
   ```

   The response shows the `isolationMode` set to your chosen mode (`AllowInternetOutbound` or `AllowOnlyApprovedOutbound`).

1. List all outbound rules and their status:

   ```azurecli
   az cognitiveservices account managed-network outbound-rule list \
     --resource-group {resource-group} \
     --name {account-name}
   ```

1. Show a specific outbound rule:

   ```azurecli
   az cognitiveservices account managed-network outbound-rule show \
     --resource-group {resource-group} \
     --name {account-name} \
     --rule {rule-name}
   ```

1. Test Agent connectivity by creating and running a basic Agent in your Foundry project. If the Agent completes successfully, the managed network is functioning correctly.

# [Bicep / Terraform](#tab/bicep)

1. Confirm the Foundry resource exists and the managed network is enabled:

   ```azurecli
   az rest --method GET \
     --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/managedNetworks/default?api-version=2026-05-01" \
     --query "properties.managedNetwork"
   ```

   The response shows the `isolationMode` set to your chosen mode (`AllowInternetOutbound` or `AllowOnlyApprovedOutbound`).

1. List the outbound rules to confirm they were created:

   ```azurecli
   az rest --method GET \
     --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/managedNetworks/default/outboundRules?api-version=2026-05-01" \
     --query "value[].{name:name, type:properties.type, status:properties.status}"
   ```

1. Test Agent connectivity by creating and running a basic Agent in your Foundry project. If the Agent completes successfully, the managed network is functioning correctly.

---

## Manage outbound rules

After deployment, you can add, update, list, and remove outbound rules to control which destinations your managed network can reach. The following outbound rule types are supported:

| Type | Description | Example destination |
| --- | --- | --- |
| `fqdn` | Allows outbound traffic to a fully qualified domain name. | `"*.openai.azure.com"` |
| `privateendpoint` | Allows outbound traffic through a private endpoint rule. | Service resource ID with a subresource target |
| `servicetag` | Allows outbound traffic to an Azure service tag, protocol, and port range. | `'{"serviceTag":"Storage","protocol":"TCP","portRanges":"443"}'` |

# [Azure CLI](#tab/azure-cli)

### Create or update an FQDN outbound rule

Use an FQDN rule to allow traffic to a domain name or wildcard domain.

```azurecli
az cognitiveservices account managed-network outbound-rule set \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name} \
  --type fqdn \
  --destination "*.openai.azure.com"
```

### Create or update a service tag outbound rule

Use a service tag rule to allow traffic to an Azure service tag over a specific protocol and port range.

```azurecli
az cognitiveservices account managed-network outbound-rule set \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name} \
  --type servicetag \
  --category UserDefined \
  --destination '{"serviceTag":"Storage","protocol":"TCP","portRanges":"443"}'
```

### Create or update a private endpoint outbound rule

Use a private endpoint rule to allow traffic through a private endpoint to an Azure resource.

```azurecli
az cognitiveservices account managed-network outbound-rule set \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name} \
  --type privateendpoint \
  --destination "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Storage/storageAccounts/{storage-name}" \
  --subresource-target blob
```

Common subresource targets include `blob` for Azure Storage, `searchService` for Azure AI Search, `Sql` for Azure Cosmos DB, and `vault` for Azure Key Vault.

### List outbound rules

```azurecli
az cognitiveservices account managed-network outbound-rule list \
  --resource-group {resource-group} \
  --name {account-name}
```

### Show an outbound rule

```azurecli
az cognitiveservices account managed-network outbound-rule show \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name}
```

### Bulk create or update outbound rules

Use `bulk-set` to create or update multiple outbound rules from a YAML or JSON file.

```azurecli
az cognitiveservices account managed-network outbound-rule bulk-set \
  --resource-group {resource-group} \
  --name {account-name} \
  --file rules.yaml
```

### Remove an outbound rule

```azurecli
az cognitiveservices account managed-network outbound-rule remove \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name}
```

# [Bicep / Terraform](#tab/bicep)

To update outbound rules by using the ARM REST API, use the `az rest` command. The following example creates a private endpoint outbound rule to an Azure Cosmos DB resource:

```azurecli
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/managedNetworks/default/outboundRules/{rule-name}?api-version=2026-05-01" \
  --body '{
    "properties": {
      "type": "PrivateEndpoint",
      "destination": {
        "serviceResourceId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmosdb-account-name}",
        "subresourceTarget": "Sql",
        "sparkEnabled": false
      }
    }
  }'
```

Replace the placeholders with values for your environment. For other resource types, change the `serviceResourceId` and `subresourceTarget` values accordingly. Common subresource targets include `blob` for Azure Storage, `searchService` for Azure AI Search, and `vault` for Azure Key Vault.

For more information, see the [outbound rules CLI](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/18-managed-virtual-network) file in the foundry-samples repository.

---

For more details on the parameters required for managed virtual network outbound rules, see [Microsoft.CognitiveServices/accounts/managedNetworks/outboundRules](/azure/templates/microsoft.cognitiveservices/accounts/managednetworks/outboundrules).

## Select Azure Firewall version

For the managed virtual network, an Azure Firewall is provisioned automatically when you add an outbound FQDN rule in **Allow only approved outbound** mode.

The default SKU is Standard for the Firewall. You can select the Basic SKU instead for reduced cost if advanced features aren't required. For more on pricing, see [Pricing](#pricing). Once you select a firewall SKU at deployment, you can't change it after deployment. Because this is a managed firewall, the firewall isn't in your tenant or in your control. The only setting you can control is the firewall SKU. 

## Private endpoints

When you enable a managed virtual network, you can create managed private endpoints so agents can securely reach required Azure resources without using the public internet. These private endpoints provide an isolated, private IP–based connection from the managed network to services such as Storage, AI Search, and other dependencies used in your Foundry projects. Unlike customer-managed virtual networks, managed private endpoints in Foundry don't expose a network interface or subnet configuration to the customer. Microsoft fully manages the private IP–based connectivity and doesn't represent it as a NIC in the customer's subscription.

The following resources support private endpoints from the managed network. You must use the CLI to create private endpoints. 

- Microsoft Foundry (AI Services)
- Azure Application Gateway (connects to your on-premises resources by using L4 or L7 traffic) 
- Azure API Management (supports only the Classic tier without VNet injection and the Standard V2 tier with virtual network integration) 
- Azure AI Search
- Azure Container Registry
- Azure Cosmos DB 
- Azure Data Factory
- Azure Database for MariaDB
- Azure Database for MySQL
- Azure Database for PostgreSQL Single Server
- Azure Database for PostgreSQL Flexible Server
- Azure Databricks
- Azure Event Hubs
- Azure Key Vault
- Azure Machine Learning
- Azure Cache for Redis
- Azure SQL Server
- Azure Storage 
- Azure Application Insights (via Azure Monitor Private Link Scope) 

When you create a managed private endpoint from the Foundry managed virtual network to a customer‑owned target resource, the **Foundry resource's managed identity** must have the correct permissions on that target resource to create and approve private endpoint connections. This requirement ensures that Foundry is explicitly authorized to establish a secure, private link to the resource.

To simplify this requirement, assign the `Azure AI Enterprise Network Connection Approver` role (role ID: `b556d68e-0be0-4f35-a333-ad7ee1ce17ea`) to the Foundry account's managed identity. This role includes the necessary permissions for most commonly used Azure services and typically provides sufficient access for Foundry to create and approve private endpoints on your behalf. Once you approve the connection, Foundry fully manages the private endpoint and requires no additional customer configuration. 

## Required outbound rules 

In **Allow Only Approved Outbound** mode of the managed virtual network, the system creates a few required outbound rules for features like the Agent service. These rules include the following destinations: 

* Private endpoint to your Cosmos DB resource
* Private endpoint to your Storage account
* Private endpoint to your AI Search resource
* Service tag to AzureActiveDirectory

## Outbound rules per scenario 

If you deploy Foundry with managed virtual network in **Allow Only Approved Outbound** mode, you might need to add the following outbound FQDN rules to ensure egress traffic is allowed. The following list shows trusted fully qualified domain names (FQDNs) and service tags to create outbound rules for, depending on the scenario or feature in Foundry. 

| Scenario | FQDNs, service tags| Description |
|---------|--------------------------|-------|
| Agents | `*.identity.azure.net`, `login.microsoftonline.com`, `*.login.microsoftonline.com`, `*.login.microsoft.com`, `mcr.microsoft.com` or AAD service tag | Required for the Azure Container App delegation for Agent service. Includes Microsoft Container Registry for container image pulls. |
| Evaluations & Traces with an Application Insights resource | `settings.sdk.monitor.azure.com`, `*.livediagnostics.monitor.azure.com`, `*.in.applicationinsights.azure.com`, AzureMachineLearning service tag | Used for sending results to the linked Application Insights resource and Evaluators Catalog. |
| Finetuning | `raw.githubusercontent.com` | Used for finetuning, when a user picks a curated sample dataset in the Foundry portal. |

## Pricing

The Foundry managed virtual network feature is free. However, you're charged for the following resources that the managed virtual network uses:

* Azure Private Link - The solution relies on Azure Private Link for private endpoints that secure communications between the managed virtual network and Azure resources. For more information on pricing, see [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link).

* FQDN outbound rules - You implement FQDN outbound rules by using Azure Firewall. If you use outbound FQDN rules, you add charges for Azure Firewall to your billing. A standard version of Azure Firewall is used by default. You can select the Basic version. The firewall isn't created until you add an outbound FQDN rule. 

For more on Azure pricing, see [Private Link Pricing](https://azure.microsoft.com/pricing/details/private-link) and [Azure Firewall Pricing](https://azure.microsoft.com/pricing/details/azure-firewall/).

## Compare managed and custom (BYO) network

Select the right outbound network isolation mode for you depending on your networking needs and limitations in your enterprise. 

| Aspect | Managed network | Custom (BYO) network |
| --- | --- | --- |
| Benefits | Microsoft handles subnet range, IP selection, delegation. | Full control: bring custom firewall, set user-defined routes, network peering, delegate subnet. |
| Limitations | Can't bring your own firewall for allow only approved outbound. Requires Application Gateway for secure on-premises (L7 and L4 traffic support by Application Gateway). No logging of outbound traffic support yet. | More complex setup such as subnet delegation to Azure Container Apps. Requires correct CapHost creation. Requires private Class A, B, and C, not public or CGNAT IP address ranges allowed. Requires minimum /27 subnet for Agent delegation. |

For more on virtual network injection set-up for Agents and the limitations , see [Configure a custom virtual network for Agents](../agents/how-to/virtual-networks.md).

## Clean up resources

To clean up your managed virtual network Foundry resource, delete the Foundry resource. This action deletes the managed virtual network as well.

## Troubleshooting

1. Failure creating CapHost
   - Delete the faulty CapHost resource and redeploy the template.
1. FQDN rule not enforced
   - Confirm the firewall SKU is provisioned and verify ports are limited to 80 or 443.
1. Private endpoint conflicts
   - Remove any service endpoint configuration and use private endpoint only.

## Related content

- [Configure a custom virtual network for Agents](../agents/how-to/virtual-networks.md)
- [Configure network isolation for Microsoft Foundry](../how-to/configure-private-link.md)
