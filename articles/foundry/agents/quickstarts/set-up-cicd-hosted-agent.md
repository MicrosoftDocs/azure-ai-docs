---
title: "Set up CI/CD for a hosted agent"
description: "Learn how to set up a GitHub Actions CI/CD pipeline that deploys and validates a hosted agent."
author: aahill
ms.author: aahi
ms.date: 06/26/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-deploy-method
#CustomerIntent: As an enterprise hosted agent developer, I want to set up a CI/CD pipeline so that I can automatically deploy and validate my agent after I update its source code.
---

# Quickstart: Hosted agent CI/CD templates

You can establish a Continuous Integration and Continuous Deployment (CI/CD) pipeline for a hosted agent in Microsoft Foundry project. This quickstart helps enterprise hosted agent developers validate code changes after they update agent source code.

The pipeline performs two tasks:

1. Deploy the updated hosted agent code.

1. Invoke the agent and verify that it returns a response.

> [!NOTE]
> This quickstart focuses on GitHub Actions. The pipeline template includes comments for values that vary by project, such as the hosted agent code root folder, Foundry project endpoint, model deployment, and test prompt. Update those values to match your repository and environment layout.

## Set up a GitHub pipeline for hosted agents

You can use GitHub Actions with Azure Developer CLI (`azd`) to deploy and validate hosted agent changes. The workflow uses GitHub OpenID Connect (OIDC) to sign in to Azure, configures the `azd` environment, deploys the agent, shows the hosted agent status, and sends a smoke-test message.

### Prerequisites

