pipeline_job = many_models_train_evaluate_factory(
    train_data_input=Input(
        type="uri_folder",
        path="./train_data"
    ),
    test_data_input=Input(
        type="uri_folder",
        path="./test_data"
    ),
    automl_config=Input(
        type="uri_file",
        path="./automl_settings_mm.yml"
    ),
    compute_name="cpu-compute"
)
pipeline_job.settings.default_compute = "cpu-compute"

returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name,
)
ml_client.jobs.stream(returned_pipeline_job.name)