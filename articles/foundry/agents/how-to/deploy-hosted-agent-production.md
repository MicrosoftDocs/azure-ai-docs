---
title: "Promote hosted agents to production with the Azure Developer CLI"
description: "Promote Microsoft Foundry hosted agents across development, test, and production, then use canary deployments to release new versions gradually with azd."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/21/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Promote hosted agents to production with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Release your Microsoft Foundry hosted agent through development, test, and production environments with the Azure Developer CLI (`azd`). After validating a release in test, deploy it to production and gradually increase the new version's share of traffic. If you find a problem, route traffic back to the previous version.

This article builds on [Set up CI/CD for hosted agents](set-up-ci-cd-cli.md). It extends your existing pipeline with source-code deployment across environments and a gradual production rollout. The Bash commands work in GitHub Actions jobs and Azure DevOps pipeline stages.

Use `azd` to manage deployment and endpoint updates. Without it, you need to manage the Azure resources and deployment operations yourself through the portal, SDKs, or REST APIs.

## Promote releases across environments

Extend your single-environment CI/CD setup to promote releases from development to test, then to production. Use the same source revision in each environment. Bind each environment to a separate existing Foundry project. Environment names alone don't isolate Azure resources.

> [!NOTE]
> Package and deploy the source code separately for each environment instead of sharing one build artifact. Promote the tested source revision and dependency files. An unchanged deployment can reuse an existing agent version.

### Configure each environment

Keep your existing source-code agent configuration in `azure.yaml`. Use `${FOUNDRY_PROJECT_ENDPOINT}` for the project service's `endpoint`, and environment-variable references for model deployment and connection names. See [Azure YAML configuration](../concepts/azure-yaml-reference.md).

