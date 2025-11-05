**Title:** Quickstart: Create a guardrail policy

**Description:** These instructions will guide you in creating a guardrail policy for your model deployments in Azure AI Foundry. This policy will allow you to govern the usage of guardrail controls across your subscription.

**Author:** \[\]

**ms.author:** \[your Microsoft alias or a team alias\]

**ms.service:** \[the approved service name\]

**ms.topic:** quickstart (Don't change)

**ms.date:** \[mm/dd/yyyy\]

**Customer intent:** As a , I want so that .

# Quickstart: Create a guardrail policy

This quick start guide will show you how to create an Azure Policy in Azure AI Foundry to govern the use of guardrail controls for model deployments across your subscription.

## Prerequisites

- Users must be using the Azure AI Foundry NextGen UI experience, currently in Public Preview.

- Users must have the appropriate roles to create an Azure Policy for their subscription. You can learn more about Azure Policy roles here: [Overview of Azure Policy - Azure Policy \| Microsoft Learn](/azure/governance/policy/overview#azure-policy-and-azure-rbac)

## Create the guardrail policy

1. The first step is to navigate to the Compliance page within the main Operate tab:


1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/compliance-tab.png" alt-text="Screenshot of the Compliance pane of the Foundry Control Plane." lightbox="media/quickstart-create-a-guardrail-policy/compliance-tab.png":::

1. Once there, select "Create new policy".

1. Select and add the various controls to be added to the policy. These will be the minimum settings that are required for a model deployment to be considered compliant with the policy. As you configure each control, select "Add control" to add it to the policy.

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/create-new-policy.png" alt-text="A screenshot of the Create Policy dialog." lightbox="media/quickstart-create-a-guardrail-policy/create-new-policy.png":::

1. Select "Next" to move to scope selection. You can scope your policy to a single subscription or a resource group. Select the desired scope and select the "Select" button to pick a subscription or resource group from a list of resources which you have access to.

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-scope.png" alt-text="Screenshot of the scope selection page showing subscription and resource group options." lightbox="media/quickstart-create-a-guardrail-policy/select-scope.png":::

1. Pick the desired subscription or resource group to apply to the policy and select the "Select" button.

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/subscription-selection.png" alt-text="Screenshot of the subscription or resource group selection dialog." lightbox="media/quickstart-create-a-guardrail-policy/subscription-selection.png":::

1. Then select the "Next" button to add exceptions to the policy. When you select the scope in the previous step as a subscription, you can create an exception for entire Resource Group as well as individual model deployments within that Subscription. When a policy is scoped just to a Resource Group, only Model Deployments can be given exceptions.

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-exception.png" alt-text="Screenshot of the exceptions configuration page." lightbox="media/quickstart-create-a-guardrail-policy/select-exception.png":::

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/resource-group-exception.png" alt-text="Screenshot of the exceptions interface showing resource group and model deployment options." lightbox="media/quickstart-create-a-guardrail-policy/resource-group-exception.png":::

1. Once all exceptions have been added, select "Next" to move to the review stage. Here, you'll name your policy and review the scope, exceptions, and controls that define the policy. Once ready, select Submit to create the policy.

1. :::image type="content" source="media/quickstart-create-a-guardrail-policy/submit-policy.png" alt-text="Screenshot of the review and submit page for the guardrail policy." lightbox="media/quickstart-create-a-guardrail-policy/submit-policy.png":::



## Next step or Related content


Now that your policy is created, you can review it in the section of the Compliance tab. Please note that it will take some time for Azure Policy to perform a compliance scan.

You can also review and manage your created policies directly in Azure Policy via the Azure Portal. When creating this policy assignment, Foundry actually creates a series of policies and associates these assignments to a policy initiative. In Foundry, you are viewing the status of the policy initiative, not an individual policy.
