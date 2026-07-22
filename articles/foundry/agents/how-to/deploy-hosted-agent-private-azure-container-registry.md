---
title: "Deploy a hosted agent with a private Azure Container Registry"
description: "Use an existing or private Azure Container Registry when you deploy Microsoft Foundry hosted agents with Azure Developer CLI."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 07/21/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy a hosted agent with a private Azure Container Registry

Use a centrally managed Azure Container Registry (ACR) when you deploy hosted agent container images. You can build locally and push to an existing ACR, or skip the build and deploy a pre-built image that was pushed by another pipeline.

## Prerequisites

- An initialized hosted agent project with an `azure.yaml` file. For setup, see [Initialize an agent project](init-agent-project.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md).
- An authenticated `azd` session.
- Access to an existing Azure Container Registry.
- Required ACR permissions for your selected build path.

## Choose your ACR workflow

Most teams want their hosted agent container images to come from a centrally managed ACR, not a new per-project registry. There are two flavors of this:

- **Build locally and push** to an existing ACR. This is typical when teams share one registry across many projects.
- **Skip the build entirely** and deploy a pre-built image that was already pushed by a separate pipeline.

> [!NOTE]
> Both workflows are independent of whether the ACR is "private" in the network sense, such as a private endpoint with `publicNetworkAccess: Disabled`. Network privacy is covered in [Configure virtual networks](virtual-networks.md). This article focuses on registry selection and access.

## Decide when to bring your own ACR

Bring your own ACR when one or more of these requirements apply:

- **Compliance.** Images must live in a centrally audited registry your org already operates.
- **Shared infrastructure.** One ACR feeds many agent projects; new per-project registries aren't acceptable.
- **ABAC-mode registries.** Your enterprise ACR is configured with attribute-based access control, requiring specific roles.
- **Pre-built images.** A separate CI pipeline builds the image with vulnerability scanning, supply-chain signing, and hardened base images. The agent project should consume that image as-is.

If none of those apply, leave the defaults alone. `azd ai agent init` creates a new ACR for the project and `azd up` pushes to it.

## Review registry selection

When you run `azd ai agent init` against an existing Microsoft Foundry project, the extension scans the project for ACR connections and offers them as choices:

- **0 ACR connections found.** You're prompted for an ACR authentication server, such as `myregistry.azurecr.io`. Leave the prompt blank to let `azd provision` create the project registry when your configuration requires one.
- **1 ACR connection found.** It's selected automatically and shown in the output.
- **2+ ACR connections found.** You pick one from a list.

Whatever is selected writes two env vars to your azd environment:

| Environment variable | What it is |
|---------|------------|
| `AZURE_CONTAINER_REGISTRY_ENDPOINT` | Authentication server, for example `myregistry.azurecr.io` |
| `AZURE_CONTAINER_REGISTRY_RESOURCE_ID` | Full ARM resource ID. Optional, but enables faster, scoped RBAC preflight checks. |

You can also set these environment variables yourself before `azd up`:

```bash
azd env set AZURE_CONTAINER_REGISTRY_ENDPOINT myregistry.azurecr.io
azd env set AZURE_CONTAINER_REGISTRY_RESOURCE_ID \
  /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/myregistry
```

When both are set, `azd` skips creating a new ACR and the build path pushes directly to the existing one.

## Build locally and push to an existing ACR

This workflow is the most common enterprise path: keep the default container build, but target a shared registry instead of a per-project one.

1. Point at the existing ACR.

   If you're about to run `azd ai agent init`, you can answer the ACR prompt with your registry's sign-in server, and the environment variables are written for you. If the project already exists, set them with `azd env set` as shown earlier.

