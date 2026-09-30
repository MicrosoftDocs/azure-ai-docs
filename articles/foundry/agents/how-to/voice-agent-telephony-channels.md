---
title: "Integrate telephony channels with a voice agent"
description: "Use Teams Phone extensibility or Twilio with a Microsoft Foundry voice agent to receive phone calls and place outbound calls through the API."
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/25/2026
ms.custom: preview
ai-usage: ai-assisted
#customer intent: As a developer, I want to connect Teams or Twilio to my voice-first agent so that it can receive calls and place outbound calls.
---

# Integrate telephony channels with a voice agent

Use [Teams Phone extensibility (TPE)](/azure/communication-services/concepts/interop/tpe/teams-phone-extensibility-overview) or Twilio to connect a phone number to your Microsoft Foundry voice agent. Receive inbound calls and place outbound calls through the call-job API.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- A saved voice-first agent in a Foundry project that passes browser testing. See [Quickstart: Create a voice-first prompt agent](../quickstarts/prompt-voice-agent.md).
- [Foundry User role](../../concepts/rbac-foundry.md) on the project, to create and manage telephony bindings.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

- Permission to update the agent and its channels, manage project connections, and create or update telephony bindings.

### Teams Phone extensibility prerequisites

For the Teams Phone extensibility path, you need:

