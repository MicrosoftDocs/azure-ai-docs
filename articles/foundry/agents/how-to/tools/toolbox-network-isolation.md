---
title: "Network isolation for a toolbox in Microsoft Foundry"
description: "Understand how toolbox tool traffic flows when your Microsoft Foundry project uses network isolation, and set up a network-secured toolbox for Basic and Standard agent projects."
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.date: 08/03/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Network isolation for a toolbox in Microsoft Foundry

A toolbox is a logical container for tools and doesn't deploy its own networking resources. The networking configuration of the Microsoft Foundry project that hosts the toolbox governs all network access.

When your project runs inside a virtual network (VNet) with [network isolation (private link)](../../../how-to/configure-private-link.md), agents reach the toolbox MCP endpoint through the project's private endpoint. Each downstream tool's traffic flows differently depending on the tool type.


Tool connectivity depends on where the downstream service is hosted. Some tools communicate with Azure resources that support private endpoints, some invoke services that run through the project's delegated subnet, and others depend on Microsoft-managed services that currently require public or backbone connectivity. Review how each tool behaves before you add it to a toolbox in a network-isolated environment.

## Network isolation support for tools in a toolbox

Network-isolated projects work best with tools that support private endpoints or VNet subnet integration. Review the support table before building a toolbox intended for regulated or highly secured environments.

The following table shows how each tool's traffic flows when your project uses network isolation. Some tools route through your VNet subnet or a private endpoint, some use public endpoints or the Microsoft backbone network, and some aren't supported in a network-isolated project.

| Tool | VNet support (traffic flow) |
| ---- | --------------------------- |
| [Model Context Protocol (MCP)](model-context-protocol.md) | ✅ Supported (through your VNet subnet). |
| [Azure AI Search](ai-search.md) | ✅ Supported (through private endpoint). |
| [File search](file-search.md) | ✅ Supported (through private endpoint). |
| [OpenAPI](openapi.md) | ✅ Supported (through your VNet subnet). |
| [Agent-to-agent (A2A)](agent-to-agent.md) | ✅ Supported (through your VNet subnet). |
| [Web search](web-search.md) | ✅ Supported. Relies on Microsoft-managed public endpoints. |
| [Code interpreter](code-interpreter.md) | ✅ Supported (Microsoft backbone network). |
| [Skills](skills.md) | ✅ Supported (network behavior depends on the tools used by the skill). |
| [Fabric IQ](fabric-iq.md) | ⚠️ Partial. Fabric IQ connectivity is provided through MCP integration. Support depends on the specific Fabric item and networking configuration. See [Restrict network access](fabric-iq.md#restrict-network-access). |
| [Work IQ](work-iq.md) | ❌ Not supported in network-isolated projects. |
| [Browser automation](browser-automation.md) | ❌ Not supported. |
| [Tool search](tool-search.md) | N/A |

Tools that use your VNet subnet communicate through the delegated subnet associated with the Foundry project. These tools can access resources reachable from that subnet, subject to your network security rules.

For the authoritative, tool-by-tool support matrix, see [Agent tools with network isolation](../../../how-to/configure-private-link.md#agent-tools-with-network-isolation). For the full list of tools and their SDK and tooling support, see [Feature support](toolbox.md#feature-support).

## Set up a network-secured project

Set up network isolation at the project level, then create your toolbox in that project. You can find the infrastructure-as-code templates in the [Foundry samples infrastructure setup repository](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) (Bicep, with a Terraform mirror). The template you choose depends on your [agent project type](../../concepts/networking-options.md#bring-your-own-virtual-network-requirements).

### Configure a Basic agent project

A Basic agent project uses platform-managed data resources. To place it inside your own virtual network with private endpoints and no public egress, deploy the [`11-private-network-basic-vnet`](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/11-private-network-basic-vnet) template. To restrict who can call the endpoint while keeping public egress, use [`10-private-network-basic`](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/10-private-network-basic).

### Configure a Standard agent project

A Standard agent project brings your own data resources (Azure Cosmos DB, Azure Storage, and Azure AI Search). For full isolation with no public egress and bring-your-own data resources, deploy the [`15-private-network-standard-agent-setup`](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup) template.

For the full template catalog and what each one provisions, see the [infrastructure setup README](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep#readme). For a step-by-step walkthrough of customizing the scaffolded infrastructure, see [Set up private networking for Foundry Agent Service](../virtual-networks.md).

## Related content

- [Networking options for Foundry Agent Service](../../concepts/networking-options.md)
- [Set up private networking for Foundry Agent Service](../virtual-networks.md)
- [Configure network isolation for Microsoft Foundry](../../../how-to/configure-private-link.md)
- [Create and manage a toolbox](toolbox.md)
