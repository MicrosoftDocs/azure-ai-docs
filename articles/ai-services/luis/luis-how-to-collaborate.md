---
title: Collaborate with others - LUIS
titleSuffix: Azure AI services
description: An app owner can add contributors to the authoring resource. These contributors can modify the model, train, and publish the app.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.topic: how-to
ms.date: 06/12/2025
---

# Add contributors to your app

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]


An app owner can add contributors to apps. These contributors can modify the model, train, and publish the app. _Contributors_ are managed in the Azure portal for the authoring resource, using the **Access control (IAM)** page. Add a user, using the collaborator's email address and the _contributor_ role.

## Add contributor to Azure authoring resource

You have migrated if your LUIS authoring experience is tied to an Authoring resource on the **Manage -> Azure resources** page in the LUIS portal.

In the Azure portal, find your Language Understanding (LUIS) authoring resource. It has the type `LUIS.Authoring`. In the resource's **Access Control (IAM)** page, add the role of **contributor** for the user that you want to contribute. For detailed steps, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

## View the app as a contributor

After you have been added as a contributor, [sign in to the LUIS portal](how-to/sign-in.md).

[!INCLUDE [switch azure directories](includes/switch-azure-directories.md)]

### Users with multiple emails

If you add contributors to a LUIS app, you are specifying the exact email address. While Microsoft Entra ID allows a single user to have more than one email account used interchangeably, LUIS requires the user to sign in with the email address specified when adding the contributor.

<a name="owner-and-collaborators"></a>

<a name='azure-active-directory-resources'></a>

### Microsoft Entra resources

If you use [Microsoft Entra ID](/azure/active-directory/) (Microsoft Entra ID) in your organization, Language Understanding (LUIS) needs permission to the information about your users' access when they want to use LUIS. The resources that LUIS requires are minimal.

You see the detailed description when you attempt to sign up with an account that has admin consent or does not require admin consent, such as administrator consent:

* Allows you to sign in to the app with your organizational account and let the app read your profile. It also allows the app to read basic company information. This gives LUIS permission to read basic profile data, such as user ID, email, name
* Allows the app to see and update your data, even when you are not currently using the app. The permission is required to refresh the access token of the user.


<a name='azure-active-directory-tenant-user'></a>

### Microsoft Entra tenant user

LUIS uses standard Microsoft Entra consent flow.

The tenant admin should work directly with the user who needs access granted to use LUIS in the Microsoft Entra ID.

* First, the user signs into LUIS, and sees the pop-up dialog needing admin approval. The user contacts the tenant admin before continuing.
* Second, the tenant admin signs into LUIS, and sees a consent flow pop-up dialog. This is the dialog the admin needs to give permission for the user. Once the admin accepts the permission, the user is able to continue with LUIS. If the tenant admin will not sign in to LUIS, the admin can access [consent](https://account.activedirectory.windowsazure.com/r#/applications) for LUIS. On this page you can filter the list to items that include the name `LUIS`.

If the tenant admin only wants certain users to use LUIS, there are a couple of possible solutions:
* Giving the "admin consent" (consent to all users of the Microsoft Entra ID), but then set to "Yes" the "User assignment required" under Enterprise Application Properties, and finally assign/add only the wanted users to the Application. With this method, the Administrator is still providing "admin consent" to the App, however, it's possible to control the users that can access it.
* A second solution is to use the [Microsoft Entra identity and access management API in Microsoft Graph](/graph/azuread-identity-access-management-concept-overview) to provide consent to each specific user.

Learn more about Microsoft Entra users and consent:
* [Restrict your app](/azure/active-directory/develop/howto-restrict-your-app-to-a-set-of-users) to a set of users

## Next steps

* Learn [how to use versions](luis-how-to-manage-versions.md) to control your app life cycle.
* Understand the about [authoring resources](luis-how-to-azure-subscription.md) and [adding contributors](luis-how-to-collaborate.md) on that resource.
* Learn [how to create](luis-how-to-azure-subscription.md) authoring and runtime resources