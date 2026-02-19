---
title: Use Azure Policies with hubs and projects
titleSuffix: Microsoft Foundry
description: Learn how to use Azure Policy with Microsoft Foundry to make sure your hubs and projects are compliant with your requirements.
ms.author: jburchel 
author: jonburchel 
ms.date: 01/06/2026
ms.service: azure-ai-foundry
ms.custom: hub-only, dev-focus
ms.topic: how-to
ms.reviewer: aashishb
reviewer: aashishb_microsoft
ai-usage: ai-assisted
# Customer Intent: As an admin, I want to understand how I can use Azure Policy to audit and govern Microsoft Foundry Services so that I can ensure compliance with my organization's requirements.
---

# Audit and manage Microsoft Foundry hubs and projects

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

As a platform administrator, use policies to set guardrails for teams to manage their own resources. [Azure Policy](/azure/governance/policy/) helps you audit and govern resource state. This article explains how you can use audit controls and governance practices for [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

## Prerequisites

- A Foundry hub and project in an Azure subscription.
- Azure RBAC permissions to create and assign Azure Policy resources at the scope where you assign policies. Use **Resource Policy Contributor** (least privilege) or **Owner**.
- If you use policies with the `deployIfNotExists` or `modify` effects and a managed identity, permissions to assign roles to that managed identity (for example, **User Access Administrator** or **Owner**).
- (Optional) Azure CLI if you use the command in this article.

## List policy aliases for Foundry resources

When you create a custom policy definition, use policy aliases (fields) to evaluate resource properties. This Azure CLI command lists the available aliases for the Azure Machine Learning resource provider (`Microsoft.MachineLearningServices`). The list includes the resource types used by Foundry hubs and projects.

```azurecli
az provider show --namespace Microsoft.MachineLearningServices --expand "resourceTypes/aliases" --query "resourceTypes[].aliases[].name"
```

Reference: [az provider show](/cli/azure/provider#az-provider-show)

## Policies for Foundry hubs and projects

[Azure Policy](/azure/governance/policy/) is a governance tool that you can use to ensure that Azure resources comply with your policies.

Azure Policy provides a set of policies that you can use for common scenarios with Foundry hubs and projects. You can assign these policy definitions to your existing subscription or use them as the basis to create your own [custom definitions](#create-custom-definitions).

The following table lists the built-in policies that apply to both Foundry and Azure Machine Learning. For a list of all Azure built-in policies, see [Built-in policies](/azure/governance/policy/samples/built-in-policies).

> [!IMPORTANT]
> Once you assign a policy, it applies to both Foundry and Azure Machine Learning workspaces. For example, a policy at the subscription level that disables public network access applies to all Foundry hubs and projects, and Azure Machine Learning workspaces.

|Name<br /><sub>(Azure portal)</sub> |Description |Effects |Version<br /><sub>(GitHub)</sub> |
|---|---|---|---|
|[Compute Instance should have idle shutdown.](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F679ddf89-ab8f-48a5-9029-e76054077449) |Having an idle shutdown schedule reduces cost by shutting down computes that are idle after a predetermined period of activity. |Audit, Deny, Disabled |[1.0.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/IdleShutdown_Audit.json) |
|[Compute instances should be recreated to get the latest software updates](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Ff110a506-2dcb-422e-bcea-d533fc8c35e2) |Ensure compute instances run on the latest available operating system. Security is improved and vulnerabilities reduced by running with the latest security patches. For more information, visit [https://aka.ms/azureml-ci-updates/](https://aka.ms/azureml-ci-updates/). |[parameters('effects')] |[1.0.3](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/ComputeInstanceUpdates_Audit.json) |
|[Computes should be in a virtual network](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F7804b5c7-01dc-4723-969b-ae300cc07ff1) |Azure Virtual Networks provide enhanced security and isolation for your compute clusters and instances, as well as subnets, access control policies, and other features to further restrict access. When a compute is configured with a virtual network, it isn't publicly addressable and can only be accessed from virtual machines and applications within the virtual network. |Audit, Disabled |[1.0.1](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Vnet_Audit.json) |
|[Computes should have local authentication methods disabled](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fe96a9a5f-07ca-471b-9bc5-6a0f33cbd68f) |Disabling local authentication methods improves security by ensuring that computes require Microsoft Entra ID identities exclusively for authentication. Learn more at: [https://aka.ms/azure-ml-aad-policy](https://aka.ms/azure-ml-aad-policy). |Audit, Deny, Disabled |[2.1.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/DisableLocalAuth_Audit.json) |
|[Hubs should be encrypted with a customer-managed key](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fba769a63-b8cc-4b2d-abf6-ac33c7204be8) |Manage encryption at rest of data with customer-managed keys. By default, customer data is encrypted with service-managed keys, but customer-managed keys are commonly required to meet regulatory compliance standards. Customer-managed keys enable the data to be encrypted with an Azure Key Vault key created and owned by you. You have full control and responsibility for the key lifecycle, including rotation and management. Learn more at [https://aka.ms/azureml-workspaces-cmk](https://aka.ms/azureml-workspaces-cmk). |Audit, Deny, Disabled |[1.1.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_CMKEnabled_Audit.json) |
|[Hubs should disable public network access](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F438c38d2-3772-465a-a9cc-7a6666a275ce) |Disabling public network access improves security by ensuring that hubs and projects aren't exposed on the public internet. You can control exposure of your workspaces by creating private endpoints instead. Learn more at: [Configure a private endpoint](configure-private-link.md). |Audit, Deny, Disabled |[2.0.1](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_PublicNetworkAccessDisabled_Audit.json) |
|[Hubs should use private link](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F45e05259-1eb5-4f70-9574-baf73e9d219b) |Azure Private Link lets you connect your virtual network to Azure services without a public IP address at the source or destination. The Private Link platform handles the connectivity between the consumer and services over the Azure backbone network. By mapping private endpoints to hubs, data leakage risks are reduced. Learn more at: [Configure a private endpoint](configure-private-link.md). |Audit, Disabled |[1.0.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_PrivateEndpoint_Audit_V2.json) |
|[Hubs should use user-assigned managed identity](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F5f0c7d88-c7de-45b8-ac49-db49e72eaa78) |Manage access to hubs and associated resources, Azure Container Registry, KeyVault, Storage, and App Insights using user-assigned managed identity. By default, system-assigned managed identity is used by a hub to access the associated resources. User-assigned managed identity allows you to create the identity as an Azure resource and maintain the life cycle of that identity. |Audit, Deny, Disabled |[1.0.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_UAIEnabled_Audit.json) |
|[Computes to disable local authentication methods](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fa6f9a2d0-cff7-4855-83ad-4cd750666512) |Disable location authentication methods so that your computes require Microsoft Entra ID identities exclusively for authentication. Learn more at: [https://aka.ms/azure-ml-aad-policy](https://aka.ms/azure-ml-aad-policy). |Modify, Disabled |[2.1.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/DisableLocalAuth_Modify.json) |
|[Configure hubs to use private DNS zones](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fee40564d-486e-4f68-a5ca-7a621edae0fb) |Use private DNS zones to override the DNS resolution for a private endpoint. A private DNS zone links to your virtual network to resolve to Foundry hubs. |DeployIfNotExists, Disabled |[1.1.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_PrivateDnsZones_DINE.json) |
|[Configure hubs to disable public network access](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fa10ee784-7409-4941-b091-663697637c0f) |Disable public network access for hubs and projects so that they aren't accessible over the public internet. This helps protect the workspaces against data leakage risks. You can control exposure of your workspaces by creating private endpoints instead. Learn more at: [Configure a private endpoint](configure-private-link.md). |Modify, Disabled |[1.0.3](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_PublicNetworkAccessDisabled_Modify.json) |
|[Configure Azure hubs with private endpoints](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F7838fd83-5cbb-4b5d-888c-bfa240972597) |Private endpoints connect your virtual network to Azure services without a public IP address at the source or destination. By mapping private endpoints to your hub, you can reduce data leakage risks. Learn more at: [Configure a private endpoint](configure-private-link.md). |DeployIfNotExists, Disabled |[1.0.0](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/Workspace_PrivateEndpoint_DINE.json) |
|[Configure diagnostic settings for hubs to Log Analytics workspace](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Ff59276f0-5740-4aaf-821d-45d185aa210e) |Deploys the diagnostic settings for Foundry hubs to stream resource logs to a Log Analytics Workspace when any hub which is missing this diagnostic setting is created or updated. |DeployIfNotExists, Disabled |[1.0.1](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/AuditDiagnosticLog_DINE.json) |
|[Resource logs in hubs should be enabled](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fafe0c3be-ba3b-4544-ba52-0c99672a8ad6) |Resource logs enable recreating activity trails to use for investigation purposes when a security incident occurs or when your network is compromised. |AuditIfNotExists, Disabled |[1.0.1](https://github.com/Azure/azure-policy/blob/master/built-in-policies/policyDefinitions/Machine%20Learning/AuditDiagnosticLog_Audit.json) |

Set policies at different scopes, such as at the subscription or resource group level. For more information, see the [Azure Policy documentation](/azure/governance/policy/overview).

## Assign built-in policies

To view the built-in policy definitions, use the following steps:

1. Go to **Azure Policy** in the [Azure portal](https://portal.azure.com).
1. Select **Definitions**.
1. For **Type**, select **Built-in**. For **Category**, select **Machine Learning**.

Select a policy definition to view it. While viewing a definition, select **Assign** to assign the policy to a scope and configure its parameters. For more information, see [Create a policy assignment to identify noncompliant resources using Azure portal](/azure/governance/policy/assign-policy-portal).

Assign policies by using [Azure PowerShell](/azure/governance/policy/assign-policy-powershell), [Azure CLI](/azure/governance/policy/assign-policy-azurecli), or [templates](/azure/governance/policy/assign-policy-template).

## Conditional access policies

Control access to Foundry hubs and projects by using [Microsoft Entra Conditional Access](/azure/active-directory/conditional-access/overview). For hubs, [assign the Conditional Access policy](/azure/active-directory/conditional-access/concept-conditional-access-cloud-apps) to these apps:

| App name | App ID | Description |
|---|---|---|
| Foundry App | cb2ff863-7f30-4ced-ab89-a00194bcf6d9 | Controls access to the Foundry portal. |
| Azure Machine Learning Web App | d7304df8-741f-47d3-9bc2-df0e24e2071f | Controls access to Azure Machine Learning studio. |
| Azure Machine Learning | 0736f41a-0425-bdb5-1563eff02385 | Controls direct access to the Azure Machine Learning API (for example, when using the SDK or REST API). Foundry hub-based projects rely on this API. |

## Configure built-in policies

### Compute instance should have idle shutdown

This policy controls whether a compute instance has idle shutdown enabled. Idle shutdown automatically stops the compute instance when it's idle for a specified period of time. This policy is useful for cost savings and to ensure that resources aren't used unnecessarily.

To configure this policy, set the effect parameter to **Audit**, **Deny**, or **Disabled**. If you set the effect to **Audit**, you can create a compute instance without idle shutdown. The service creates a warning event in the activity log.

### Compute instances should be recreated to get software updates

Controls whether compute instances are audited to make sure they're running the latest available software updates. This policy is useful to ensure that compute instances are running the latest software updates to maintain security and performance. For more information, see [Vulnerability management](../concepts/vulnerability-management.md#compute-instance).

To configure this policy, set the effect parameter to __Audit__ or __Disabled__. If set to __Audit__, a warning event is created in the activity log when a compute isn't running the latest software updates.

### Compute cluster and instance should be in a virtual network

Controls auditing of compute cluster and instance resources behind a virtual network.

To configure this policy, set the effect parameter to __Audit__ or __Disabled__. If set to __Audit__, you can create a compute that isn't configured behind a virtual network and a warning event is created in the activity log.

### Compute clusters and instances should have local authentication disabled

Controls whether a compute cluster or instance disables local authentication (SSH).

To configure this policy, set the effect parameter to __Audit__, __Deny__, or __Disabled__. If set to __Audit__, you can create a compute with SSH enabled and a warning event is created in the activity log.

If the policy is set to __Deny__, then you can't create a compute unless SSH is disabled. Attempting to create a compute with SSH enabled results in an error. The error is also logged in the activity log. The policy identifier is returned as part of this error.

### Hubs should be encrypted with a customer-managed key

Controls whether a hub and its projects are encrypted with a customer-managed key, or with a Microsoft-managed key to encrypt metrics and metadata. For more information on using customer-managed key, see the [Customer-managed keys](../concepts/encryption-keys-portal.md) article.

To configure this policy, set the effect parameter to __Audit__ or __Deny__. If set to __Audit__, you can create a hub without a customer-managed key and a warning event is created in the activity log.

If the policy is set to __Deny__, then you can't create a hub unless it specifies a customer-managed key. Attempting to create a hub without a customer-managed key results in an error similar to `Resource 'clustername' was disallowed by policy` and creates an error in the activity log. The policy identifier is also returned as part of this error.

### Configure hubs to disable public network access

Controls whether a hub and its projects disable network access from the public internet.

To configure this policy, set the effect parameter to __Audit__, __Deny__, or __Disabled__. If you set it to __Audit__, you can create a hub with public access and a warning event is created in the activity log.

If you set the policy to __Deny__, you can't create a hub that allows network access from the public internet.

### Hubs should use Azure Private Link

Controls whether a hub and its projects use Azure Private Link to communicate with Azure Virtual Network. For more information on using private link, see [Configure a private endpoint](configure-private-link.md).

To configure this policy, set the effect parameter to __Audit__ or __Deny__. If you set it to __Audit__, you can create a hub without using private link and a warning event is created in the activity log.

If you set the policy to __Deny__, you can't create a hub unless it uses a private link. Attempting to create a hub without a private link results in an error. The error is also logged in the activity log. The policy identifier is returned as part of this error.

### Hubs should use a user-assigned managed identity

Controls whether a hub is created using a system-assigned managed identity (default) or a user-assigned managed identity. The managed identity for the hub is used to access associated resources such as Azure Storage, Azure Container Registry, Azure Key Vault, and Azure Application Insights.

To configure this policy, set the effect parameter to __Audit__, __Deny__, or __Disabled__. If you set it to __Audit__, you can create a hub without specifying a user-assigned managed identity. A system-assigned identity is used, and a warning event is created in the activity log.

If you set the policy to __Deny__, you can't create a hub unless you provide a user-assigned identity during the creation process. Attempting to create a hub without providing a user-assigned identity results in an error. The error is also logged to the activity log. The policy identifier is returned as part of this error.

### Configure compute resources to modify or disable local authentication

This policy modifies any compute cluster or instance creation request to disable local authentication (SSH).

To configure this policy, set the effect parameter to __Modify__ or __Disabled__. If you set __Modify__, any creation of a compute cluster or instance within the scope where the policy applies automatically has local authentication disabled.

### Configure a hub to use private DNS zones

This policy configures a hub to use a private DNS zone, overriding the default DNS resolution for a private endpoint.

To configure this policy, set the effect parameter to __DeployIfNotExists__. Set the __privateDnsZoneId__ to the Azure Resource Manager ID of the private DNS zone to use. 

### Configure a hub to disable public network access

Configures a hub and its projects to disable network access from the public internet. Disabling public network access helps protect against data leakage risks. You can instead access your hub and projects by creating private endpoints. For more information, see [Configure a private endpoint](configure-private-link.md).

To configure this policy, set the effect parameter to __Modify__ or __Disabled__. If you set it to __Modify__, any creation of a hub within the scope where the policy applies automatically has public network access disabled.

### Configure a hub with private endpoints

Configures a hub to create a private endpoint within the specified subnet of an Azure Virtual Network.

To configure this policy, set the effect parameter to __DeployIfNotExists__. Set the __privateEndpointSubnetID__ to the Azure Resource Manager ID of the subnet.

### Configure diagnostic hub to send logs to Log Analytics workspaces

Configures the diagnostic settings for a hub to send logs to a Log Analytics workspace.

To configure this policy, set the effect parameter to __DeployIfNotExists__ or __Disabled__. If you set it to __DeployIfNotExists__, the policy creates a diagnostic setting to send logs to a Log Analytics workspace if it doesn't already exist.

### Resource logs in a hub should be enabled

Audits whether resource logs are enabled for a hub. Resource logs provide detailed information about operations performed on resources in the hub.

To configure this policy, set the effect parameter to __AuditIfNotExists__ or __Disabled__. If you set it to __AuditIfNotExists__, the policy audits if resource logs aren't enabled for the hub.

## Create custom definitions

Create custom policies by using the [Azure Policy definition structure](/azure/governance/policy/concepts/definition-structure-basics). Use the [Azure Policy Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=AzurePolicy.azurepolicyextension) to author and test policies.

Find allowed values for a specific alias in the [Azure Machine Learning REST API](/rest/api/azureml/) reference.

For a general tutorial on creating custom policies, see [Create a custom policy definition](/azure/governance/policy/tutorials/create-custom-policy-definition).

### Example: Deny serverless Spark compute jobs

```json
{
    "properties": {
        "displayName": "Deny serverless Spark compute jobs",
        "description": "Deny serverless Spark compute jobs",
        "mode": "All",
        "policyRule": {
            "if": {
                "allOf": [
                    {
                        "field": "Microsoft.MachineLearningServices/workspaces/jobs/jobType",
                        "in": [
                            "Spark"
                        ]
                    }
                ]
            },
            "then": {
                "effect": "Deny"
            }
        },
        "parameters": {}
    }
}
```

Reference: [Azure Policy definition structure](/azure/governance/policy/concepts/definition-structure-basics)

### Example: Deny public IPs for managed computes

```json
{
    "properties": {
        "displayName": "Deny compute instance and compute cluster creation with public IP",
        "description": "Deny compute instance and compute cluster creation with public IP",
        "mode": "All",
        "parameters": {
            "effectType": {
                "type": "string",
                "defaultValue": "Deny",
                "allowedValues": [
                    "Deny",
                    "Disabled"
                ],
                "metadata": {
                    "displayName": "Effect",
                    "description": "Enable or disable the execution of the policy"
                }
            }
        },
        "policyRule": {
            "if": {
                "allOf": [
                  {
                    "field": "type",
                    "equals": "Microsoft.MachineLearningServices/workspaces/computes"
                  },
                  {
                    "allOf": [
                      {
                        "field": "Microsoft.MachineLearningServices/workspaces/computes/computeType",
                        "notEquals": "AKS"
                      },
                      {
                        "field": "Microsoft.MachineLearningServices/workspaces/computes/enableNodePublicIP",
                        "equals": true
                      }
                    ]
                  }
                ]
              },
            "then": {
                "effect": "[parameters('effectType')]"
            }
        }
    }
}
```

Reference: [Azure Policy definition structure](/azure/governance/policy/concepts/definition-structure-basics)


## Related content

* [Azure Policy documentation](/azure/governance/policy/overview)
* [Working with security policies with Microsoft Defender for Cloud](/azure/security-center/tutorial-security-policy)
* The [Cloud Adoption Framework scenario for data management and analytics](/azure/cloud-adoption-framework/scenarios/data-management/) outlines considerations for running data and analytics workloads in the cloud.
* [Use policy to integrate Azure Private Link with Azure Private DNS zones](/azure/cloud-adoption-framework/ready/azure-best-practices/private-link-and-dns-integration-at-scale)
