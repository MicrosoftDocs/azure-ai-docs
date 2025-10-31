from azure.ai.ml import Input, Output
my_train_data_input = Input(
    type=AssetTypes.MLTABLE,
    path='./train_data'
)

my_test_data_input = Input(
    type=AssetTypes.URI_FOLDER,
    path='./test_data'
)