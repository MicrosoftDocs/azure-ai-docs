---
title: "Scale to handle more enrolled users - Face"
titleSuffix: Azure AI services
description: This guide is an article on how to scale up from existing PersonGroup and FaceList objects to LargePersonGroup and LargeFaceList objects.
#services: cognitive-services
author: nitinme
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.topic: how-to
ms.date: 02/14/2024
ms.author: nitinme
ms.devlang: csharp
ms.custom:
  - devx-track-csharp
  - ignite-2023
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Scale to handle more enrolled users

[!INCLUDE [Gate notice](../includes/identity-gate-notice.md)]

This guide shows you how to scale up from existing **PersonGroup** and **FaceList** objects to **LargePersonGroup** and **LargeFaceList** objects, respectively. **PersonGroups** can hold up to 1000 persons in the free tier and 10,000 in the paid tier, while **LargePersonGroups** can hold up to one million persons in the paid tier.

> [!IMPORTANT]
> The newer data structure **PersonDirectory** is recommended for new development. It can hold up to 20 million identities and does not require manual training. For more information, see the [PersonDirectory guide](./use-persondirectory.md).

This guide demonstrates the migration process. It assumes a basic familiarity with **PersonGroup** and **FaceList** objects, the **Train** operation, and the face recognition functions. To learn more about these subjects, see the [face recognition](../concept-face-recognition.md) conceptual guide.

**LargePersonGroup** and **LargeFaceList** are collectively referred to as large-scale operations. **LargePersonGroup** can contain up to 1 million persons, each with a maximum of 248 faces. **LargeFaceList** can contain up to 1 million faces. The large-scale operations are similar to the conventional **PersonGroup** and **FaceList** but have some differences because of the new architecture. 

The samples are written in C#.

> [!NOTE]
> To enable Face search performance for **Identification** and **FindSimilar** in large-scale, introduce a **Train** operation to preprocess the **LargeFaceList** and **LargePersonGroup**. The training time varies from seconds to about half an hour based on the actual capacity. During the training period, it's possible to perform **Identification** and **FindSimilar** if a successful training operating was done before. The drawback is that the new added persons and faces don't appear in the result until a new post migration to large-scale training is completed.

## Step 1: Code migration

This section focuses on how to migrate **PersonGroup** or **FaceList** implementation to **LargePersonGroup** or **LargeFaceList**. Although **LargePersonGroup** or **LargeFaceList** differs from **PersonGroup** or **FaceList** in design and internal implementation, the API interfaces are similar for backward compatibility.

Data migration isn't supported. You re-create the **LargePersonGroup** or **LargeFaceList** instead.

### Migrate a PersonGroup to a LargePersonGroup

Migration from a **PersonGroup** to a **LargePersonGroup** is simple. They share exactly the same group-level operations.

For **PersonGroup** or person-related implementation, it's necessary to change only the API paths or SDK class/module to **LargePersonGroup** and **LargePersonGroup** **Person**.

Add all of the faces and persons from the **PersonGroup** to the new **LargePersonGroup**. For more information, see [Add faces](add-faces.md).

### Migrate a FaceList to a LargeFaceList

| **FaceList** APIs | **LargeFaceList** APIs |
|:---:|:---:|
| Create | Create |
| Delete | Delete |
| Get | Get |
| List | List |
| Update | Update |
| - | Train |
| - | Get Training Status |

The preceding table is a comparison of list-level operations between **FaceList** and **LargeFaceList**. As is shown, **LargeFaceList** comes with new operations, [Train](/rest/api/face/face-list-operations/train-large-face-list) and [Get Training Status](/rest/api/face/face-list-operations/get-large-face-list-training-status), when compared with **FaceList**. Training the **LargeFaceList** is a precondition of the 
[FindSimilar](/rest/api/face/face-recognition-operations/find-similar-from-large-face-list) operation. Training isn't required for **FaceList**. The following snippet is a helper function to wait for the training of a **LargeFaceList**:

