---
 author: PatrickFarley
 ms.service: azure-ai-custom-vision
 ms.topic: include
 ms.date: 07/17/2019
 ms.author: pafarley
---

As a minimum, you should use at least 30 images per tag in the initial training set. You should also collect a few extra images to test your model after it's trained.

In order to train your model effectively, use images with visual variety. Select images that vary by:
* camera angle
* lighting
* background
* visual style
* individual/grouped subject(s)
* size
* type

Additionally, make sure all of your training images meet the following criteria:
* must be .jpg, .png, .bmp, or .gif format
* no greater than 6 MB in size (4 MB for prediction images)
* no less than 256 pixels on the shortest edge; any images shorter than 256 pixels are automatically scaled up by the Custom Vision service
