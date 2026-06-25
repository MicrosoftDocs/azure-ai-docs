---
title: "Set up private networking for Foundry Agent Service"
description: "Set up private networking for Foundry Agent Service using Bicep or Terraform. Deploy a virtual network with private endpoints, DNS zones, and deny-by-default network rules."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.custom:
  - azure-ai-agents, references_regions, doc-kit-assisted
  - classic-and-new
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-network-method
---

# Set up private networking for Foundry Agent Service

For background on the network architecture, subnet sizing, and IP allocation model behind these steps, see [Deep dive into Foundry Agent Service networking](../concepts/agents-networking-deep-dive.md).

This article describes two approaches. Use the **Portal or templates** path to provision a network-secured Foundry environment with Bicep or Terraform. Use the **Azure Developer CLI** path to place the dependencies of an `azd` hosted agent project behind private endpoints. Choose a method with the selector.

:::zone pivot="templates"

[!INCLUDE [virtual-networks content](../includes/how-to-virtual-networks-content.md)]

:::zone-end

:::zone pivot="azd"

Many enterprise environments require that Foundry, the container registry, and dependent services such as Application Insights and Storage be reachable only from a private network. This section explains how to provision and deploy `azd` hosted agents whose dependencies sit behind private endpoints in a virtual network (VNet).

You achieve VNet integration by customizing the scaffolded `infra/` Bicep templates and by running `azd` from inside (or with access to) the VNet.

## Prerequisites

* An initialized hosted agent project. To create one, see [Initialize a hosted agent project with the Azure Developer CLI](init-agent-project.md).
* The [Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md) installed.
* A virtual network (new or existing) and permission to create private endpoints and private DNS zones.
* Familiarity with the scaffolded Bicep. See [Hosted agent infrastructure with the Azure Developer CLI](../concepts/cli-infrastructure.md).

## What VNet protection means for an azd deployment

A hosted agent project provisions several Azure resources. You can disable public network access on each one and place a private endpoint in your VNet.

| Resource | Can be VNet-protected? | What private mode means |
| -------- | ---------------------- | ----------------------- |
| AI Services account | Yes | The Foundry account is reachable only through a private endpoint, for both data-plane and ARM calls. |
| Foundry project | Yes, with the account | Inherits the account's network posture. |
| Azure Container Registry | Yes | `publicNetworkAccess: Disabled`. Build, push, and pull happen over the private endpoint. |
| Application Insights | Yes, through an Azure Monitor Private Link Scope | Telemetry ingestion routes through the private link scope. |
| Azure Storage | Yes | Blob, Files, and Queue services sit behind private endpoints. |
| Agent endpoint itself | No, in this preview | The deployed agent endpoint URL stays publicly addressable. Isolation is done with Foundry isolation keys. See [Pass isolation keys](pass-isolation-keys.md). |

If you need the agent endpoint itself to be private, that's a platform-side feature outside the scope of this extension today.

## What the extension does and doesn't do

| Capability | Status |
| ---------- | ------ |
| CLI flag to enable VNet integration | Not supported. No `--vnet` or `--private-endpoint` flag ships by default. |
| Reuse of an existing private ACR | Supported through `AZURE_CONTAINER_REGISTRY_RESOURCE_ID` and `AZURE_CONTAINER_REGISTRY_ENDPOINT`. See [Deploy a hosted agent with a private Azure Container Registry](deploy-hosted-agent-private-azure-container-registry.md). |
| Reuse of an existing Foundry account | Supported through `AZURE_AI_ACCOUNT_NAME` and `USE_EXISTING_AI_PROJECT=true`. |
| Custom Bicep modules in `infra/` | Fully supported. The `infra/` directory is standard `azd` Bicep that you own. |
| `azd ai agent doctor` from inside the VNet | Works. Remote checks require DNS resolution of the Foundry data-plane endpoint. Use `--local-only` to skip them. |
| Self-hosted GitHub runners or Azure DevOps agents in the VNet | Recommended pattern. CI provisions and deploys from inside the network. |

## Decide your topology

Most VNet-protected deployments fall into one of these shapes. Pick one before you edit Bicep:

