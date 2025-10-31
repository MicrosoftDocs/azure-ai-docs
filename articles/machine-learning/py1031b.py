from azure.ai.ml import automl
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import Input, Output 

my_train_data_input = Input(
    type=AssetTypes.MLTABLE,
    path="./train_data"
)

my_test_data_input = Input(
    type=AssetTypes.URI_FOLDER,
    path='./test_data',
)
pipeline_job = forecasting_train_and_evaluate_factory(
    my_train_data_input,
    my_test_data_input,
    target_column_name,
    time_column_name,
    forecast_horizon
)

# Set pipeline-level compute.
pipeline_job.settings.default_compute = compute_name

# Submit pipeline job.
returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name
)
returned_pipeline_job