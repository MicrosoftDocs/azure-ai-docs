---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Data storage

Foundry provides flexible and secure data storage options to support a wide range of AI workloads.

### Managed storage for file upload

In the default setup, Foundry uses Microsoft-managed storage accounts that are logically separated and support direct file uploads for select use cases, such as OpenAI models and Agents, without requiring a customer-provided storage account.

### Bring your own storage

You can optionally connect your own Azure Storage accounts. Foundry tools such as evaluations and batch processing can read inputs from and write outputs to these accounts. For details on supported scenarios, see [Bring-your-own resources with the Agent service](../agents/how-to/use-your-own-resources.md).

### Agent state storage

- With the [basic agent setup](../agents/how-to/use-your-own-resources.md), the Agent service stores threads, messages, and files in Microsoft-managed multitenant storage, with logical separation.
- With the [standard agent setup](../agents/how-to/use-your-own-resources.md), you bring your own Azure resources for all customer data—including files, conversations, and vector stores. In this configuration, data is isolated by project within your storage accounts.

### Customer-managed key encryption

By default, Azure services encrypt data at rest and in transit using Microsoft-managed keys with FIPS 140-2 compliant 256-bit AES encryption. No code changes are required.

To use your own keys instead, confirm these prerequisites before enabling customer-managed keys for Foundry:

- Key Vault is deployed in the same Azure region as your Foundry resource.
- Soft delete and purge protection are enabled on Key Vault.
- Managed identities have required key permissions, such as the **Key Vault Crypto User** role when using Azure RBAC.

### Bring your own Key Vault

By default, Foundry stores all API key-based connection secrets in a managed Azure Key Vault. If you prefer to manage secrets yourself, connect your key vault to the Foundry resource. One Azure Key Vault connection manages all project and resource level connection secrets. For more information, see [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).

To learn more about data encryption, see [customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md).

### Data residency and compliance

Foundry stores all data at rest in the designated Azure geography. Inferencing data (prompts and completions) is processed according to the deployment type: global deployments might route to any Azure region, data zone deployments stay within the US or EU zone, and standard or regional deployments process in the deployment region. For details, see [Deployment types](../foundry-models/concepts/deployment-types.md). Foundry doesn't support automatic cross-region failover. If your organization requires multi-region availability, deploy separate Foundry resources in each target region and manage data synchronization and routing at the application layer. For compliance certification details, see [Azure compliance documentation](/azure/compliance/).

## Validate architecture decisions

Before rollout, validate the following for your target environment:

- Verify that required models and features are available in your deployment regions. For details, see [Feature availability across cloud regions](../reference/region-support.md).
- Check that role assignments are scoped correctly at both the Foundry resource and project levels. For details, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).
- Validate network isolation requirements and private access paths. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).
- Confirm encryption and secret-management requirements, including customer-managed keys and Azure Key Vault integration. For details, see [Customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md) and [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).
- Review quotas and limits for your target resources, including model deployment limits and rate limits. For details, see [Azure OpenAI quotas and limits](../openai/quotas-limits.md) and [Agent Service limits, quotas, and regions](../agents/concepts/limits-quotas-regions.md).

## Related content

* [Foundry rollout across my organization](../concepts/planning.md)
* [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
* [Customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md)
* [How to configure a private link for Foundry](../how-to/configure-private-link.md)
* [Bring-your-own resources with the Agent service](../agents/how-to/use-your-own-resources.md)
* [Azure Monitor overview](/azure/azure-monitor/overview)
* [Azure OpenAI quotas and limits](../openai/quotas-limits.md)
* [Deployment types for Foundry Models](../foundry-models/concepts/deployment-types.md)
* [Guardrails and controls overview](../guardrails/guardrails-overview.md)
* [Feature availability across cloud regions](../reference/region-support.md)
