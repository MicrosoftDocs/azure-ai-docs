from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Get credential to access azureml registry.
try:
    credential = DefaultAzureCredential()
    # Check whether token can be obtained.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential if DefaultAzureCredential fails.
    credential = InteractiveBrowserCredential()

# Get HTS training component.
hts_train_component = ml_client_registry.components.get(
    name='automl_hts_training',
    version='latest'
)

# Get HTS inference component.
hts_inference_component = ml_client_registry.components.get(
    name='automl_hts_inference',
    version='latest'
)

# Get component to compute evaluation metrics.
compute_metrics_component = ml_client_metrics_registry.components.get(
    name="compute_metrics",
    label="latest"
)

@pipeline(description="AutoML HTS Forecasting Pipeline")
def hts_train_evaluate_factory(
    train_data_input,
    test_data_input,
    automl_config_input,
    max_concurrency_per_node=4,
    parallel_step_timeout_in_seconds=3700,
    max_nodes=4,
    forecast_mode="rolling",
    forecast_step=1,
    forecast_level="SKU",
    allocation_method='proportions_of_historical_average'
):
    hts_train = hts_train_component(
        raw_data=train_data_input,
        automl_config=automl_config_input,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        max_nodes=max_nodes
    )
    hts_inference = hts_inference_component(
        raw_data=test_data_input,
        max_nodes=max_nodes,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        optional_train_metadata=hts_train.outputs.run_output,
        forecast_level=forecast_level,
        allocation_method=allocation_method,
        forecast_mode=forecast_mode,
        step=forecast_step
    )
    compute_metrics_node = compute_metrics_component(
        task="tabular-forecasting",
        prediction=hts_inference.outputs.evaluation_data,
        ground_truth=hts_inference.outputs.evaluation_data,
        evaluation_config=hts_inference.outputs.evaluation_configs
    )

    # Return metrics results from rolling evaluation.
    return {
        "metrics_result": compute_metrics_node.outputs.evaluation_result
    }