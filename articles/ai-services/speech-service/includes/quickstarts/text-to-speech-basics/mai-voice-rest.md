Send an SSML `POST` request to the `cognitiveservices/v1` endpoint of your Speech resource.

Set these environment variables:

```bash
export SPEECH_KEY="<your-speech-resource-key>"
export SPEECH_REGION="<your-speech-resource-region>"
```

Run the following command:

```azurecli
curl -X POST \
  "https://${SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1" \
  --header "Content-Type: application/ssml+xml" \
  --header "X-Microsoft-OutputFormat: audio-24khz-160kbitrate-mono-mp3" \
  --header "Ocp-Apim-Subscription-Key: ${SPEECH_KEY}" \
  --data '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1">
    Hello, this is a sample from MAI Voice.
  </voice>
</speak>' \
  --output output.mp3
```

On success, an `output.mp3` file is saved to the current directory.
