---
title: Switch models and inference providers at runtime
titleSuffix: Microsoft Agent Framework
description: Understand when an agent can switch models or inference providers during a conversation without losing context.
zone_pivot_groups: programming-languages
author: westey-m
ms.topic: article
ms.author: westey
ms.date: 08/28/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Switch models and inference providers at runtime

Applications can use models from different inference services for different
turns of a conversation. For example, an application might change models based
on user choice, model capabilities, availability, or cost.

Changing the destination for the next request is only one part of routing. The
new model also needs the prior conversation to continue with the same context.
Whether it can receive that context depends on where the chat history is stored
and who controls it.

## Chat history storage determines portability

Inference services support different approaches to conversation state. Some
APIs expect the caller to provide the relevant message history with every
request. Other APIs store the conversation in the inference service and let the
caller continue it by passing an identifier.

| History model | Where the messages are stored | What the caller sends |
|---|---|---|
| Caller-managed | In application-controlled memory or durable storage | The relevant message history plus any new messages with each request |
| Inference-service-managed | In storage controlled by the inference service | A service-specific conversation or response identifier, plus any new messages. |

Some inference services support both approaches through different APIs or options. For example, OpenAI responses has the `store` parameter which you can set to `true` for inference-service-managed chat history, and to `false` for caller-managed.

## Caller-managed history supports routing

When the caller manages history, it has access to the messages from earlier
turns. A router can select another model or inference service, and the caller
can send those messages with the next request.

The history doesn't have to remain in process memory. It can come from
application-owned durable storage, as long as the application can load it and
send it to the selected service. The destination must also support the message
content and features used earlier in the conversation.

## Inference-service–managed history limits routing

When an inference service manages history, it is the source of truth for the conversation. The caller typically retains an opaque identifier instead of the messages themselves.

That identifier refers to state held by the originating service. Access can also depend on the account or project, endpoint, and credentials used to create the conversation. A client for another service can't use the identifier to retrieve the messages. Another client for the same service might also be unable to access the conversation if it uses a different scope.

A service might support changing models within one of its own stored conversations. That behavior is specific to the service and isn't portable routing. A general router can't transfer the service-side conversation to another provider without first retrieving or reconstructing the messages.

| Routing scenario | History model | Result |
|---|---|---|
| Switch between models from one provider | Caller-managed | The caller can replay the history to the new model. The new model must support the message and content types used in earlier turns. |
| Switch between different inference providers | Caller-managed | The caller can replay the history to the new provider. The new provider must accept the roles, content types, tool-call messages, and tool-result messages used in earlier turns. |
| Change models within one service-side conversation | Inference-service-managed | The switch works only if the inference service lets the existing conversation continue with the new model. The routing client can't enable this behavior. |
| Switch to a different inference service | Inference-service-managed | The new service can't access the original service's conversation identifier. Retrieve or reconstruct the messages, and start the new route with caller-managed history. |

For more information about these storage models, see [Storage](conversations/storage.md).

## How Agent Framework implements runtime routing

::: zone pivot="programming-language-csharp"

Agent Framework can provide the caller-managed history needed for portable
routing. In this routing pattern, a chat history provider is the source of truth
for the conversation. It can store messages in the agent session or in
application-owned storage.

In Agent Framework, caller-managed history includes local session state and
custom chat history storage. Inference-service-managed history corresponds to
service-managed storage.

For a `ChatClientAgent`, a routing chat client sits in the chat-client layer of
the [agent pipeline](agent-pipeline.md). The agent and its session remain the
same while the routing client selects one of several named `IChatClient`
instances for each request.

A routed request follows this sequence:

1. The chat history provider loads the conversation history.
1. The agent combines the history with the input for the current turn.
1. The routing client selects the active chat client for the session.
1. The selected client receives the complete request.
1. The chat history provider stores the new messages after the run.

Because the selected client receives the history loaded by the provider, the
application can change routes without manually rebuilding the conversation.

The .NET SDK provides the experimental
`RoutePersistingRoutingChatClient`. Set the initial route with
`RoutePersistingRoutingChatClientOptions.DefaultRoute`, inspect a session's
route with `GetActiveRoute`, and change it with `SetActiveRoute`. If you don't
set a default route, the client uses the first route provided at construction.

More routing clients exist in `Microsoft.Extensions.AI` that allow further
routing strategies.

See the
[multi-model routing sample](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/Agents/Agent_Step24_MultiModelRouting)
for a complete C# implementation.

> [!IMPORTANT]
> Every chat client registered as a route must use caller-managed history
> supplied by a chat history provider. The provider can store that history in
> the session or in application-owned storage. Don't register a route that uses
> inference-service-managed conversation history.

::: zone-end

::: zone pivot="programming-language-python"

Python support is not currently available.

::: zone-end

::: zone pivot="programming-language-go"

Go support is not currently available.

::: zone-end

## Next steps

> [!div class="nextstepaction"]
> [Create a custom agent](custom-agents.md)

## Related content

- [Agent pipeline architecture](agent-pipeline.md)
- [Session](conversations/session.md)
- [Storage](conversations/storage.md)
- [Model providers](../../integrations/by-component/model-providers/index.md)
