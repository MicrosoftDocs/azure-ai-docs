---
title: Make predictions with AutoML ONNX Model in .NET
description: Learn how to make predictions using an AutoML ONNX model in .NET with ML.NET.
titleSuffix: Azure Machine Learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.date: 02/11/2026
ms.topic: how-to
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.custom: automl, devx-track-dotnet
#customer intent: As a data scientist, I want to learn how to make predictions using an AutoML ONNX model with ML.NET, so I can make predictions in .NET ecosystem applications.

---

# Make predictions using an AutoML ONNX model in .NET

In this article, you learn how to use an Azure Machine Learning AutoML Open Neural Network Exchange (ONNX) model to make predictions in a C# console application using ML.NET. [ML.NET](/dotnet/machine-learning/) is an open-source, cross-platform, machine learning framework for the .NET ecosystem that lets you train and consume custom machine learning models. ML.NET supports a code-first approach like C# or F#, or low-code tooling like [Model Builder](/dotnet/machine-learning/automate-training-with-model-builder) and the [ML.NET CLI](/dotnet/machine-learning/automate-training-with-cli).

The ML.NET framework is extensible so you can use other popular machine learning frameworks like TensorFlow and ONNX. [ONNX](https://onnx.ai/) is an open-source format for AI models that supports interoperability between frameworks. You can train a model in a popular machine learning framework like PyTorch, convert it into ONNX format, and consume the ONNX model in a different framework like ML.NET.

## Prerequisites

- [.NET 6 SDK or later](https://dotnet.microsoft.com/download).
- A command shell and text editor or an IDE such as [Visual Studio](https://visualstudio.microsoft.com/vs/) or [Visual Studio Code](https://code.visualstudio.com/Download).
- An ONNX model. You can follow the [NYC taxi data regression notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/2c_nyc_taxi_data_regression/nyc_taxi_data_regression.ipynb) to create an example model.
- Optionally, a tool like [`Netron`](https://github.com/lutzroeder/netron) to inspect the ONNX model.

## Create a C# console application

This example uses the [.NET CLI](/dotnet/core/tools/) to build your application. You can also use Visual Studio or another IDE.

1. Open a new terminal and create a new C# .NET console application named `AutoMLONNXConsoleApp`. A directory with that name is created for your application.

   ```console
   dotnet new console -o AutoMLONNXConsoleApp
   ```

1. Change to the *AutoMLONNXConsoleApp* directory.

    ```console
    cd AutoMLONNXConsoleApp
    ```

## Add software packages

ML.NET provides an API that uses the [ONNX runtime](https://github.com/Microsoft/onnxruntime) for predictions. The **Microsoft.ML**, **Microsoft.ML.OnnxRuntime**, and **Microsoft.ML.OnnxTransformer** NuGet packages contain the dependencies required to use an ONNX model in a .NET application.

1. Install the packages.

   ```dotnetcli
   dotnet add package Microsoft.ML
   dotnet add package Microsoft.ML.OnnxRuntime
   dotnet add package Microsoft.ML.OnnxTransformer
   ```

1. Edit the *Program.cs* file to add the following `using` directives at the top.

   ```csharp
   using System.Linq;
   using Microsoft.ML;
   using Microsoft.ML.Data;
   using Microsoft.ML.Transforms.Onnx;
   ```

## Add a reference to the ONNX model

Add a reference to your ONNX model file to your application. One way for the application to access the ONNX model is through the build output directory. For more information about MSBuild common items, see the [MSBuild guide](/visualstudio/msbuild/common-msbuild-project-items).

1. Copy your ONNX model and paste it into your application's *AutoMLONNXConsoleApp* root directory.
1. Edit the *AutoMLONNXConsoleApp.csproj* file to add the following code inside the `Project` node. In this case, the name of the ONNX model file is *automl-model.onnx*.

   ```xml
   <ItemGroup>
       <None Include="automl-model.onnx">
           <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
       </None>
   </ItemGroup>
   ```

1. Edit the *Program.cs* file to add the following line inside the `Program` class.

   ```csharp
   static string ONNX_MODEL_PATH = "automl-model.onnx";
   ```

1. Create a new instance of [`MLContext`](xref:Microsoft.ML.MLContext) in the `Main` method of the `Program` class.

   ```csharp
   MLContext mlContext = new MLContext();
   ```

The [`MLContext`](xref:Microsoft.ML.MLContext) class is a starting point for all ML.NET operations. Initializing `mlContext` creates a new ML.NET environment that can be shared across the model lifecycle. The class is conceptually similar to <xref:Microsoft.EntityFrameworkCore.DbContext> in Entity Framework.

## Define the model data schema

A model expects input and output data in a specific format. ML.NET lets you define the format of your data via classes. The following table shows a sample from a model that uses data from the NYC Taxi Trip dataset.

| vendor_id | rate_code | passenger_count | trip_time_in_secs | trip_distance | payment_type | fare_amount |
|-----------|-----------|-----------------|-------------------|---------------|--------------|-------------|
| `VTS`       | 1         | 1               | 1140              | 3.75          | `CRD`          | 15.5        |
| `VTS`       | 1         | 1               | 480               | 2.72          | `CRD`          | 10.0        |
| `VTS`       | 1         | 1               | 1680              | 7.8           | `CSH`          | 26.5        |

### Inspect the ONNX model

 If you don't already know what your data format looks like, you can use a tool like `Netron` to inspect the ONNX model. To use `Netron` to inspect your model's inputs and outputs:

1. Open `Netron`.
1. In the top menu bar, select **File** > **Open** and use the file browser to select your model.
1. Your model opens. For example, the structure of the `automl-model.onnx` model looks like the following screenshot:

   :::image type="content" source="media/how-to-use-automl-onnx-model-dotnet/netron-automl-onnx-model.png" alt-text="Screenshot showing a `Netron` AutoML ONNX Model." lightbox="media/how-to-use-automl-onnx-model-dotnet/netron-automl-onnx-model.png":::

1. Select the last node at the bottom of the graph, `variable_out1` in this case, to display the model's metadata. The inputs and outputs on the sidebar show you the model's expected inputs, outputs, and data types. Use this information to define the input and output schema of your model.

### Define model input schema

In your *Program.cs* file, create a new class called `OnnxInput` with the following properties:

```csharp
public class OnnxInput
{
    [ColumnName("vendor_id")]
    public string VendorId { get; set; }

    [ColumnName("rate_code"),OnnxMapType(typeof(Int64),typeof(Single))]
    public Int64 RateCode { get; set; }

    [ColumnName("passenger_count"), OnnxMapType(typeof(Int64), typeof(Single))]
    public Int64 PassengerCount { get; set; }

    [ColumnName("trip_time_in_secs"), OnnxMapType(typeof(Int64), typeof(Single))]
    public Int64 TripTimeInSecs { get; set; }

    [ColumnName("trip_distance")]
    public float TripDistance { get; set; }

    [ColumnName("payment_type")]
    public string PaymentType { get; set; }
}
```

### Use data attributes

Each property maps to a column in the dataset. The properties are further annotated with attributes.

- The [`ColumnName`](xref:Microsoft.ML.Data.ColumnNameAttribute) attribute lets you specify how ML.NET should reference the column when it operates on the data. For example, although the `TripDistance` property follows standard .NET naming conventions, the model only has a column or feature called `trip_distance`. To address this naming discrepancy, the [`ColumnName`](xref:Microsoft.ML.Data.ColumnNameAttribute) attribute maps the `TripDistance` property to the column or feature named `trip_distance`.

- For numerical values, ML.NET operates only on [`Single`](xref:System.Single) value types, but the original data types of some of the columns are integers. The [`OnnxMapType`](xref:Microsoft.ML.Transforms.Onnx.OnnxMapTypeAttribute) attribute maps types between ONNX and ML.NET.

For more information about data attributes, see the [ML.NET load data guide](/dotnet/machine-learning/how-to-guides/load-data-ml-net).

### Define model output schema

Once the data is processed, it produces an output of a certain format. To define your data output schema, create a new class called `OnnxOutput` in the *Program.cs* file with the following properties:

```csharp
public class OnnxOutput
{
    [ColumnName("variable_out1")]
    public float[] PredictedFare { get; set; }
}
```

Similar to `OnnxInput`, use the [`ColumnName`](xref:Microsoft.ML.Data.ColumnNameAttribute) attribute to map the `variable_out1` output to the more descriptive name `PredictedFare`.

## Define a prediction pipeline

A pipeline in ML.NET is typically a series of chained transformations that operate on the input data to produce an output. For more information about data transformations, see the [ML.NET data transformation guide](/dotnet/machine-learning/resources/transforms).

1. Create a new method called `GetPredictionPipeline` inside the `Program` class.

   ```csharp
   static ITransformer GetPredictionPipeline(MLContext mlContext)
   {
   
   }
   ```

1. To define the input and output column names, add the following code inside the `GetPredictionPipeline` method.

   ```csharp
   var inputColumns = new string []
   {
       "vendor_id", "rate_code", "passenger_count", "trip_time_in_secs", "trip_distance", "payment_type"
   };
   
   var outputColumns = new string [] { "variable_out1" };
   ```

1. Add code that defines your pipeline. An [`IEstimator`](xref:Microsoft.ML.IEstimator%601) provides a blueprint of the operations and the input and output schemas of your pipeline.

   ```csharp
   var onnxPredictionPipeline =
       mlContext
           .Transforms
           .ApplyOnnxModel(
               outputColumnNames: outputColumns,
               inputColumnNames: inputColumns,
               ONNX_MODEL_PATH);
   ```

   In this case, [`ApplyOnnxModel`](xref:Microsoft.ML.OnnxCatalog.ApplyOnnxModel%2A) is the only transform in the pipeline, which takes in the names of the input and output columns and the path to the ONNX model file.

1. An [`IEstimator`](xref:Microsoft.ML.IEstimator%601) only defines the set of operations to apply to your data. Use the `Fit` method to create an [`ITransformer`](xref:Microsoft.ML.ITransformer) from your `onnxPredictionPipeline` to operate on your data.

   ```csharp
   var emptyDv = mlContext.Data.LoadFromEnumerable(new OnnxInput[] {});
   
   return onnxPredictionPipeline.Fit(emptyDv);
   ```

   The [`Fit`](xref:Microsoft.ML.IEstimator%601.Fit%2A) method expects an [`IDataView`](xref:Microsoft.ML.IDataView) input to perform the operations on. An [`IDataView`](xref:Microsoft.ML.IDataView) represents data in ML.NET using a tabular format. In this case, the pipeline is only for predictions, so you can provide an empty [`IDataView`](xref:Microsoft.ML.IDataView) to give the [`ITransformer`](xref:Microsoft.ML.ITransformer) the necessary input and output schema information. The fitted [`ITransformer`](xref:Microsoft.ML.ITransformer) is then returned for further use in your application.

   > [!TIP]
   > This sample defines and uses the pipeline within the same application. However, it's best to use separate applications to define and use your pipeline for predictions. In ML.NET, your pipelines can be serialized and saved for further use in other .NET end-user applications.
   >
   > ML.NET supports various deployment targets, such as desktop applications, web services, and WebAssembly applications. For more information about saving pipelines, see the [ML.NET save and load trained models guide](/dotnet/machine-learning/how-to-guides/save-load-machine-learning-models-ml-net).

1. Inside the `Main` method, call the `GetPredictionPipeline` method with the required parameters.

   ```csharp
   var onnxPredictionPipeline = GetPredictionPipeline(mlContext);
   ```

## Use the model to make predictions

Now that you have a pipeline, you can use it to make predictions. ML.NET provides a convenience API for making predictions on a single data instance called [`PredictionEngine`](xref:Microsoft.ML.PredictionEngine%602).

1. Inside the `Main` method, create a [`PredictionEngine`](xref:Microsoft.ML.PredictionEngine%602) by using the [`CreatePredictionEngine`](xref:Microsoft.ML.ModelOperationsCatalog.CreatePredictionEngine%2A) method.

   ```csharp
   var onnxPredictionEngine = mlContext.Model.CreatePredictionEngine<OnnxInput, OnnxOutput>(onnxPredictionPipeline);
   ```

1. Create a test data input.

   ```csharp
   var testInput = new OnnxInput
   {
       VendorId = "CMT",
       RateCode = 1,
       PassengerCount = 1,
       TripTimeInSecs = 1271,
       TripDistance = 3.8f,
       PaymentType = "CRD"
   };
   ```

1. Use the `onnxPredictionEngine` to make predictions based on the new `testInput` data using the [`Predict`](xref:Microsoft.ML.PredictionEngineBase%602.Predict%2A) method.

   ```csharp
   var prediction = onnxPredictionEngine.Predict(testInput);
   ```

1. Write the result of your prediction to the console.

   ```csharp
   Console.WriteLine($"Predicted Fare: {prediction.PredictedFare.First()}");
   ```

1. Use the .NET CLI to run your application.

   ```dotnetcli
   dotnet run
   ```

   The result should look similar to the following output:

   ```Output
   Predicted Fare: 15.621523
   ```

For more information about making predictions in ML.NET, see [Use a model to make predictions](/dotnet/machine-learning/how-to-guides/machine-learning-model-predictions-ml-net).

## Related content

- [Deploy your model as an ASP.NET Core Web API](/dotnet/machine-learning/how-to-guides/serve-model-web-api-ml-net)
- [Deploy your model as a serverless .NET Azure Function](/dotnet/machine-learning/how-to-guides/serve-model-serverless-azure-functions-ml-net)