```csharp
/// <summary>
/// Helper function to train LargeFaceList and wait for finish.
/// </summary>
/// <remarks>
/// The time interval can be adjusted considering the following factors:
/// - The training time which depends on the capacity of the LargeFaceList.
/// - The acceptable latency for getting the training status.
/// - The call frequency and cost.
///
/// Estimated training time for LargeFaceList in different scale:
/// -     1,000 faces cost about  1 to  2 seconds.
/// -    10,000 faces cost about  5 to 10 seconds.
/// -   100,000 faces cost about  1 to  2 minutes.
/// - 1,000,000 faces cost about 10 to 30 minutes.
/// </remarks>
/// <param name="largeFaceListId">The Id of the LargeFaceList for training.</param>
/// <param name="timeIntervalInMilliseconds">The time interval for getting training status in milliseconds.</param>
/// <returns>A task of waiting for LargeFaceList training finish.</returns>
private static async Task TrainLargeFaceList(
    string largeFaceListId,
    int timeIntervalInMilliseconds = 1000)
{
    HttpClient httpClient = new HttpClient();
    httpClient.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", SUBSCRIPTION_KEY);

    // Trigger a train call.
    await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/largefacelists/{largeFaceListId}/train", null);

    // Wait for training finish.
    while (true)
    {
        await Task.Delay(timeIntervalInMilliseconds);
        string? trainingStatus = null;
        using (var response = await httpClient.GetAsync($"{ENDPOINT}/face/v1.0/largefacelists/{largeFaceListId}/training"))
        {
            string contentString = await response.Content.ReadAsStringAsync();
            trainingStatus = (string?)(JsonConvert.DeserializeObject<Dictionary<string, object>>(contentString)?["status"]);
        }

        if ("running".Equals(trainingStatus))
        {
            continue;
        }
        else if ("succeeded".Equals(trainingStatus))
        {
            break;
        }
        else
        {
            throw new Exception("The train operation is failed!");
        }
    }
}
```

Previously, a typical use of **FaceList** with added faces and **FindSimilar** looked like the following:

```csharp
// Create a FaceList.
const string FaceListId = "myfacelistid_001";
const string FaceListName = "MyFaceListDisplayName";
const string ImageDir = @"/path/to/FaceList/images";
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["name"] = FaceListName, ["recognitionModel"] = "recognition_04" }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PutAsync($"{ENDPOINT}/face/v1.0/facelists/{FaceListId}", content);
}

// Add Faces to the FaceList.
Parallel.ForEach(
    Directory.GetFiles(ImageDir, "*.jpg"),
    async imagePath =>
    {
        using (Stream stream = File.OpenRead(imagePath))
        {
            using (var content = new StreamContent(stream))
            {
                content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
                await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/facelists/{FaceListId}/persistedfaces?detectionModel=detection_03", content);
            }
        }
    });

// Perform FindSimilar.
const string QueryImagePath = @"/path/to/query/image";
var results = new List<HttpResponseMessage>();
using (Stream stream = File.OpenRead(QueryImagePath))
{
    var response = await faceClient.DetectAsync(BinaryData.FromStream(stream), FaceDetectionModel.Detection03, FaceRecognitionModel.Recognition04, returnFaceId: true);
    var faces = response.Value;
    foreach (var face in faces)
    {
        using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["faceId"] = face.FaceId, ["faceListId"] = FaceListId }))))
        {
            content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            results.Add(await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/findsimilars", content));
        }
    }
}
```

When migrating it to **LargeFaceList**, it becomes the following:

```csharp
// Create a LargeFaceList.
const string LargeFaceListId = "mylargefacelistid_001";
const string LargeFaceListName = "MyLargeFaceListDisplayName";
const string ImageDir = @"/path/to/FaceList/images";
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["name"] = LargeFaceListName, ["recognitionModel"] = "recognition_04" }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PutAsync($"{ENDPOINT}/face/v1.0/largefacelists/{LargeFaceListId}", content);
}

// Add Faces to the LargeFaceList.
Parallel.ForEach(
    Directory.GetFiles(ImageDir, "*.jpg"),
    async imagePath =>
    {
        using (Stream stream = File.OpenRead(imagePath))
        {
            using (var content = new StreamContent(stream))
            {
                content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
                await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/largefacelists/{LargeFaceListId}/persistedfaces?detectionModel=detection_03", content);
            }
        }
    });

// Train() is newly added operation for LargeFaceList.
// Must call it before FindSimilar to ensure the newly added faces searchable.
await TrainLargeFaceList(LargeFaceListId);

// Perform FindSimilar.
const string QueryImagePath = @"/path/to/query/image";
var results = new List<HttpResponseMessage>();
using (Stream stream = File.OpenRead(QueryImagePath))
{
    var response = await faceClient.DetectAsync(BinaryData.FromStream(stream), FaceDetectionModel.Detection03, FaceRecognitionModel.Recognition04, returnFaceId: true);
    var faces = response.Value;
    foreach (var face in faces)
    {
        using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["faceId"] = face.FaceId, ["largeFaceListId"] = LargeFaceListId }))))
        {
            content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            results.Add(await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/findsimilars", content));
        }
    }
}
```

As previously shown, the data management and the **FindSimilar** part are almost the same. The only exception is that a fresh preprocessing **Train** operation must complete in the **LargeFaceList** before **FindSimilar** works.

