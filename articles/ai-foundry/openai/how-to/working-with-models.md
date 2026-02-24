---
title: Azure OpenAI in Microsoft Foundry Models working with models
titleSuffix: Azure OpenAI
description: Learn about managing model deployment life cycle, updates, & retirement.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 02/12/2026
ms.custom: references_regions, build-2023, build-2023-dataai, devx-track-azurepowershell
manager: nitinme
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Working with models

Azure OpenAI in Microsoft Foundry Models is powered by a diverse set of models with different capabilities and price points. [Model availability varies by region](../../foundry-models/concepts/models-sold-directly-by-azure.md).

You can get a list of models that are available for both inference and fine-tuning by your Azure OpenAI resource by using the [Models List API](/rest/api/azureopenai/models/list).

This article shows you how to:

- Configure automatic model updates.
- View and update a deployment's version upgrade policy.
- Update a deployed model version by using the Azure Resource Manager API.
- Migrate provisioned deployments to a different model version or family.

## Prerequisites

- An Azure subscription with an Azure OpenAI models.

## Model updates

Azure OpenAI supports automatic updates for select model deployments. On models where automatic update support is available, a model version upgrade policy drop-down is available.

You can learn more about Azure OpenAI model versions and how they work in the [Azure OpenAI model versions](../concepts/model-versions.md) article.

