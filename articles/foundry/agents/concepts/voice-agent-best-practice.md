---
title: "Best practices for voice-based agents"
description: "Design guidance and production readiness practices for building reliable voice-based agents in Microsoft Foundry."
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 09/25/2026
ms.custom: preview
ai-usage: ai-assisted
---

# Best practices for voice-based agents

This article shows the design, security, and operational practices that matter most when you build, test, secure, and release a voice-based agent in Microsoft Foundry Agent Service.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Design for latency first

Perceived responsiveness is the difference between a natural conversation and an awkward one. Time to first audio, not total response time, is what a caller experiences.

- **Emit a response quickly.** Configure `interim_response` so the agent speaks while it waits on a slow tool. Prefer `static_interim_response`, which adds no model latency. Reserve `llm_interim_response` for cases where the filler must reflect context. Never let an interim phrase imply that an action already completed.
- **Tune the trigger threshold.** `latency_threshold_ms` defaults to 2000 milliseconds. In practice, silence becomes noticeable well before that, so lower it for conversational scenarios.
- **Cap output.** Set `max_output_tokens`. A shorter answer starts and finishes sooner and is less likely to be interrupted.
- **Prefer speech-to-speech for conversation.** A native real-time model fuses audio understanding and generation into one step. A cascaded pipeline adds separate recognition and synthesis stages, which is the right trade only when model and voice flexibility, custom voices, specific locales, or transcription control outweigh the added stages.
- **Keep context focused.** Trim instructions and retrieved context to what each turn needs. Long prompts and large retrieved payloads slow every response.
- **Keep tool inventories small and fast.** Every attached tool adds context to every turn, which costs latency on all of them, not just the turn that calls the tool. Prefer fast tools.
- **Monitor time to first audio and stage latency after every release.**

## Make turn-taking feel natural

Turn detection determines when the agent believes the caller finishes. Getting it wrong is the most common cause of a bad-sounding agent.

- Increase `silence_duration_ms` when callers think out loud, read numbers from paperwork, or aren't speaking their first language. Reduce it for quick lookups where speed matters more than patience.
- Raise `threshold` in noisy environments so background speech doesn't trigger a turn.
- Use a semantic turn detection type when callers pause mid-sentence, so natural thought completion isn't cut short. Silence-based detection can't tell a thinking pause from a finished thought.
- Use basic detection when acoustic thresholds must be tuned directly.
- Change one turn-detection setting at a time so you can attribute each behavior change.
- Leave `interrupt_response` enabled. Being able to interrupt is what makes an agent feel like a conversation partner rather than a recording.
- Match `noise_reduction` to the channel: `near_field` for headsets and handsets, `far_field` for speakerphones and rooms, and `azure_deep_noise_suppression` for contact centers.
- Test the hard cases: short answers such as "yes," "no," and a single digit; hesitant speech and long pauses; and interruptions at the beginning, middle, and end of a response.
- Provide a clear recovery path after repeated no-input or no-match events.

## Write for the ear

Spoken output has different constraints from text output. See [Optimize voice agent instructions](../how-to/optimize-voice-agent-instructions.md) for the full guidance. The essentials:

- One or two sentences per turn, then stop and let the caller talk.
- Put the answer first, then any qualifications.
- One question at a time. Compound questions get partial answers.
- No markdown, bullets, headings, tables, raw URLs, or long menus.
- Numbers, currency, dates, abbreviations, and identifiers spoken as natural words.
- Break complex tasks into confirmed steps, and offer to repeat or summarize.
- Don't force callers to remember more than a few choices.
- An opening greeting that names two or three concrete capabilities and ends with an open question.

## Improve recognition

Recognition errors are one of the most common causes of failed voice turns. Product names, place names, and identifiers are the words most often transcribed wrong.

- Select only the likely languages, and set a default language for the primary audience.
- Add a focused `phrase_list` for products, people, and locations, or use a custom speech model for domain vocabulary.
- Test accents, speaking rates, quiet speech, noise, and telephone audio.
- Compare input audio with the trace transcript to find systematic misrecognitions.
- Use noise suppression and echo cancellation only after device testing.
- Provide a confirmation step for values that are easy to misrecognize.

## Choose a voice responsibly

- Test the voice with actual domain content, including long numbers, names, abbreviations, and legal statements.
- Confirm language, locale, and model compatibility.
- Set a speaking rate that stays understandable.
- Use custom lexicons for approved pronunciation requirements.
- Follow consent and disclosure requirements for custom voices.
- Don't imitate a real person without the required rights and approvals.

## Use avatars appropriately

- Treat the avatar as a browser visual layer, not a telephony capability.
- Verify regional availability and pricing.
- Test synchronization at expected network quality.
- Provide an audio-only experience that remains complete on its own.
- Avoid relying on gestures or visual text to communicate required information.
- Follow custom-avatar consent and responsible AI requirements.

## Design tools for spoken interaction

- **Return small results.** A tool that returns a large object forces the model to summarize it aloud. Return only the fields the caller needs.
- **Choose response scheduling deliberately.** `when_idle` is the default and suits most cases. Use `interrupt` only when the result invalidates what the agent is currently saying. Use `silent` for side effects such as logging that shouldn't produce speech.
- **Handle failures out loud.** Instruct the agent to say a tool failed and offer to retry or transfer. Silence after a failed call sounds like a dropped connection. Define explicit failure behavior for each tool.
- **Make operations idempotent where possible,** so a retry after an interruption or timeout doesn't duplicate an action.
- **Never fabricate.** Require the agent to state only what its tools return. A caller has no screen on which to catch an invented confirmation number.
- **Add `end_conversation`.** Attach the system tool and tell the agent when to use it, so completed calls end instead of idling.

