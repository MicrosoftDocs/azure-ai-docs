# Speech Service How-To Pivot Audit
Generated: 2026-04-09

---

## 1. Missing Pivots by Feature Area

Standard expected pivot set: `cli.md`, `cpp.md`, `csharp.md`, `go.md`, `java.md`, `javascript.md`, `objectivec.md`, `python.md`, `rest.md`, `swift.md`

UI-only features are excluded — they intentionally use Speech Studio / AI Foundry tabs instead of SDK pivots.

| Feature Area | Status | Missing Pivots | Notes |
|---|---|---|---|
| audio-content-creation | <span style="color:gray">UI-only</span> | — | — |
| compressed-audio-input | <span style="color:green">COMPLETE</span> | — | — |
| custom-avatar | <span style="color:gray">UI-only</span> | — | — |
| custom-speech | <span style="color:red">**INCOMPLETE**</span> | cpp, csharp, go, java, javascript, objectivec, python, rest, swift | only cli-api-kind.md present |
| diagnostics | <span style="color:red">**INCOMPLETE**</span> | cli, go, javascript, rest, swift | — |
| meeting-transcription | <span style="color:red">**INCOMPLETE**</span> | cli, cpp, go, java, objectivec, rest, swift | only csharp, javascript, python present |
| post-processing | <span style="color:green">COMPLETE</span> | — | — |
| professional-voice | <span style="color:gray">UI-only</span> | — | — |
| recognize-speech | <span style="color:green">COMPLETE</span> | — | — |
| recognize-speech-results | <span style="color:red">**INCOMPLETE**</span> | rest | — |
| speech-synthesis | <span style="color:green">COMPLETE</span> | — | — |
| text-to-speech-avatar | <span style="color:gray">UI-only</span> | — | — |
| translate-speech | <span style="color:green">COMPLETE</span> | — | — |
| video-translation | <span style="color:gray">UI-only</span> | — | — |
| voice-live-agents | <span style="color:red">**INCOMPLETE**</span> | cli, cpp, go, objectivec, rest, swift | — |
| voice-live-proactive-and-pregenerated-messages | <span style="color:red">**INCOMPLETE**</span> | cli, cpp, go, java, javascript, objectivec, rest, swift | — |

---

## 2. Pivot Files That Claim the Feature Is Unsupported

These are cases where a pivot file exists (there is a tab for the language) but the file explicitly states the SDK does not support the feature.

### <span style="color:orange">Flagged — has a tab but claims unsupported</span>

| File | Line | Unsupported Claim |
|---|---|---|
| compressed-audio-input/javascript.md | 12 | "The Speech SDK for JavaScript does not support compressed audio." |
| compressed-audio-input/swift.md | 11 | "The Speech SDK for Swift does not support compressed audio." |
| compressed-audio-input/objectivec.md | 11 | "The Speech SDK for Objective-C does not support compressed audio." |

### Other "unsupported" mentions — no action needed

| File | Line | Notes |
|---|---|---|
| recognize-speech/javascript.md | 36 | Node.js microphone caveat — legitimate env-level note |
| audio-content-creation/speech-studio.md | 16 | Foundry resource type limitation in UI |
| professional-voice/train-voice/speech-studio.md | 236 | Voice training method limitation |
| professional-voice/train-voice/ai-foundry.md | 241 | Same as above |
| professional-voice/deploy-endpoint/speech-studio.md | 27 | Regional availability note |
| professional-voice/deploy-endpoint/ai-foundry.md | 30 | Same as above |
| compressed-audio-input/gstreamer-android.md | 55 | Makefile build error string, not a docs claim |

---

## 3. Summary

- <span style="color:red">**6 feature areas**</span> have incomplete pivot coverage: custom-speech, diagnostics, meeting-transcription, recognize-speech-results, voice-live-agents, voice-live-proactive-and-pregenerated-messages
- <span style="color:orange">**3 pivot files**</span> have a tab but claim unsupported — all in compressed-audio-input: JavaScript, Swift, Objective-C
- All other "unsupported" mentions are context-appropriate — no action needed