- **Greenfield, everything inside a new VNet.** Run `azd ai agent init`, then add private endpoint modules to the scaffolded `infra/`. You provision both the VNet and the resources from one Bicep run.
- **Brownfield, attach to an existing VNet.** Same as the greenfield approach, but you reference the existing VNet through parameters instead of creating one. This is useful when a different team owns networking.
- **Reuse all existing resources.** A platform team preprovisioned the Foundry account, ACR, and Application Insights on private endpoints. You bring just the agent definition and point the environment variables at the existing resources. `main.bicep` creates only what's missing.

Topologies 2 and 3 are the most common in regulated enterprises. Topology 1 fits self-contained pilots.

## Customize the scaffolded Bicep

The `infra/` directory generated by `azd ai agent init` is standard `azd` Bicep. You own it, and changes persist across deployments. The default templates create public resources, so you replace or augment them to add private endpoints.

### Add VNet and subnet parameters

Add parameters to `infra/main.bicep` and bind them in `infra/main.parameters.json`:

```bicep
// infra/main.bicep (excerpt)

@description('Resource ID of the existing virtual network. If empty, a new VNet is created.')
param vnetResourceId string = ''

@description('Name of the subnet hosting private endpoints.')
param privateEndpointSubnetName string = 'snet-pe'

@description('Disable public network access on data-plane resources.')
param disablePublicNetworkAccess bool = true
```

```json
// infra/main.parameters.json (excerpt)
{
  "vnetResourceId":              { "value": "${AZURE_VNET_RESOURCE_ID=}" },
  "privateEndpointSubnetName":   { "value": "${AZURE_PE_SUBNET_NAME=snet-pe}" },
  "disablePublicNetworkAccess":  { "value": "${DISABLE_PUBLIC_NETWORK=true}" }
}
```

Set the environment variables before `azd provision`:

```bash
azd env set AZURE_VNET_RESOURCE_ID \
  /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<vnet>
azd env set AZURE_PE_SUBNET_NAME snet-pe
azd env set DISABLE_PUBLIC_NETWORK true
```

### Lock down each resource

For every resource the templates create, set `publicNetworkAccess: 'Disabled'` and add a private endpoint module. The following pattern is illustrative. Adapt the resource types and DNS zones to your environment.

```bicep
// infra/core/ai/account.bicep (excerpt)
resource aiAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  // ...existing properties...
  properties: {
    // ...existing properties...
    publicNetworkAccess: disablePublicNetworkAccess ? 'Disabled' : 'Enabled'
    networkAcls: {
      defaultAction: disablePublicNetworkAccess ? 'Deny' : 'Allow'
    }
  }
}
```

Add a private endpoint module that wires the account into the VNet:

```bicep
module aiAccountPrivateEndpoint '../network/private-endpoint.bicep' = if (disablePublicNetworkAccess) {
  name: 'pe-ai-account'
  params: {
    name: 'pe-${aiAccount.name}'
    location: location
    subnetId: '${vnetResourceId}/subnets/${privateEndpointSubnetName}'
    privateLinkServiceId: aiAccount.id
    groupId: 'account'
    privateDnsZoneId: privateDnsZones.cognitiveServices
  }
}
```

Repeat this pattern for the resources you want to make private:

* AI Services account: group ID `account`. DNS zones include `privatelink.cognitiveservices.azure.com`, `privatelink.openai.azure.com`, and `privatelink.services.ai.azure.com`, depending on the data plane.
* Container Registry: group ID `registry`. DNS zone `privatelink.azurecr.io`. Adds a data endpoint per region.
* Application Insights: through an Azure Monitor Private Link Scope. DNS zones include `privatelink.monitor.azure.com`, `privatelink.ods.opinsights.azure.com`, `privatelink.oms.opinsights.azure.com`, and `privatelink.agentsvc.azure-automation.net`.
* Storage account: group IDs `blob`, `file`, `queue`, and `table` as needed. DNS zones per service, for example `privatelink.blob.core.windows.net`.

