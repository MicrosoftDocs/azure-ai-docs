---
title: "Integrate third-party guardrails with Microsoft Foundry"
description: "Learn how to connect external safety solutions to AI models and agents in Microsoft Foundry using third-party integrations."
ms.custom: ai-assisted, references_regions
ms.author: pafarley
author: PatrickFarley
ms.service: azure-ai-content-safety
ms.topic: how-to
---

# Integrate third-party guardrails
Microsoft Foundry supports third-party safety and security integrations. You can connect external solutions to your AI models and agents at runtime to enhance Foundry Guardrails & Controls with best-in-class security capabilities from trusted partners.


## Prerequisites

Before you set up the integration, ensure you have:

- **Azure subscription**: You need the Owner role on the subscription.
- **Key Vault**: Create at least one Key Vault with the Key Vault Administrator role assigned to you.
- **Foundry project**: Create a project with the Azure AI User and Azure AI Account Owner roles assigned to you.
- **Managed Identity**: Create at least one user-assigned Managed Identity and attach it to the Foundry resource in the Azure portal under **Resource Management** > **Identity**.

### Enablement and data processing 
Third-party integrations  are enabled via a Bring Your Own License (BYOL) approach, allowing you to utilize existing third-party software licenses from supported partners. Your data will be processed outside of Azure AI Foundry using the service you selected. The terms and privacy commitments for your other service will apply to this processing. 

## Third-party integrations

This section links resources to 3rd party instructions on retrieving API keys and creating custom profiles. In the [Steps to connect integration](#steps-to-connect-integration) section, you can use these links to continue connecting your integration. 

| Model   | onboarding step |
|--------------------|----------------------|
| Zenity  | [AIDR](https://zenity.io/platform/ai-security-platform/aidr).     |
| Palo Alto Networks |  [Prisma AIRS](https://docs.paloaltonetworks.com/ai-runtime-security/activation-and-onboarding/ai-runtime-security-api-intercept-overview/onboard-api-runtime-security-api-intercept-in-scm) |

## Steps to connect integration

1. Follow the [Third-party integrations steps](#third-party-integrations) and retrieve your API key linked to your custom security profile. 
1. Go to AI Foundry and select **Guardrails**. 
1. Select the Integrations tab, add a third-party integration and select Zenity. 
1. Select a Keyvault and Managed Identity. Learn more. 
1. Add the endpoint(s) and API key(s). To get the endpoint-API key pair, follow the [Third-party integrations steps](#third-party-integrations).


#### Region availability 

The following table shows supported regions. We recommend that your Foundry project is in the same region as the Third-party endpoint. Different regions can cause higher latency and potential timeouts.

| Azure Region | Recommended Endpoint | Third-party Integration |
|---|---|---|
| West US | US | Zenity, Palo Alto Networks Prisma AIRS |
| West US 2 | US | Zenity |
| West US 3 | US | Zenity, Palo Alto Networks Prisma AIRS |
| West Central US | US | Zenity, Palo Alto Networks Prisma AIRS |
| Central US | US | Zenity |
| North Central US | US | Zenity |
| South Central US | US | Zenity |
| East US | US | Zenity |
| East US 2 | US | Zenity |
| Canada Central | US | Zenity |
| Canada East | US | Zenity |
| West Europe | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| North Europe | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| France Central | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Germany West Central | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Italy North | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Spain Central | Europe | Zenity |
| Sweden Central | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Norway East | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Switzerland North | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| Switzerland West | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| UK South | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| UK West | Europe | Zenity, Palo Alto Networks Prisma AIRS |
| South India | India | Palo Alto Networks Prisma AIRS |
| Southeast Asia | Singapore | Palo Alto Networks Prisma AIRS |
| East Asia | Singapore | Palo Alto Networks Prisma AIRS |




## Attach Integrations to Foundry Guardrails

1. Select one or more Foundry Guardrails to attach the integration.
1. Select **Save** and confirm integration and guardrail attachment in the integrations table.
1. Confirm the status:Running indicates a successful connection.
1. Error messages provide concrete recommendations (for example, missing Managed Identity).
1. Follow the main Foundry Guardrail flow to [assign a custom guardrail](guardrails-overview.md) with an active third-party integration to a model or agent.
1. Test in Playground.


## Code Examples

Examples adapted from Guardrail annotations – [Microsoft Foundry](/azure/ai-foundry/openai/concepts/content-filter-annotations): 

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
