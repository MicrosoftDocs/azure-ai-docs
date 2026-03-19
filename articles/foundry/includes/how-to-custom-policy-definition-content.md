---
title: include file
description: include file
author: scottpolly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include
---

Learn how to use custom Azure policies to enable teams to self-manage Microsoft Foundry resources. Apply guardrails and constraints on allowed configurations so you can provide flexibility while meeting security and compliance requirements.

By using custom policies, you can:

- **Enforce governance**: Prevent unauthorized creation of Foundry hubs, projects, connections, or capability hosts.
- **Control resource behavior**: Ensure security configurations, enforce tagging, or allow only approved integrations.
- **Ensure compliance**: Apply enterprise security and operational standards consistently across environments.

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]
- [!INCLUDE [rbac-assign-roles](rbac-assign-roles.md)]
- The **Resource Policy Contributor** role (least privilege) or **Owner** role at the scope where you create and assign the policy definition.

For more information, see [What is Azure Policy?](/azure/governance/policy/overview)

## Steps to create a custom policy

1. **Open policy in the Azure portal**
   - Go to [Azure portal](https://portal.azure.com).
   - Search for _Policy_ and select it.

1. **Define a new policy**
   - In the **Authoring** section, select **Definitions** > **+ Policy definition**.
   - Provide:
     - **Definition location**: Subscription (applies to resources in a single subscription) or management group (applies across multiple subscriptions).
     - **Name**: A unique name (for example, `Deny-Unapproved-Connections`).
     - **Description**: Explain the purpose (for example, “Restrict Foundry connections to approved categories”).
     - **Category**: Use an existing category or create one such as `AI Governance`.

1. **Add policy rule**
   - Enter the rule in [JSON format](/azure/governance/policy/concepts/definition-structure-policy-rule). For example, the following policy restricts Foundry connections to approved categories:

      ```json
      {
        "mode": "All",
        "policyRule": {
          "if": {
            "allOf": [
              {
                "field": "type",
                "in": [
                  "Microsoft.CognitiveServices/accounts/connections",
                  "Microsoft.CognitiveServices/accounts/projects/connections"
                ]
              },
              {
                "field": "Microsoft.CognitiveServices/accounts/connections/category",
                "notIn": "[parameters('allowedCategories')]"
              }
            ]
          },
          "then": {
            "effect": "Deny"
          }
        },
        "parameters": {
          "allowedCategories": {
            "type": "Array",
            "metadata": {
              "displayName": "Allowed connection categories",
              "description": "List of connection categories approved for use"
            }
          }
        }
      }
      ```

      For a complete, ready-to-use version of this policy, see the full sample:

      :::code language="json" source="~/foundry-samples-main/infrastructure/infrastructure-setup-bicep/05-custom-policy-definitions/deny-disallowed-connections.json"
      

  This policy denies creation of Foundry connections when the connection `category` isn't in the `allowedCategories` parameter. It applies to both `Microsoft.CognitiveServices/accounts/connections` and `Microsoft.CognitiveServices/accounts/projects/connections`.

  To customize the behavior, update `allowedCategories` (or override it when you assign the policy) with the connection categories your organization approves.

  References:
  - Reference: [Policy definition structure](/azure/governance/policy/concepts/definition-structure)
  - Reference: [Policy rule structure](/azure/governance/policy/concepts/definition-structure-policy-rule)
  - Reference: [Policy effects](/azure/governance/policy/concepts/effects)

1. **Assign the policy**
   - After saving, assign the policy to the desired scope (subscription, resource group, or hub).

1. **Validate the policy assignment**
   - Try to create a connection with a category that isn't in `allowedCategories` and confirm the request is denied.
   - Try to create a connection with a category that is in `allowedCategories` and confirm the request succeeds.

## Common custom policy scenarios

- **Allow only approved connection categories**  
  Block any connection category other than those approved by your organization.

- **Deny connections that use API keys as the authentication type**  
  Require all other authentication types because API keys are typically less secure.

- **Audit Foundry resources without a valid Agent capability host**  
  Check for the existence of a virtual network subnet ARM ID and custom storage resources when using Agent service in a regulated environment.

- **Deny creation of account kinds that don't have full Foundry capabilities**  
  Ensure new accounts are configured so users can access all Foundry capabilities.

## Sample library

Explore ready-to-use templates and examples in the GitHub repository:  
[Custom policy definitions](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/05-custom-policy-definitions)

This library includes JSON templates for common scenarios.

## Next steps

- Review [Built-in Policies for Foundry](../../ai-services/policy-reference.md) for built-in and custom policies for comprehensive compliance.
- Test policies in a nonproduction environment before enforcing them broadly.

## Troubleshooting

- If you can't create or assign a policy definition, confirm you have the required role at the scope you're using.
- If a connection isn't blocked as expected, confirm the policy assignment scope includes the target resource.
- If a policy blocks more resources than expected, review the `allowedCategories` value used in the assignment.
- Policy evaluation can take up to 30 minutes after assignment. To force immediate evaluation, run `az policy state trigger-scan --resource-group <resource-group-name>`.
