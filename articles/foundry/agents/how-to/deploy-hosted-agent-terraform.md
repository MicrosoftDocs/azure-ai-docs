---
title: "Deploy a Microsoft Foundry hosted agent with Terraform"
description: "Build a container image and deploy a hosted agent with Terraform and AzAPI. Separate shared Foundry infrastructure from agent releases and verify readiness."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 09/23/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy a Microsoft Foundry hosted agent with Terraform

Use Terraform and the AzAPI provider to deploy a container-backed hosted agent in Microsoft Foundry. Foundry runs your agent code on managed compute. You manage the logical agent's configuration in source control alongside your infrastructure as code (IaC).

Separate shared infrastructure from agent releases: provision the Foundry resources, build and push an image, then apply the agent definition and verify readiness. This article focuses on the agent deployment configuration and accepts existing platform resources as inputs.

This workflow doesn't require Azure Developer CLI (`azd`). For Terraform infrastructure with azd-managed agent deployment, see [Set up CI/CD with azd](set-up-ci-cd-cli.md#choose-the-infrastructure-provider). To upload source code instead of a container image, see [Deploy a hosted agent from source code](deploy-hosted-agent-code.md).

<!-- [TO VERIFY] Validate hosted CRUD, unchanged apply, candidate capture, readiness failures, protocol 2.0.0, and preservation of the production selector in an approved test project before publication. -->

## Prerequisites