1. From the directory containing `azure.yaml`, create any missing environments. Skip environments you already configured, and use each target project's subscription and region:

   ```bash
   azd env new development --subscription "<dev-subscription-id>" \
     --location "<dev-region>" --no-prompt
   azd env new test --subscription "<test-subscription-id>" \
     --location "<test-region>" --no-prompt
   azd env new production --subscription "<prod-subscription-id>" \
     --location "<prod-region>" --no-prompt
   ```

   Reference: [azd env new](/azure/developer/azure-developer-cli/reference#azd-env-new).

1. Run this block for `development`, `test`, and `production`, replacing the values for each target. Keep any additional model, connection, and runtime settings specific to that environment:

   ```bash
   TARGET_ENV="test"

   azd env set AZURE_TENANT_ID "<tenant-id>" -e "$TARGET_ENV"
   azd env set AZURE_RESOURCE_GROUP "<resource-group>" -e "$TARGET_ENV"
   azd env set AZURE_AI_PROJECT_ID "<project-resource-id>" -e "$TARGET_ENV"
   azd env set FOUNDRY_PROJECT_ENDPOINT "<project-endpoint>" -e "$TARGET_ENV"
   azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "<model-name>" -e "$TARGET_ENV"
   ```

   Reference: [azd env set](/azure/developer/azure-developer-cli/reference#azd-env-set).

    Use the full project ARM resource ID and its matching endpoint. Each project needs its own dependencies and deployment permissions; switching environments doesn't copy these resources or permissions.

### Deploy and test the release

Use the following sequence in either CI/CD provider. Replace `my-agent` with your service name; these examples use the Responses protocol.

1. Deploy and test in `development`:

    ```bash
    TARGET_ENV="development"
    azd deploy my-agent -e "$TARGET_ENV" --no-prompt
    azd ai agent show my-agent -e "$TARGET_ENV" --output json --no-prompt
    azd ai agent invoke my-agent "<feature-test-prompt>" \
      -e "$TARGET_ENV" --protocol responses \
      --new-session --new-conversation --no-prompt
    ```

    Reference: [azd deploy](/azure/developer/azure-developer-cli/reference#azd-deploy), [Invoke a hosted agent](invoke-hosted-agent.md).

    Confirm that the agent returns the expected result, and record the source commit.

1. Check out the same commit in the test job or stage. Repeat the commands with `TARGET_ENV="test"`, then run your regression and integration tests. If code or dependencies change, repeat both environments' checks.

1. After approval, use the same commit in the production job or stage. Follow [Roll out a production version gradually](#roll-out-a-production-version-gradually) before deploying to keep the stable version serving traffic.

### Apply the stages in your pipeline

Extend your existing pipeline with the sequence above:

- **GitHub Actions:** Use dependent jobs for development, test, and production. Scope variables and secrets to each GitHub environment, and configure [environment protection rules](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) for production approval.
- **Azure DevOps:** Use dependent stages with deployment jobs targeting development, test, and production environments. Scope variables and service connections to the appropriate stage, and configure [approvals and checks](/azure/devops/pipelines/process/approvals) on the production environment.

For either provider, configure the selected `azd` environment on each runner or build agent; local `.azure` settings aren't transferred automatically. Serialize production deployments and route changes, and require approval before increasing the candidate's traffic share.

## Roll out a production version gradually

A canary deployment sends a small share of production traffic to a candidate version while the stable version serves the rest. Both versions use the same production agent endpoint. Change traffic through `agentEndpoint.versionSelector` and `azd ai agent endpoint update`; use `--version` to test a specific candidate.

Use an isolated production checkout for the following routing edits. Keep the source revision approved in test unchanged, and retain the production routing configuration with your release records. Don't apply production version numbers to development or test.

### Keep the stable version serving traffic

Before deploying the candidate, identify the current production routing configuration:

```bash
azd ai agent endpoint show my-agent -e production --output json --no-prompt
```

Reference: [Agent CLI commands](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.agents).

Record the stable version and the existing endpoint settings. The following examples use stable version `1` and candidate version `2`. Replace them with the actual versions in your production project, not the version numbers from test.

1. Add or update this block under `services.my-agent` in the production checkout's `azure.yaml`. Keep the rest of the service configuration, including any endpoint protocols and authorization settings:

   ```yaml
   agentEndpoint:
     versionSelector:
       versionSelectionRules:
         - type: FixedRatio
           agentVersion: "1"
           trafficPercentage: 100
   ```

1. Apply the stable route and read it back:

   ```bash
   azd ai agent endpoint update my-agent -e production --no-prompt
   azd ai agent endpoint show my-agent -e production --output json --no-prompt
   ```

   Confirm that `version_selection_rules` assigns 100% to the stable version. Do this before deploying new code, and keep this block in place during deployment.

### Deploy the candidate and start a canary

Deploy the approved source revision while keeping the stable route configured:

```bash
azd deploy my-agent -e production --no-prompt
azd ai agent show my-agent -e production --output json --no-prompt
azd ai agent endpoint show my-agent -e production --output json --no-prompt
```

Confirm that the candidate is active, record its production version number, and verify that the endpoint still points to the stable version. The following example assumes the new version is `2`.

1. Change only the version selection rules to send 10% to the candidate and 90% to the stable version:

   ```yaml
   agentEndpoint:
     versionSelector:
       versionSelectionRules:
         - type: FixedRatio
           agentVersion: "1"
           trafficPercentage: 90
         - type: FixedRatio
           agentVersion: "2"
           trafficPercentage: 10
   ```

1. Apply the change without redeploying the code:

   ```bash
   azd ai agent endpoint update my-agent -e production --no-prompt
   azd ai agent endpoint show my-agent -e production --output json --no-prompt
   ```

   Confirm that the returned rules contain both production versions with the intended percentages. Endpoint updates change routing without creating another agent version.

### Test the candidate version

Use `--version` to select the candidate and start a fresh session and conversation for the test. Send a read-only prompt that exercises the new feature:

```bash
azd ai agent invoke my-agent "<candidate-feature-test-prompt>" \
  -e production --protocol responses --version 2 \
  --new-session --new-conversation --no-prompt
```

Inspect the response and confirm the new behavior against your expected result. You can also point your application's test client at the production agent endpoint and run end-to-end feature checks. Review errors, latency, and response quality during the canary before approving more traffic.

For an agent that uses the Invocations protocol, supply a payload that matches its handler:

```bash
azd ai agent invoke my-agent --input-file candidate-test.json \
  -e production --protocol invocations --version 2 --new-session --no-prompt
```

Create `candidate-test.json` from a known, read-only request for your agent and check the returned result. The `--version` flag selects the version for the session; it doesn't change the configured traffic percentages.

### Increase traffic or return to the stable version

After testing succeeds, adjust the two percentages, apply the endpoint update, and review the result at each stage. Keep the total at 100%. For example, move from 90/10 to 50/50 before completing the rollout.

To complete the release, replace the selection rules with a single rule for the candidate:

```yaml
agentEndpoint:
  versionSelector:
    versionSelectionRules:
      - type: FixedRatio
        agentVersion: "2"
        trafficPercentage: 100
```

Apply and verify the full rollout:

```bash
azd ai agent endpoint update my-agent -e production --no-prompt
azd ai agent endpoint show my-agent -e production --output json --no-prompt
```

If a canary check fails, stop increasing traffic. Replace the rules with the stable version at 100%:

```yaml
agentEndpoint:
  versionSelector:
    versionSelectionRules:
      - type: FixedRatio
        agentVersion: "1"
        trafficPercentage: 100
```

Run the same endpoint update and show commands to apply and verify the return to the stable version. This operation doesn't rebuild code or create another version. Retain the working stable version until the release is accepted.

Save the final routing configuration with the production release settings. Use it as the starting point for the next deployment, so a later pipeline run doesn't reapply an outdated traffic split.

## Related content

- [Set up CI/CD for hosted agents](set-up-ci-cd-cli.md) for pipeline installation and authentication.
- [Deploy a hosted agent from source code](deploy-hosted-agent-code.md) for code-deployment configuration.
- [Hosted agent permissions](../concepts/hosted-agent-permissions.md) for deployment and runtime access requirements.