The [azd-ai-starter-basic](https://github.com/Azure-Samples/azd-ai-starter-basic) repository that the agent extension scaffolds from is a useful reference for what's created by default. Augment those modules rather than replace them.

### Provision the resources

```bash
azd provision
```

After provisioning, every dependency on your list is reachable only through its private endpoint. Public DNS resolution still returns the public hostname, but the private DNS zones override it inside the VNet.

## Run azd up from inside the VNet

After you disable public network access, you can't run `azd up` or `azd deploy` from a public-internet workstation. The ARM control plane is reachable, but data-plane calls to Foundry and ACR push fail with `403` or connection-refused errors. Use one of the following patterns.

### Self-hosted GitHub Actions runner

Provision a runner VM, or an AKS-hosted runner, in a subnet of the same VNet. Point your workflow at that runner with `runs-on: [self-hosted, agent-vnet]`. Every `azd ai` step then resolves the private DNS names correctly and pushes through the private endpoint.

```yaml
jobs:
  deploy:
    runs-on: [self-hosted, agent-vnet]
    steps:
      - uses: actions/checkout@v4
      - uses: Azure/setup-azd@v2
      - run: azd ext install microsoft.foundry
      - run: azd auth login --client-id ${{ secrets.AZURE_CLIENT_ID }} \
          --federated-credential-provider github \
          --tenant-id ${{ secrets.AZURE_TENANT_ID }}
      - run: azd up --no-prompt
```

### Azure DevOps self-hosted agent

Use the same pattern for Azure DevOps. Install the agent in a VNet subnet and target it with the `pool: name: agent-vnet` directive. The `azd` CLI and the Foundry extension run unchanged.

### Bastion or jump host for one-off runs

For ad hoc runs, such as manual incident response or an out-of-cycle deploy, connect through Azure Bastion to a jump host inside the VNet, install `azd` and the extensions there, and run `azd` from that host. Keep the jump host minimal. The long-term answer is CI.

## Develop locally against a private Foundry endpoint

Local development (`azd ai agent run` and `azd ai agent invoke`) talks to your local agent process over loopback and to the Foundry data plane for tools, models, and sessions during `invoke`. When the Foundry endpoint is VNet-only, you need network reachability from your development machine. Options include:

* A point-to-site or always-on VPN that drops you into the VNet DNS scope.
* Azure Bastion to a development VM inside the VNet. Run `azd ai agent run` on that VM and forward port 8088, and 8087 for the inspector, through the Bastion tunnel.
* A workstation in the corporate network with an ExpressRoute or hub-VNet path to the spoke that hosts the private endpoints.

The `FOUNDRY_PROJECT_ENDPOINT` resolution doesn't change. The value still comes from the active `azd` environment or the global config. What matters is that DNS resolves the endpoint to the private IP rather than the public one.

## Combine with a private ACR

If both the Foundry endpoint and the ACR are on private endpoints in the same VNet, do the following:

1. Run `azd up` from inside the VNet.
1. Set `AZURE_CONTAINER_REGISTRY_ENDPOINT` and `AZURE_CONTAINER_REGISTRY_RESOURCE_ID` to point at the existing private ACR, so the Bicep skips creating a new public one.
1. Make sure the agent identity has the **AcrPull** role on the registry. `azd deploy` handles this automatically after it creates the agent identity.

For registry-specific details, see [Deploy a hosted agent with a private Azure Container Registry](deploy-hosted-agent-private-azure-container-registry.md).

## Diagnose networking issues

* `azd ai agent doctor` runs network reachability checks against the Foundry data plane. From inside the VNet, the checks pass. From outside, they fail clearly. Use `--local-only` to skip remote checks when you debug non-network issues.
* `azd ai agent invoke --output raw "ping"` dumps the full HTTP response. A connection-refused or no-such-host error here is a DNS or routing problem, not an authentication problem.
* For ACR push failures, the CLI emits a paste-ready `az role assignment create` command when the cause is a missing role rather than a network issue.

## Known limitations

* No first-class CLI flag. All VNet wiring is manual Bicep customization plus operational discipline for runner placement, DNS, and RBAC.
* The agent endpoint stays public in this preview. Tenant isolation on a public endpoint is done with [isolation keys](pass-isolation-keys.md), not network privacy.
* Region constraints apply. Hosted agents are available in a fixed set of regions. The VNet, ACR, and Foundry account should all live in, or peer to, one of those regions. Run `azd ai agent doctor` to validate.
* DNS is the most common failure mode. Confirm private DNS resolution end to end, for example with `nslookup <endpoint>` from the runner or development VM, before you assume the issue is RBAC.

## Related content

* [Deploy a hosted agent with a private Azure Container Registry](deploy-hosted-agent-private-azure-container-registry.md)
* [Pass isolation keys to a hosted agent](pass-isolation-keys.md)
* [Hosted agent infrastructure with the Azure Developer CLI](../concepts/cli-infrastructure.md)
* [Diagnose a project with agent doctor](agent-doctor.md)

:::zone-end
