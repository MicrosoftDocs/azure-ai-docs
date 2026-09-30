Install the Speech SDK for JavaScript:

```bash
npm install microsoft-cognitiveservices-speech-sdk
```

Set the `SPEECH_KEY` and `SPEECH_REGION` environment variables. The following Node.js example synthesizes SSML to an MP3 file:

```javascript
const fs = require("fs");
const sdk = require("microsoft-cognitiveservices-speech-sdk");

const speechConfig = sdk.SpeechConfig.fromSubscription(
  process.env.SPEECH_KEY,
  process.env.SPEECH_REGION
);
speechConfig.speechSynthesisOutputFormat =
  sdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3;

const synthesizer = new sdk.SpeechSynthesizer(speechConfig);
const ssml = `
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1-Flash">
    Hello, this is a sample from MAI Voice.
  </voice>
</speak>`;

synthesizer.speakSsmlAsync(
  ssml,
  (result) => {
    fs.writeFileSync("output.mp3", Buffer.from(result.audioData));
    synthesizer.close();
  },
  (error) => {
    synthesizer.close();
    throw error;
  }
);
```

On success, an `output.mp3` file is saved to the current directory.