| **Item** | **Description** |
| --- | --- |
| Hosted agent project | Your repository contains an agent project created with `azd init`. Run `azd provision` and `azd deploy` before using this CI/CD pipeline so that a Foundry project and hosted agent already exist in the cloud. |
| GitHub OIDC configuration | Configure a Microsoft Entra application or federated credential that allows your GitHub workflow to sign in to Azure with OIDC. For more information, see [Use the Azure login action with OpenID Connect](/azure/developer/github/connect-from-azure#use-the-azure-login-action-with-openid-connect). |
| Deployment permissions | After you create the OIDC federated credential, assign roles to the workflow identity. For code deployment (`azd ai agent init --deploy-mode code`), grant the Foundry User role and Contributor role on the target Foundry project. If your project uses container deployment (`--deploy-mode container`), also grant the Azure RBAC permissions required to build, push, and deploy the container image and access related Azure resources. |
| Repository variables | Store non-secret configuration such as subscription ID, tenant ID, client ID, project endpoint, project ID, location, model deployment name, and test prompt as GitHub Actions variables. The specific variables to configure are listed later in this quickstart. |

### Set up pipeline with GitHub

1. Create a `.github/workflows/hosted-agent-cd.yml` file in your repository with the following content:

   ```yaml
   name: Hosted Agent CI/CD

   on:
     push:
       branches:
         - main
     workflow_dispatch:

   permissions:
     id-token: write
     contents: read

   env:
     # Update this path to the root folder for your hosted agent code.
     AGENT_PROJECT_DIR: ./path-to-your-agent-code-root

     # Update this environment name to match your environment.
     AZD_ENV_NAME: staging

     # Update this prompt to a safe smoke-test message that your agent should answer.
     AGENT_TEST_PROMPT: "Hello from CI. Reply with a short confirmation that you are running."

   jobs:
     deploy-and-test:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout repository
           uses: actions/checkout@v4

         - name: Install Azure Developer CLI
           uses: Azure/setup-azd@v2

         - name: Install azd Foundry extension
           run: azd ext install microsoft.foundry

         - name: Verify azd Foundry extension
           run: |
             set -euo pipefail
             azd ext list | grep -q "microsoft.foundry"
             azd ai agent --help > /dev/null

         - name: Azure login with OIDC
           uses: azure/login@v2
           with:
             client-id: ${{ vars.AZURE_CLIENT_ID }}
             tenant-id: ${{ vars.AZURE_TENANT_ID }}
             subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

         - name: Configure azd authentication
           run: |
             azd config set auth.useAzCliAuth true
             azd config set defaults.subscription "${{ vars.AZURE_SUBSCRIPTION_ID }}"

         - name: Configure deployment environment
           working-directory: ${{ env.AGENT_PROJECT_DIR }}
           run: |
             set -euo pipefail

             # Select or create the environment for this hosted agent project.
             azd env select "$AZD_ENV_NAME" || azd env new "$AZD_ENV_NAME" --no-prompt

             # Configure cloud resource parameters for the already deployed environment.
             # Add or remove azd env values based on the parameters used by your azure.yaml and agent.yaml.
             azd env set AZURE_SUBSCRIPTION_ID "${{ vars.AZURE_SUBSCRIPTION_ID }}"
             azd env set AZURE_TENANT_ID "${{ vars.AZURE_TENANT_ID }}"
             azd env set AZURE_LOCATION "${{ vars.AZURE_LOCATION }}"
             azd env set FOUNDRY_PROJECT_ENDPOINT "${{ vars.FOUNDRY_PROJECT_ENDPOINT }}"
             azd env set AZURE_AI_PROJECT_ID "${{ vars.AZURE_AI_PROJECT_ID }}"
             azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "${{ vars.AZURE_AI_MODEL_DEPLOYMENT_NAME }}"

             azd env get-values

         - name: Deploy agent
           working-directory: ${{ env.AGENT_PROJECT_DIR }}
           run: azd deploy --no-prompt

         - name: Show agent status
           working-directory: ${{ env.AGENT_PROJECT_DIR }}
           run: azd ai agent show --no-prompt

         - name: Test agent
           working-directory: ${{ env.AGENT_PROJECT_DIR }}
           run: |
             set -euo pipefail

             # For responses-protocol agents, a plain text prompt is enough.
             # If your agent uses the invocations protocol, replace this command with:
             #   printf '{"message":"%s"}' "$AGENT_TEST_PROMPT" > /tmp/test-payload.json
             #   azd ai agent invoke -p invocations -f /tmp/test-payload.json --no-prompt > /tmp/agent-response.txt 2>&1
             azd ai agent invoke "$AGENT_TEST_PROMPT" > /tmp/agent-response.txt 2>&1

             echo "--- Agent response ---"
             cat /tmp/agent-response.txt
             echo "--- End agent response ---"

             if [ ! -s /tmp/agent-response.txt ]; then
               echo "::error::The agent returned an empty response."
               exit 1
             fi

             echo "Smoke test passed."
   ```

1. In GitHub, go to **Settings** > **Secrets and variables** > **Actions** and add the following repository variables:

   * `AZURE_CLIENT_ID`
   * `AZURE_TENANT_ID`
   * `AZURE_SUBSCRIPTION_ID`
   * `AZURE_LOCATION`
   * `FOUNDRY_PROJECT_ENDPOINT`
   * `AZURE_AI_PROJECT_ID`
   * `AZURE_AI_MODEL_DEPLOYMENT_NAME`

    Except for `AZURE_CLIENT_ID`, which comes from your OIDC application registration, you can find these values in your project `.azure/<project-name>/.env` file. You can also get the project endpoint, project ID, and model deployment name from the corresponding agent details page in the Foundry portal.

1. Add any additional variables or secrets required by your hosted agent project.

1. Update the workflow placeholders.

   In `hosted-agent-cd.yml`, update the following values:

    * `AGENT_PROJECT_DIR`: The repository-relative path to the root folder for your hosted agent code.
    * `AZD_ENV_NAME`: The staging `azd` environment name for deployment.
    * `AGENT_TEST_PROMPT`: A smoke-test prompt that should produce a reliable response from your agent.
    * Optional `azd env set` lines: Any additional environment values required by your agent.

1. Run the pipeline.

   Push code to the `main` branch or run the workflow manually from the GitHub Actions page.

  After the pipeline executes successfully, the log shows that the hosted agent was deployed, the agent status was returned, and the smoke-test invocation returned a non-empty response.

## See also

* [Azure Developer CLI documentation](/azure/developer/azure-developer-cli/)
* [Use OpenID Connect with Azure Login for GitHub Actions](/azure/developer/github/connect-from-azure)
* [GitHub Actions variables](https://docs.github.com/actions/learn-github-actions/variables)
* [GitHub Actions secrets](https://docs.github.com/actions/security-guides/using-secrets-in-github-actions)
* [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
