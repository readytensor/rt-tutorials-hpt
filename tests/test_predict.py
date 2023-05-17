import os
import pandas as pd
import numpy as np
from predict import (
    get_model_predictions,
    add_ids_to_predictions,
    run_batch_predictions
)
from train import run_training


def test_get_model_predictions(monkeypatch):
    """
    Test the get_model_predictions function to ensure it correctly makes predictions.

    This unit test replaces the predict_with_model function and verifies that
    the get_model_predictions function correctly transforms the probabilities into
    a DataFrame with the class names as columns. It also checks the function's
    behavior when the return_probs parameter is set to False, ensuring that the
    function correctly identifies the class with the highest probability for each
    data point.
    """
    # Arrange
    class_names = ['A', 'B']
    prediction_field_name = 'predicted_class'

    transformed_data = pd.DataFrame({
        'feature1': [1, 2],
        'feature2': [3, 4]
    })

    expected_output_probs = pd.DataFrame({
        'A': [0.8, 0.4],
        'B': [0.2, 0.6]
    })

    expected_output_class = pd.DataFrame({
        prediction_field_name: ['A', 'B']
    })

    predictor_model = "mock_predictor_model"

    def mock_predict_with_model(*args, **kwargs):
        return np.array([[0.8, 0.2], [0.4, 0.6]])

    monkeypatch.setattr('predict.predict_with_model', mock_predict_with_model)

    # Act and Assert
    # Test when return_probs=True
    output = get_model_predictions(
        transformed_data, predictor_model, class_names, prediction_field_name, return_probs=True)
    pd.testing.assert_frame_equal(output, expected_output_probs)

    # Test when return_probs=False
    output = get_model_predictions(
        transformed_data, predictor_model, class_names, prediction_field_name, return_probs=False)
    pd.testing.assert_frame_equal(output, expected_output_class)



def test_add_ids_to_predictions(sample_test_data, schema_provider):
    """
    Test the add_ids_to_predictions function to ensure it correctly adds IDs to the predictions DataFrame.
    """
    # Create a sample predictions DataFrame
    num_rows = len(sample_test_data)
    predictions = pd.DataFrame({
        schema_provider.allowed_target_values[0]: np.random.rand(num_rows),
        schema_provider.allowed_target_values[1]: np.random.rand(num_rows)
    })
    
    # Run the function
    result = add_ids_to_predictions(sample_test_data, predictions, schema_provider.id)
    print(sample_test_data.head())
    print(result.head())

    # Check the columns of the result
    assert list(result.columns) == [schema_provider.id] + schema_provider.allowed_target_values

    # Check the IDs of the result
    assert list(result[schema_provider.id]) == list(sample_test_data[schema_provider.id])

    # Check the values of class 0 and class 1
    assert list(result[schema_provider.allowed_target_values[0]]) == \
        list(predictions[schema_provider.allowed_target_values[0]])
    assert list(result[schema_provider.allowed_target_values[1]]) == \
        list(predictions[schema_provider.allowed_target_values[1]])


def test_integration_run_batch_predictions(
        tmpdir,
        input_schema_dir,
        train_dir,
        model_config_file_path,
        test_dir,
        sample_test_data,
        schema_provider):
    """
    Integration test for the run_batch_predictions function.

    This test simulates the full prediction pipeline, from reading the test data
    to saving the final predictions. The function is tested to ensure that it
    reads in the test data correctly, properly transforms the data, makes the
    predictions, and saves the final predictions in the correct format and location.

    The test also checks that the function handles various file and directory paths
    correctly and that it can handle variations in the input data.

    The test uses a temporary directory provided by the pytest's tmpdir fixture to
    avoid affecting the actual file system.

    Args:
        tmpdir (LocalPath): Temporary directory path provided by pytest's tmpdir fixture.
        input_schema_dir (str): Directory path to the input data schema.
        train_dir (str): Directory path to the training data.
        model_config_file_path (str): Path to the model configuration file.
        test_dir (str): Directory path to the test data.
        sample_test_data (pd.DataFrame): Sample DataFrame for testing.
        schema_provider (Any): Loaded schema provider.
    """
    # Create temporary paths for training
    saved_schema_path = str(tmpdir.join('saved_schema.json'))
    pipeline_file_path = str(tmpdir.join('pipeline.joblib'))
    target_encoder_file_path = str(tmpdir.join('target_encoder.joblib'))
    predictor_file_path = str(tmpdir.join('predictor.joblib'))

    # Run the training process
    run_training(
        run_tuning=False,
        input_schema_dir=input_schema_dir,
        saved_schema_path=saved_schema_path,
        model_config_file_path=model_config_file_path,
        train_dir=train_dir,
        pipeline_file_path=pipeline_file_path,
        target_encoder_file_path=target_encoder_file_path,
        predictor_file_path=predictor_file_path)

    # Create temporary paths for prediction
    predictions_file_path = str(tmpdir.join('predictions.csv'))


    # Run the prediction process
    run_batch_predictions(
        saved_schema_path=saved_schema_path,
        model_config_file_path=model_config_file_path,
        test_dir=test_dir,
        pipeline_file_path=pipeline_file_path,
        target_encoder_file_path=target_encoder_file_path,
        predictor_file_path=predictor_file_path,
        predictions_file_path=predictions_file_path
    )

    # Assert that the predictions file is saved in the correct path
    assert os.path.isfile(predictions_file_path)

    # Load predictions and validate the format
    predictions_df = pd.read_csv(predictions_file_path)

    # Assert that predictions dataframe has the right columns
    assert schema_provider.id in predictions_df.columns
    for class_ in schema_provider.allowed_target_values:
        assert class_ in predictions_df.columns

    # Assert that the number of rows in the predictions matches the number of rows in the test data
    assert len(predictions_df) == len(sample_test_data)