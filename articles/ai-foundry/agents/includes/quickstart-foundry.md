---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: include
ms.date: 07/11/2025
---

## Prerequisites
- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope, which will grant the necessary permissions for creating the project
    * Alternatively, having the **Contributor** or **Owner** role at the subscription level will allow the creation of the project
- Once the project is created, ensure that the individual creating the agent within the project has the **Azure AI User** role at the project level


> [!IMPORTANT]
> The Microsoft Foundry portal only supports basic agent setup at this time. If you want to perform a standard agent setup, see the [Environment setup](../environment-setup.md) article to learn about more.

## Create a Foundry account and project in Foundry portal

To create an account and project in Foundry, follow these steps:

1. Go to Foundry. If you are in a project, select Foundry at the top left of the page to go to the Home page.

1. Use the Agent getting started creation flow for the fastest experience. Click **Create an agent**.

    :::image type="content" source="../media\quickstart\foundry-landing-page.png" alt-text="A screenshot of the Foundry portal." lightbox="../media\quickstart\foundry-landing-page.png":::


1. Enter a name for the project. If you want to customize the default values, select **Advanced options**.

    :::image type="content" source="../media\quickstart\create-project.png" alt-text="A screenshot of the advanced options for creating a project." lightbox="../media\quickstart\create-project.png":::

1. Select **Create**.

1. Wait for your resources to be provisioned.
    1. An account and project (child resource of your account) will be created.
    1. The gpt-4o model will automatically be deployed
    1. A default agent will be created

1. Once complete, you will land directly in the agent playground and you can start creating agents. You can give your agent instructions on what to do and how to do it. For example: *"You are a helpful agent that can answer questions about geography."* Then you can start chatting with your agent.

    :::image type="content" source="../media\quickstart\agent-playground.png" alt-text="Screenshot of the agent playground." lightbox="../media\quickstart\agent-playground.png":::

    > [!NOTE]
    > If you are getting permission error when trying to configure or create agents ensure you have the **Azure AI User** on the project.
