---
title: "Quickstart: Deploy a Foundry resource by using Bicep"
titleSuffix: Microsoft Foundry
description: Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription.
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 07/28/2026
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: quickstart
ms.custom:
  - classic-and-new
  - "subject-bicepqs"
  - "build-aifnd"
  - "build-2025"
  - "dev-focus"
  - doc-kit-assisted
ai-usage: ai-assisted
# Customer intent: As a DevOps person, I need to automate or customize the creation of a Foundry resource by using templates.
---

# Quickstart: Deploy a Microsoft Foundry resource by using a Bicep file

[!INCLUDE [create-resource-template-deploy](../includes/how-to-create-resource-template-deploy.md)]

[!INCLUDE [create-resource-template-export](../includes/how-to-create-resource-template-export.md)]

### Related security configurations

When you customize your template, consider adding the following security configurations. Choose based on your governance requirements:

| Control | When to add it | Learn more |
| --- | --- | --- |
| **Private endpoints (network isolation)** | Your organization bans public endpoints, or you need to keep traffic on your virtual network for compliance (HIPAA, PCI, FedRAMP). | [Configure network isolation with private endpoints](configure-private-link.md) |
| **Customer-managed keys (CMK) for encryption** | You must control the encryption-key lifecycle, rotation cadence, or revocation, or your data classification requires bring-your-own-key. | [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md) |
| **Role-based access control (RBAC)** | You need least-privilege access for builders versus administrators, or you grant access to multiple teams that share a Foundry resource. | [Configure role-based access control for Foundry](../concepts/rbac-foundry.md) |
| **Custom Azure Policy definitions** | Your platform team enforces a security baseline (allowed regions, required tags, allowed SKUs, mandatory CMK or private link) across every Foundry resource the organization creates. | [Create custom Azure Policy definitions](custom-policy-definition.md) |

[!INCLUDE [create-resource-template 1](../includes/how-to-create-resource-template-1.md)]

## Troubleshooting

| Symptom | Cause | Resolution |
| --- | --- | --- |
| `ServiceModelDeprecating` error during deployment | The Bicep template includes a model deployment that references a retired or deprecating model version. | Open `main.bicep`, find the `modelDeployment` resource block, and either comment it out or update the model `name` and `version` to a currently available model. Run `az cognitiveservices model list --location <your-location> --query "[?model.lifecycleStatus=='GenerallyAvailable']"` to find available models. |
| `The content for this response was already consumed` | Azure CLI versions 2.74–2.75 have a known bug that masks the actual deployment error. | Run the command again with `--debug` and search for `Exception Details:` in the output to find the real error. |
| Deployment fails with `AccountNameInvalid` | The `aiFoundryName` value must be globally unique, 2–64 characters, and can contain only lowercase letters, numbers, and hyphens. | Choose a different name, such as `<your-name>-foundry-<random-suffix>`. |
| Resources deploy to a different region than the resource group | The Bicep template's `location` parameter defaults to `eastus2`, but the resource group might be in a different region. | Pass the `location` parameter explicitly. For example, add `location=eastus` to your `--parameters` list. |

## Related content

- [Get started with the SDK](../quickstarts/get-started-code.md)
- [Configure network isolation with private endpoints](../how-to/configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Security configurations samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) — See example Bicep template configurations for enterprise security configurations, including network isolation, customer-managed key encryption, advanced identity options, and Agents standard setup.
