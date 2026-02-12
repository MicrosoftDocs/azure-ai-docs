---
title: 'Integrate Azure OpenAI with Weights & Biases'
titleSuffix: Azure OpenAI
description: Learn how to integrate Weights & Biases and Azure OpenAI fine-tuning.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
---

# Integrate Azure OpenAI fine-tuning with Weights & Biases (preview)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Weights & Biases (W&B) is a powerful AI developer platform that enables machine learning practitioners to train, fine-tune, and deploy models efficiently. Azure OpenAI fine-tuning integrates with W&B, allowing you to track metrics, parameters, and visualize your Azure OpenAI fine-tuning training runs within your W&B projects. In this article, we will guide you through setting up the Weights & Biases integration.

:::image type="content" source="../media/how-to/weights-and-biases/dashboards.png" alt-text="Screenshot of the weights and biases dashboards." lightbox="../media/how-to/weights-and-biases/dashboards.png":::

## Prerequisites

- An Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md). The resource should be in a [region that supports fine-tuning](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).
- Ensure all team members who need to fine-tune models have **Azure AI User** access assigned for the new Azure OpenAI resource.
- A [Weights & Biases](https://wandb.ai) account and API key.
- [Azure Key Vault](https://portal.azure.com/#create/Microsoft.KeyVault). For more information on creating a key vault, see the [Azure Key Vault quickstart](/azure/key-vault/general/quick-create-portal).

## Enable System Managed Identity

First, enable [System Managed Identity](/entra/identity/managed-identities-azure-resources/overview) for your Azure OpenAI resource.

:::image type="content" source="../media/how-to/weights-and-biases/system-managed.png" alt-text="Screenshot of the system managed identity interface." lightbox="../media/how-to/weights-and-biases/system-managed.png":::

## Retrieve Weights & Biases API key

Sign in to [https://wandb.ai](https://wandb.ai) and go to the [User Settings](https://wandb.ai/settings).

Under **API Keys**, select **Reveal** to access your key and copy it to the clipboard.

:::image type="content" source="../media/how-to/weights-and-biases/reveal-key.png" alt-text="Screenshot of API keys section of User Settings user experience." lightbox="../media/how-to/weights-and-biases/reveal-key.png":::

If you would like to create a new key, use [https://wandb.ai/authorize](https://wandb.ai/authorize), and copy the key to add to your integration configuration later.

## Configure Azure Key Vault

To securely send data from Azure OpenAI to your Weights & Biases projects, you'll need to use [Azure Key Vault](/azure/key-vault/general/overview).

### Add your Weights & Biases API key as a Secret to your Azure Key Vault

1. Navigate to the Azure Key Vault you are planning to use.
2. To read and write secrets to your Azure Key Vault, you must explicitly assign access.
3. Go to **Settings** > **Access** configuration. Under **Permission** model, we recommend you select Azure role-based access control if this isn't already selected. Learn more about [Azure role-based access control](/azure/role-based-access-control/overview?WT.mc_id=Portal-Microsoft_Azure_KeyVault).

    :::image type="content" source="../media/how-to/weights-and-biases/role-based-access-control.png" alt-text="Screenshot of key vault access configuration user interface." lightbox="../media/how-to/weights-and-biases/role-based-access-control.png":::

### Assign Key Vault Secrets Officer role

Now that you have set your permission model to Azure role-based access control, you can give yourself the **Key Vault Secrets Officer** role.

1. Go to **Access control (IAM)** and then **Add role assignment**

    :::image type="content" source="../media/how-to/weights-and-biases/access-control.png" alt-text="Screenshot of the access control add role assignment user experience." lightbox="../media/how-to/weights-and-biases/access-control.png":::

2. Choose **Key Vault Secrets Officer**, add your account as a member, and select **review & assign**.

    :::image type="content" source="../media/how-to/weights-and-biases/key-vault-secret-officer.png" alt-text="Screenshot of the key vault secret officer role assignment." lightbox="../media/how-to/weights-and-biases/key-vault-secret-officer.png":::

### Create secrets

1. From within your key vault resource under **Objects**, select **Secrets** > **Generate/Import**.

    :::image type="content" source="../media/how-to/weights-and-biases/secrets.png" alt-text="Screenshot of the key vault secrets user interface." lightbox="../media/how-to/weights-and-biases/secrets.png":::

2. Provide a name for your secret and save the generated Weights & Biases API key to the **secret value**.

    :::image type="content" source="../media/how-to/weights-and-biases/create-secret.png" alt-text="Screenshot of the key vault secrets creation user interface." lightbox="../media/how-to/weights-and-biases/create-secret.png":::

3. Make sure to capture the secret name and key vault URL. The key vault URL can be retrieved from **Overview** section of your key vault.

### Give your Key Vault permission on your Azure OpenAI account

If you used a Vault Access policy earlier to read and write secrets to your Azure Key Vault, you should use that again. Otherwise, continue to use Azure role-based access control. **We recommend Azure role-based access control. However, if it does not work for you, please try Vault Access policy.**

Give your Azure OpenAI resource the **Key Vault Secrets Officer** role.

:::image type="content" source="../media/how-to/weights-and-biases/assign.png" alt-text="Screenshot of the assign managed identity user interface." lightbox="../media/how-to/weights-and-biases/assign.png":::

## Link Weights & Biases with Azure OpenAI

1. Navigate to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) and select your Azure OpenAI fine-tuning resource.

    :::image type="content" source="../media/how-to/weights-and-biases/manage-integrations.png" alt-text="Screenshot of the manage integrations button." lightbox="../media/how-to/weights-and-biases/manage-integrations.png":::

2. Add your key vault URL and secret. Then, select **Update**.

    :::image type="content" source="../media/how-to/weights-and-biases/integration.png" alt-text="Screenshot of the manage integrations for Weights and Biases user experience." lightbox="../media/how-to/weights-and-biases/integration.png":::

3. Now, when you create new fine-tuning jobs, you'll have the option to log data from the job to your Weights & Biases account.

    :::image type="content" source="../media/how-to/weights-and-biases/dashboards.png" alt-text="Screenshot of the weights and biases dashboards." lightbox="../media/how-to/weights-and-biases/dashboards.png":::