- [Terraform](/azure/developer/terraform/quickstart-configure) 1.4 or later, which includes `terraform_data`.
- The [AzAPI provider](/azure/developer/terraform/overview-azapi-provider) 2.9.0 or later. Commit the reviewed provider lockfile so your team uses the same provider version.
- An existing Foundry project and model deployment in a supported region with sufficient quota. To create supporting infrastructure with Terraform, see [Manage Foundry resources with Terraform](../../how-to/create-resource-terraform.md).
- An existing guardrail (RAI policy) on the Foundry account and its full Azure Resource Manager resource ID. See [Add guardrails to a hosted agent](add-hosted-agent-guardrails.md).
- An Azure Container Registry instance that the Foundry runtime can access, with the required project connection and pull permissions configured.
- Hosted-agent code and a Dockerfile, or an existing container image addressed by its immutable digest. The image must target `linux/amd64`, meet the [runtime contract](../concepts/hosted-agent-contract.md), and support [container protocol 2.0.0](migrate-hosted-agent-preview.md#container-protocol-200).
- Docker if you build the image locally. Workstations with Arm processors, including Apple Silicon, also need Docker cross-platform emulation for `linux/amd64`.
- Permission to create and manage agents in the project, and the configured identity's permission to pull your image. See [Hosted agent permissions](../concepts/hosted-agent-permissions.md) and [Deploy a hosted agent](deploy-hosted-agent.md#required-permissions).
- PowerShell 7.4 or later and an authenticated [Azure CLI](/cli/azure/install-azure-cli) for the readiness script. For local development, sign in with `az login` before applying the configuration.
- A single deployment owner for the named agent. Coordinate Terraform, portal, SDK, and other pipeline writers so they don't update that agent concurrently.

## Separate infrastructure from agent deployment

Platform and application teams can manage separate deployment lifecycles. A platform team can own the Foundry account, project, model deployments, guardrail policies, connections, and monitoring. An application team can own the agent code, container image, and logical agent definition.

These resources use different API surfaces:

| Resource | API surface | Deployment approach |
| --- | --- | --- |
| Foundry project (`Microsoft.CognitiveServices/accounts/projects`) | Azure Resource Manager control plane | Terraform or Bicep. |
| Project connection (`Microsoft.CognitiveServices/accounts/projects/connections`) | Azure Resource Manager control plane | Terraform or Bicep; configure registry access before deploying the agent. |
| Logical hosted agent (`Microsoft.Foundry/agents@v1`) | Foundry project data plane | Terraform `azapi_data_plane_resource`, SDK, or REST API. |

The project's data-plane endpoint is the logical agent's parent. Foundry manages the supporting compute; the agent isn't deployed as an App Service or Azure Container Apps resource in Azure Resource Manager. For how AzAPI targets this endpoint, see [Understand the AzAPI data plane framework](/azure/developer/terraform/concept-azapi-data-plane-framework).

Use `azapi_data_plane_resource` with type `Microsoft.Foundry/agents@v1` to manage the **named agent**. This approach doesn't create an independently managed Terraform resource for each version.

A changed definition can create a new version, and Foundry manages the version history under the logical agent. An unchanged apply doesn't provide a new release identifier.

The basic example starts with a new agent name. For an existing production agent, [pin production to its current version](manage-hosted-agent.md#release-a-version-without-changing-production) before applying a candidate definition. Review Terraform ownership and import requirements before adopting an agent that another tool already manages.

## Plan the deployment stages

For the initial deployment, complete the stages in this order:

1. Provision or reuse the base infrastructure: the Foundry account and project, model deployment, guardrail policy, registry connection, required identities and role assignments, and monitoring.
1. Build the agent's `linux/amd64` image and push it to Azure Container Registry.
1. Apply the hosted-agent Terraform configuration with the project endpoint, image digest, model deployment name, and full RAI policy resource ID.
1. Wait for the resulting version to become `active`, then invoke and validate that version.

Azure Container Registry can have a separate lifecycle from the Foundry resources. Reuse a centrally managed registry when your organization shares one across application teams.

For subsequent agent releases, reuse the base infrastructure unless its configuration needs to change. Build and push the new image, apply the updated agent definition, and repeat the readiness and application checks. Keep production pinned until the candidate passes those checks.

For an end-to-end example, see the community-maintained [simple-hosted-agent-deploy-azapi sample](https://github.com/JFolberth/simple-hosted-agent-deploy-azapi). It separates a `foundry_base` Terraform configuration, an image build, and a `hosted_agent` Terraform configuration, and includes a reusable [hosted-agent module](https://github.com/JFolberth/simple-hosted-agent-deploy-azapi/tree/main/simple_agent/azure/infra/modules/hosted_agent). Follow its README for development-container setup, deployment commands, and cleanup.

The sample uses local Terraform state by default. Review its settings against current platform requirements and configure secure remote state and release controls before adapting it for a shared environment.

## Build and push the container image

Skip the build if an image pipeline already supplies a compatible image digest. Otherwise, run these Bash commands from the directory containing your agent's Dockerfile. Use a unique release tag and don't overwrite it during deployment.

```bash
set -euo pipefail

ACR_NAME="<registry-name>"
IMAGE_NAME="<image-name>"
IMAGE_TAG="<unique-release-tag>"
LOGIN_SERVER=$(az acr show --name "$ACR_NAME" \
  --query loginServer --output tsv)

az acr login --name "$ACR_NAME"
docker build --platform linux/amd64 \
  --tag "$LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG" .
docker push "$LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"

DIGEST=$(az acr repository show --name "$ACR_NAME" \
  --image "$IMAGE_NAME:$IMAGE_TAG" --query digest --output tsv)
if [[ ! "$DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  echo "The registry didn't return a valid image digest." >&2
  exit 1
fi

printf 'image_uri = "%s/%s@%s"\n' "$LOGIN_SERVER" "$IMAGE_NAME" "$DIGEST"
```

Copy the printed `image_uri` assignment into `terraform.tfvars` in the next section. Pinning a digest makes the release independent of later tag changes. Keep the image available while agent versions or rollback requirements depend on it.

Permission to push an image doesn't grant the Foundry runtime permission to pull it. Configure registry access separately. See [Hosted agent permissions](../concepts/hosted-agent-permissions.md).

Reference: [Container requirements](deploy-hosted-agent.md#container-requirements), [az acr login](/cli/azure/acr#az-acr-login), and [az acr repository show](/cli/azure/acr/repository#az-acr-repository-show).

## Configure providers and inputs

Create the following files in a separate Terraform configuration directory. Pass the shared platform's project endpoint, model deployment name, and guardrail resource ID as inputs; this configuration doesn't recreate those resources. You can supply the values from reviewed platform outputs or pipeline configuration.

1. Create `providers.tf`:

   ```terraform
   terraform {
     required_version = ">= 1.4.0"

     required_providers {
       azapi = {
         source  = "Azure/azapi"
         version = ">= 2.9.0, < 3.0.0"
       }
     }
   }

   provider "azapi" {}
   ```

   For local development, the provider can use your Azure CLI sign-in. In CI, configure provider authentication and the Azure CLI sign-in separately. Authenticating the provider with OIDC doesn't automatically authenticate the CLI used by the waiter.

1. Create `variables.tf`:

   ```terraform
   variable "project_endpoint" {
     type        = string
     description = "HTTPS Foundry project data-plane endpoint."

     validation {
       condition = can(regex(
         "^https://[^/?#]+/api/projects/[^/?#]+/?$",
         var.project_endpoint
       ))
       error_message = "Use an HTTPS project endpoint without a query."
     }
   }

   variable "agent_name" {
     type        = string
     description = "Name of the agent managed by this configuration."
   }

   variable "image_uri" {
     type        = string
     description = "Container image URI including its sha256 digest."

     validation {
       condition     = can(regex("@sha256:[0-9a-f]{64}$", var.image_uri))
       error_message = "Use an immutable image URI ending in @sha256:digest."
     }
   }

   variable "model_deployment_name" {
     type        = string
     description = "Existing model deployment used by the container."
   }

   variable "cpu" {
     type        = string
     description = "CPU cores for the hosted container."
     default     = "0.5"
     nullable    = false
   }

   variable "memory" {
     type        = string
     description = "Memory for the hosted container."
     default     = "1Gi"
     nullable    = false
   }

   variable "environment_variables" {
     type        = map(string)
     description = "Additional nonsecret container environment variables."
     default     = {}
   }

   variable "rai_policy_id" {
     type        = string
     description = "Full ARM resource ID of an existing RAI policy."
     nullable    = false

     validation {
       condition = can(regex(join("", [
         "(?i)^/subscriptions/[^/]+/resourceGroups/[^/]+",
         "/providers/Microsoft\\.CognitiveServices/accounts/[^/]+",
         "/raiPolicies/[^/]+$"
       ]), var.rai_policy_id))
       error_message = "Provide the full account-scoped RAI policy ARM ID."
     }
   }
   ```

1. Create `terraform.tfvars` with your own values:

   ```terraform
   project_endpoint = "https://<account>.services.ai.azure.com/api/projects/<project>"
   agent_name       = "<agent-name>"
   image_uri        = "<registry>/<repository>@sha256:<64-character-digest>"

   model_deployment_name = "<existing-model-deployment>"
   rai_policy_id         = "<full-rai-policy-arm-resource-id>"

   cpu    = "0.5"
   memory = "1Gi"
   ```

   Replace every placeholder. Use an image that your Foundry project can pull; a digest doesn't configure registry permissions. Get the full `rai_policy_id` from the platform configuration or policy resource:

   ```text
   /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>
   ```

For team use, configure a secure remote backend before running deployments. Use separate state keys for environments and restrict access to state and saved plans. See [Store Terraform state in Azure Storage](/azure/developer/terraform/store-state-in-azure-storage).

## Define the hosted agent

Create `main.tf`. The `parent_id` is the project endpoint without `https://`, not the project's Azure Resource Manager ID.

```terraform
locals {
  project_endpoint = trimsuffix(var.project_endpoint, "/")

  agent_definition = {
    kind = "hosted"
    container_configuration = {
      image = var.image_uri
    }
    cpu    = var.cpu
    memory = var.memory
    protocol_versions = [
      {
        protocol = "responses"
        version  = "2.0.0"
      }
    ]
    environment_variables = merge(var.environment_variables, {
      AZURE_AI_MODEL_DEPLOYMENT_NAME = var.model_deployment_name
    })
    rai_config = {
      rai_policy_name = var.rai_policy_id
    }
  }
}

resource "azapi_data_plane_resource" "hosted_agent" {
  type      = "Microsoft.Foundry/agents@v1"
  name      = var.agent_name
  parent_id = trimprefix(local.project_endpoint, "https://")

  body = {
    name       = var.agent_name
    definition = local.agent_definition
  }

  response_export_values = ["versions.latest.version"]

  lifecycle {
    prevent_destroy = true

    precondition {
      condition = contains(
        ["0.5:1Gi", "1:2Gi", "2:4Gi"], "${var.cpu}:${var.memory}"
      )
      error_message = "Choose a supported CPU and memory pair."
    }
  }
}
```

The default inputs use a documented [sandbox size](../concepts/hosted-agents.md#sandbox-sizes). Change `cpu` and `memory` together to another supported pair. Change `AZURE_AI_MODEL_DEPLOYMENT_NAME` if your container expects a different environment-variable name. The variable selects an existing model deployment; it doesn't create one.

These fields use the Foundry REST schema, not the `azure.yaml` schema. Despite its name, the hosted-agent field `rai_policy_name` takes the **full Azure Resource Manager resource ID of the RAI policy**, not a bare policy name. The example requires `rai_policy_id` and passes it to that field.

Confirm the policy exists on the account and [test content safety filtering](add-hosted-agent-guardrails.md#test-content-safety-filtering). A version can report `active` even when an invalid policy reference prevents filtering. Readiness isn't proof that the guardrail is effective.

Don't put secrets directly in the environment-variable map. Terraform state can retain configuration values. For runtime secret resolution, see [Reference project connections in environment variables](deploy-hosted-agent.md#reference-project-connections-in-environment-variables).

The explicit response export makes the version available through `output.versions.latest.version`. Without it, don't assume the provider exports the agent response.

## Add a readiness gate

A successful resource write doesn't prove that the hosted version is active. Check the version's status separately.

The provider rereads the named agent to populate its output. Its `latest` value isn't an atomic receipt for a version created by this deployment. Keep exclusive deployment ownership, capture the value once, and verify the candidate before using it for tests or promotion.

1. Create a `scripts` directory and save the following as `scripts/Get-HostedAgentStatus.ps1`:

   ```powershell
   $ErrorActionPreference = "Stop"
   Set-StrictMode -Version Latest

   function Get-RequiredEnvironmentValue([string] $Name) {
       $value = [Environment]::GetEnvironmentVariable($Name)
       if ([string]::IsNullOrWhiteSpace($value)) {
           throw "Missing required environment variable: $Name."
       }
       return $value
   }

   function Get-PositiveInteger([string] $Name) {
       $value = Get-RequiredEnvironmentValue $Name
       $number = 0
       if (-not [int]::TryParse($value, [ref] $number) -or $number -le 0) {
           throw "$Name must be a positive integer."
       }
       return $number
   }

   $endpoint = Get-RequiredEnvironmentValue "PROJECT_ENDPOINT"
   $name = Get-RequiredEnvironmentValue "AGENT_NAME"
   $version = Get-RequiredEnvironmentValue "AGENT_VERSION"
   $expectedImage = Get-RequiredEnvironmentValue "EXPECTED_IMAGE_URI"
   $timeout = Get-PositiveInteger "TIMEOUT_SECONDS"
   $interval = Get-PositiveInteger "POLL_INTERVAL_SECONDS"

   $projectUri = $null
   if (-not [Uri]::TryCreate($endpoint, [UriKind]::Absolute,
           [ref] $projectUri) -or
       $projectUri.Scheme -ne "https" -or
       $projectUri.UserInfo -or $projectUri.Query -or $projectUri.Fragment) {
       throw "PROJECT_ENDPOINT must be an HTTPS endpoint without credentials."
   }

   $agentPath = [Uri]::EscapeDataString($name)
   $versionPath = [Uri]::EscapeDataString($version)
   $url = $endpoint.TrimEnd("/") +
       "/agents/$agentPath/versions/${versionPath}?api-version=v1"

   $tokenOutput = & az account get-access-token `
       --resource https://ai.azure.com --query accessToken `
       --output tsv --only-show-errors 2>$null
   if ($LASTEXITCODE -ne 0) {
       throw "Azure CLI token acquisition failed. Check the runner sign-in."
   }
   $token = ($tokenOutput -join "").Trim()
   if ([string]::IsNullOrWhiteSpace($token)) {
       throw "Azure CLI returned an empty access token."
   }
   $headers = @{ Authorization = "Bearer $token" }
   $clock = [Diagnostics.Stopwatch]::StartNew()

   while ($clock.Elapsed.TotalSeconds -lt $timeout) {
       $remaining = $timeout - $clock.Elapsed.TotalSeconds
       $requestTimeout = [int][Math]::Min(30, [Math]::Ceiling($remaining))
       $response = $null
       $delay = [double] $interval

       try {
           $response = Invoke-WebRequest -Method Get -Uri $url `
               -Headers $headers -TimeoutSec $requestTimeout `
               -MaximumRedirection 0 -SkipHttpErrorCheck
       }
       catch [System.Net.Http.HttpRequestException],
             [System.OperationCanceledException] {
           Write-Host "Transient status-request failure; retrying."
       }

       if ($clock.Elapsed.TotalSeconds -ge $timeout) {
           break
       }

       if ($null -ne $response) {
           $httpStatus = [int] $response.StatusCode
           if ($httpStatus -eq 200) {
               try {
                   $body = ConvertFrom-Json -InputObject $response.Content `
                       -AsHashtable
               }
               catch [System.ArgumentException] {
                   throw "The version endpoint returned invalid JSON."
               }
               if ($body -isnot [System.Collections.IDictionary] -or
                   -not $body.Contains("status") -or
                   $body["status"] -isnot [string]) {
                   throw "The version response is missing a valid status."
               }

               $status = $body["status"]
               switch -CaseSensitive ($status) {
                   "active" {
                       $image = $body.definition.container_configuration.image
                       if ($image -cne $expectedImage) {
                           throw "Candidate image doesn't match the release."
                       }
                       Write-Host "Candidate version is active; image matches."
                       exit 0
                   }
                   "creating" { Write-Host "Candidate is creating." }
                   "failed" { throw "Candidate provisioning failed." }
                   "deleting" { throw "Candidate is being deleted." }
                   "deleted" { throw "Candidate has been deleted." }
                   default { throw "Unrecognized version status." }
               }
           }
           elseif ($httpStatus -in @(408, 429, 500, 502, 503, 504)) {
               Write-Host "Transient HTTP $httpStatus; retrying."
               $retryAfter = [string] $response.Headers["Retry-After"]
               $retrySeconds = 0
               $retryDate = [DateTimeOffset]::MinValue
               if ([int]::TryParse($retryAfter, [ref] $retrySeconds)) {
                   $delay = [Math]::Max($delay, $retrySeconds)
               }
               elseif ([DateTimeOffset]::TryParse($retryAfter,
                       [ref] $retryDate)) {
                   $seconds = ($retryDate - [DateTimeOffset]::UtcNow).TotalSeconds
                   $delay = [Math]::Max($delay, $seconds)
               }
           }
           else {
               throw "Version lookup failed with HTTP $httpStatus."
           }
       }

       $remaining = $timeout - $clock.Elapsed.TotalSeconds
       if ($remaining -gt 0) {
           Start-Sleep -Seconds ([Math]::Min($delay, $remaining))
       }
   }

   throw "Timed out waiting for the candidate version to become active."
   ```

   This script obtains a token before starting its bounded status poll. It retries selected transient errors, rejects permanent HTTP failures, and exits unsuccessfully on failure, deletion, malformed responses, or timeout. It doesn't print tokens or response bodies.

   The image check is an additional safeguard, not a replacement for exclusive ownership or checking the rest of the candidate definition.

1. Add the gate to `main.tf`:

   ```terraform
   resource "terraform_data" "hosted_agent_status" {
     triggers_replace = {
       endpoint = local.project_endpoint
       name     = var.agent_name
       version = tostring(
         azapi_data_plane_resource.hosted_agent.output.versions.latest.version
       )
     }

     provisioner "local-exec" {
       working_dir = path.module
       interpreter = ["pwsh", "-NoProfile", "-NonInteractive", "-Command"]
       command     = "& './scripts/Get-HostedAgentStatus.ps1'"

       environment = {
         PROJECT_ENDPOINT = local.project_endpoint
         AGENT_NAME       = var.agent_name
         AGENT_VERSION = tostring(
           azapi_data_plane_resource.hosted_agent.output.versions.latest.version
         )
         EXPECTED_IMAGE_URI    = var.image_uri
         TIMEOUT_SECONDS       = "600"
         POLL_INTERVAL_SECONDS = "10"
       }
     }
   }
   ```

   Adjust the timeout and polling interval for your pipeline. The timeout is a bounded example, not a service readiness guarantee.

   `terraform_data` runs this gate when its trigger changes. It isn't continuous health monitoring. Rerun the same script as a pipeline check when you need to recheck a candidate after an approval wait.

1. Create `outputs.tf`:

   ```terraform
   output "agent_version" {
     description = "Captured version from this serialized deployment."
     value = tostring(
       azapi_data_plane_resource.hosted_agent.output.versions.latest.version
     )
     depends_on = [terraform_data.hosted_agent_status]
   }
   ```

Reference: [Terraform data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data), [local-exec provisioner](https://developer.hashicorp.com/terraform/language/resources/provisioners/local-exec), and [hosted version statuses](manage-hosted-agent.md#version-status-values).

## Apply and validate the deployment

Apply this configuration only after reviewing its resource ownership and, for an existing production agent, pinning the production version.

1. Initialize and validate the complete configuration:

   ```bash
   terraform init
   terraform fmt -check
   terraform validate
   terraform plan -out=tfplan
   ```

1. Review the plan. Stop if it replaces an existing agent or changes resources outside the intended release.

1. Apply the reviewed plan:

   ```bash
   terraform apply tfplan
   terraform output -raw agent_version
   ```

   A successful apply includes the readiness gate for a new candidate. Save the returned version as the release's candidate identifier. Protect the saved plan, and don't keep it in source control.

1. Inspect that exact version and confirm its image and configuration match the intended release. Don't rediscover `latest` after another writer has had access to the agent.

1. [Create a fresh session pinned to the candidate version](manage-hosted-sessions.md#create-a-session-explicitly-advanced). Invoke it using the returned session ID and assert successful protocol completion and expected response content.

1. Confirm that the version references the intended full guardrail policy ID and [test its filtering behavior](add-hosted-agent-guardrails.md#test-content-safety-filtering).

Readiness confirms that the version is active. An application-level smoke test checks that it performs the intended task. Don't promote a candidate if readiness, application, or guardrail checks fail.

## Use the configuration in CI/CD

Separate the pipeline into infrastructure and definition apply, candidate tests, approval, and promotion. Keep the captured candidate identifier and expected image digest together as the release record.

If platform and application teams use separate Terraform configurations, keep their state and permissions separate too. Pass reviewed platform outputs into the agent configuration. An application-only release doesn't need to reapply unchanged shared infrastructure.

For unattended execution:

- Install the reviewed Terraform version, PowerShell, and Azure CLI on the runner.
- Configure OIDC or another approved workload identity for provider, backend, and CLI authentication. Don't rely on a developer's cached sign-in.
- Use secure remote state and serialize the entire release across all writers, not just the apply step.
- Recheck candidate readiness and the production selector after approval.
- [Promote the tested version explicitly](manage-hosted-agent.md#release-a-version-without-changing-production), retaining the previous version for rollback.

The Terraform configuration above owns the agent definition. Coordinate endpoint-promotion ownership separately, and verify a subsequent refresh and apply doesn't revert the selector. Don't let two independent configurations manage the same fields.

## Troubleshoot and clean up

Use status and HTTP diagnostics without printing full definitions or credentials into CI logs.

| Symptom | Action |
| --- | --- |
| Missing version output | Confirm `response_export_values` includes `versions.latest.version`. |
| Token acquisition fails | Authenticate Azure CLI in the same runner context as the provisioner. |
| HTTP 401 or 403 | Check the token audience and the deployment identity's data-plane roles. |
| Candidate reaches `failed` | Inspect the specific version and available diagnostics. Check image access, runtime compatibility, and configuration. |
| Candidate image doesn't match | Stop the release and investigate other writers or incorrect inputs. Don't promote the observed latest version. |
| Agent is active but filtering doesn't work | Verify the policy exists, use its full Azure Resource Manager resource ID in `rai_policy_name`, and test filtering separately from readiness. |
| Readiness timeout | Inspect that version before retrying. Don't treat successful Terraform resource creation as readiness. |
| Destruction is blocked | `prevent_destroy` intentionally prevents agent deletion or replacement. Review ownership and retention requirements before changing it. |

Deleting the named agent deletes its versions and can be blocked by active sessions. It isn't rollback. For a disposable deployment, review the [agent deletion procedure](manage-hosted-agent.md#delete-an-agent), resolve session dependencies, and remove `prevent_destroy` only after approving that deletion. Don't force-delete production sessions as part of a routine release.

## Related content

- [Manage hosted agents](manage-hosted-agent.md) for version lifecycle and endpoint selection.
- [Set up azd CI/CD with Terraform](set-up-ci-cd-cli.md) for azd-managed agent deployment.
- [Manage Foundry infrastructure with Terraform](../../how-to/create-resource-terraform.md) for control-plane resources.
