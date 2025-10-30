---
title: Create a custom Azure Policy for AI Foundry
titleSuffix: Azure AI Foundry
description: "Learn how to use custom Azure policies to enable self-serve resource management in your organization, while putting guardrails and constrainst on allowed configurations to meet security and compliance requirements."
ms.author: deeikele 
author: compliance 
ms.service: azure-ai-foundry
ms.topic: how-to #Don't change
ms.date: 10/29/2025
ms.reviewer: jburchel
reviewer: jonburchel
#customer intent: As an admin, I want to enable self-serve resource management while staying compliant to security and compliance requirements.

---

# Create Custom Policies for Azure AI Foundry

Learn how to use custom Azure policies to enable teams to self-serve manage AI Foundry resources. Set guardrails and constrainst on allowed configurations, so you can give flexiblity but continue to meet security and compliance requirements.

Custom policies allow you to:

- **Enforce governance**: Prevent unauthorized creation of AI Foundry, projects, connections, or capability hosts.
- **Control resource behavior**: Ensure security configurations, enforce tagging, or allow only approved integrations.
- **Ensure compliance**: Apply enterprise security and operational standards consistently across environments.

## Prerequisites

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.
- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Steps to Create a Custom Policy

1. **Open Azure Policy in the Portal**
   - Navigate to https://portal.azure.com.
   - Search for **Policy** and select it.

2. **Define a New Policy**
   - In the **Authoring** section, select **Definitions** > **+ Policy definition**.
   - Provide:
     - **Definition location**: Subscription or management group.
     - **Name**: A unique name (e.g., `Deny-Unapproved-Connections`).
     - **Description**: Explain the purpose (e.g., “Restrict AI Foundry connections to approved categories”).
     - **Category**: Use an existing category or create one like `AI Governance`.

3. **Add Policy Rule**
   - Enter the rule in JSON format. For example, to allow only approved connection categories:

    :::code language="json" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup/05-custom-policy-definitions/deny-disallowed-connections.json"

4. **Assign the Policy**
   - After saving, assign the policy to the desired scope (subscription, resource group, or hub).

## Common Custom Policy Scenarios

- **Allow only approved connection categories**  
  Block any other connection category than the ones you allow as an organization.

- **Deny connections that use API keys as authentication type**  
  Requires all other authentication types for connections than API keys as typically less secure authentication method.

- **Audit AI Foundry resources without valid Agent capability host**  
  Scan for existance of virtual network subnet ARM ID, and custom storage resources when using Agent service in a regulated environment.

- **Deny creation of account kinds that do not have full Foundry capabilities**  
  Enforce any new accounts to be configured such that users can access all AI Foundry capabilities.

## Sample Library

Explore ready-to-use templates and examples in the GitHub repository:  
https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/05-custom-policy-definitions

This library includes JSON templates for common scenarios.


## Next Steps

- Review https://learn.microsoft.com/azure/ai-studio/how-to/azure-policy for baseline governance.
- Combine built-in and custom policies for comprehensive compliance.
- Test policies in a non-production environment before enforcing them broadly.** to create custom policies that control resource configurations, restrict actions, and ensure consistent standards across hubs and projects.
