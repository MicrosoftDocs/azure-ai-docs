Install the [Speech SDK for Python](../../../quickstarts/setup-platform.md?pivots=programming-language-python), and set the `SPEECH_KEY` and `SPEECH_REGION` environment variables.

The following example synthesizes SSML to an MP3 file:

```python
import os

import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ["SPEECH_KEY"],
    region=os.environ["SPEECH_REGION"],
)
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
)
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.mp3")
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config,
)

ssml = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1-Flash">
    Hello, this is a sample from MAI Voice.
  </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml).get()
if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
    raise RuntimeError(f"Speech synthesis failed: {result.reason}")
```

On success, an `output.mp3` file is saved to the current directory.
