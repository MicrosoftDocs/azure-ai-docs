---
title: Troubleshoot evaluation and observability issues - Microsoft Foundry
description: Learn how to troubleshoot common issues with evaluations and observability in Microsoft Foundry, including storage account access, RBAC, and network configuration.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: naposani
ms.service: microsoft-foundry
ms.topic: troubleshooting
ms.date: 06/16/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to troubleshoot common evaluation and observability issues in Microsoft Foundry so that I can resolve problems quickly.
---

# Troubleshoot evaluation and observability issues

This article provides information to help you solve common issues you might encounter when you use evaluation and observability features in Microsoft Foundry. Some issues relate to storage account configuration, role-based access control (RBAC), or network settings for the Foundry project. Other issues happen while an evaluation runs, such as authentication failures, model capacity or quota limits, data format problems, or missing scores.

## Storage account not linked to the Foundry project

Evaluation features require a storage account linked to your Foundry project through a connection. If the storage account isn't connected, evaluations fail because the service can't read or write evaluation data.

**Symptoms:**

- Evaluations fail with errors related to storage access or missing storage configuration.
- The evaluation service can't upload evaluation results or download datasets.

### Connect a storage account to the Foundry project

Connect your storage account to the Foundry project by creating an Azure Blob Storage connection. For step-by-step instructions, see [Add a new connection to your project](../../how-to/connections-add.md).

