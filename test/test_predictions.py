import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score

from bikeshare_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_no_predictions = 179

    # When
    # Get a single row from the test data
    single_test_input = sample_input_data[0].iloc[0].to_dict()
    result = make_prediction(input_data=single_test_input)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == 1
    
    # Get actual value
    y_true = sample_input_data[1].iloc[0]
    
    # Calculate absolute error
    mae = mean_absolute_error([y_true], predictions)
    
    # Print values for debugging
    print(f"Predicted value: {predictions[0]}")
    print(f"Actual value: {y_true}")
    print(f"Mean Absolute Error: {mae}")
    
    # Assert that the absolute error is within a reasonable range
    # Adjust this threshold based on your model's typical performance
    assert mae < 100  # Allow prediction to be off by at most 100 bikes