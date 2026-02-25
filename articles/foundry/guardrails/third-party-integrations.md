---
title: "Integrate third-party guardrails with Microsoft Foundry (temp)"
description: "Learn how to connect external safety solutions to AI models and agents in Microsoft Foundry using third-party integrations. (temp)"
ms.date: 02/24/2026
ms.custom: ai-assisted, references_regions
ms.author: pafarley
author: PatrickFarley
ms.service: azure-ai-content-safety
ms.topic: how-to

---

# Integrate third-party guardrails (temp)

Microsoft Foundry supports third-party safety and security integrations. You can connect external solutions to your AI models and agents at runtime to enhance Foundry Guardrails & Controls with best-in-class security capabilities from trusted partners.

## Prerequisites

Before you set up the integration, ensure you have:

- **Azure subscription**: You need the Owner role on the subscription.
- **Key Vault**: Create at least one Key Vault with the Key Vault Administrator role assigned to you.
- **Foundry project**: Create a project with the Azure AI User and Azure AI Account Owner roles assigned to you.
- **Managed Identity**: Create at least one user-assigned Managed Identity and attach it to the Foundry resource in the Azure portal under **Resource Management** > **Identity**.

## Palo Alto Networks Prisma AIRS

Palo Alto Networks Prisma AIRS delivers runtime security for AI applications, models, and agents. Prisma AIRS scans for threats, blocks unsafe behavior, and provides actionable alerts.

### License and data processing

Palo Alto Networks Prisma AIRS uses a Bring Your Own License (BYOL) approach. You can use your existing third-party software licenses from supported partners. Your data is processed outside of Foundry using the service you selected. The terms and privacy commitments for the other service apply to this processing.

### Register and connect to Prisma AIRS

To register your Prisma AIRS integration:

1. Follow the [Prisma AIRS onboarding steps](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/onboard-api-runtime-security-api-intercept-in-scm) to retrieve your API key linked to your custom security profile.
1. In Foundry, select **Guardrails**.
1. Select the **Integrations** tab, then select **Add integration** > **Palo Alto Networks Prisma AIRS**.
1. Select a Key Vault and Managed Identity.
1. Add the Prisma AIRS endpoint and API key. To get the endpoint and API key pair, complete the [Palo Alto Networks Prisma AIRS onboarding flow](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/onboard-api-runtime-security-api-intercept-in-scm).

You only need to return to this step if you rotate your API key or change components such as Managed Identity or Key Vault.

#### Region availability 

The following table shows supported regions. We recommend that your Foundry project is in the same region as the Palo Alto Networks Prisma AIRS endpoint. Different regions can cause higher latency and potential timeouts.

| Azure Region | Recommended integration endpoint |
|--------------|----------------------------------|
| West US | US |
| West US3 | US |
| West Central US | US |
| Germany West Central | Europe |
| West Europe | Europe |
| France Central | Europe |
| Switzerland North | Europe |
| Switzerland West | Europe |
| Sweden Central | Europe |
| Italy North | Europe |
| Norway East | Europe |
| North Europe | Europe |
| UK South | Europe |
| UK West | Europe |
| South India | India |
| Southeast Asia | Singapore |
| East Asia | Singapore |

### Attach and test the integration

To attach the integration to your guardrails:

1. Select one or more Foundry guardrails to attach the integration.
1. Select **Save**, and confirm the integration and guardrail attachment in the integrations table.
1. Verify the status. **Running** indicates a successful connection. Error messages provide specific recommendations, such as **Missing Managed Identity**.
1. [Assign a Foundry custom guardrail](/azure/ai-foundry/guardrails/guardrails-overview) with an active third-party integration to a model or agent.
1. Test the setup in the playground.

## Test with code

The following example shows how to test the integration using the OpenAI Python SDK. This code sends a request that violates the configured safety policy and demonstrates the content filtering response.

```python
from openai import OpenAI

# Replace with your endpoint and API key
endpoint = "<your-endpoint>"
deployment_name = "gpt-5.2-chat"
api_key = "<your-api-key>"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "<prompt-that-violates-rai-policy>",
        }
    ],
    temperature=0.7,
)

print(response)
```

## Output

```console
openai.BadRequestError: Error code: 400 - 
{
  "error": {
    "message": "The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry. To learn more about our content filtering policies please read our documentation: https://go.microsoft.com/fwlink/?linkid=2198766",
    "type": null,
    "param": "prompt",
    "code": "content_filter",
    "status": 400
  }
}

{
  "innererror": {
    "code": "ResponsibleAIPolicyViolation",
    "content_filter_result": {
      "external_safety_provider": {
        "detected": true,
        "filtered": true,
        "results": [
          {
            "provider_name": "Palo Alto Networks Prisma AIRS",
            "error": false,
            "detected": true,
            "filtered": true,
            "role": "User",
            "source": "AI-Runtime-Azure-AI-Foundry",
            "details": {
              "created_at": "2026-02-18T01:11:29.3949427Z",
              "completed_at": "2026-02-18T01:11:29.436312651Z",
              "detections": {
                "action": "block",
                "category": "malicious",
                "content_detected": {
                  "injection": false,
                  "toxic_content": true
                }
              }
            },
            "profile_id": "b44235eb-2960-49f9-bc44-13c69cb3f5f6",
            "profile_name": "safety-provider-do-not-use",
            "scan_id": "c41ac678-c675-4180-9f74-a109a25457cc",
            "report_id": "Rc41ac678-c675-4180-9f74-a109a25457cc",
            "session_id": "182e5add-f49a-4a63-931f-30c864866dd6",
            "tr_id": "182e5add-f49a-4a63-931f-30c864866dd6"
          }
        ]
      },
      "hate": {
        "filtered": false,
        "severity": "safe"
      },
      "self_harm": {
        "filtered": false,
        "severity": "safe"
      },
      "sexual": {
        "filtered": false,
        "severity": "safe"
      },
      "violence": {
        "filtered": false,
        "severity": "safe"
      },
      "jailbreak": {
        "detected": false,
        "filtered": false
      }
    }
  }
}
```

## Next steps

- [Learn about Foundry Guardrails](/azure/ai-foundry/guardrails/guardrails-overview)
