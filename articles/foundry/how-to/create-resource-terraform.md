---
title: "Use Terraform to create Microsoft Foundry"
description: "In this article, you create a Microsoft Foundry resource, a Microsoft Foundry project, using Terraform infrastructure as code templates."
ms.topic: how-to
ms.date: 03/31/2026
ms.service: azure-ai-foundry
ms.reviewer: deeikele 
ms.author: sgilley
author: sdgilley
ms.custom: 
  - classic-and-new
  - devx-track-terraform
  - update-code2
  - dev-focus
  - doc-kit-assisted
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a Terraform user, I want to see how to configure Microsoft Foundry using Terraform, so I can automate my setup.
---

# Use Terraform to manage Microsoft Foundry resources

Use Terraform to automate the creation of [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resources, projects, deployments, and connections.

If you already configured a Foundry resource in the Azure portal, you can [export that configuration as Terraform code](#export-an-existing-resource-to-terraform) instead of authoring a configuration from scratch.

You can use either the Terraform [AzAPI Provider](/azure/developer/terraform/overview-azapi-provider) or [AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) to manage Foundry resources. The AzAPI provider lets you access all Foundry control plane configurations including preview features. The AzureRM variant is limited to core management capabilities.

Terraform state files can include sensitive values. Use a secure backend and access controls for team scenarios.

> [!TIP]
> For production-ready Terraform configurations that cover common Foundry deployment scenarios, see the [infrastructure-setup-terraform](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform) folder in the Foundry samples repository. Clone the repository and customize the configurations instead of starting from scratch.


[!INCLUDE [About Terraform](~/azure-dev-docs-pr/articles/terraform/includes/abstract.md)]

## Provider capabilities

The following table shows which actions each provider supports:

|Action|AzAPI Provider|AzureRM Provider|
|---|---|---|
|Create a resource group|✅|✅|
|Create a Foundry resource|✅|✅|
|Configure deployments|✅|✅|
|Configure projects|✅|✅|
|Configure a connection to knowledge and tools|✅|-|
|Configure a capability host (for advanced tool configurations like [Agent standard setup](../agents/concepts/capability-hosts.md))|✅|-|

[!INCLUDE [create-resource-terraform 1](../includes/how-to-create-resource-terraform-1.md)]

## Verify your deployment

Run the following commands to verify deployed resources:

```terraform
terraform state list
terraform output
```

## Export an existing resource to Terraform

If you already configured a Foundry resource in the Azure portal, you can export that configuration as Terraform code. The export captures your current resource settings, including network rules, identity configuration, and project associations. Use the exported code as a starting point for managing the resource with Terraform.

1. In the [Azure portal](https://portal.azure.com), go to your Foundry resource.
1. In the left menu under **Automation**, select **Export template**.
1. Select the **Terraform** tab to view the generated Terraform code.
1. Select **Download** to save the file locally, or **Copy** to copy the code to your clipboard.

> [!NOTE]
> The export might complete with warnings if some resource types don't support full export. Review the output and fill in any missing properties manually.

### Import the exported resource into Terraform state

To manage the exported resource with Terraform going forward, import it into your Terraform state. For the AzAPI provider:

```terraform
terraform import azapi_resource.example <resource-id>
```

Replace `<resource-id>` with the full Azure resource ID shown in the exported file (for example, `/subscriptions/.../providers/Microsoft.CognitiveServices/accounts/<name>`).

### Customize the exported configuration

The exported Terraform code contains hardcoded values specific to your subscription and resource group. Before you reuse the configuration:

- Replace hardcoded subscription IDs, resource group names, and resource IDs with [Terraform variables](https://developer.hashicorp.com/terraform/language/values/variables).
- Remove any properties you don't need or that reference resources outside the deployment scope.
- Add or adjust security configurations to match your organization's requirements.

For production-ready Terraform configurations with enterprise security built in, see the [infrastructure-setup-terraform](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform) folder in the Foundry samples repository.

### Related security configurations

When you customize your configuration, consider adding the following security settings:

- [Configure network isolation with private endpoints](configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Create custom Azure Policy definitions](custom-policy-definition.md)

[!INCLUDE [create-resource-terraform 2](../includes/how-to-create-resource-terraform-2.md)]
