---
title: "Quickstart - Deploy a hosted agent with browser automation"
description: "Step-by-step guide to setting up and running the browser automation sample in Hosted Agents."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/11/2026
author: Abhinav-Premsekhar
reviewer: lindazqli
ms.author: apremsekhar
ms.reviewer: zhuoqunli
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-browser-tool
#CustomerIntent: As a developer building AI agents, I want to automate web browsing tasks so that my agents can interact with external websites and extract information.
---

# Getting started with Browser automation tool (preview) in Hosted agents
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

## Prerequisites
- An Azure account with an active subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn_8302daa3-997f-d193-0f14-db5b4342a668) before you begin.
- Your Azure account needs the [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner) or [Contributor](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#contributor) roles on a resource group.
- Azure Developer CLI. If you don't have Azure Developer CLI, see Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows).
    - The `azd ai agent extension` installed (`azd extension install azure.ai.agents`). If you don't have the extension installed, when you initialize the starter template or run `azd ai agent` the extension is installed automatically.

## Step 1: Create a Playwright Workspace

To use the browser automation tool, you first need to create a [Playwright workspace](https://aka.ms/pww/docs). (If you have an existing Playwright Workspace, you can skip this step.)

1. Sign in to the [Azure portal](https://portal.azure.com/) by using the credentials for your Azure subscription.
2. From the portal Home page, search for and select [Playwright Workspaces](https://aka.ms/pww/docs/manage-workspaces).
3. Select Create and enter the following information:
    - Subscription
    - Resource group
    - Name
    - Location
4. Select Review + Create and then select Create. It takes a few minutes to create the workspace. Wait for the portal page to display Your deployment is complete before moving on.

## Step 2: Deploy the sample hosted agent 

To get started with browser automation tool in hosted agents, we have two samples –
- [Microsoft Agent Framework](https://github.com/microsoft-foundry/foundry-samples-pr/tree/main/samples/python/hosted-agents/agent-framework/responses/14-browser-automation-agent)
- [Bring-your-own Framework](https://github.com/microsoft-foundry/foundry-samples-pr/tree/main/samples/python/hosted-agents/bring-your-own/responses/browser-automation)

You can use any one of these depending on which framework you want to use to build your hosted agent.

### Step 2.1: Scaffold the sample hosted agent application

1. Open a new directory and initialize the agent sample by running the command –
    - Microsoft Agent Framework - 
    ```
    azd ai agent init -m “https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/14-browser-automation-agent/agent.manifest.yaml”
    ```

    - Bring-your-own Framework -
    ```
    azd ai agent init -m “https://github.com/microsoft-foundry/foundry-samples-pr/blob/main/samples/python/hosted-agents/bring-your-own/responses/browser-automation/agent.manifest.yaml”
    ```

2. The interactive flow will prompt for the following details -
    - **App directory**: The local path to initialize the application.
    - **Agent name**: Customize the name or accept the default, browser-automation-agent-sample-foundry. (Name should be within 1-63 characters, should start and end with a letter or number, and contain only letters, numbers, and internal hyphens)
    - **Foundry project**: Select an existing Foundry project or create a new project. (If you’re using an existing Foundry project, you must have the **Foundry Project Manager** role at project scope or another role that grants both data-plane and role-assignment permissions. For the full role matrix, see [Hosted agent permissions reference](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-permissions))
    - **Model**: Select the default, gpt-4.1, or another model you can access.
    - **Model version**: Select the default option.
    - **Model SKU**: Select an option with available quota that isn't Batch, usually Standard or GlobalStandard
    - **Deployment capacity**: Select the default, 10
    - **Deployment name**: Select the default, gpt-4.1
    - **Playwright Workspace access token**: Enter the access token (or [generate a workspace access token](https://learn.microsoft.com/azure/app-testing/playwright-workspaces/how-to-manage-access-tokens#generate-a-workspace-access-token))
    - **Playwright Workspace resource ID**: To get the resource ID, open the Playwright Workspace resource, go to Overview page, select JSON View and copy the Resource ID.
    - **Playwright Workspace service URL**: To get the service URL, open the Playwright Workspace resource and go to Overview page, copy the Browser endpoint (it starts with wss://).

Once the application is successfully initialized, you’ll get the following message – 
```console
AI agent definition added to your azd project successfully!
```

### Step 2.2: Provision the Azure resources

Provision the resources defined in azure.yaml:
```
azd provision
```

This step takes a few minutes and creates the following resources. After provisioning, you’ll see the following message –
```console
SUCCESS: Your application was provisioned in Azure in X minute YY seconds.
```

### Step 2.3: Deploy the agent to Foundry Agent Service

Build and deploy the agent container:
```
azd deploy
```

When the agent is deployed, you'll see the following message -
```console
SUCCESS: Your application was deployed to Azure in X minutes YY seconds.
```

## Step 3: Test the agent in the Foundry Playground

1.	Open the [Foundry portal](https://ai.azure.com/) and sign in.
2.	Select your project from Recent projects or All projects.
3.	In the left navigation, select Build > Agents.
4.	Select your agent, then select Open in playground.
5.	Enter a prompt such as -
```
Go to the website finance.yahoo.com, search for MSFT and report the Microsoft stock price.
```

## Step 4: Clean up resources

Delete the resources when you're finished so you stop incurring charges.
```
azd down
```
azd lists the resources it deletes and prompts for confirmation. Cleanup takes about 2-5 minutes.