> [!NOTE]
> Automatic model updates are only supported for Standard deployment types. For more information on how to manage model updates and migrations on provisioned deployment types, refer to the section on [managing models on provisioned deployment types](./working-with-models.md#managing-models-on-provisioned-deployment-types)

### Auto update to default

When you set your deployment to **Auto-update to default**, your model deployment is automatically updated within two weeks of a change in the default version.  For a preview version, it updates automatically when a new preview version is available starting two weeks after the new preview version is released.

If you're still in the early testing phases for inference models, we recommend deploying models with **auto-update to default** set whenever it's available.

### Specific model version

As your use of Azure OpenAI evolves, and you start to build and integrate with applications you might want to manually control model updates. You can first test and validate that your application behavior is consistent for your use case before upgrading.

When you select a specific model version for a deployment, this version remains selected until you either choose to manually update yourself, or once you reach the retirement date for the model. When the retirement date is reached the model will automatically upgrade to the default version at the time of retirement.

## Model deployment upgrade configuration

You can check what model upgrade options are set for previously deployed models using REST, Azure CLI, and Azure PowerShell, as well as with the Foundry portal.

The corresponding property can also be accessed via [REST](../how-to/working-with-models.md#model-deployment-upgrade-configuration), [Azure PowerShell](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccountdeployment), and [Azure CLI](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-show).

|Option| Read | Update |
|---|---|---|
| [REST](../how-to/working-with-models.md#model-deployment-upgrade-configuration) | Yes. If `versionUpgradeOption` isn't returned, it means it's `null` |Yes |
| [Azure PowerShell](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccountdeployment) | Yes.`VersionUpgradeOption` can be checked for `$null`| Yes |
| [Azure CLI](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-show) | Yes. It shows `null` if `versionUpgradeOption` isn't set.| *No.* It's currently not possible to update the version upgrade option.|

There are three distinct model deployment upgrade options:

| Name | Description |
|------|--------|
| `OnceNewDefaultVersionAvailable` | Once a new version is designated as the default, the model deployment automatically upgrades to the default version within two weeks of that designation change being made. |
|`OnceCurrentVersionExpired` | Once the retirement date is reached the model deployment automatically upgrades to the current default version. |
|`NoAutoUpgrade` | The model deployment never automatically upgrades. Once the retirement date is reached the model deployment stops working. You need to update your code referencing that deployment to point to a nonexpired model deployment. |

> [!NOTE]
> `null` is equivalent to `OnceCurrentVersionExpired`. If the **Version update policy** option isn't present in the properties for a model that supports model upgrades this indicates the value is currently `null`. Once you explicitly modify this value, the property is visible in the studio properties page as well as via the REST API.

### Examples

# [PowerShell](#tab/powershell)

Review the Azure PowerShell [getting started guide](/powershell/azure/get-started-azureps) to install Azure PowerShell locally or you can use the [Azure Cloud Shell](/azure/cloud-shell/overview).

The steps below demonstrate checking the `VersionUpgradeOption` option property as well as updating it:

```powershell
# Step 1: Get deployment
$deployment = Get-AzCognitiveServicesAccountDeployment -ResourceGroupName {ResourceGroupName} -AccountName {AccountName} -Name {DeploymentName}
 
# Step 2: Show VersionUpgradeOption
$deployment.Properties.VersionUpgradeOption
 
# VersionUpgradeOption can be null. One way to check is:
$null -eq $deployment.Properties.VersionUpgradeOption
 
# Step 3: Update VersionUpgradeOption
$deployment.Properties.VersionUpgradeOption = "NoAutoUpgrade"
New-AzCognitiveServicesAccountDeployment -ResourceGroupName {ResourceGroupName} -AccountName {AccountName} -Name {DeploymentName} -Properties $deployment.Properties -Sku $deployment.Sku
 
# Repeat steps 1 and 2 to confirm the change.
# If you aren't sure about the deployment name, list all deployments under an account:
Get-AzCognitiveServicesAccountDeployment -ResourceGroupName {ResourceGroupName} -AccountName {AccountName}
```

```powershell
# Update to a new model version

# Step 1: Get deployment
$deployment = Get-AzCognitiveServicesAccountDeployment -ResourceGroupName {ResourceGroupName} -AccountName {AccountName} -Name {DeploymentName}

# Step 2: Show the current model version
$deployment.Properties.Model.Version

# Step 3: Update the model version
$deployment.Properties.Model.Version = "0613"
New-AzCognitiveServicesAccountDeployment -ResourceGroupName {ResourceGroupName} -AccountName {AccountName} -Name {DeploymentName} -Properties $deployment.Properties -Sku $deployment.Sku

# Repeat steps 1 and 2 to confirm the change.
```

# [REST](#tab/rest)

To query the current model deployment settings including the deployment upgrade configuration for a given resource use [`Deployments List`](/rest/api/aiservices/accountmanagement/deployments/list?tabs=HTTP#code-try-0). If the value is null, you won't see a `versionUpgradeOption` property.

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/deployments?api-version=2023-05-01
```

**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```accountName``` | string |  Required | The name of your Azure OpenAI resource. |
| ```resourceGroupName``` | string |  Required | The name of the associated resource group for this model deployment. |
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2025-06-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2025-06-01/cognitiveservices.json)

### Example response

```json
{
  "value": [
    {
      "id": "/subscriptions/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeb/resourceGroups/az-test-openai/providers/Microsoft.CognitiveServices/accounts/aztestopenai001/deployments/gpt-35-turbo",
      "type": "Microsoft.CognitiveServices/accounts/deployments",
      "name": "gpt-35-turbo",
      "sku": {
        "name": "Standard",
        "capacity": 80
      },
      "properties": {
        "model": {
          "format": "OpenAI",
          "name": "gpt-35-turbo",
          "version": "0301"
        },
        "versionUpgradeOption": "OnceNewDefaultVersionAvailable",
        "capabilities": {
          "completion": "true",
          "chatCompletion": "true"
        },
        "raiPolicyName": "Microsoft.Default",
        "provisioningState": "Succeeded",
        "rateLimits": [
          {
            "key": "request",
            "renewalPeriod": 10,
            "count": 80
          },
          {
            "key": "token",
            "renewalPeriod": 60,
            "count": 80000
          }
        ]
      },
      "systemData": {
        "createdBy": "docs@contoso.com",
        "createdByType": "User",
        "createdAt": "2023-07-31T16:45:32.622404Z",
        "lastModifiedBy": "docs@contoso.com",
        "lastModifiedByType": "User",
        "lastModifiedAt": "2023-10-31T13:59:34.4978286Z"
      },
      "etag": "\"aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee\""
    }
  ]
}
```

You can then take the settings from this list to construct an update model REST API call as described below if you want to modify the deployment upgrade configuration.

---

## Update & deploy models via the API

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/deployments/{deploymentName}?api-version=2025-06-01
```

**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```accountName``` | string |  Required | The name of your Azure OpenAI resource. |
| ```deploymentName``` | string | Required | The deployment name you chose when you deployed an existing model or the name you would like a new model deployment to have.   |
| ```resourceGroupName``` | string |  Required | The name of the associated resource group for this model deployment. |
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2025-06-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2025-06-01/cognitiveservices.json)

**Request body**

This is only a subset of the available request body parameters. For the full list of the parameters, you can refer to the [REST API reference documentation](/rest/api/aiservices/accountmanagement/deployments/create-or-update).

|Parameter|Type| Description |
|--|--|--|
|versionUpgradeOption | String | Deployment model version upgrade options:<br>`OnceNewDefaultVersionAvailable`<br>`OnceCurrentVersionExpired`<br>`NoAutoUpgrade`|
|capacity|integer|This represents the amount of [quota](../how-to/quota.md) you're assigning to this deployment. A value of 1 equals 1,000 Tokens per Minute (TPM)|

#### Example request

```bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-35-turbo?api-version=2025-06-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"Standard","capacity":120},"properties": {"model": {"format": "OpenAI","name": "gpt-35-turbo","version": "0613"},"versionUpgradeOption":"OnceCurrentVersionExpired"}}'
```

> [!NOTE]
> There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account?view=azure-cli-latest#az-account-get-access-token&preserve-view=true). You can use this token as your temporary authorization token for API testing.

#### Example response

```json
 {
  "id": "/subscriptions/{subscription-id}/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-35-turbo",
  "type": "Microsoft.CognitiveServices/accounts/deployments",
  "name": "gpt-35-turbo",
  "sku": {
    "name": "Standard",
    "capacity": 120
  },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "gpt-35-turbo",
      "version": "0613"
    },
    "versionUpgradeOption": "OnceCurrentVersionExpired",
    "capabilities": {
      "chatCompletion": "true"
    },
    "provisioningState": "Succeeded",
    "rateLimits": [
      {
        "key": "request",
        "renewalPeriod": 10,
        "count": 120
      },
      {
        "key": "token",
        "renewalPeriod": 60,
        "count": 120000
      }
    ]
  },
  "systemData": {
    "createdBy": "docs@contoso.com",
    "createdByType": "User",
    "createdAt": "2023-02-28T02:57:15.8951706Z",
    "lastModifiedBy": "docs@contoso.com",
    "lastModifiedByType": "User",
    "lastModifiedAt": "2023-10-31T15:35:53.082912Z"
  },
  "etag": "\"GUID\""
}
```

## Managing models on provisioned deployment types

Provisioned deployments support distinct model management practices. Provisioned deployment model management practices are intended to give you the greatest control over when and how you migrate between model versions and model families. Currently, there are two approaches available to manage models on provisioned deployments: (1) in-place migrations and (2) multi-deployment migrations.

### Prerequisites

- Validate that the target model version or model family is supported for your existing deployment type. Migrations can only occur between provisioned deployments of the same deployment type. For more information on deployment types, review the [deployment type documentation](../../foundry-models/concepts/deployment-types.md).
- Validate capacity availability for your target model version or model family prior to attempting a migration. For more information on determining capacity availability, review the [capacity transparency documentation](../concepts/provisioned-throughput.md#capacity-transparency).
- For multi-deployment migrations, validate that you have sufficient quota to support multiple deployments simultaneously. For more information on how to validate quota for each provisioned deployment type, review the [provisioned throughput cost documentation](../how-to/provisioned-throughput-onboarding.md).

### In-place migrations for provisioned deployments

In-place migrations allow you to maintain the same provisioned deployment name and size while changing the model version or model family assigned to that deployment. With in-place migrations, Azure OpenAI takes care of migrating any existing traffic between model versions or model families throughout the migration over a 20-30 minute window. Throughout the migration window, your provisioned deployment will display an "updating" provisioned state. You can continue to use your provisioned deployment as you normally would. Once the in-place migration is complete, the provisioned state will be updated to "succeeded", indicating that all traffic has been migrated over to the target model version or model family. 

#### In-place migration: model version update

In-place migrations that target updating an existing provisioned deployment to a new model version within the same model family are supported through Foundry, REST API, and Azure CLI. To perform an in-place migration targeting a model version update within Foundry, select **Deployments** > under the deployment name column select the deployment name of the provisioned deployment you would like to migrate.

Selecting a deployment name opens the **Properties** for the model deployment. From this view, select the **edit** button, which will show the **Update deployment** dialogue box. Select the model version dropdown to set a new model version for the provisioned deployment. As noted, the provisioning state will change to "updating" during the migration and will revert to "succeeded" once the migration is complete. 

#### In-place migration: model family change
In-place migrations that target updating an existing provisioned deployment to a new model family are supported through REST API and Azure CLI. To perform an in-place migration targeting a model family change, use the example request below as a guide. In the request, you'll need to update the model name and model version for the target model you're migrating to. 

```bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-4o-ptu-deployment?api-version=2024-10-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"GlobalProvisionedManaged","capacity":100},"properties": {"model": {"format": "OpenAI","name": "gpt-4o-mini","version": "2024-07-18"}}}'
```
#### Example response

```json
{
  "id": "/subscriptions/{subscription-id}/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-4o-ptu-deployment",
  "type": "Microsoft.CognitiveServices/accounts/deployments",
  "name": "gpt-4o-ptu-deployment",
  "sku": {
    "name": "GlobalProvisionedManaged",
    "capacity": 100
  },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "gpt-4o-mini",
      "version": "2024-07-18"
    },
    "versionUpgradeOption": "OnceCurrentVersionExpired",
    "currentCapacity": 100,
    "capabilities": {
      "area": "EUR",
      "chatCompletion": "true",
      "jsonObjectResponse": "true",
      "maxContextToken": "128000",
      "maxOutputToken": "16834",
      "assistants": "true"
    },
    "provisioningState": "Updating",
    "rateLimits": [
      {
        "key": "request",
        "renewalPeriod": 10,
        "count": 300
      }
    ]
  },
  "systemData": {
    "createdBy": "docs@contoso.com",
    "createdByType": "User",
    "createdAt": "2025-01-28T02:57:15.8951706Z",
    "lastModifiedBy": "docs@contoso.com",
    "lastModifiedByType": "User",
    "lastModifiedAt": "2025-01-29T15:35:53.082912Z"
  },
  "etag": "\"GUID\""
}
```

> [!NOTE]
> There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account?view=azure-cli-latest#az-account-get-access-token&preserve-view=true). You can use this token as your temporary authorization token for API testing.

### Multi-deployment migrations for provisioned deployments

Multi-deployment migrations allow you to have greater control over the model migration process. With multi-deployment migrations, you can dictate how quickly you would like to migrate your existing traffic to the target model version or model family on a new provisioned deployment. The process to migrate to a new model version or model family using the multi-deployment migration approach is as follows:
- Create a new provisioned deployment. For this new deployment, you can choose to maintain the same provisioned deployment type as your existing deployment or select a new deployment type if desired.
- Transition traffic from the existing provisioned deployment to the newly created provisioned deployment with your target model version or model family until all traffic is offloaded from the original deployment. 
- Once traffic is migrated over to the new deployment, validate that there are no inference requests being processed on the previous provisioned deployment by ensuring the Azure OpenAI Requests metric doesn't show any API calls made within 5-10 minutes of the inference traffic being migrated over to the new deployment. For more information on this metric, [see the Monitor Azure OpenAI documentation](https://aka.ms/aoai/docs/monitor-azure-openai).
- Once you confirm that no inference calls have been made, delete the original provisioned deployment.

## Troubleshooting

### You get 401 or 403 responses from the Azure Resource Manager API

- Confirm your access token is valid and unexpired.
- Confirm you have permission to read and update deployments for the resource. 