## Step 2: Train suggestions

Although the **Train** operation speeds up [FindSimilar](/rest/api/face/face-recognition-operations/find-similar-from-large-face-list)
and [Identification](/rest/api/face/face-recognition-operations/identify-from-large-person-group), the training time suffers, especially when coming to large scale. The estimated training time in different scales is listed in the following table.

| Scale for faces or persons | Estimated training time |
|:---:|:---:|
| 1,000 | 1-2 sec |
| 10,000 | 5-10 sec |
| 100,000 | 1-2 min |
| 1,000,000 | 10-30 min |

To better utilize the large-scale feature, we recommend the following strategies.

### Step 2a: Customize time interval

As is shown in `TrainLargeFaceList()`, there's a time interval in milliseconds to delay the infinite training status checking process. For **LargeFaceList** with more faces, using a larger interval reduces the call counts and cost. Customize the time interval according to the expected capacity of the **LargeFaceList**.

The same strategy also applies to **LargePersonGroup**. For example, when you train a **LargePersonGroup** with 1 million persons, `timeIntervalInMilliseconds` might be 60,000, which is a 1-minute interval.

### Step 2b: Small-scale buffer

Persons or faces in a **LargePersonGroup** or a **LargeFaceList** are searchable only after being trained. In a dynamic scenario, new persons or faces are constantly added and must be immediately searchable, yet training might take longer than desired. 

To mitigate this problem, use an extra small-scale **LargePersonGroup** or **LargeFaceList** as a buffer only for the newly added entries. This buffer takes a shorter time to train because of the smaller size. The immediate search capability on this temporary buffer should work. Use this buffer in combination with training on the master **LargePersonGroup** or **LargeFaceList** by running the master training on a sparser interval. Examples are in the middle of the night and daily.

An example workflow:

1. Create a master **LargePersonGroup** or **LargeFaceList**, which is the master collection. Create a buffer **LargePersonGroup** or **LargeFaceList**, which is the buffer collection. The buffer collection is only for newly added persons or faces.
1. Add new persons or faces to both the master collection and the buffer collection.
1. Only train the buffer collection with a short time interval to ensure that the newly added entries take effect.
1. Call Identification or **FindSimilar** against both the master collection and the buffer collection. Merge the results.
1. When the buffer collection size increases to a threshold or at a system idle time, create a new buffer collection. Trigger the **Train** operation on the master collection.
1. Delete the old buffer collection after the **Train** operation finishes on the master collection.

### Step 2c: Standalone training

If a relatively long latency is acceptable, it isn't necessary to trigger the **Train** operation right after you add new data. Instead, the **Train** operation can be split from the main logic and triggered regularly. This strategy is suitable for dynamic scenarios with acceptable latency. It can be applied to static scenarios to further reduce the **Train** frequency.

Suppose there's a `TrainLargePersonGroup` function similar to `TrainLargeFaceList`. A typical implementation of the standalone training on a **LargePersonGroup** by invoking the [`Timer`](/dotnet/api/system.timers.timer) class in `System.Timers` is:

```csharp
private static void Main()
{
    // Set up standalone training at regular intervals.
    const int TimeIntervalForStatus = 1000 * 60; // 1-minute interval for getting training status.
    const double TimeIntervalForTrain = 1000 * 60 * 60; // 1-hour interval for training.
    var trainTimer = new Timer(TimeIntervalForTrain);
    trainTimer.Elapsed += (sender, args) => TrainTimerOnElapsed("mylargepersongroupid_001", TimeIntervalForStatus);
    trainTimer.AutoReset = true;
    trainTimer.Enabled = true;

    // Other operations like creating persons, adding faces, and identification, except for Train.
    // ...
}

private static void TrainTimerOnElapsed(string largePersonGroupId, int timeIntervalInMilliseconds)
{
    TrainLargePersonGroup(largePersonGroupId, timeIntervalInMilliseconds).Wait();
}
```

For more information about data management and identification-related implementations, see [Add faces](add-faces.md).

## Summary

In this guide, you learned how to migrate the existing **PersonGroup** or **FaceList** code, not data, to the **LargePersonGroup** or **LargeFaceList**:

- **LargePersonGroup** and **LargeFaceList** work similar to **PersonGroup** or **FaceList**, except that the **Train** operation is required by **LargeFaceList**.
- Take the proper **Train** strategy to dynamic data update for large-scale data sets.

## Next steps

Follow a how-to guide to learn how to add faces to a **PersonGroup** or write a script to do the **Identify** operation on a **PersonGroup**.

- [Add faces](add-faces.md)
- [Face client library quickstart](../quickstarts-sdk/identity-client-library.md)
