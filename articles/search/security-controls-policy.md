---
title: Azure Policy Regulatory Compliance controls for Azure AI Search
description: Lists Azure Policy Regulatory Compliance controls available for Azure AI Search. These built-in policy definitions provide common approaches to managing the compliance of your Azure resources.
ms.date: 02/06/2024
ms.update-cycle: 365-days
ms.topic: concept-article
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - subject-policy-compliancecontrols
  - ignite-2023
---
# Azure Policy Regulatory Compliance controls for Azure AI Search

If you are using [Azure Policy](/azure/governance/policy/overview) to enforce the recommendations in
[Microsoft cloud security benchmark](/azure/security/benchmarks/introduction), then you probably already know
that you can create policies for identifying and fixing non-compliant services. These policies might
be custom, or they might be based on built-in definitions that provide compliance criteria and
appropriate solutions for well-understood best practices.

For Azure AI Search, there is currently one built-definition, listed below, that you can use
in a policy assignment. The built-in is for logging and monitoring. By using this built-in
definition in a [policy that you create](/azure/governance/policy/assign-policy-portal), the system
will scan for search services that do not have [resource logging](monitor-azure-cognitive-search.md), and
then enable it accordingly.

[Regulatory Compliance in Azure Policy](/azure/governance/policy/concepts/regulatory-compliance)
provides Microsoft-created and managed initiative definitions, known as _built-ins_, for the
**compliance domains** and **security controls** related to different compliance standards. This
page lists the **compliance domains** and **security controls** for Azure AI Search. You can
assign the built-ins for a **security control** individually to help make your Azure resources
compliant with the specific standard.

[!INCLUDE [azure-policy-compliancecontrols-introwarning](~/azure-docs-pr-policy-includes/includes/policy/standards/intro-warning.md)]

[!INCLUDE [azure-policy-compliancecontrols-search](~/azure-policy-autogen-docs/includes/policy/standards/byrp/microsoft.search.md)]

## Next steps

- Learn more about [Azure Policy Regulatory Compliance](/azure/governance/policy/concepts/regulatory-compliance).
- See the built-ins on the [Azure Policy GitHub repo](https://github.com/Azure/azure-policy).