## Handle interruptions and recovery

When a caller interrupts, the agent's turn ends early and the conversation context is truncated to what was actually heard. Design for that:

- Put the answer first and the qualifications after. If a caller interrupts, they should already have the useful part.
- Expect that the agent's own record of the turn is the truncated text, not what the model generated. Don't write instructions that assume the agent remembers something the caller never heard.
- Treat a rising barge-in rate as a signal that responses are too long, and shorten them before you adjust detection settings.

## Design human handoff

Decide the handoff design explicitly:

- Which intents require a person.
- What the agent says before transfer.
- What context can be passed.
- What happens when no person is available.
- Emergency and crisis boundaries.
- Whether the caller can request a person at any time.

Don't claim a transfer succeeded until the downstream system confirms it.

## Protect callers and data

- **Verify before disclosing.** Make identity verification a guardrail, and gate account tools behind it. Require confirmation before high-impact actions.
- **Authenticate securely.** Use managed identity or approved Microsoft Entra authentication, and apply least privilege.
- **Never expose secrets.** Don't put keys, tokens, connection strings, or SAS URLs in instructions, transcripts, screenshots, or source control, and don't read secrets or complete sensitive records aloud.
- **Provide required notices and consent.** Give required AI, recording, and monitoring notices, and obtain consent where required.
- **Keep `store` off by default.** It defaults to `false`. Enable it for the conversations you intend to review, and remember that it persists audio as well as transcripts.
- **Treat trace content capture as a privacy decision.** Transcripts and audio references aren't captured by default. Decide which audio, transcript, trace, and tool fields are necessary, and restrict Application Insights and protected-table access, because anyone who can read the project's Application Insights resource can read captured content once it's there.
- **Control audio and retention.** Set retention according to legal and business requirements, and control audio download.
- **Avoid using live sensitive conversations as broad evaluation datasets.**
- **Plan for deletion.** Deleting a conversation cascades to its responses, items, and audio. Define deletion and subject-request procedures, and build them into your data lifecycle rather than adding them later.
- **Decide storage ownership early.** With bring-your-own-storage, access to recordings is governed by Azure RBAC on your storage account, independently of who can access the agent. Migrating later is harder than choosing correctly now.
- **Log enough correlation data to investigate without collecting unnecessary content.**

## Test across channels

Browser and telephone audio differ, and each channel exposes different failures. Test:

- Typed test flows hide transcription errors, filler words, and interruptions, so test with real audio.
- Failure paths where a tool times out, verification fails, and the caller interrupts mid-answer. These paths reach callers more often than they reach test plans.
- Built-in and external microphones, and speakers and headsets.
- Preview web app access with a non-developer account.
- Teams resource-account numbers and Twilio voice-capable numbers.
- Quiet and noisy environments.
- Mobile and poor network conditions.
- DTMF expectations, if part of the upstream telephony design.
- Session reconnect and unexpected disconnect.
- The same agent version across each channel.

## Validate quality with evidence

- **Iterate in the playground** for rapid testing, and then use trace transcripts and audio for root-cause analysis.
- **Watch the right signals.** Monitor metrics for sessions, turns, errors, tools, tokens, and latency. Track time to first audio, barge-in rate, and session outcome. Rising `idle_timeout` or `client_abort` outcomes usually mean callers are giving up.
- **Evaluate transcripts continuously.** Use agent evaluators for intent resolution, tool-call accuracy, and task adherence, plus safety evaluators. Rerun them on every version. Use full-conversation evaluation and controlled scenario datasets that include failures and edge cases.
- Text conversation evaluators don't replace human review of pronunciation, prosody, interruption, or acoustic quality.

## Release safely

Every change creates a new immutable version. Test a new version against the endpoint's version override before you make it active, and keep the previous version available for rollback.

1. Save a version.
1. Test the complete scenario matrix.
1. Review traces.
1. Run supported evaluations.
1. Confirm roles and identities.
1. Confirm pricing and quota.
1. Validate browser and telephone channels.
1. Record the released version.
1. Monitor the rollout.
1. Keep a tested rollback version.

## Production readiness checklist

- [ ] Preview terms and support boundaries are accepted.
- [ ] Region and model availability are confirmed.
- [ ] Instructions are optimized for listening.
- [ ] Recognition and turn detection pass the scenario matrix.
- [ ] Voice and avatar approvals are complete.
- [ ] Tools use least privilege and safe confirmation.
- [ ] Human handoff is tested.
- [ ] AI, recording, privacy, and consent notices are approved.
- [ ] Application Insights access and retention are configured.
- [ ] Monitoring alerts and investigation ownership are defined.
- [ ] Evaluation uses representative existing conversations.
- [ ] Preview web app access is tested with intended users.
- [ ] Phone-number security and provider callbacks are validated, including Event Grid delivery for Teams inbound calls.
- [ ] Model, Speech, avatar, telephony-provider, and monitoring costs are reviewed.
- [ ] A versioned rollback plan exists.

## Related content

- [Configure a voice agent](../how-to/configure-voice-agent.md)
- [Optimize voice agent instructions](../how-to/optimize-voice-agent-instructions.md)
- [Voice agent tracing, monitoring, and evaluation](voice-agent-observability.md)
- [Pricing for voice-based agents](voice-agent-pricing.md)
- [Integrate a telephony channel](../how-to/voice-agent-telephony-channels.md)