1. Confirm developer RBAC.

   `azd up` runs a preflight check against the ACR before it starts building. The role you need depends on which build path is configured in `azure.yaml`:

   | Build path | Required developer role on the ACR |
   |------------|------------------------------------|
   | **Local build** (`docker.remoteBuild: false`) | **AcrPush** -- data-plane push of the locally built image |
   | **Remote build** (`docker.remoteBuild: true`, the default) | **Container Registry Tasks Contributor** -- needed to call `listBuildSourceUploadUrl` and `scheduleRun` |

   If the registry is **ABAC-enabled**, the preflight check also looks for one of:

   - Local build: **Container Registry Repository Writer** (per-repository grant), or
   - Remote build: **Owner**/**Contributor**, since the Repository Writer role doesn't cover ACR Tasks actions.

   When the push or remote build fails with a 403, `azd up` classifies the error and prints a ready-to-paste `az role assignment create` command, substituting your object ID and the ACR scope from the ARM error response.

1. Run `azd up`.

   ```bash
   azd up
   ```

   The build artifact is pushed to your existing ACR. The agent identity is granted **AcrPull** at deploy time so the Microsoft Foundry hosted agent runtime can pull it.

## Deploy a pre-built image

Use this workflow when a separate CI pipeline already builds, scans, signs, and pushes the image. The agent project consumes that image directly, with no Dockerfile and no local build.

1. Set the `image` field in the `azure.ai.agent` service in `azure.yaml`.

   ```yaml
   services:
     my-agent:
       host: azure.ai.agent
       project: src/my-agent
       kind: hosted
       name: my-agent
       image: myregistry.azurecr.io/agents/my-agent:1.2.3
       protocols:
         - protocol: responses
           version: "2.0.0"
   ```

   The `image` value must be a valid container reference. Both tags and SHA digests are accepted. Pin to a digest (`@sha256:...`) for reproducible deploys.

   For a new project, provide the image during initialization instead:

   ```bash
   azd ai agent init --image myregistry.azurecr.io/agents/my-agent:1.2.3 --agent-name my-agent
   ```

   The `--image` option uses the prebuilt image path and skips code scaffolding, Dockerfile generation, and ACR setup.

1. Run the deploy.

   ```bash
   azd deploy

   # Or run up end-to-end
   azd up
   ```

   The Foundry hosted agent runtime pulls the image from your ACR using the per-agent **agent identity**, which `azd` granted **AcrPull** during deploy.

## Review RBAC

| Actor | Role | Scope | Required when |
|-------|------|-------|---------------|
| Developer (you, running `azd up`) | **AcrPush** | ACR | Local build path (`docker.remoteBuild: false`) |
| Developer | **Container Registry Tasks Contributor** | ACR | Remote build path (`docker.remoteBuild: true` -- the default) |
| Developer | **Container Registry Repository Writer** | ACR | ABAC-mode ACR, local build path |
| Developer | **Owner** or **Contributor** | ACR | ABAC-mode ACR, remote build path (Repository Writer doesn't cover Tasks) |
| Agent identity (created by Foundry) | **AcrPull** | ACR | Always -- granted automatically by `azd deploy` |

Run `azd ai agent doctor` after a deploy attempt to see the RBAC state. Failed pushes also surface the missing role and a paste-ready `az role assignment create` command.

## Work with a private endpoint on the ACR

If the ACR has `publicNetworkAccess: Disabled`, and is only reachable from a virtual network, then `azd up` must run from inside that virtual network. Use a self-hosted runner, an Azure DevOps agent, or a jump host.

The Foundry runtime separately needs network reachability to the registry to pull the image. That requirement is a platform concern beyond this article.

See [Configure virtual networks](virtual-networks.md) for the network-side picture and for how to integrate this workflow with private endpoints on the ACR, Foundry account, AppInsights, and Storage.

## Troubleshoot ACR deployment

| Symptom | Cause | What to try |
|---------|-------|-------------|
| `403 unauthorized` on local push | Missing **AcrPush** on the registry. | Paste the `az role assignment create ...` command the CLI emitted, or assign **AcrPush** via the portal. Re-run `azd deploy`. |
| `403` from `listBuildSourceUploadUrl` or `scheduleRun` | Missing **Container Registry Tasks Contributor** on the registry (remote-build path). | Assign **Container Registry Tasks Contributor** at the ACR scope. |
| 403 mentions `Microsoft.Authorization/roleAssignments/write` failing on an ACR scope | ABAC-mode registry; **Repository Writer** alone is insufficient for remote build. | Use **Owner**/**Contributor** at the ACR scope, or switch `docker.remoteBuild: false` and grant **Repository Writer**. |
| `Image not found` at runtime | The agent identity doesn't have **AcrPull** on the registry. | Re-run `azd deploy` -- the role assignment step retries. If it still fails, grant **AcrPull** to the agent identity manually. |
| Interactive prompt for "build vs pre-built" appears every deploy | The interactive default is intentional -- it is "build", to avoid silently switching off the Dockerfile. | Use the pre-built image workflow explicitly each time, or remove the Dockerfile from the service path so there is nothing to build. |
| In `--no-prompt` mode, deploy keeps building instead of using the configured image | Non-interactive mode picks the default (build) automatically. | Remove the Dockerfile from the service directory so the build path isn't selected, or set `AZURE_CONTAINER_REGISTRY_ENDPOINT` and pre-push the image separately. |
| `AZURE_CONTAINER_REGISTRY_ENDPOINT not set -- skipping ACR role check` warning | The environment variable is unset; the preflight check is informational and skips. | Set it with `azd env set` if you want the preflight gate, or leave it empty if `main.bicep` will create the ACR during `provision`. |

## Related content

- [Deploy a hosted agent](deploy-hosted-agent.md) for the end-to-end deploy flow this article customizes.
- [Configure virtual networks](virtual-networks.md) for private endpoints, self-hosted runners, and DNS for virtual-network-protected ACRs.
