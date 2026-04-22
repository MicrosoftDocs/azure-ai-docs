---
title: "Configure Claude Desktop for Microsoft Foundry"
description: "Configure Claude Desktop to use Microsoft Foundry as its inference provider for enterprise deployments."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 04/22/2026
ms.custom: dev-focus, doc-kit-assisted
author: msakande
ms.author: mopeakande
ai-usage: ai-assisted
#CustomerIntent: As an IT admin, I want to configure Claude Desktop to use Microsoft Foundry as its inference provider so that my organization can run Claude Cowork and Claude Code with Azure-managed billing, enterprise security, and local conversation storage.
---

# Configure Claude Desktop for Microsoft Foundry

Anthropic's Claude Desktop runs the Claude Cowork and Claude Code clients. When you configure Claude Desktop to use Microsoft Foundry as the inference provider, all Claude model requests route through your own Foundry resource. Billing stays on your Azure account, conversations remain on user devices, and you can deploy and manage the app through your existing enterprise Mobile Device Management (MDM) tools such as Microsoft Intune, Group Policy, or Jamf.

This article shows you how to set up Claude Desktop with a Microsoft Foundry inference provider, for a single device or for an entire fleet.

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go). Free trial, student, credit–based accounts, Enterprise accounts in South Korea, and Cloud Solution Provider subscriptions aren't supported for Claude models. For details on these restrictions, see [subscription type and region support](#subscription-type-and-region-support).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A Microsoft Foundry resource with one or more Claude models deployed. See [Deploy and use Claude models in Microsoft Foundry (preview)](use-foundry-models-claude.md).
- Your Foundry resource name. In the Foundry portal, select your project name > **Project details** > **Parent resource** to find it.
- An API key for your Foundry deployment.


### Subscription type and region support

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

## Set up a single machine

> [!IMPORTANT]
> Claude models in Microsoft Foundry are currently in preview. Model availability might change. Check the [Foundry Models from partners](../concepts/models-from-partners.md) page for the latest list of available models.

Use this procedure for evaluation or pilot use on an individual device.

1. Install Claude Desktop from [claude.com/download](https://claude.com/download).

1. Open Claude Desktop, then select **Help** > **Troubleshooting** > **Enable Developer Mode**.

1. Select **Developer** > **Configure third-party inference** to open the configuration window. The window is organized into seven sections in the left sidebar. Work through them in order; each maps to a group of configuration keys, and the window validates values as you enter them.

1. Select the **Connection** section on the configuration window.

1. Select **Foundry** as the inference provider.

1. Enter your Foundry resource name and API key.

1. Set your model list by entering your Foundry model deployment names. The first entry in the list is the default model.

1. Configure settings in the other sections of the configuration window. For details on these, see [Build a configuration in the app](https://claude.com/docs/cowork/3p/installation#2-build-a-configuration-in-the-app).

1. Select **Apply locally**. Claude Desktop relaunches in third-party (3P) mode.

1. On the sign-in screen, choose **Start in Cowork on 3P** to begin using Claude Cowork with your Foundry deployment.

## Deploy to your organization with MDM

For fleet-wide rollout via Microsoft Intune, Group Policy, or Jamf, use a managed configuration instead of per-device setup. For a full list of managed configuration keys, see the [Cowork on 3P configuration reference](https://claude.com/docs/cowork/3p/configuration).

1. Complete the single-machine setup on an admin device to validate your configuration.

1. In the configuration window, review the **Firewall allowlist** section and add the listed hostnames to your network egress rules.

1. In the same configuration window, select **Export configuration**. On Windows, save the file as a `.reg` file. On macOS, save it as a `.mobileconfig` file.

1. Deploy the exported configuration file through your MDM to your target device groups.

1. Push the Claude Desktop installer to enrolled devices. When the app launches and finds a managed configuration, it enters 3P mode automatically without requiring users to sign in.

For more details about installing Claude Desktop, see [Installation and setup](https://claude.com/docs/cowork/3p/installation).

## Telemetry and session monitoring

You can export full session telemetry to your own OpenTelemetry collector for audit and usage tracking. Events include:

- User prompts and API requests (with token counts and estimated cost)
- Tool execution results (success/failure, duration)
- Errors and performance metrics
- Session and user attribution for per-team cost breakdowns

Anthropic-bound telemetry (crash reports and product analytics) contains no conversation content and can be fully disabled via managed configuration. For details, see [Telemetry and egress](https://claude.com/docs/cowork/3p/telemetry-egress).

## Operational considerations

- **Data residency**: Conversations are stored on the user's local device. Inference requests go to your Microsoft Foundry endpoint.
- **Compliance**: Anthropic has noted that data-residency and "no conversation data sent to Anthropic" guarantees equivalent to those for Vertex AI and Amazon Bedrock are coming for Microsoft Foundry. Refer to [Anthropic's documentation](https://claude.com/docs/cowork/3p/overview) for the latest status.
- **Billing**: All inference is billed through your Azure account as token-based consumption. There's no seat licensing from Anthropic.
- **Updates**: Auto-updates are enabled by default. You can disable them and redistribute builds through your MDM on your own schedule.

## Related content

- [Configure Claude Code for Microsoft Foundry](configure-claude-code.md)
- [Deploy and use Claude models in Microsoft Foundry (preview)](use-foundry-models-claude.md)
- [Claude Docs: Cowork on 3P — Overview](https://claude.com/docs/cowork/overview) 
- [Claude Docs: Claude Code Overview](https://code.claude.com/docs/en/overview) 