- A Teams Phone service number assigned to a resource account. See [Get Microsoft Teams Calling Plan phone numbers for your tenant](/microsoftteams/getting-phone-numbers-for-your-users).
- The setup in [Prepare Teams Phone extensibility](#prepare-teams-phone-extensibility), completed with a Teams or Microsoft 365 administrator.
- Access to the selected Azure Communication Services resource.
- For inbound calls, Event Grid write permission on that resource.
- Help from a tenant administrator when secure webhook setup requires Microsoft Entra application or app-role changes.

The current project-managed-identity flow requires the Foundry project and Azure Communication Services resource to be in the same Microsoft Entra tenant.

### Twilio prerequisites

For the Twilio path, you need:

- A [Twilio](https://www.twilio.com/phone-numbers) account with at least one active, voice-capable phone number for inbound calls.
- A Twilio project connection, or the **Account SID** and **Primary Auth Token** to create one.

Twilio doesn't require an Azure Communication Services resource, Teams resource account, or Event Grid subscription. Store the Auth Token in the project connection, not in binding requests, logs, screenshots, or support requests.

## Compare the channel integrations

Choose the provider that owns your number.

| Path | Use it when | What you provide in Foundry |
| --- | --- | --- |
| Teams Phone extensibility | Your organization owns a service number in Teams and routes it through a Teams resource account to Azure Communication Services. | An Azure Communication Services project connection and the resource-account object ID as a GUID, without the `28:orgid:` prefix. |
| Twilio | Your organization owns one or more active voice-capable numbers in Twilio. | An existing Twilio project connection, or the Account SID and Primary Auth Token for a new connection. |

The Twilio option appears only in supported public-cloud environments.

## Understand the call path

The channel integration determines how an inbound call reaches the agent.

```text
Caller
  -> Teams resource-account number or Twilio number
  -> telephony provider
  -> Foundry project telephony endpoint
  -> telephony binding
  -> voice-based agent
```

For Teams Phone extensibility, your Teams tenant keeps ownership of the number and Azure Communication Services provides the call automation and media path:

1. A caller dials the Teams phone number.
1. Teams routes the call to your resource account.
1. The resource account routes the call to your Communication Services resource.
1. Communication Services raises a `Microsoft.Communication.IncomingCall` event through Event Grid to your agent's telephony callback endpoint.
1. Foundry matches the callee to a telephony binding, answers the call on your Communication Services resource, and streams the audio to the agent.

Because the Teams number stays in Teams, the agent can act as one destination among others in your existing call flow. You can leave auto attendants and call queues in place and route selected paths to the agent.

For Twilio, Foundry uses the selected project connection to discover the numbers in your Twilio account and create a binding for each number you select. You don't create an Azure Communication Services resource or Event Grid subscription for the Twilio path.

## Prepare Teams Phone extensibility

A Teams or Microsoft 365 administrator usually completes these steps. Skip this section for Twilio.

1. Follow [Teams Phone System extensibility quick start](/azure/communication-services/quickstarts/tpe/teams-phone-extensibility-quickstart) to provision the application, bot, resource account, and Azure Communication Services association.
1. Create or select the Azure Communication Services resource that receives calls for the resource account.
1. Create the Teams resource account with the Phone Extensibility application ID.
1. Associate the resource account with the Azure Communication Services resource, and synchronize the resource account.
1. Acquire a Teams service number and assign it to the resource account. The number can use Calling Plan, Operator Connect, or Direct Routing according to your Teams telephony configuration.
1. Assign the **Microsoft Teams Phone Resource Account** license when required.
1. Provide Azure Communication Services server consent for the exact tenant and resource-account object ID.
1. For inbound calls, place a controlled call and confirm that Azure Communication Services emits `Microsoft.Communication.IncomingCall`.

Provide the Foundry owner with the callable Teams number, Azure Communication Services ARM resource ID, and resource-account object ID. For inbound setup, also confirm that Azure Communication Services received the test call.

<!-- Screenshot: Teams resource account showing the service number and application association. Alt text: "Teams resource account with its assigned service number and Phone Extensibility application." -->

## Set up your preferred interface

Choose **Foundry portal**, **Python SDK**, or **REST**. The Python examples share a client and variables across sections.

# [Foundry portal](#tab/portal)

Open your project in the [Foundry portal](https://ai.azure.com). You don't need the Python packages or a manually acquired bearer token for the portal steps.

# [Python SDK](#tab/python)

Use Python 3.10 or later and install the packages:

```bash
python -m pip install "azure-ai-projects>=2.7.0" azure-identity
```

For local development, sign in with `az login` before using `DefaultAzureCredential`. Replace the endpoint and agent name, then run this setup once in your Python session:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

endpoint = "https://<account>.services.ai.azure.com/api/projects/<project>"
agent_name = "my-voice-agent"
credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=endpoint, credential=credential)
telephony = project_client.beta.voice_agents.telephony
```

Reference: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient) | [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential).

The beta client uses `api-version=v1` and adds `Foundry-Features: VoiceAgents=V1Preview` automatically. These operations don't require `allow_preview=True`.

Examples that need response headers use the `cls` callback to return the model and raw HTTP headers together. After running the examples you need, close `project_client` and `credential` with their `close()` methods.

# [REST](#tab/rest)

Replace `{projectEndpoint}` with your Foundry project endpoint and `{agentName}` with the voice agent's name. Send a Microsoft Entra bearer token for `https://ai.azure.com/` and `Foundry-Features: VoiceAgents=V1Preview` on every request. The examples use `api-version=v1`.

---

## Configure a provider connection

Use a project connection for your provider. The portal number setup flow can create it for you. For SDK or REST requests, create or select the connection first.

### Create a connection to Communication Services

For Teams, use the category `AzureCommunicationServices`. Set `target` to the resource's HTTPS endpoint, such as `https://<resource-name>.communication.azure.com`, not its Azure resource ID. Store the matching resource ID in `ResourceId` metadata.

Choose an authentication type supported by the connection:

| Authentication | `authType` | What you provide |
| --- | --- | --- |
| Project managed identity | `ProjectManagedIdentity` | Grant the project identity access to the Communication Services resource. |
| Account managed identity | `AccountManagedIdentity` | Grant the Foundry account identity access to the resource. |
| User-assigned managed identity | `RegistryIdentity` | Identity resource ID and client ID, with access to the resource. |
| Service principal | `ServicePrincipal` | Tenant ID, client ID, and client secret, with access to the resource. |
| Connection string | `CustomKeys` | The Communication Services connection string in the `connectionString` credential key. |

For a managed identity or service principal, grant the required Communication Services permissions before creating a binding or placing calls.

### Configure the Twilio project connection

For Twilio, use these settings:

| Setting | Value |
| --- | --- |
| `category` | `Twilio`. |
| `target` | Your Twilio Account SID, not a Twilio API URL or phone number. |
| `authType` | `ApiKey`. |
| Credential `key` | Your Twilio Primary Auth Token. |

Use the connection's name as `connection_name` in binding and outbound requests. Don't include provider credentials in those requests.

## Understand telephony bindings

A binding routes inbound calls to one agent. You don't need a binding for outbound call jobs.

| Property | Purpose |
| --- | --- |
| `id` | Service-generated binding ID for later reads, updates, and deletion. |
| `provider` | `teams_phone_extension` or `twilio`. |
| `connection_name` | Foundry project connection name. Secrets stay in the connection. |
| `resource_account_object_id` | Required Teams resource-account GUID, without `28:orgid:`. Don't send this property for Twilio. |
| `phone_number` | Optional display metadata for Teams; required owned E.164 number for Twilio. |
| `status` | `active` or `suspended`. Suspension stops new inbound calls without deleting the binding. |
| `label` | Optional display label. |
| `incoming_call_url` | Service-generated incoming-call delivery URL. |

Create and list bindings at `{projectEndpoint}/agents/{agentName}/telephony/bindings`. Append `/{bindingId}` to read, update, or delete one. Use the latest ETag for conditional updates and deletion.

Creating a Twilio binding updates the number's voice URL and status callback, replacing its existing inbound voice routing. Use a number you want to route to this agent.

# [Foundry portal](#tab/portal)

## Connect a number in the Foundry portal

The portal provides separate setup flows for Teams Phone extensibility and Twilio. Select **Microsoft Teams** for the Teams Phone extensibility flow.

### Open the phone-number channel

1. In Foundry, open **Build** > **Agents**.
1. Select the voice-based agent.
1. Open **Channels**.
1. In **Phone numbers**, select **Add a number**.
1. Select **Microsoft Teams** or **Twilio**.

<!-- Screenshot: Voice-first Channels page with Add a number, Microsoft Teams, and Twilio highlighted. Alt text: "Phone numbers channel menu for a voice-first agent with Microsoft Teams and Twilio options." -->

### Connect a Microsoft Teams number

The Teams Phone extensibility flow creates or updates the Azure Communication Services project connection and telephony binding. Depending on the secure-delivery option, Foundry can also configure the webhook application and IncomingCall Event Grid subscription.

#### Choose secure incoming-call delivery

When **Secure incoming-call delivery** is shown, choose the approved mode.

| Option | Use it when |
| --- | --- |
| **Automatic configuration (Recommended)** | Use when the tenant allows Foundry to create or update the webhook app, app-role assignments, and Event Grid subscription. |
| **Manual configuration** | Use an approved customer-managed application, or select an existing Event Grid and app-registration configuration. |

Under **Manual configuration**, choose the option that matches your setup:

- **Use a customer-managed app registration and let Foundry configure Event Grid**: Use a dedicated single-tenant application that you own, or ask an administrator to complete the changes.
- **Event Grid and app registration are already configured**: Use only when authenticated Event Grid delivery to the exact Foundry webhook is complete. Foundry skips that bootstrap work.

For a customer-managed application:

1. Select an eligible single-tenant app registration.
1. Enter any governance reference required by your organization.
1. If the application isn't listed, confirm that you're an owner and refresh.
1. Ask a tenant administrator to complete required API permissions and app-role assignments.

Never disable authentication to work around a webhook validation error.

<!-- Screenshot: Secure-delivery choices and app-registration picker. Alt text: "Microsoft Teams phone-number dialog showing secure Event Grid delivery options." -->

#### Select Azure Communication Services

In **Azure Communication Services resource**, select the resource that receives the calls.

If it isn't listed:

- Confirm the tenant and subscription.
- Confirm you can read the resource.
- Confirm the expected resource provider is registered.
- Ask an Azure administrator to correct RBAC.

Foundry creates or updates the project connection to the Azure Communication Services endpoint and uses the project managed identity. Don't enter an Azure Communication Services key or connection string.

#### Enter the Teams number details

Enter the **Resource account object ID** that the Teams administrator provides. Foundry constructs:

```text
28:orgid:<resource-account-object-id>
```

### Connect a Twilio number

1. In **Phone numbers**, select **Add a number** > **Twilio**.
1. Select a compatible existing Twilio connection. If none is available, select **Create a new Twilio connection**.
1. To create a connection, enter:
   - A unique **Connection name**.
   - The Twilio **Account SID**. It starts with `AC` and contains 34 characters.
   - The Twilio **Primary Auth Token**.
1. Select **Connect** or **Continue**.
1. Select one or more voice-capable phone numbers discovered from the Twilio account. You can't select numbers without the Voice capability.
1. Select **Continue**.
1. Review the agent, connection, masked Account SID, and selected numbers.
1. Optionally change the display label for each number.
1. Select **Add selected numbers**.
1. Review the result for each number. Retry any number that has a failed or unconfirmed result.
1. Select **Done** after all binding operations finish.

Foundry stores the Twilio credentials in the project connection and creates a separate telephony binding for each selected number.

If you don't find any voice-capable numbers, get a number in the Twilio Console and retry discovery.

<!-- Screenshot: Twilio add-number wizard showing connection selection, discovered voice-capable numbers, and review step. Alt text: "Twilio phone-number wizard with a project connection and selected voice-capable numbers." -->

### Manage a connected number

The **Phone numbers** card shows each connected number, its optional label, and its provider.

1. Open the number's actions menu.
1. Select **View details**.
1. Select **Edit** if the binding supports updates.
1. For Microsoft Teams, update the displayed phone number or label. The resource-account object ID and connection are read-only.
1. For Twilio, update the label. The phone number and connection are read-only.
1. Select **Save**.

# [Python SDK](#tab/python)

## Connect a number with the Python SDK

Use the client from [Set up your preferred interface](#set-up-your-preferred-interface) and your [provider connection](#configure-a-provider-connection). Choose one of the following request models, and then create the binding.

For **Teams Phone extensibility**, use your resource-account GUID. The phone number is optional display metadata.

```python
from azure.ai.projects.models import (
    CreateTeamsPhoneExtensionTelephonyBindingRequest,
)

binding_request = CreateTeamsPhoneExtensionTelephonyBindingRequest(
    connection_name="my-acs-connection",
    resource_account_object_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    phone_number="+12065550123",
    label="Support line",
)
```

Reference: [CreateTeamsPhoneExtensionTelephonyBindingRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createteamsphoneextensiontelephonybindingrequest).

For **Twilio**, use an owned, voice-capable E.164 number. Don't send Teams resource-account fields.

```python
from azure.ai.projects.models import CreateTwilioTelephonyBindingRequest

binding_request = CreateTwilioTelephonyBindingRequest(
    connection_name="my-twilio-connection",
    phone_number="+12065550123",
    label="Support line",
)
```

Reference: [CreateTwilioTelephonyBindingRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createtwiliotelephonybindingrequest).

After running the request-model snippet for your provider, create its binding:

```python
binding = telephony.create_binding(
    agent_name=agent_name,
    telephony_binding=binding_request,
)
binding_id = binding.id
print(binding_id, binding.incoming_call_url)
```

Reference: [BetaVoiceAgentsTelephonyOperations.create_binding](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Save `binding_id` for later requests. For Teams, use `incoming_call_url` to [register the Event Grid subscription](#register-the-event-grid-subscription). For Twilio, Foundry configures callbacks automatically.

To suspend new inbound calls, read the binding's latest ETag and pass it to `update_binding` with `MatchConditions.IfNotModified`:

```python
from azure.ai.projects.models import UpdateTelephonyBindingRequest
from azure.core import MatchConditions

binding, binding_headers = telephony.get_binding(
    agent_name=agent_name,
    binding_id=binding_id,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
binding = telephony.update_binding(
    agent_name=agent_name,
    binding_id=binding_id,
    body=UpdateTelephonyBindingRequest(status="suspended"),
    etag=binding_headers["ETag"],
    match_condition=MatchConditions.IfNotModified,
)
```

Reference: [BetaVoiceAgentsTelephonyOperations](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations) | [MatchConditions](/python/api/azure-core/azure.core.matchconditions).

Read the latest ETag before every update. The [binding update rules](#binding-update-rules) apply to either interface.

# [REST](#tab/rest)

## Connect a number by using the API

Use your [provider connection](#configure-a-provider-connection) and the authentication headers from [Set up your preferred interface](#set-up-your-preferred-interface).

### Create the binding

For **Teams Phone extensibility**, set `connection_name` to your ACS connection and `resource_account_object_id` to your Teams resource-account GUID. The optional `phone_number` is display metadata, not the routing identifier.

```http
POST {projectEndpoint}/agents/{agentName}/telephony/bindings?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json

{
  "provider": "teams_phone_extension",
  "connection_name": "my-acs-connection",
  "resource_account_object_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "phone_number": "+12065550123",
  "label": "Support line"
}
```

For **Twilio**, send the same `POST` request with this JSON body instead:

```json
{
  "provider": "twilio",
  "connection_name": "my-twilio-connection",
  "phone_number": "+12065550123",
  "label": "Support line"
}
```

Reference: [CreateTwilioTelephonyBindingRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createtwiliotelephonybindingrequest).

Replace the example identifiers and numbers with your values. Use `connection_name`, not the legacy `connection` alias. Don't send `identifier`, `provider_config`, or Teams fields in a Twilio request.

The service returns `201 Created`, the binding's `id` and `incoming_call_url`, and an `ETag` header. Save the binding ID. For Teams, [register the Event Grid subscription](#register-the-event-grid-subscription); for Twilio, Foundry configures callbacks automatically.

### Read or update the binding

Read the binding to get its current properties and `ETag`:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Use `PATCH` with `application/merge-patch+json` to update the binding. For example, suspend new inbound calls without deleting the binding:

```http
PATCH {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/merge-patch+json
If-Match: <etag-from-latest-binding-read>

{
  "status": "suspended"
}
```

Read the latest `ETag` before each update. Don't reuse an ETag after another change.

---

### Binding update rules

Set `status` to `active` to accept new inbound calls again. Both providers support updates to `status` and `label`.

Teams bindings also support changes to `connection_name` and the display `phone_number`. The provider and resource-account object ID are immutable. For Twilio, delete and recreate the binding to change its phone number or connection.

### Register the Event Grid subscription

This section applies only to **Teams inbound calls**, not Twilio or outbound-only setup. Create an Event Grid subscription on the Communication Services resource that targets the binding's `incoming_call_url`. If the portal already configured secure delivery, don't create a duplicate subscription.

Before running the Bash example, sign in with `az login` and set these variables:

| Variable | Value |
| --- | --- |
| `eventSubscriptionName` | A name for the Event Grid event subscription. |
| `acsResourceId` | The Azure resource ID of the Communication Services resource. |
| `webhook` | The `incoming_call_url` returned when you create the binding. |
| `webhookTenantId` | The tenant ID configured for the webhook application. |
| `webhookApplicationIdOrUri` | The webhook application's client ID or Application ID URI. |

Complete the application and role setup in [Deliver events to Microsoft Entra protected endpoints](/azure/event-grid/secure-webhook-delivery) first. Obtain the webhook tenant and audience from the administrator who configures secure incoming-call delivery. The webhook application identifies the token audience; it isn't the Microsoft Event Grid first-party application.

```azurecli
az eventgrid event-subscription create \
  --name "$eventSubscriptionName" \
  --source-resource-id "$acsResourceId" \
  --endpoint-type webhook \
  --endpoint "$webhook" \
  --included-event-types Microsoft.Communication.IncomingCall \
  --event-delivery-schema eventgridschema \
  --azure-active-directory-tenant-id "$webhookTenantId" \
  --azure-active-directory-application-id-or-uri "$webhookApplicationIdOrUri"
```

Reference: [az eventgrid event-subscription create](/cli/azure/eventgrid/event-subscription#az-eventgrid-event-subscription-create).

During creation, Event Grid sends a validation event that the endpoint answers automatically.

Foundry validates the Microsoft Entra token that Event Grid attaches to each delivery, and then requires an active binding whose project, agent, Communication Services resource, and callee all match the event. Calls that don't match a binding aren't answered.

Event Grid allows up to 500 event subscriptions per system topic. Plan incoming-call delivery within the [Event Grid quotas and limits](/azure/event-grid/quotas-limits).

## Place outbound calls by using the API

Create an outbound call job to call a phone number through a project connection. Creating a call job doesn't change inbound routing.

Complete [Set up your preferred interface](#set-up-your-preferred-interface) before running the Python or REST examples. Use a destination you have permission to call.

Create or select the [provider connection](#configure-a-provider-connection), but skip the inbound binding and Event Grid procedures for outbound-only use.

### Set the outbound caller and destination

The connection category selects the provider. Use these required settings:

| Field | Teams Phone extensibility | Twilio |
| --- | --- | --- |
| `connection_name` | The name of an `AzureCommunicationServices` connection in the current project. | The name of a `Twilio` connection in the current project. |
| `source` | The Teams resource-account object ID as a nonzero GUID. Don't include `28:orgid:` or use the account's display phone number. | An E.164 caller number authorized for the connected Twilio account. |
| `destination` | `{"type": "phone_number", "value": "+14255550123"}` with the recipient's E.164 number. | The same phone-number destination shape. |

Supply a connection name, not a resource ID or URL. Don't send `provider`, `telephony_binding_id`, or the legacy `connection` field in an outbound request.

Generate an idempotency key of 1 to 256 characters for each new call intent. Reuse it with an equivalent request when retrying an uncertain response. The service returns the same job; reusing the key with a different request returns `409 Conflict`.

Creation returns `202 Accepted` with the job's `id`, `ETag`, `Location`, and `Retry-After` in seconds. Acceptance doesn't mean the recipient answered or the call completed.

The service resolves the latest saved agent definition for each attempt. Provide any required agent inputs in `structured_inputs`.

# [Foundry portal](#tab/portal)

This section covers outbound calls through the API. Select **Python SDK** or **REST** to create, read, or cancel a call job. You can use a project connection created in the portal without creating an inbound binding.

# [Python SDK](#tab/python)

### Create an outbound job with Python

Choose the caller settings for your provider. Run only one of these assignments, replacing the example values.

For **Teams Phone extensibility**:

```python
connection_name = "my-acs-connection"
source = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
```

For **Twilio**:

```python
connection_name = "my-twilio-connection"
source = "+14255550100"
```

Then create one job with those settings and an approved destination:

```python
from uuid import uuid4

from azure.ai.projects.models import (
    CreateTelephonyCallJobRequest,
    TelephonyOutboundDestination,
)

idempotency_key = str(uuid4())
job, job_headers = telephony.create_call_job(
    agent_name=agent_name,
    body=CreateTelephonyCallJobRequest(
        connection_name=connection_name,
        source=source,
        destination=TelephonyOutboundDestination(
            type="phone_number", value="+14255550123"
        ),
    ),
    idempotency_key=idempotency_key,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
call_job_id = job.id
retry_after = int(job_headers["Retry-After"])
print(call_job_id, job.status)
```

Reference: [CreateTelephonyCallJobRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createtelephonycalljobrequest) | [BetaVoiceAgentsTelephonyOperations.create_call_job](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Save `idempotency_key`, `call_job_id`, and the response headers. Add any required `structured_inputs` to the request model. You can also pass the [optional outbound settings](#optional-outbound-settings).

### Read an outbound job with Python

Wait for the interval from the create response before reading the job:

```python
import time

time.sleep(retry_after)
job, job_headers = telephony.get_call_job(
    agent_name=agent_name,
    call_job_id=call_job_id,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
print(job.status, job.attempt_count, job.terminal_reason)
```

Reference: [BetaVoiceAgentsTelephonyOperations.get_call_job](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Repeat the read at that interval while the job is nonterminal. Keep `retry_after` from creation; a read doesn't necessarily return that header.

### Cancel an outbound job with Python

Read the job again to get its current ETag before requesting cancellation:

```python
from azure.core import MatchConditions

job, job_headers = telephony.get_call_job(
    agent_name=agent_name,
    call_job_id=call_job_id,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
job = telephony.cancel_call_job(
    agent_name=agent_name,
    call_job_id=call_job_id,
    etag=job_headers["ETag"],
    match_condition=MatchConditions.IfNotModified,
)
print(job.status)
```

Reference: [BetaVoiceAgentsTelephonyOperations.cancel_call_job](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations) | [MatchConditions](/python/api/azure-core/azure.core.matchconditions).

Use the job's ETag, not a binding's ETag. Continue reading until the job is terminal.

# [REST](#tab/rest)

### Create a call job

Send `POST` to `call_jobs` with an underscore and `api-version=v1`. This example uses Teams Phone extensibility:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/call_jobs?api-version=v1
Authorization: Bearer <token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json
Idempotency-Key: <unique-request-key>

{
  "connection_name": "my-acs-connection",
  "source": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "destination": {
    "type": "phone_number",
    "value": "+14255550123"
  }
}
```

Reference: [CreateTelephonyCallJobRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createtelephonycalljobrequest).

For **Twilio**, send the same `POST` request with this JSON body instead:

```json
{
  "connection_name": "my-twilio-connection",
  "source": "+14255550100",
  "destination": {
    "type": "phone_number",
    "value": "+14255550123"
  }
}
```

Reference: [CreateTelephonyCallJobRequest](/python/api/azure-ai-projects/azure.ai.projects.models.createtelephonycalljobrequest).

Replace the connection, caller identity, and destination with your values. Add any required `structured_inputs`. Save the returned job ID and response headers.

### Read the call job

Use the returned job `id` as `{callJobId}`, or follow the `Location` URL:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/call_jobs/{callJobId}?api-version=v1
Authorization: Bearer <token>
Foundry-Features: VoiceAgents=V1Preview
```

Reference: [BetaVoiceAgentsTelephonyOperations.get_call_job](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

The response contains the job and its current `ETag`. Poll at the interval from the create response's `Retry-After`; don't assume each read returns that header.

### Cancel a call job

Read the job again, then send its latest `ETag` in `If-Match`. Use the job's ETag, not a binding's ETag. Send no request body:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/call_jobs/{callJobId}:cancel?api-version=v1
Authorization: Bearer <token>
Foundry-Features: VoiceAgents=V1Preview
If-Match: <etag-from-latest-call-job-read>
```

Reference: [BetaVoiceAgentsTelephonyOperations.cancel_call_job](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

---

### Interpret the job status

Inspect `status`, `attempt_count`, and `terminal_reason`. Terminal statuses are `completed`, `blocked`, `expired`, `failed`, and `cancelled`. Interpret the reason with the status: a queued job can retain a temporary dispatch-deferral reason.

Cancellation returns `202 Accepted` while pending, or `200 OK` when the job is terminal. Continue reading the job until it reaches a terminal status. Cancellation doesn't hang up a connected call; a cancellation request after connection can return `409 Conflict`.

A job ID isn't a live call ID. Don't pass it to `/telephony/calls/{callId}`.

### Optional outbound settings

Use these settings in the Python request model or REST JSON body. The SDK converts Python date and duration objects to the REST wire format.

| Optional setting | Usage |
| --- | --- |
| `purpose` | A description of why you're placing the call. |
| `structured_inputs` | Values available to the agent and its greeting. Declared inputs must match their schemas. |
| `schedule.not_before` | The earliest dispatch time. Use a timezone-aware `datetime.datetime` in Python or a Unix timestamp in seconds in REST. |
| `schedule.expires_at` | The time after which the job expires without dispatch. Use a timezone-aware `datetime.datetime` in Python or a Unix timestamp in seconds in REST. |
| `retry_policy` | Use a `fixed_interval` policy with `max_attempts` from 1 through 5, including the first attempt. Use `datetime.timedelta` for `interval` in Python or seconds in REST. Omit the policy for one attempt. |

For Python, use `TelephonyCallJobSchedule` and `TelephonyOutboundFixedIntervalRetryPolicy` to construct these optional values.

## Configure transfer to a person

An agent that can't complete a request should reach a human rather than end the call. Configure named transfer targets for the agent. These targets are separate from its telephony bindings.

The examples use PSTN targets, which work with either provider. Use destinations approved for your call flow.

# [Foundry portal](#tab/portal)

Select **Python SDK** or **REST** for the transfer-target configuration examples.

# [Python SDK](#tab/python)

Read the current target list and its ETag, and then replace the list. Include every target you want to keep. An empty list clears the target list.

```python
from azure.ai.projects.models import (
    PSTNTelephonyTransferDestination,
    TelephonyTransferTarget,
)
from azure.core import MatchConditions

targets, target_headers = telephony.get_transfer_targets(
    agent_name=agent_name,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
targets = telephony.replace_transfer_targets(
    agent_name=agent_name,
    transfer_targets=[
        TelephonyTransferTarget(
            name="billing",
            description="Billing and payment questions",
            destination=PSTNTelephonyTransferDestination(
                value="+14255550111"
            ),
        ),
        TelephonyTransferTarget(
            name="operator",
            description="A person at the front desk",
            destination=PSTNTelephonyTransferDestination(
                value="+14255550112"
            ),
        ),
    ],
    etag=target_headers["ETag"],
    match_condition=MatchConditions.IfNotModified,
)
```

Reference: [BetaVoiceAgentsTelephonyOperations](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Replace the example destinations with your approved targets.

# [REST](#tab/rest)

First, read the current target list and its `ETag` response header:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/transfer_targets?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Replace the target list with `PUT`, using the returned `ETag` in `If-Match`. Include every target you want to keep: this operation replaces the entire list, and an empty array clears it.

```http
PUT {projectEndpoint}/agents/{agentName}/telephony/transfer_targets?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json
If-Match: <etag-from-latest-transfer-targets-read>

{
  "transfer_targets": [
    {
      "name": "billing",
      "description": "Billing and payment questions",
      "destination": { "kind": "pstn", "value": "+14255550111" }
    },
    {
      "name": "operator",
      "description": "A person at the front desk",
      "destination": { "kind": "pstn", "value": "+14255550112" }
    }
  ]
}
```

---

Use these destination kinds for provider-specific routing:

| Destination `kind` | Value | Supported provider |
| --- | --- | --- |
| `pstn` | E.164 phone number. | Teams or Twilio. |
| `teams` | Teams user or resource-account GUID, optionally prefixed with `28:orgid:`. | Teams through Azure Communication Services. |
| `sip` | SIP or SIPS URI. | Twilio. |

There's no `twilio` destination kind. For Python, use `PSTNTelephonyTransferDestination`, `TeamsTelephonyTransferDestination`, or `SipTelephonyTransferDestination` for the corresponding destination.

Give each target a `description` that says when to use it. The agent chooses based on that text.

Transfer requests select a target from the agent's configured list rather than supplying an arbitrary destination.

## Manage a live call

These operations list and manage inbound calls. Use a live call ID, not an outbound job ID. Complete [Set up your preferred interface](#set-up-your-preferred-interface) before running the examples.

# [Foundry portal](#tab/portal)

Select **Python SDK** or **REST** to list calls or send a transfer or end-call request.

# [Python SDK](#tab/python)

List calls and select the ID of the active call you want to manage:

```python
for call in telephony.list_calls(agent_name=agent_name):
    print(call.id, call.status)
```

Reference: [BetaVoiceAgentsTelephonyOperations.list_calls](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

To transfer that call to the configured `operator` target:

```python
call_id = "<active-call-id>"
call = telephony.transfer_call(
    agent_name=agent_name, call_id=call_id, target="operator"
)
```

Reference: [BetaVoiceAgentsTelephonyOperations.transfer_call](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Alternatively, end an active call. Don't run this step on a call you want to keep connected:

```python
call_id = "<active-call-id>"
call = telephony.end_call(agent_name=agent_name, call_id=call_id)
```

Reference: [BetaVoiceAgentsTelephonyOperations.end_call](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

Both operations return the call record. Use `telephony.get_call(agent_name=agent_name, call_id=call_id)` to check its current status and lifecycle events.

# [REST](#tab/rest)

List the agent's calls, and use the service-generated call `id` as `{callId}` in subsequent requests:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/calls?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

To transfer an active call to the configured `operator` target:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}:transfer?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json

{ "target": "operator" }
```

To end an active call, send a separate request with no request body:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}:end?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Both operations return the call record. To inspect the call's current status and lifecycle events, use `GET {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}?api-version=v1`.

---

## Configure audio for phone calls

Phone networks carry narrowband audio, so tune the agent for the channel:

- Set `noise_reduction.type` to `azure_deep_noise_suppression` for contact center traffic.
- Increase `silence_duration_ms`. Callers on a phone pause more than callers at a keyboard.
- Add `phrase_list` hints for the identifiers callers read aloud, such as order or policy numbers.
- Attach the `end_conversation` system tool so the agent can end a completed call.

See [Configure a voice agent](configure-voice-agent.md).

## Test the call

1. Wait for the selected provider and binding changes to propagate. For Microsoft Teams, also allow time for Azure Communication Services and Event Grid propagation.
1. From a controlled caller, call the configured number.
1. Confirm the agent answers.
1. Complete a short conversation.
1. Interrupt the agent.
1. Use one safe tool or knowledge path.
1. Test the approved human-handoff behavior.
1. End the call.
1. Confirm that monitoring and trace data appear.

Record:

- Test timestamp and time zone.
- Called number.
- Callee identifier.
- Telephony provider and provider call ID, such as an Azure Communication Services correlation ID or Twilio Call SID.
- Agent name and version.
- For Microsoft Teams, the Azure Communication Services resource ID and Event Grid delivery result.
- For Twilio, the Foundry project connection name.

For an outbound test, create a job for an approved test recipient and record the job ID, status, attempt count, and reason. Don't treat `202 Accepted` as proof that the call connected.

<!-- Screenshot: Phone numbers card showing connected numbers and their actions menus. Alt text: "Voice-agent phone-number channel with connected numbers and provider badges." -->

## Trace phone calls

When a call arrives through telephony, the session's root trace span records the provider, the provider's call ID, and the dialed and calling numbers. You can correlate a Foundry session with a record in your telephony provider.

Caller and callee phone numbers are personal data. Review who can read your project's Application Insights resource before you enable content capture. See [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Troubleshoot telephony

| Symptom | What to check |
| --- | --- |
| Busy signal and no Azure Communication Services event | Teams number activation, license, PSTN connectivity, calling bot channel, TPE association, synchronization, and Azure Communication Services consent. |
| Azure Communication Services receives the call but Foundry reports no binding | Compare `IncomingCall.data.to.rawId` with `28:orgid:<resource_account_object_id>` constructed from the binding's GUID. Keep the prefix out of the REST binding field. |
| Event Grid validation fails | Endpoint, tenant, webhook audience, app-role assignment, delivery identity, and Event Grid write access. |
| Secure setup reports a Graph permission error | Ask a tenant administrator to grant the approved application-management permissions and retry. |
| Azure Communication Services `AnswerCall` returns 401 or 403 | Project connection target, project managed identity, Azure Communication Services role assignment, and RBAC propagation. |
| Call connects but is silent | Media endpoint reachability, selected model and voice, output device path, and required PCM media format. |
| Call disconnects unexpectedly | Callback reachability, media errors, service limits, and correlation logs. |
| The wrong agent answers | Confirm the agent that owns the binding collection and inspect that agent's active version. |
| The number doesn't appear after refresh | Query active bindings and confirm provisioning completed; don't rely only on temporary browser state. |
| Twilio numbers don't load | Check the connection's `Twilio` category, Account SID target, and `ApiKey` credential containing the current Primary Auth Token. Confirm that you can read the connection credentials. |
| No Twilio numbers can be selected | Confirm the Twilio account owns an active number with the Voice capability. |
| Twilio rejects the credentials | Update or recreate the project connection with the current Account SID and Primary Auth Token. |
| A Twilio number is already bound | Use the existing binding or disconnect it from the other agent before retrying. |
| A Twilio number doesn't reach the agent | Check that the number is active and voice-capable, its binding is active, and its voice URL points to Foundry. Review webhook delivery errors in Twilio. |
| A binding update, deletion, or transfer-target replacement fails with a precondition error | Read the resource again, review any concurrent changes, and use the latest `ETag` in `If-Match`. |
| Outbound creation returns `400 Bad Request` | Check `connection_name`, the provider-specific `source`, the E.164 destination, required structured inputs, and the `Idempotency-Key` header. |
| Outbound creation returns `409 Conflict` | The idempotency key was used with a different request. Reuse the original request to recover its job, or use a new key for a new call intent. |
| Outbound creation returns `503 Service Unavailable` with a dispatch-not-configured message | Outbound dispatch isn't configured for the service instance. Contact support to confirm availability; creating an inbound binding doesn't enable dispatch. |
| Call-job cancellation returns `409 Conflict` | Read the latest job and ETag. Retry with the current ETag only if the call hasn't connected and cancellation is still appropriate. |
| An outbound job is accepted but the destination doesn't ring | Read the job's status, attempt count, schedule, and reason. Check caller authorization and provider connectivity; `202 Accepted` isn't confirmation of a connected call. |

## Disconnect a number

Remove the inbound mapping when you no longer want the number to route calls to this agent. Outbound jobs don't require a binding; cancel any unwanted jobs separately.

# [Foundry portal](#tab/portal)

1. Open the agent **Channels** tab.
1. In **Phone numbers**, open the number's actions menu.
1. Select **Disconnect number**.
1. Confirm.

# [Python SDK](#tab/python)

Read the binding again and use its current ETag to delete it:

```python
from azure.core import MatchConditions

binding_id = "<binding-id>"
binding, binding_headers = telephony.get_binding(
    agent_name=agent_name,
    binding_id=binding_id,
    cls=lambda response, result, _: (result, response.http_response.headers),
)
telephony.delete_binding(
    agent_name=agent_name,
    binding_id=binding_id,
    etag=binding_headers["ETag"],
    match_condition=MatchConditions.IfNotModified,
)
```

Reference: [BetaVoiceAgentsTelephonyOperations.delete_binding](/python/api/azure-ai-projects/azure.ai.projects.operations.betavoiceagentstelephonyoperations).

The method returns `None` on success.

# [REST](#tab/rest)

Read the binding to get its current `ETag`, and then delete it by using that value in `If-Match`.  

```http
GET {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

```http
DELETE {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
If-Match: <etag-from-latest-binding-read>
```

A successful deletion returns `204 No Content`.

---

Disconnecting removes the Foundry binding. It doesn't:

- Release the Teams or Twilio number.
- Remove the Teams resource account.
- Delete Azure Communication Services.
- Remove the bot or app registration.
- Revoke Teams Phone extensibility consent.
- Delete the Twilio account or the Foundry project connection.

Coordinate upstream cleanup separately. For Twilio, review the number's voice routing before using it with another application.

## Security checklist

- Use Microsoft Entra authentication for Foundry API requests. Prefer managed identity for the Azure Communication Services connection.
- Don't share Azure Communication Services keys, connection strings, tokens, bot secrets, or portal cookies.
- Store the Twilio Auth Token in the project connection. If it's exposed, rotate it and update the connection.
- Confirm that the Twilio account owns each inbound number and authorizes each outbound caller number.
- For Teams inbound calls, validate that the Event Grid topic is the intended Azure Communication Services resource.
- Use the exact public Foundry project webhook endpoint.
- Keep webhook audience and Event Grid delivery identity concepts separate.
- Use a dedicated single-tenant webhook application when governance requires it.
- Don't persist service-generated call callback or media tokens.
- Confirm the binding target before update or deletion.
- Apply recording, consent, disclosure, retention, and privacy requirements.
- Prevent sensitive caller data from being read aloud or unnecessarily stored.

## Related content

Use these guides to configure and validate the agent behind your telephony channel:

- [Configure a voice agent](configure-voice-agent.md)
- [Publish and share a voice-based agent](voice-agent-channels-publish.md)
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md)