You can authenticate the connection by using either an **account key** or **Microsoft Entra ID** (recommended). If you use Entra ID, see [Missing RBAC role assignment for Entra ID authentication](#missing-rbac-role-assignment-for-entra-id-authentication) to configure the required permissions.

For more details on bringing your own storage for evaluations, see [Rate limits, region support, and enterprise features for evaluation](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage).

## Missing RBAC role assignment for Entra ID authentication

If you connect your storage account by using Microsoft Entra ID authentication, the Foundry project's managed identity must have the **Storage Blob Data Contributor** role on the storage account. Without this role, the service can't read or write blob data and evaluations fail.

**Symptoms:**

- Evaluations fail with `403 Forbidden` or `AuthorizationPermissionMismatch` errors.
- You see errors indicating insufficient permissions to access the storage account.
- Storage operations time out or are denied.

### Verify the managed identity role assignment

Use the following Azure CLI commands to check whether the correct RBAC role is assigned to the Foundry project's managed identity on the storage account.

First, retrieve the managed identity principal ID for your Foundry project:

```azurecli
az resource show \
  --resource-group <your-resource-group> \
  --name <your-foundry-account-name> \
  --resource-type "Microsoft.CognitiveServices/accounts" \
  --query "identity.principalId" \
  --output tsv
```

Then, list the role assignments on the storage account and filter for the managed identity:

```azurecli
az role assignment list \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>" \
  --assignee <principal-id> \
  --output table
```

Verify that the output includes a role assignment with `RoleDefinitionName` set to **Storage Blob Data Contributor** (or **Storage Blob Data Owner**).

### Assign the Storage Blob Data Contributor role

If the role assignment is missing, assign the **Storage Blob Data Contributor** role to the Foundry project's managed identity:

```azurecli
az role assignment create \
  --assignee <principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
```

> [!NOTE]
> Role assignments can take up to 10 minutes to propagate. Wait a few minutes after assigning the role before retrying the evaluation.

## Storage account network access restrictions

When you use Microsoft Entra ID authentication, the storage account must have public network access enabled. If network access is restricted, the Foundry evaluation service might not be able to reach the storage account.

**Symptoms:**

- Evaluations fail with network-related errors or timeouts.
- You see `403 Forbidden` errors even though RBAC roles are correctly assigned.
- Connections to the storage account are refused.

### Verify the storage account network configuration

Use the following Azure CLI command to check the network access settings of your storage account:

```azurecli
az storage account show \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --query "{publicNetworkAccess: publicNetworkAccess, defaultAction: networkRuleSet.defaultAction, virtualNetworkRules: networkRuleSet.virtualNetworkRules, ipRules: networkRuleSet.ipRules}" \
  --output json
```

Check the output for the following values:

| Property | Expected value | Description |
|---|---|---|
| `publicNetworkAccess` | `Enabled` | Public network access must be enabled. |
| `defaultAction` | `Allow` | The default network rule should allow access. |

If `publicNetworkAccess` is set to `Disabled` or `defaultAction` is set to `Deny`, the evaluation service can't reach the storage account. 

> [!NOTE]
> For virtual network based (network-isolated) agent setups where resources are expected to operate with public network access disabled and rely on private endpoints connectivity virtual network instead, see [Set up private networking](../../agents/how-to/virtual-networks.md).

### Enable public network access

Enable public network access on the storage account:

```azurecli
az storage account update \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --public-network-access Enabled
```

If you need to keep the firewall enabled but allow access, set the default action to **Allow**:

```azurecli
az storage account update \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --default-action Allow
```

> [!IMPORTANT]
> Enabling public network access or setting the default action to **Allow** makes the storage account accessible from all networks. Evaluate this change against your organization's security requirements.

## Troubleshooting checklist

Use this checklist to quickly verify your evaluation setup:

1. **Storage connection exists**: Confirm that an Azure Blob Storage connection is configured in your Foundry project. Navigate to **Build** > **Tools** in the Foundry portal to check.

1. **Authentication type**: Identify whether the connection uses an account key or Microsoft Entra ID. If Entra ID, complete the remaining checks.

1. **RBAC role assigned**: Verify that the Foundry project's managed identity has the **Storage Blob Data Contributor** role on the storage account.

   ```azurecli
   az role assignment list \
     --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>" \
     --assignee <principal-id> \
     --query "[].{Role:roleDefinitionName, Principal:principalId}" \
     --output table
   ```

1. **Network access**: Verify that the storage account has public network access enabled.

   ```azurecli
   az storage account show \
     --resource-group <resource-group> \
     --name <storage-account-name> \
     --query "publicNetworkAccess" \
     --output tsv
   ```

1. **Propagation delay**: If you recently made RBAC or network changes, wait at least 10 minutes before retrying.

## Evaluation run is slow, stuck, or fails with capacity or quota errors

An evaluation run might stay in the **Running** or pending state for a long time, run slowly, or fail with quota errors. This condition usually happens when the judge model deployment doesn't have enough capacity, so the service throttles or retries requests.

**Symptoms:**

- The run stays in the **Running** or pending state much longer than expected.
- The run fails with a `429 Too Many Requests` error.
- You see errors that mention quota or rate limits.

**Resolution:**

- Confirm the judge model deployment has enough quota. The judge model used for AI-assisted evaluators counts against your Azure OpenAI quota.
- Increase the tokens-per-minute (TPM) quota for the model deployment in the Azure portal, then run the evaluation again.
- Reduce the size of your dataset, or split it into smaller batches. For simulations, decrease the maximum turns per conversation.
- Use a smaller or lower-cost judge model deployment for faster, cheaper runs.
- For a stuck SDK run, cancel it with `client.evals.runs.cancel(run_id, eval_id=eval_id)`, increase capacity, then resubmit.
- For a `429` error, check the `retry-after` header for the recommended wait time, and use exponential backoff when you retry.

## Authentication or authorization errors (401 or 403)

If an evaluation fails with a `401 Unauthorized` or `403 Forbidden` error that isn't related to storage, the cause is usually project authentication or a missing role assignment.

> [!NOTE]
> If the `403` error mentions blob or storage access, see [Missing RBAC role assignment for Entra ID authentication](#missing-rbac-role-assignment-for-entra-id-authentication) instead.

**Resolution:**

- Verify that `DefaultAzureCredential` is configured correctly. If you use the Azure CLI, run `az login`. If you use the Azure Developer CLI, run `azd auth login`.
- Confirm your account has the **Foundry User** role on the Foundry project.
- Verify the project endpoint URL is correct and includes both the account and project names.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

## Data format or field mapping errors

If an evaluation fails with a schema, data mapping, or field mapping error, the test data doesn't match what the evaluators expect.

**Resolution:**

- Verify your JSONL file has exactly one valid JSON object per line.
- Confirm that the field names in your data mapping match the field names in your dataset exactly. Field names are case-sensitive.
- Check that the schema you define, such as `item_schema` in the SDK, matches the fields in your dataset.
- For portal evaluations, verify your dataset contains the required columns for the evaluation scope. For conversation evaluations, make sure the **messages** column contains properly formatted chat messages.
- If you evaluate at the conversation level, remove turn-only evaluators or switch to turn-level evaluation. A turn-only evaluator used with conversation-level evaluation causes an incompatible evaluation level error.

## Missing or zero evaluator scores

After a run completes, some evaluator scores might be missing or unexpectedly zero.

| Symptom | Possible cause | Action |
|---|---|---|
| An evaluator's metric is missing | The evaluator wasn't selected when the evaluation was created | Rerun the evaluation and select the required evaluators. |
| All safety metrics are zero | The safety category is disabled, or the model doesn't support the evaluator | Confirm model and evaluator support in [Risk and safety evaluators](../../concepts/built-in-evaluators.md#risk-and-safety-evaluators). |
| Groundedness is unexpectedly low | The retrieval context is incomplete | Verify how context is constructed, and check retrieval latency. |
| Many rows show errors or low scores | Agent response or evaluator errors during the run | Open the run report, review the errored rows, fix the underlying errors, then rerun. |

## Agent evaluator tool errors

If an agent evaluator returns an error for unsupported tools:

- Check the [supported tools](../../concepts/evaluation-evaluators/agent-evaluators.md#supported-tools) for agent evaluators.
- As a workaround, wrap unsupported tools as user-defined function tools so the evaluator can assess them.

## Azure Developer CLI (azd) evaluation issues

These issues apply when you run agent evaluations with the `azd ai agent eval` commands.

| Issue | Solution |
|---|---|
| `azd ai agent eval` command not found or fails | Run `azd ext list` and verify the `azd ai agent` extension is 0.1.40-preview or later. Upgrade with `azd ext upgrade azure.ai.agents`. |
| Evaluation target not found or agent not invokable | Confirm the agent is deployed and invokable with `azd ai agent show`. Redeploy with `azd deploy` if needed. |
| Eval model deployment not found | Verify the chat-completion deployment name exists in your project under **Build** > **Deployments**. |

For the full azd evaluation workflow, see [Run agent evaluations with the azd CLI](azure-developer-cli-evaluation.md).

## Trace evaluation issues

[Trace evaluation](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview) runs evaluators against agent interactions that Application Insights already captured, instead of replaying requests. 

### Project managed identity is missing trace read permissions

The Foundry project's managed identity reads traces from Application Insights. Without the right role, the service can't query traces, and the trace evaluation returns no data or fails.

**Symptoms:**

- Trace evaluation fails with a permission or authorization error.
- The run finds no traces even though traces exist in Application Insights.

**Resolution:**

Assign the **Log Analytics Reader** role to the project's managed identity on *both* the Application Insights resource and its linked Log Analytics workspace. To find the managed identity principal ID, see [Verify the managed identity role assignment](#verify-the-managed-identity-role-assignment).

```azurecli
az role assignment create \
  --assignee <principal-id> \
  --role "Log Analytics Reader" \
  --scope "<application-insights-or-log-analytics-resource-id>"
```

Run the command twice: once for the Application Insights resource and once for the Log Analytics workspace it's linked to. Role assignments can take up to 10 minutes to propagate. For setup details, see [Set up tracing in Microsoft Foundry](trace-agent-setup.md).

> [!NOTE]
> If the Log Analytics tables that store your traces are [protected](/azure/azure-monitor/logs/protected-tables-configure) (their protection level is set to **Protected**), the Log Analytics Reader role can't read them. In that case, also assign the [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader) role to the managed identity at the same scopes so trace evaluation can read the protected trace tables.

### Fetched traces have no input or output messages

Quality evaluators read the query and response from each trace. If the fetched `invoke_agent` spans have neither the `gen_ai.input.messages` nor the `gen_ai.output.messages` attribute, the evaluators have no conversation content to score.

**Symptoms:**

- Quality evaluators, such as coherence, fluency, relevance, and intent resolution, return `score=None`.
- Safety evaluators run but don't produce meaningful results.

**Cause:** The agent doesn't emit the GenAI message attributes on its `invoke_agent` spans, so the captured traces don't contain the conversation content. The evaluation service only reads spans where `gen_ai.operation.name` equals `invoke_agent`.

**Resolution:**

- Make sure your agent emits OpenTelemetry spans that follow the [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/), including the `gen_ai.input.messages` and `gen_ai.output.messages` attributes on `invoke_agent` spans.
- For Python agents built with the Azure AI Agent Server SDK, install the tracing extra so spans are emitted automatically:

  ```bash
  pip install "azure-ai-agentserver-core[tracing]"
  ```

- In Application Insights, confirm the `invoke_agent` spans include the message attributes before you rerun the evaluation.

## Human evaluation

This section covers common issues with the human evaluation feature for Foundry agents.

### Feedback button doesn't appear after the agent responds

**Cause:** No evaluation template is set as active for the agent.

**Resolution:** In the **Human Evaluation** tab, select **Set as active** for the desired template. Only one template can be active at a time. For more information, see [Set up human evaluation for your agents](human-evaluation.md#manage-your-evaluation-templates).

### No results visible in the Evaluation Results section

**Cause:** Application Insights isn't configured for the project, or there's a data ingestion delay (up to 5 minutes after an evaluation is submitted).

**Resolution:** Verify that Application Insights is connected to your project. For setup instructions, see [Configure Application Insights for agent tracing](trace-agent-setup.md). If Application Insights is already configured, wait a few minutes and refresh the page.

### Reviewer can't access the preview web app

**Cause:** The reviewer doesn't have the required role on the Foundry project.

**Resolution:** Assign the **Foundry User** role to the reviewer on the Foundry project. For instructions, see [Role-based access control in Microsoft Foundry](../../concepts/rbac-foundry.md).

## Related content

- [Add a new connection to your project](../../how-to/connections-add.md)
- [Connect to your own storage](../../how-to/bring-your-own-azure-storage-foundry.md)
- [Rate limits, region support, and enterprise features for evaluation](../../concepts/evaluation-regions-limits-virtual-network.md)
- [Evaluate your AI agents](evaluate-agent.md)
- [Run agent evaluations with the azd CLI](azure-developer-cli-evaluation.md)
- [Run evaluations from the Foundry portal](../../how-to/evaluate-generative-ai-app.md)
- [View evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Set up human evaluation for your agents](human-evaluation.md)
