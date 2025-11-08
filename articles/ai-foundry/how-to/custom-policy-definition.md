---
title: Create a custom Azure Policy for AI Foundry
titleSuffix: Azure AI Foundry
description: "Learn how to use custom Azure policies to enable self-service resource management in your organization, while applying guardrails and constraints on allowed configurations to meet security and compliance requirements."
ms.author: deeikele
author: compliance
ms.service: azure-ai-foundry
ms.topic: how-to #Don't change
ms.date: 10/29/2025
ms.reviewer: jburchel
reviewer: jonburchel
#customer intent: As an admin, I want to enable self-service resource management while staying compliant with security and compliance requirements.
---

# Create custom policies for Azure AI Foundry

Learn how to use custom Azure policies to enable teams to self-manage AI Foundry resources. Apply guardrails and constraints on allowed configurations so you can provide flexibility while meeting security and compliance requirements.

Custom policies allow you to:

- **Enforce governance**: Prevent unauthorized creation of AI Foundry hubs, projects, connections, or capability hosts.
- **Control resource behavior**: Ensure security configurations, enforce tagging, or allow only approved integrations.
- **Ensure compliance**: Apply enterprise security and operational standards consistently across environments.

## Prerequisites

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- Permissions to create and assign policies. You must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the subscription or resource group level.
n more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Steps to create a custom policy

1. **Open Azure Policy in the portal**
   - Go to [Azure portal](https://portal.azure.com).
   - Search for your policy and select it.

2. **Define a new policy**
   - In the **Authoring** section, select **Definitions** > **+ Policy definition**.
   - Provide:
     - **Definition location**: Subscription or management group.
     - **Name**: A unique name (for example, `Deny-Unapproved-Connections`).
     - **Description**: Explain the purpose (for example, “Restrict AI Foundry connections to approved categories”).
     - **Category**: Use an existing category or create one such as `AI Governance`.

3. **Add policy rule**
   - Enter the rule in JSON format. For example, to allow only approved connection categories:

     :::code language="json" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup/05-custom-policy-definitions/deny-disallowed-connections.json"

4. **Assign the policy**
   - After saving, assign the policy to the desired scope (subscription, resource group, or hub).

## Common custom policy scenarios

- **Allow only approved connection categories**  
  Block any connection category other than those approved by your organization.

- **Deny connections that use API keys as the authentication type**  
  Require all other authentication types because API keys are typically less secure.

- **Audit AI Foundry resources without a valid Agent capability host**  
  Check for the existence of a virtual network subnet ARM ID and custom storage resources when using Agent service in a regulated environment.

- **Deny creation of account kinds that don't have full Foundry capabilities**  
  Ensure new accounts are configured so users can access all AI Foundry capabilities.

## Sample library

Explore ready-to-use templates and examples in the GitHub repository:  
[Custom policy definitions](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/05-custom-policy-definitions)

This library includes JSON templates for common scenarios.

## Next steps

- Review [Built-in Policies for AI Foundry](../../ai-services/policy-reference.md) for built-in and custom policies for comprehensive compliance.
- Test policies in a non-production environment before enforcing them broadly.