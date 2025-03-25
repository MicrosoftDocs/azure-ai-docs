---
title: Verify a COCO annotation file
titleSuffix: Azure AI services
description: Use a Python script to verify your COCO file for custom model training.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.custom: devx-track-python
ms.topic: how-to
ms.date: 01/19/2024
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.author: pafarley
---

# Check the format of your COCO annotation file


[!INCLUDE [model-customization-deprecation](../includes/model-customization-deprecation.md)]

> [!TIP]
> This article is based on the Jupyter notebook *check_coco_annotation.ipynb*. **[Open in GitHub](https://github.com/Azure-Samples/cognitive-service-vision-model-customization-python-samples/blob/main/docs/check_coco_annotation.ipynb)**.

This guide demonstrates how to check if the format of your annotation file is correct. First, install the python samples package from the command line:

```python
pip install cognitive-service-vision-model-customization-python-samples
```

Then, run the following python code to check the file's format. You can either enter this code in a Python script, or run the [Jupyter Notebook](https://github.com/Azure-Samples/cognitive-service-vision-model-customization-python-samples/blob/main/docs/check_coco_annotation.ipynb) on a compatible platform.

```python
from cognitive_service_vision_model_customization_python_samples import check_coco_annotation_file, AnnotationKind, Purpose
import pathlib
import json

coco_file_path = pathlib.Path("{your_coco_file_path}")
annotation_kind = AnnotationKind.MULTICLASS_CLASSIFICATION # or AnnotationKind.OBJECT_DETECTION
purpose = Purpose.TRAINING # or Purpose.EVALUATION

check_coco_annotation_file(json.loads(coco_file_path.read_text()), annotation_kind, purpose)
```


## Use COCO file in a new project

Once your COCO file is verified, you're ready to import it to your model customization project. See [Create and train a custom model](model-customization.md) and go to the section on selecting/importing a COCO file&mdash;you can follow the guide from there to the end.

## Next step

> [!div class="nextstepaction"]
> [Create and train a custom model](model-customization.md)
