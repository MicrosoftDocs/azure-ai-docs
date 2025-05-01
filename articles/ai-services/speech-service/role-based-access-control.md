---
title: Role-based access control for Speech resources
titleSuffix: Azure AI services
description: Learn how to assign access roles for an AI Services resource for Speech.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 11/19/2024
ms.author: eur
# Customer intent: As a developer, I want to learn how to assign access roles for an AI Services resource for Speech.
---

# Role-based access control for Speech resources

You can manage access and permissions to your Speech resources with Azure role-based access control (Azure RBAC). Assigned roles can vary across Speech resources. For example, you can assign a role to an AI Services resource for Speech that should only be used to train a custom speech model. You can assign another role to an AI Services resource for Speech that is used to transcribe audio files. Depending on who can access each Speech resource, you can effectively set a different level of access per application or user. For more information on Azure RBAC, see the [Azure RBAC documentation](/azure/role-based-access-control/overview).

> [!NOTE]
> An AI Services resource for Speech can inherit or be assigned multiple roles. The final level of access to the resource is a combination of all role permissions.

## Roles for Speech resources

A role definition is a collection of permissions. When you create an AI Services resource for Speech, the built-in roles in the following table are available for assignment. 

> [!WARNING]
> Speech service architecture differs from other Azure AI services in the way it uses [Azure control plane and data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane). Speech service is extensively using data plane comparing to other Azure AI services, and this requires different set up for the roles. Because of this some general Cognitive Services roles have actual access right set that doesn't exactly match their name when used in Speech services scenario. For instance *Cognitive Services User* provides in effect the Contributor rights, while *Cognitive Services Contributor* provides no access at all. The same is true for generic *Owner* and *Contributor* roles which have no data plane rights and consequently provide no access to Speech resource. To keep consistency we recommend to use roles containing *Speech* in their names. These roles are *Cognitive Services Speech User* and *Cognitive Services Speech Contributor*. Their access right sets were designed specifically for the Speech service. In case you would like to use general Cognitive Services roles and Azure generic roles, we ask you to very carefully study the following access right table.

| Role | Can list resource keys | Access to data, models, and endpoints in custom projects| Access to speech transcription and synthesis APIs
| ---| ---| ---| ---|
|**Owner** |Yes |None |No |
|**Contributor** |Yes |None |No |
|**Cognitive Services Contributor** |Yes |None |No |
|**Cognitive Services User** |Yes |View, create, edit, and delete |Yes |
|**Cognitive Services Speech Contributor** |No | View, create, edit, and delete |Yes |
|**Cognitive Services Speech User** |No |View only |Yes |
|**Cognitive Services Data Reader (Preview)** |No |View only |Yes |

> [!IMPORTANT]
> Whether a role can list resource keys is important for [Speech Studio authentication](#speech-studio-authentication). To list resource keys, a role must have permission to run the `Microsoft.CognitiveServices/accounts/listKeys/action` operation. Please note that if key authentication is disabled in the Azure portal, then none of the roles can list keys.

Keep the built-in roles if your Speech resource can have full read and write access to the projects. 

For finer-grained resource access control, you can [add or remove roles](/azure/role-based-access-control/role-assignments-portal?tabs=current) using the Azure portal. For example, you could create a custom role with permission to upload custom speech datasets, but without permission to deploy a custom speech model to an endpoint. 

## Authentication with keys and tokens

The [roles](#roles-for-speech-resources) define what permissions you have. Authentication is required to use the Speech resource. 

To authenticate with Speech resource keys, all you need is the key and region. To authenticate with a Microsoft Entra token, the Speech resource must have a [custom subdomain](speech-services-private-link.md#create-a-custom-domain-name).

Here's how to create a new Azure AI Services resource with a custom subdomain. You can also use an existing resource, but it must have a custom subdomain. For more information about creating a custom subdomain, see [Create a custom domain name](speech-services-private-link.md#create-a-custom-domain-name).

```bash
resourceGroupName=my-speech-rg
location=eastus
AIServicesResourceName=my-aiservices-$location

# create an AIServices resource for Speech and other AI services
az cognitiveservices account create --name $AIServicesResourceName --resource-group $resourceGroupName --kind AIServices --sku S0 --location $location --custom-domain $AIServicesResourceName

# get the resource id
speechResourceId=$(az cognitiveservices account show --name $AIServicesResourceName --resource-group $resourceGroupName --query id -o tsv)
# assign Cognitive Services User role to the app id
appId=$(az ad signed-in-user show --query id -o tsv)
az role assignment create --role "Cognitive Services User" --assignee $appId --scope $speechResourceId
# assign Cognitive Services Speech User role to the app id
az role assignment create --role "Cognitive Services Speech User" --assignee $appId --scope $speechResourceId

# get an access token
accessToken=$(az account get-access-token --scope "https://cognitiveservices.azure.com/.default" --query accessToken -o tsv)
echo $accessToken
```

The returned `accessToken` is a Microsoft Entra token that you can use to authenticate without API keys. The token has a [limited lifetime](/entra/identity-platform/configurable-token-lifetimes#access-tokens).

Now you can use the `accessToken` to authenticate with the AI Services resource. For example, you can use the token via the [Fast transcription REST API](./fast-transcription-create.md):

```bash
uri="https://$AIServicesResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15"

curl -v "$uri" \
    --header 'Content-Type: multipart/form-data' \
    --form 'definition={"locales": ["en-US"]}' \
    --form 'audio=@Call1_separated_16k_health_insurance.wav' \
    --header "Authorization: Bearer $accessToken" 
```

### Speech SDK authentication

For the SDK, you configure whether to authenticate with an API key or Microsoft Entra token. For details, see [Microsoft Entra authentication with the Speech SDK](how-to-configure-azure-ad-auth.md).

### Speech Studio authentication

Once you're signed into [Speech Studio](speech-studio-overview.md), you select a subscription and Speech resource. You don't choose whether to authenticate with an API key or Microsoft Entra token. Speech Studio gets the key or token automatically from the Speech resource. If one of the assigned [roles](#roles-for-speech-resources) has permission to list resource keys and the key authentication is not disabled, Speech Studio authenticates with the key. Otherwise, Speech Studio authenticates with the Microsoft Entra token.

If Speech Studio utilizes your Microsoft Entra token and your Speech resource lacks a properly configured custom subdomain, Role-based access control (RBAC) will not be activated, and you will be unable to access any features in Speech Studio. RBAC determines your access to features based on the role assigned to you and the permissions associated with that role. If your role does not grant access to a specific feature, a warning message will be displayed on the page. Ensure you have the appropriate role to access the desired feature.

| Authentication credential                      | Feature availability                                                |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| Speech resource key                            | Full access. Role configuration is ignored if resource key is used. |
| Microsoft Entra token with custom subdomain    | Full access limited only by the assigned role permissions.          |
| Microsoft Entra token without custom subdomain | No access.                       |

## Next steps

* [Microsoft Entra authentication with the Speech SDK](how-to-configure-azure-ad-auth.md).
* [Speech service encryption of data at rest](speech-encryption-of-data-at-rest.md).
