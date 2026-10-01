Install the [Speech SDK for C#](../../../quickstarts/setup-platform.md?pivots=programming-language-csharp), and set the `SPEECH_KEY` and `SPEECH_REGION` environment variables.

The following example synthesizes SSML to an MP3 file:

```csharp
using System;
using System.IO;
using Microsoft.CognitiveServices.Speech;

var speechConfig = SpeechConfig.FromSubscription(
    Environment.GetEnvironmentVariable("SPEECH_KEY"),
    Environment.GetEnvironmentVariable("SPEECH_REGION")
);
speechConfig.SetSpeechSynthesisOutputFormat(
    SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
);

using var synthesizer = new SpeechSynthesizer(speechConfig);
const string ssml = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1-Flash">
    Hello, this is a sample from MAI Voice.
  </voice>
</speak>
""";

using var result = await synthesizer.SpeakSsmlAsync(ssml);
if (result.Reason != ResultReason.SynthesizingAudioCompleted)
{
    throw new InvalidOperationException($"Speech synthesis failed: {result.Reason}");
}

await File.WriteAllBytesAsync("output.mp3", result.AudioData);
```

On success, an `output.mp3` file is saved to the current directory.
