Use this voice name for MAI-Voice-2.1-Flash:

```xml
<voice name="en-US-Harper:MAI-Voice-2.1-Flash">
```

The same suffix applies to any supported prebuilt voice.

### Basic SSML

The following example uses Harper with MAI-Voice-2.1-Flash:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1-Flash">
    Hello world. This is a sample from MAI Voice.
  </voice>
</speak>
```

### Multilingual SSML

The following SSML synthesizes a greeting in Spanish (Mexico) by using `es-MX-Valeria:MAI-Voice-2.1-Flash`.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="es-MX">
  <voice name="es-MX-Valeria:MAI-Voice-2.1-Flash">
    Hola, esta es una muestra de MAI Voice 2.1 Flash.
  </voice>
</speak>
```

### Expressive control with SSML `mstts:express-as`

Use the `style` and `styledegree` attributes to control expression:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2.1-Flash">
    <mstts:express-as style="happiness" styledegree="1.2">
      Welcome to Microsoft Build. MAI Voice 2.1 Flash supports multilingual expressive synthesis.
    </mstts:express-as>
  </voice>
</speak>
```
