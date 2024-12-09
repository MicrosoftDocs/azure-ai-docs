---
author: PatrickFarley
ms.service: azure-ai-custom-vision
ms.topic: include
ms.date: 05/22/2023
ms.author: pafarley
---

## Create environment variables 

In this example, you'll write your credentials to environment variables on the local machine running the application.

[!INCLUDE [find key and endpoint](./find-key.md)]

To set the environment variables, open a console window and follow the instructions for your operating system and development environment. 

- To set the `VISION_TRAINING KEY` environment variable, replace `<your-training-key>` with one of the keys for your training resource.
- To set the `VISION_TRAINING_ENDPOINT` environment variable, replace `<your-training-endpoint>` with the endpoint for your training resource.
- To set the `VISION_PREDICTION_KEY` environment variable, replace `<your-prediction-key>` with one of the keys for your prediction resource.
- To set the `VISION_PREDICTION_ENDPOINT` environment variable, replace `<your-prediction-endpoint>` with the endpoint for your prediction resource.
- To set the `VISION_PREDICTION_RESOURCE_ID` environment variable, replace `<your-resource-id>` with the resource ID for your prediction resource.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

#### [Windows](#tab/windows)

```console
setx VISION_TRAINING_KEY <your-training-key>
```

```console
setx VISION_TRAINING_ENDPOINT <your-training-endpoint>
```

```console
setx VISION_PREDICTION_KEY <your-prediction-key>
```

```console
setx VISION_PREDICTION_ENDPOINT <your-prediction-endpoint>
```

```console
setx VISION_PREDICTION_RESOURCE_ID <your-resource-id>
```

After you add the environment variables, you might need to restart any running programs that read the environment variables, including the console window.

#### [Linux](#tab/linux)

```bash
export VISION_TRAINING_KEY=<your-training-key>
```

```bash
export VISION_TRAINING_ENDPOINT=<your-training-endpoint>
```

```bash
export VISION_PREDICTION_KEY=<your-prediction-key>
```

```bash
export VISION_PREDICTION_ENDPOINT=<your-prediction-endpoint>
```

```bash
export VISION_PREDICTION_RESOURCE_ID=<your-resource-id>
```

After you add the environment variables, run `source ~/.bashrc` from your console window to make the changes effective.

---
