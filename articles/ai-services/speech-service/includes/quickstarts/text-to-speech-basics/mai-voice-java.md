Install the [Speech SDK for Java](../../../quickstarts/setup-platform.md?pivots=programming-language-java), and set the `SPEECH_KEY` and `SPEECH_REGION` environment variables.

The following example synthesizes SSML to an MP3 file:

```java
import com.microsoft.cognitiveservices.speech.ResultReason;
import com.microsoft.cognitiveservices.speech.SpeechConfig;
import com.microsoft.cognitiveservices.speech.SpeechSynthesisOutputFormat;
import com.microsoft.cognitiveservices.speech.SpeechSynthesisResult;
import com.microsoft.cognitiveservices.speech.SpeechSynthesizer;
import java.nio.file.Files;
import java.nio.file.Path;

public class MaiVoiceSynthesis {
    public static void main(String[] args) throws Exception {
        SpeechConfig speechConfig = SpeechConfig.fromSubscription(
            System.getenv("SPEECH_KEY"),
            System.getenv("SPEECH_REGION")
        );
        speechConfig.setSpeechSynthesisOutputFormat(
            SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
        );

        String ssml = """
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
              <voice name="en-US-Harper:MAI-Voice-2.1">
                Hello, this is a sample from MAI Voice.
              </voice>
            </speak>
            """;

        try (SpeechSynthesizer synthesizer = new SpeechSynthesizer(speechConfig);
             SpeechSynthesisResult result = synthesizer.SpeakSsmlAsync(ssml).get()) {
            if (result.getReason() != ResultReason.SynthesizingAudioCompleted) {
                throw new IllegalStateException(
                    "Speech synthesis failed: " + result.getReason()
                );
            }
            Files.write(Path.of("output.mp3"), result.getAudioData());
        } finally {
            speechConfig.close();
        }
    }
}
```

On success, an `output.mp3` file is saved to the current directory.
